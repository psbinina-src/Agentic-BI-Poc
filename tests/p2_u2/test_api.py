from __future__ import annotations

from pathlib import Path

import duckdb
import pytest
from fastapi.testclient import TestClient

from p2_u2.api import create_app


@pytest.fixture
def api_client(tmp_path: Path) -> TestClient:
    gold_dir = tmp_path / "gold"
    gold_dir.mkdir()
    duckdb.sql(
        "SELECT * FROM (VALUES "
        "('L1', 'O1', 'P1', 'C1', DATE '2025-01-01', 'Online', 2, 10.00, 0.0, 20.00, 0.00, CAST(20.00 AS DECIMAL(18,6))), "
        "('L2', 'O2', 'P2', 'C2', DATE '2025-01-02', 'Retail', 1, 15.00, 0.0, 15.00, 0.00, 15.00), "
        "('L3', 'O3', 'P1', 'C1', DATE '2025-01-03', 'Online', 1, 5.00, 0.0, 5.00, 0.00, 5.00)"
        ") AS sales(order_line_id, order_id, product_id, customer_id, order_date, channel, quantity, "
        "unit_price, discount_rate, gross_sales_amount, discount_amount, net_sales_amount)"
    ).write_parquet(str(gold_dir / "sales_gold.parquet"))
    duckdb.sql(
        "SELECT * FROM (VALUES ('C1', 'Plus', 'North'), ('C2', 'Standard', 'South')) "
        "AS customers(customer_id, customer_segment, region)"
    ).write_parquet(str(gold_dir / "customers_gold.parquet"))
    return TestClient(create_app(gold_dir))


def test_catalog_and_dataset_details(api_client: TestClient) -> None:
    catalog = api_client.get("/catalog").json()

    assert {dataset["name"] for dataset in catalog["datasets"]} == {
        "sales_gold",
        "customers_gold",
        "products_gold",
        "inventory_gold",
    }
    assert next(dataset for dataset in catalog["datasets"] if dataset["name"] == "sales_gold")["available"] is True
    assert {
        (relationship["from_dataset"], relationship["to_dataset"])
        for relationship in catalog["relationships"]
    } >= {("sales_gold", "customers_gold"), ("sales_gold", "products_gold")}

    details = api_client.get("/catalog/sales_gold")
    assert details.status_code == 200
    payload = details.json()
    assert payload["grain"] == "One row per completed order line."
    assert payload["key_fields"] == ["order_line_id"]
    assert {field["name"]: field["type"] for field in payload["fields"]}["net_sales_amount"] == "DECIMAL(18,6)"
    assert next(field for field in payload["fields"] if field["name"] == "net_sales_amount")["description"]


def test_query_supports_projection_filters_and_bounded_results(api_client: TestClient) -> None:
    response = api_client.post(
        "/query",
        json={
            "dataset": "sales_gold",
            "fields": ["order_id", "channel", "net_sales_amount"],
            "filters": [{"field": "channel", "operator": "eq", "value": "Online"}],
            "order_by": [{"field": "net_sales_amount", "direction": "desc"}],
            "limit": 1,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["columns"] == ["order_id", "channel", "net_sales_amount"]
    assert payload["rows"] == [{"order_id": "O1", "channel": "Online", "net_sales_amount": 20.0}]
    assert payload["row_count"] == 1
    assert payload["truncated"] is True


def test_query_supports_safe_grouped_aggregation(api_client: TestClient) -> None:
    response = api_client.post(
        "/query",
        json={
            "dataset": "sales_gold",
            "group_by": ["channel"],
            "aggregations": [{"field": "net_sales_amount", "function": "sum"}],
            "order_by": [{"field": "sum_net_sales_amount", "direction": "desc"}],
        },
    )

    assert response.status_code == 200
    assert response.json()["limit"] == 100
    assert response.json()["rows"] == [
        {"channel": "Online", "sum_net_sales_amount": 25.0},
        {"channel": "Retail", "sum_net_sales_amount": 15.0},
    ]


def test_query_accepts_iso_date_filters(api_client: TestClient) -> None:
    response = api_client.post(
        "/query",
        json={
            "dataset": "sales_gold",
            "fields": ["order_id", "order_date"],
            "filters": [{"field": "order_date", "operator": "gte", "value": "2025-01-02"}],
            "order_by": [{"field": "order_date", "direction": "asc"}],
        },
    )

    assert response.status_code == 200
    assert response.json()["rows"] == [
        {"order_id": "O2", "order_date": "2025-01-02"},
        {"order_id": "O3", "order_date": "2025-01-03"},
    ]


def test_query_uses_only_documented_gold_relationships(api_client: TestClient) -> None:
    response = api_client.post(
        "/query",
        json={
            "dataset": "sales_gold",
            "joins": ["customers_gold"],
            "group_by": ["customers_gold.region"],
            "aggregations": [{"field": "sales_gold.net_sales_amount", "function": "sum"}],
            "order_by": [{"field": "customers_gold.region", "direction": "asc"}],
        },
    )
    unsupported = api_client.post(
        "/query",
        json={"dataset": "sales_gold", "joins": ["inventory_gold"], "fields": ["order_id"]},
    )

    assert response.status_code == 200
    assert response.json()["rows"] == [
        {"customers_gold.region": "North", "sum_sales_gold_net_sales_amount": 25.0},
        {"customers_gold.region": "South", "sum_sales_gold_net_sales_amount": 15.0},
    ]
    assert unsupported.status_code == 422


def test_query_rejects_unknown_fields_datasets_sql_and_large_limits(api_client: TestClient) -> None:
    bad_field = api_client.post("/query", json={"dataset": "sales_gold", "fields": ["channel; DROP TABLE sales_gold"]})
    bad_dataset = api_client.post("/query", json={"dataset": "other_table", "fields": ["channel"]})
    sql_input = api_client.post("/query", json={"dataset": "sales_gold", "sql": "SELECT * FROM sales_gold"})
    large_limit = api_client.post("/query", json={"dataset": "sales_gold", "fields": ["channel"], "limit": 501})

    assert bad_field.status_code == 422
    assert bad_dataset.status_code == 404
    assert sql_input.status_code == 422
    assert large_limit.status_code == 422


def test_unavailable_dataset_details_return_not_found(api_client: TestClient) -> None:
    assert api_client.get("/catalog/unknown").status_code == 404
    assert api_client.get("/catalog/products_gold").status_code == 404

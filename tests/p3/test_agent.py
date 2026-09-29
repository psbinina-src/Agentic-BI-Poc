from __future__ import annotations

import json
from types import SimpleNamespace

import httpx
import pytest
from fastapi.testclient import TestClient

from p3_agent.agent import ChartProposal, Phase3Agent
from p3_agent.api import create_app


CATALOG = {
    "datasets": [
        {"name": "sales_gold", "available": True},
        {"name": "customers_gold", "available": True},
        {"name": "products_gold", "available": True},
        {"name": "inventory_gold", "available": True},
    ],
    "relationships": [
        {"from_dataset": "sales_gold", "to_dataset": "customers_gold"},
        {"from_dataset": "sales_gold", "to_dataset": "products_gold"},
        {"from_dataset": "inventory_gold", "to_dataset": "products_gold"},
    ],
}

DETAILS = {
    "sales_gold": {
        "key_fields": ["order_line_id"],
        "fields": [
            {"name": "order_line_id", "type": "VARCHAR"},
            {"name": "order_date", "type": "DATE"},
            {"name": "customer_id", "type": "VARCHAR"},
            {"name": "net_sales_amount", "type": "DECIMAL(18,6)"},
            {"name": "channel", "type": "VARCHAR"},
        ],
    },
    "customers_gold": {
        "key_fields": ["customer_id"],
        "fields": [
            {"name": "customer_id", "type": "VARCHAR"},
            {"name": "region", "type": "VARCHAR"},
            {"name": "customer_segment", "type": "VARCHAR"},
        ],
    },
    "inventory_gold": {
        "key_fields": ["snapshot_date", "product_id"],
        "fields": [
            {"name": "snapshot_date", "type": "DATE"},
            {"name": "product_id", "type": "VARCHAR"},
            {"name": "inventory_on_hand", "type": "INTEGER"},
            {"name": "sales_velocity_units_per_day", "type": "DOUBLE"},
            {"name": "stock_coverage_days", "type": "DOUBLE"},
            {"name": "low_stock_flag", "type": "BOOLEAN"},
        ],
    },
    "products_gold": {
        "key_fields": ["product_id"],
        "fields": [
            {"name": "product_id", "type": "VARCHAR"},
            {"name": "product_name", "type": "VARCHAR"},
            {"name": "category", "type": "VARCHAR"},
            {"name": "subcategory", "type": "VARCHAR"},
        ],
    },
}


def make_agent() -> Phase3Agent:
    def respond(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/catalog":
            return httpx.Response(200, json=CATALOG)
        if request.url.path.startswith("/catalog/"):
            dataset = request.url.path.rsplit("/", 1)[-1]
            return httpx.Response(200, json=DETAILS[dataset])
        if request.url.path == "/query":
            return httpx.Response(
                200,
                json={
                    "dataset": "sales_gold",
                    "columns": ["customers_gold.region", "sum_sales_gold_net_sales_amount"],
                    "rows": [
                        {"customers_gold.region": "North", "sum_sales_gold_net_sales_amount": 1200.0},
                        {"customers_gold.region": "West", "sum_sales_gold_net_sales_amount": 900.0},
                    ],
                    "row_count": 2,
                    "limit": 20,
                    "truncated": False,
                },
            )
        return httpx.Response(404)

    return Phase3Agent(api_key="test-key", http_client=httpx.Client(transport=httpx.MockTransport(respond)))


def test_query_validator_accepts_catalogue_joins_and_aggregate_fields() -> None:
    agent = make_agent()
    request = agent._validate_query({
        "dataset": "sales_gold",
        "joins": ["customers_gold"],
        "group_by": ["region"],
        "aggregations": [{"field": "sales_gold.net_sales_amount", "function": "sum"}],
        "order_by": [{"field": "sum_net_sales_amount", "direction": "desc"}],
        "filters": [],
        "limit": 20,
    })
    assert request["joins"] == ["customers_gold"]
    assert request["limit"] == 20
    assert request["order_by"][0]["field"] == "sum_sales_gold_net_sales_amount"

    full_alias = agent._validate_query({
        "dataset": "sales_gold",
        "joins": ["customers_gold"],
        "group_by": ["region"],
        "aggregations": [{"field": "net_sales_amount", "function": "sum"}],
        "order_by": [{"field": "sum_sales_gold_net_sales_amount", "direction": "desc"}],
        "filters": [],
        "limit": 20,
    })
    assert full_alias["order_by"][0]["field"] == "sum_net_sales_amount"
    invalid_sort = agent._validate_query({
        "dataset": "sales_gold",
        "joins": ["customers_gold"],
        "group_by": ["region"],
        "aggregations": [{"field": "net_sales_amount", "function": "sum"}],
        "order_by": [{"field": "unavailable_alias", "direction": "desc"}],
        "filters": [],
        "limit": 20,
    })
    assert invalid_sort["order_by"] == []
    agent.close()


def test_query_validator_blocks_identifiers_and_unapproved_joins() -> None:
    agent = make_agent()
    base = {
        "dataset": "sales_gold",
        "joins": [],
        "group_by": [],
        "aggregations": [{"field": "sales_gold.net_sales_amount", "function": "sum"}],
        "filters": [],
        "limit": 20,
    }
    with pytest.raises(ValueError, match="Identifier fields"):
        agent._validate_query({**base, "group_by": ["customer_id"]})
    with pytest.raises(ValueError, match="does not document a join"):
        agent._validate_query({**base, "joins": ["inventory_gold"]})
    with pytest.raises(ValueError, match="between 1 and 200"):
        agent._validate_query({**base, "limit": 201})
    agent.close()


def test_query_validator_qualifies_ambiguous_base_measure_for_distinct_count() -> None:
    agent = make_agent()
    request = agent._validate_query({
        "dataset": "inventory_gold",
        "joins": ["products_gold"],
        "group_by": ["category"],
        "aggregations": [{"field": "product_id", "function": "count_distinct"}],
        "order_by": [],
        "filters": [],
        "limit": 20,
    })
    agent.close()

    assert request["aggregations"][0]["field"] == "inventory_gold.product_id"


def test_query_validator_allows_counting_keys_but_not_summing_them() -> None:
    agent = make_agent()
    valid = agent._validate_query({
        "dataset": "inventory_gold",
        "joins": ["products_gold"],
        "group_by": ["category"],
        "aggregations": [{"field": "product_id", "function": "count"}],
        "order_by": [],
        "filters": [
            {"field": "low_stock_flag", "operator": "eq", "value": True},
            {"field": "sales_velocity_units_per_day", "operator": "gt", "value": 0},
            {"field": "snapshot_date", "operator": "eq", "value": "2025-12-31"},
        ],
        "limit": 20,
    })
    assert valid["aggregations"][0]["field"] == "inventory_gold.product_id"
    with pytest.raises(ValueError, match="count or distinct-count"):
        agent._validate_query({
            "dataset": "inventory_gold",
            "joins": ["products_gold"],
            "group_by": ["category"],
            "aggregations": [{"field": "product_id", "function": "sum"}],
            "order_by": [],
            "filters": [],
            "limit": 20,
        })
    agent.close()


def test_vega_lite_spec_is_built_from_returned_fields_only() -> None:
    agent = make_agent()
    query = {
        "columns": ["region", "sum_net_sales_amount"],
        "rows": [{"region": "North", "sum_net_sales_amount": 1200.0}],
    }
    response = {
        "title": "Net Sales by Region",
        "mark": "bar",
        "encoding": {
            "x": {"field": "region", "type": "nominal", "title": None},
            "y": {"field": "sum_net_sales_amount", "type": "quantitative", "title": None},
            "color": None,
            "tooltip": None,
        },
    }
    chart = agent._build_vega_spec(ChartProposal.model_validate(response), query)
    agent.close()

    assert chart["data"]["values"] == query["rows"]
    assert chart["encoding"]["x"]["field"] == "region"
    assert chart["mark"] == "bar"


def test_vega_spec_rejects_fields_not_returned_by_gold_api() -> None:
    agent = make_agent()
    proposal = ChartProposal.model_validate({"title": "Bad chart", "mark": "bar", "encoding": {"x": {"field": "customer_id", "type": "nominal", "title": None}, "y": {"field": "sum_net_sales_amount", "type": "quantitative", "title": None}, "color": None, "tooltip": None}})
    with pytest.raises(RuntimeError, match="unsupported channel or field"):
        agent._build_vega_spec(proposal, {"columns": ["sum_net_sales_amount"], "rows": [{"sum_net_sales_amount": 3}]})
    agent.close()


def test_openai_tool_schema_does_not_allow_arbitrary_sql() -> None:
    from p3_agent.agent import _tool_definitions

    serialized = json.dumps(_tool_definitions())
    assert '"sql"' not in serialized.lower()
    assert '"path"' not in serialized.lower()


class FakeOpenAIClient:
    def __init__(self) -> None:
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self.create))
        self.responses = [
            _tool_completion("query_gold_aggregate", {
                "dataset": "sales_gold",
                "joins": ["customers_gold"],
                "group_by": ["region"],
                "aggregations": [{"field": "sales_gold.net_sales_amount", "function": "sum"}],
                "order_by": [{"field": "region", "direction": "asc"}],
                "filters": [],
                "limit": 20,
            }),
            _final_completion({
                "answer": "Net sales by customer region",
                "insight": "North leads in this sample result.",
                "chart": {
                    "title": "Net Sales by Region",
                    "mark": "bar",
                    "encoding": {
                        "x": {"field": "customers_gold.region", "type": "nominal", "title": None},
                        "y": {"field": "sum_sales_gold_net_sales_amount", "type": "quantitative", "title": None},
                        "color": None,
                        "tooltip": None,
                    },
                },
            }),
        ]

    def create(self, **_kwargs):
        return self.responses.pop(0)


def _tool_completion(name: str, arguments: dict) -> SimpleNamespace:
    call = SimpleNamespace(
        id=f"call-{name}",
        function=SimpleNamespace(name=name, arguments=json.dumps(arguments)),
    )
    message = SimpleNamespace(
        content=None,
        tool_calls=[call],
        model_dump=lambda exclude_none=True: {
            "role": "assistant",
            "tool_calls": [{
                "id": call.id,
                "type": "function",
                "function": {"name": name, "arguments": call.function.arguments},
            }],
        },
    )
    return SimpleNamespace(choices=[SimpleNamespace(message=message)])


def _final_completion(payload: dict) -> SimpleNamespace:
    message = SimpleNamespace(content=json.dumps(payload), tool_calls=None)
    return SimpleNamespace(choices=[SimpleNamespace(message=message)])


def test_agent_runs_catalog_tool_query_tool_and_validates_chart() -> None:
    agent = make_agent()
    agent.openai_client = FakeOpenAIClient()
    result = agent.answer("Show net sales by customer region")
    agent.close()

    assert result["answer"] == "Net sales by customer region"
    assert result["chart"]["encoding"]["x"]["field"] == "customers_gold.region"
    assert len(result["data"]["rows"]) == 2


def test_agent_discovers_catalog_and_schemas_before_llm_query() -> None:
    agent = make_agent()
    metadata = agent._discover_metadata()
    agent.close()

    assert len(metadata["datasets"]) == 4
    assert "sales_gold" in metadata["details"]
    assert "customers_gold" in metadata["details"]
    assert metadata["relationships"] == CATALOG["relationships"]


def test_phase3_api_serves_dashboard_health_and_prompt_endpoint() -> None:
    class StubAgent:
        def answer(self, question: str) -> dict:
            return {"answer": question, "insight": "Test insight", "chart": None, "data": None}

        def close(self) -> None:
            pass

    client = TestClient(create_app(StubAgent()))
    assert client.get("/").status_code == 200
    assert client.get("/health").json()["status"] == "ok"
    response = client.post("/api/ask", json={"question": "summarize inventory"})
    assert response.status_code == 200
    assert response.json()["answer"] == "summarize inventory"
    assert client.post("/api/ask", json={"question": ""}).status_code == 422

from __future__ import annotations

import json
import math
import os
import time
from decimal import Decimal
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import duckdb

ROOT = Path(__file__).resolve().parents[1]
CUBE_URL = os.environ.get("CUBE_URL", "http://127.0.0.1:4000").rstrip("/")
CUBE_TOKEN = os.environ.get("CUBE_API_TOKEN")
GOLD_DIR = Path(os.environ.get("AGENTIC_BI_GOLD_DIR", ROOT / "lakehouse" / "gold"))


def _open_with_startup_retry(request: Request):
    for attempt in range(45):
        try:
            return urlopen(request, timeout=30)
        except HTTPError:
            raise
        except URLError:
            if attempt == 44:
                raise
            time.sleep(1)


def cube_get(path: str, query: dict | None = None) -> dict:
    if not CUBE_TOKEN:
        raise RuntimeError("Set CUBE_API_TOKEN in the local environment before running catalog validation.")
    params = ""
    if query is not None:
        params = "?" + urlencode({"query": json.dumps(query, separators=(",", ":"))})
    request = Request(
        f"{CUBE_URL}/cubejs-api/v1/{path}{params}",
        headers={"Authorization": CUBE_TOKEN},
    )
    for _ in range(45):
        try:
            with _open_with_startup_retry(request) as response:
                result = json.load(response)
        except HTTPError as error:
            raise RuntimeError(f"Cube API returned HTTP {error.code}: {error.read().decode('utf-8', 'replace')}") from error
        if result.get("error") != "Continue wait":
            return result
        time.sleep(1)
    raise TimeoutError("Cube query did not complete within 45 seconds.")


def assert_rejected(path: str, query: dict | None, token: str, label: str, auth_failure: bool = False) -> None:
    params = ""
    if query is not None:
        params = "?" + urlencode({"query": json.dumps(query, separators=(",", ":"))})
    request = Request(
        f"{CUBE_URL}/cubejs-api/v1/{path}{params}",
        headers={"Authorization": token},
    )
    try:
        with _open_with_startup_retry(request) as response:
            result = json.load(response)
    except HTTPError as error:
        if auth_failure and error.code not in (401, 403):
            raise AssertionError(f"{label} returned unexpected HTTP {error.code}.") from error
        if not auth_failure and not 400 <= error.code < 500:
            raise AssertionError(f"{label} returned unexpected HTTP {error.code}.") from error
        return
    if result.get("error") and result.get("error") != "Continue wait":
        return
    raise AssertionError(f"{label} was unexpectedly accepted by Cube.")


def _assert_close(actual: object, expected: object, label: str) -> None:
    if not math.isclose(float(actual), float(expected), rel_tol=1e-10, abs_tol=1e-7):
        raise AssertionError(f"{label}: Cube={actual}, DuckDB={expected}")


def main() -> int:
    assert_rejected("meta", None, "Bearer invalid", "Invalid REST authentication", auth_failure=True)
    print("PASS: unauthenticated/invalid-token REST access is rejected")

    meta = cube_get("meta")
    cubes = {cube["name"]: cube for cube in meta.get("cubes", [])}
    required_cubes = {"Sales", "Customers", "Products", "Inventory"}
    if not required_cubes.issubset(cubes):
        raise AssertionError(f"Missing semantic cubes: {sorted(required_cubes - cubes.keys())}")

    expected_members = {
        "Sales.netSales",
        "Sales.orderCount",
        "Sales.unitsSold",
        "Sales.customerContributionShare",
        "Customers.customerSegment",
        "Products.category",
        "Inventory.salesVelocityUnitsPerDay",
        "Inventory.stockCoverageDays",
        "Inventory.stockCoverageStatus",
    }
    published_members = {
        member["name"]
        for cube in meta["cubes"]
        for field in ("measures", "dimensions", "segments")
        for member in cube.get(field, [])
    }
    if not expected_members.issubset(published_members):
        raise AssertionError(f"Missing semantic members: {sorted(expected_members - published_members)}")
    print("PASS: catalog publishes required cubes and governed members")

    assert_rejected(
        "load",
        {"measures": ["Sales.memberThatDoesNotExist"]},
        CUBE_TOKEN,
        "Unknown semantic member",
    )
    print("PASS: unsupported semantic members are rejected")

    sales_result = cube_get("load", {"measures": ["Sales.netSales", "Sales.orderCount"]})["data"][0]
    customer_result = cube_get(
        "load",
        {
            "measures": ["Sales.netSales", "Sales.orderCount", "Sales.customerContributionShare"],
            "dimensions": ["Customers.region"],
        },
    )["data"]
    inventory_result = cube_get(
        "load",
        {
            "measures": [
                "Inventory.inventoryOnHand",
                "Inventory.lowStockRows",
                "Inventory.salesVelocityUnitsPerDay",
                "Inventory.stockCoverageDays",
            ]
        },
    )["data"][0]

    with duckdb.connect() as connection:
        for table in ("sales_gold", "customers_gold", "products_gold", "inventory_gold"):
            connection.register(table, connection.read_parquet(str(GOLD_DIR / f"{table}.parquet")))
        sales_expected = connection.sql(
            "SELECT SUM(net_sales_amount), COUNT(DISTINCT order_id) FROM sales_gold"
        ).fetchone()
        customer_expected = connection.sql(
            """
            SELECT c.region, SUM(s.net_sales_amount), COUNT(DISTINCT s.order_id)
            FROM sales_gold s JOIN customers_gold c USING (customer_id)
            GROUP BY c.region
            """
        ).fetchall()
        inventory_expected = connection.sql(
            """
            SELECT SUM(inventory_on_hand), SUM(CASE WHEN low_stock_flag THEN 1 ELSE 0 END),
                   AVG(sales_velocity_units_per_day), AVG(stock_coverage_days)
            FROM inventory_gold
            """
        ).fetchone()

    _assert_close(sales_result["Sales.netSales"], sales_expected[0], "Net sales")
    _assert_close(sales_result["Sales.orderCount"], sales_expected[1], "Distinct completed orders")
    expected_by_region = {row[0]: row[1:] for row in customer_expected}
    for row in customer_result:
        expected = expected_by_region[row["Customers.region"]]
        _assert_close(row["Sales.netSales"], expected[0], f"Net sales for {row['Customers.region']}")
        _assert_close(row["Sales.orderCount"], expected[1], f"Distinct orders for {row['Customers.region']}")
        _assert_close(
            row["Sales.customerContributionShare"],
            Decimal(expected[0]) / Decimal(sales_expected[0]),
            f"Customer contribution share for {row['Customers.region']}",
        )
    inventory_keys = (
        "Inventory.inventoryOnHand",
        "Inventory.lowStockRows",
        "Inventory.salesVelocityUnitsPerDay",
        "Inventory.stockCoverageDays",
    )
    for key, expected in zip(inventory_keys, inventory_expected, strict=True):
        _assert_close(inventory_result[key], expected, key)
    print("PASS: sales, customer-region, and inventory metrics match direct DuckDB results")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

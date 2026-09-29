from __future__ import annotations

from pathlib import Path

import duckdb


def run_sample_queries(gold_dir: Path) -> dict[str, duckdb.DuckDBPyRelation]:
    con = duckdb.connect()
    sales = con.read_parquet(str(gold_dir / "sales_gold.parquet"))
    customers = con.read_parquet(str(gold_dir / "customers_gold.parquet"))
    inventory = con.read_parquet(str(gold_dir / "inventory_gold.parquet"))

    con.register("sales", sales)
    con.register("customers", customers)
    con.register("inventory", inventory)

    return {
        "sales_trend": con.sql("SELECT SUM(net_sales_amount) AS net_sales FROM sales"),
        "customer_profile": con.sql("SELECT COUNT(*) AS customer_count FROM customers"),
        "inventory_risk": con.sql("SELECT COUNT(*) AS low_stock_rows FROM inventory WHERE low_stock_flag = TRUE"),
    }

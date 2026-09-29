from __future__ import annotations

from pathlib import Path

import duckdb

from p1_u4.config import GoldConfig


def build_gold(config: GoldConfig) -> dict[str, duckdb.DuckDBPyRelation]:
    silver_dir = Path(config.silver_dir)
    gold_dir = Path(config.gold_dir)
    gold_dir.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect()
    customers = con.read_parquet(str(silver_dir / "customers.parquet"))
    products = con.read_parquet(str(silver_dir / "products.parquet"))
    orders = con.read_parquet(str(silver_dir / "orders.parquet"))
    order_lines = con.read_parquet(str(silver_dir / "order_lines.parquet"))
    inventory = con.read_parquet(str(silver_dir / "inventory_snapshots.parquet"))

    con.register("l", order_lines)
    con.register("o", orders)
    sales = con.sql(
        """
        SELECT
            l.order_line_id,
            l.order_id,
            l.product_id,
            o.customer_id,
            CAST(o.order_date AS DATE) AS order_date,
            l.quantity,
            l.unit_price,
            l.discount_rate,
            (l.quantity * l.unit_price) AS gross_sales_amount,
            (l.quantity * l.unit_price * l.discount_rate) AS discount_amount,
            (l.quantity * l.unit_price * (1 - l.discount_rate)) AS net_sales_amount
        FROM l
        JOIN o ON l.order_id = o.order_id
        """
    )
    sales.write_parquet(str(gold_dir / "sales_gold.parquet"))

    customers_gold = customers.select(
        "customer_id",
        "customer_segment",
        "region",
        "acquisition_channel",
        "acquisition_date",
        "customer_status",
    )
    customers_gold.write_parquet(str(gold_dir / "customers_gold.parquet"))

    products_gold = products.select(
        "product_id",
        "product_name",
        "category",
        "subcategory",
        "list_price",
        "product_status",
    )
    products_gold.write_parquet(str(gold_dir / "products_gold.parquet"))

    con.register("inventory", inventory)
    inventory_gold = con.sql(
        """
        SELECT
            snapshot_date,
            product_id,
            inventory_on_hand,
            reorder_point,
            CASE
                WHEN reorder_point IS NULL OR reorder_point = 0 THEN NULL
                ELSE CAST(inventory_on_hand / reorder_point AS DOUBLE)
            END AS stock_coverage_days,
            CASE
                WHEN inventory_on_hand <= reorder_point THEN TRUE
                ELSE FALSE
            END AS low_stock_flag,
            CAST(inventory_on_hand AS DOUBLE) AS inventory_velocity
        FROM inventory
        """
    )
    inventory_gold.write_parquet(str(gold_dir / "inventory_gold.parquet"))

    return {
        "sales_gold": con.read_parquet(str(gold_dir / "sales_gold.parquet")),
        "customers_gold": con.read_parquet(str(gold_dir / "customers_gold.parquet")),
        "products_gold": con.read_parquet(str(gold_dir / "products_gold.parquet")),
        "inventory_gold": con.read_parquet(str(gold_dir / "inventory_gold.parquet")),
    }

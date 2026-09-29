from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import duckdb

from p1_u3.config import SilverConfig

ENTITY_FILES = {
    "customers": "customers.parquet",
    "products": "products.parquet",
    "orders": "orders.parquet",
    "order_lines": "order_lines.parquet",
    "inventory_snapshots": "inventory_snapshots.parquet",
}


def standardize_bronze_to_silver(config: SilverConfig) -> dict[str, duckdb.DuckDBPyRelation]:
    bronze_dir = Path(config.bronze_dir)
    silver_dir = Path(config.silver_dir)
    silver_dir.mkdir(parents=True, exist_ok=True)

    outputs: dict[str, duckdb.DuckDBPyRelation] = {}
    for name, filename in ENTITY_FILES.items():
        source_path = bronze_dir / filename
        if not source_path.exists():
            raise FileNotFoundError(f"Required Bronze file missing: {source_path}")

        sql = {
            "customers": (
                "SELECT customer_id, customer_name, customer_segment, region, acquisition_channel, "
                "CAST(acquisition_date AS DATE) AS acquisition_date, customer_status, "
                "source_file, source_row_number, source_run_id, ingested_at "
                f"FROM read_parquet('{source_path.as_posix()}')"
            ),
            "products": (
                "SELECT product_id, product_name, category, subcategory, "
                "CAST(list_price AS DECIMAL(18,2)) AS list_price, CAST(reorder_point AS INTEGER) AS reorder_point, "
                "product_status, source_file, source_row_number, source_run_id, ingested_at "
                f"FROM read_parquet('{source_path.as_posix()}')"
            ),
            "orders": (
                "SELECT order_id, customer_id, CAST(order_date AS DATE) AS order_date, order_status, "
                "payment_method, channel, source_file, source_row_number, source_run_id, ingested_at "
                f"FROM read_parquet('{source_path.as_posix()}')"
            ),
            "order_lines": (
                "SELECT order_line_id, order_id, product_id, CAST(quantity AS INTEGER) AS quantity, "
                "CAST(unit_price AS DECIMAL(18,2)) AS unit_price, CAST(discount_rate AS DECIMAL(18,4)) AS discount_rate, "
                "source_file, source_row_number, source_run_id, ingested_at "
                f"FROM read_parquet('{source_path.as_posix()}')"
            ),
            "inventory_snapshots": (
                "SELECT CAST(snapshot_date AS DATE) AS snapshot_date, product_id, CAST(inventory_on_hand AS INTEGER) AS inventory_on_hand, "
                "CAST(reorder_point AS INTEGER) AS reorder_point, source_file, source_row_number, source_run_id, ingested_at "
                f"FROM read_parquet('{source_path.as_posix()}')"
            ),
        }[name]

        cleaned = duckdb.sql(sql)
        target_path = silver_dir / f"{name}.parquet"
        cleaned.write_parquet(str(target_path))
        outputs[name] = duckdb.read_parquet(str(target_path))

    return outputs

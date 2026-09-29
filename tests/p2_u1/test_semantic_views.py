from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import duckdb


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
PREPARE_SCRIPT = WORKSPACE_ROOT / "semantic" / "cube" / "prepare_gold_views.py"


def test_prepare_gold_views_registers_parquet_paths(tmp_path: Path) -> None:
    gold_dir = tmp_path / "gold's files"
    gold_dir.mkdir()
    database_path = tmp_path / ".local" / "semantic.duckdb"

    duckdb.sql(
        "SELECT 'L1' AS order_line_id, 'O1' AS order_id, 'C1' AS customer_id, 'P1' AS product_id, "
        "DATE '2024-01-01' AS order_date, 'Online' AS channel, 1 AS quantity, "
        "10.0 AS unit_price, 0.0 AS discount_rate, 10.0 AS gross_sales_amount, "
        "0.0 AS discount_amount, 10.0 AS net_sales_amount"
    ).write_parquet(str(gold_dir / "sales_gold.parquet"))
    duckdb.sql(
        "SELECT 'C1' AS customer_id, 'Plus' AS customer_segment, 'North' AS region, "
        "'Search' AS acquisition_channel, DATE '2023-01-01' AS acquisition_date, 'Active' AS customer_status"
    ).write_parquet(str(gold_dir / "customers_gold.parquet"))
    duckdb.sql(
        "SELECT 'P1' AS product_id, 'Widget' AS product_name, 'Home' AS category, "
        "'Small' AS subcategory, 10.0 AS list_price, 'Active' AS product_status"
    ).write_parquet(str(gold_dir / "products_gold.parquet"))
    duckdb.sql(
        "SELECT DATE '2024-01-01' AS snapshot_date, 'P1' AS product_id, 5 AS inventory_on_hand, "
        "2 AS reorder_point, 1.0 AS sales_velocity_units_per_day, 5.0 AS stock_coverage_days, "
        "'calculated' AS stock_coverage_status, FALSE AS low_stock_flag"
    ).write_parquet(str(gold_dir / "inventory_gold.parquet"))

    subprocess.run(
        [
            sys.executable,
            str(PREPARE_SCRIPT),
            "--gold-dir",
            str(gold_dir),
            "--database-path",
            str(database_path),
        ],
        cwd=WORKSPACE_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    with duckdb.connect(str(database_path), read_only=True) as connection:
        assert connection.sql("SELECT COUNT(*) FROM sales_gold").fetchone() == (1,)
        assert connection.sql("SELECT SUM(net_sales_amount) FROM sales_gold").fetchone() == (10.0,)
        assert connection.sql("SELECT stock_coverage_status FROM inventory_gold").fetchone() == ("calculated",)
        assert {row[0] for row in connection.sql("SHOW TABLES").fetchall()} == {
            "customers_gold",
            "inventory_gold",
            "products_gold",
            "sales_gold",
        }

from pathlib import Path

import duckdb

from p1_u4.cli import main


def test_cli_builds_gold_outputs(tmp_path: Path) -> None:
    silver_dir = tmp_path / 'silver'
    silver_dir.mkdir()
    gold_dir = tmp_path / 'gold'

    duckdb.sql("SELECT 'C1' AS customer_id, 'Plus' AS customer_segment, 'North' AS region, 'Search' AS acquisition_channel, DATE '2024-01-01' AS acquisition_date, 'Active' AS customer_status, 'customers.csv' AS source_file, 1 AS source_row_number, 'run-1' AS source_run_id, TIMESTAMP '2024-01-01 00:00:00' AS ingested_at").write_parquet(str(silver_dir / 'customers.parquet'))
    duckdb.sql("SELECT 'P1' AS product_id, 'Widget' AS product_name, 'Electronics' AS category, 'Audio' AS subcategory, CAST('99.99' AS DECIMAL(18,2)) AS list_price, 'Active' AS product_status, 'products.csv' AS source_file, 1 AS source_row_number, 'run-1' AS source_run_id, TIMESTAMP '2024-01-01 00:00:00' AS ingested_at").write_parquet(str(silver_dir / 'products.parquet'))
    duckdb.sql("SELECT 'O1' AS order_id, 'C1' AS customer_id, DATE '2024-01-01' AS order_date, 'Completed' AS order_status, 'Card' AS payment_method, 'Online' AS channel, 'orders.csv' AS source_file, 1 AS source_row_number, 'run-1' AS source_run_id, TIMESTAMP '2024-01-01 00:00:00' AS ingested_at").write_parquet(str(silver_dir / 'orders.parquet'))
    duckdb.sql("SELECT 'L1' AS order_line_id, 'O1' AS order_id, 'P1' AS product_id, 2 AS quantity, CAST('49.99' AS DECIMAL(18,2)) AS unit_price, CAST('0.10' AS DECIMAL(18,4)) AS discount_rate, 'order_lines.csv' AS source_file, 1 AS source_row_number, 'run-1' AS source_run_id, TIMESTAMP '2024-01-01 00:00:00' AS ingested_at").write_parquet(str(silver_dir / 'order_lines.parquet'))
    duckdb.sql("SELECT DATE '2024-01-01' AS snapshot_date, 'P1' AS product_id, 10 AS inventory_on_hand, 5 AS reorder_point, 'inventory_snapshots.csv' AS source_file, 1 AS source_row_number, 'run-1' AS source_run_id, TIMESTAMP '2024-01-01 00:00:00' AS ingested_at").write_parquet(str(silver_dir / 'inventory_snapshots.parquet'))

    assert main(['--silver-dir', str(silver_dir), '--gold-dir', str(gold_dir)]) == 0

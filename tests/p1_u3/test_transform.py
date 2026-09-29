from pathlib import Path

import duckdb

from p1_u3.config import SilverConfig
from p1_u3.transform import standardize_bronze_to_silver


def test_transform_creates_silver_tables(tmp_path: Path) -> None:
    bronze_dir = tmp_path / "bronze"
    bronze_dir.mkdir()
    customer_rel = duckdb.sql("SELECT 'C1' AS customer_id, 'Alice' AS customer_name, 'Plus' AS customer_segment, 'North' AS region, 'Search' AS acquisition_channel, '2024-01-01' AS acquisition_date, 'Active' AS customer_status, 'customers.csv' AS source_file, 1 AS source_row_number, 'run-001' AS source_run_id, TIMESTAMP '2024-01-01 00:00:00' AS ingested_at")
    product_rel = duckdb.sql("SELECT 'P1' AS product_id, 'Widget' AS product_name, 'Electronics' AS category, 'Audio' AS subcategory, '99.99' AS list_price, 5 AS reorder_point, 'Active' AS product_status, 'products.csv' AS source_file, 1 AS source_row_number, 'run-001' AS source_run_id, TIMESTAMP '2024-01-01 00:00:00' AS ingested_at")
    order_rel = duckdb.sql("SELECT 'O1' AS order_id, 'C1' AS customer_id, '2024-01-01' AS order_date, 'Completed' AS order_status, 'Card' AS payment_method, 'Online' AS channel, 'orders.csv' AS source_file, 1 AS source_row_number, 'run-001' AS source_run_id, TIMESTAMP '2024-01-01 00:00:00' AS ingested_at")
    line_rel = duckdb.sql("SELECT 'L1' AS order_line_id, 'O1' AS order_id, 'P1' AS product_id, 2 AS quantity, '49.99' AS unit_price, '0.10' AS discount_rate, 'order_lines.csv' AS source_file, 1 AS source_row_number, 'run-001' AS source_run_id, TIMESTAMP '2024-01-01 00:00:00' AS ingested_at")
    snapshot_rel = duckdb.sql("SELECT '2024-01-01' AS snapshot_date, 'P1' AS product_id, 10 AS inventory_on_hand, 5 AS reorder_point, 'inventory_snapshots.csv' AS source_file, 1 AS source_row_number, 'run-001' AS source_run_id, TIMESTAMP '2024-01-01 00:00:00' AS ingested_at")

    customer_rel.write_parquet(str(bronze_dir / 'customers.parquet'))
    product_rel.write_parquet(str(bronze_dir / 'products.parquet'))
    order_rel.write_parquet(str(bronze_dir / 'orders.parquet'))
    line_rel.write_parquet(str(bronze_dir / 'order_lines.parquet'))
    snapshot_rel.write_parquet(str(bronze_dir / 'inventory_snapshots.parquet'))

    silver_dir = tmp_path / 'silver'
    outputs = standardize_bronze_to_silver(SilverConfig(bronze_dir=bronze_dir, silver_dir=silver_dir))

    assert set(outputs) == {'customers', 'products', 'orders', 'order_lines', 'inventory_snapshots'}
    assert outputs['customers'].shape[0] == 1
    assert 'acquisition_date' in outputs['customers'].columns

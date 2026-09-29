from pathlib import Path

from p1_u3.cli import main


def test_cli_runs_successfully_with_valid_silver_contract(tmp_path: Path) -> None:
    bronze_dir = tmp_path / "bronze"
    bronze_dir.mkdir()
    silver_dir = tmp_path / "silver"

    for name, content in {
        "customers": "SELECT 'C1' AS customer_id, 'Alice' AS customer_name, 'Plus' AS customer_segment, 'North' AS region, 'Search' AS acquisition_channel, DATE '2024-01-01' AS acquisition_date, 'Active' AS customer_status, 'customers.csv' AS source_file, 1 AS source_row_number, 'run-001' AS source_run_id, TIMESTAMP '2024-01-01 00:00:00' AS ingested_at",
        "products": "SELECT 'P1' AS product_id, 'Widget' AS product_name, 'Electronics' AS category, 'Audio' AS subcategory, CAST('99.99' AS DECIMAL(18,2)) AS list_price, 5 AS reorder_point, 'Active' AS product_status, 'products.csv' AS source_file, 1 AS source_row_number, 'run-001' AS source_run_id, TIMESTAMP '2024-01-01 00:00:00' AS ingested_at",
        "orders": "SELECT 'O1' AS order_id, 'C1' AS customer_id, DATE '2024-01-01' AS order_date, 'Completed' AS order_status, 'Card' AS payment_method, 'Online' AS channel, 'orders.csv' AS source_file, 1 AS source_row_number, 'run-001' AS source_run_id, TIMESTAMP '2024-01-01 00:00:00' AS ingested_at",
        "order_lines": "SELECT 'L1' AS order_line_id, 'O1' AS order_id, 'P1' AS product_id, 2 AS quantity, CAST('49.99' AS DECIMAL(18,2)) AS unit_price, CAST('0.10' AS DECIMAL(18,4)) AS discount_rate, 'order_lines.csv' AS source_file, 1 AS source_row_number, 'run-001' AS source_run_id, TIMESTAMP '2024-01-01 00:00:00' AS ingested_at",
        "inventory_snapshots": "SELECT DATE '2024-01-01' AS snapshot_date, 'P1' AS product_id, 10 AS inventory_on_hand, 5 AS reorder_point, 'inventory_snapshots.csv' AS source_file, 1 AS source_row_number, 'run-001' AS source_run_id, TIMESTAMP '2024-01-01 00:00:00' AS ingested_at",
    }.items():
        import duckdb
        duckdb.sql(content).write_parquet(str(bronze_dir / f"{name}.parquet"))

    assert main(["--bronze-dir", str(bronze_dir), "--silver-dir", str(silver_dir)]) == 0

from pathlib import Path

import duckdb

from p1_u4.queries import run_sample_queries


def test_run_sample_queries_returns_expected_shapes(tmp_path: Path) -> None:
    gold_dir = tmp_path / 'gold'
    gold_dir.mkdir()
    sales = duckdb.sql("SELECT 'L1' AS order_line_id, 'O1' AS order_id, 'P1' AS product_id, 'C1' AS customer_id, DATE '2024-01-01' AS order_date, 2 AS quantity, CAST('49.99' AS DECIMAL(18,2)) AS unit_price, CAST('0.10' AS DECIMAL(18,4)) AS discount_rate, 99.98 AS gross_sales_amount, 9.998 AS discount_amount, 89.982 AS net_sales_amount").write_parquet(str(gold_dir / 'sales_gold.parquet'))
    duckdb.sql("SELECT 'C1' AS customer_id, 'Plus' AS customer_segment, 'North' AS region, 'Search' AS acquisition_channel, DATE '2024-01-01' AS acquisition_date, 'Active' AS customer_status").write_parquet(str(gold_dir / 'customers_gold.parquet'))
    duckdb.sql("SELECT DATE '2024-01-01' AS snapshot_date, 'P1' AS product_id, 10 AS inventory_on_hand, 5 AS reorder_point, 2.0 AS stock_coverage_days, TRUE AS low_stock_flag, 10.0 AS inventory_velocity").write_parquet(str(gold_dir / 'inventory_gold.parquet'))
    del sales

    results = run_sample_queries(gold_dir)

    assert 'sales_trend' in results
    assert 'customer_profile' in results
    assert 'inventory_risk' in results

from pathlib import Path

import duckdb
import pytest

from p1_u4.config import GoldConfig
from p1_u4.gold import build_gold


def _write_silver_fixtures(silver_dir: Path) -> None:
    silver_dir.mkdir()
    duckdb.sql(
        """
        SELECT * FROM (VALUES
            ('C1', 'Plus', 'North', 'Search', DATE '2023-01-01', 'Active'),
            ('C2', 'Basic', 'South', 'Social', DATE '2023-01-01', 'Active')
        ) AS t(customer_id, customer_segment, region, acquisition_channel, acquisition_date, customer_status)
        """
    ).write_parquet(str(silver_dir / "customers.parquet"))
    duckdb.sql(
        """
        SELECT * FROM (VALUES
            ('P1', 'Widget', 'Electronics', 'Audio', CAST('99.99' AS DECIMAL(18,2)), 'Active'),
            ('P2', 'Gadget', 'Home', 'Small', CAST('10.00' AS DECIMAL(18,2)), 'Active'),
            ('P3', 'Speaker', 'Electronics', 'Audio', CAST('49.99' AS DECIMAL(18,2)), 'Active')
        ) AS t(product_id, product_name, category, subcategory, list_price, product_status)
        """
    ).write_parquet(str(silver_dir / "products.parquet"))
    duckdb.sql(
        """
        SELECT * FROM (VALUES
            ('O_OLD', 'C1', DATE '2024-01-01', 'Completed', 'Card', 'Online'),
            ('O_START', 'C1', DATE '2024-01-02', 'Completed', 'Card', 'Online'),
            ('O_END', 'C1', DATE '2024-01-31', 'Completed', 'Card', 'Store'),
            ('O_SNAPSHOT', 'C1', DATE '2024-02-01', 'Completed', 'Card', 'Online'),
            ('O_CANCEL', 'C2', DATE '2024-01-31', 'Cancelled', 'Card', 'Online')
        ) AS t(order_id, customer_id, order_date, order_status, payment_method, channel)
        """
    ).write_parquet(str(silver_dir / "orders.parquet"))
    duckdb.sql(
        """
        SELECT * FROM (VALUES
            ('L_OLD', 'O_OLD', 'P1', 99, CAST('1.00' AS DECIMAL(18,2)), CAST('0.00' AS DECIMAL(18,4))),
            ('L_START', 'O_START', 'P1', 2, CAST('10.00' AS DECIMAL(18,2)), CAST('0.10' AS DECIMAL(18,4))),
            ('L_END', 'O_END', 'P1', 6, CAST('10.00' AS DECIMAL(18,2)), CAST('0.25' AS DECIMAL(18,4))),
            ('L_SNAPSHOT', 'O_SNAPSHOT', 'P1', 100, CAST('10.00' AS DECIMAL(18,2)), CAST('0.00' AS DECIMAL(18,4))),
            ('L_CANCEL', 'O_CANCEL', 'P1', 500, CAST('10.00' AS DECIMAL(18,2)), CAST('0.00' AS DECIMAL(18,4))),
            ('L_P3', 'O_START', 'P3', 6, CAST('5.00' AS DECIMAL(18,2)), CAST('0.00' AS DECIMAL(18,4)))
        ) AS t(order_line_id, order_id, product_id, quantity, unit_price, discount_rate)
        """
    ).write_parquet(str(silver_dir / "order_lines.parquet"))
    duckdb.sql(
        """
        SELECT * FROM (VALUES
            (DATE '2024-02-01', 'P1', 20, 5),
            (DATE '2024-02-01', 'P2', 0, 10),
            (DATE '2024-02-01', 'P3', 10, 1)
        ) AS t(snapshot_date, product_id, inventory_on_hand, reorder_point)
        """
    ).write_parquet(str(silver_dir / "inventory_snapshots.parquet"))


def test_build_gold_applies_completed_sales_and_inventory_demand_rules(tmp_path: Path) -> None:
    silver_dir = tmp_path / "silver"
    gold_dir = tmp_path / "gold"
    _write_silver_fixtures(silver_dir)

    outputs = build_gold(GoldConfig(silver_dir=silver_dir, gold_dir=gold_dir))

    assert set(outputs) == {"sales_gold", "customers_gold", "products_gold", "inventory_gold"}

    sales = outputs["sales_gold"].df()
    assert len(sales) == 5
    assert "L_CANCEL" not in set(sales["order_line_id"])
    assert set(sales["channel"]) == {"Online", "Store"}
    assert sales["gross_sales_amount"].sum() == pytest.approx(1209.0)
    assert sales["discount_amount"].sum() == pytest.approx(17.0)
    assert sales["net_sales_amount"].sum() == pytest.approx(1192.0)

    inventory = outputs["inventory_gold"].df().set_index("product_id")
    assert len(inventory) == 3
    # Include Jan 2 and Jan 31; exclude Jan 1 (outside the window) and Feb 1 (snapshot day).
    assert inventory.loc["P1", "sales_velocity_units_per_day"] == pytest.approx(8 / 30)
    assert inventory.loc["P1", "stock_coverage_days"] == pytest.approx(75.0)
    assert inventory.loc["P1", "stock_coverage_status"] == "calculated"
    assert not bool(inventory.loc["P1", "low_stock_flag"])
    assert inventory.loc["P2", "sales_velocity_units_per_day"] == pytest.approx(0.0)
    assert inventory.loc["P2", "stock_coverage_days"] == pytest.approx(0.0)
    assert inventory.loc["P2", "stock_coverage_status"] == "no_demand"
    assert bool(inventory.loc["P2", "low_stock_flag"])
    assert inventory.loc["P3", "sales_velocity_units_per_day"] == pytest.approx(6 / 30)
    assert inventory.loc["P3", "stock_coverage_days"] == pytest.approx(50.0)

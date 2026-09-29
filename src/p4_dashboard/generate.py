from __future__ import annotations

from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[2]
GOLD_DIR = ROOT / "lakehouse" / "gold"


def _safe_float(value: object) -> float:
    if value is None:
        return 0.0
    return float(value)


def build_dashboard_payload(gold_dir: str | Path | None = None) -> dict:
    gold_path = Path(gold_dir) if gold_dir is not None else GOLD_DIR
    con = duckdb.connect()

    sales = con.read_parquet(str(gold_path / "sales_gold.parquet"))
    customers = con.read_parquet(str(gold_path / "customers_gold.parquet"))
    products = con.read_parquet(str(gold_path / "products_gold.parquet"))
    inventory = con.read_parquet(str(gold_path / "inventory_gold.parquet"))
    con.register("sales", sales)
    con.register("customers", customers)
    con.register("products", products)
    con.register("inventory", inventory)

    summary = con.sql(
        """
        SELECT
            SUM(net_sales_amount) AS net_sales,
            SUM(gross_sales_amount) AS gross_sales,
            SUM(quantity) AS units_sold,
            COUNT(DISTINCT order_id) AS total_orders,
            AVG(net_sales_amount) AS avg_order_value
        FROM sales
        """
    ).fetchone()

    sales_rows = con.sql(
        """
        SELECT
            CAST(s.order_date AS DATE) AS order_date,
            s.order_id,
            s.customer_id,
            c.region AS region,
            s.channel AS channel,
            p.product_name AS product_name,
            s.net_sales_amount AS net_sales_amount,
            s.gross_sales_amount AS gross_sales_amount,
            s.quantity AS quantity
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.customer_id
        LEFT JOIN products p ON s.product_id = p.product_id
        ORDER BY s.order_date ASC
        """
    ).fetchall()

    revenue_by_region = con.sql(
        """
        SELECT
            c.region AS label,
            ROUND(SUM(s.net_sales_amount), 2) AS value
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.customer_id
        GROUP BY c.region
        ORDER BY value DESC
        """
    ).fetchall()

    sales_by_channel = con.sql(
        """
        SELECT
            s.channel AS label,
            ROUND(SUM(s.net_sales_amount), 2) AS value
        FROM sales s
        GROUP BY s.channel
        ORDER BY value DESC
        """
    ).fetchall()

    daily_sales = con.sql(
        """
        SELECT
            CAST(order_date AS DATE) AS label,
            ROUND(SUM(net_sales_amount), 2) AS value
        FROM sales
        GROUP BY CAST(order_date AS DATE)
        ORDER BY CAST(order_date AS DATE)
        """
    ).fetchall()

    inventory_risk = con.sql(
        """
        SELECT
            p.product_name AS product_name,
            i.inventory_on_hand AS inventory_on_hand,
            i.sales_velocity_units_per_day AS sales_velocity_units_per_day,
            i.stock_coverage_days AS stock_coverage_days,
            i.low_stock_flag AS low_stock_flag
        FROM inventory i
        LEFT JOIN products p ON i.product_id = p.product_id
        ORDER BY i.stock_coverage_days ASC, i.inventory_on_hand ASC
        LIMIT 10
        """
    ).fetchall()

    semantic_view = [
        {
            "table": "sales_gold",
            "description": "Completed-order sales fact for the governed revenue metrics.",
            "key_fields": ["order_line_id", "order_id", "product_id", "customer_id", "order_date"],
            "dimensions": ["customer_id", "product_id", "channel", "order_date"],
            "measures": ["gross_sales_amount", "discount_amount", "net_sales_amount", "quantity"],
        },
        {
            "table": "customers_gold",
            "description": "Customer-level profile and segmentation dimensions.",
            "key_fields": ["customer_id"],
            "dimensions": ["customer_segment", "region", "acquisition_channel"],
            "measures": [],
        },
        {
            "table": "products_gold",
            "description": "Catalog product dimension used for category, subcategory, and pricing views.",
            "key_fields": ["product_id"],
            "dimensions": ["product_name", "category", "subcategory"],
            "measures": ["list_price"],
        },
        {
            "table": "inventory_gold",
            "description": "Product-day inventory health and demand coverage snapshot.",
            "key_fields": ["snapshot_date", "product_id"],
            "dimensions": ["snapshot_date", "product_id"],
            "measures": ["inventory_on_hand", "sales_velocity_units_per_day", "stock_coverage_days"],
        },
    ]

    revenue_by_region_rows = revenue_by_region
    sales_by_channel_rows = sales_by_channel
    daily_sales_rows = daily_sales
    inventory_risk_rows = inventory_risk

    product_names = sorted({row[5] for row in sales_rows if row[5]})
    customer_ids = sorted({row[2] for row in sales_rows if row[2]})
    date_values = [row[0] for row in sales_rows if row[0] is not None]

    revenue_by_region_rows = revenue_by_region
    sales_by_channel_rows = sales_by_channel
    daily_sales_rows = daily_sales
    inventory_risk_rows = inventory_risk

    payload = {
        "dashboard_title": "Product Sales & Inventory Monitor",
        "summary": {
            "net_sales": _safe_float(summary[0]),
            "gross_sales": _safe_float(summary[1]),
            "units_sold": _safe_float(summary[2]),
            "total_orders": _safe_float(summary[3]),
            "avg_order_value": _safe_float(summary[4]),
        },
        "filters": {
            "date_min": min(date_values).isoformat() if date_values else None,
            "date_max": max(date_values).isoformat() if date_values else None,
            "products": product_names,
            "customers": customer_ids,
        },
        "sales_rows": [
            {
                "order_date": row[0].isoformat() if row[0] is not None else None,
                "order_id": row[1],
                "customer_id": row[2],
                "region": row[3],
                "channel": row[4],
                "product_name": row[5],
                "net_sales_amount": float(row[6]) if row[6] is not None else 0.0,
                "gross_sales_amount": float(row[7]) if row[7] is not None else 0.0,
                "quantity": float(row[8]) if row[8] is not None else 0.0,
            }
            for row in sales_rows
        ],
        "semantic_view": semantic_view,
        "revenue_by_region": [
            {"label": row[0], "value": float(row[1]) if row[1] is not None else 0.0}
            for row in revenue_by_region_rows
        ],
        "sales_by_channel": [
            {"label": row[0], "value": float(row[1]) if row[1] is not None else 0.0}
            for row in sales_by_channel_rows
        ],
        "daily_sales": [
            {"label": str(row[0]), "value": float(row[1]) if row[1] is not None else 0.0}
            for row in daily_sales_rows
        ],
        "inventory_risk": [
            {
                "product_name": row[0],
                "inventory_on_hand": float(row[1]) if row[1] is not None else 0.0,
                "sales_velocity": float(row[2]) if row[2] is not None else 0.0,
                "stock_coverage_days": float(row[3]) if row[3] is not None else 0.0,
                "low_stock_flag": bool(row[4]),
            }
            for row in inventory_risk_rows
        ],
    }

    return payload


def main() -> int:
    payload = build_dashboard_payload()
    output_path = ROOT / "dashboard" / "data.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(__import__("json").dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote dashboard payload to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

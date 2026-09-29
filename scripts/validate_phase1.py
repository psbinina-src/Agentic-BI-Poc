import duckdb

con = duckdb.connect()

queries = {
    "source_counts": """
        SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM read_csv_auto('lakehouse/source/customers.csv')
        UNION ALL
        SELECT 'products', COUNT(*) FROM read_csv_auto('lakehouse/source/products.csv')
        UNION ALL
        SELECT 'orders', COUNT(*) FROM read_csv_auto('lakehouse/source/orders.csv')
        UNION ALL
        SELECT 'order_lines', COUNT(*) FROM read_csv_auto('lakehouse/source/order_lines.csv')
        UNION ALL
        SELECT 'inventory_snapshots', COUNT(*) FROM read_csv_auto('lakehouse/source/inventory_snapshots.csv')
    """,
    "bronze_counts": """
        SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM read_parquet('lakehouse/bronze/customers.parquet')
        UNION ALL
        SELECT 'products', COUNT(*) FROM read_parquet('lakehouse/bronze/products.parquet')
        UNION ALL
        SELECT 'orders', COUNT(*) FROM read_parquet('lakehouse/bronze/orders.parquet')
        UNION ALL
        SELECT 'order_lines', COUNT(*) FROM read_parquet('lakehouse/bronze/order_lines.parquet')
        UNION ALL
        SELECT 'inventory_snapshots', COUNT(*) FROM read_parquet('lakehouse/bronze/inventory_snapshots.parquet')
    """,
    "silver_counts": """
        SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM read_parquet('lakehouse/silver/customers.parquet')
        UNION ALL
        SELECT 'products', COUNT(*) FROM read_parquet('lakehouse/silver/products.parquet')
        UNION ALL
        SELECT 'orders', COUNT(*) FROM read_parquet('lakehouse/silver/orders.parquet')
        UNION ALL
        SELECT 'order_lines', COUNT(*) FROM read_parquet('lakehouse/silver/order_lines.parquet')
        UNION ALL
        SELECT 'inventory_snapshots', COUNT(*) FROM read_parquet('lakehouse/silver/inventory_snapshots.parquet')
    """,
    "gold_counts": """
        SELECT 'sales_gold' AS table_name, COUNT(*) AS row_count FROM read_parquet('lakehouse/gold/sales_gold.parquet')
        UNION ALL
        SELECT 'customers_gold', COUNT(*) FROM read_parquet('lakehouse/gold/customers_gold.parquet')
        UNION ALL
        SELECT 'products_gold', COUNT(*) FROM read_parquet('lakehouse/gold/products_gold.parquet')
        UNION ALL
        SELECT 'inventory_gold', COUNT(*) FROM read_parquet('lakehouse/gold/inventory_gold.parquet')
    """,
    "gold_sales_summary": """
        SELECT SUM(net_sales_amount) AS total_net_sales, COUNT(*) AS sales_rows
        FROM read_parquet('lakehouse/gold/sales_gold.parquet')
    """,
    "inventory_risk": """
        SELECT COUNT(*) AS low_stock_rows
        FROM read_parquet('lakehouse/gold/inventory_gold.parquet')
        WHERE low_stock_flag = TRUE
    """,
}

for name, sql in queries.items():
    print(f"## {name}")
    for row in con.execute(sql).fetchall():
        print(row)
    print()

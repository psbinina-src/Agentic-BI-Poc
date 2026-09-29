# Phase 1 Lakehouse Validation SQL

This file contains validation queries for the Phase 1 lakehouse contract across source, Bronze, Silver, and Gold.

## Working execution method in this environment
The validated and reliable method in this workspace is Python + DuckDB, not the direct `duckdb` CLI shell. The project has been successfully validated by running:

```powershell
python scripts/validate_phase1.py
```

The direct DuckDB CLI may be flaky or unavailable in this environment, but the same SQL statements below are valid when executed through Python/DuckDB or any compatible DuckDB client.

## Prerequisites
- DuckDB Python package is available.
- The local lakehouse folders are populated under `lakehouse/`.

## 1) Source layer validation

```sql
SELECT
  table_name,
  row_count
FROM (
  SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM read_csv_auto('lakehouse/source/customers.csv')
  UNION ALL
  SELECT 'products', COUNT(*) FROM read_csv_auto('lakehouse/source/products.csv')
  UNION ALL
  SELECT 'orders', COUNT(*) FROM read_csv_auto('lakehouse/source/orders.csv')
  UNION ALL
  SELECT 'order_lines', COUNT(*) FROM read_csv_auto('lakehouse/source/order_lines.csv')
  UNION ALL
  SELECT 'inventory_snapshots', COUNT(*) FROM read_csv_auto('lakehouse/source/inventory_snapshots.csv')
);
```

```sql
SELECT *
FROM read_json('lakehouse/source/manifest.json');
```

## 2) Bronze layer validation

```sql
SELECT
  table_name,
  row_count
FROM (
  SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM read_parquet('lakehouse/bronze/customers.parquet')
  UNION ALL
  SELECT 'products', COUNT(*) FROM read_parquet('lakehouse/bronze/products.parquet')
  UNION ALL
  SELECT 'orders', COUNT(*) FROM read_parquet('lakehouse/bronze/orders.parquet')
  UNION ALL
  SELECT 'order_lines', COUNT(*) FROM read_parquet('lakehouse/bronze/order_lines.parquet')
  UNION ALL
  SELECT 'inventory_snapshots', COUNT(*) FROM read_parquet('lakehouse/bronze/inventory_snapshots.parquet')
);
```

```sql
SELECT
  COUNT(*) AS bronze_rows_with_lineage
FROM read_parquet('lakehouse/bronze/customers.parquet')
WHERE source_file IS NOT NULL
  AND source_row_number IS NOT NULL
  AND source_run_id IS NOT NULL;
```

## 3) Silver layer validation

```sql
SELECT
  table_name,
  row_count
FROM (
  SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM read_parquet('lakehouse/silver/customers.parquet')
  UNION ALL
  SELECT 'products', COUNT(*) FROM read_parquet('lakehouse/silver/products.parquet')
  UNION ALL
  SELECT 'orders', COUNT(*) FROM read_parquet('lakehouse/silver/orders.parquet')
  UNION ALL
  SELECT 'order_lines', COUNT(*) FROM read_parquet('lakehouse/silver/order_lines.parquet')
  UNION ALL
  SELECT 'inventory_snapshots', COUNT(*) FROM read_parquet('lakehouse/silver/inventory_snapshots.parquet')
);
```

```sql
SELECT
  COUNT(*) AS customers_missing_required_fields
FROM read_parquet('lakehouse/silver/customers.parquet')
WHERE customer_id IS NULL
   OR customer_segment IS NULL
   OR region IS NULL;
```

```sql
SELECT COUNT(*) AS duplicate_order_lines
FROM (
  SELECT order_line_id, COUNT(*) AS n
  FROM read_parquet('lakehouse/silver/order_lines.parquet')
  GROUP BY order_line_id
  HAVING COUNT(*) > 1
);
```

## 4) Gold layer validation

```sql
SELECT
  table_name,
  row_count
FROM (
  SELECT 'sales_gold' AS table_name, COUNT(*) AS row_count FROM read_parquet('lakehouse/gold/sales_gold.parquet')
  UNION ALL
  SELECT 'customers_gold', COUNT(*) FROM read_parquet('lakehouse/gold/customers_gold.parquet')
  UNION ALL
  SELECT 'products_gold', COUNT(*) FROM read_parquet('lakehouse/gold/products_gold.parquet')
  UNION ALL
  SELECT 'inventory_gold', COUNT(*) FROM read_parquet('lakehouse/gold/inventory_gold.parquet')
);
```

```sql
SELECT
  SUM(net_sales_amount) AS total_net_sales,
  COUNT(*) AS sales_rows
FROM read_parquet('lakehouse/gold/sales_gold.parquet');
```

```sql
SELECT
  COUNT(*) AS low_stock_rows
FROM read_parquet('lakehouse/gold/inventory_gold.parquet')
WHERE low_stock_flag = TRUE;
```

## 5) Cross-layer contract checks

```sql
SELECT
  'bronze_customers' AS entity,
  COUNT(*) AS rows
FROM read_parquet('lakehouse/bronze/customers.parquet')
UNION ALL
SELECT
  'silver_customers',
  COUNT(*)
FROM read_parquet('lakehouse/silver/customers.parquet');
```

```sql
SELECT
  COUNT(*) AS unmatched_order_lines
FROM read_parquet('lakehouse/gold/sales_gold.parquet') s
LEFT JOIN read_parquet('lakehouse/silver/orders.parquet') o
  ON s.order_id = o.order_id
WHERE o.order_id IS NULL;
```

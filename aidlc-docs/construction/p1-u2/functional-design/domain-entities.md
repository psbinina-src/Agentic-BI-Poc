# P1-U2 Domain Entities — Bronze Ingestion and Lineage

## Entity Summary
P1-U2 is a raw-ingestion layer. Its domain entities are the accepted source entities plus a minimal lineage envelope. The Bronze domain does not restructure the business model; it preserves file data and runtime traceability only.

## Source Entities and Bronze Representation

### Customer entity
- Source: `customers.csv`
- Bronzed grain: one row per source customer row.
- Preserved source columns: `customer_id`, `customer_name`, `customer_segment`, `region`, `acquisition_channel`, `acquisition_date`, `customer_status`.
- Added metadata: `source_file`, `source_row_number`, `source_run_id`, `ingested_at`.
- Key: `customer_id` remains the primary business key; `source_run_id` is used for lineage across repeated loads.

### Product entity
- Source: `products.csv`
- Bronzed grain: one row per source product row.
- Preserved source columns: `product_id`, `product_name`, `category`, `subcategory`, `list_price`, `reorder_point`, `product_status`.
- Added metadata: `source_file`, `source_row_number`, `source_run_id`, `ingested_at`.
- Key: `product_id` remains the primary business key.

### Order entity
- Source: `orders.csv`
- Bronzed grain: one row per source order row.
- Preserved source columns: `order_id`, `customer_id`, `order_date`, `order_status`, `payment_method`, `channel`.
- Added metadata: `source_file`, `source_row_number`, `source_run_id`, `ingested_at`.
- Key: `order_id` remains the primary business key; `customer_id` remains the source relationship reference.

### Order-line entity
- Source: `order_lines.csv`
- Bronzed grain: one row per source order-line row.
- Preserved source columns: `order_line_id`, `order_id`, `product_id`, `quantity`, `unit_price`, `discount_rate`.
- Added metadata: `source_file`, `source_row_number`, `source_run_id`, `ingested_at`.
- Key: `order_line_id` remains the primary business key; `order_id` and `product_id` remain foreign keys to the source contract.

### Inventory snapshot entity
- Source: `inventory_snapshots.csv`
- Bronzed grain: one row per source snapshot row.
- Preserved source columns: `snapshot_date`, `product_id`, `inventory_on_hand`, `reorder_point`.
- Added metadata: `source_file`, `source_row_number`, `source_run_id`, `ingested_at`.
- Key: composite key (`snapshot_date`, `product_id`) remains the business key; each row also includes lineage metadata.

## Run Metadata Entity
The Bronze ingestion run itself produces a run-level metadata record.

### Load manifest fields
- `source_manifest_path`
- `source_run_id`
- `source_seed`
- `source_start_date`
- `source_end_date`
- `source_counts`
- `bronze_output_paths`
- `status` (`success` or `failed`)
- `ingested_at`
- `record_count_total`
- `checksum_status` (pass/fail)
- `source_validation_status` (pass/fail)

This run metadata is stored adjacent to the Bronze Parquet outputs and used as the contract for downstream Silver and Gold runs.

## Relationship Rules
- Source entity relationships remain the same as the original CSV contract.
- `orders.customer_id` references `customers.customer_id`.
- `order_lines.order_id` references `orders.order_id`.
- `order_lines.product_id` references `products.product_id`.
- `inventory_snapshots.product_id` references `products.product_id`.
- U2 preserves these relationships only as source data and lineage metadata; no deduplication, normalization, or business semantics are introduced.

## Out-of-Scope Entities
- Silver standardization tables, Gold dimension and fact tables, and any typed quality domain outcomes are not part of the Bronze domain model.
- U2 does not define new business semantics beyond source traceability and the raw ingest contract.

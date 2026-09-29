# P1-U3 Domain Entities — Silver Standardization and Data Quality

## Domain Model
P1-U3 creates a typed version of the accepted Bronze model without changing the business meaning of the source data.

### `customers_silver`
- Primary key: `customer_id`
- Standardized columns: `customer_segment`, `region`, `acquisition_channel`, `acquisition_date`, `customer_status`
- Retained lineage fields: `source_file`, `source_row_number`, `source_run_id`, `ingested_at`
- Quality checks: required fields, domain values, date validity, duplicate keys

### `products_silver`
- Primary key: `product_id`
- Standardized columns: `category`, `subcategory`, `list_price`, `reorder_point`, `product_status`
- Retained lineage fields: `source_file`, `source_row_number`, `source_run_id`, `ingested_at`
- Quality checks: numeric validity, domain values, duplicate keys, required fields

### `orders_silver`
- Primary key: `order_id`
- Standardized columns: `customer_id`, `order_date`, `order_status`, `payment_method`, `channel`
- Retained lineage fields: `source_file`, `source_row_number`, `source_run_id`, `ingested_at`
- Quality checks: customer reference, date validity, status domain, required fields

### `order_lines_silver`
- Primary key: `order_line_id`
- Standardized columns: `order_id`, `product_id`, `quantity`, `unit_price`, `discount_rate`
- Retained lineage fields: `source_file`, `source_row_number`, `source_run_id`, `ingested_at`
- Quality checks: numeric validity, required keys, referential integrity, positive quantity policy

### `inventory_snapshots_silver`
- Composite key: `snapshot_date`, `product_id`
- Standardized columns: `inventory_on_hand`, `reorder_point`
- Retained lineage fields: `source_file`, `source_row_number`, `source_run_id`, `ingested_at`
- Quality checks: date validity, valid product key, nonnegative inventory values, expected daily grain

## Quality Report Contract
The Silver run produces a report containing:
- check name
- check description
- table/column scope
- pass/fail result
- row or count-based evidence
- run timestamp and source run ID

This report is the required gate before P1-U4 Gold modeling begins.

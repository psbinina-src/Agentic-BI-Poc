# P1-U1 CSV Source Schema and Bronze Handoff

## File Conventions
- Encoding: UTF-8.
- Delimiter: comma; quote handling follows Python's standard CSV writer.
- Header and row ordering are stable. Dates use ISO `YYYY-MM-DD`; decimals use canonical decimal strings.
- All data is synthetic. Identifiers are stable strings; no real customer identity data is used.
- Default generation is seed `42`, inclusive date window 2023-01-01 through 2025-12-31, 10,000 customers, 1,000 products, and 100,000 order lines.
- See [generation-guide.md](generation-guide.md) for installation, commands, overrides, and failure behavior.

## `customers.csv`
**Grain**: One row per customer. **Primary key**: `customer_id`.

| Column | Type/format | Meaning |
|---|---|---|
| `customer_id` | Synthetic string | Stable ID, e.g. `CUST-000001` |
| `customer_name` | Synthetic string | Label, e.g. `Customer 000001` |
| `customer_segment` | String category | Standard, Plus, or Premium |
| `region` | String category | North, South, East, West, or Central |
| `acquisition_channel` | String category | Search, Referral, Social, or Direct |
| `acquisition_date` | ISO date | No later than the customer's first order |
| `customer_status` | String category | Active or Inactive |

## `products.csv`
**Grain**: One row per product. **Primary key**: `product_id`.

| Column | Type/format | Meaning |
|---|---|---|
| `product_id` | Synthetic string | Stable ID, e.g. `PROD-000001` |
| `product_name` | Synthetic string | Label, e.g. `Product 000001` |
| `category` | String category | Electronics, Home, Outdoor, or Apparel |
| `subcategory` | String category | Deterministic child category |
| `list_price` | Decimal | Nonnegative synthetic reference price |
| `reorder_point` | Integer | Nonnegative inventory threshold |
| `product_status` | String category | Active or Discontinued |

## `orders.csv`
**Grain**: One row per order. **Primary key**: `order_id`. **Foreign key**: `customer_id` references `customers.csv`.

| Column | Type/format | Meaning |
|---|---|---|
| `order_id` | Synthetic string | Stable ID, e.g. `ORD-0000001` |
| `customer_id` | Synthetic string | Existing customer |
| `order_date` | ISO date | Within the configured inclusive window |
| `order_status` | String category | Completed or Cancelled |
| `payment_method` | String category | Card, Wallet, or Transfer |
| `channel` | String category | Online, Retail, or Marketplace |

One or more order lines must exist for each order. Order count is derived; order-line count is configurable and exact.

## `order_lines.csv`
**Grain**: One product line per order. **Primary key**: `order_line_id`. **Foreign keys**: `order_id` references `orders.csv`; `product_id` references `products.csv`.

| Column | Type/format | Meaning |
|---|---|---|
| `order_line_id` | Synthetic string | Stable ID, e.g. `LINE-0000001` |
| `order_id` | Synthetic string | Existing order |
| `product_id` | Synthetic string | Existing product |
| `quantity` | Positive integer | Units on line |
| `unit_price` | Decimal | Synthetic transaction unit price |
| `discount_rate` | Decimal | Discount fraction from 0.00 to 0.15 |

## `inventory_snapshots.csv`
**Grain**: One product per calendar day. **Composite key**: (`snapshot_date`, `product_id`). **Foreign key**: `product_id` references `products.csv`.

| Column | Type/format | Meaning |
|---|---|---|
| `snapshot_date` | ISO date | Every date in the configured inclusive window |
| `product_id` | Synthetic string | Existing product |
| `inventory_on_hand` | Nonnegative integer | End-of-day synthetic stock level |
| `reorder_point` | Nonnegative integer | Product threshold for risk analysis |

Snapshot row count is `product_count × inclusive calendar days`. At defaults this is 1,096,000 rows.

## `manifest.json`
Written after all entity CSVs are complete and validation/scenario checks pass. Contains:
- `schema_version`, `seed`, `start_date`, `end_date`.
- `requested_volumes` and `actual_counts` by entity.
- `output_files` and SHA-256 `checksums` keyed by entity.
- `validation.passed`, validation issues, scenario-presence results, and operational `generated_at`.

**P1-U2 contract**: Require parseable `manifest.json`, `validation.passed == true`, all five paths present, and matching checksums before loading CSVs. If no valid manifest exists, treat any CSVs at the source path as unaccepted/partial output.

# P2-U1 Domain Entities — Gold Contract and Semantic Catalog

## Sales Gold (`sales_gold`)
- **Grain**: completed order line.
- **Primary key**: `order_line_id`.
- **Foreign/business keys**: `order_id`, `customer_id`, `product_id`.
- **Time key**: `order_date`.
- **Measures**: `quantity`, `unit_price`, `discount_rate`, `gross_sales_amount`, `discount_amount`, `net_sales_amount`.
- **Eligibility**: only lines attached to `Completed` orders.

## Customer Gold (`customers_gold`)
- **Grain / key**: one row per `customer_id`.
- **Attributes**: `customer_segment`, `region`, `acquisition_channel`, `acquisition_date`, `customer_status`.
- **Analytical behavior**: net sales, order count, and repeat-purchase status derive from the related completed sales fact, rather than duplicating order measures in the customer dimension.

## Product Gold (`products_gold`)
- **Grain / key**: one row per `product_id`.
- **Attributes**: `product_name`, `category`, `subcategory`, `list_price`, `product_status`.

## Inventory Gold (`inventory_gold`)
- **Grain / composite key**: one row per (`product_id`, `snapshot_date`).
- **Attributes/measures**: `inventory_on_hand`, `reorder_point`, `low_stock_flag`, `sales_velocity_units_per_day`, `stock_coverage_days`, `stock_coverage_status`.
- **Velocity**: completed units over `[snapshot_date - 30 days, snapshot_date)`, divided by 30.
- **Coverage**: on-hand divided by daily velocity for positive demand; zero with status `no_demand` when demand is zero.
- **Coverage**: on-hand divided by daily velocity for positive demand, status `calculated`; zero with status `no_demand` when demand is zero.

## Relationships
- `sales_gold.customer_id` -> `customers_gold.customer_id` (many sales lines to one customer).
- `sales_gold.product_id` -> `products_gold.product_id` (many sales lines to one product).
- `inventory_gold.product_id` -> `products_gold.product_id` (many snapshots to one product).
- Sales time is `order_date`; inventory time is `snapshot_date`. No persisted date dimension is required for this phase.
- Do not directly combine order-line sales and product-day inventory rows before aggregation; each fact has a distinct grain.

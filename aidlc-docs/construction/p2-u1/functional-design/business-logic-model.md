# P2-U1 Business Logic Model — Gold Contract and Semantic Catalog

## Purpose
Publish corrected Phase 2 Gold inputs and a governed semantic catalog over the existing sales, customer, product, and inventory model. Forecast measures remain excluded.

## Inputs and Flow
Accepted Silver customers, products, orders, order lines, and inventory snapshots -> corrected Gold outputs -> semantic facts, dimensions, and measures.

The P2-U1 implementation retains existing Phase 1 paths and Parquet contracts unless a listed semantic correction requires a schema addition.

## Business Model

### Sales Fact
- Grain: one row per order line for completed orders only.
- Keys/relationships: `order_line_id` (unique), `order_id`, `customer_id`, `product_id`, `order_date`.
- Measures: quantity, gross sales, discount, net sales, order-line count, distinct completed-order count.
- Formulas:
  - `gross_sales_amount = quantity * unit_price`
  - `discount_amount = gross_sales_amount * discount_rate`
  - `net_sales_amount = gross_sales_amount - discount_amount`
- Include a source order only when `order_status = 'Completed'`. Cancelled orders contribute to no sales or customer measures.

### Customer Dimension and Behavior
- Grain: one row per `customer_id` from `customers_gold`.
- Descriptive attributes: segment, region, acquisition channel, acquisition date, status.
- Customer sales/contribution and repeat-purchase analysis are calculated from the completed-order sales fact, grouped by customer. Repeat means more than one distinct completed `order_id`.

### Product Dimension
- Grain: one row per `product_id` from `products_gold`.
- Attributes: name, category, subcategory, list price, status.

### Inventory Fact
- Grain: one row per `product_id` and `snapshot_date`.
- Source measures: inventory on hand, reorder point, low-stock state.
- Demand velocity: for each snapshot, sum completed-order units for that product on dates from `snapshot_date - 30 days` inclusive to `snapshot_date` exclusive, then divide by 30. This is a trailing 30-calendar-day average with same-day sales excluded. If fewer than 30 calendar days of sales history exist, still divide by 30; unavailable days count as zero demand, per the selected answer.
- Stock coverage: if calculated daily velocity is positive, `inventory_on_hand / sales_velocity_units_per_day`; if velocity is zero, publish coverage as 0 and set a status indicator to `no_demand` so consumers can distinguish the sentinel from an ordinary zero-stock result.
- Status: use `calculated` for positive demand with a calculated coverage value; use `no_demand` when the 30-day demand sum is zero. Other data-quality-invalid inputs fail the Gold validation rather than silently becoming demand.
- Low stock: true when on-hand inventory is at or below a valid reorder point; false when it is above the reorder point.

## Semantic Query Capabilities
- Time roll-up by sales order date and inventory snapshot date.
- Sales by customer, segment, region, channel, product, and category.
- Customer contribution ranked by completed net sales; repeat behavior grouped by customer/segment.
- Inventory on-hand, low-stock, sales velocity, and coverage by product/category and snapshot date.
- Fact-to-dimension joins use the documented keys. Sales and inventory facts are not directly joined at row grain; cross-fact queries must aggregate each fact at compatible product/time dimensions to avoid row multiplication.

## P2-U2 Handoff Examples
Publish representative, reproducible queries and expected results for:
1. Completed net sales and distinct orders by month and region.
2. Customer net sales and distinct completed orders, including repeat-purchase identification.
3. Product-day inventory, 30-day velocity, coverage value/status, and low-stock flag by product/category.

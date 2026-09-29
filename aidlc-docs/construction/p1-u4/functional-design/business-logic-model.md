# P1-U4 Business Logic Model — Gold Models, Samples, and Phase 2 Handoff

## Purpose
P1-U4 produces the final Gold layer for sales, customer profile, and inventory analysis from the accepted Silver data. The Gold outputs support BI and semantic modeling and include documented sample queries that demonstrate the major required business questions.

## Business Model
### Core Gold Sales Model
- Grain: one row per order line.
- Key fields: `order_line_id`, `order_id`, `product_id`, `customer_id`, `order_date`.
- Measures: quantity, sales_amount, discount_amount, net_sales_amount.
- Dimensions: product, customer, date, channel, region.

### Customer Profile Model
- Grain: one row per customer with profile metrics derived from accepted Silver customer and order data.
- Dimensions: customer segment, region, acquisition channel.
- KPIs: total orders, total spend, average order value, repeat purchase indicators.

### Inventory Model
- Grain: one row per product-day snapshot.
- Metrics: inventory_on_hand, reorder_point, stock_coverage_days, low_stock_flag, inventory_velocity.
- Dimensions: product, date, category, region or channel as applicable.

## Rules
- Gold must preserve the Silver lineage and run provenance.
- Sales measures must be derived consistently from order lines and accepted order/payment status semantics.
- Inventory values must use daily product-snapshot grain.
- All derived metrics are deterministic and based on the approved Phase 1 contract.

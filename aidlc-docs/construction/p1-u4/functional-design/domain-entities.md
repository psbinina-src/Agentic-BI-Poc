# P1-U4 Domain Entities — Gold Models, Samples, and Phase 2 Handoff

## Gold Sales Fact
- Name: `sales_gold`
- Grain: order-line fact
- Core fields: `order_line_id`, `order_id`, `product_id`, `customer_id`, `order_date`, `quantity`, `unit_price`, `discount_rate`, `gross_sales_amount`, `discount_amount`, `net_sales_amount`
- Dimensions: product, customer, date, channel, region

## Gold Customer Dimension
- Name: `customers_gold`
- Grain: customer
- Fields: `customer_id`, `customer_segment`, `region`, `acquisition_channel`, `acquisition_date`, `customer_status`, `customer_profile_metrics`

## Gold Product Dimension
- Name: `products_gold`
- Grain: product
- Fields: `product_id`, `product_name`, `category`, `subcategory`, `list_price`, `product_status`

## Gold Inventory Fact
- Name: `inventory_gold`
- Grain: product-day snapshot
- Fields: `snapshot_date`, `product_id`, `inventory_on_hand`, `reorder_point`, `stock_coverage_days`, `low_stock_flag`, `inventory_velocity`

## Sample Query Contract
The Gold layer must support sample queries for:
- sales trends by period and product category
- repeat-purchase behavior by customer and segment
- inventory risk and low-stock analysis by product and date

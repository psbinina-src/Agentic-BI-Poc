# P1-U3 Business Logic Model — Silver Standardization and Data Quality

## Purpose
P1-U3 creates a typed, quality-checked Silver layer from the accepted Bronze source tables. The Silver layer preserves business meaning while keeping lineage to Bronze source rows and accepted run metadata. This stage standardizes types and validates required values before Gold data modeling begins.

## Business Flow
1. Accept Bronze output only if the Bronze source contract, manifest checks, and lineage metadata are valid.
2. Standardize each Bronze entity into a typed Silver table.
3. Apply explicit row-level and entity-level quality rules.
4. Record pass/fail quality outcomes for each rule.
5. Publish a Silver data contract and summary evidence to the downstream Gold unit.

## Standardization Rules
- Convert raw source strings to typed Silver values where the business contract and the source columns imply a specific type.
- Preserve canonical keys (`customer_id`, `product_id`, `order_id`, `order_line_id`, `snapshot_date`) as stable identifiers.
- Standardize dates to ISO date values.
- Standardize decimal values to canonical numeric representation consistent with their source contract.
- Keep row-level lineage columns to maintain source traceability.

## Quality Gates
A Silver run must report pass/fail status for the following categories:
- required-field checks
- type checks
- null/invalid-value checks
- duplicate-key checks
- referential-integrity checks
- domain checks for status and category fields

Any critical failure blocks the Silver handoff to Gold.

## Data Model Outline
- `customers_silver`: typed customer dimension with standardized region, segment, channel, status, and dates
- `products_silver`: typed product dimension with category, subcategory, price, reorder point, and status
- `orders_silver`: typed order fact-like table retaining the required key and date/status semantics
- `order_lines_silver`: typed order-line table with quantity, price, and discount conditions
- `inventory_snapshots_silver`: typed daily product-snapshot table with date and inventory values

Each table retains the Bronze lineage fields plus the business keys and values required for later Gold modeling.

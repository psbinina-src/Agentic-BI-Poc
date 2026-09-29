# P1-U3 Business Rules — Silver Standardization and Data Quality

## Core Rules
1. Bronze is the source of truth; Silver only standardizes and validates, never invents values.
2. Required business keys must remain stable and unique where the source contract defines them.
3. Date fields must be valid ISO dates and must be kept in canonical format.
4. Quantity, price, reorder point, and numeric values must be typed consistently with the source contract.
5. Null values are allowed only where the source contract explicitly permits them; otherwise they are treated as quality failures.
6. Duplicate keys are blocking failures when they violate the expected entity grain.
7. Referential integrity checks are required between `orders.customer_id`, `order_lines.order_id`, `order_lines.product_id`, and `inventory_snapshots.product_id`.
8. Status/category domain checks are required for fields such as `order_status`, `customer_status`, `product_status`, `category`, and `region`.
9. Critical data-quality failures block the Silver-to-Gold handoff.
10. The quality report must list every check and its pass/fail result in a machine-readable and human-readable way.

## Quality Policy
The Silver unit must produce a quality report with named checks such as:
- `required_fields_present`
- `valid_iso_dates`
- `duplicate_primary_keys`
- `null_check`
- `domain_values_valid`
- `referential_integrity_ok`

The report must be inspectable and deterministic for downstream business users and the P1-U4 Gold unit.

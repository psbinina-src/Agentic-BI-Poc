# Phase 2 Requirements Verification Questions

Please complete each `[Answer]:` field. Phase 2 is being planned for one data engineer working sequentially, with concise design artifacts and implementation-focused units.

## Question 1: Forecast scope
The Phase 1 Gold handoff documents sales, customer, product, and inventory Parquet outputs, but no forecast Gold output is listed. How should Phase 2 handle forecast measures?

A) Keep Phase 2 on the currently published Gold outputs; defer forecast measures until a forecast Gold dataset is available.

B) Add or complete the Phase 1 forecast Gold output as a prerequisite, then model its measures in Phase 2.

X) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 2: Inventory metric semantics
The current Gold inventory fields include `stock_coverage_days` (calculated as inventory on hand divided by reorder point) and `inventory_velocity` (currently copied from inventory on hand). Which approach should the semantic layer take?

A) Expose only meanings supported by the current data: label the ratio as a stock-to-reorder-point ratio, treat inventory on hand as a dated snapshot, and defer true coverage-days and sales-velocity metrics until their Gold calculations are corrected.

B) Correct or extend the Phase 1 Gold calculations first, then expose true coverage-days and sales-velocity metrics in Phase 2.

X) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 3: Property-Based Testing Extension
Should property-based testing rules be enforced for this project?

A) Yes — enforce all property-based testing rules as blocking constraints.

B) Partial — enforce them only for pure functions and serialization round-trips.

C) No — skip property-based testing rules. This matches the current project configuration.

X) Other (please describe after [Answer]: tag below)

[Answer]: C

## Question 4: Security Baseline Extension
Should security baseline rules be enforced for this project?

A) Yes — enforce all security rules as blocking constraints.

B) No — skip the security baseline. This matches the current project configuration.

X) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 5: Resiliency Baseline Extension
Should the resiliency baseline be applied to this project?

A) Yes — apply the resiliency baseline as directional best practices and design-time guidance.

B) No — skip the resiliency baseline. This matches the current project configuration and supports rapid PoC iteration.

X) Other (please describe after [Answer]: tag below)

[Answer]: B

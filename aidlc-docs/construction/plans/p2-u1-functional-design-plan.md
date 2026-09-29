# P2-U1 Functional Design Plan — Gold Contract and Semantic Catalog

## Scope and Baseline
- Story: P2-US-1, discover governed metrics and dimensions over Gold.
- Unit: [P2-U1 definition](../../inception/application-design/p2/units/unit-of-work.md).
- Preserve order-line sales grain and product-day inventory grain from Phase 1.
- Sales measures use completed orders only. Forecast measures are deferred.
- Correct inventory demand/coverage semantics in Gold before publishing them in Cube.
- Keep design concise; no frontend components are in scope.

## Design Checklist
- [x] Define the P2-U1 business logic model and Gold-to-semantic flow.
- [x] Specify sales, customer, product, and inventory entities, keys, grains, and relationships needed by P2-U1.
- [x] Define completed-order sales measures and distinct-order/repeat-customer semantics.
- [x] Define demand velocity and stock coverage formulas, time-window alignment, and edge-case outcomes using the answers below.
- [x] Define semantic catalog metadata and representative sales/customer/inventory query outcomes for the P2-U2 handoff.
- [x] Define validation rules that prevent cancelled orders, duplicate joins, or invalid/unsupported members from corrupting metrics.
- [x] Validate design against Phase 2 requirements, approved application design, and P2-U1 handoff criteria.
- [x] Generate `business-logic-model.md`, `business-rules.md`, and `domain-entities.md` under `aidlc-docs/construction/p2-u1/functional-design/`.

## Question 1: Demand lookback and snapshot alignment
How should daily product sales velocity be calculated for each inventory snapshot? The lookback end date determines whether sales on the snapshot date can be counted before that day's stock measurement.

A) Use the 30 complete calendar days strictly before the snapshot date; velocity is completed-order units divided by 30. Require the full 30-day history before publishing the rate. (Recommended; avoids same-day look-ahead.)

B) Use the 90 complete calendar days strictly before the snapshot date; velocity is completed-order units divided by 90. Require the full 90-day history.

X) Other (please describe after [Answer]: tag below)

[Answer]: A - simple

## Question 2: Zero demand and insufficient history
For an inventory snapshot where the selected full lookback window is available, but completed-order demand is zero—or where the full lookback history is not available—what should Gold publish?

A) With a complete window and zero demand, publish velocity as 0 and coverage as NULL with a no-demand indicator. With incomplete history, publish velocity and coverage as NULL with an insufficient-history indicator. (Recommended; do not invent infinite coverage.)

B) Use any available partial history; with zero demand, publish coverage as 0 and distinguish the case using a status field.

X) Other (please describe after [Answer]: tag below)

[Answer]: B - simple

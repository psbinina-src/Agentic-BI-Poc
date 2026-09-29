# Functional Design Plan — P1-U4 Gold Models, Samples, and Phase 2 Handoff

## Unit Context
- **Unit**: P1-U4 — Gold models, samples, and Phase 2 handoff.
- **Story**: P1-US-2 — publish the final business-ready Gold layer for sales, customer profile, and inventory analysis.
- **Owner**: One data engineer.
- **Predecessor**: P1-U3 Silver layer must be accepted and quality-passing before Gold begins.

## Planning and Generation Steps
- [x] Confirm the accepted Silver contract and the quality-report gate.
- [x] Define the Gold dimensional grain and model boundaries.
- [x] Define the customer, sales, and inventory Gold outputs and sample queries.
- [x] Define the final Phase 2 readiness contract and handoff evidence.
- [x] Generate the Gold functional design artifacts.

## Gold Model Summary
P1-U4 creates the final business-ready Gold layer from the accepted Silver tables. It includes the sales-order-line fact and the inventory-snapshot fact, plus the customer and product dimensions needed for downstream BI and semantic modeling. The unit also includes curated sample business queries and a documented Phase 2 handoff.

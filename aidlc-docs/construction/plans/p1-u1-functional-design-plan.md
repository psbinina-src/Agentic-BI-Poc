# Functional Design Plan — P1-U1 Synthetic Generator and Source Contract

## Unit Context
- **Unit**: P1-U1 — Synthetic generator and source contract.
- **Story**: P1-US-1 — reproducibly generate synthetic e-commerce source data and publish stable inputs for Bronze.
- **Owner**: One data engineer; work is sequential.
- **Inputs**: Approved generator decisions and configurable three-year dataset default; no production or real personal data.
- **Outputs**: Customer, product, order/order-line, and inventory CSV source entities; manifest, schemas/keys, configuration contract, and reproducibility evidence under the source-input area.
- **Dependency**: None. Bronze ingestion is the downstream unit and consumes the source manifest/CSV contract.

## Planning and Generation Steps
- [x] Resolve the functional questions below and the follow-up; verify answers are specific and consistent with the approved Phase 1 requirements.
- [x] Define the source-domain entities, grains, key relationships, and required analytic attributes from the approved answer.
- [x] Define deterministic generation inputs, fixed defaults, date coverage, and volume interpretation.
- [x] Define scenario-generation rules for trends, regions/categories, repeat purchasing, and inventory-risk demonstration.
- [x] Define valid-record rules, configuration validation, and behavior for invalid configurations or test-only edge cases.
- [x] Generate `aidlc-docs/construction/p1-u1/functional-design/business-logic-model.md`.
- [x] Generate `aidlc-docs/construction/p1-u1/functional-design/business-rules.md`.
- [x] Generate `aidlc-docs/construction/p1-u1/functional-design/domain-entities.md`.
- [x] Validate that the source contract supports P1-US-1 and downstream daily inventory, sales, customer, and forecast use cases without introducing real personal data.
- [x] Update the plan and AI-DLC state; present the completed artifacts for explicit review and approval.

## Clarification Questions
Please answer every `[Answer]:` field. Use `X) Other` for a custom response and provide the details after the tag. These questions concern P1-U1's source-domain behavior; implementation syntax and detailed code structure remain for later stages.

### Question 1: Source entities and grains
Which source entity contract should the generator publish?

A) Separate customers, products, order headers, order lines, and daily product inventory snapshots; order lines reference both order and product, and headers reference customers (recommended; supports the requested sales and inventory grains)

B) Customers, products, and order lines only; derive order-level information from line records and inventory from another entity

C) Customers, products, orders/order lines, and inventory movements; derive daily inventory snapshots downstream

X) Other (please describe after [Answer]: tag below)

[Answer]: A

### Question 2: Fixed reproducibility defaults
Which fixed default date window and seed should accompany the already-approved three-year configurable period and volume defaults?

A) 2023-01-01 through 2025-12-31 inclusive, default seed `42`; both remain configurable (recommended; fixed historical window gives reproducible defaults)

B) Use another fixed three-year date window and seed; specify both after `[Answer]:`

C) Anchor the three-year default window to the current date while fixing seed `42`

X) Other (please describe after [Answer]: tag below)

[Answer]: C

**Follow-up resolved**: The user selected a fixed historical three-year default; use the previously offered 2023-01-01 through 2025-12-31 inclusive and seed `42`. Dates and seed remain configurable.

### Question 3: Analytic scenario construction
How should the generator ensure the required analysis scenarios are present?

A) Combine seeded variation with documented, deterministic scenario profiles: repeat buyers, distinguishable time/region/category patterns, and known low-stock/high-velocity products (recommended; guarantees demonstrable cases)

B) Use only seeded probabilistic variation and document any scenarios that happen to occur

C) Use fixed, fully scripted values for all business entities and transactions

X) Other (please describe after [Answer]: tag below)

[Answer]: A

### Question 4: Invalid data and test edge cases
How should malformed, duplicate, or referentially invalid records be handled by the source generator?

A) Default source generation emits valid business records only; provide separate opt-in test fixtures for negative data-quality cases (recommended; keeps Bronze source valid while enabling quality-rule tests)

B) Support an explicit configuration option to inject a documented proportion of invalid records into generated source data

C) Generate only valid records and do not provide negative test fixtures

X) Other (please describe after [Answer]: tag below)

[Answer]: C

## Category Applicability
- Business logic, domain entities, business rules, data flow, validation/error handling, and scenario/edge-case questions are applicable and covered above.
- Integration is local and file-based; no external system or API exists. The output CSV/manifest contract with U2 is already established by Application Design and Unit Generation.
- Frontend/UI questions are not applicable because P1-U1 is a generator/source-data unit with no user interface.

## Completion Gate
After answers are reviewed, resolve any ambiguity before producing the three functional design artifacts. Explicit approval of the completed functional design is required before proceeding to the next stage for P1-U1.

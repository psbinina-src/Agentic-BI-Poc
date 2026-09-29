- [x] Validate story coverage, unit boundaries, handoff evidence, and consistency with approved Phase 2 design.
# Phase 2 Unit of Work Plan

## Approved Baseline
- Requirements and Workflow Plan are approved.
- Phase 2 Application Design is approved; see `aidlc-docs/inception/application-design/p2/`.
- One data engineer owns two sequential units. Preserve the P2-U1-to-P2-U2 gate; no parallel ownership.
- No new decomposition questions are needed: story ownership/grouping, unit boundaries, dependencies, local-only runtime, domain split, and application components were explicitly confirmed in the approved requirements, workflow plan, and application design.
- Keep Phase 1 artifacts unchanged. Phase 2 unit-generation artifacts will be stored under `aidlc-docs/inception/application-design/p2/units/`.

## Planning Steps
- [x] Define exactly two unit boundaries, responsibilities, and concise outcomes.
- [x] Map supplied P2-US-1 and P2-US-2 to the two units; keep one engineer as owner.
- [x] Define P2-U1 -> P2-U2 dependency and blocking handoff evidence.
- [x] Include native Cube Core + DuckDB feasibility as a P2-U1 exit check; if it fails without containers, stop before building interfaces.
- [x] Generate Phase 2 `unit-of-work.md`, `unit-of-work-dependency.md`, and `unit-of-work-story-map.md` in the Phase 2 units folder.
- [ ] Validate story coverage, unit boundaries, handoff evidence, and consistency with approved Phase 2 design.

## Proposed Decomposition

### P2-U1 — Gold Contract and Semantic Catalog
- Verify/correct the completed-order sales and inventory velocity/coverage Gold inputs.
- Prove native Cube Core + DuckDB can read the local Gold Parquet data without Docker or a hosted service.
- Define Cube models, stable semantic names, dimensions, joins, and governed measures.
- Publish contract, catalog metadata, focused tests, and representative expected results as the P2-U2 handoff.

### P2-U2 — Local Interfaces and Parity
- Depends on P2-U1's passing contract, model, and representative expected results.
- Run Cube Core locally with REST and SQL APIs enabled.
- Implement the approved small, read-only Python MCP stdio adapter calling Cube REST with allowlisted members and bounded results.
- Verify REST/MCP/SQL parity and publish concise setup/endpoint examples and test evidence.

## Handoff Gate
P2-U2 must not begin until P2-U1 demonstrates: (1) documented Gold grains/keys/formulas; (2) native Cube Core + DuckDB local startup and successful representative semantic queries; (3) stable semantic member names; and (4) expected results for sales, customer, and inventory examples.

## Approval
**Plan approved** by the user request "do rapid development of all unites" on 2026-09-29; the three Phase 2 unit artifacts have been generated. Explicit review approval of the generated artifacts is still required before Construction begins. No application code has been generated yet.

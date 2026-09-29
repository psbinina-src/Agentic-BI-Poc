# Phase 2 Unit Dependencies

## Dependency Matrix

| Unit | Depends on | Dependency type | Gate |
|---|---|---|---|
| P2-U1 — Gold Contract and Semantic Catalog | Approved Phase 1 Gold data and Phase 2 requirements/design | Upstream contract | Verify/correct Gold semantics and prove native Cube Core + DuckDB feasibility |
| P2-U2 — Local Interfaces and Parity | P2-U1 | Blocking sequential dependency | Do not start interface implementation until P2-U1 handoff is accepted |

## P2-U1 to P2-U2 Handoff
P2-U1 publishes:
- Gold grains, keys, fields, and corrected sales/inventory metric semantics.
- Stable Cube model member names, descriptions, measures, dimensions, joins, and supported filters.
- Successful native Cube Core + DuckDB local startup and representative query evidence over Gold Parquet.
- Expected result fixtures/examples for sales, customer, and inventory queries.
- Focused test output and a pass/fail handoff checklist.

P2-U2 uses this contract directly for REST, SQL, and MCP integration tests. If any required evidence fails or the local native runtime cannot be proven, stop and resolve the Gold/runtime issue before interface work; do not bypass Cube or add a hosted/container dependency.

## Execution
Single-owner sequence: P2-U1 -> handoff review -> P2-U2 -> integrated Build and Test. No parallel unit development is planned.

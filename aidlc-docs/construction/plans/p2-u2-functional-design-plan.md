# P2-U2 Functional Design Plan — Local Interfaces and Parity

## Unit Context
- Story: P2-US-2 — consume the same governed metrics through REST, MCP, and SQL-compatible BI access.
- Dependency: P2-U1 implementation and handoff are approved; use its four Cube models and REST-vs-DuckDB expected-result validator.
- Components: Cube REST/SQL APIs and a small read-only Python MCP stdio adapter; one canonical Cube metric layer.
- Owner: one data engineer, sequential work; keep this unit focused on interface contracts, tests, and setup documentation.
- NFR work for local listener/authentication safety is a separate required P2-U2 stage after Functional Design; the current Cube Core wildcard-bind finding must be resolved there before service exposure.

## Functional Design Checklist
- [x] Define the local MCP tool inputs/outputs for catalog discovery and governed metric queries.
- [x] Specify allowed semantic member names, filters, date inputs, and result bounds.
- [x] Specify error behavior for unsupported members, filters, malformed requests, and Cube errors.
- [x] Define REST/MCP/SQL parity cases and expected results using the approved P2-U1 catalog baseline.
- [x] Define local SQL/BI connection example fields without placing credentials in the repository.
- [x] Generate concise `business-logic-model.md`, `business-rules.md`, and `domain-entities.md` for P2-U2.
- [x] Validate that no adapter redefines metrics, directly accesses Gold, or accepts arbitrary SQL.

## Question 1: MCP query surface and result bounds
How should the local MCP adapter constrain metric-query requests?

A) Keep a small, read-only contract: allowlisted Cube measures/dimensions; equality and `inDateRange` filters only; optional time granularity; default 100 rows, hard maximum 500; reject arbitrary SQL and every unsupported filter/member. (Recommended for the PoC.)

B) Forward all Cube-supported filters/operators and rely on Cube validation, while enforcing a fixed result limit of 500.

X) Other (please describe after [Answer]: tag below)

[Answer]: B — forward Cube-supported filters/operators after validating public member names and input shape; enforce a 500-row hard cap.

## Plan Approval
**Approved** by the user on 2026-09-30: "approved , keep it simple for simple funcationality finish development". The functional design uses public-member validation, Cube-supported filter/operators, default result limit 100 / hard maximum 500, and rejects arbitrary SQL. No P2-U2 implementation begins until its required NFR Design is approved.

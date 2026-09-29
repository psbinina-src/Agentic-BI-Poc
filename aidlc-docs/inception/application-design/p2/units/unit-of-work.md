# Phase 2 Units of Work

> **Scope amendment (2026-09-30):** The Cube semantic catalog and multi-interface work described below is superseded for the current delivery. P2-U2 is now the local Gold REST API defined in [the current code-generation plan](../../../../construction/plans/p2-u2-code-generation-plan.md); P2-U1 Cube artifacts remain optional historical reference.

## Delivery Model
- One data engineer owns the work end-to-end and executes units sequentially.
- Keep the implementation to two units; P2-U2 cannot start until the P2-U1 handoff passes.
- Code layout details are deferred to the Code Generation plan; preserve the existing Phase 1 modules and data.

## P2-U1 — Gold Contract and Semantic Catalog
**Story**: P2-US-1 — discover governed metrics and dimensions over Gold.

**Outcome**: Correct/verify the Gold measures needed for Phase 2 and publish the version-controlled Cube model/catalog over the local Gold data.

**Responsibilities**
- Verify sales data includes only completed orders; correct Gold output if needed.
- Correct inventory sales velocity and stock coverage calculations with formulas and edge cases established in Functional Design.
- Verify native, non-container Cube Core + DuckDB access to the Gold Parquet files. This is an early exit gate, not a reason to add hosted services or containers.
- Define semantic facts, dimensions, keys, joins, metrics, descriptions, and stable member names in Cube model files.
- Validate model compilation and representative queries; document expected results and the data contract for U2.

**Exit / Handoff Evidence**
1. Documented Gold table grains, keys, relevant columns, and measure formulas.
2. Native Cube Core + DuckDB starts and queries local Gold without Docker, WSL, or hosted services.
3. Cube model/catalog compiles and discovery metadata shows the agreed stable members.
4. Representative sales, customer, and inventory expected results are recorded and verified.
5. Focused Gold and semantic tests pass.

## P2-U2 — Local Interfaces and Parity
**Story**: P2-US-2 — access the same governed metrics through supported consumer interfaces.

**Outcome**: Provide local REST, SQL-compatible BI access, and MCP access to the same Cube model, with concise parity and setup evidence.

**Responsibilities**
- Configure Cube Core REST and Postgres-protocol SQL APIs for local use.
- Implement the approved small, read-only Python MCP stdio adapter calling Cube REST metadata/load APIs.
- Allowlist semantic member names and supported filters; bound result sizes; reject arbitrary SQL and unsupported query members.
- Add representative integration and parity tests for REST, SQL, and MCP against P2-U1 expected results.
- Document local configuration, environment variables, startup, endpoints, MCP client setup, and SQL/BI example.

**Entry / Exit Evidence**
- Entry: P2-U1's complete handoff is reviewed and passing.
- Exit: Required local interfaces run; equivalent requests match P2-U1 expected results; focused tests pass; setup and endpoints are documented.

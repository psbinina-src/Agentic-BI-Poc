# Phase 2 Application Design — Local Open Semantic Layer

> **Scope amendment (2026-09-30):** This approved Cube/MCP/SQL design is retained as historical context and is superseded for current delivery by the local Gold REST API. See [current Phase 2 requirements](../../../../requirements/phased/phase-2-semantic-layer-mcp-rest.md) and [P2-U2 code plan](../../../construction/plans/p2-u2-code-generation-plan.md). Do not implement or start Cube/MCP/SQL as part of this increment.

## Purpose and Approved Direction
Implement a small, local-first semantic layer over Phase 1 Gold files. Cube Core is the canonical semantic model; Cube REST and SQL APIs serve consumers, and a minimal local Python MCP adapter provides local MCP access. No Cube Cloud, hosted semantic service, Docker, WSL, or other container runtime is a prerequisite.

## Components
1. **Gold Contract** — P2-U1 corrects/verifies completed-order sales eligibility and inventory demand/coverage inputs, documents grains/keys, and publishes expected result examples.
2. **Cube Core Semantic Service** — version-controlled model and local configuration map Gold Parquet data through DuckDB and expose catalog, REST, and Postgres-protocol SQL APIs.
3. **Local MCP Adapter** — a Python MCP stdio process exposing a small read-only discovery/query tool set. It calls Cube REST, validates allowlisted semantic members and bounded filters/results, and never executes SQL or reads Gold directly.
4. **Consumers** — applications use REST; BI validation uses Cube SQL; MCP clients use the local adapter.

## High-Level Flow
P2-U1 Gold contract -> DuckDB local Gold access -> Cube semantic model -> REST / SQL consumers.

MCP clients -> local Python MCP adapter -> validated Cube REST requests -> same Cube semantic model.

## Units and Handoffs
- **P2-U1: Gold contract and semantic catalog.** Publish corrected or verified Gold semantics, Cube model, stable names, representative expected results, and model-validation evidence.
- **P2-U2: Local interfaces and parity.** After the P2-U1 handoff passes, wire native local startup, REST/SQL access, MCP adapter, focused interface tests, parity evidence, and setup instructions.
- One data engineer owns both units sequentially. Parity validation remains in P2-U2; no separate parity unit is created.

## Local Runtime and Safety Boundaries
- Configure Cube's DuckDB connection to read the local Gold path; keep paths, Cube API secret, and SQL credentials in local environment configuration, not source control.
- Run native processes on loopback only. Do not expose Cube development endpoints to a network or treat development mode as production security.
- Validate native Cube Core + DuckDB operation against Gold Parquet without a container before proceeding with interface integration. If this cannot be shown for the selected open-source release, stop and request a direction change instead of silently adding infrastructure.
- Reject arbitrary SQL at the MCP boundary. REST and SQL requests remain subject to Cube's semantic model and configured query controls.

## Deferred to Functional Design
Exact sales/inventory formula corrections, sales-velocity lookback, stock-coverage behavior for zero or insufficient demand, Cube model member names, filter allowlists, query limits, and representative parity inputs/results are defined per unit before implementation.

## Interface Verification Basis
Cube's official documentation describes its REST (JSON) API and a Core Postgres-protocol SQL API; the SQL API must be enabled in local configuration. The documented Cube MCP connector is a hosted HTTPS/OAuth service, so this design uses a small local adapter to honor the approved local-only MCP requirement. DuckDB's Cube configuration supports a local database path; direct Parquet modeling and native host startup remain explicit feasibility checks for P2-U1.

## Traceability
- Approved requirements: [Phase 2 requirements](../../requirements/p2-requirements.md).
- Approved workflow: [Phase 2 execution plan](../../plans/p2-execution-plan.md).
- Supplied stories: P2-US-1 (catalog discovery) and P2-US-2 (governed access across interfaces).

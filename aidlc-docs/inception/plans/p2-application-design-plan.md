# Phase 2 Application Design Plan

## Context
- Approved requirements: `aidlc-docs/inception/requirements/p2-requirements.md`.
- Approved workflow: two sequential units, one data engineer, local open-source Cube Core, no container runtime, and rapid implementation focus.
- Preserve the existing Phase 1 application-design artifacts; create Phase 2 design artifacts under `aidlc-docs/inception/application-design/p2/`.
- Official Cube documentation confirms local DuckDB configuration, a Core REST API, and a Cube Core Postgres-protocol SQL API. The documented Cube MCP connector is a hosted HTTPS/OAuth endpoint, not the required native local MCP service; a small local MCP adapter may be needed.

## Design Plan
- [x] Generate `components.md` defining the Phase 2 Gold contract, Cube Core semantic model/service, and minimal MCP adapter responsibilities.
- [x] Generate `component-methods.md` with concise high-level interfaces and inputs/outputs.
- [x] Generate `services.md` describing native local startup, REST/SQL use, and MCP-to-Cube request flow.
- [x] Generate `component-dependency.md` showing Gold -> Cube Core -> REST/SQL consumers and the local MCP adapter.
- [x] Generate `application-design.md` consolidating the approved Phase 2 design and handoffs.
- [x] Verify local DuckDB Gold path and native (non-container) Cube Core start are explicit design constraints; defer the runnable proof to P2-U1 code-generation/build checks.
- [x] Verify Phase 2 component boundaries and dependencies support the two approved sequential units.
- [x] Validate all artifacts and preserve existing Phase 1 documents.

## Question 1: MCP integration boundary
Cube's documented MCP endpoint is hosted, while Phase 2 requires local-only operation. Which small integration should the design use?

A) Add a local, read-only Python MCP server with a few allowlisted discovery/query tools that calls Cube Core's local REST metadata and load APIs. Do not forward arbitrary SQL. This preserves MCP and keeps Cube as the metric authority.

B) Do not add a local MCP server; defer MCP and use Cube REST and SQL only. This changes the approved P2 MCP requirement and would require a requirements change.

X) Other (please describe after [Answer]: tag below)

[Answer]: A - keep it simple; implement the local read-only Python MCP adapter over Cube REST.

## Assumptions carried forward (not requiring new decisions)
- Use Cube Core REST and SQL APIs locally for the interfaces they provide; SQL API is explicitly enabled in native configuration and has a documented local endpoint.
- Use local DuckDB over the Gold Parquet files, with the Gold path supplied through local environment/configuration.
- Keep Cube's development interface bound to loopback only; keep the API secret and SQL credentials local and untracked.
- Defer exact business formulas and edge cases to each unit's Functional Design.
- Native Cube Core/DuckDB startup feasibility is an early implementation gate. If the supported Cube Core release cannot meet the approved no-container constraint, stop and present the smallest alternative before adding extra infrastructure.

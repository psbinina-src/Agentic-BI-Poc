# Phased Requirements Overview

This folder contains the project requirements organized by implementation phase.

For a recorded end-to-end walkthrough, use the [AI-DLC phase demo runbook](../../aidlc-docs/phase-demo-runbook.md).

## Cross-Phase Runtime Baseline

- Run application components as native local processes; Docker, Docker Compose, WSL, and a container runtime are not prerequisites for this PoC.
- Document the local prerequisites, environment configuration, service endpoints, and startup order as components are introduced.
- Keep lakehouse files and DuckDB query execution local. Use the OpenAI API as the selected hosted LLM provider; its API key must be supplied locally and excluded from version control.
- The OpenAI API is an external dependency, so the PoC is local-first but not fully offline or entirely cloud-independent.
- These decisions are the cross-phase baseline and take precedence over conflicting runtime or LLM wording in individual source inputs.

## Single-Engineer Delivery Baseline

The phases are delivered sequentially by one data engineer. Keep units concise and prioritize an end-to-end working proof while preserving verifiable contracts and phase acceptance checks.

- Give each unit one accountable owner and avoid parallel work assumptions.
- Confirm contracts and boundaries before implementing downstream phases.
- Observe each phase's handoff gate before downstream work.
- Each unit must have a verifiable acceptance check, and each phase must pass its integration and acceptance checks before its outputs are treated as a downstream contract.
- Record ownership changes before starting the affected phase; keep story/unit IDs stable for traceability.

## Phase 1: Lakehouse Foundation and Gold Data Model

- File: [phase-1-lakehouse-gold-data-model.md](phase-1-lakehouse-gold-data-model.md)
- Covers: Bronze, Silver, and Gold lakehouse layers for BI use cases

## Phase 2: Local Gold Data REST API

- File: [phase-2-semantic-layer-mcp-rest.md](phase-2-semantic-layer-mcp-rest.md)
- Covers: Gold catalogue/schema discovery, documented model relationships, and bounded local REST data access for Phase 3. A semantic layer, Cube, MCP, and SQL/BI integration are deferred.

## Phase 3: Agentic BI Implementation

- File: [phase-3-agentic-bi-implementation.md](phase-3-agentic-bi-implementation.md)
- Covers: a simple local prompt dashboard, OpenAI tool-calling over the Phase 2 Gold REST API, concise insights, and validated Vega-Lite charts. LangGraph/Next.js and multi-widget canvases are deferred.

## Phase 4: Static Business Intelligence Dashboard

- File: [phase-4-static-bi-dashboard.md](phase-4-static-bi-dashboard.md)
- Covers: the implemented static Product Sales & Inventory Monitor over Phase 1 Gold Parquet; Metabase and semantic-SQL parity are deferred.

## Overall Delivery Flow

1. Build the lakehouse foundation and Gold data model.
2. Expose the Gold model through a local REST API.
3. Build the Agentic BI experience on the Phase 2 API.
4. Deliver the static BI dashboard directly over Gold as a parallel validation layer.

Within each phase, use its stated single-engineer slices and acceptance criteria. Phase 3 consumes the Phase 2 REST contract. Phase 4 reads Gold directly and is an independent validation view; its values can be compared with Phase 3 when that flow is available.

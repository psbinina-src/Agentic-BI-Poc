# Phased Requirements Overview

This folder contains the project requirements organized by implementation phase.

## Cross-Phase Runtime Baseline

- Run application components as native local processes; Docker, Docker Compose, WSL, and a container runtime are not prerequisites for this PoC.
- Document the local prerequisites, environment configuration, service endpoints, and startup order as components are introduced.
- Keep lakehouse files and DuckDB query execution local. Use the OpenAI API as the selected hosted LLM provider; its API key must be supplied locally and excluded from version control.
- The OpenAI API is an external dependency, so the PoC is local-first but not fully offline or entirely cloud-independent.
- These decisions are the cross-phase baseline and take precedence over conflicting runtime or LLM wording in individual source inputs.

## Two-Developer Delivery Baseline

The phase documents define stories and independently verifiable units for a two-developer team. Developer A and Developer B are role labels; confirm named owners at each phase kickoff. The refined requirement's Section 10.1 is the cross-phase story/unit ownership baseline.

- Give each unit one accountable owner; avoid concurrent edits to the same component or file.
- Agree shared contracts and boundaries before parallel work begins.
- Work may proceed in parallel within a phase when units have no unresolved dependency; observe each phase's handoff gate before integration or downstream work.
- Each unit must have a verifiable acceptance check, and each phase must pass its integration and acceptance checks before its outputs are treated as a downstream contract.
- Record ownership changes before starting the affected phase; keep story/unit IDs stable for traceability.

## Phase 1: Lakehouse Foundation and Gold Data Model

- File: [phase-1-lakehouse-gold-data-model.md](phase-1-lakehouse-gold-data-model.md)
- Covers: Bronze, Silver, and Gold lakehouse layers for BI use cases

## Phase 2: Semantic Layer Implementation

- File: [phase-2-semantic-layer-mcp-rest.md](phase-2-semantic-layer-mcp-rest.md)
- Covers: semantic modeling, metrics, REST, MCP, and BI integration

## Phase 3: Agentic BI Implementation

- File: [phase-3-agentic-bi-implementation.md](phase-3-agentic-bi-implementation.md)
- Covers: conversational analytics, query orchestration, and dynamic visualization

## Phase 4: Static Business Intelligence Dashboard

- File: [phase-4-static-bi-dashboard.md](phase-4-static-bi-dashboard.md)
- Covers: traditional dashboard experience for sales, customer, and inventory analytics

## Overall Delivery Flow

1. Build the lakehouse foundation and Gold data model
2. Implement the semantic layer on top of the Gold model
3. Add the Agentic BI conversational experience
4. Deliver the static BI dashboard as a parallel validation layer

Within each phase, use the developer slices in its phase requirement. Phase 4 depends on the Phase 2 semantic SQL contract and may be developed after that contract is stable; its dashboard values are validated against the Agentic BI flow when Phase 3 is available.

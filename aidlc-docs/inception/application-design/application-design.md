# Phase 1 Application Design

## Purpose
This design defines the high-level software components and orchestration for the approved local Phase 1 data flow: deterministic synthetic CSV inputs, Bronze ingestion, DuckDB SQL transformations, quality checks, Gold analytical outputs, and sample queries. It does not replace the detailed data/business-rule design planned for the Construction phase.

## Confirmed Design Choices
- **Component organization**: One Python project with separate modules for generation, Bronze ingestion, Silver/Gold transformation, quality checks, and query/demo helpers.
- **Pipeline entry points**: Stage-specific commands plus a command to run the complete flow.
- **Component communication**: Documented CSV/Parquet files are explicit stage contracts; pass local paths and configuration between command stages.
- **Repository layout**: Python and SQL are together under `src/`; tests are in `tests/`; lakehouse source and Bronze/Silver/Gold data remain isolated under root `lakehouse/` subfolders.
- **Runtime**: Native local process with DuckDB embedded in the stage that queries or transforms files. No service process, HTTP API, container runtime, or external data service is required.
- **Ownership**: One data engineer owns all components and runs dependent work sequentially.

## High-Level Architecture

| Component | Responsibility | Primary inputs | Primary outputs |
|---|---|---|---|
| Configuration and Path Resolver | Load defaults/overrides and provide validated paths/settings | Config file and CLI overrides | Shared config and resolved paths |
| Synthetic Source Generator | Create reproducible synthetic customers, products, orders/order lines, and inventory | Seed, date range, configured volumes | CSV source files and manifest |
| Bronze Ingestion | Load source CSV while retaining raw business values and adding load metadata | CSV and manifest | Bronze Parquet and load result |
| Silver/Gold Transformation Runner | Execute DuckDB SQL in dependency order | Bronze/Silver Parquet and SQL assets | Silver and Gold Parquet |
| Data Quality Validator | Run configured quality checks at data-layer boundaries | Source and layer outputs | Quality reports and pass/fail result |
| Gold Query and Demo Helpers | Run agreed sample analytics | Gold Parquet and query parameters | Tabular sample outputs |
| Pipeline CLI and Orchestrator | Invoke individual stages or the end-to-end pipeline | User command and configuration | Ordered stage results and status |

See [components.md](components.md) for component boundaries, [component-methods.md](component-methods.md) for method interface sketches, [services.md](services.md) for orchestration, and [component-dependency.md](component-dependency.md) for dependencies and flow.

## Candidate Repository Layout

```text
src/
  <python-package>/
    config and path resolution
    generator, bronze, transformations, quality, queries, cli
    sql/                 # SQL assets colocated with Python project

tests/
  unit/
  integration/
  data-contract/

lakehouse/
  source/                # generated CSV and manifest; runtime data
  bronze/                # Parquet and ingestion metadata
  silver/                # standardized Parquet
  gold/                  # business-ready Parquet
```

Exact package names and the location of user-facing setup/schema documentation remain implementation/documentation organization details. Generated and modeled data must be excluded from source control by default.

## Orchestration and Data Contracts
- The CLI provides discrete operations for generation, ingestion, transformation, validation, and demos, plus one full pipeline operation.
- Data passes across stage boundaries as CSV/Parquet files and explicit paths; contracts remain inspectable and a later stage can be restarted from persisted input.
- DuckDB is opened within the operation that performs SQL/query work and is not a shared database service.
- Expected high-level order: generate -> validate source -> ingest Bronze -> validate Bronze -> build Silver -> validate Silver -> build Gold -> validate Gold -> run optional demo queries.
- A critical stage or quality failure is returned to the orchestrator and blocks dependent work; detailed failure policy and atomic publication are deferred to NFR/Functional Design.

## Dependencies and Handoffs
1. Generator publishes source schemas, keys, seed/configuration, manifest, samples, and CSV outputs for Bronze ingestion.
2. Bronze ingestion publishes raw-value-preserving Parquet with source/load metadata for Silver transformations.
3. Silver transformations publish standardized typed Parquet and quality outcomes for Gold modeling.
4. Gold transformations publish documented sales, customer, inventory, and forecast contracts for sample queries and Phase 2 semantic modeling.
5. The single data engineer verifies the source/Bronze handoff, then the Bronze/Silver/Gold flow and final downstream contract in sequence.

## Detailed Design Deferred
Functional Design will define exact schemas, business keys, grain and measure formulas, null/duplicate/invalid-row handling, the baseline forecast grain/lookback/insufficient-history behavior, and quality thresholds. NFR Requirements/Design will define practical local performance and reproducibility targets, test evidence, and run/recovery expectations. Application Design intentionally does not prescribe those business rules.

## Traceability
- Approved requirements: P1-FR-1 through P1-FR-6 and their local-runtime, reproducibility, and testability constraints.
- Approved stories: P1-US-1 (generator/source/Bronze) and P1-US-2 (Silver/Gold, analytics samples, and Phase 2 handoff).
- Approved workflow plan: Application Design and Units Generation execute; Infrastructure Design is skipped.

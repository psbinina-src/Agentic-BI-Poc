# Phase 1 Application Components

## Design Decisions
- One Python project with clear modules for the source generator, Bronze ingestion, Silver/Gold transformations, quality checks, and query/demo helpers.
- Python and SQL reside together under `src/`; tests are separate under `tests/`; data artifacts are isolated under `lakehouse/`.
- Provide stage-specific commands and one full-pipeline command.
- Components exchange documented CSV/Parquet files and explicit configuration/path values. DuckDB reads/writes these local files; no service or network boundary is introduced.
- One data engineer owns and runs the components sequentially.

## Components

### Configuration and Path Resolver
- **Purpose**: Load generator and pipeline settings and resolve repository-relative input, output, and SQL paths.
- **Responsibilities**: Provide seed, date range, configured entity volumes, run options, and layer locations to pipeline stages; validate configuration presence at startup.
- **Interface**: Immutable configuration object shared by CLI and stage functions; no secrets or sensitive data are required.

### Synthetic Source Generator
- **Purpose**: Create deterministic synthetic e-commerce source entities.
- **Responsibilities**: Generate customer, product, order/order-line, and inventory inputs; write CSV files and a manifest describing configuration, seed, entity counts, and outputs.
- **Interface**: Accept configuration and output path; return generated-file manifest and counts.

### Bronze Ingestion
- **Purpose**: Load generated source CSVs into the local Bronze layer.
- **Responsibilities**: Validate expected source files, preserve source business values, write Parquet outputs, add source/load metadata, and report load status.
- **Interface**: Accept manifest or input paths and Bronze destination; return per-entity load results and output paths.

### Silver/Gold Transformation Runner
- **Purpose**: Transform Bronze datasets into standardized Silver and business-ready Gold datasets using DuckDB and SQL.
- **Responsibilities**: Execute SQL in dependency order, publish Parquet outputs at each layer, and record run results/lineage.
- **Interface**: Accept layer paths and run configuration; return produced datasets and execution summary. Detailed transformation rules are defined in Functional Design.

### Data Quality Validator
- **Purpose**: Make source-to-Silver and Silver-to-Gold quality outcomes visible.
- **Responsibilities**: Run the applicable required-field, type, key, duplicate, domain, and referential checks; return results and critical-failure status to the calling stage.
- **Interface**: Accept dataset paths and check configuration; return named check outcomes and summary. Exact rules and thresholds are deferred to Functional Design.

### Gold Query and Demo Helpers
- **Purpose**: Demonstrate the Gold contract against the Phase 1 questions.
- **Responsibilities**: Run sample sales trend, customer repeat-purchase, and inventory-risk queries through DuckDB; emit inspectable results and query examples.
- **Interface**: Accept Gold paths and query parameters; return tabular results and query/run metadata.

### Pipeline CLI and Orchestrator
- **Purpose**: Expose repeatable local stage operations and a single integrated flow.
- **Responsibilities**: Parse command/configuration, invoke the requested stage(s) in dependency order, stop on critical errors, and report output paths/status.
- **Interface**: `generate`, `ingest`, `transform`, `validate`, `demo`, and `run` commands are candidate command names; exact flags are defined during implementation planning.

## Repository-Level Component Boundaries
- `src/`: Python modules and their associated SQL files, including configuration, stage modules, and CLI orchestration.
- `tests/`: unit, data-contract, quality, and integration tests.
- `lakehouse/source/`: generated CSV inputs and manifests (runtime data; ignored by source control).
- `lakehouse/bronze/`, `lakehouse/silver/`, `lakehouse/gold/`: local Parquet outputs (runtime data; ignored by source control by default).
- `aidlc-docs/` and project-facing documentation locations: workflow and user documentation; finalized location is a code-generation decision.

## Explicitly Out of Scope
Cube, LangGraph, Next.js, Metabase, LLM APIs, hosted services, HTTP endpoints, and production scheduling are later-phase concerns, not Phase 1 components.

# Phase 1 Pipeline Services and Orchestration

## Runtime Model
The application is a local command-line pipeline, not a set of network services. The CLI coordinates Python modules in one process. Stage outputs are written to documented local CSV/Parquet paths; each stage can be run independently for inspection or recovery, and the `run` command invokes the complete dependency chain.

## Service Responsibilities

### Configuration Service
- Loads the selected configuration and default values.
- Resolves source, Bronze, Silver, and Gold locations relative to the repository or explicit user settings.
- Validates basic configuration shape before starting a stage.

### Generation Service
- Creates deterministic synthetic entities from the effective seed and size/date configuration.
- Writes raw CSV files and a manifest to `lakehouse/source/`.
- Returns output paths and entity counts to the orchestrator.

### Bronze Ingestion Service
- Reads the source manifest and CSV files.
- Writes raw-value-preserving Bronze Parquet outputs plus load metadata under `lakehouse/bronze/`.
- Returns load status, counts, and output paths.

### Transformation Service
- Opens a DuckDB connection for a transformation run.
- Executes SQL assets within `src/` against the agreed layer file paths.
- Publishes Silver outputs first and Gold outputs after their inputs are available.
- Returns execution status, output paths, and summary counts.

### Quality Service
- Runs the checks associated with source/Bronze/Silver/Gold boundaries.
- Writes inspectable quality reports with named outcomes and critical-failure status.
- Allows orchestration to stop before downstream publication when a required gate fails.

### Demo Query Service
- Executes the agreed sample queries against Gold Parquet using DuckDB.
- Provides tabular evidence for sales trends, customer repeat purchases, and inventory risk.

### Pipeline Orchestrator and CLI
- Exposes stage-specific operations and one full-pipeline operation.
- Passes configuration and paths to component functions; it does not transport full datasets in memory between stages.
- Orders work as generation -> source checks -> Bronze -> Bronze checks -> Silver -> Silver checks -> Gold -> Gold checks -> optional demos.
- Reports outcomes and paths to the console; failure reporting and exit behavior are refined during implementation design.

## Command-Level Interface

| Command (candidate) | Orchestration responsibility | Expected result |
|---|---|---|
| `generate` | Run synthetic generation only | CSV source files and manifest |
| `ingest` | Load an existing source manifest/CSV into Bronze | Bronze Parquet datasets and load report |
| `transform` | Build Silver and Gold from existing Bronze inputs | Silver/Gold Parquet outputs and transformation summary |
| `validate` | Run quality checks for configured available layers | Quality report and status |
| `demo` | Run sample Gold queries | Tabular sample results |
| `run` | Generate, ingest, transform, validate, and run demos in dependency order | Integrated phase result and all documented layer outputs |

Exact command flags and whether `transform` allows individual layer selection are implementation details, not fixed here.

## Failure and Restart Concept
A stage consumes prior persisted outputs and writes to its designated layer path. A failed validation or stage should be reported before dependent stages continue. The user can rerun a stage from its stable input contract instead of regenerating all upstream data. Atomic output replacement, run identifiers, and detailed recovery behavior are deferred to Functional/NFR Design.

# Phase 1 Application Design Plan

## Purpose and Scope
Define high-level component responsibilities, method/service interfaces, orchestration, and dependencies for the Phase 1 local data pipeline. Detailed business logic, schemas, and transformation rules remain for Functional Design. Implementation remains owned and sequenced by one data engineer.

**Approved constraints**: Python synthetic data generator; DuckDB SQL transformations; CSV synthetic raw inputs; Parquet Bronze/Silver/Gold outputs; local native processes; repository-root `lakehouse/` separate from code; order-line sales, daily product inventory snapshots, and a deterministic baseline forecast.

## Proposed Design Direction
Use a small modular Python application for the sequential local pipeline, with stage-specific modules and repeatable entry points. Use documented files as layer boundaries and DuckDB for loading/querying and SQL transformation. Keep generated data under `lakehouse/` and source, SQL, tests, and documentation in separate code/documentation roots. Avoid service processes, network APIs, containers, or infrastructure components in Phase 1.

## Design Questions
Please answer each question in the `[Answer]:` field. Choose `X` and describe a different preference if none of the listed options fits. These decisions establish high-level boundaries and interfaces; detailed business rules will be designed later.

### Question 1: Component boundaries
How should the Phase 1 pipeline components be grouped?

A) One small Python project with separate modules for generation, Bronze ingestion, Silver/Gold transformations, quality checks, and query/demo helpers (recommended; clear responsibilities without service/package overhead)

B) Separate Python packages for generator, ingestion, and transformations

C) One compact module/script with functions grouped by pipeline stage

X) Other (please describe after [Answer]: tag below)

[Answer]: A - one project with separate modules

### Question 2: Pipeline orchestration and entry points
How should a developer run the local pipeline?

A) Provide stage-specific commands (generate, ingest, transform/validate) plus one command to run the complete flow (recommended; supports handoffs and debugging)

B) Provide only one end-to-end command that generates, ingests, transforms, and validates

C) Provide only separate commands for each stage; no combined orchestration command

X) Other (please describe after [Answer]: tag below)

[Answer]: A

### Question 3: Component communication and data contracts
How should components exchange data?

A) Use documented CSV/Parquet files as explicit stage contracts and pass paths/configuration between stage entry points (recommended; visible lineage and restartable stages)

B) Invoke stage functions in-process and use DuckDB tables/relations as the primary internal handoff, with files at published layer outputs

C) Use both: file contracts between pipeline stages, with in-process function calls within a stage

X) Other (please describe after [Answer]: tag below)

[Answer]: A

### Question 4: Repository layout
Which high-level repository layout should the design use?

A) Separate root areas for `src/`, `sql/`, `tests/`, and `lakehouse/source/`, `lakehouse/bronze/`, `lakehouse/silver/`, `lakehouse/gold/` (recommended; code, transformation SQL, validation, and data outputs stay distinct)

B) Keep Python and SQL together under `src/`, with tests separate and the same dedicated `lakehouse/` layer folders

C) Use another organization while keeping all lakehouse data separate from implementation code

X) Other (please describe after [Answer]: tag below)

[Answer]: B

## Planned Artifacts
After all questions are answered and any ambiguity resolved, create:
- [x] `aidlc-docs/inception/application-design/components.md` — component purposes, responsibilities, and high-level interfaces.
- [x] `aidlc-docs/inception/application-design/component-methods.md` — method signatures and input/output contracts; detailed business rules deferred to Functional Design.
- [x] `aidlc-docs/inception/application-design/services.md` — local pipeline orchestration responsibilities and interactions.
- [x] `aidlc-docs/inception/application-design/component-dependency.md` — dependency matrix and data-flow representation with a text alternative.
- [x] `aidlc-docs/inception/application-design/application-design.md` — consolidated design and decisions.
- [x] Validate completeness and consistency against the approved Phase 1 requirements, stories, chosen answers, and single-owner sequential delivery; all design files passed workspace checks, no unanswered tags remain, and the dependency diagram has a text alternative.
- [x] Update `aidlc-docs/aidlc-state.md` and this plan as each artifact is completed.
- [x] Present the design artifacts for explicit user approval before Units Generation.

## Design Constraints and Deferred Decisions
- No HTTP/API service or separate database server is needed for Phase 1.
- No charting, semantic-layer, agent, Metabase, or later-phase implementation is in this design scope.
- Exact source and Gold schemas, key rules, quality policies, forecast window/formula, and test thresholds are detailed during Functional Design.
- The data engineer remains the single accountable owner; component separation supports clarity and testability, not parallel ownership.

# NFR Design Plan — P1-U1 Synthetic Generator

## Unit Context
- **Unit**: P1-U1 — Synthetic generator and source contract.
- **Approved NFRs**: No fixed runtime/memory target; normal summary includes elapsed time and row counts; no named stress profile, but size/date inputs remain configurable; no staging/backup/retention subsystem; publish the success manifest only after all source validation and file writes succeed.
- **Runtime**: Local Python CLI, direct configured `lakehouse/source/` paths; no remote service, container, queue, cache, or hosted database.
- **Functional invariants**: Valid synthetic data only, deterministic logical records, fixed default window/seed, stable CSV schema/order, and actionable failure status. Unmanifested output is invalid for P1-U2.

## NFR Design Direction
Keep the design lightweight and within the approved modular local application. Use the generator and path/config modules, local validation, CSV writer, and manifest publishing as the only relevant logical elements. Avoid infrastructure or production-service patterns. Design detail will specify how the accepted NFRs are realized without adding a hard performance target or a prior-run preservation guarantee.

## Category Applicability
- **Resilience**: Applicable to local generation failures; clarify retries and unmanifested partial-file behavior.
- **Scalability/performance**: Applicable because the default contains over one million inventory snapshots and sizes remain configurable; no SLA or named larger profile. Clarify whether row streaming or full in-memory assembly is preferred.
- **Security**: Requirements are already fixed: synthetic-only, no external calls, generated files excluded from source control. Security extension is opted out; no added security component is warranted.
- **Logical components/infrastructure**: The existing CLI, configuration, generator, validation, CSV writer, and manifest from approved Application Design cover this unit. No queues, caches, circuit breakers, service processes, or infrastructure components are applicable.

## Planning Steps
- [x] Review approved P1-U1 functional and NFR requirements and answer the design questions.
- [x] Define a generator resource strategy consistent with the supported default and configurable volumes.
- [x] Define local failure/retry and partial-output handling consistent with direct output and manifest gating.
- [x] Define component responsibilities for timings/counts, validation, CSV output, and final manifest publication.
- [x] Generate `aidlc-docs/construction/p1-u1/nfr-design/nfr-design-patterns.md`.
- [x] Generate `aidlc-docs/construction/p1-u1/nfr-design/logical-components.md`.
- [x] Validate no design decision adds targets or durability guarantees excluded by the approved NFRs; update state and present artifacts for explicit approval. Workspace checks passed; no unanswered plan fields remain.

## Clarification Questions
Please fill in each `[Answer]:` field. Use `X) Other` for a different preference and describe it after the tag.

### Question 1: Resource strategy for configurable generation
How should generated rows be handled to support the default and configurable sizes?

A) Generate and validate records incrementally while writing entity CSVs in stable order; retain only necessary bounded validation state (recommended for the 1,096,000-row default inventory output and configurable scale)

B) Build complete entity collections in memory, validate them, then write CSV files (simpler data flow but memory use grows with configured volume)

C) Use another approach; describe it after `[Answer]:`

X) Other (please describe after [Answer]: tag below)

[Answer]: B - keep it simple

### Question 2: Retry behavior
What retry behavior should apply to generator/configuration/file-operation failures?

A) Fail fast with an actionable error; do not automatically retry (recommended minimal CLI behavior; user can rerun with the same settings)

B) Retry transient filesystem errors once, then fail with diagnostics; never retry invalid configuration or data validation errors

C) Define another retry policy after `[Answer]:`

X) Other (please describe after [Answer]: tag below)

[Answer]: A  - simple for poc

### Question 3: Partial output cleanup
If a run fails after it has begun writing direct source files but before a success manifest is published, what should happen to those files?

A) Leave any partial/unmanifested files in place; report failure and rely on a later run to overwrite them. P1-U2 must require a valid success manifest (recommended minimal behavior, no cleanup/backup subsystem)

B) Delete files created by the failed run, but do not restore an earlier successful dataset

C) Define another cleanup/recovery policy after `[Answer]:`

X) Other (please describe after [Answer]: tag below)

[Answer]: A - keep it simple

## Answer Gate
NFR design artifacts will be generated after all answers are complete and checked for ambiguity. The final NFR design remains subject to explicit user approval before P1-U1 Code Generation planning.

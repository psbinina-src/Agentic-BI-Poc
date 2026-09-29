# NFR Requirements Plan — P1-U1 Synthetic Generator and Source Contract

## Unit Context
- **Functional design**: P1-U1 generates five synthetic CSV entities and a manifest, with defaults of 10,000 customers, 1,000 products, 100,000 order lines, inclusive dates 2023-01-01 through 2025-12-31, and seed 42.
- **Data volume**: At default inventory snapshot grain, the source contains 1,096,000 daily product snapshot rows (including leap day in 2024), in addition to customer/product/order/order-line records.
- **Runtime/stack**: Native local Python project; generated files under `lakehouse/source/`; no container or external data service. DuckDB is used by subsequent stages.
- **Reliability baseline**: The functional design rejects invalid configuration and publishes an accepted manifest only after all expected outputs and source validation succeed. Atomic/staged publication mechanics remain open.
- **Governance choices**: Synthetic-only data; Security Baseline, Property-Based Testing, and Resiliency Baseline extensions are disabled. Conventional deterministic tests remain in scope.

## NFR Category Assessment
- **Scalability**: Applicable; configurable date and entity volumes, plus a useful performance-test profile need defining.
- **Performance**: Applicable; generation of the default and performance profile should be benchmarkable, but no hardware-independent service latency target is implied.
- **Availability/DR**: Not applicable to an offline developer CLI; no uptime, failover, or disaster-recovery service is planned.
- **Security/privacy**: Applicable at a basic PoC level; synthetic data only, no real identifying/production data, and no external data transfer. Security extension opt-out does not waive these approved requirements.
- **Tech stack**: Resolved by approved requirements/design: Python, CSV, DuckDB-compatible local workflow, Parquet downstream. No new stack choice is needed for U1.
- **Reliability**: Applicable; deterministic reruns, valid-output publication, informative errors, and preservation of prior successful outputs need clarity.
- **Maintainability/testability**: Applicable; keep deterministic conventional checks and observable run/row-count/configuration evidence; PBT extension remains disabled.
- **Usability**: Applicable as a CLI utility; stage-specific generation command, configuration feedback, progress/result summary, and actionable errors are expected; no GUI or accessibility surface exists.

## Planning Steps
- [x] Collect and validate answers to the questions below; resolve ambiguity before drafting NFRs.
- [x] Define generator performance evidence and any expected limits for the approved default dataset.
- [x] Define configurable performance-test profile and supported growth expectations.
- [x] Define safe output-publication/recovery expectations for interrupted or failed generation.
- [x] Document applicable privacy, maintainability, observability, and usability NFRs, and explicitly mark service availability/DR as N/A.
- [x] Generate `aidlc-docs/construction/p1-u1/nfr-requirements/nfr-requirements.md`.
- [x] Generate `aidlc-docs/construction/p1-u1/nfr-requirements/tech-stack-decisions.md` with confirmed stack and rationale.
- [x] Validate against U1 Functional Design and approved Phase 1 requirements; update AI-DLC state and present the two artifacts for explicit approval. Workspace checks passed and no answer fields remain blank.

## Clarification Questions
Answer each `[Answer]:` field. If none fits, choose `X) Other` and provide details after the tag.

### Question 1: Performance evidence/target
What performance expectation should apply to the default generator run?

A) Record wall-clock duration, peak memory where practical, output size, and row throughput on the documented developer host; use this as a baseline without a universal pass/fail time limit (recommended for a local PoC with unspecified hardware)

B) Set a fixed runtime target now; specify the target and reference host after `[Answer]:` (for example, a time limit on a stated CPU/memory configuration)

C) Defer performance measurement until after implementation; no baseline requirement for U1

X) Other (please describe after [Answer]: tag below)

[Answer]: X - keep it simple

### Question 2: Performance-test profile and scale
Which configurable stress profile should U1 document in addition to the default dataset?

A) Include the previously considered larger profile: five years, about 50,000 customers, 5,000 products, and 1,000,000 order lines; record resulting inventory volume from daily product snapshots and make values configurable (recommended for a useful scalability test)

B) Use the approved default profile only; all values remain configurable but no named stress profile is specified

C) Define a different named stress profile; specify dates, customers, products, and order lines after `[Answer]:`

X) Other (please describe after [Answer]: tag below)

[Answer]: X - simple

### Question 3: Output safety on failed or repeated runs
How should generation preserve source outputs when a run fails or is repeated?

A) Generate into a unique temporary/run directory; validate all files; publish the manifest/accepted run only on success and preserve the previous successful run (recommended; avoids partial data appearing valid)

B) Write directly to the configured source files and remove/replace incomplete outputs on failure

C) Write separate timestamped run directories; retain all runs without a cleanup policy in U1

X) Other (please describe after [Answer]: tag below)

[Answer]: X - minimum or no , just good data for now

**Follow-up resolved**: Q1 maps to minimal, non-gating performance evidence (elapsed time and generated row counts; no fixed time/memory target). Q2 maps to no named stress profile while retaining configurable dates and sizes. Q3 maps to no added staging/backup/retention guarantee; use configured source paths, retain source validation and success-manifest gating, and report failures without treating incomplete outputs as successful. The original custom answers remain unchanged in the clarification file.

## Answer Analysis Gate
Do not generate NFR artifacts until all answers are complete and checked for vague or conflicting requirements. If performance targets depend on an unspecified machine, capture the host as a benchmark context rather than pretending the number is portable. Availability/DR remain explicitly not applicable unless the user changes the local CLI scope.

# P1-U1 Non-Functional Requirements — Synthetic Generator

## Scope and Baseline
P1-U1 is a local command-line source generator that creates synthetic customer, product, order, order-line, and daily inventory snapshot CSVs plus a manifest. Defaults are seed `42`, inclusive dates 2023-01-01 through 2025-12-31, approximately 10,000 customers, 1,000 products, 100,000 order lines, and 1,096,000 inventory snapshots. Dataset dates and volumes remain configurable.

## Performance
- No hardware-independent completion-time, memory, throughput, or output-size pass/fail target is imposed for this PoC unit.
- The normal run summary reports elapsed generation time and generated row counts; this is informational evidence, not a service-level target.
- Benchmark results, if collected, must note the developer host context to support meaningful comparison.

## Scalability
- Date range and customer, product, and order-line sizes remain configurable for development and performance-test runs.
- No additional named stress profile or maximum supported size is required for P1-U1.
- The generator must report requested settings and actual row counts so larger runs can be inspected. Practical resource limits may be documented if discovered during implementation; do not invent a universal capacity claim.
- Daily inventory snapshot output scales with `product_count × inclusive_calendar_days`; the default date range includes leap day 2024.

## Reliability and Output Handling
- For the same generator version, effective seed, dates, sizes, and configuration, logical source records and canonical CSV data must be reproducible.
- Configuration and generated records must pass the approved source validation rules before a run is reported as successful.
- Publish the success manifest only after every expected entity file is written and all source-level validation/scenario-presence checks pass.
- Keep output handling minimal: write to configured source paths without a staging/backup/retention subsystem. No guarantee is made that a previous successful dataset is preserved if a write or process fails.
- A failed run must return a failure status and must not publish a success manifest. Any partial/unmanifested outputs are not a valid source contract and must not be consumed by P1-U2.
- A rerun may recreate the configured source outputs. Exact filesystem atomicity is not an NFR target for this unit.

## Data Privacy and Security Baseline
- Generate synthetic values only; do not read, import, transmit, or reproduce production/confidential/identifying source data.
- Do not call external services for source generation; all generation runs locally.
- Customer labels/identifiers are synthetic placeholders, not realistic personal records.
- Generated CSVs and manifests are runtime data under `lakehouse/source/` and are excluded from source control by default; document schemas and instructions instead.
- The Security Baseline extension is disabled, but these already-approved data-handling requirements remain applicable.

## Maintainability and Testability
- Keep generator configuration, generation logic, source schemas, and CLI responsibilities separated within the approved modular project.
- Document defaults, effective configuration, entity counts, source schemas/keys, scenario profiles, output paths, and regeneration command.
- Use conventional deterministic unit/contract checks for reproducibility, counts, required entities, stable IDs, referential integrity, domain values, and required scenario presence. Property-Based Testing is not required because that extension is disabled.
- Provide actionable configuration/validation errors and a concise successful/failed run summary; no GUI or always-on observability service is required.

## Availability and Disaster Recovery
- **Not applicable**: P1-U1 is an offline developer CLI, not a continuously available service. No uptime, failover, disaster-recovery, or backup SLA is defined.
- Users can rerun generation from documented settings and seed. A prior generated dataset is not guaranteed to survive a failed write under the selected minimal output-handling approach.

## Acceptance Evidence
1. The default and configurable run reports effective seed/date/volume settings and actual row counts.
2. A same-version/same-settings rerun produces matching logical data and canonical entity CSV content.
3. Source validation failures result in a failed process outcome and no success manifest.
4. A successful run produces all five entity files plus a manifest, with data under the documented local source path and excluded from source control by default.
5. The ordinary summary includes elapsed generation time and counts without imposing a hardware-independent performance threshold.

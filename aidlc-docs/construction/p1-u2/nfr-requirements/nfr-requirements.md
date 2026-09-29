# P1-U2 NFR Requirements — Bronze Ingestion and Lineage

## Summary
P1-U2 is a local-first Bronze ingestion unit that must accept only validated, checksum-verified source files and load them into Parquet with raw-value preservation and row-level lineage. The non-functional requirements are intentionally modest and targeted to the PoC scope: correctness, inspectability, deterministic behavior, and clean local handling.

## Scalability
- The unit should handle the approved P1-U1 default source sizes without requiring distributed compute or a container runtime.
- The design should remain compatible with larger local source files by streaming through DuckDB CSV readers and writing Parquet incrementally per entity.
- Default local processing should be bounded to a single host process with a clear source and output location.

## Performance
- Bronze ingestion should complete within practical local expectations for the approved source volumes; there is no hard SLA beyond deterministic, inspectable processing.
- The workflow should minimize unnecessary copies and avoid moving raw data through unnecessary intermediate layers.
- CSV-to-Parquet conversion should be performed in a single pass per entity once source validation has succeeded.

## Availability and Reliability
- The unit should fail fast on invalid or changed source data rather than publishing partial Bronze outputs.
- A failed run must leave no false success signal; the source contract is authoritative and all-or-nothing Bronze publication is required.
- Local file errors, missing files, malformed CSVs, and checksum mismatches are surfaced as actionable errors.

## Security and Data Handling
- The source is synthetic test data only; no secret or personal data is introduced.
- Source data is processed locally without external transmission.
- Manifest and checksums are treated as integrity controls, not as a security boundary beyond the PoC scope.
- Access is limited to local workspace files and the user environment.

## Maintainability
- The implementation should remain simple and explicit: source validation, CSV read, lineaged Parquet write, and clear diagnostics.
- The configuration and file paths should be easy to inspect during local execution.
- The logic should be readable for future P1-U3 and P1-U4 consumers.

## Reliability and Observability
- Each successful ingest should emit record counts and metadata for source file, source run, and row lineage.
- The ingest unit must retain enough metadata to debug source drift or downstream issues without storing sensitive data.
- Broken source checks must stop the run before a dependent stage can consume Bronze output.

## Tech Stack Decisions
- Runtime: Python 3.11+ with local DuckDB processing.
- Storage: Parquet under `lakehouse/bronze/`.
- Data flow: ad hoc local controlled file reads/writes only, no service or container dependency.
- Validation controls: manifest JSON, checksum verification, and source file existence checks.
- Reasoning: This is the minimum stack that preserves the approved contract while keeping the PoC local-first, deterministic, and testable.

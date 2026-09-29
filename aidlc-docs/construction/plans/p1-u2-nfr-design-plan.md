# NFR Design Plan — P1-U2 Bronze Ingestion and Lineage

## Unit Context
- **Unit**: P1-U2 — Bronze ingestion and lineage.
- **NFR Requirements**: local-first ingestion, fail-fast integrity checks, explicit lineage metadata, and simple deterministic execution.
- **Design objective**: convert the NFR requirements into a minimal but robust local design that is easy to validate and straightforward to extend.

## Planned NFR Design
- [x] Review P1-U2 NFR requirements and confirm the design constraints.
- [x] Map the local runtime, file-processing, and Parquet-writing pattern.
- [x] Define the logical components needed for manifest validation, ingestion, lineage capture, and error reporting.
- [x] Capture resilience, reliability, and performance design decisions.
- [x] Draft the final NFR design artifacts.
- [x] Prepare the approval prompt for the NFR design review gate.

## Decision Notes
- No container runtime is required.
- One Python process and one DuckDB local engine are sufficient.
- Source validation is a hard gate before any Bronze write.
- Failure reporting is explicit and blocks downstream usage.
- Row-level lineage and run metadata are part of the Bronze design contract.

# P1-U2 Tech Stack Decisions — Bronze Ingestion and Lineage

## Chosen Stack
- Python 3.11+ for the local orchestration and file handling.
- DuckDB for CSV ingestion and Parquet output.
- Local filesystem for source manifests, CSV files, and Bronze Parquet outputs.
- JSON manifest for source metadata and SHA-256 checksums.

## Rationale
This unit is intentionally constrained to the local-first PoC. The selected stack matches the approved project direction, keeps implementation lightweight, and avoids any requirement for containers, distributed systems, or external runtime services.

## Design Considerations
- CSV ingestion is handled directly from source files rather than a network API to keep the pipeline inspectable and deterministic.
- Parquet is selected as the Bronze storage format because it preserves raw values and scales well for local lakehouse use without container complexity.
- Checksum validation and manifest gating are implemented before publication to protect against silent drift or accidental file mutation.
- Row-level lineage and run metadata are appended as lightweight columns to preserve traceability without changing the source business schema.

## Non-Goals
- No external orchestrator, queue system, or remote storage.
- No resilient retry framework beyond fail-fast, deterministic local checks.
- No distributed or high-availability deployment assumptions.

## Acceptance Fit
The selected stack supports the approved Bronze contract, allows local reproduction, and keeps the implementation aligned with the broader Phase 1 local lakehouse approach.

# P1-U2 NFR Design Patterns — Bronze Ingestion and Lineage

## Design Pattern Summary
P1-U2 adopts a simple, deterministic local pipeline pattern. The ingestion flow is intentionally linear and explicit: validate source contract -> ingest raw CSV -> attach lineage -> write Bronze Parquet -> surface success/failure.

## Resilience and Failure Handling
- Fail-fast validation: if source manifest or checksum data is invalid, processing stops before any Bronze write.
- Atomic Bronze publication: the unit writes only after the entire expected source set has passed validation.
- Error transparency: missing files, parse errors, and mismatched checksums are surfaced as actionable exceptions.
- No hidden retries: the PoC does not add automatic retry loops or backoff logic; the correct path is to correct the source or manifest and rerun.

## Scalability Pattern
- The ingestion unit uses file-oriented local processing rather than a multi-node service model.
- The design supports increasing local file sizes by reading one file at a time and storing Parquet output incrementally.
- It scales by capacity of the local host rather than by distributed orchestration, which matches the PoC constraints.

## Performance Pattern
- One-pass CSV read with direct Parquet output keeps overhead low.
- Checksums and validation happen upfront to avoid wasted write work.
- DuckDB handles the data conversion efficiently without introducing additional ETL layers.

## Security Pattern
- Local-only processing and synthetic test data mean the design does not require secrets, network policies, or external access patterns.
- Integrity is enforced by SHA-256 checks against the P1-U1 manifest, which provides a clear trust boundary for source acceptability.

## Reliability Pattern
- The design preserves run provenance and row-level lineage so a failed or suspect load can be audited.
- Bronze data is always traceable back to the exact source run and file row that created it.
- Since direct overwrite is the default minimal behavior, human operators can rerun cleanly after fixing the source contract.

## Logical Component Model
1. Source Contract Checker
   - validates manifest existence, parseability, and accepted counts
2. Integrity Verifier
   - validates file presence and SHA-256 checksums
3. CSV Reader / Ingestion Layer
   - loads each entity into DuckDB and retains raw values
4. Lineage Enricher
   - appends `source_file`, `source_row_number`, `source_run_id`, and `ingested_at`
5. Bronze Writer
   - writes each entity to `lakehouse/bronze/*.parquet`
6. Run Status Reporter
   - reports outcome, counts, and output paths for downstream consumption

## Design Fit
This NFR design is intentionally minimal for the P1-U2 unit and keeps the technology stack and behavior aligned with the approved local-first Phase 1 lakehouse approach.

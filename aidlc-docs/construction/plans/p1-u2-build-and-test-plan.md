# Build and Test Plan — P1-U2 Bronze Ingestion and Lineage

## Purpose
This plan verifies that the P1-U2 Bronze ingestion unit meets the approved functional and NFR design, produces valid output under the accepted source contract, and remains ready for the next downstream unit.

## Scope
- Validate source manifest preflight and checksum contract.
- Validate CSV-to-Bronze Parquet ingest path.
- Validate raw-value retention and lineage metadata.
- Validate CLI success and failure behavior.
- Confirm the unit is fit to hand off to the next downstream stage.

## Build and Test Actions
- [x] Confirm the local Python + DuckDB runtime is available.
- [x] Run focused unit tests for ingest validation and CLI behavior.
- [x] Ensure failures are explicit and non-silent.
- [x] Keep the test scope aligned to the approved unit scope; no unrelated infrastructure or service layers are added.

## Evidence
- Test command: `python -m pytest tests/p1_u2 -q`
- Result: 6 passed in 1.27s

## Handoff Gate
P1-U2 is ready to hand off to the next approved stage once the current unit’s design and implementation have been reviewed for the accepted local-first Bronze contract.

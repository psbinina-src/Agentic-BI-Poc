# Functional Design Plan — P1-U2 Bronze Ingestion and Lineage

## Unit Context
- **Unit**: P1-U2 — Bronze ingestion and lineage.
- **Story**: P1-US-1 — ingest reproducible synthetic inputs as stable, traceable Bronze data.
- **Owner**: One data engineer; execute after P1-U1 acceptance.
- **Accepted upstream contract**: Five UTF-8 CSVs and `manifest.json` in a configured source directory. Manifest includes schema version, effective seed/date window/volumes, output paths, counts, SHA-256 checksums, validation/scenario status, and run timestamp. Only a valid manifest with passing validation and matching files is accepted.
- **Application design**: Python modules/SQL in `src/`, tests in `tests/`, local data under `lakehouse/`; DuckDB is embedded; Parquet is used for Bronze; no containers or separate service.
- **Boundary**: U2 performs source contract preflight and Bronze ingestion with minimal transformation, preserving raw values and lineage. Silver cleansing/typing/business transformations belong to P1-U3.

## Planning and Generation Steps
- [x] Resolve the questions below and verify decisions against the approved source manifest/CSV contract and the P1-U2 acceptance criteria.
- [x] Define the Bronze data grain, schemas and raw-value preservation semantics for each source entity.
- [x] Define manifest/checksum preflight, CSV parsing failures, and all-or-nothing ingestion behavior.
- [x] Define ingestion metadata (source, timestamp, run/load status), its row-level or run-level placement, and lineage back to input files/rows.
- [x] Define repeat-load semantics, output layout, and handoff evidence for Silver.
- [x] Generate `aidlc-docs/construction/p1-u2/functional-design/business-logic-model.md`.
- [x] Generate `aidlc-docs/construction/p1-u2/functional-design/business-rules.md`.
- [x] Generate `aidlc-docs/construction/p1-u2/functional-design/domain-entities.md`.
- [x] Validate design coverage for every P1-U1 source entity and the P1-U2 exit handoff; update plan/state and request explicit Functional Design approval.

## Clarification Questions
Please fill each `[Answer]:` tag. If choosing `X) Other`, include the custom response after the tag. These decisions define Bronze behavior; detailed DuckDB code and NFRs are handled in later stages.

### Question 1: Raw value and type preservation
How should CSV fields be represented in Bronze?

A) Read source values according to the published CSV schema and write them to Parquet without business transformation; preserve textual field values where the contract defines strings, while retaining dates/numbers in their source-declared representations (recommended balance of fidelity and usable schema)

B) Store every CSV field as a string in Bronze, preserving decoded CSV values exactly; defer all typing to Silver

C) Infer/cast data types during ingestion using the manifest/schema, but make no business-rule changes

X) Other (please describe after [Answer]: tag below)

[Answer]: B

### Question 2: Ingestion metadata and lineage placement
Where should Bronze ingestion metadata be recorded?

A) Keep business columns unchanged and write a per-run sidecar load manifest with source paths/checksums, load timestamp/status, counts, and output paths (recommended simple contract)

B) Append source-file, source-row number, load timestamp, and load-run ID columns to every Bronze row, plus a per-run status summary

C) Include the sidecar manifest and row-level lineage columns

X) Other (please describe after [Answer]: tag below)

[Answer]: C

Resolved: include both the selected run-level load manifest and row-level source-file/source-row/load-time/run-ID fields. This preserves source columns while providing per-row lineage plus per-load status.

### Question 3: Repeat-load and Bronze retention behavior
How should a rerun of Bronze ingestion handle existing outputs?

A) Create a distinct immutable Bronze run directory for each accepted source-manifest/run ID and retain earlier runs; the load manifest records the run path (recommended for traceability and avoiding silent overwrite)

B) Replace the current Bronze outputs idempotently after successful input validation; do not retain previous Bronze runs

C) Keep one current output and allow an explicit option to retain versioned run directories

X) Other (please describe after [Answer]: tag below)

[Answer]: A - replace current Bronze output after a successful run, but only after all source checks pass; do not retain earlier Bronze runs in the default minimal behavior

### Question 4: Manifest, checksum, and entity-load failures
What should happen if the source manifest is missing/invalid, a checksum fails, or any entity CSV cannot be parsed?

A) Preflight the manifest and all five listed CSVs/checksums before publishing any Bronze data; fail the whole run with actionable diagnostics and no successful load manifest if any source check fails (recommended strict unit handoff)

B) Load valid entities and report failed entities separately; do not mark the overall run successful

C) Ignore checksum mismatches if CSV files can still be parsed

X) Other (please describe after [Answer]: tag below)

[Answer]: A - preserve the approved P1-U1 contract: require matching SHA-256 checksums and fail the whole Bronze load before publishing any outputs if a mismatch occurs

## Category Applicability
- Business rules, data flow, source entities, input/output contracts, and error cases are applicable and covered above.
- Integration is local and file-based; no external systems, API, or network interaction applies.
- There is no frontend/UI in P1-U2.
- The P1-U2 handoff is blocking: P1-U3 uses only a successful Bronze run with documented schemas, paths, counts, metadata, and lineage evidence.

## Completion Gate
After answers are complete, check for ambiguities and resolve any conflicts before writing the three U2 Functional Design artifacts. Explicit approval of U2 Functional Design is required before proceeding to NFR Requirements for P1-U2.

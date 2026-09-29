# P1-U3 NFR Design Patterns — Silver Standardization and Data Quality

## Design Pattern Summary
P1-U3 uses a direct, local, deterministic transformation pattern. It reads accepted Bronze outputs, standardizes them into typed Silver tables, validates them with explicit checks, and publishes pass/fail evidence before downstream Gold work begins.

## Resilience and Failure Handling
- Critical quality failures are blocking.
- A failing quality check prevents a downstream Gold handoff and keeps the unit in a clearly failed state.
- No silent repair is allowed; unacceptable source data remains blocked.

## Scalability Pattern
- Incremental local file processing is sufficient for the project’s synthetic PoC volume.
- The unit remains valid for larger local data sizes by using standard file-based DuckDB processing.

## Performance Pattern
- One-pass reads of Bronze outputs and one-pass writes of typed Silver outputs minimize unnecessary processing.
- Quality checks are performed by table and rule, not through expensive repeated scans of the same data.

## Security Pattern
- The design stays fully local and synthetic.
- No external secret handling or API access is introduced.

## Reliability Pattern
- Every check is named and inspectable.
- The quality report is persistent evidence for acceptance or rejection.

## Logical Component Model
1. Bronze Intake Validator
   - validates accepted Bronze source and run identity
2. Standardization Component
   - converts Bronze values to canonical Silver types and structures
3. Quality Check Component
   - runs required field, null, type, duplicate, referential, and domain checks
4. Quality Report Publisher
   - writes pass/fail details and run metadata
5. Silver Output Publisher
   - writes final Silver outputs for downstream Gold use

This model keeps the design explicit and straightforward while preserving evidence for later review.

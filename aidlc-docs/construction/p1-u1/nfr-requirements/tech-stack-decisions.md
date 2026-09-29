# P1-U1 Technology Stack Decisions

## Confirmed Decisions

| Concern | Decision | Rationale/status |
|---|---|---|
| Generator language | Python | Approved Phase 1 choice; suitable for deterministic synthetic data generation and local CLI use. |
| Raw source format | UTF-8 CSV entity files plus a manifest | Approved; inspectable local input contract for Bronze ingestion. |
| Generated-data location | Repository-root `lakehouse/source/` | Approved data/code separation; generated runtime data excluded from version control by default. |
| Generator execution | Native local CLI | Approved local-first runtime; no Docker, WSL, container, remote service, or API dependency. |
| Randomness | Deterministic seeded generator using configured default seed `42` | Required for repeatable logical records; use documented deterministic behavior and stable ordering. |
| Downstream query/ingestion | DuckDB is part of the approved local pipeline, principally consumed by Bronze and transformation units | No separately hosted database is required; P1-U1 only creates CSV and manifest outputs. |
| Modeled layer format | Parquet for Bronze, Silver, and Gold outputs | Approved Phase 1 format; P1-U1 produces the CSV source consumed by P1-U2. |
| Testing approach | Conventional deterministic unit/contract tests | Required for behavior and acceptance; Property-Based Testing extension was opted out. |
| Extensions | Security Baseline, Resiliency Baseline, and Property-Based Testing extensions disabled | User-selected at Requirements Analysis; approved privacy and reproducibility constraints remain in effect. |

## Decisions Deferred to Code Generation
- Exact supported Python minor version and dependency pinning.
- CLI implementation details and exact command names/flags.
- Whether any third-party generator or CLI library is needed; no new dependency is required by this design, and additions should be justified by concrete needs.
- Cross-platform support beyond the current Windows development environment.

## Rationale and Constraints
- Keep P1-U1 dependency-light and local; no external data source or data-generation service is permitted.
- Avoid realistic personal identities; generated names are synthetic labels.
- Keep configuration, source schema, generation code, and output paths documented and version-controlled; do not commit generated dataset files.
- If any implementation choice changes CSV schema or deterministic behavior, update the P1-U1 source contract and notify the dependent P1-U2 work before accepting the handoff.

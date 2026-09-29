# P2-U2 NFR Requirements — Local Gold REST API

## Scope
Minimal local-PoC requirements for a read-only Python API over Gold Parquet. Production hosting, multi-user authentication, HA, DR, monitoring, and performance SLAs are out of scope.

## Security and Network Boundary
1. Bind the service to `127.0.0.1` only; document that it is not remotely accessible or production-secured.
2. The API reads only the four fixed Gold Parquet filenames from the configured Gold directory. Requests cannot supply file paths or SQL.
3. Expose read-only catalogue and query operations. Validate table/field identifiers against the known dataset catalogue and physical Parquet schemas; parameterize filter values.
4. Cap query result rows at 500 (default 100), and bound the number of projected, grouped, filtered, and aggregated fields.
5. Do not log source rows, prompt contents, or filesystem paths. Return concise errors without stack traces.
6. This API does not call an external LLM/service. Phase 3 must apply its own data-minimization decisions before sending any context externally.

## Runtime and Maintainability
- Native Python FastAPI/Uvicorn and embedded DuckDB; no Docker, WSL, Node, Cube, or hosted service required for this API.
- Gold Parquet remains the source of truth. The API adds no stored database, copied data, or business metric definitions.
- Start and stop manually; no background service or production deployment.

## Reliability and Performance
- Single-process local PoC; no uptime, HA, failover, backup, DR, or numeric latency target.
- Reject invalid dataset/field/filter requests and database errors with structured HTTP responses; do not silently widen or rewrite queries.

## Verification Criteria
- Service starts on loopback and reports Gold dataset availability.
- Catalogue metadata matches all four Gold Parquet schemas and documented grains/keys.
- Query API validates field references and request shape, caps rows at 500, rejects SQL/path injection, and matches direct DuckDB fixture results.
- The default Gold directory and `AGENTIC_BI_GOLD_DIR` override are documented.

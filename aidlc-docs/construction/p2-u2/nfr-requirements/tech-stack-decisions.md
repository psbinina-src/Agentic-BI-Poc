# P2-U2 Tech Stack Decisions — Direct Gold REST

## Selected Stack
- **REST application**: FastAPI with Uvicorn, run as a native local Python process.
- **Data access**: embedded DuckDB scans the four local Gold Parquet files directly; no intermediate DuckDB catalog is required.
- **Metadata**: field names/types discovered from Parquet; dataset grain/key and field descriptions are version-controlled.
- **Runtime boundary**: explicit Uvicorn bind to `127.0.0.1`; no Docker, WSL, Node, Cube, credentials, or hosted service required.
- **Tests**: pytest plus FastAPI TestClient using temporary synthetic Gold Parquet fixtures.

## Rationale and Constraints
- REST is a small, inspectable contract that the Phase 3 Python agent can call directly; the agent can wrap endpoints as its own tools.
- The API exposes Gold fields and generic query operations, not a centralized metric/semantic layer. The existing P2-U1 Cube prototype is retained only as optional reference and is not in this runtime path.
- Query identifiers are schema-validated; filter values are bound parameters; arbitrary SQL and client-supplied paths are rejected.
- No additional database, API gateway, dashboard, or observability stack is added.

# Build Instructions — Phase 2 Gold REST API

## Prerequisites
- Windows PowerShell and Python 3.11 or newer.
- Phase 1 Gold Parquet files under `lakehouse/gold/`.
- Python dependencies declared in `pyproject.toml`.

## Install Dependencies
Run from the repository root:

```powershell
py -m pip install -e ".[test]"
```

## Validate and Start
Compile the Phase 2 API package and tests:

```powershell
py -m compileall -q src/p2_u2 tests/p2_u2
```

Start the local API in a dedicated terminal. The bind address must remain loopback-only:

```powershell
py -m uvicorn p2_u2.api:app --app-dir src --host 127.0.0.1 --port 8100
```

Stop the server with `Ctrl+C`. No build artifact, database copy, secret, or external service is required.

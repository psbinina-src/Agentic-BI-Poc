# P2-U2 Logical NFR Components — Local Gold REST API

| Component | NFR responsibility | PoC behavior |
|---|---|---|
| FastAPI/Uvicorn | Local HTTP interface and request validation | Manually started native process, bound to `127.0.0.1`; no CORS or remote listener |
| Gold data access | Read-only Parquet access | DuckDB scans only the four configured, allowlisted Gold Parquet files |
| Query validator | Constrain agent-supplied requests | Validate dataset and physical fields; parameterize values; reject SQL/path inputs; cap results at 500 |
| Gold catalogue | Explain dataset and field contracts | Grain/key descriptions are version-controlled; field names/types are inspected from Parquet |
| Local configuration | Select Gold directory | Default `lakehouse/gold/`; optional `AGENTIC_BI_GOLD_DIR`; no credentials required for loopback-only use |

## Start/Stop Contract
Start manually from the repository root with Uvicorn bound to `127.0.0.1`; stop with `Ctrl+C`. Do not use wildcard/host-network binding, change firewall rules, create a Windows service, or expose the API outside the host.

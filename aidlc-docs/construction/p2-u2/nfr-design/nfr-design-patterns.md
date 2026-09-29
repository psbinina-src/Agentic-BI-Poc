# P2-U2 NFR Design Patterns — Direct Gold REST PoC

## Access and Validation
- Bind Uvicorn only to `127.0.0.1`; do not expose the API to the LAN or public network.
- No API credentials are needed for this host-only PoC. Do not treat the service as remotely authenticated or production-ready.
- Permit only fixed Gold dataset names and fields found in the corresponding Parquet schema. Parameterize filter values and cap queries at default 100 / maximum 500 rows.
- Never accept SQL text, arbitrary table names, or request-supplied file paths.

## Network Boundary
- Use Uvicorn's explicit `--host 127.0.0.1` command. Do not use wildcard binding, port forwarding, firewall changes, or a reverse proxy.
- If the service is ever needed from another device, stop and add an approved authentication/network design first; this PoC's loopback setting is a hard boundary.

## Availability and Failure Handling
- One manually started native Python API process. No supervisor, retries, failover, HA, backup, or DR is added.
- Invalid requests and missing/corrupt Gold inputs return concise errors. No silent query substitution or retry is added.

## Performance and Scope
- No numeric latency or throughput SLO. Keep the response ceiling at 500 rows and bound request lists.
- Do not add pre-aggregation, caching infrastructure, or performance services without measurements.
- The API itself never sends records to an external service. Phase 3 is responsible for prompt data minimization.

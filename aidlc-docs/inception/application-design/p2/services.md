# Phase 2 Services and Orchestration

## Local Semantic Service
- Start Cube Core as a native host process with model/configuration files from the repository and credentials/configuration from local environment variables.
- Configure Cube's DuckDB driver to read the local Gold data path. No hosted data service or container runtime is part of the design.
- Serve catalog and metric queries over Cube REST; enable its Postgres-protocol SQL API for BI validation.
- Keep service ports bound to loopback for this local PoC. Never commit secrets. Do not rely on Cube development mode being reachable by other machines.
- Confirm native Cube Core + DuckDB operation before implementing downstream access; if the no-container constraint cannot be met, stop and seek direction rather than introducing Docker or a hosted service.

## Local MCP Service
- Start a small Python MCP process using stdio, configured by the MCP client.
- Expose only catalog discovery and bounded metric-query tools.
- Translate MCP tool arguments into Cube REST metadata/load requests. Reuse Cube's names and results; do not recalculate metrics in the adapter.
- Reject unknown measures/dimensions, unsupported filters, arbitrary SQL, and unbounded result requests before calling Cube.

## Sequential Orchestration
1. P2-U1 verifies/corrects the Gold contract and defines the Cube semantic model. It publishes expected results and a stable catalog contract.
2. After the P2-U1 contract gate passes, P2-U2 starts Cube Core locally and connects REST, SQL, and MCP consumers to the same model.
3. P2-U2 runs parity cases through Cube REST, Cube SQL, and MCP, then publishes local setup and endpoint examples.

## Runtime Ownership
- The data engineer runs and stops the native processes locally; no daemon supervisor or production operations layer is introduced.
- Required environment values, ports, and startup commands are documented and validated during implementation.

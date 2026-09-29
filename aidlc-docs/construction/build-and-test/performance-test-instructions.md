# Performance Test Instructions — Phase 2 Gold REST API

## Applicability
Formal performance testing is not applicable to this single-workstation PoC. There is no numeric latency, throughput, or concurrency target, and the security/resiliency extensions are disabled.

## Existing Query Bound
- Query results default to 100 rows and are capped at 500.
- Request field lists and filter lists are bounded by the API schema.
- No load/stress test or performance claim is made.

If Phase 3 or later introduces a measured performance requirement or larger workload, define a target first and add a focused benchmark against representative local Gold data.

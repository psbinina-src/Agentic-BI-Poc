# P1-U1 NFR Design Patterns

## Design Basis
This design realizes the approved P1-U1 Functional Design and NFR Requirements. It keeps the generator a local CLI with no new infrastructure or service pattern. Default workload includes 1,096,000 daily inventory rows; dataset sizes and date range are configurable, but no maximum-size or fixed runtime/memory target is promised.

## Generation and Resource Pattern
- Use a simple in-memory generation flow: resolve settings, construct the configured entity collections, validate their keys/relationships/domain rules/scenario presence, then write the entity CSVs.
- Stable entity ordering, deterministic seeded variation, stable IDs, fixed default dates, and canonical CSV formatting preserve logical repeatability.
- This choice favors a straightforward implementation but memory use grows with configured size; very large custom configurations may exhaust local memory. No streaming/batching optimization is required by this design. If practical limits are discovered, report them and seek a design change rather than silently switching patterns.
- The CLI reports elapsed run duration and generated row counts. It does not enforce time limits or collect peak-memory/output-size metrics.

## Validation and Publication Pattern
1. Validate configuration before generating entities; invalid settings fail with a field-specific diagnostic.
2. Construct configured entities and evaluate the approved source-level checks before writing the accepted data set.
3. Write the five CSV entity files directly to configured source paths.
4. Publish the success manifest only after all expected entity files are written and source/scenario checks pass; it includes effective settings, row counts, paths, checksums, schema version, and validation outcomes.
5. P1-U2 accepts a source run only when a valid success manifest exists and its listed files/checksums are present and match.

There is no temporary-run promotion, backup, retention, or automatic cleanup subsystem. A process or filesystem failure during output writing may leave partial/unmanifested files or affect a prior run at the same paths. Such files are not a valid source contract; the operator corrects the cause and reruns generation. This accepted limitation is documented and visible in the CLI failure summary.

## Failure and Retry Pattern
- Fail fast on configuration errors, generation/validation failures, and local file-operation errors.
- Do not automatically retry. Report the failed operation and error in actionable terms; the operator may rerun with the same configuration after resolving the cause.
- Do not publish a success manifest for an unsuccessful or incomplete run.
- No automatic rollback or preservation of earlier source outputs is guaranteed.

## Performance and Scale Pattern
- Keep seed, date range, and entity volumes configurable; no named stress profile is embedded in U1.
- Report actual row counts and elapsed run time for default and user-configured runs. Use these as observational evidence, not hardware-independent acceptance thresholds.
- The default snapshot-row count follows `product_count × inclusive calendar days`; custom range/volume runs can be used for local performance experiments.

## Privacy and Security Pattern
- Generate only synthetic labels and values; no external network calls, production data, or real personal identities.
- Keep generated CSVs and manifest under ignored local runtime paths; publish schemas/instructions, not data files, to source control.
- No authentication, authorization, encryption service, secrets store, or security infrastructure is applicable to this offline generator. The project's approved data-safety constraints still apply although the Security Baseline extension is disabled.

## Explicitly Not Applied
No queue, cache, circuit breaker, distributed worker, hosted storage, service failover, backup schedule, automatic retry, hard SLA, or named stress profile is introduced. These would add complexity not requested for this local PoC unit.

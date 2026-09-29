# P1-U2 Functional Design — Clarification Questions

I reviewed the answers in [p1-u2-functional-design-plan.md](p1-u2-functional-design-plan.md). Q1 and Q2 are clear. Q3's “simple allowed” does not specify whether Bronze reruns replace data or retain prior runs. Q4 selects ignoring checksum mismatches, which conflicts with the already-approved P1-U1 handoff contract requiring matching SHA-256 checksums before P1-U2 ingestion. Please resolve both points below.

## Question 1: Bronze repeat-load behavior
Which concrete behavior did you mean by “simple allowed” for Q3?

A) Keep one current Bronze output set and replace it on each successful run after the complete source preflight passes; do not retain earlier Bronze runs (simplest local PoC behavior)

B) Write each accepted source-manifest/run to a distinct immutable Bronze run directory and retain earlier runs (stronger lineage, additional storage)

C) Keep one current output set by default and add an optional run-retention mode

X) Other (please describe after [Answer]: tag below)

[Answer]: A - replace current Bronze output after a successful run, but only after all source checks pass; do not retain earlier Bronze runs in the default minimal behavior

## Question 2: Checksum mismatch versus the approved source contract
P1-U1 Functional Design and the approved U1 source schema specify that P1-U2 accepts a source run only when all listed file checksums match. Your Q4 answer selects ignoring checksum mismatches. Which contract should govern P1-U2?

A) Preserve the approved contract: require matching SHA-256 checksums and fail the whole Bronze load before publishing any outputs if a mismatch occurs (recommended; detects changed/truncated data)

B) Change the cross-unit contract: accept parseable CSVs even when hashes differ, and revise P1-U1 documentation/tests and its acceptance handoff before U2 implementation (reduces integrity protection and requires reopening the approved U1 contract)

C) Check manifest, entity names/counts, and CSV parseability, but treat checksums as informational only; revise U1 documentation/tests and acceptance handoff accordingly

X) Other (please describe after [Answer]: tag below)

[Answer]: A - preserve the approved P1-U1 contract: require matching SHA-256 checksums and fail the whole Bronze load before publishing any outputs if a mismatch occurs

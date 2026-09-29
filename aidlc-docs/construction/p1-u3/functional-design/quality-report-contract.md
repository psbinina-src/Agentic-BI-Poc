# P1-U3 Quality Report Contract

## Purpose
The quality report is the evidence boundary for the accepted Silver layer. It names every applicable quality rule and records whether the rule passed or failed for the current run.

## Required Format
The report should include:
- run ID
- source Bronze run ID
- table name
- check name
- check description
- pass/fail outcome
- sample rows or counts
- timestamp

## Required Checks
- required field completeness
- valid ISO dates
- duplicate key detection
- null and invalid value detection
- domain validation for status/category fields
- referential integrity across entity relationships

## Gate Behavior
If any critical check fails, the Silver layer is not accepted for downstream Gold modeling. The failure must be explicit in the report and the run status must be marked failed.

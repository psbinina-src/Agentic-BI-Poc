# P1-U1 NFR Requirements — Clarification Questions

I reviewed your three responses in [p1-u1-nfr-requirements-plan.md](p1-u1-nfr-requirements-plan.md). “Keep it simple,” “simple,” and “minimum or no, just good data for now” express a preference for minimal NFR overhead but do not fully specify performance evidence, a named stress profile, or failed-run output behavior. Please confirm the following concrete interpretation or choose an alternative.

## Question 1: Minimal performance evidence
Which performance treatment should apply?

A) No hard time/memory pass-fail targets; include elapsed time and generated row counts in the ordinary run summary when readily available (recommended minimal evidence)

B) Do not collect or report performance information for P1-U1

C) Define a specific benchmark/limit; provide it after `[Answer]:`

X) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 2: Named scalability profile
Should U1 define an additional named stress profile beyond the default dataset?

A) No named stress profile; keep date range and sizes configurable so the user can create performance-test runs as needed (recommended minimal scope)

B) Add the previously listed larger profile: five years, about 50,000 customers, 5,000 products, and 1,000,000 order lines

C) Add a different named profile; specify date range, customer count, product count, and order-line count after `[Answer]:`

X) Other (please describe after [Answer]: tag below)

[Answer]: X - nothing , skip

## Question 3: Minimal failed-run output behavior
Which output handling should apply, retaining the already approved rule that a success manifest is published only after all generated files and source validations succeed?

A) Write to the configured source paths directly; on failure, do not publish a success manifest, but do not add staging/backup or a guarantee that a prior successful dataset is preserved (recommended minimal implementation)

B) Write to a temporary run directory and promote only after validation, preserving the prior successful dataset on failure

C) Specify another behavior after `[Answer]:`

X) Other (please describe after [Answer]: tag below)

[Answer]: X- for now nothing

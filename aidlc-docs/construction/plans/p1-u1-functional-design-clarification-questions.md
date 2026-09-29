# P1-U1 Functional Design — Clarification Question

I reviewed the answers in [p1-u1-functional-design-plan.md](p1-u1-functional-design-plan.md). Questions 1, 3, and 4 are clear. Question 2 selects a current-date-anchored default window with seed `42`, while the approved requirement also says that the same settings and seed must reproduce the same logical dataset. A moving default date means a later run can use different dates unless the resolved window is captured and reused.

## Question 1: Reproducibility with a rolling date window
Which behavior should apply to the default three-year date range?

A) Keep the current-date-anchored default. Resolve and record the actual start/end dates in the generated manifest; an exact replay must reuse those recorded dates, while a fresh run later may cover a different date window.

B) Use a fixed historical default date window and seed so an unchanged default configuration remains reproducible over time (recommended for stable default regeneration).

X) Other (please describe after [Answer]: tag below)

[Answer]: B — use the previously proposed fixed default window 2023-01-01 through 2025-12-31 inclusive and retain seed 42. Keep both dates and the seed configurable.

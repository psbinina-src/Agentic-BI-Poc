# P2-U1 Functional Design — Clarification

Your selected answers were:
- Lookback: A — 30 complete calendar days strictly before the snapshot date.
- Zero demand / incomplete history: B — use available partial history; publish zero coverage for zero demand with a status field.

One detail in the partial-history choice needs a denominator so the velocity measure is deterministic.

## Question 1: Partial-history denominator
If fewer than 30 days of eligible sales history exist before an inventory snapshot, how should average daily sales velocity be calculated?

A) Divide completed-order units by the number of calendar days with valid history available (up to 30), including days with no sales. If no prior history exists, publish velocity and coverage as NULL with an insufficient-history status. (Recommended.)

B) Divide completed-order units by 30 even when fewer than 30 days are available; treat unavailable earlier days as zero-demand days.

X) Other (please describe after [Answer]: tag below)

[Answer]: B
[Answer]: B — keep a fixed 30-day denominator for partial history; unavailable days count as zero-demand days.

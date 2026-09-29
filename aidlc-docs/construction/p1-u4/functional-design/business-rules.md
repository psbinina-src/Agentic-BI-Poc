# P1-U4 Business Rules — Gold Models, Samples, and Phase 2 Handoff

## Core Rules
1. Gold is derived only from accepted Silver outputs and the final quality report.
2. Sales is at order-line grain; inventory is at daily product grain.
3. Order-line revenue is derived deterministically from quantity × unit price × (1 - discount_rate).
4. Net revenue is defined as gross sales minus discount amount.
5. Customer profile metrics are computed only from accepted orders and customer dimension data.
6. Inventory metrics such as stock coverage and low-stock flags are derived from daily product snapshots.
7. The Gold layer must remain traceable to the accepted Silver run and source lineage metadata.
8. The final P1-U4 output must support the Phase 2 semantic modeling handoff.

## Quality Gate
Gold work only begins after the Silver quality report passes and is accepted as the upstream contract.

# Phase 1 Requirement Verification Questions

Please answer each question by entering the option letter after `[Answer]:`. For `X) Other`, add the details after the letter. These answers will finalize Phase 1 assumptions before story, slice, and unit planning. The delivery baseline is already set to one team with one data engineer owning the Phase 1 work.

## Question 1: Transformation and source-file approach
Which local-first implementation approach should Phase 1 use for synthetic data, ingestion, and Bronze/Silver/Gold transformations?

A) Python utility plus DuckDB SQL transformations; store generated and modeled data as Parquet (recommended for the stated DuckDB/local-file target)

B) Python utility plus dbt-duckdb transformations; store generated and modeled data as Parquet

C) Python utility plus DuckDB SQL transformations; use CSV for generated inputs and Parquet for modeled outputs

X) Other (please describe after [Answer]: tag below)

[Answer]: A - but use csv for raw and parquet for lakehouse - ensure to create spearate root  folders in the repo for lakehouse/related artifacts within subfolders arranged

## Question 2: Sales and inventory grains
Which default grains should the Gold model use?

A) Sales fact at order-line grain; inventory as daily product-level snapshots (recommended, supports transaction detail and stock trends)

B) Sales fact at order grain; inventory as product-level movements

C) Sales fact at order-line grain; inventory as product-level movements

X) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 3: Forecast representation for Phase 1
How should Phase 1 provide forecast-versus-actual analysis?

A) Include a simple, deterministic baseline forecast in Gold (for example, a documented trailing-period average); treat it as a PoC benchmark, not a production forecast

B) Include synthetic forecast records generated alongside sales data, without implementing a forecasting calculation

C) Deliver forecast-ready historical measures only; defer forecast values and comparisons to a later phase

X) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 4: Reproducible dataset defaults
What default dataset size and date coverage should the generator use while keeping both configurable?

A) 3 years, about 10,000 customers, 1,000 products, and 100,000 order lines (recommended PoC default; inventory snapshot volume follows the selected grain)

B) 1 year, about 1,000 customers, 250 products, and 10,000 order lines (small development default)

C) 5 years, about 50,000 customers, 5,000 products, and 1,000,000 order lines (larger performance-test default)

X) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 5: Property-Based Testing Extension
Should property-based testing (PBT) rules be enforced for this project?

A) Yes — enforce all PBT rules as blocking constraints (recommended for data generation and transformation logic)

B) Partial — enforce PBT rules only for pure functions and serialization round-trips

C) No — skip all PBT rules

X) Other (please describe after [Answer]: tag below)

[Answer]: C

## Question 6: Security Baseline Extension
Should security extension rules be enforced for this project?

A) Yes — enforce all SECURITY rules as blocking constraints

B) No — skip all SECURITY rules (suitable for this local-first PoC)

X) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 7: Resiliency Baseline Extension
Should the resiliency baseline be applied as directional design-time guidance?

A) Yes — apply the resiliency baseline as directional best practices

B) No — skip the resiliency baseline (suitable for a local PoC prioritizing rapid iteration)

X) Other (please describe after [Answer]: tag below)

[Answer]: B

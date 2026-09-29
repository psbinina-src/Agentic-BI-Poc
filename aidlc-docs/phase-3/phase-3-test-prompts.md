# Phase 3 Prompt Test Results

Use the dashboard at `http://127.0.0.1:8200/`. The following prompts returned a successful Phase 3 API response with a validated Vega-Lite chart and aggregated data during live testing on 2026-09-30:

| # | Prompt tested | Gold query | Groups returned | Result |
|---|---|---|---:|---|
| 1 | Show net sales by customer region. | Sales joined to customers; sum net sales by region. | 5 | Pass |
| 2 | Show units sold by product category. | Sales joined to products; sum quantity by category. | 4 | Pass |
| 3 | What is the average discount rate by sales channel? | Average discount rate by channel. | 3 | Pass |
| 4 | Compare average product-day stock coverage by product category. | Inventory joined to products; average coverage by category. | 4 | Pass |
| 5 | Daily net sales by region during December 2025. | Daily net sales grouped by date and customer region, bounded to December 2025. | 155 | Pass |
| 6 | Net sales by customer segment. | Sales joined to customers; sum net sales by segment. | 3 | Pass |

All six successful results used aggregate Gold data only; no row-level customer or product IDs were returned.

## Dashboard Suggestion Status

| Suggestion | Status |
|---|---|
| Daily net sales by region during December 2025 | Pass — same prompt as test 5. |
| Net sales by customer segment | Pass — same prompt as test 6. |
| Count low-stock products with positive demand by category on 2025-12-31 | Not verified live. The earlier run failed because the model selected an ambiguous unqualified `product_id`. A base-table key-count qualification fix is covered by automated tests, but no post-fix live retest was performed before Phase 3 sign-off. |

## Phase 2 Data-Access Checks
The matching Phase 2 `POST /query` requests were separately verified against Gold Parquet for five contracts: net sales by channel (3 groups), net sales by customer region (5), units sold by category (4), average discount by channel (3), and average stock coverage by category (4). These checks validate the data endpoint independently of LLM interpretation.

## Manual Pass Criteria
For each live dashboard test:
1. The assistant returns an answer and insight grounded in the aggregated results.
2. A Vega-Lite chart renders with x/y fields present in the result columns.
3. **View aggregated data** displays the result rows.
4. No row-level customer/product IDs appear.

Also try an unsupported prompt such as **Forecast next quarter's revenue.** Gold contains no forecast dataset; the assistant should explain that limitation rather than inventing a forecast.

## Sign-Off Boundary
Phase 3 was signed off using the results above at the user's direction to stop testing. Do not interpret the pending low-stock row or the unsupported-request example as a live pass.

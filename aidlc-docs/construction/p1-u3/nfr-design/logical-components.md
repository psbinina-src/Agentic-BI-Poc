# P1-U3 Logical Components — Silver Standardization and Data Quality

## Component Inventory

### 1. Bronze Intake Validator
Validates the accepted Bronze outputs and run metadata before any Silver standardization starts.

### 2. Standardization Component
Standardizes raw Bronze values into typed Silver domain structures while preserving the original keys and lineage fields.

### 3. Quality Check Component
Runs the required data quality checks:
- required field checks
- null checks
- duplicate key checks
- type validation
- referential integrity checks
- domain validation

### 4. Quality Report Component
Publishes the named pass/fail results and aggregated evidence.

### 5. Silver Publisher
Writes the final accepted Silver outputs to the local lakehouse path.

## Interaction Order
1. Validate Bronze inputs
2. Standardize Bronze to typed Silver
3. Run quality checks
4. Publish quality report
5. Publish Silver outputs only when critical checks pass

This structure ensures Silver is evidence-backed and ready for the P1-U4 Gold stage.

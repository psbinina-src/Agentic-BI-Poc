# Phase 4 Commands — Product Sales & Inventory Monitor

Run from the repository root in Windows PowerShell.

## Prerequisites
- Python dependencies installed with `py -m pip install -e ".[test]"`.
- Phase 1 Gold Parquet files present under `lakehouse/gold/`.

## Generate Dashboard Data

```powershell
py -m p4_dashboard.generate
```

This refreshes `dashboard/data.json` from the Gold Parquet files.

## Start the Static Dashboard

```powershell
py -m http.server 8000 --directory dashboard
```

Open `http://127.0.0.1:8000/`. Stop with `Ctrl+C`.

## Test

```powershell
py -m pytest tests/test_phase4_dashboard.py -q
py -m pytest -q
```

The generator and static server are independent of Phase 2 and Phase 3 services. Regenerate data after rebuilding Gold so the dashboard reflects the latest Parquet outputs.

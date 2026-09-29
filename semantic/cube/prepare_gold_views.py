from __future__ import annotations

import argparse
from pathlib import Path

import duckdb

GOLD_TABLES = ("sales_gold", "customers_gold", "products_gold", "inventory_gold")


def _sql_path(path: Path) -> str:
    return "'" + path.resolve().as_posix().replace("'", "''") + "'"


def prepare_gold_views(gold_dir: Path, database_path: Path) -> None:
    missing = [gold_dir / f"{table}.parquet" for table in GOLD_TABLES if not (gold_dir / f"{table}.parquet").is_file()]
    if missing:
        raise FileNotFoundError("Required Gold Parquet files are missing: " + ", ".join(map(str, missing)))

    database_path.parent.mkdir(parents=True, exist_ok=True)
    with duckdb.connect(str(database_path)) as connection:
        for table in GOLD_TABLES:
            parquet_path = gold_dir / f"{table}.parquet"
            connection.execute(
                f"CREATE OR REPLACE VIEW {table} AS SELECT * FROM read_parquet({_sql_path(parquet_path)})"
            )


def main() -> int:
    workspace_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description="Register local Gold Parquet files as DuckDB views for Cube Core.")
    parser.add_argument("--gold-dir", type=Path, default=workspace_root / "lakehouse" / "gold")
    parser.add_argument("--database-path", type=Path, default=workspace_root / ".local" / "agentic_bi.duckdb")
    args = parser.parse_args()

    prepare_gold_views(args.gold_dir, args.database_path)
    print(f"Registered {', '.join(GOLD_TABLES)} in {args.database_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from p1_u2.config import BronzeConfig
from p1_u2.ingest import ingest_source_to_bronze


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Load validated source CSVs into the Bronze layer.")
    parser.add_argument("--source-dir", type=Path, required=True, help="directory containing manifest.json and source CSV files")
    parser.add_argument("--bronze-dir", type=Path, required=True, help="target Bronze directory")
    parser.add_argument("--run-id", help="optional explicit run identifier for Bronze lineage")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        config = BronzeConfig(source_dir=args.source_dir, bronze_dir=args.bronze_dir, run_id=args.run_id)
        results = ingest_source_to_bronze(config)
    except Exception as exc:  # pragma: no cover - CLI failure contract
        print(f"Bronze ingest failed: {exc}", file=sys.stderr)
        return 1

    print(f"Bronze ingest succeeded for run {config.run_id or 'default'}")
    for name, rel in results.items():
        print(f"{name}: {rel.shape[0]} rows -> {config.bronze_dir / f'{name}.parquet'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

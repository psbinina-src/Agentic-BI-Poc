from __future__ import annotations

import argparse
import sys
from pathlib import Path

from p1_u3.config import SilverConfig
from p1_u3.quality import run_quality_checks
from p1_u3.transform import standardize_bronze_to_silver


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build typed Silver outputs from accepted Bronze files.")
    parser.add_argument("--bronze-dir", type=Path, required=True, help="directory containing Bronze Parquet files")
    parser.add_argument("--silver-dir", type=Path, required=True, help="target directory for Silver outputs")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        config = SilverConfig(bronze_dir=args.bronze_dir, silver_dir=args.silver_dir)
        outputs = standardize_bronze_to_silver(config)
        report = run_quality_checks(args.silver_dir, outputs)
        if not report["passed"]:
            raise ValueError("Silver quality checks failed")
    except Exception as exc:  # pragma: no cover - CLI contract behavior
        print(f"Silver build failed: {exc}", file=sys.stderr)
        return 1

    print(f"Silver build succeeded: {len(outputs)} tables written to {args.silver_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

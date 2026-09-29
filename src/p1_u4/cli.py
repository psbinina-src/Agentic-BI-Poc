from __future__ import annotations

import argparse
import sys
from pathlib import Path

from p1_u4.config import GoldConfig
from p1_u4.gold import build_gold
from p1_u4.queries import run_sample_queries


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build Gold models and sample outputs from accepted Silver data.")
    parser.add_argument("--silver-dir", type=Path, required=True, help="directory containing accepted Silver Parquet files")
    parser.add_argument("--gold-dir", type=Path, required=True, help="directory for Gold outputs and sample query evidence")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        config = GoldConfig(silver_dir=args.silver_dir, gold_dir=args.gold_dir)
        outputs = build_gold(config)
        _ = run_sample_queries(args.gold_dir)
    except Exception as exc:  # pragma: no cover - CLI contract behavior
        print(f"Gold build failed: {exc}", file=sys.stderr)
        return 1

    print(f"Gold build succeeded with {len(outputs)} objects in {args.gold_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

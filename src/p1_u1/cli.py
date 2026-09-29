"""Command-line entry point for the P1-U1 generator."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from p1_u1.config import ConfigurationError, GeneratorConfig, load_config
from p1_u1.csv_writer import write_entity_csvs
from p1_u1.generator import generate_dataset
from p1_u1.manifest import MANIFEST_FILENAME, publish_success_manifest
from p1_u1.models import GenerationResult
from p1_u1.validation import validate_dataset


class GenerationError(RuntimeError):
    """Raised when the configured dataset fails source-level validation."""


def run_generation(config: GeneratorConfig) -> GenerationResult:
    """Generate, validate, write CSV outputs, then publish the manifest last."""
    started = time.perf_counter()
    dataset = generate_dataset(config)
    validation = validate_dataset(dataset, config)
    elapsed = time.perf_counter() - started
    if not validation.passed:
        details = "; ".join(issue.message for issue in validation.issues[:8])
        raise GenerationError(f"source validation failed: {details}")

    config.output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = config.output_dir / MANIFEST_FILENAME
    # Invalidate an earlier success marker before directly overwriting its files.
    # If a later write fails, partial files cannot masquerade as the prior run.
    manifest_path.unlink(missing_ok=True)
    outputs = write_entity_csvs(dataset, config.output_dir)
    manifest = publish_success_manifest(config, dataset, validation, outputs)
    elapsed = time.perf_counter() - started
    return GenerationResult(dataset=dataset, validation=validation, elapsed_seconds=elapsed, manifest=manifest)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate deterministic synthetic P1-U1 source CSVs.")
    parser.add_argument("--config", type=Path, default=None, help="TOML configuration file")
    parser.add_argument("--seed", type=int, help="deterministic random seed")
    parser.add_argument("--start-date", help="inclusive start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="inclusive end date (YYYY-MM-DD)")
    parser.add_argument("--customers", type=int, dest="customer_count", help="number of synthetic customers")
    parser.add_argument("--products", type=int, dest="product_count", help="number of synthetic products")
    parser.add_argument("--order-lines", type=int, dest="order_line_count", help="exact number of order lines")
    parser.add_argument("--output-dir", type=Path, help="source output directory (default: lakehouse/source)")
    return parser


def _format_counts(counts: dict[str, int]) -> str:
    return ", ".join(f"{name}={count}" for name, count in counts.items())


def main(argv: list[str] | None = None) -> int:
    """Parse options, run generation and print a concise summary."""
    args = _parser().parse_args(argv)
    try:
        config = load_config(
            args.config,
            seed=args.seed,
            start_date=args.start_date,
            end_date=args.end_date,
            customer_count=args.customer_count,
            product_count=args.product_count,
            order_line_count=args.order_line_count,
            output_dir=args.output_dir,
        )
        result = run_generation(config)
    except (ConfigurationError, GenerationError, OSError) as exc:
        print(f"Generation failed: {exc}", file=sys.stderr)
        print("No success manifest was published for this run.", file=sys.stderr)
        return 1

    print(
        "Generation succeeded: "
        f"seed={config.seed}, dates={config.start_date.isoformat()}..{config.end_date.isoformat()}, "
        f"counts[{_format_counts(result.dataset.entity_counts())}], "
        f"elapsed_seconds={result.elapsed_seconds:.3f}"
    )
    for name, path in result.manifest.output_files.items():
        print(f"{name}: {path}")
    print(f"manifest: {result.manifest.manifest_path.resolve()}")
    return 0

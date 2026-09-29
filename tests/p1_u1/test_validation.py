from dataclasses import replace
from datetime import date
from pathlib import Path

from p1_u1.config import GeneratorConfig
from p1_u1.generator import generate_dataset
from p1_u1.validation import validate_dataset


def test_validator_rejects_unknown_product_reference() -> None:
    config = GeneratorConfig(42, date(2023, 1, 1), date(2023, 3, 31), 20, 10, 100, Path("unused"))
    dataset = generate_dataset(config)
    dataset.order_lines[0] = replace(dataset.order_lines[0], product_id="UNKNOWN")
    report = validate_dataset(dataset, config)
    assert not report.passed
    assert any(issue.code == "unknown_product" for issue in report.issues)


def test_validator_rejects_duplicate_customer_id() -> None:
    config = GeneratorConfig(42, date(2023, 1, 1), date(2023, 3, 31), 20, 10, 100, Path("unused"))
    dataset = generate_dataset(config)
    dataset.customers[1] = replace(dataset.customers[1], customer_id=dataset.customers[0].customer_id)
    report = validate_dataset(dataset, config)
    assert not report.passed
    assert any(issue.code == "duplicate_customer_id" for issue in report.issues)

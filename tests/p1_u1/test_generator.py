from datetime import date
from pathlib import Path

from p1_u1.config import GeneratorConfig
from p1_u1.generator import generate_dataset
from p1_u1.validation import validate_dataset


def small_config(**overrides: object) -> GeneratorConfig:
    values: dict[str, object] = {
        "seed": 42,
        "start_date": date(2023, 1, 1),
        "end_date": date(2023, 3, 31),
        "customer_count": 50,
        "product_count": 20,
        "order_line_count": 500,
        "output_dir": Path("unused"),
    }
    values.update(overrides)
    return GeneratorConfig(**values)  # type: ignore[arg-type]


def test_same_config_generates_identical_entities_and_ids() -> None:
    config = small_config()
    first = generate_dataset(config)
    second = generate_dataset(config)
    assert first == second
    assert first.entity_counts() == second.entity_counts()
    assert first.order_lines[-1].order_line_id == "LINE-0000500"


def test_entities_are_related_and_scenarios_exist() -> None:
    config = small_config()
    dataset = generate_dataset(config)
    assert len(dataset.customers) == 50
    assert len(dataset.products) == 20
    assert len(dataset.order_lines) == 500
    assert len(dataset.inventory_snapshots) == 20 * 90
    assert all(order.order_id for order in dataset.orders)
    assert validate_dataset(dataset, config).passed


def test_small_single_day_window_still_has_required_non_time_scenarios() -> None:
    config = small_config(end_date=date(2023, 1, 1), order_line_count=100)
    dataset = generate_dataset(config)
    report = validate_dataset(dataset, config)
    assert report.scenarios["repeat_purchasing"]
    assert report.scenarios["low_stock_with_sales_velocity"]
    assert report.passed

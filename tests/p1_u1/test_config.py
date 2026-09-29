from datetime import date
from pathlib import Path

import pytest

from p1_u1.config import ConfigurationError, load_config


def test_default_config_uses_approved_values() -> None:
    config = load_config()
    assert config.seed == 42
    assert config.start_date == date(2023, 1, 1)
    assert config.end_date == date(2025, 12, 31)
    assert config.customer_count == 10_000
    assert config.product_count == 1_000
    assert config.order_line_count == 100_000
    assert config.inventory_snapshot_count == 1_096_000


def test_toml_config_and_explicit_overrides(tmp_path: Path) -> None:
    config_file = tmp_path / "config.toml"
    config_file.write_text(
        '[generator]\nseed=7\nstart_date="2024-01-01"\nend_date="2024-01-02"\n'
        'customer_count=3\nproduct_count=2\norder_line_count=9\noutput_dir="source"\n',
        encoding="utf-8",
    )
    config = load_config(config_file, seed=8, customer_count=4, output_dir=tmp_path / "out")
    assert config.seed == 8
    assert config.customer_count == 4
    assert config.product_count == 2
    assert config.inventory_snapshot_count == 4
    assert config.output_dir == tmp_path / "out"


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        ({"customer_count": 0}, "customer_count must be a positive integer"),
        ({"product_count": -1}, "product_count must be a positive integer"),
        ({"order_line_count": 0}, "order_line_count must be a positive integer"),
        ({"seed": True}, "seed must be an integer"),
        ({"start_date": "2024-02-30"}, "start_date must be a valid ISO date"),
        ({"start_date": "2024-02-02", "end_date": "2024-02-01"}, "end_date must be on or after start_date"),
        ({"output_dir": ""}, "output_dir must be a non-empty path"),
    ],
)
def test_invalid_configuration_is_rejected(overrides: dict[str, object], message: str) -> None:
    with pytest.raises(ConfigurationError, match=message):
        load_config(**overrides)


def test_missing_explicit_config_file_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(ConfigurationError, match="config file does not exist"):
        load_config(tmp_path / "missing.toml")

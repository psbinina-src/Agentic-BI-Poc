from pathlib import Path

from p1_u1.cli import main


def test_cli_reports_success_settings_counts_and_elapsed_time(tmp_path: Path, capsys) -> None:
    result = main([
        "--seed", "9",
        "--start-date", "2023-01-01",
        "--end-date", "2023-02-28",
        "--customers", "20",
        "--products", "10",
        "--order-lines", "100",
        "--output-dir", str(tmp_path),
    ])
    output = capsys.readouterr().out
    assert result == 0
    assert "seed=9" in output
    assert "customers=20" in output
    assert "elapsed_seconds=" in output
    assert (tmp_path / "manifest.json").exists()


def test_cli_rejects_invalid_configuration(capsys) -> None:
    result = main(["--customers", "0"])
    output = capsys.readouterr().err
    assert result == 1
    assert "customer_count must be a positive integer" in output
    assert "No success manifest" in output

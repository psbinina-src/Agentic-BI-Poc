from pathlib import Path

import duckdb

from p1_u3.quality import run_quality_checks


def test_quality_report_marks_pass_for_nonempty_tables(tmp_path: Path) -> None:
    rel = duckdb.sql("SELECT 1 AS a, 'x' AS b")
    report = run_quality_checks(tmp_path, {"customers": rel})
    assert report["passed"] is True
    assert any(item["check"] == "required_fields_present" for item in report["checks"])

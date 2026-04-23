from pathlib import Path

from src.build_repurpose_plan import build_plan


def test_build_plan(tmp_path: Path) -> None:
    csv_path = tmp_path / "sources.csv"
    csv_path.write_text(
        "source_title,source_url,key_topic,audience\n"
        "Video A,https://example.com/a,Topic A,SMB owners\n"
    )
    result = build_plan(csv_path, tmp_path / "out")
    assert result.clip_count == 1
    assert (tmp_path / "out" / "clip_plan.csv").exists()
    assert (tmp_path / "out" / "publishing_calendar.md").exists()

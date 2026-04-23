from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass
class BuildResult:
    output_dir: Path
    clip_count: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate faceless content repurposing plans")
    parser.add_argument("--input", required=True, help="Input CSV")
    parser.add_argument("--output", default="out", help="Output directory")
    return parser.parse_args()


def build_plan(input_csv: Path, output_dir: Path) -> BuildResult:
    if not input_csv.exists():
        raise FileNotFoundError(f"Input CSV not found: {input_csv}")

    clips: list[dict] = []
    with open(input_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"source_title", "source_url", "key_topic", "audience"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing headers: {sorted(missing)}")

        for row in reader:
            title = row["source_title"].strip()
            topic = row["key_topic"].strip()
            audience = row["audience"].strip()
            clips.append(
                {
                    "source_title": title,
                    "source_url": row["source_url"].strip(),
                    "key_topic": topic,
                    "audience": audience,
                    "hook": f"{topic}: what most {audience.lower()} miss",
                    "youtube_short_title": f"{topic} in 30s ({audience})",
                    "reddit_angle": f"Actionable breakdown for {audience} on {topic}",
                }
            )

    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "clip_plan.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        fields = [
            "source_title",
            "source_url",
            "key_topic",
            "audience",
            "hook",
            "youtube_short_title",
            "reddit_angle",
        ]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(clips)

    calendar = ["# Publishing Calendar", ""]
    for idx, clip in enumerate(clips, start=1):
        calendar.append(f"Day {idx}: {clip['youtube_short_title']}")
        calendar.append(f"- Hook: {clip['hook']}")
        calendar.append(f"- Repurpose to Reddit: {clip['reddit_angle']}")
        calendar.append("")

    (output_dir / "publishing_calendar.md").write_text("\n".join(calendar), encoding="utf-8")
    return BuildResult(output_dir=output_dir, clip_count=len(clips))


def main() -> None:
    args = parse_args()
    result = build_plan(Path(args.input), Path(args.output))
    print(f"Generated {result.clip_count} repurposing items -> {result.output_dir}")


if __name__ == "__main__":
    main()

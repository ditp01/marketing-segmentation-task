from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
import csv


REPO_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = REPO_ROOT / "timekeeping-logs.csv"
OUTPUT_PATH = REPO_ROOT / "timekeeping-total.csv"
TIME_FORMAT = "%H:%M"


def parse_time(value: str) -> datetime:
    return datetime.strptime(value.strip(), TIME_FORMAT)


def duration_minutes(start: str, end: str) -> int:
    start_dt = parse_time(start)
    end_dt = parse_time(end)
    if end_dt < start_dt:
        end_dt += timedelta(days=1)
    return int((end_dt - start_dt).total_seconds() // 60)


def format_hhmm(total_minutes: int) -> str:
    hours, minutes = divmod(total_minutes, 60)
    return f"{hours:02d}:{minutes:02d}"


def calculate_total_minutes(input_path: Path) -> tuple[int, int]:
    with input_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        required_columns = {"start", "end"}
        if reader.fieldnames is None or not required_columns.issubset(set(reader.fieldnames)):
            raise ValueError("Input CSV must contain 'start' and 'end' columns.")

        total_minutes = 0
        row_count = 0
        for row in reader:
            total_minutes += duration_minutes(row["start"], row["end"])
            row_count += 1

    return total_minutes, row_count


def write_total_csv(output_path: Path, total_minutes: int, row_count: int) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["entry_count", "total_minutes", "total_hours_decimal", "total_time_hhmm"],
        )
        writer.writeheader()
        writer.writerow(
            {
                "entry_count": row_count,
                "total_minutes": total_minutes,
                "total_hours_decimal": f"{total_minutes / 60:.2f}",
                "total_time_hhmm": format_hhmm(total_minutes),
            }
        )


def main() -> None:
    total_minutes, row_count = calculate_total_minutes(INPUT_PATH)
    write_total_csv(OUTPUT_PATH, total_minutes, row_count)
    print(f"Saved {OUTPUT_PATH.as_posix()}")
    print(f"Total entries: {row_count}")
    print(f"Total time: {format_hhmm(total_minutes)} ({total_minutes / 60:.2f} hours)")


if __name__ == "__main__":
    main()

from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.clean import EVALUATION_ONLY_COLUMNS, apply_stage_01_review_decisions
from src.load_data import load_marketing_data


def main() -> None:
    raw_path = REPO_ROOT / "data" / "raw" / "marketing_campaign.csv"
    processed_dir = REPO_ROOT / "data" / "processed"
    processed_path = processed_dir / "marketing_campaign_processed.csv"

    processed_dir.mkdir(parents=True, exist_ok=True)

    raw_df = load_marketing_data(raw_path)
    processed_df, summary = apply_stage_01_review_decisions(raw_df)

    processed_df.to_csv(processed_path, sep=";", index=False)

    evaluation_columns_present = [col for col in EVALUATION_ONLY_COLUMNS if col in processed_df.columns]
    clustering_exclusions = ["ID"] + evaluation_columns_present

    print("Processed dataset created.")
    print(f"Input rows: {summary.input_rows}")
    print(f"Output rows: {summary.output_rows}")
    print(f"Dropped missing Income rows: {summary.dropped_missing_income_rows}")
    print(f"Dropped Income==666666 rows: {summary.dropped_income_outlier_rows}")
    print(f"Dropped implausible Year_Birth rows: {summary.dropped_implausible_year_birth_rows}")
    print(
        "Year_Birth plausibility range used: "
        f"{summary.min_plausible_year_birth} to {summary.max_plausible_year_birth} "
        f"(reference year: {summary.reference_year_for_age_plausibility})"
    )
    print(f"Saved file: {processed_path.as_posix()}")
    print(
        "Columns reserved for evaluation (exclude from clustering): "
        + (", ".join(evaluation_columns_present) if evaluation_columns_present else "<none found>")
    )
    print("Identifier column to keep out of clustering features: ID")
    print("Recommended clustering exclusions for next stage: " + ", ".join(clustering_exclusions))


if __name__ == "__main__":
    main()

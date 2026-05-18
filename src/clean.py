from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

RARE_MARITAL_STATUS_VALUES = {"Alone", "Absurd", "YOLO"}
CONSTANT_COLUMNS_TO_DROP = ["Z_CostContact", "Z_Revenue"]
EVALUATION_ONLY_COLUMNS = [
    "Response",
    "AcceptedCmp1",
    "AcceptedCmp2",
    "AcceptedCmp3",
    "AcceptedCmp4",
    "AcceptedCmp5",
]


@dataclass(frozen=True)
class ProcessingSummary:
    input_rows: int
    output_rows: int
    dropped_missing_income_rows: int
    dropped_income_outlier_rows: int
    dropped_implausible_year_birth_rows: int
    reference_year_for_age_plausibility: int
    min_plausible_year_birth: int
    max_plausible_year_birth: int


def _get_reference_year_from_dates(df: pd.DataFrame, date_column: str = "Dt_Customer") -> int:
    if date_column not in df.columns:
        raise KeyError(f"Required column missing: {date_column}")
    parsed_dates = pd.to_datetime(df[date_column], errors="coerce")
    if parsed_dates.dropna().empty:
        raise ValueError(f"Could not parse any values in {date_column}.")
    return int(parsed_dates.max().year)


def apply_stage_01_review_decisions(df: pd.DataFrame) -> tuple[pd.DataFrame, ProcessingSummary]:
    """
    Apply approved Stage 01 review decisions to create a processed dataset.

    Rules applied:
    - Drop rows with missing Income
    - Drop rows where Income == 666666
    - Drop rows with implausible Year_Birth (< reference_year - 100 or > reference_year)
    - Replace rare Marital_Status values (Alone, Absurd, YOLO) with Unknown
    - Drop constant columns Z_CostContact and Z_Revenue
    """
    required_columns = {"Income", "Year_Birth", "Marital_Status", "Dt_Customer"}
    missing_required = sorted(required_columns - set(df.columns))
    if missing_required:
        raise KeyError(f"Missing required columns: {missing_required}")

    working = df.copy()
    input_rows = int(len(working))

    reference_year = _get_reference_year_from_dates(working, "Dt_Customer")
    min_plausible_year_birth = reference_year - 100
    max_plausible_year_birth = reference_year

    missing_income_mask = working["Income"].isna()
    income_outlier_mask = working["Income"] == 666666
    implausible_year_birth_mask = (working["Year_Birth"] < min_plausible_year_birth) | (
        working["Year_Birth"] > max_plausible_year_birth
    )

    dropped_missing_income_rows = int(missing_income_mask.sum())
    dropped_income_outlier_rows = int((income_outlier_mask & ~missing_income_mask).sum())
    dropped_implausible_year_birth_rows = int((implausible_year_birth_mask & ~missing_income_mask & ~income_outlier_mask).sum())

    drop_mask = missing_income_mask | income_outlier_mask | implausible_year_birth_mask
    processed = working.loc[~drop_mask].copy()

    processed["Marital_Status"] = processed["Marital_Status"].replace(
        {value: "Unknown" for value in RARE_MARITAL_STATUS_VALUES}
    )

    drop_columns = [col for col in CONSTANT_COLUMNS_TO_DROP if col in processed.columns]
    if drop_columns:
        processed = processed.drop(columns=drop_columns)

    summary = ProcessingSummary(
        input_rows=input_rows,
        output_rows=int(len(processed)),
        dropped_missing_income_rows=dropped_missing_income_rows,
        dropped_income_outlier_rows=dropped_income_outlier_rows,
        dropped_implausible_year_birth_rows=dropped_implausible_year_birth_rows,
        reference_year_for_age_plausibility=reference_year,
        min_plausible_year_birth=min_plausible_year_birth,
        max_plausible_year_birth=max_plausible_year_birth,
    )

    return processed, summary

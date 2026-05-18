from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

import numpy as np
import pandas as pd

DEFAULT_BINARY_COLUMNS = [
    "AcceptedCmp1",
    "AcceptedCmp2",
    "AcceptedCmp3",
    "AcceptedCmp4",
    "AcceptedCmp5",
    "Complain",
    "Response",
]

SPEND_COLUMNS = [
    "MntWines",
    "MntFruits",
    "MntMeatProducts",
    "MntFishProducts",
    "MntSweetProducts",
    "MntGoldProds",
]

PURCHASE_COLUMNS = [
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases",
]


@dataclass(frozen=True)
class DateAuditResult:
    parsed_dates: pd.Series
    parse_fail_count: int
    parse_fail_pct: float
    min_date: pd.Timestamp | None
    max_date: pd.Timestamp | None


def get_id_column(df: pd.DataFrame) -> str | None:
    for candidate in ("Id", "ID", "id"):
        if candidate in df.columns:
            return candidate
    return None


def build_missing_values_table(df: pd.DataFrame) -> pd.DataFrame:
    missing_count = df.isna().sum()
    table = pd.DataFrame(
        {
            "column": missing_count.index,
            "missing_count": missing_count.values,
            "missing_pct": (missing_count.values / max(len(df), 1)) * 100,
            "non_missing_count": len(df) - missing_count.values,
        }
    )
    return table.sort_values(["missing_count", "column"], ascending=[False, True]).reset_index(drop=True)


def build_constant_table(df: pd.DataFrame, near_constant_threshold: float = 0.95) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    row_count = max(len(df), 1)

    for column in df.columns:
        value_counts = df[column].value_counts(dropna=False)
        non_null_unique_count = int(df[column].nunique(dropna=True))

        if value_counts.empty:
            top_value = "<empty>"
            top_count = 0
            top_pct = 0.0
        else:
            top_value_raw = value_counts.index[0]
            top_value = "<missing>" if pd.isna(top_value_raw) else str(top_value_raw)
            top_count = int(value_counts.iloc[0])
            top_pct = (top_count / row_count) * 100

        is_constant = non_null_unique_count <= 1
        is_near_constant = (not is_constant) and ((top_pct / 100) >= near_constant_threshold)

        rows.append(
            {
                "column": column,
                "non_null_unique_count": non_null_unique_count,
                "top_value": top_value,
                "top_count": top_count,
                "top_pct": top_pct,
                "is_constant": is_constant,
                "is_near_constant": is_near_constant,
            }
        )

    return pd.DataFrame(rows).sort_values("column").reset_index(drop=True)


def build_numeric_summary_table(df: pd.DataFrame) -> pd.DataFrame:
    numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()
    if not numeric_columns:
        return pd.DataFrame(
            columns=[
                "column",
                "count",
                "missing_count",
                "missing_pct",
                "mean",
                "std",
                "min",
                "p01",
                "p05",
                "p25",
                "p50",
                "p75",
                "p95",
                "p99",
                "max",
                "iqr",
                "lower_bound",
                "upper_bound",
                "outlier_count",
                "outlier_pct",
                "negative_count",
            ]
        )

    describe = (
        df[numeric_columns]
        .describe(percentiles=[0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
        .T.reset_index()
        .rename(columns={"index": "column", "1%": "p01", "5%": "p05", "50%": "p50", "95%": "p95", "99%": "p99"})
    )

    rows: list[dict[str, object]] = []
    for _, row in describe.iterrows():
        column = row["column"]
        series = df[column].dropna()
        q1 = float(row["25%"])
        q3 = float(row["75%"])
        iqr = q3 - q1
        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)
        unique_non_null = int(series.nunique())
        if iqr == 0 or unique_non_null <= 2:
            outlier_count = 0
        else:
            outlier_count = int(((series < lower_bound) | (series > upper_bound)).sum())
        non_missing_count = int(series.shape[0])
        missing_count = int(df[column].isna().sum())
        missing_pct = (missing_count / max(len(df), 1)) * 100
        outlier_pct = (outlier_count / max(non_missing_count, 1)) * 100
        negative_count = int((series < 0).sum())

        rows.append(
            {
                "column": column,
                "count": float(row["count"]),
                "missing_count": missing_count,
                "missing_pct": missing_pct,
                "mean": float(row["mean"]),
                "std": float(row["std"]) if not pd.isna(row["std"]) else np.nan,
                "min": float(row["min"]),
                "p01": float(row["p01"]),
                "p05": float(row["p05"]),
                "p25": float(row["25%"]),
                "p50": float(row["p50"]),
                "p75": float(row["75%"]),
                "p95": float(row["p95"]),
                "p99": float(row["p99"]),
                "max": float(row["max"]),
                "iqr": iqr,
                "lower_bound": lower_bound,
                "upper_bound": upper_bound,
                "outlier_count": outlier_count,
                "outlier_pct": outlier_pct,
                "negative_count": negative_count,
            }
        )

    return pd.DataFrame(rows).sort_values("column").reset_index(drop=True)


def build_categorical_summary_table(
    df: pd.DataFrame,
    rare_threshold_pct: float = 1.0,
    exclude_columns: Iterable[str] | None = None,
) -> pd.DataFrame:
    categorical_columns = df.select_dtypes(include=["object", "category"]).columns.tolist()
    excluded = set(exclude_columns or [])
    rows: list[dict[str, object]] = []
    row_count = max(len(df), 1)

    for column in categorical_columns:
        if column in excluded:
            continue
        value_counts = df[column].value_counts(dropna=False)
        for level, count in value_counts.items():
            pct = (count / row_count) * 100
            rows.append(
                {
                    "column": column,
                    "level": "<missing>" if pd.isna(level) else str(level),
                    "count": int(count),
                    "pct": pct,
                    "is_rare": pct < rare_threshold_pct,
                    "is_missing_level": bool(pd.isna(level)),
                }
            )

    if not rows:
        return pd.DataFrame(columns=["column", "level", "count", "pct", "is_rare", "is_missing_level"])

    return pd.DataFrame(rows).sort_values(["column", "count"], ascending=[True, False]).reset_index(drop=True)


def build_binary_validation_table(df: pd.DataFrame, binary_columns: Iterable[str] = DEFAULT_BINARY_COLUMNS) -> pd.DataFrame:
    rows: list[dict[str, object]] = []

    for column in binary_columns:
        if column not in df.columns:
            rows.append(
                {
                    "column": column,
                    "present": False,
                    "invalid_value_count": np.nan,
                    "invalid_value_pct": np.nan,
                    "zero_count": np.nan,
                    "one_count": np.nan,
                    "positive_rate_pct": np.nan,
                    "missing_count": np.nan,
                }
            )
            continue

        series = df[column]
        missing_mask = series.isna()
        valid_mask = series.isin([0, 1])
        invalid_mask = (~missing_mask) & (~valid_mask)
        invalid_count = int(invalid_mask.sum())
        valid_non_missing = series[~missing_mask]
        one_count = int((valid_non_missing == 1).sum())
        zero_count = int((valid_non_missing == 0).sum())
        denominator = max(one_count + zero_count, 1)
        positive_rate = (one_count / denominator) * 100

        rows.append(
            {
                "column": column,
                "present": True,
                "invalid_value_count": invalid_count,
                "invalid_value_pct": (invalid_count / max(len(df), 1)) * 100,
                "zero_count": zero_count,
                "one_count": one_count,
                "positive_rate_pct": positive_rate,
                "missing_count": int(missing_mask.sum()),
            }
        )

    return pd.DataFrame(rows).sort_values("column").reset_index(drop=True)


def audit_dates(df: pd.DataFrame, date_column: str = "Dt_Customer") -> DateAuditResult:
    if date_column not in df.columns:
        empty = pd.Series(dtype="datetime64[ns]")
        return DateAuditResult(empty, parse_fail_count=0, parse_fail_pct=0.0, min_date=None, max_date=None)

    parsed = pd.to_datetime(df[date_column], errors="coerce")
    parse_fail_count = int(parsed.isna().sum() - df[date_column].isna().sum())
    parse_fail_pct = (parse_fail_count / max(len(df), 1)) * 100

    non_null = parsed.dropna()
    min_date = non_null.min() if not non_null.empty else None
    max_date = non_null.max() if not non_null.empty else None
    return DateAuditResult(parsed, parse_fail_count, parse_fail_pct, min_date, max_date)


def build_logical_consistency_table(df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    row_count = max(len(df), 1)

    available_spend_cols = [col for col in SPEND_COLUMNS if col in df.columns]
    available_purchase_cols = [col for col in PURCHASE_COLUMNS if col in df.columns]

    if available_spend_cols:
        spend_total = df[available_spend_cols].sum(axis=1)
        negative_spend_rows = int((df[available_spend_cols] < 0).any(axis=1).sum())
        rows.append(
            {
                "check": "negative_spend_values",
                "issue_count": negative_spend_rows,
                "issue_pct": (negative_spend_rows / row_count) * 100,
                "description": "Rows with at least one negative spend value.",
            }
        )
    else:
        spend_total = pd.Series(np.nan, index=df.index)

    if available_purchase_cols:
        purchase_total = df[available_purchase_cols].sum(axis=1)
        negative_purchase_rows = int((df[available_purchase_cols] < 0).any(axis=1).sum())
        rows.append(
            {
                "check": "negative_purchase_counts",
                "issue_count": negative_purchase_rows,
                "issue_pct": (negative_purchase_rows / row_count) * 100,
                "description": "Rows with at least one negative purchase count.",
            }
        )
    else:
        purchase_total = pd.Series(np.nan, index=df.index)

    if available_spend_cols and available_purchase_cols:
        spend_zero_purchase_positive = int(((spend_total == 0) & (purchase_total > 0)).sum())
        spend_positive_purchase_zero = int(((spend_total > 0) & (purchase_total == 0)).sum())
        rows.extend(
            [
                {
                    "check": "spend_zero_but_purchases_positive",
                    "issue_count": spend_zero_purchase_positive,
                    "issue_pct": (spend_zero_purchase_positive / row_count) * 100,
                    "description": "Rows with zero total spend but at least one purchase.",
                },
                {
                    "check": "spend_positive_but_no_purchases",
                    "issue_count": spend_positive_purchase_zero,
                    "issue_pct": (spend_positive_purchase_zero / row_count) * 100,
                    "description": "Rows with positive total spend but zero purchases across channels.",
                },
            ]
        )

    if "Recency" in df.columns:
        recency_out_of_range = int(((df["Recency"] < 0) | (df["Recency"] > 365)).sum())
        rows.append(
            {
                "check": "recency_out_of_range_0_365",
                "issue_count": recency_out_of_range,
                "issue_pct": (recency_out_of_range / row_count) * 100,
                "description": "Rows where Recency is outside 0-365 days.",
            }
        )

    return pd.DataFrame(rows).sort_values("check").reset_index(drop=True)


def build_plausibility_table(df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    current_year = datetime.now().year
    row_count = max(len(df), 1)

    if "Year_Birth" in df.columns:
        year_birth = df["Year_Birth"]
        invalid_year = int(((year_birth < 1900) | (year_birth > current_year)).sum())
        likely_under_18 = int((year_birth > (current_year - 18)).sum())
        likely_over_100 = int((year_birth < (current_year - 100)).sum())
        rows.extend(
            [
                {
                    "check": "year_birth_outside_1900_current_year",
                    "issue_count": invalid_year,
                    "issue_pct": (invalid_year / row_count) * 100,
                },
                {
                    "check": "likely_under_18_year_birth",
                    "issue_count": likely_under_18,
                    "issue_pct": (likely_under_18 / row_count) * 100,
                },
                {
                    "check": "likely_over_100_year_birth",
                    "issue_count": likely_over_100,
                    "issue_pct": (likely_over_100 / row_count) * 100,
                },
            ]
        )

    if "Income" in df.columns:
        income = df["Income"]
        negative_income = int((income < 0).sum())
        zero_income = int((income == 0).sum())
        very_high_income = int((income > 300000).sum())
        rows.extend(
            [
                {
                    "check": "negative_income",
                    "issue_count": negative_income,
                    "issue_pct": (negative_income / row_count) * 100,
                },
                {
                    "check": "zero_income",
                    "issue_count": zero_income,
                    "issue_pct": (zero_income / row_count) * 100,
                },
                {
                    "check": "income_above_300k",
                    "issue_count": very_high_income,
                    "issue_pct": (very_high_income / row_count) * 100,
                },
            ]
        )

    spend_columns = [col for col in SPEND_COLUMNS if col in df.columns]
    if spend_columns:
        any_negative_spend = int((df[spend_columns] < 0).any(axis=1).sum())
        rows.append(
            {
                "check": "rows_with_any_negative_spend",
                "issue_count": any_negative_spend,
                "issue_pct": (any_negative_spend / row_count) * 100,
            }
        )

    purchase_like_columns = [col for col in df.columns if col.startswith("Num")]
    if purchase_like_columns:
        any_negative_num = int((df[purchase_like_columns] < 0).any(axis=1).sum())
        rows.append(
            {
                "check": "rows_with_any_negative_num_variable",
                "issue_count": any_negative_num,
                "issue_pct": (any_negative_num / row_count) * 100,
            }
        )

    return pd.DataFrame(rows).sort_values("check").reset_index(drop=True)


def build_missingness_behavior_table(df: pd.DataFrame) -> pd.DataFrame:
    missing_any = df.isna().any(axis=1)
    if int(missing_any.sum()) == 0:
        return pd.DataFrame(columns=["feature", "mean_missing_any", "mean_not_missing_any", "difference", "pct_difference"])

    candidate_columns = [col for col in (SPEND_COLUMNS + PURCHASE_COLUMNS + ["Income", "Recency"]) if col in df.columns]
    rows: list[dict[str, float | str]] = []

    for column in candidate_columns:
        if not pd.api.types.is_numeric_dtype(df[column]):
            continue

        missing_mean = float(df.loc[missing_any, column].mean())
        non_missing_mean = float(df.loc[~missing_any, column].mean())
        difference = missing_mean - non_missing_mean
        pct_difference = np.nan
        if non_missing_mean != 0 and not np.isnan(non_missing_mean):
            pct_difference = (difference / non_missing_mean) * 100

        rows.append(
            {
                "feature": column,
                "mean_missing_any": missing_mean,
                "mean_not_missing_any": non_missing_mean,
                "difference": difference,
                "pct_difference": pct_difference,
            }
        )

    return pd.DataFrame(rows).sort_values("feature").reset_index(drop=True)

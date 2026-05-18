from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.audit import (
    DEFAULT_BINARY_COLUMNS,
    audit_dates,
    build_binary_validation_table,
    build_categorical_summary_table,
    build_constant_table,
    build_logical_consistency_table,
    build_missing_values_table,
    build_missingness_behavior_table,
    build_numeric_summary_table,
    build_plausibility_table,
    get_id_column,
)
from src.load_data import load_marketing_data


def as_markdown_code_block(dataframe: pd.DataFrame, max_rows: int = 15) -> str:
    if dataframe.empty:
        return "No rows."
    return "```\n" + dataframe.head(max_rows).to_string(index=False) + "\n```"


def write_stage_markdown(
    output_path: Path,
    data_path: Path,
    df: pd.DataFrame,
    id_column: str | None,
    missing_values: pd.DataFrame,
    numeric_summary: pd.DataFrame,
    categorical_summary: pd.DataFrame,
    constant_table: pd.DataFrame,
    binary_validation: pd.DataFrame,
    date_audit,
    logical_consistency: pd.DataFrame,
    plausibility: pd.DataFrame,
    missingness_behavior: pd.DataFrame,
    duplicate_row_count: int,
    duplicate_id_count: int | None,
    duplicate_id_unique_count: int | None,
) -> None:
    dtypes_table = (
        pd.DataFrame({"column": df.columns, "dtype": [str(dtype) for dtype in df.dtypes.values]})
        .sort_values("column")
        .reset_index(drop=True)
    )

    missing_rows = int(df.isna().any(axis=1).sum())
    total_cells = int(df.shape[0] * df.shape[1])
    missing_cells = int(df.isna().sum().sum())

    constant_columns = constant_table.loc[constant_table["is_constant"], "column"].tolist()
    near_constant_columns = constant_table.loc[constant_table["is_near_constant"], "column"].tolist()
    rare_levels = categorical_summary[categorical_summary["is_rare"]]
    outlier_table = numeric_summary[numeric_summary["outlier_count"] > 0].sort_values("outlier_pct", ascending=False)

    issues: list[str] = []
    income_missing_row = missing_values.loc[missing_values["column"] == "Income"]
    if not income_missing_row.empty and int(income_missing_row.iloc[0]["missing_count"]) > 0:
        count = int(income_missing_row.iloc[0]["missing_count"])
        pct = float(income_missing_row.iloc[0]["missing_pct"])
        issues.append(
            f"`Income` has missing values ({count} rows, {pct:.2f}%). Decide imputation strategy in Stage 02."
        )
    if duplicate_row_count > 0:
        issues.append(f"There are {duplicate_row_count} fully duplicated rows. Decide whether to deduplicate in Stage 02.")
    if duplicate_id_count and duplicate_id_count > 0:
        issues.append(
            f"`{id_column}` has {duplicate_id_count} duplicated rows across {duplicate_id_unique_count} duplicated IDs."
        )
    if constant_columns:
        issues.append(
            "Constant columns detected (" + ", ".join(f"`{col}`" for col in constant_columns) + "). Drop as non-informative."
        )
    if near_constant_columns:
        issues.append(
            "Near-constant columns detected (" + ", ".join(f"`{col}`" for col in near_constant_columns) + ")."
        )
    if not rare_levels.empty:
        rare_count = rare_levels.shape[0]
        issues.append(f"{rare_count} categorical levels are rare (<1%). Decide whether to combine levels in Stage 02.")
    if not outlier_table.empty:
        issues.append(
            "Potential clustering outliers detected in numeric features; decide winsorisation/capping/transformation strategy."
        )

    lines = [
        "# Stage 01 Data Audit",
        "",
        "## Dataset Overview",
        f"- Source file: `{data_path.as_posix()}`",
        f"- Dataset shape: {df.shape[0]} rows x {df.shape[1]} columns",
        f"- Missing cells: {missing_cells} / {total_cells} ({(missing_cells / max(total_cells, 1)) * 100:.2f}%)",
        f"- Rows with any missing value: {missing_rows}",
        "",
        "## Columns and Data Types",
        as_markdown_code_block(dtypes_table, max_rows=40),
        "",
        "## Missing Values",
        as_markdown_code_block(missing_values[missing_values["missing_count"] > 0], max_rows=20),
        "",
        "## Duplicates",
        f"- Duplicate full rows: {duplicate_row_count}",
    ]

    if id_column is None:
        lines.append("- ID column not found (`Id`/`ID`/`id`).")
    else:
        lines.extend(
            [
                f"- ID column used: `{id_column}`",
                f"- Duplicate `{id_column}` rows: {duplicate_id_count}",
                f"- Unique duplicated `{id_column}` values: {duplicate_id_unique_count}",
            ]
        )

    lines.extend(
        [
            "",
            "## Constant and Near-Constant Columns",
            as_markdown_code_block(constant_table[constant_table["is_constant"] | constant_table["is_near_constant"]], max_rows=20),
            "",
            "## Numeric Summary and Implausible Value Checks",
            as_markdown_code_block(numeric_summary, max_rows=20),
            "",
            "Implausible value checks:",
            as_markdown_code_block(plausibility, max_rows=20),
            "",
            "## Categorical Levels and Rare Categories",
            as_markdown_code_block(categorical_summary, max_rows=30),
            "",
            "## Binary Variable Validity and Response Rates",
            as_markdown_code_block(binary_validation, max_rows=20),
            "",
            "## Date Parsing (`Dt_Customer`)",
        ]
    )

    if date_audit.min_date is None or date_audit.max_date is None:
        lines.append("- Date column missing or no parseable values.")
    else:
        lines.extend(
            [
                f"- Parse failures: {date_audit.parse_fail_count} ({date_audit.parse_fail_pct:.2f}%)",
                f"- Date range: {date_audit.min_date.date()} to {date_audit.max_date.date()}",
            ]
        )

    lines.extend(
        [
            "",
            "## Logical Consistency Checks",
            as_markdown_code_block(logical_consistency, max_rows=20),
            "",
            "## Likely Outliers Relevant to Clustering",
            as_markdown_code_block(outlier_table[["column", "outlier_count", "outlier_pct", "p95", "p99", "max"]], max_rows=20),
            "",
            "## Exploratory Check: Customers Missing Any Data",
            f"- Customers missing any variable: {missing_rows} ({(missing_rows / max(len(df), 1)) * 100:.2f}%)",
            as_markdown_code_block(missingness_behavior, max_rows=20),
            "",
            "## Issues Requiring Decisions in Stage 02",
        ]
    )

    if issues:
        lines.extend(f"- {issue}" for issue in issues)
    else:
        lines.append("- No major issues detected that require a Stage 02 decision.")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    data_path = repo_root / "data" / "raw" / "marketing_campaign.csv"
    output_tables_dir = repo_root / "outputs" / "tables"
    output_stage_dir = repo_root / "outputs" / "stage-outputs"
    output_tables_dir.mkdir(parents=True, exist_ok=True)
    output_stage_dir.mkdir(parents=True, exist_ok=True)

    df = load_marketing_data(data_path)
    id_column = get_id_column(df)

    missing_values = build_missing_values_table(df)
    numeric_summary = build_numeric_summary_table(df)
    categorical_summary = build_categorical_summary_table(df, exclude_columns=["Dt_Customer"])
    constant_table = build_constant_table(df)
    binary_validation = build_binary_validation_table(df, DEFAULT_BINARY_COLUMNS)
    date_audit = audit_dates(df, "Dt_Customer")
    logical_consistency = build_logical_consistency_table(df)
    plausibility = build_plausibility_table(df)
    missingness_behavior = build_missingness_behavior_table(df)

    duplicate_row_count = int(df.duplicated().sum())
    duplicate_id_count: int | None = None
    duplicate_id_unique_count: int | None = None
    if id_column is not None:
        duplicate_id_mask = df[id_column].duplicated(keep=False)
        duplicate_id_count = int(duplicate_id_mask.sum())
        duplicate_id_unique_count = int(df.loc[duplicate_id_mask, id_column].nunique())

    data_quality_summary = pd.DataFrame(
        [
            {"metric": "row_count", "value": int(df.shape[0])},
            {"metric": "column_count", "value": int(df.shape[1])},
            {"metric": "missing_cells_total", "value": int(df.isna().sum().sum())},
            {"metric": "rows_with_any_missing", "value": int(df.isna().any(axis=1).sum())},
            {"metric": "duplicate_rows", "value": duplicate_row_count},
            {"metric": "duplicate_id_rows", "value": duplicate_id_count if duplicate_id_count is not None else 0},
            {
                "metric": "duplicate_id_unique_values",
                "value": duplicate_id_unique_count if duplicate_id_unique_count is not None else 0,
            },
            {"metric": "constant_columns", "value": int(constant_table["is_constant"].sum())},
            {"metric": "near_constant_columns", "value": int(constant_table["is_near_constant"].sum())},
            {"metric": "binary_columns_checked", "value": int(binary_validation["present"].fillna(False).sum())},
            {"metric": "binary_invalid_value_cells", "value": int(binary_validation["invalid_value_count"].fillna(0).sum())},
            {"metric": "date_parse_failures", "value": int(date_audit.parse_fail_count)},
            {"metric": "numeric_columns_with_outliers", "value": int((numeric_summary["outlier_count"] > 0).sum())},
        ]
    )

    data_quality_summary.to_csv(output_tables_dir / "data_quality_summary.csv", index=False)
    missing_values.to_csv(output_tables_dir / "missing_values.csv", index=False)
    numeric_summary.to_csv(output_tables_dir / "numeric_summary.csv", index=False)
    categorical_summary.to_csv(output_tables_dir / "categorical_summary.csv", index=False)

    # Additional helpful tables for review.
    binary_validation.to_csv(output_tables_dir / "binary_validation.csv", index=False)
    constant_table.to_csv(output_tables_dir / "constant_columns.csv", index=False)
    logical_consistency.to_csv(output_tables_dir / "logical_consistency_checks.csv", index=False)
    plausibility.to_csv(output_tables_dir / "plausibility_checks.csv", index=False)
    missingness_behavior.to_csv(output_tables_dir / "missingness_behavior_comparison.csv", index=False)

    write_stage_markdown(
        output_path=output_stage_dir / "01-data-audit.md",
        data_path=data_path,
        df=df,
        id_column=id_column,
        missing_values=missing_values,
        numeric_summary=numeric_summary,
        categorical_summary=categorical_summary,
        constant_table=constant_table,
        binary_validation=binary_validation,
        date_audit=date_audit,
        logical_consistency=logical_consistency,
        plausibility=plausibility,
        missingness_behavior=missingness_behavior,
        duplicate_row_count=duplicate_row_count,
        duplicate_id_count=duplicate_id_count,
        duplicate_id_unique_count=duplicate_id_unique_count,
    )

    print("Stage 01 data audit completed.")
    print(f"Markdown output: {(output_stage_dir / '01-data-audit.md').as_posix()}")
    print(f"Tables output dir: {output_tables_dir.as_posix()}")


if __name__ == "__main__":
    main()

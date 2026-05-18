from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.features import (
    CAMPAIGN_COLUMNS,
    ENGINEERED_FEATURES,
    NON_CLUSTERING_COLUMNS,
    build_engineered_numeric_summary,
    build_feature_catalog,
    build_missing_values_table,
    engineer_marketing_features,
)


def as_markdown_code_block(dataframe: pd.DataFrame, max_rows: int = 20) -> str:
    if dataframe.empty:
        return "No rows."
    return "```\n" + dataframe.head(max_rows).to_string(index=False) + "\n```"


def write_stage_markdown(
    output_path: Path,
    input_path: Path,
    output_dataset_path: Path,
    input_df: pd.DataFrame,
    engineered_df: pd.DataFrame,
    summary,
    feature_catalog: pd.DataFrame,
    engineered_numeric_summary: pd.DataFrame,
    missing_values_summary: pd.DataFrame,
) -> None:
    channel_share_cols = ["Web_Purchase_Share", "Catalog_Purchase_Share", "Store_Purchase_Share"]
    channel_share_total = engineered_df[channel_share_cols].sum(axis=1)
    zero_total_purchase_mask = engineered_df["Total_Purchases"] == 0
    non_zero_total_purchase_mask = engineered_df["Total_Purchases"] > 0

    if int(non_zero_total_purchase_mask.sum()) > 0:
        mean_channel_share_sum_non_zero = float(channel_share_total.loc[non_zero_total_purchase_mask].mean())
    else:
        mean_channel_share_sum_non_zero = 0.0

    if int(zero_total_purchase_mask.sum()) > 0:
        max_channel_share_sum_zero_purchase = float(channel_share_total.loc[zero_total_purchase_mask].max())
    else:
        max_channel_share_sum_zero_purchase = 0.0

    recommended_exclusions = [col for col in NON_CLUSTERING_COLUMNS if col in engineered_df.columns]
    campaign_eval_columns = [col for col in CAMPAIGN_COLUMNS if col in engineered_df.columns]

    lines = [
        "# Stage 02 Feature Engineering",
        "",
        "## Input and Output",
        f"- Input dataset: `{input_path.as_posix()}`",
        f"- Output dataset: `{output_dataset_path.as_posix()}`",
        f"- Input shape: {input_df.shape[0]} rows x {input_df.shape[1]} columns",
        f"- Output shape: {engineered_df.shape[0]} rows x {engineered_df.shape[1]} columns",
        "",
        "## Assumptions and Handling Choices",
        f"- `Dt_Customer` reference date: {summary.reference_date.date()} (max observed date).",
        f"- Age reference year: {summary.reference_year}.",
        f"- Age plausibility check: {summary.age_plausibility_min} to {summary.age_plausibility_max} years.",
        "- Missing income handling: inherited from Stage 01 preprocessing (rows already removed in input file).",
        "- Division-by-zero handling: all ratio/share features are set to `0` when denominator is `0`.",
        "- `Response` and `AcceptedCmp1-5` are retained for evaluation but excluded from clustering inputs.",
        "",
        "## Features Created",
        as_markdown_code_block(feature_catalog, max_rows=40),
        "",
        "## Key Validation Checks",
        f"- `Dt_Customer` parse failures: {summary.dt_parse_failures}",
        f"- Rows with `Total_Purchases = 0`: {summary.zero_total_purchase_rows}",
        f"- Rows with `Total_Spend = 0`: {summary.zero_total_spend_rows}",
        f"- Rows with `NumWebVisitsMonth = 0`: {summary.zero_web_visit_rows}",
        f"- Mean channel-share sum for rows with `Total_Purchases > 0`: {mean_channel_share_sum_non_zero:.4f}",
        f"- Max channel-share sum for rows with `Total_Purchases = 0`: {max_channel_share_sum_zero_purchase:.4f}",
        f"- Recommended clustering exclusions: {', '.join(recommended_exclusions)}",
        f"- Campaign evaluation columns retained: {', '.join(campaign_eval_columns)}",
        "",
        "## Engineered Feature Descriptive Statistics",
        as_markdown_code_block(engineered_numeric_summary, max_rows=25),
        "",
        "## Missing Values After Feature Engineering",
        as_markdown_code_block(missing_values_summary[missing_values_summary['missing_count'] > 0], max_rows=25),
        "",
        "## Recommended Next Steps for EDA",
        "- Review skew/outliers in `Total_Spend`, `Average_Spend_Per_Purchase`, and spend-share features.",
        "- Evaluate correlation and redundancy among spending and purchase-ratio features.",
        "- Confirm final clustering feature set excludes identifier and outcome/evaluation variables.",
    ]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    input_path = REPO_ROOT / "data" / "processed" / "marketing_campaign_processed.csv"
    processed_dir = REPO_ROOT / "data" / "processed"
    output_path = processed_dir / "marketing_campaign_processed_features_engineered.csv"
    output_tables_dir = REPO_ROOT / "outputs" / "tables"
    output_stage_dir = REPO_ROOT / "outputs" / "stage-outputs"

    processed_dir.mkdir(parents=True, exist_ok=True)
    output_tables_dir.mkdir(parents=True, exist_ok=True)
    output_stage_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_path}. "
            "Run the Stage 01 processing step first to create marketing_campaign_processed.csv."
        )

    input_df = pd.read_csv(input_path, sep=";")
    engineered_df, summary = engineer_marketing_features(input_df)
    engineered_df.to_csv(output_path, sep=";", index=False)

    feature_catalog = build_feature_catalog(engineered_df)
    feature_summary = pd.DataFrame(
        [
            {"metric": "input_rows", "value": summary.input_rows},
            {"metric": "output_rows", "value": summary.output_rows},
            {"metric": "input_columns", "value": summary.input_columns},
            {"metric": "output_columns", "value": summary.output_columns},
            {"metric": "engineered_features_created", "value": summary.features_created},
            {"metric": "dt_customer_parse_failures", "value": summary.dt_parse_failures},
            {"metric": "reference_date", "value": summary.reference_date.date().isoformat()},
            {"metric": "reference_year", "value": summary.reference_year},
            {"metric": "age_plausibility_min", "value": summary.age_plausibility_min},
            {"metric": "age_plausibility_max", "value": summary.age_plausibility_max},
            {"metric": "zero_total_purchase_rows", "value": summary.zero_total_purchase_rows},
            {"metric": "zero_total_spend_rows", "value": summary.zero_total_spend_rows},
            {"metric": "zero_web_visit_rows", "value": summary.zero_web_visit_rows},
            {
                "metric": "recommended_non_clustering_columns_present",
                "value": ",".join([col for col in NON_CLUSTERING_COLUMNS if col in engineered_df.columns]),
            },
            {
                "metric": "engineered_feature_names",
                "value": ",".join([feature for feature in ENGINEERED_FEATURES if feature in engineered_df.columns]),
            },
        ]
    )
    engineered_numeric_summary = build_engineered_numeric_summary(engineered_df, ENGINEERED_FEATURES)
    missing_values_summary = build_missing_values_table(engineered_df)

    feature_summary.to_csv(output_tables_dir / "02_feature_summary.csv", index=False)
    engineered_numeric_summary.to_csv(output_tables_dir / "02_engineered_numeric_summary.csv", index=False)
    missing_values_summary.to_csv(output_tables_dir / "02_missing_values_after_feature_engineering.csv", index=False)

    write_stage_markdown(
        output_path=output_stage_dir / "02-feature-engineering.md",
        input_path=input_path,
        output_dataset_path=output_path,
        input_df=input_df,
        engineered_df=engineered_df,
        summary=summary,
        feature_catalog=feature_catalog,
        engineered_numeric_summary=engineered_numeric_summary,
        missing_values_summary=missing_values_summary,
    )

    print("Stage 02 feature engineering completed.")
    print(f"Input file: {input_path.as_posix()}")
    print(f"Output file: {output_path.as_posix()}")
    print(f"Rows preserved: {summary.output_rows} / {summary.input_rows}")
    print("Generated table outputs:")
    print(f"- {(output_tables_dir / '02_feature_summary.csv').as_posix()}")
    print(f"- {(output_tables_dir / '02_engineered_numeric_summary.csv').as_posix()}")
    print(f"- {(output_tables_dir / '02_missing_values_after_feature_engineering.csv').as_posix()}")
    print(f"Stage summary: {(output_stage_dir / '02-feature-engineering.md').as_posix()}")


if __name__ == "__main__":
    main()

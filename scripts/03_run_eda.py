from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.eda import (
    KEY_CORRELATION_COLUMNS,
    build_channel_summary_by_response,
    build_correlation_table,
    build_household_summary_by_response,
    build_overall_kpi_summary,
    build_response_by_band_tables,
    build_response_rate_summary,
    build_spend_summary_by_response,
    build_top_product_category_spend_summary,
    save_average_spend_by_category,
    save_channel_usage_summary,
    save_income_distribution_with_clip,
    save_recency_vs_total_spend,
    save_response_rate_by_bands,
    save_total_spend_distribution,
)


def as_markdown_code_block(dataframe: pd.DataFrame, max_rows: int = 20) -> str:
    if dataframe.empty:
        return "No rows."
    return "```\n" + dataframe.head(max_rows).to_string(index=False) + "\n```"


def write_stage_markdown(
    output_path: Path,
    input_path: Path,
    df: pd.DataFrame,
    overall_kpi_summary: pd.DataFrame,
    response_rate_summary: pd.DataFrame,
    spend_summary_by_response: pd.DataFrame,
    channel_summary_by_response: pd.DataFrame,
    household_summary_by_response: pd.DataFrame,
    top_product_category_spend_summary: pd.DataFrame,
    correlation_table: pd.DataFrame,
    response_by_income_band: pd.DataFrame,
    response_by_spend_band: pd.DataFrame,
    income_clip_value: float,
    figure_paths: list[Path],
) -> None:
    responders = spend_summary_by_response.loc[spend_summary_by_response["Response"] == 1].iloc[0]
    non_responders = spend_summary_by_response.loc[spend_summary_by_response["Response"] == 0].iloc[0]
    avg_spend_gap = float(responders["avg_total_spend"] - non_responders["avg_total_spend"])
    avg_purchase_gap = float(responders["avg_spend_per_purchase"] - non_responders["avg_spend_per_purchase"])

    income_band_top = response_by_income_band.sort_values("response_rate_pct", ascending=False).iloc[0]
    spend_band_top = response_by_spend_band.sort_values("response_rate_pct", ascending=False).iloc[0]

    corr_with_response = (
        correlation_table.set_index("variable")
        .loc[[col for col in correlation_table["variable"] if col != "Response"], "Response"]
        .sort_values(key=lambda s: s.abs(), ascending=False)
    )
    top_corr_feature = corr_with_response.index[0]
    top_corr_value = float(corr_with_response.iloc[0])

    top_category = top_product_category_spend_summary.iloc[0]

    lines = [
        "# Stage 03 EDA",
        "",
        "## Dataset and Scope",
        f"- Input file: `{input_path.as_posix()}`",
        f"- Rows: {df.shape[0]} | Columns: {df.shape[1]}",
        f"- Key correlation variables reviewed: {', '.join([c for c in KEY_CORRELATION_COLUMNS if c in df.columns])}",
        "",
        "## Overall KPI Summary",
        as_markdown_code_block(overall_kpi_summary, max_rows=20),
        "",
        "## Response and Behaviour Summaries",
        "Response rates:",
        as_markdown_code_block(response_rate_summary, max_rows=20),
        "",
        "Spend summary by response:",
        as_markdown_code_block(spend_summary_by_response, max_rows=20),
        "",
        "Channel summary by response:",
        as_markdown_code_block(channel_summary_by_response, max_rows=20),
        "",
        "Household summary by response:",
        as_markdown_code_block(household_summary_by_response, max_rows=20),
        "",
        "Top product category spend summary:",
        as_markdown_code_block(top_product_category_spend_summary, max_rows=20),
        "",
        "Correlation table (key numeric variables):",
        as_markdown_code_block(correlation_table, max_rows=20),
        "",
        "Response by income band:",
        as_markdown_code_block(response_by_income_band, max_rows=20),
        "",
        "Response by spend band:",
        as_markdown_code_block(response_by_spend_band, max_rows=20),
        "",
        "## Key Patterns for Segmentation",
        f"- Responders spend more on average (`+{avg_spend_gap:.2f}` in `Total_Spend`) and have higher spend per purchase (`+{avg_purchase_gap:.2f}`).",
        f"- Highest response by income band: `{income_band_top['Income_Band']}` at `{income_band_top['response_rate_pct']:.2f}%`.",
        f"- Highest response by spend band: `{spend_band_top['Spend_Band']}` at `{spend_band_top['response_rate_pct']:.2f}%`.",
        f"- Highest average product spend category is `{top_category['product_category']}` (`{top_category['avg_spend_overall']:.2f}`).",
        f"- Strongest linear relationship with `Response` among reviewed variables: `{top_corr_feature}` (`corr={top_corr_value:.3f}`).",
        "",
        "## Notes",
        f"- Income distribution chart is clipped at P99 (`{income_clip_value:.2f}`) for readability; raw values are unchanged.",
        "- This stage is exploratory only: no clustering or segment naming performed.",
        "",
        "## Recommended Variables/Themes for Clustering Stage",
        "- Value: `Total_Spend`, `Average_Spend_Per_Purchase`, `Income`.",
        "- Engagement: `Recency`, `Total_Purchases`, `NumWebVisitsMonth`.",
        "- Channel behaviour: channel share features and `Deal_Purchase_Share`.",
        "- Product preference: product spend shares.",
        "- Household context: `Has_Children` / `Household_Children`.",
        "",
        "## Generated Figures",
    ]
    lines.extend([f"- `{figure_path.as_posix()}`" for figure_path in figure_paths])
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    input_path = REPO_ROOT / "data" / "processed" / "marketing_campaign_processed_features_engineered.csv"
    output_tables_dir = REPO_ROOT / "outputs" / "tables"
    output_stage_dir = REPO_ROOT / "outputs" / "stage-outputs"
    figures_dir = REPO_ROOT / "reports" / "figures"

    output_tables_dir.mkdir(parents=True, exist_ok=True)
    output_stage_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_path}. Run Stage 02 feature engineering first."
        )

    df = pd.read_csv(input_path, sep=";")

    overall_kpi_summary = build_overall_kpi_summary(df)
    response_rate_summary = build_response_rate_summary(df)
    spend_summary_by_response = build_spend_summary_by_response(df)
    channel_summary_by_response = build_channel_summary_by_response(df)
    household_summary_by_response = build_household_summary_by_response(df)
    top_product_category_spend_summary = build_top_product_category_spend_summary(df)
    correlation_table = build_correlation_table(df)
    response_by_income_band, response_by_spend_band = build_response_by_band_tables(df)

    overall_kpi_summary.to_csv(output_tables_dir / "03_overall_kpi_summary.csv", index=False)
    response_rate_summary.to_csv(output_tables_dir / "03_response_rate_summary.csv", index=False)
    spend_summary_by_response.to_csv(output_tables_dir / "03_spend_summary_by_response.csv", index=False)
    channel_summary_by_response.to_csv(output_tables_dir / "03_channel_summary_by_response.csv", index=False)
    household_summary_by_response.to_csv(output_tables_dir / "03_household_summary_by_response.csv", index=False)
    top_product_category_spend_summary.to_csv(
        output_tables_dir / "03_top_product_category_spend_summary.csv",
        index=False,
    )
    correlation_table.to_csv(output_tables_dir / "03_correlation_key_numeric.csv", index=False)
    response_by_income_band.to_csv(output_tables_dir / "03_response_by_income_band.csv", index=False)
    response_by_spend_band.to_csv(output_tables_dir / "03_response_by_spend_band.csv", index=False)

    figure_total_spend = figures_dir / "03_total_spend_distribution.png"
    figure_income_distribution = figures_dir / "03_income_distribution_clipped_p99.png"
    figure_response_by_bands = figures_dir / "03_response_rate_by_income_and_spend_bands.png"
    figure_avg_spend_by_category = figures_dir / "03_average_spend_by_product_category.png"
    figure_channel_usage = figures_dir / "03_channel_usage_summary.png"
    figure_recency_vs_spend = figures_dir / "03_recency_vs_total_spend_by_response.png"

    save_total_spend_distribution(df, figure_total_spend)
    income_clip_value = save_income_distribution_with_clip(df, figure_income_distribution, clip_quantile=0.99)
    save_response_rate_by_bands(response_by_income_band, response_by_spend_band, figure_response_by_bands)
    save_average_spend_by_category(df, figure_avg_spend_by_category)
    save_channel_usage_summary(df, figure_channel_usage)
    save_recency_vs_total_spend(df, figure_recency_vs_spend)

    figure_paths = [
        figure_total_spend,
        figure_income_distribution,
        figure_response_by_bands,
        figure_avg_spend_by_category,
        figure_channel_usage,
        figure_recency_vs_spend,
    ]

    write_stage_markdown(
        output_path=output_stage_dir / "03-eda.md",
        input_path=input_path,
        df=df,
        overall_kpi_summary=overall_kpi_summary,
        response_rate_summary=response_rate_summary,
        spend_summary_by_response=spend_summary_by_response,
        channel_summary_by_response=channel_summary_by_response,
        household_summary_by_response=household_summary_by_response,
        top_product_category_spend_summary=top_product_category_spend_summary,
        correlation_table=correlation_table,
        response_by_income_band=response_by_income_band,
        response_by_spend_band=response_by_spend_band,
        income_clip_value=income_clip_value,
        figure_paths=figure_paths,
    )

    print("Stage 03 EDA completed.")
    print(f"Input file: {input_path.as_posix()}")
    print("Saved EDA tables:")
    print(f"- {(output_tables_dir / '03_overall_kpi_summary.csv').as_posix()}")
    print(f"- {(output_tables_dir / '03_response_rate_summary.csv').as_posix()}")
    print(f"- {(output_tables_dir / '03_spend_summary_by_response.csv').as_posix()}")
    print(f"- {(output_tables_dir / '03_channel_summary_by_response.csv').as_posix()}")
    print(f"- {(output_tables_dir / '03_household_summary_by_response.csv').as_posix()}")
    print(f"- {(output_tables_dir / '03_top_product_category_spend_summary.csv').as_posix()}")
    print(f"- {(output_tables_dir / '03_correlation_key_numeric.csv').as_posix()}")
    print(f"- {(output_tables_dir / '03_response_by_income_band.csv').as_posix()}")
    print(f"- {(output_tables_dir / '03_response_by_spend_band.csv').as_posix()}")
    print("Saved figures:")
    for path in figure_paths:
        print(f"- {path.as_posix()}")
    print(f"Stage summary: {(output_stage_dir / '03-eda.md').as_posix()}")


if __name__ == "__main__":
    main()

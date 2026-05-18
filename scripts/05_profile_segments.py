from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.profiling import (
    SEGMENT_COL,
    SEGMENT_ASSIGNMENT_COL,
    build_segment_channel_summary,
    build_segment_name_recommendations,
    build_segment_product_summary,
    build_segment_profile_indexed,
    build_segment_profile_summary,
    build_segment_response_summary,
    join_segment_assignments,
    save_avg_total_spend_plot,
    save_channel_share_plot,
    save_children_rate_plot,
    save_income_spend_comparison_plot,
    save_product_spend_share_plot,
    save_response_rate_plot,
    save_segment_size_share_plot,
)


def as_markdown_code_block(dataframe: pd.DataFrame, max_rows: int = 20) -> str:
    if dataframe.empty:
        return "No rows."
    return "```\n" + dataframe.head(max_rows).to_string(index=False) + "\n```"


def _determine_value_band(avg_spend: float, spend_values: pd.Series) -> str:
    p33 = float(spend_values.quantile(0.33))
    p66 = float(spend_values.quantile(0.66))
    if avg_spend <= p33:
        return "Low value"
    if avg_spend >= p66:
        return "High value"
    return "Mid value"


def _determine_response_band(response_rate: float, response_values: pd.Series) -> str:
    p33 = float(response_values.quantile(0.33))
    p66 = float(response_values.quantile(0.66))
    if response_rate <= p33:
        return "Lower responsiveness"
    if response_rate >= p66:
        return "Higher responsiveness"
    return "Moderate responsiveness"


def write_stage_markdown(
    output_path: Path,
    engineered_input_path: Path,
    assignments_input_path: Path,
    clustering_summary_path: Path,
    row_count_profiled: int,
    profile_summary: pd.DataFrame,
    profile_indexed: pd.DataFrame,
    response_summary: pd.DataFrame,
    channel_summary: pd.DataFrame,
    product_summary: pd.DataFrame,
    name_recommendations: pd.DataFrame,
    figure_paths: list[Path],
) -> None:
    segment_sizes = profile_summary[[SEGMENT_COL, "customer_count", "customer_share_pct"]].copy()
    response_range = float(profile_summary["response_rate_pct"].max() - profile_summary["response_rate_pct"].min())
    spend_range = float(profile_summary["avg_total_spend"].max() - profile_summary["avg_total_spend"].min())
    deal_share_range = float(
        profile_summary["avg_deal_purchase_share"].max() - profile_summary["avg_deal_purchase_share"].min()
    )

    lines = [
        "# Stage 05 Segment Profiling",
        "",
        "## Inputs Used",
        f"- Engineered dataset: `{engineered_input_path.as_posix()}`",
        f"- Segment assignments: `{assignments_input_path.as_posix()}`",
        f"- Stage 04 summary: `{clustering_summary_path.as_posix()}`",
        "- Segment assignment source: `kmeans` / `kmeans_k3` from Stage 04.",
        f"- Row count profiled: {row_count_profiled}",
        "",
        "## Segment Size Summary",
        as_markdown_code_block(segment_sizes, max_rows=10),
        "",
        "## Provisional Segment Names",
        as_markdown_code_block(name_recommendations, max_rows=10),
        "",
        "## Absolute Segment Profile",
        as_markdown_code_block(profile_summary, max_rows=20),
        "",
        "## Indexed Segment Profile (Overall = 100)",
        as_markdown_code_block(profile_indexed, max_rows=20),
        "",
        "## Response and Campaign Summary",
        as_markdown_code_block(response_summary, max_rows=20),
        "",
        "## Channel Mix Summary",
        as_markdown_code_block(channel_summary, max_rows=20),
        "",
        "## Product Preference Summary",
        as_markdown_code_block(product_summary, max_rows=20),
        "",
        "## Segment Narratives",
    ]

    for _, name_row in name_recommendations.sort_values("segment_id").iterrows():
        segment_id = int(name_row["segment_id"])
        summary_row = profile_summary.loc[profile_summary[SEGMENT_COL] == segment_id].iloc[0]
        product_row = product_summary.loc[product_summary[SEGMENT_COL] == segment_id].iloc[0]
        value_level = _determine_value_band(float(summary_row["avg_total_spend"]), profile_summary["avg_total_spend"])
        response_level = _determine_response_band(float(summary_row["response_rate_pct"]), profile_summary["response_rate_pct"])
        lines.extend(
            [
                f"### Segment {segment_id}: {name_row['provisional_segment_name']}",
                f"- Size/share: {int(summary_row['customer_count'])} customers ({float(summary_row['customer_share_pct']):.2f}%).",
                f"- Defining characteristics: income {float(summary_row['avg_income']):.0f}, total spend {float(summary_row['avg_total_spend']):.0f}, total purchases {float(summary_row['avg_total_purchases']):.1f}, household children {float(summary_row['avg_household_children']):.2f}.",
                f"- Value level: {value_level}.",
                f"- Responsiveness: {response_level} (response rate {float(summary_row['response_rate_pct']):.2f}%, avg campaign acceptance total {float(summary_row['avg_campaign_acceptance_total']):.2f}).",
                f"- Channel behaviour: web {float(summary_row['avg_web_purchase_share']):.2f}, catalog {float(summary_row['avg_catalog_purchase_share']):.2f}, store {float(summary_row['avg_store_purchase_share']):.2f}, deal {float(summary_row['avg_deal_purchase_share']):.2f}.",
                f"- Product preferences: top category by avg spend `{product_row['top_category_by_avg_spend']}`, top by spend share `{product_row['top_category_by_spend_share']}`.",
                f"- Caveat: {name_row['risks_or_caveats']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Key Differences Across Segments",
            f"- Response-rate spread: {response_range:.2f} percentage points.",
            f"- Average total spend spread: {spend_range:.2f}.",
            f"- Deal-share spread: {deal_share_range:.2f}.",
            "- Segments differ materially on value, household composition, channel mix, and campaign responsiveness.",
            "",
            "## Caveats",
            "- Segment labels are provisional and descriptive, not causal.",
            "- Profiles are based on one dataset snapshot and should be validated with future campaign outcomes.",
            "",
            "## Recommended Next Steps for Stage 06",
            "- Translate each segment profile into targeted campaign objectives and message strategies.",
            "- Prioritise segments by expected commercial uplift and execution feasibility.",
            "- Define segment-specific channel and offer hypotheses to test.",
            "",
            "## Generated Figures",
        ]
    )
    lines.extend([f"- `{path.as_posix()}`" for path in figure_paths])
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    engineered_input_path = REPO_ROOT / "data" / "processed" / "marketing_campaign_processed_features_engineered.csv"
    assignments_input_path = REPO_ROOT / "outputs" / "segment_assignments.csv"
    clustering_summary_path = REPO_ROOT / "outputs" / "stage-outputs" / "04-clustering.md"
    model_comparison_path = REPO_ROOT / "outputs" / "tables" / "04_model_comparison.csv"

    output_tables_dir = REPO_ROOT / "outputs" / "tables"
    output_stage_dir = REPO_ROOT / "outputs" / "stage-outputs"
    figures_dir = REPO_ROOT / "reports" / "figures"

    output_tables_dir.mkdir(parents=True, exist_ok=True)
    output_stage_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    if not engineered_input_path.exists():
        raise FileNotFoundError(f"Missing engineered dataset: {engineered_input_path}")
    if not assignments_input_path.exists():
        raise FileNotFoundError(f"Missing segment assignments file: {assignments_input_path}")
    if not clustering_summary_path.exists():
        raise FileNotFoundError(f"Missing Stage 04 summary: {clustering_summary_path}")
    if not model_comparison_path.exists():
        raise FileNotFoundError(f"Missing Stage 04 model comparison table: {model_comparison_path}")

    model_comparison = pd.read_csv(model_comparison_path)
    recommended_flag = (
        model_comparison["recommended_solution"]
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(["true", "1", "yes"])
    )
    recommended_rows = model_comparison[recommended_flag]
    if recommended_rows.empty:
        raise ValueError("No recommended solution found in 04_model_comparison.csv")
    recommended = recommended_rows.iloc[0]
    recommended_method = str(recommended["method"])
    recommended_solution = str(recommended["solution"])
    if recommended_method != "kmeans" or recommended_solution != SEGMENT_ASSIGNMENT_COL:
        raise ValueError(
            f"Stage 05 expects recommended solution kmeans/{SEGMENT_ASSIGNMENT_COL}, "
            f"but found {recommended_method}/{recommended_solution}."
        )

    engineered_df = pd.read_csv(engineered_input_path, sep=";")
    assignments_df = pd.read_csv(assignments_input_path)
    profiled_df = join_segment_assignments(engineered_df, assignments_df, assignment_column=SEGMENT_ASSIGNMENT_COL)

    profile_summary = build_segment_profile_summary(profiled_df)
    profile_indexed = build_segment_profile_indexed(profiled_df, profile_summary)
    response_summary = build_segment_response_summary(profiled_df)
    channel_summary = build_segment_channel_summary(profiled_df)
    product_summary = build_segment_product_summary(profiled_df)
    name_recommendations = build_segment_name_recommendations(profile_summary)

    profile_summary.to_csv(output_tables_dir / "05_segment_profile_summary.csv", index=False)
    profile_indexed.to_csv(output_tables_dir / "05_segment_profile_indexed.csv", index=False)
    response_summary.to_csv(output_tables_dir / "05_segment_response_summary.csv", index=False)
    channel_summary.to_csv(output_tables_dir / "05_segment_channel_summary.csv", index=False)
    product_summary.to_csv(output_tables_dir / "05_segment_product_summary.csv", index=False)
    name_recommendations.to_csv(output_tables_dir / "05_segment_name_recommendations.csv", index=False)

    fig_size_share = figures_dir / "05_segment_size_share.png"
    fig_avg_spend = figures_dir / "05_avg_total_spend_by_segment.png"
    fig_response_rate = figures_dir / "05_response_rate_by_segment.png"
    fig_income_spend = figures_dir / "05_income_vs_spend_by_segment.png"
    fig_channel = figures_dir / "05_channel_share_by_segment.png"
    fig_product_share = figures_dir / "05_product_spend_share_by_segment.png"
    fig_children = figures_dir / "05_children_rate_by_segment.png"

    save_segment_size_share_plot(profile_summary, fig_size_share)
    save_avg_total_spend_plot(profile_summary, fig_avg_spend)
    save_response_rate_plot(profile_summary, fig_response_rate)
    save_income_spend_comparison_plot(profile_summary, fig_income_spend)
    save_channel_share_plot(channel_summary, fig_channel)
    save_product_spend_share_plot(product_summary, fig_product_share)
    save_children_rate_plot(profile_summary, fig_children)

    figure_paths = [
        fig_size_share,
        fig_avg_spend,
        fig_response_rate,
        fig_income_spend,
        fig_channel,
        fig_product_share,
        fig_children,
    ]

    write_stage_markdown(
        output_path=output_stage_dir / "05-segment-profiling.md",
        engineered_input_path=engineered_input_path,
        assignments_input_path=assignments_input_path,
        clustering_summary_path=clustering_summary_path,
        row_count_profiled=len(profiled_df),
        profile_summary=profile_summary,
        profile_indexed=profile_indexed,
        response_summary=response_summary,
        channel_summary=channel_summary,
        product_summary=product_summary,
        name_recommendations=name_recommendations,
        figure_paths=figure_paths,
    )

    print("Stage 05 segment profiling completed.")
    print(f"Input engineered dataset: {engineered_input_path.as_posix()}")
    print(f"Input assignments dataset: {assignments_input_path.as_posix()}")
    print(f"Rows profiled: {len(profiled_df)}")
    print(f"Confirmed clustering assignment used: {SEGMENT_ASSIGNMENT_COL}")
    print("Saved tables:")
    print(f"- {(output_tables_dir / '05_segment_profile_summary.csv').as_posix()}")
    print(f"- {(output_tables_dir / '05_segment_profile_indexed.csv').as_posix()}")
    print(f"- {(output_tables_dir / '05_segment_response_summary.csv').as_posix()}")
    print(f"- {(output_tables_dir / '05_segment_channel_summary.csv').as_posix()}")
    print(f"- {(output_tables_dir / '05_segment_product_summary.csv').as_posix()}")
    print(f"- {(output_tables_dir / '05_segment_name_recommendations.csv').as_posix()}")
    print("Saved figures:")
    for path in figure_paths:
        print(f"- {path.as_posix()}")
    print(f"Stage summary: {(output_stage_dir / '05-segment-profiling.md').as_posix()}")


if __name__ == "__main__":
    main()

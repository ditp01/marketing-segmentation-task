from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd

SEGMENT_COL = "segment_id"

SEGMENT_NAME_MAP = {
    0: "High-Value Premium Buyers",
    1: "Value-Conscious Family Shoppers",
    2: "Low-Value Deal Seekers",
}

RECOMMENDATION_COLUMNS = [
    "segment_name",
    "short_segment_description",
    "marketing_objective",
    "messaging_strategy",
    "offer_strategy",
    "channel_strategy",
    "product_focus",
    "suggested_kpis",
]

KPI_GUIDANCE_COLUMNS = [
    "segment_name",
    "kpi_name",
    "baseline_value",
    "target_guidance",
    "data_status",
    "notes",
]


def _validate_columns(df: pd.DataFrame, required_columns: list[str], name: str) -> None:
    missing = [column for column in required_columns if column not in df.columns]
    if missing:
        raise KeyError(f"{name} missing required columns: {missing}")


def _fmt_pct(value: float, decimals: int = 1) -> str:
    return f"{value:.{decimals}f}%"


def _fmt_num(value: float, decimals: int = 1) -> str:
    return f"{value:.{decimals}f}"


def as_markdown_code_block(dataframe: pd.DataFrame, max_rows: int = 80) -> str:
    if dataframe.empty:
        return "No rows."
    return "```\n" + dataframe.head(max_rows).to_string(index=False) + "\n```"


def _safe_markdown_cell(value: object) -> str:
    text = str(value)
    text = text.replace("|", "/")
    text = text.replace("\n", " ")
    return text.strip()


def dataframe_to_markdown_table(dataframe: pd.DataFrame) -> str:
    if dataframe.empty:
        return "_No rows._"
    header = "| " + " | ".join([_safe_markdown_cell(column) for column in dataframe.columns]) + " |"
    separator = "| " + " | ".join(["---"] * len(dataframe.columns)) + " |"
    rows = []
    for _, row in dataframe.iterrows():
        rows.append("| " + " | ".join([_safe_markdown_cell(value) for value in row.tolist()]) + " |")
    return "\n".join([header, separator, *rows])


def load_stage05_segment_inputs(
    profile_summary_path: Path,
    response_summary_path: Path,
    channel_summary_path: Path,
    product_summary_path: Path,
) -> pd.DataFrame:
    profile_df = pd.read_csv(profile_summary_path)
    response_df = pd.read_csv(response_summary_path)
    channel_df = pd.read_csv(channel_summary_path)
    product_df = pd.read_csv(product_summary_path)

    _validate_columns(
        profile_df,
        [
            SEGMENT_COL,
            "customer_count",
            "customer_share_pct",
            "avg_income",
            "avg_total_spend",
            "avg_total_purchases",
            "avg_spend_per_purchase",
            "avg_recency",
        ],
        "05_segment_profile_summary.csv",
    )
    _validate_columns(
        response_df,
        [SEGMENT_COL, "response_rate_pct", "avg_campaign_acceptance_total", "complaint_rate_pct"],
        "05_segment_response_summary.csv",
    )
    _validate_columns(
        channel_df,
        [
            SEGMENT_COL,
            "avg_web_purchase_share",
            "avg_catalog_purchase_share",
            "avg_store_purchase_share",
            "avg_deal_purchase_share",
        ],
        "05_segment_channel_summary.csv",
    )
    _validate_columns(
        product_df,
        [
            SEGMENT_COL,
            "avg_mnt_wines",
            "avg_mnt_meat_products",
            "avg_mnt_gold_prods",
            "top_category_by_avg_spend",
        ],
        "05_segment_product_summary.csv",
    )

    profile_trim = profile_df[
        [
            SEGMENT_COL,
            "customer_count",
            "customer_share_pct",
            "avg_income",
            "avg_total_spend",
            "avg_total_purchases",
            "avg_spend_per_purchase",
            "avg_recency",
        ]
    ].copy()
    response_trim = response_df[
        [SEGMENT_COL, "response_rate_pct", "avg_campaign_acceptance_total", "complaint_rate_pct"]
    ].copy()
    channel_trim = channel_df[
        [
            SEGMENT_COL,
            "avg_web_purchase_share",
            "avg_catalog_purchase_share",
            "avg_store_purchase_share",
            "avg_deal_purchase_share",
        ]
    ].copy()
    product_trim = product_df[
        [
            SEGMENT_COL,
            "avg_mnt_wines",
            "avg_mnt_meat_products",
            "avg_mnt_gold_prods",
            "top_category_by_avg_spend",
            "top_category_by_spend_share",
        ]
    ].copy()

    segment_df = (
        profile_trim.merge(response_trim, on=SEGMENT_COL, how="inner")
        .merge(channel_trim, on=SEGMENT_COL, how="inner")
        .merge(product_trim, on=SEGMENT_COL, how="inner")
        .sort_values(SEGMENT_COL)
        .reset_index(drop=True)
    )
    segment_df["segment_name"] = segment_df[SEGMENT_COL].map(SEGMENT_NAME_MAP)

    if segment_df["segment_name"].isna().any():
        unknown = segment_df.loc[segment_df["segment_name"].isna(), SEGMENT_COL].tolist()
        raise ValueError(f"Found unexpected segment IDs that are not mapped in stage 06: {unknown}")
    return segment_df


def build_recommendation_matrix(segment_df: pd.DataFrame) -> pd.DataFrame:
    recommendations_by_segment: dict[int, dict[str, str]] = {
        0: {
            "short_segment_description": "Highest-value segment with strong spend, high response, and low reliance on deals.",
            "marketing_objective": "Protect and grow high-margin revenue from premium loyalists.",
            "messaging_strategy": "Use premium, quality-led messaging centered on provenance, exclusivity, and early access.",
            "offer_strategy": "Prioritise personalised premium bundles and loyalty perks; avoid broad discounting.",
            "channel_strategy": "Lead with catalog/direct and store support, backed by targeted email and web retargeting.",
            "product_focus": "Wine, meat, premium bundles, and exclusive ranges.",
            "response_target": "24.0%",
            "avg_spend_target": "1250.0",
            "deal_share_target": "<= 10.0%",
        },
        1: {
            "short_segment_description": "Mid-value family segment with solid spend and moderate response, but higher deal sensitivity.",
            "marketing_objective": "Grow basket value and frequency without over-subsidising existing purchases.",
            "messaging_strategy": "Use practical value messaging: family bundles, convenience, multi-buy, and seasonal household needs.",
            "offer_strategy": "Use targeted discounts and bundle offers to drive basket growth, not blanket price cuts.",
            "channel_strategy": "Prioritise web and store journeys, with selective promotional support.",
            "product_focus": "Wine-led baskets, family bundles, and household meal solutions.",
            "response_target": "13.0%",
            "avg_spend_target": "545.0",
            "deal_share_target": "28.0%-33.0%",
        },
        2: {
            "short_segment_description": "Low-value, price-sensitive segment with low response and high deal dependence.",
            "marketing_objective": "Defend profitability while selectively reactivating commercially viable customers.",
            "messaging_strategy": "Use simple, deal-led reactivation messaging with clear everyday value.",
            "offer_strategy": "Limit activity to low-cost automated campaigns and entry-level promotions where incremental gain is plausible.",
            "channel_strategy": "Focus on store-led promotions and low-cost digital reactivation.",
            "product_focus": "Entry-level bundles, meat/value essentials, and promotional packs.",
            "response_target": "10.5%",
            "avg_spend_target": "90.0",
            "deal_share_target": "34.0%-40.0%",
        },
    }

    rows: list[dict[str, str]] = []
    for _, segment in segment_df.sort_values(SEGMENT_COL).iterrows():
        segment_id = int(segment[SEGMENT_COL])
        strategy = recommendations_by_segment[segment_id]
        kpi_line = (
            f"Response >= {strategy['response_target']}, "
            f"Avg spend >= {strategy['avg_spend_target']}, "
            f"Deal share target {strategy['deal_share_target']} "
            f"(baseline {_fmt_pct(float(segment['avg_deal_purchase_share']) * 100, 1)})."
        )

        rows.append(
            {
                "segment_name": f"Segment {segment_id}: {segment['segment_name']}",
                "short_segment_description": strategy["short_segment_description"],
                "marketing_objective": strategy["marketing_objective"],
                "messaging_strategy": strategy["messaging_strategy"],
                "offer_strategy": strategy["offer_strategy"],
                "channel_strategy": strategy["channel_strategy"],
                "product_focus": strategy["product_focus"],
                "suggested_kpis": kpi_line,
            }
        )
    return pd.DataFrame(rows, columns=RECOMMENDATION_COLUMNS)


def _build_kpi_rows_for_segment(segment: pd.Series) -> list[dict[str, str]]:
    segment_id = int(segment[SEGMENT_COL])
    segment_name = f"Segment {segment_id}: {segment['segment_name']}"
    baseline_response_rate = float(segment["response_rate_pct"])
    baseline_total_spend = float(segment["avg_total_spend"])
    baseline_spend_per_purchase = float(segment["avg_spend_per_purchase"])
    baseline_purchase_count = float(segment["avg_total_purchases"])
    baseline_deal_share = float(segment["avg_deal_purchase_share"]) * 100
    baseline_campaign_acceptance = float(segment["avg_campaign_acceptance_total"])
    baseline_complaint_rate = float(segment["complaint_rate_pct"])
    baseline_recency = float(segment["avg_recency"])

    if segment_id == 0:
        targets = {
            "response_rate": ">= 24.0%",
            "avg_total_spend": ">= 1250.0",
            "avg_spend_per_purchase": ">= 67.0",
            "purchase_count": ">= 19.5",
            "channel_mix": "Catalog + Store >= 72%; Web 24-30%",
            "product_spend": "Wine >= 550.0 and Meat >= 410.0",
            "deal_share": "<= 10.0%",
            "campaign_acceptance": ">= 0.60",
            "complaint_rate": "<= 1.0%",
            "recency": "<= 50.0 days",
            "incremental_spend": ">= +5% incremental spend vs holdout with no deal-share increase above 1pp",
            "margin_per_discounted_order": "Maintain positive net margin per discounted order",
        }
    elif segment_id == 1:
        targets = {
            "response_rate": ">= 13.0%",
            "avg_total_spend": ">= 545.0",
            "avg_spend_per_purchase": ">= 35.0",
            "purchase_count": ">= 13.5",
            "channel_mix": "Web + Store >= 84%; Catalog 10-16%",
            "product_spend": "Wine >= 340.0 and Meat >= 90.0",
            "deal_share": "28.0%-33.0%",
            "campaign_acceptance": ">= 0.30",
            "complaint_rate": "<= 1.0%",
            "recency": "<= 45.0 days",
            "incremental_spend": ">= +8% incremental basket value vs holdout in promoted cohorts",
            "margin_per_discounted_order": "Promotions must deliver non-negative gross margin uplift",
        }
    else:
        targets = {
            "response_rate": ">= 10.5%",
            "avg_total_spend": ">= 90.0",
            "avg_spend_per_purchase": ">= 13.5",
            "purchase_count": ">= 5.8",
            "channel_mix": "Store >= 58%; Catalog <= 10%; Web 28-35%",
            "product_spend": "Meat >= 22.0 and Wine >= 20.0",
            "deal_share": "34.0%-40.0%",
            "campaign_acceptance": ">= 0.09",
            "complaint_rate": "<= 1.5%",
            "recency": "<= 48.0 days",
            "incremental_spend": ">= +10% incremental spend in contacted reactivation cohort",
            "margin_per_discounted_order": "Discount activity should be retained only if net margin is positive",
        }

    channel_baseline = (
        f"Web {_fmt_pct(float(segment['avg_web_purchase_share']) * 100, 1)} | "
        f"Catalog {_fmt_pct(float(segment['avg_catalog_purchase_share']) * 100, 1)} | "
        f"Store {_fmt_pct(float(segment['avg_store_purchase_share']) * 100, 1)}"
    )
    product_baseline = (
        f"Wine {_fmt_num(float(segment['avg_mnt_wines']), 1)} | "
        f"Meat {_fmt_num(float(segment['avg_mnt_meat_products']), 1)} | "
        f"Gold {_fmt_num(float(segment['avg_mnt_gold_prods']), 1)}"
    )

    rows = [
        {
            "segment_name": segment_name,
            "kpi_name": "response_rate",
            "baseline_value": _fmt_pct(baseline_response_rate, 1),
            "target_guidance": targets["response_rate"],
            "data_status": "available_in_dataset",
            "notes": "Directly observed from stage-05 response summary.",
        },
        {
            "segment_name": segment_name,
            "kpi_name": "average_total_spend",
            "baseline_value": _fmt_num(baseline_total_spend, 1),
            "target_guidance": targets["avg_total_spend"],
            "data_status": "available_in_dataset",
            "notes": "Use as core commercial value KPI.",
        },
        {
            "segment_name": segment_name,
            "kpi_name": "average_spend_per_purchase",
            "baseline_value": _fmt_num(baseline_spend_per_purchase, 1),
            "target_guidance": targets["avg_spend_per_purchase"],
            "data_status": "available_in_dataset",
            "notes": "Useful for testing premium or bundle positioning impact.",
        },
        {
            "segment_name": segment_name,
            "kpi_name": "purchase_count",
            "baseline_value": _fmt_num(baseline_purchase_count, 1),
            "target_guidance": targets["purchase_count"],
            "data_status": "available_in_dataset",
            "notes": "Proxy for frequency and repeat engagement.",
        },
        {
            "segment_name": segment_name,
            "kpi_name": "channel_mix",
            "baseline_value": channel_baseline,
            "target_guidance": targets["channel_mix"],
            "data_status": "available_in_dataset",
            "notes": "Channel shares indicate preferred route to market by segment.",
        },
        {
            "segment_name": segment_name,
            "kpi_name": "product_category_spend",
            "baseline_value": product_baseline,
            "target_guidance": targets["product_spend"],
            "data_status": "available_in_dataset",
            "notes": "Category mix helps align assortment and messaging strategy.",
        },
        {
            "segment_name": segment_name,
            "kpi_name": "deal_purchase_share",
            "baseline_value": _fmt_pct(baseline_deal_share, 1),
            "target_guidance": targets["deal_share"],
            "data_status": "available_in_dataset",
            "notes": "Tracks discount dependency and margin risk.",
        },
        {
            "segment_name": segment_name,
            "kpi_name": "campaign_acceptance_rate",
            "baseline_value": _fmt_num(baseline_campaign_acceptance, 2),
            "target_guidance": targets["campaign_acceptance"],
            "data_status": "available_in_dataset",
            "notes": "Average accepted campaigns per customer from historical data.",
        },
        {
            "segment_name": segment_name,
            "kpi_name": "complaint_rate",
            "baseline_value": _fmt_pct(baseline_complaint_rate, 2),
            "target_guidance": targets["complaint_rate"],
            "data_status": "available_in_dataset",
            "notes": "Safeguard to prevent value strategy from harming customer experience.",
        },
        {
            "segment_name": segment_name,
            "kpi_name": "recency",
            "baseline_value": f"{_fmt_num(baseline_recency, 1)} days",
            "target_guidance": targets["recency"],
            "data_status": "available_in_dataset",
            "notes": "Lower recency indicates more recent purchasing activity.",
        },
        {
            "segment_name": segment_name,
            "kpi_name": "incremental_spend_uplift_vs_holdout",
            "baseline_value": "Not available in historical snapshot",
            "target_guidance": targets["incremental_spend"],
            "data_status": "provisional_requires_more_data",
            "notes": "Requires controlled holdout test to isolate causal uplift.",
        },
        {
            "segment_name": segment_name,
            "kpi_name": "net_margin_per_discounted_order",
            "baseline_value": "Not available (cost/margin inputs absent)",
            "target_guidance": targets["margin_per_discounted_order"],
            "data_status": "provisional_requires_more_data",
            "notes": "Requires COGS, discount depth, and contribution margin data.",
        },
    ]
    return rows


def build_kpi_guidance(segment_df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, str]] = []
    for _, segment in segment_df.sort_values(SEGMENT_COL).iterrows():
        rows.extend(_build_kpi_rows_for_segment(segment))
    return pd.DataFrame(rows, columns=KPI_GUIDANCE_COLUMNS)


def build_segment_evidence_summary(segment_df: pd.DataFrame) -> pd.DataFrame:
    summary = segment_df[
        [
            SEGMENT_COL,
            "segment_name",
            "customer_count",
            "customer_share_pct",
            "avg_total_spend",
            "avg_total_purchases",
            "response_rate_pct",
            "avg_deal_purchase_share",
        ]
    ].copy()
    summary["customer_share_pct"] = summary["customer_share_pct"].map(lambda v: _fmt_pct(float(v), 2))
    summary["avg_total_spend"] = summary["avg_total_spend"].map(lambda v: _fmt_num(float(v), 1))
    summary["avg_total_purchases"] = summary["avg_total_purchases"].map(lambda v: _fmt_num(float(v), 1))
    summary["response_rate_pct"] = summary["response_rate_pct"].map(lambda v: _fmt_pct(float(v), 2))
    summary["avg_deal_purchase_share"] = summary["avg_deal_purchase_share"].map(lambda v: _fmt_pct(float(v) * 100, 2))
    summary = summary.rename(
        columns={
            SEGMENT_COL: "segment_id",
            "segment_name": "segment_name",
            "customer_count": "customer_count",
            "customer_share_pct": "customer_share_pct",
            "avg_total_spend": "avg_total_spend",
            "avg_total_purchases": "avg_total_purchases",
            "response_rate_pct": "response_rate_pct",
            "avg_deal_purchase_share": "deal_purchase_share_pct",
        }
    )
    return summary


def write_stage06_summary_markdown(
    output_path: Path,
    input_paths: list[Path],
    segment_evidence: pd.DataFrame,
    recommendation_matrix: pd.DataFrame,
    kpi_guidance: pd.DataFrame,
) -> None:
    spend_values = segment_evidence["avg_total_spend"].astype(float)
    response_values = segment_evidence["response_rate_pct"].str.rstrip("%").astype(float)
    deal_values = segment_evidence["deal_purchase_share_pct"].str.rstrip("%").astype(float)

    spend_multiple = float(spend_values.max() / spend_values.min())
    response_gap = float(response_values.max() - response_values.min())
    deal_gap = float(deal_values.max() - deal_values.min())

    kpi_status_summary = (
        kpi_guidance.groupby("data_status")
        .size()
        .reset_index(name="kpi_count")
        .sort_values("data_status")
        .reset_index(drop=True)
    )

    lines = [
        "# Stage 06 Recommendations",
        "",
        "## Inputs Used",
    ]
    lines.extend([f"- `{path.as_posix()}`" for path in input_paths])
    lines.extend(
        [
            "",
            "## Overall Recommendation",
            "- Use the three identified K-means groups as operational marketing segments.",
            "- Apply fixed segment names: Segment 0 = High-Value Premium Buyers, Segment 1 = Value-Conscious Family Shoppers, Segment 2 = Low-Value Deal Seekers.",
            "- Prioritise Segment 0 for high-margin growth, Segment 1 for basket-size expansion, and Segment 2 for selective low-cost reactivation.",
            "",
            "## Why These Three Segments Should Be Used",
            f"- Average total spend differs by {spend_multiple:.1f}x between highest- and lowest-value segments.",
            f"- Response rate spread is {response_gap:.2f} percentage points across segments.",
            f"- Deal purchase share spread is {deal_gap:.2f} percentage points, indicating materially different price sensitivity.",
            "- Profiles also differ on channel usage and product category mix, supporting differentiated campaign treatment.",
            "",
            "Evidence snapshot:",
            as_markdown_code_block(segment_evidence, max_rows=10),
            "",
            "## Recommendation Matrix",
            as_markdown_code_block(recommendation_matrix, max_rows=10),
            "",
            "## KPI Guidance",
            as_markdown_code_block(kpi_guidance, max_rows=80),
            "",
            "KPI data availability split:",
            as_markdown_code_block(kpi_status_summary, max_rows=10),
            "",
            "## Limitations",
            "- Segment profiles are descriptive and based on one historical data snapshot; they are not causal proof.",
            "- Incrementality and profitability KPIs are provisional until holdout testing and margin data are available.",
            "- Recommended targets should be tuned after first campaign test cycles by segment.",
        ]
    )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_final_report_markdown(
    output_path: Path,
    segment_evidence: pd.DataFrame,
    recommendation_matrix: pd.DataFrame,
    kpi_guidance: pd.DataFrame,
) -> None:
    priority_kpis = kpi_guidance[
        kpi_guidance["kpi_name"].isin(
            [
                "response_rate",
                "average_total_spend",
                "deal_purchase_share",
                "campaign_acceptance_rate",
                "complaint_rate",
            ]
        )
    ].copy()

    data_status_summary = (
        kpi_guidance.groupby("data_status")
        .size()
        .reset_index(name="kpi_count")
        .sort_values("data_status")
        .reset_index(drop=True)
    )

    lines = [
        "# Marketing Segmentation Final Report",
        "",
        f"Generated on: {date.today().isoformat()}",
        "",
        "## Executive Summary",
        "- Three behaviourally distinct customer segments were identified and should be used as the go-forward campaign segmentation framework.",
        "- Segment 0 (High-Value Premium Buyers) should receive premium-led, low-discount treatment to protect margin and grow high-value revenue.",
        "- Segment 1 (Value-Conscious Family Shoppers) should receive practical value and bundle-led propositions to increase basket size and purchase frequency.",
        "- Segment 2 (Low-Value Deal Seekers) should be managed with selective low-cost reactivation and strict profitability controls.",
        "",
        "## Segment Evidence Snapshot",
        dataframe_to_markdown_table(segment_evidence),
        "",
        "## Recommendation Matrix",
        dataframe_to_markdown_table(recommendation_matrix),
        "",
        "## KPI Plan",
        "Priority KPI targets:",
        dataframe_to_markdown_table(priority_kpis),
        "",
        "KPI availability split:",
        dataframe_to_markdown_table(data_status_summary),
        "",
        "## Limitations and Controls",
        "- Profiles and KPI baselines are historical and descriptive; they should be validated through campaign experiments.",
        "- Incremental uplift and net margin KPIs are provisional until holdout-test outcomes and cost/margin data are integrated.",
        "- To avoid over-discounting, deal-led tactics should be monitored with margin guardrails by segment.",
        "",
        "## Recommended Next Actions",
        "1. Launch segmented campaign pilots for each segment with explicit holdout groups.",
        "2. Track KPI movement weekly against the segment-specific targets in `outputs/tables/06_kpi_guidance.csv`.",
        "3. Recalibrate targets after the first campaign cycle using observed incremental and margin outcomes.",
    ]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

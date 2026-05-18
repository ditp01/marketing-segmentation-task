from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str((Path.cwd() / ".cache" / "matplotlib").resolve()))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

SPEND_COLUMNS = [
    "MntWines",
    "MntFruits",
    "MntMeatProducts",
    "MntFishProducts",
    "MntSweetProducts",
    "MntGoldProds",
]

CHANNEL_COUNT_COLUMNS = [
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases",
]

CHANNEL_SHARE_COLUMNS = [
    "Web_Purchase_Share",
    "Catalog_Purchase_Share",
    "Store_Purchase_Share",
    "Deal_Purchase_Share",
]

KEY_CORRELATION_COLUMNS = [
    "Income",
    "Total_Spend",
    "Average_Spend_Per_Purchase",
    "Recency",
    "Total_Purchases",
    "NumWebVisitsMonth",
    "Campaign_Acceptance_Total",
    "Response",
]

CAMPAIGN_COLUMNS = ["AcceptedCmp1", "AcceptedCmp2", "AcceptedCmp3", "AcceptedCmp4", "AcceptedCmp5"]

INCOME_BAND_LABELS = ["Q1 Low Income", "Q2", "Q3", "Q4", "Q5 High Income"]
SPEND_BAND_LABELS = ["Q1 Low Spend", "Q2", "Q3", "Q4", "Q5 High Spend"]


def _safe_qcut(series: pd.Series, q: int, labels: list[str]) -> pd.Series:
    return pd.qcut(series, q=q, labels=labels, duplicates="drop")


def _to_rate_pct(series: pd.Series) -> float:
    return float(series.mean() * 100)


def build_overall_kpi_summary(df: pd.DataFrame) -> pd.DataFrame:
    overall_response = _to_rate_pct(df["Response"])
    total_spend_sum = float(df["Total_Spend"].sum())
    avg_total_spend = float(df["Total_Spend"].mean())
    median_total_spend = float(df["Total_Spend"].median())
    avg_income = float(df["Income"].mean())
    avg_total_purchases = float(df["Total_Purchases"].mean())
    avg_recency = float(df["Recency"].mean())
    avg_campaign_accept_total = float(df["Campaign_Acceptance_Total"].mean())
    has_children_rate = float(df["Has_Children"].mean() * 100)

    rows = [
        {"metric": "customer_count", "value": int(len(df))},
        {"metric": "response_rate_pct", "value": overall_response},
        {"metric": "total_spend_sum", "value": total_spend_sum},
        {"metric": "avg_total_spend", "value": avg_total_spend},
        {"metric": "median_total_spend", "value": median_total_spend},
        {"metric": "avg_income", "value": avg_income},
        {"metric": "avg_total_purchases", "value": avg_total_purchases},
        {"metric": "avg_recency_days", "value": avg_recency},
        {"metric": "avg_campaign_acceptance_total", "value": avg_campaign_accept_total},
        {"metric": "has_children_rate_pct", "value": has_children_rate},
    ]
    return pd.DataFrame(rows)


def build_response_rate_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, float | str | int]] = []
    rows.append(
        {
            "metric": "Response",
            "positive_count": int(df["Response"].sum()),
            "positive_rate_pct": _to_rate_pct(df["Response"]),
        }
    )

    for campaign_col in CAMPAIGN_COLUMNS:
        rows.append(
            {
                "metric": campaign_col,
                "positive_count": int(df[campaign_col].sum()),
                "positive_rate_pct": _to_rate_pct(df[campaign_col]),
            }
        )

    rows.append(
        {
            "metric": "Any_Previous_Campaign_Accepted",
            "positive_count": int((df["Campaign_Acceptance_Total"] > 0).sum()),
            "positive_rate_pct": float((df["Campaign_Acceptance_Total"] > 0).mean() * 100),
        }
    )
    return pd.DataFrame(rows)


def build_spend_summary_by_response(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby("Response").agg(
        customer_count=("ID", "count"),
        avg_income=("Income", "mean"),
        median_income=("Income", "median"),
        avg_total_spend=("Total_Spend", "mean"),
        median_total_spend=("Total_Spend", "median"),
        avg_spend_per_purchase=("Average_Spend_Per_Purchase", "mean"),
        median_spend_per_purchase=("Average_Spend_Per_Purchase", "median"),
    )
    grouped = grouped.reset_index()
    grouped["response_label"] = grouped["Response"].map({0: "Non-Responder", 1: "Responder"})
    return grouped[
        [
            "Response",
            "response_label",
            "customer_count",
            "avg_income",
            "median_income",
            "avg_total_spend",
            "median_total_spend",
            "avg_spend_per_purchase",
            "median_spend_per_purchase",
        ]
    ]


def build_channel_summary_by_response(df: pd.DataFrame) -> pd.DataFrame:
    group_cols = CHANNEL_COUNT_COLUMNS + CHANNEL_SHARE_COLUMNS + ["Total_Purchases", "NumWebVisitsMonth"]
    grouped = (
        df.groupby("Response")[group_cols]
        .mean()
        .reset_index()
        .rename(columns={"NumWebVisitsMonth": "avg_num_web_visits_month"})
    )
    grouped["response_label"] = grouped["Response"].map({0: "Non-Responder", 1: "Responder"})
    return grouped[
        [
            "Response",
            "response_label",
            "Total_Purchases",
            "NumWebPurchases",
            "NumCatalogPurchases",
            "NumStorePurchases",
            "Web_Purchase_Share",
            "Catalog_Purchase_Share",
            "Store_Purchase_Share",
            "Deal_Purchase_Share",
            "avg_num_web_visits_month",
        ]
    ]


def build_household_summary_by_response(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby("Response").agg(
        customer_count=("ID", "count"),
        avg_household_children=("Household_Children", "mean"),
        median_household_children=("Household_Children", "median"),
        has_children_rate_pct=("Has_Children", lambda s: float(s.mean() * 100)),
        avg_total_spend=("Total_Spend", "mean"),
        avg_response_recency=("Recency", "mean"),
    )
    grouped = grouped.reset_index()
    grouped["response_label"] = grouped["Response"].map({0: "Non-Responder", 1: "Responder"})
    return grouped[
        [
            "Response",
            "response_label",
            "customer_count",
            "avg_household_children",
            "median_household_children",
            "has_children_rate_pct",
            "avg_total_spend",
            "avg_response_recency",
        ]
    ]


def build_top_product_category_spend_summary(df: pd.DataFrame) -> pd.DataFrame:
    long_df = (
        df.melt(
            id_vars=["Response"],
            value_vars=SPEND_COLUMNS,
            var_name="product_category",
            value_name="spend",
        )
        .groupby(["product_category", "Response"])
        .agg(
            avg_spend=("spend", "mean"),
            median_spend=("spend", "median"),
            total_spend=("spend", "sum"),
        )
        .reset_index()
    )
    pivot_resp = long_df.pivot(index="product_category", columns="Response", values="avg_spend").reset_index()
    pivot_resp.columns = ["product_category", "avg_spend_non_responder", "avg_spend_responder"]

    overall = (
        df[SPEND_COLUMNS]
        .mean()
        .sort_values(ascending=False)
        .rename_axis("product_category")
        .reset_index(name="avg_spend_overall")
    )
    merged = overall.merge(pivot_resp, on="product_category", how="left")
    merged["responder_minus_non_responder"] = merged["avg_spend_responder"] - merged["avg_spend_non_responder"]
    return merged.sort_values("avg_spend_overall", ascending=False).reset_index(drop=True)


def build_correlation_table(df: pd.DataFrame) -> pd.DataFrame:
    available_columns = [col for col in KEY_CORRELATION_COLUMNS if col in df.columns]
    corr = df[available_columns].corr(numeric_only=True).reset_index().rename(columns={"index": "variable"})
    return corr


def build_response_by_band_tables(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    income_band = _safe_qcut(df["Income"], q=5, labels=INCOME_BAND_LABELS)
    spend_band = _safe_qcut(df["Total_Spend"], q=5, labels=SPEND_BAND_LABELS)

    income_table = (
        df.assign(Income_Band=income_band)
        .groupby("Income_Band", observed=False)
        .agg(
            customer_count=("ID", "count"),
            response_rate_pct=("Response", lambda s: float(s.mean() * 100)),
            avg_total_spend=("Total_Spend", "mean"),
            avg_total_purchases=("Total_Purchases", "mean"),
        )
        .reset_index()
    )

    spend_table = (
        df.assign(Spend_Band=spend_band)
        .groupby("Spend_Band", observed=False)
        .agg(
            customer_count=("ID", "count"),
            response_rate_pct=("Response", lambda s: float(s.mean() * 100)),
            avg_income=("Income", "mean"),
            avg_total_purchases=("Total_Purchases", "mean"),
        )
        .reset_index()
    )
    return income_table, spend_table


def save_total_spend_distribution(df: pd.DataFrame, output_path: Path) -> None:
    plt.figure(figsize=(10, 6))
    sns.histplot(df["Total_Spend"], bins=40, kde=True, color="#1f77b4")
    plt.title("Distribution of Total Spend")
    plt.xlabel("Total Spend")
    plt.ylabel("Customer Count")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def save_income_distribution_with_clip(df: pd.DataFrame, output_path: Path, clip_quantile: float = 0.99) -> float:
    clip_value = float(df["Income"].quantile(clip_quantile))
    clipped = df["Income"].clip(upper=clip_value)
    plt.figure(figsize=(10, 6))
    sns.histplot(clipped, bins=40, kde=True, color="#2ca02c")
    plt.title(f"Income Distribution (Clipped at P{int(clip_quantile * 100)})")
    plt.xlabel("Income (Clipped)")
    plt.ylabel("Customer Count")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    return clip_value


def save_response_rate_by_bands(
    income_table: pd.DataFrame, spend_table: pd.DataFrame, output_path: Path
) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)

    sns.barplot(data=income_table, x="Income_Band", y="response_rate_pct", ax=axes[0], color="#4c78a8")
    axes[0].set_title("Response Rate by Income Band")
    axes[0].set_xlabel("Income Band")
    axes[0].set_ylabel("Response Rate (%)")
    axes[0].tick_params(axis="x", rotation=25)

    sns.barplot(data=spend_table, x="Spend_Band", y="response_rate_pct", ax=axes[1], color="#f58518")
    axes[1].set_title("Response Rate by Total Spend Band")
    axes[1].set_xlabel("Spend Band")
    axes[1].set_ylabel("")
    axes[1].tick_params(axis="x", rotation=25)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def save_average_spend_by_category(df: pd.DataFrame, output_path: Path) -> None:
    category_avg = df[SPEND_COLUMNS].mean().sort_values(ascending=False).reset_index()
    category_avg.columns = ["product_category", "avg_spend"]

    plt.figure(figsize=(10, 6))
    sns.barplot(data=category_avg, x="avg_spend", y="product_category", color="#9467bd")
    plt.title("Average Spend by Product Category")
    plt.xlabel("Average Spend")
    plt.ylabel("Product Category")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def save_channel_usage_summary(df: pd.DataFrame, output_path: Path) -> None:
    channel_avg = (
        df[CHANNEL_COUNT_COLUMNS]
        .mean()
        .rename(
            {
                "NumWebPurchases": "Web",
                "NumCatalogPurchases": "Catalog",
                "NumStorePurchases": "Store",
            }
        )
        .reset_index()
    )
    channel_avg.columns = ["channel", "avg_purchase_count"]

    plt.figure(figsize=(8, 5))
    sns.barplot(data=channel_avg, x="channel", y="avg_purchase_count", color="#17becf")
    plt.title("Average Purchase Count by Channel")
    plt.xlabel("Channel")
    plt.ylabel("Average Purchase Count")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def save_recency_vs_total_spend(df: pd.DataFrame, output_path: Path) -> None:
    sampled = df.sample(min(1000, len(df)), random_state=42).copy()
    sampled["response_label"] = sampled["Response"].map({0: "Non-Responder", 1: "Responder"})

    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=sampled,
        x="Recency",
        y="Total_Spend",
        hue="response_label",
        alpha=0.7,
        s=40,
        palette={"Non-Responder": "#7f7f7f", "Responder": "#d62728"},
    )
    plt.title("Recency vs Total Spend (Sampled)")
    plt.xlabel("Recency (days)")
    plt.ylabel("Total Spend")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

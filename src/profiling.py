from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str((Path.cwd() / ".cache" / "matplotlib").resolve()))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

SEGMENT_COL = "segment_id"
SEGMENT_ASSIGNMENT_COL = "kmeans_k3"

SPEND_COLUMNS = [
    "MntWines",
    "MntFruits",
    "MntMeatProducts",
    "MntFishProducts",
    "MntSweetProducts",
    "MntGoldProds",
]

SPEND_SHARE_COLUMNS = [
    "Wine_Spend_Share",
    "Fruit_Spend_Share",
    "Meat_Spend_Share",
    "Fish_Spend_Share",
    "Sweet_Spend_Share",
    "Gold_Spend_Share",
]

CHANNEL_SHARE_COLUMNS = [
    "Web_Purchase_Share",
    "Catalog_Purchase_Share",
    "Store_Purchase_Share",
    "Deal_Purchase_Share",
]

CHANNEL_COUNT_COLUMNS = [
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases",
    "NumWebVisitsMonth",
]

INDEX_METRICS = [
    ("Income", "avg_income"),
    ("Total_Spend", "avg_total_spend"),
    ("Total_Purchases", "avg_total_purchases"),
    ("Average_Spend_Per_Purchase", "avg_spend_per_purchase"),
    ("Response_Rate_Pct", "response_rate_pct"),
    ("Catalog_Purchase_Share", "avg_catalog_purchase_share"),
    ("Deal_Purchase_Share", "avg_deal_purchase_share"),
    ("Household_Children", "avg_household_children"),
]


def join_segment_assignments(
    engineered_df: pd.DataFrame,
    assignments_df: pd.DataFrame,
    assignment_column: str = SEGMENT_ASSIGNMENT_COL,
) -> pd.DataFrame:
    if "ID" not in engineered_df.columns:
        raise KeyError("`ID` missing from engineered dataset.")
    if "ID" not in assignments_df.columns:
        raise KeyError("`ID` missing from assignments dataset.")
    if assignment_column not in assignments_df.columns:
        raise KeyError(f"`{assignment_column}` missing from assignments dataset.")

    merge_cols = ["ID", assignment_column]
    merged = engineered_df.merge(assignments_df[merge_cols], on="ID", how="inner", validate="one_to_one")
    merged = merged.rename(columns={assignment_column: SEGMENT_COL})
    merged[SEGMENT_COL] = merged[SEGMENT_COL].astype(int)
    return merged


def _rate_pct(series: pd.Series) -> float:
    return float(series.mean() * 100)


def build_segment_profile_summary(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby(SEGMENT_COL).agg(
        customer_count=("ID", "count"),
        avg_income=("Income", "mean"),
        median_income=("Income", "median"),
        avg_total_spend=("Total_Spend", "mean"),
        median_total_spend=("Total_Spend", "median"),
        avg_total_purchases=("Total_Purchases", "mean"),
        median_total_purchases=("Total_Purchases", "median"),
        avg_spend_per_purchase=("Average_Spend_Per_Purchase", "mean"),
        median_spend_per_purchase=("Average_Spend_Per_Purchase", "median"),
        avg_recency=("Recency", "mean"),
        avg_age=("Age", "mean"),
        avg_customer_tenure_years=("Customer_Tenure_Years", "mean"),
        avg_household_children=("Household_Children", "mean"),
        pct_with_children=("Has_Children", lambda s: float(s.mean() * 100)),
        response_rate_pct=("Response", lambda s: float(s.mean() * 100)),
        avg_campaign_acceptance_total=("Campaign_Acceptance_Total", "mean"),
        pct_any_previous_campaign_acceptance=(
            "Campaign_Acceptance_Total",
            lambda s: float((s > 0).mean() * 100),
        ),
        complaint_rate_pct=("Complain", lambda s: float(s.mean() * 100)),
        avg_web_purchase_share=("Web_Purchase_Share", "mean"),
        avg_catalog_purchase_share=("Catalog_Purchase_Share", "mean"),
        avg_store_purchase_share=("Store_Purchase_Share", "mean"),
        avg_deal_purchase_share=("Deal_Purchase_Share", "mean"),
        avg_num_web_purchases=("NumWebPurchases", "mean"),
        avg_num_catalog_purchases=("NumCatalogPurchases", "mean"),
        avg_num_store_purchases=("NumStorePurchases", "mean"),
        avg_num_web_visits_month=("NumWebVisitsMonth", "mean"),
        avg_mnt_wines=("MntWines", "mean"),
        avg_mnt_fruits=("MntFruits", "mean"),
        avg_mnt_meat_products=("MntMeatProducts", "mean"),
        avg_mnt_fish_products=("MntFishProducts", "mean"),
        avg_mnt_sweet_products=("MntSweetProducts", "mean"),
        avg_mnt_gold_prods=("MntGoldProds", "mean"),
        avg_wine_spend_share=("Wine_Spend_Share", "mean"),
        avg_meat_spend_share=("Meat_Spend_Share", "mean"),
        avg_fish_spend_share=("Fish_Spend_Share", "mean"),
        avg_fruit_spend_share=("Fruit_Spend_Share", "mean"),
        avg_sweet_spend_share=("Sweet_Spend_Share", "mean"),
        avg_gold_spend_share=("Gold_Spend_Share", "mean"),
    )
    grouped = grouped.reset_index().sort_values(SEGMENT_COL).reset_index(drop=True)

    grouped["customer_share_pct"] = (grouped["customer_count"] / grouped["customer_count"].sum()) * 100
    grouped["rank_total_spend_desc"] = grouped["avg_total_spend"].rank(method="dense", ascending=False).astype(int)
    grouped["rank_income_desc"] = grouped["avg_income"].rank(method="dense", ascending=False).astype(int)
    grouped["rank_response_rate_desc"] = grouped["response_rate_pct"].rank(method="dense", ascending=False).astype(int)
    grouped["rank_total_purchases_desc"] = grouped["avg_total_purchases"].rank(method="dense", ascending=False).astype(int)
    grouped["rank_deal_share_desc"] = grouped["avg_deal_purchase_share"].rank(method="dense", ascending=False).astype(int)
    return grouped


def build_segment_profile_indexed(df: pd.DataFrame, profile_summary: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, float | str | int]] = []
    segment_ids = profile_summary[SEGMENT_COL].tolist()

    for metric_label, profile_column in INDEX_METRICS:
        overall_value = float(df[metric_label].mean()) if metric_label in df.columns else float(profile_summary[profile_column].mean())
        row: dict[str, float | str | int] = {"metric": metric_label, "overall_value": overall_value}
        for segment_id in segment_ids:
            segment_value = float(
                profile_summary.loc[profile_summary[SEGMENT_COL] == segment_id, profile_column].iloc[0]
            )
            index_value = (segment_value / overall_value) * 100 if overall_value != 0 else float("nan")
            row[f"segment_{segment_id}_value"] = segment_value
            row[f"segment_{segment_id}_index"] = index_value
        rows.append(row)
    return pd.DataFrame(rows)


def build_segment_response_summary(df: pd.DataFrame) -> pd.DataFrame:
    response_cols = ["AcceptedCmp1", "AcceptedCmp2", "AcceptedCmp3", "AcceptedCmp4", "AcceptedCmp5"]

    grouped = df.groupby(SEGMENT_COL).agg(
        customer_count=("ID", "count"),
        customer_share_pct=("ID", lambda s: float(len(s) / len(df) * 100)),
        response_rate_pct=("Response", lambda s: float(s.mean() * 100)),
        avg_campaign_acceptance_total=("Campaign_Acceptance_Total", "mean"),
        pct_any_previous_campaign_acceptance=(
            "Campaign_Acceptance_Total",
            lambda s: float((s > 0).mean() * 100),
        ),
        complaint_rate_pct=("Complain", lambda s: float(s.mean() * 100)),
    )
    grouped = grouped.reset_index().sort_values(SEGMENT_COL).reset_index(drop=True)

    for col in response_cols:
        grouped[f"{col}_rate_pct"] = (
            df.groupby(SEGMENT_COL)[col].mean().reset_index(drop=True) * 100
        )
    return grouped


def build_segment_channel_summary(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby(SEGMENT_COL).agg(
        avg_web_purchase_share=("Web_Purchase_Share", "mean"),
        avg_catalog_purchase_share=("Catalog_Purchase_Share", "mean"),
        avg_store_purchase_share=("Store_Purchase_Share", "mean"),
        avg_deal_purchase_share=("Deal_Purchase_Share", "mean"),
        avg_num_web_purchases=("NumWebPurchases", "mean"),
        avg_num_catalog_purchases=("NumCatalogPurchases", "mean"),
        avg_num_store_purchases=("NumStorePurchases", "mean"),
        avg_num_web_visits_month=("NumWebVisitsMonth", "mean"),
    )
    grouped = grouped.reset_index().sort_values(SEGMENT_COL).reset_index(drop=True)
    return grouped


def build_segment_product_summary(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby(SEGMENT_COL).agg(
        avg_mnt_wines=("MntWines", "mean"),
        avg_mnt_fruits=("MntFruits", "mean"),
        avg_mnt_meat_products=("MntMeatProducts", "mean"),
        avg_mnt_fish_products=("MntFishProducts", "mean"),
        avg_mnt_sweet_products=("MntSweetProducts", "mean"),
        avg_mnt_gold_prods=("MntGoldProds", "mean"),
        avg_wine_spend_share=("Wine_Spend_Share", "mean"),
        avg_fruit_spend_share=("Fruit_Spend_Share", "mean"),
        avg_meat_spend_share=("Meat_Spend_Share", "mean"),
        avg_fish_spend_share=("Fish_Spend_Share", "mean"),
        avg_sweet_spend_share=("Sweet_Spend_Share", "mean"),
        avg_gold_spend_share=("Gold_Spend_Share", "mean"),
    )
    grouped = grouped.reset_index().sort_values(SEGMENT_COL).reset_index(drop=True)

    spend_cols = [
        "avg_mnt_wines",
        "avg_mnt_fruits",
        "avg_mnt_meat_products",
        "avg_mnt_fish_products",
        "avg_mnt_sweet_products",
        "avg_mnt_gold_prods",
    ]
    share_cols = [
        "avg_wine_spend_share",
        "avg_fruit_spend_share",
        "avg_meat_spend_share",
        "avg_fish_spend_share",
        "avg_sweet_spend_share",
        "avg_gold_spend_share",
    ]

    grouped["top_category_by_avg_spend"] = grouped[spend_cols].idxmax(axis=1).str.replace("avg_mnt_", "", regex=False)
    grouped["top_category_by_spend_share"] = (
        grouped[share_cols].idxmax(axis=1).str.replace("avg_", "", regex=False).str.replace("_spend_share", "", regex=False)
    )
    pretty_map = {
        "wines": "wine",
        "fruits": "fruit",
        "meat_products": "meat",
        "fish_products": "fish",
        "sweet_products": "sweet",
        "gold_prods": "gold",
    }
    grouped["top_category_by_avg_spend"] = grouped["top_category_by_avg_spend"].replace(pretty_map)
    grouped["top_category_by_spend_share"] = grouped["top_category_by_spend_share"].replace(pretty_map)
    return grouped


def build_segment_name_recommendations(profile_summary: pd.DataFrame) -> pd.DataFrame:
    # Determine role by relative ranking.
    highest_value_segment = int(profile_summary.sort_values("avg_total_spend", ascending=False).iloc[0][SEGMENT_COL])
    lowest_value_segment = int(profile_summary.sort_values("avg_total_spend", ascending=True).iloc[0][SEGMENT_COL])
    middle_segment = int(
        profile_summary.loc[
            ~profile_summary[SEGMENT_COL].isin([highest_value_segment, lowest_value_segment]),
            SEGMENT_COL,
        ].iloc[0]
    )

    name_map = {
        highest_value_segment: "Affluent Premium Responders",
        middle_segment: "Mid-Value Family Wine Buyers",
        lowest_value_segment: "Low-Value Deal-Oriented Shoppers",
    }

    rows: list[dict[str, object]] = []
    for _, row in profile_summary.sort_values(SEGMENT_COL).iterrows():
        segment = int(row[SEGMENT_COL])
        name = name_map[segment]

        value_level = "High value" if segment == highest_value_segment else ("Low value" if segment == lowest_value_segment else "Mid value")
        response_level = (
            "High responsiveness"
            if row["rank_response_rate_desc"] == 1
            else ("Low responsiveness" if row["rank_response_rate_desc"] == 3 else "Moderate responsiveness")
        )

        channel_behaviour = (
            f"Web share {row['avg_web_purchase_share']:.2f}, "
            f"catalog share {row['avg_catalog_purchase_share']:.2f}, "
            f"store share {row['avg_store_purchase_share']:.2f}, "
            f"deal share {row['avg_deal_purchase_share']:.2f}."
        )
        product_preference = (
            f"Wine share {row['avg_wine_spend_share']:.2f}, "
            f"meat share {row['avg_meat_spend_share']:.2f}, "
            f"gold share {row['avg_gold_spend_share']:.2f}."
        )

        defining_characteristics = (
            f"Income {row['avg_income']:.0f}, total spend {row['avg_total_spend']:.0f}, "
            f"purchases {row['avg_total_purchases']:.1f}, children rate {row['pct_with_children']:.1f}%."
        )

        risks = (
            "Profile is descriptive only; validate stability with future data and campaign experiments."
        )

        rows.append(
            {
                "segment_id": segment,
                "provisional_segment_name": name,
                "size_share_pct": float(row["customer_share_pct"]),
                "value_level": value_level,
                "response_rate_pct": float(row["response_rate_pct"]),
                "response_level": response_level,
                "channel_behaviour_summary": channel_behaviour,
                "product_preference_summary": product_preference,
                "defining_characteristics": defining_characteristics,
                "risks_or_caveats": risks,
            }
        )
    return pd.DataFrame(rows)


def save_segment_size_share_plot(profile_summary: pd.DataFrame, output_path: Path) -> None:
    plot_df = profile_summary[[SEGMENT_COL, "customer_share_pct"]].copy()
    plt.figure(figsize=(8, 5))
    sns.barplot(data=plot_df, x=SEGMENT_COL, y="customer_share_pct", color="#1f77b4")
    plt.title("Segment Size Share (%)")
    plt.xlabel("Segment")
    plt.ylabel("Share of Customers (%)")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def save_avg_total_spend_plot(profile_summary: pd.DataFrame, output_path: Path) -> None:
    plot_df = profile_summary[[SEGMENT_COL, "avg_total_spend"]].copy()
    plt.figure(figsize=(8, 5))
    sns.barplot(data=plot_df, x=SEGMENT_COL, y="avg_total_spend", color="#2ca02c")
    plt.title("Average Total Spend by Segment")
    plt.xlabel("Segment")
    plt.ylabel("Average Total Spend")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def save_response_rate_plot(profile_summary: pd.DataFrame, output_path: Path) -> None:
    plot_df = profile_summary[[SEGMENT_COL, "response_rate_pct"]].copy()
    plt.figure(figsize=(8, 5))
    sns.barplot(data=plot_df, x=SEGMENT_COL, y="response_rate_pct", color="#d62728")
    plt.title("Response Rate by Segment")
    plt.xlabel("Segment")
    plt.ylabel("Response Rate (%)")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def save_income_spend_comparison_plot(profile_summary: pd.DataFrame, output_path: Path) -> None:
    plot_df = profile_summary[[SEGMENT_COL, "avg_income", "avg_total_spend"]].copy()
    long_df = plot_df.melt(id_vars=[SEGMENT_COL], var_name="metric", value_name="value")
    plt.figure(figsize=(9, 5))
    sns.barplot(data=long_df, x=SEGMENT_COL, y="value", hue="metric")
    plt.title("Income vs Total Spend by Segment")
    plt.xlabel("Segment")
    plt.ylabel("Average Value")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def save_channel_share_plot(channel_summary: pd.DataFrame, output_path: Path) -> None:
    long_df = channel_summary[
        [SEGMENT_COL, "avg_web_purchase_share", "avg_catalog_purchase_share", "avg_store_purchase_share", "avg_deal_purchase_share"]
    ].melt(id_vars=[SEGMENT_COL], var_name="channel_metric", value_name="value")

    plt.figure(figsize=(10, 6))
    sns.barplot(data=long_df, x=SEGMENT_COL, y="value", hue="channel_metric")
    plt.title("Channel Mix by Segment")
    plt.xlabel("Segment")
    plt.ylabel("Average Share")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def save_product_spend_share_plot(product_summary: pd.DataFrame, output_path: Path) -> None:
    long_df = product_summary[
        [
            SEGMENT_COL,
            "avg_wine_spend_share",
            "avg_fruit_spend_share",
            "avg_meat_spend_share",
            "avg_fish_spend_share",
            "avg_sweet_spend_share",
            "avg_gold_spend_share",
        ]
    ].melt(id_vars=[SEGMENT_COL], var_name="product_share_metric", value_name="value")

    plt.figure(figsize=(11, 6))
    sns.barplot(data=long_df, x=SEGMENT_COL, y="value", hue="product_share_metric")
    plt.title("Product Spend Share by Segment")
    plt.xlabel("Segment")
    plt.ylabel("Average Spend Share")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def save_children_rate_plot(profile_summary: pd.DataFrame, output_path: Path) -> None:
    plot_df = profile_summary[[SEGMENT_COL, "pct_with_children"]].copy()
    plt.figure(figsize=(8, 5))
    sns.barplot(data=plot_df, x=SEGMENT_COL, y="pct_with_children", color="#9467bd")
    plt.title("Customers with Children by Segment")
    plt.xlabel("Segment")
    plt.ylabel("Customers with Children (%)")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

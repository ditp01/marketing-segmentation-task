from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

SPEND_COLUMNS = [
    "MntWines",
    "MntFruits",
    "MntMeatProducts",
    "MntFishProducts",
    "MntSweetProducts",
    "MntGoldProds",
]

CHANNEL_PURCHASE_COLUMNS = [
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases",
]

CAMPAIGN_COLUMNS = [
    "AcceptedCmp1",
    "AcceptedCmp2",
    "AcceptedCmp3",
    "AcceptedCmp4",
    "AcceptedCmp5",
]

ENGINEERED_FEATURES = [
    "Age",
    "Age_Plausible_Flag",
    "Customer_Tenure_Days",
    "Customer_Tenure_Years",
    "Total_Spend",
    "Total_Purchases",
    "Campaign_Acceptance_Total",
    "Household_Children",
    "Has_Children",
    "Web_Purchase_Share",
    "Catalog_Purchase_Share",
    "Store_Purchase_Share",
    "Deal_Purchase_Share",
    "Wine_Spend_Share",
    "Fruit_Spend_Share",
    "Meat_Spend_Share",
    "Fish_Spend_Share",
    "Sweet_Spend_Share",
    "Gold_Spend_Share",
    "Average_Spend_Per_Purchase",
    "Web_Purchases_Per_Web_Visit",
]

NON_CLUSTERING_COLUMNS = [
    "ID",
    "Response",
    "AcceptedCmp1",
    "AcceptedCmp2",
    "AcceptedCmp3",
    "AcceptedCmp4",
    "AcceptedCmp5",
    "Campaign_Acceptance_Total",
]


@dataclass(frozen=True)
class FeatureEngineeringSummary:
    input_rows: int
    output_rows: int
    input_columns: int
    output_columns: int
    features_created: int
    dt_parse_failures: int
    reference_date: pd.Timestamp
    reference_year: int
    age_plausibility_min: int
    age_plausibility_max: int
    zero_total_purchase_rows: int
    zero_total_spend_rows: int
    zero_web_visit_rows: int


def _safe_divide(numerator: pd.Series, denominator: pd.Series, fill_value: float = 0.0) -> pd.Series:
    """Element-wise division with explicit handling for zero/missing denominator."""
    valid_mask = denominator.notna() & (denominator != 0)
    result = pd.Series(fill_value, index=numerator.index, dtype="float64")
    result.loc[valid_mask] = numerator.loc[valid_mask] / denominator.loc[valid_mask]
    return result


def _validate_columns(df: pd.DataFrame, required: list[str]) -> None:
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise KeyError(f"Missing required columns: {missing}")


def engineer_marketing_features(df: pd.DataFrame) -> tuple[pd.DataFrame, FeatureEngineeringSummary]:
    required_columns = ["Year_Birth", "Dt_Customer", "Kidhome", "Teenhome", "NumDealsPurchases", "NumWebVisitsMonth"]
    required_columns.extend(SPEND_COLUMNS)
    required_columns.extend(CHANNEL_PURCHASE_COLUMNS)
    required_columns.extend(CAMPAIGN_COLUMNS)
    _validate_columns(df, required_columns)

    engineered = df.copy()
    input_rows = int(len(engineered))
    input_columns = int(engineered.shape[1])

    dt_customer_parsed = pd.to_datetime(engineered["Dt_Customer"], errors="coerce")
    parse_failures = int(dt_customer_parsed.isna().sum() - engineered["Dt_Customer"].isna().sum())
    if dt_customer_parsed.dropna().empty:
        raise ValueError("No parseable Dt_Customer values found.")

    reference_date = dt_customer_parsed.max()
    reference_year = int(reference_date.year)

    engineered["Age"] = reference_year - engineered["Year_Birth"]
    engineered["Age_Plausible_Flag"] = engineered["Age"].between(18, 100, inclusive="both").astype(int)

    engineered["Customer_Tenure_Days"] = (reference_date - dt_customer_parsed).dt.days
    engineered["Customer_Tenure_Years"] = engineered["Customer_Tenure_Days"] / 365.25

    engineered["Total_Spend"] = engineered[SPEND_COLUMNS].sum(axis=1)
    engineered["Total_Purchases"] = engineered[CHANNEL_PURCHASE_COLUMNS].sum(axis=1)
    engineered["Campaign_Acceptance_Total"] = engineered[CAMPAIGN_COLUMNS].sum(axis=1)
    engineered["Household_Children"] = engineered["Kidhome"] + engineered["Teenhome"]
    engineered["Has_Children"] = (engineered["Household_Children"] > 0).astype(int)

    engineered["Web_Purchase_Share"] = _safe_divide(engineered["NumWebPurchases"], engineered["Total_Purchases"])
    engineered["Catalog_Purchase_Share"] = _safe_divide(
        engineered["NumCatalogPurchases"], engineered["Total_Purchases"]
    )
    engineered["Store_Purchase_Share"] = _safe_divide(engineered["NumStorePurchases"], engineered["Total_Purchases"])
    engineered["Deal_Purchase_Share"] = _safe_divide(engineered["NumDealsPurchases"], engineered["Total_Purchases"])

    engineered["Wine_Spend_Share"] = _safe_divide(engineered["MntWines"], engineered["Total_Spend"])
    engineered["Fruit_Spend_Share"] = _safe_divide(engineered["MntFruits"], engineered["Total_Spend"])
    engineered["Meat_Spend_Share"] = _safe_divide(engineered["MntMeatProducts"], engineered["Total_Spend"])
    engineered["Fish_Spend_Share"] = _safe_divide(engineered["MntFishProducts"], engineered["Total_Spend"])
    engineered["Sweet_Spend_Share"] = _safe_divide(engineered["MntSweetProducts"], engineered["Total_Spend"])
    engineered["Gold_Spend_Share"] = _safe_divide(engineered["MntGoldProds"], engineered["Total_Spend"])

    engineered["Average_Spend_Per_Purchase"] = _safe_divide(engineered["Total_Spend"], engineered["Total_Purchases"])
    engineered["Web_Purchases_Per_Web_Visit"] = _safe_divide(
        engineered["NumWebPurchases"], engineered["NumWebVisitsMonth"]
    )

    summary = FeatureEngineeringSummary(
        input_rows=input_rows,
        output_rows=int(len(engineered)),
        input_columns=input_columns,
        output_columns=int(engineered.shape[1]),
        features_created=len([feature for feature in ENGINEERED_FEATURES if feature in engineered.columns]),
        dt_parse_failures=parse_failures,
        reference_date=reference_date,
        reference_year=reference_year,
        age_plausibility_min=18,
        age_plausibility_max=100,
        zero_total_purchase_rows=int((engineered["Total_Purchases"] == 0).sum()),
        zero_total_spend_rows=int((engineered["Total_Spend"] == 0).sum()),
        zero_web_visit_rows=int((engineered["NumWebVisitsMonth"] == 0).sum()),
    )

    return engineered, summary


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


def build_engineered_numeric_summary(df: pd.DataFrame, engineered_feature_names: list[str]) -> pd.DataFrame:
    numeric_engineered = [col for col in engineered_feature_names if col in df.columns and pd.api.types.is_numeric_dtype(df[col])]
    if not numeric_engineered:
        return pd.DataFrame()

    summary = (
        df[numeric_engineered]
        .describe(percentiles=[0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
        .T.reset_index()
        .rename(
            columns={
                "index": "feature",
                "count": "non_missing_count",
                "mean": "mean",
                "std": "std",
                "min": "min",
                "1%": "p01",
                "5%": "p05",
                "25%": "p25",
                "50%": "p50",
                "75%": "p75",
                "95%": "p95",
                "99%": "p99",
                "max": "max",
            }
        )
    )

    missing_count_map = df[numeric_engineered].isna().sum().to_dict()
    summary["missing_count"] = summary["feature"].map(missing_count_map).astype(int)
    summary["missing_pct"] = (summary["missing_count"] / max(len(df), 1)) * 100
    summary["zero_count"] = summary["feature"].map(lambda col: int((df[col] == 0).sum()))
    summary["zero_pct"] = (summary["zero_count"] / max(len(df), 1)) * 100

    ordered_columns = [
        "feature",
        "non_missing_count",
        "missing_count",
        "missing_pct",
        "zero_count",
        "zero_pct",
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
    ]
    return summary[ordered_columns].sort_values("feature").reset_index(drop=True)


def build_feature_catalog(df: pd.DataFrame) -> pd.DataFrame:
    descriptions = {
        "Age": "Reference year minus Year_Birth.",
        "Age_Plausible_Flag": "1 if Age is between 18 and 100, else 0.",
        "Customer_Tenure_Days": "Days between Dt_Customer and reference date.",
        "Customer_Tenure_Years": "Customer_Tenure_Days divided by 365.25.",
        "Total_Spend": "Sum of all Mnt* spend variables.",
        "Total_Purchases": "Sum of web, catalog, and store purchase counts.",
        "Campaign_Acceptance_Total": "Sum of AcceptedCmp1 to AcceptedCmp5.",
        "Household_Children": "Kidhome + Teenhome.",
        "Has_Children": "1 if Household_Children > 0 else 0.",
        "Web_Purchase_Share": "NumWebPurchases / Total_Purchases; 0 when denominator is 0.",
        "Catalog_Purchase_Share": "NumCatalogPurchases / Total_Purchases; 0 when denominator is 0.",
        "Store_Purchase_Share": "NumStorePurchases / Total_Purchases; 0 when denominator is 0.",
        "Deal_Purchase_Share": "NumDealsPurchases / Total_Purchases; 0 when denominator is 0.",
        "Wine_Spend_Share": "MntWines / Total_Spend; 0 when denominator is 0.",
        "Fruit_Spend_Share": "MntFruits / Total_Spend; 0 when denominator is 0.",
        "Meat_Spend_Share": "MntMeatProducts / Total_Spend; 0 when denominator is 0.",
        "Fish_Spend_Share": "MntFishProducts / Total_Spend; 0 when denominator is 0.",
        "Sweet_Spend_Share": "MntSweetProducts / Total_Spend; 0 when denominator is 0.",
        "Gold_Spend_Share": "MntGoldProds / Total_Spend; 0 when denominator is 0.",
        "Average_Spend_Per_Purchase": "Total_Spend / Total_Purchases; 0 when denominator is 0.",
        "Web_Purchases_Per_Web_Visit": "NumWebPurchases / NumWebVisitsMonth; 0 when denominator is 0.",
    }

    rows: list[dict[str, object]] = []
    for feature in ENGINEERED_FEATURES:
        present = feature in df.columns
        rows.append(
            {
                "feature": feature,
                "created": present,
                "dtype": str(df[feature].dtype) if present else "<missing>",
                "description": descriptions.get(feature, ""),
                "recommended_for_clustering": feature not in NON_CLUSTERING_COLUMNS,
            }
        )

    return pd.DataFrame(rows)

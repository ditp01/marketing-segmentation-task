from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str((Path.cwd() / ".cache" / "matplotlib").resolve()))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score, silhouette_score
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

RANDOM_SEED = 42

BASE_FEATURES = [
    "Age",
    "Income",
    "Customer_Tenure_Years",
    "Recency",
    "Total_Spend",
    "Total_Purchases",
    "Average_Spend_Per_Purchase",
    "NumWebVisitsMonth",
    "Household_Children",
    "Web_Purchase_Share",
    "Catalog_Purchase_Share",
    "Store_Purchase_Share",
    "Deal_Purchase_Share",
    "Wine_Spend_Share",
    "Meat_Spend_Share",
    "Fish_Spend_Share",
    "Fruit_Spend_Share",
    "Sweet_Spend_Share",
    "Gold_Spend_Share",
]

LOG_TRANSFORM_FEATURES = [
    "Income",
    "Total_Spend",
    "Total_Purchases",
    "Average_Spend_Per_Purchase",
    "NumWebVisitsMonth",
]

EXCLUDED_CLUSTER_INPUTS = [
    "ID",
    "Response",
    "AcceptedCmp1",
    "AcceptedCmp2",
    "AcceptedCmp3",
    "AcceptedCmp4",
    "AcceptedCmp5",
    "Campaign_Acceptance_Total",
    "Z_CostContact",
    "Z_Revenue",
]

PROFILE_COLUMNS = [
    "Total_Spend",
    "Income",
    "Recency",
    "Total_Purchases",
    "Average_Spend_Per_Purchase",
    "Household_Children",
    "Response",
    "Campaign_Acceptance_Total",
    "Web_Purchase_Share",
    "Catalog_Purchase_Share",
    "Store_Purchase_Share",
    "Deal_Purchase_Share",
    "Wine_Spend_Share",
    "Meat_Spend_Share",
    "Fish_Spend_Share",
    "Fruit_Spend_Share",
    "Sweet_Spend_Share",
    "Gold_Spend_Share",
]


@dataclass(frozen=True)
class ClusteringPrepResult:
    modelling_df: pd.DataFrame
    eval_df: pd.DataFrame
    scaled_array: np.ndarray
    scaler: StandardScaler
    feature_table: pd.DataFrame
    dropped_rows: int
    dropped_row_pct: float


def _validate_required_columns(df: pd.DataFrame, required: list[str]) -> None:
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise KeyError(f"Missing required columns for clustering: {missing}")


def _cluster_size_stats(labels: np.ndarray) -> tuple[str, int, float]:
    counts = pd.Series(labels).value_counts().sort_index()
    size_str = "|".join([f"{int(idx)}:{int(count)}" for idx, count in counts.items()])
    min_size = int(counts.min())
    min_share = float(counts.min() / counts.sum())
    return size_str, min_size, min_share


def _interpretability_note(min_cluster_share: float) -> str:
    if min_cluster_share < 0.05:
        return "Very small cluster detected (<5%): risk of unstable niche segment."
    if min_cluster_share < 0.08:
        return "Small cluster detected (<8%): interpret with caution."
    if min_cluster_share < 0.12:
        return "Moderately imbalanced cluster sizes."
    return "Cluster sizes appear reasonably balanced."


def _safe_minmax_scale(series: pd.Series, ascending: bool = True) -> pd.Series:
    values = series.astype(float).to_numpy()
    finite_mask = np.isfinite(values)
    if finite_mask.sum() == 0:
        return pd.Series(0.0, index=series.index)
    finite_values = values[finite_mask]
    min_v = float(finite_values.min())
    max_v = float(finite_values.max())
    if np.isclose(max_v, min_v):
        scaled = np.ones_like(values, dtype=float) * 0.5
    else:
        scaled = (values - min_v) / (max_v - min_v)
    scaled = np.where(finite_mask, scaled, 0.0)
    if not ascending:
        scaled = 1.0 - scaled
    return pd.Series(scaled, index=series.index)


def prepare_clustering_data(df: pd.DataFrame) -> ClusteringPrepResult:
    _validate_required_columns(df, BASE_FEATURES)

    modelling_df = df.copy()
    for feature in BASE_FEATURES:
        if feature in LOG_TRANSFORM_FEATURES:
            modelling_df[f"log1p_{feature}"] = np.log1p(modelling_df[feature])
        else:
            modelling_df[f"log1p_{feature}"] = modelling_df[feature]

    modelling_feature_columns = [f"log1p_{feature}" for feature in BASE_FEATURES]
    model_matrix = modelling_df[modelling_feature_columns].replace([np.inf, -np.inf], np.nan)

    valid_mask = ~model_matrix.isna().any(axis=1)
    dropped_rows = int((~valid_mask).sum())
    dropped_row_pct = float((dropped_rows / max(len(df), 1)) * 100)

    modelling_df = modelling_df.loc[valid_mask].copy().reset_index(drop=True)
    eval_df = df.loc[valid_mask].copy().reset_index(drop=True)
    model_matrix = model_matrix.loc[valid_mask].reset_index(drop=True)

    scaler = StandardScaler()
    scaled_array = scaler.fit_transform(model_matrix)

    feature_rows = []
    for feature in BASE_FEATURES:
        transformed_name = f"log1p_{feature}"
        feature_rows.append(
            {
                "feature_original": feature,
                "feature_model_input": transformed_name,
                "log1p_applied": feature in LOG_TRANSFORM_FEATURES,
                "excluded_from_clustering": feature in EXCLUDED_CLUSTER_INPUTS,
                "notes": (
                    "Magnitude feature transformed with log1p to reduce skew."
                    if feature in LOG_TRANSFORM_FEATURES
                    else "Used as-is before scaling."
                ),
            }
        )
    feature_table = pd.DataFrame(feature_rows)

    return ClusteringPrepResult(
        modelling_df=modelling_df,
        eval_df=eval_df,
        scaled_array=scaled_array,
        scaler=scaler,
        feature_table=feature_table,
        dropped_rows=dropped_rows,
        dropped_row_pct=dropped_row_pct,
    )


def run_kmeans_candidates(
    scaled_array: np.ndarray,
    eval_df: pd.DataFrame,
    candidate_ks: list[int],
) -> tuple[pd.DataFrame, dict[str, np.ndarray]]:
    rows: list[dict[str, object]] = []
    labels_map: dict[str, np.ndarray] = {}

    for k in candidate_ks:
        model = KMeans(n_clusters=k, n_init=20, random_state=RANDOM_SEED)
        labels = model.fit_predict(scaled_array)
        solution = f"kmeans_k{k}"
        labels_map[solution] = labels

        cluster_size_str, min_cluster_size, min_cluster_share = _cluster_size_stats(labels)
        silhouette = float(silhouette_score(scaled_array, labels))
        calinski = float(calinski_harabasz_score(scaled_array, labels))
        davies = float(davies_bouldin_score(scaled_array, labels))

        response_means = eval_df.assign(cluster=labels).groupby("cluster")["Response"].mean()
        spend_means = eval_df.assign(cluster=labels).groupby("cluster")["Total_Spend"].mean()

        rows.append(
            {
                "method": "kmeans",
                "solution": solution,
                "n_clusters": k,
                "inertia": float(model.inertia_),
                "silhouette_score": silhouette,
                "calinski_harabasz_score": calinski,
                "davies_bouldin_score": davies,
                "cluster_size_distribution": cluster_size_str,
                "min_cluster_size": min_cluster_size,
                "min_cluster_share": min_cluster_share,
                "response_rate_range": float(response_means.max() - response_means.min()),
                "total_spend_mean_range": float(spend_means.max() - spend_means.min()),
                "interpretability_note": _interpretability_note(min_cluster_share),
            }
        )

    metrics_df = pd.DataFrame(rows).sort_values("n_clusters").reset_index(drop=True)
    return metrics_df, labels_map


def run_gmm_candidates(
    scaled_array: np.ndarray,
    eval_df: pd.DataFrame,
    candidate_components: list[int],
) -> tuple[pd.DataFrame, dict[str, np.ndarray], dict[str, np.ndarray], dict[str, GaussianMixture]]:
    rows: list[dict[str, object]] = []
    labels_map: dict[str, np.ndarray] = {}
    proba_map: dict[str, np.ndarray] = {}
    model_map: dict[str, GaussianMixture] = {}

    for n_components in candidate_components:
        model = GaussianMixture(
            n_components=n_components,
            covariance_type="full",
            random_state=RANDOM_SEED,
            n_init=5,
            reg_covar=1e-6,
        )
        model.fit(scaled_array)
        probabilities = model.predict_proba(scaled_array)
        labels = model.predict(scaled_array)

        solution = f"gmm_n{n_components}"
        labels_map[solution] = labels
        proba_map[solution] = probabilities
        model_map[solution] = model

        cluster_size_str, min_cluster_size, min_cluster_share = _cluster_size_stats(labels)
        silhouette = float(silhouette_score(scaled_array, labels))
        max_assignment_prob = probabilities.max(axis=1)

        response_means = eval_df.assign(cluster=labels).groupby("cluster")["Response"].mean()
        spend_means = eval_df.assign(cluster=labels).groupby("cluster")["Total_Spend"].mean()

        rows.append(
            {
                "method": "gmm",
                "solution": solution,
                "n_components": n_components,
                "aic": float(model.aic(scaled_array)),
                "bic": float(model.bic(scaled_array)),
                "silhouette_score": silhouette,
                "cluster_size_distribution": cluster_size_str,
                "min_cluster_size": min_cluster_size,
                "min_cluster_share": min_cluster_share,
                "avg_max_assignment_probability": float(max_assignment_prob.mean()),
                "pct_max_assignment_prob_below_0_60": float((max_assignment_prob < 0.60).mean() * 100),
                "pct_max_assignment_prob_below_0_70": float((max_assignment_prob < 0.70).mean() * 100),
                "response_rate_range": float(response_means.max() - response_means.min()),
                "total_spend_mean_range": float(spend_means.max() - spend_means.min()),
                "interpretability_note": _interpretability_note(min_cluster_share),
            }
        )

    metrics_df = pd.DataFrame(rows).sort_values("n_components").reset_index(drop=True)
    return metrics_df, labels_map, proba_map, model_map


def build_model_comparison_table(kmeans_metrics: pd.DataFrame, gmm_metrics: pd.DataFrame) -> pd.DataFrame:
    kmeans = kmeans_metrics.copy()
    gmm = gmm_metrics.copy()

    kmeans["avg_max_assignment_probability"] = np.nan
    kmeans["pct_max_assignment_prob_below_0_70"] = np.nan
    kmeans["bic"] = np.nan
    kmeans["aic"] = np.nan
    kmeans["model_complexity"] = kmeans["n_clusters"]

    gmm["inertia"] = np.nan
    gmm["calinski_harabasz_score"] = np.nan
    gmm["davies_bouldin_score"] = np.nan
    gmm["model_complexity"] = gmm["n_components"]

    combined = pd.concat(
        [
            kmeans[
                [
                    "method",
                    "solution",
                    "model_complexity",
                    "silhouette_score",
                    "min_cluster_share",
                    "response_rate_range",
                    "total_spend_mean_range",
                    "davies_bouldin_score",
                    "calinski_harabasz_score",
                    "inertia",
                    "aic",
                    "bic",
                    "avg_max_assignment_probability",
                    "pct_max_assignment_prob_below_0_70",
                    "interpretability_note",
                ]
            ],
            gmm[
                [
                    "method",
                    "solution",
                    "model_complexity",
                    "silhouette_score",
                    "min_cluster_share",
                    "response_rate_range",
                    "total_spend_mean_range",
                    "davies_bouldin_score",
                    "calinski_harabasz_score",
                    "inertia",
                    "aic",
                    "bic",
                    "avg_max_assignment_probability",
                    "pct_max_assignment_prob_below_0_70",
                    "interpretability_note",
                ]
            ],
        ],
        ignore_index=True,
    )

    score = pd.Series(0.0, index=combined.index)
    score += _safe_minmax_scale(combined["silhouette_score"], ascending=True)
    score += _safe_minmax_scale(combined["min_cluster_share"], ascending=True)
    score += _safe_minmax_scale(combined["response_rate_range"], ascending=True)
    score += _safe_minmax_scale(combined["total_spend_mean_range"], ascending=True)
    score += _safe_minmax_scale(combined["davies_bouldin_score"], ascending=False)
    score += _safe_minmax_scale(combined["calinski_harabasz_score"], ascending=True)
    score += _safe_minmax_scale(combined["avg_max_assignment_probability"], ascending=True)
    score += _safe_minmax_scale(combined["pct_max_assignment_prob_below_0_70"], ascending=False)
    score += _safe_minmax_scale(combined["bic"], ascending=False)

    combined["composite_score"] = score.round(6)
    combined["overall_rank"] = combined["composite_score"].rank(method="dense", ascending=False).astype(int)

    combined["method_rank"] = (
        combined.groupby("method")["composite_score"].rank(method="dense", ascending=False).astype(int)
    )
    combined = combined.sort_values(["overall_rank", "method", "model_complexity"]).reset_index(drop=True)
    return combined


def build_cluster_profiles(
    eval_df: pd.DataFrame,
    assignments: pd.DataFrame,
) -> pd.DataFrame:
    rows: list[pd.DataFrame] = []

    profile_columns_available = [column for column in PROFILE_COLUMNS if column in eval_df.columns]

    for assignment_column in assignments.columns:
        if assignment_column == "ID":
            continue
        method = "kmeans" if assignment_column.startswith("kmeans_") else "gmm"
        temp = eval_df.copy()
        temp["cluster"] = assignments[assignment_column]
        grouped = temp.groupby("cluster").agg(
            cluster_size=("cluster", "count"),
            cluster_share=("cluster", lambda s: float(len(s) / len(temp))),
            **{f"avg_{col}": (col, "mean") for col in profile_columns_available},
        )
        grouped = grouped.reset_index()
        grouped.insert(0, "solution", assignment_column)
        grouped.insert(0, "method", method)
        rows.append(grouped)

    if not rows:
        return pd.DataFrame()
    return pd.concat(rows, ignore_index=True)


def choose_recommended_solution(model_comparison: pd.DataFrame) -> tuple[str, str]:
    # Prefer stable cluster sizes with non-trivial commercial separation.
    stable = model_comparison[model_comparison["min_cluster_share"] >= 0.08].copy()
    if stable.empty:
        stable = model_comparison.copy()

    stable = stable.sort_values(
        ["composite_score", "response_rate_range", "total_spend_mean_range"],
        ascending=[False, False, False],
    )
    best_row = stable.iloc[0]
    return str(best_row["method"]), str(best_row["solution"])


def build_segment_assignments_table(
    id_series: pd.Series,
    kmeans_labels_map: dict[str, np.ndarray],
    gmm_labels_map: dict[str, np.ndarray],
    gmm_proba_map: dict[str, np.ndarray],
    recommended_method: str,
    recommended_solution: str,
) -> pd.DataFrame:
    assignments = pd.DataFrame({"ID": id_series.values})
    for solution, labels in kmeans_labels_map.items():
        assignments[solution] = labels
    for solution, labels in gmm_labels_map.items():
        assignments[solution] = labels

    assignments["recommended_method"] = recommended_method
    assignments["recommended_solution"] = recommended_solution
    assignments["recommended_cluster"] = assignments[recommended_solution]

    if recommended_solution in gmm_proba_map:
        probs = gmm_proba_map[recommended_solution].max(axis=1)
        assignments["recommended_max_assignment_probability"] = probs
    else:
        assignments["recommended_max_assignment_probability"] = 1.0

    return assignments


def fit_pca_for_visualisation(scaled_array: np.ndarray) -> tuple[np.ndarray, PCA]:
    pca = PCA(n_components=2, random_state=RANDOM_SEED)
    components = pca.fit_transform(scaled_array)
    return components, pca


def save_kmeans_metrics_plot(kmeans_metrics: pd.DataFrame, output_path: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    sns.lineplot(data=kmeans_metrics, x="n_clusters", y="inertia", marker="o", ax=axes[0, 0], color="#1f77b4")
    axes[0, 0].set_title("KMeans Inertia by k")

    sns.lineplot(
        data=kmeans_metrics, x="n_clusters", y="silhouette_score", marker="o", ax=axes[0, 1], color="#ff7f0e"
    )
    axes[0, 1].set_title("KMeans Silhouette by k")

    sns.lineplot(
        data=kmeans_metrics,
        x="n_clusters",
        y="calinski_harabasz_score",
        marker="o",
        ax=axes[1, 0],
        color="#2ca02c",
    )
    axes[1, 0].set_title("KMeans Calinski-Harabasz by k")

    sns.lineplot(
        data=kmeans_metrics,
        x="n_clusters",
        y="davies_bouldin_score",
        marker="o",
        ax=axes[1, 1],
        color="#d62728",
    )
    axes[1, 1].set_title("KMeans Davies-Bouldin by k")

    for ax in axes.flatten():
        ax.set_xlabel("k")
        ax.grid(alpha=0.2)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def save_gmm_aic_bic_plot(gmm_metrics: pd.DataFrame, output_path: Path) -> None:
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=gmm_metrics, x="n_components", y="aic", marker="o", label="AIC", color="#1f77b4")
    sns.lineplot(data=gmm_metrics, x="n_components", y="bic", marker="o", label="BIC", color="#ff7f0e")
    plt.title("GMM AIC/BIC by Components")
    plt.xlabel("Number of Components")
    plt.ylabel("Score (Lower is Better)")
    plt.grid(alpha=0.2)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def save_cluster_size_comparison(
    assignments: pd.DataFrame, recommended_solution: str, output_path: Path
) -> None:
    size_df = assignments[recommended_solution].value_counts().sort_index().reset_index()
    size_df.columns = ["cluster", "count"]
    size_df["share_pct"] = (size_df["count"] / size_df["count"].sum()) * 100
    plt.figure(figsize=(8, 5))
    sns.barplot(data=size_df, x="cluster", y="share_pct", color="#2ca02c")
    plt.title(f"Cluster Size Share (%) - {recommended_solution}")
    plt.xlabel("Cluster")
    plt.ylabel("Share of Customers (%)")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def save_response_rate_by_cluster(
    eval_df: pd.DataFrame, assignments: pd.DataFrame, recommended_solution: str, output_path: Path
) -> None:
    temp = eval_df.copy()
    temp["cluster"] = assignments[recommended_solution]
    rate_df = temp.groupby("cluster")["Response"].mean().reset_index()
    rate_df["response_rate_pct"] = rate_df["Response"] * 100
    plt.figure(figsize=(8, 5))
    sns.barplot(data=rate_df, x="cluster", y="response_rate_pct", color="#d62728")
    plt.title(f"Response Rate by Cluster - {recommended_solution}")
    plt.xlabel("Cluster")
    plt.ylabel("Response Rate (%)")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def save_pca_cluster_plot(
    pca_components: np.ndarray,
    assignments: pd.DataFrame,
    recommended_solution: str,
    output_path: Path,
) -> None:
    plot_df = pd.DataFrame(
        {
            "PC1": pca_components[:, 0],
            "PC2": pca_components[:, 1],
            "cluster": assignments[recommended_solution],
        }
    )
    sampled = plot_df.sample(min(1500, len(plot_df)), random_state=RANDOM_SEED)
    plt.figure(figsize=(9, 6))
    sns.scatterplot(data=sampled, x="PC1", y="PC2", hue="cluster", palette="tab10", alpha=0.7, s=30)
    plt.title(f"PCA (2D) - {recommended_solution}")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

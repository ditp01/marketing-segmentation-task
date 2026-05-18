from __future__ import annotations

from pathlib import Path
import sys

import joblib
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.clustering import (
    BASE_FEATURES,
    EXCLUDED_CLUSTER_INPUTS,
    RANDOM_SEED,
    build_cluster_profiles,
    build_model_comparison_table,
    build_segment_assignments_table,
    choose_recommended_solution,
    fit_pca_for_visualisation,
    prepare_clustering_data,
    run_gmm_candidates,
    run_kmeans_candidates,
    save_cluster_size_comparison,
    save_gmm_aic_bic_plot,
    save_kmeans_metrics_plot,
    save_pca_cluster_plot,
    save_response_rate_by_cluster,
)


def as_markdown_code_block(dataframe: pd.DataFrame, max_rows: int = 20) -> str:
    if dataframe.empty:
        return "No rows."
    return "```\n" + dataframe.head(max_rows).to_string(index=False) + "\n```"


def write_stage_markdown(
    output_path: Path,
    input_path: Path,
    eda_output_path: Path,
    decisions_path: Path,
    row_count_used: int,
    prep_dropped_rows: int,
    prep_dropped_row_pct: float,
    feature_table: pd.DataFrame,
    kmeans_metrics: pd.DataFrame,
    gmm_metrics: pd.DataFrame,
    comparison: pd.DataFrame,
    recommended_method: str,
    recommended_solution: str,
    cluster_profiles: pd.DataFrame,
    figure_paths: list[Path],
) -> None:
    recommended_row = comparison[comparison["solution"] == recommended_solution].iloc[0]
    best_kmeans_row = comparison[comparison["method"] == "kmeans"].sort_values(
        "composite_score", ascending=False
    ).iloc[0]
    best_gmm_row = comparison[comparison["method"] == "gmm"].sort_values(
        "composite_score", ascending=False
    ).iloc[0]
    rec_profiles = cluster_profiles[cluster_profiles["solution"] == recommended_solution].copy()
    rec_profiles = rec_profiles.sort_values("cluster").reset_index(drop=True)

    risk_notes: list[str] = []
    if float(recommended_row["min_cluster_share"]) < 0.08:
        risk_notes.append("Recommended solution includes a small cluster (<8% of customers).")
    if recommended_method == "gmm":
        fuzzy_pct = float(recommended_row.get("pct_max_assignment_prob_below_0_70", 0.0))
        if fuzzy_pct > 30:
            risk_notes.append(
                f"GMM assignment uncertainty is notable ({fuzzy_pct:.2f}% of customers below 0.70 max probability)."
            )
    if prep_dropped_rows > 0:
        risk_notes.append(
            f"{prep_dropped_rows} rows ({prep_dropped_row_pct:.2f}%) were dropped during clustering preprocessing."
        )
    if not risk_notes:
        risk_notes.append("No major preprocessing or stability risks identified for the recommended solution.")

    decisions_note = (
        f"Decision context file found: `{decisions_path.as_posix()}`."
        if decisions_path.exists()
        else f"Decision context file not found: `{decisions_path.as_posix()}`."
    )

    lines = [
        "# Stage 04 Clustering",
        "",
        "## Inputs and Row Count",
        f"- Input dataset: `{input_path.as_posix()}`",
        f"- EDA summary used: `{eda_output_path.as_posix()}`",
        f"- {decisions_note}",
        f"- Rows used for clustering: {row_count_used}",
        "",
        "## Preprocessing Applied",
        f"- Fixed random seed: `{RANDOM_SEED}`",
        f"- Candidate base features (before transformation): {', '.join(BASE_FEATURES)}",
        f"- Explicitly excluded from clustering inputs: {', '.join(EXCLUDED_CLUSTER_INPUTS)}",
        "- `log1p` applied to skewed magnitude features (Income, Total_Spend, Total_Purchases, Average_Spend_Per_Purchase, NumWebVisitsMonth).",
        "- Infinite values replaced with missing and rows with missing model features dropped.",
        f"- Dropped rows during preprocessing: {prep_dropped_rows} ({prep_dropped_row_pct:.2f}%).",
        "- Numeric model features standardized with `StandardScaler` before KMeans/GMM.",
        "",
        "Final clustering input feature table:",
        as_markdown_code_block(feature_table, max_rows=30),
        "",
        "## KMeans Candidate Results",
        as_markdown_code_block(kmeans_metrics, max_rows=20),
        "",
        "## GMM Candidate Results",
        as_markdown_code_block(gmm_metrics, max_rows=20),
        "",
        "## Model Comparison",
        as_markdown_code_block(comparison, max_rows=20),
        "",
        "KMeans vs GMM comparison notes:",
        f"- Best KMeans candidate: `{best_kmeans_row['solution']}` | silhouette `{float(best_kmeans_row['silhouette_score']):.4f}` | min cluster share `{float(best_kmeans_row['min_cluster_share']) * 100:.2f}%`.",
        f"- Best GMM candidate: `{best_gmm_row['solution']}` | silhouette `{float(best_gmm_row['silhouette_score']):.4f}` | min cluster share `{float(best_gmm_row['min_cluster_share']) * 100:.2f}%`.",
        f"- GMM assignment certainty (best GMM): avg max probability `{float(best_gmm_row['avg_max_assignment_probability']):.4f}`, below 0.70 for `{float(best_gmm_row['pct_max_assignment_prob_below_0_70']):.2f}%` of customers.",
        "- GMM produced smaller niche components across candidates, while KMeans offered more balanced cluster sizes for practical campaign targeting.",
        "",
        "## Recommended Solution",
        f"- Recommended method: `{recommended_method}`",
        f"- Recommended solution: `{recommended_solution}`",
        f"- Composite score: {float(recommended_row['composite_score']):.4f}",
        f"- Silhouette score: {float(recommended_row['silhouette_score']):.4f}",
        f"- Minimum cluster share: {float(recommended_row['min_cluster_share']) * 100:.2f}%",
        f"- Response-rate range across clusters: {float(recommended_row['response_rate_range']) * 100:.2f} percentage points",
        f"- Total spend mean range across clusters: {float(recommended_row['total_spend_mean_range']):.2f}",
        f"- Interpretability note: {recommended_row['interpretability_note']}",
        "",
        "Recommended solution profile table:",
        as_markdown_code_block(rec_profiles, max_rows=30),
        "",
        "## Risks and Caveats",
    ]
    lines.extend([f"- {note}" for note in risk_notes])
    lines.extend(
        [
            "",
            "## Generated Figures",
        ]
    )
    lines.extend([f"- `{path.as_posix()}`" for path in figure_paths])

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    input_path = REPO_ROOT / "data" / "processed" / "marketing_campaign_processed_features_engineered.csv"
    eda_output_path = REPO_ROOT / "outputs" / "stage-outputs" / "03-eda.md"
    decisions_path = REPO_ROOT / "project" / "decisions.md"

    output_tables_dir = REPO_ROOT / "outputs" / "tables"
    output_stage_dir = REPO_ROOT / "outputs" / "stage-outputs"
    output_models_dir = REPO_ROOT / "outputs" / "models"
    output_figures_dir = REPO_ROOT / "reports" / "figures"
    segment_assignments_path = REPO_ROOT / "outputs" / "segment_assignments.csv"

    output_tables_dir.mkdir(parents=True, exist_ok=True)
    output_stage_dir.mkdir(parents=True, exist_ok=True)
    output_models_dir.mkdir(parents=True, exist_ok=True)
    output_figures_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    if not eda_output_path.exists():
        raise FileNotFoundError(f"Expected Stage 03 output not found: {eda_output_path}")

    df = pd.read_csv(input_path, sep=";")
    prep = prepare_clustering_data(df)

    kmeans_metrics, kmeans_labels_map = run_kmeans_candidates(prep.scaled_array, prep.eval_df, [3, 4, 5, 6])
    gmm_metrics, gmm_labels_map, gmm_proba_map, gmm_model_map = run_gmm_candidates(
        prep.scaled_array, prep.eval_df, [3, 4, 5, 6]
    )

    comparison = build_model_comparison_table(kmeans_metrics, gmm_metrics)
    recommended_method, recommended_solution = choose_recommended_solution(comparison)
    comparison["recommended_solution"] = comparison["solution"] == recommended_solution

    candidate_assignments = pd.DataFrame({"ID": prep.eval_df["ID"].values})
    for solution, labels in kmeans_labels_map.items():
        candidate_assignments[solution] = labels
    for solution, labels in gmm_labels_map.items():
        candidate_assignments[solution] = labels

    cluster_profiles = build_cluster_profiles(prep.eval_df, candidate_assignments)

    segment_assignments = build_segment_assignments_table(
        id_series=prep.eval_df["ID"],
        kmeans_labels_map=kmeans_labels_map,
        gmm_labels_map=gmm_labels_map,
        gmm_proba_map=gmm_proba_map,
        recommended_method=recommended_method,
        recommended_solution=recommended_solution,
    )

    prep.feature_table.to_csv(output_tables_dir / "04_clustering_input_features.csv", index=False)
    kmeans_metrics.to_csv(output_tables_dir / "04_kmeans_metrics.csv", index=False)
    gmm_metrics.to_csv(output_tables_dir / "04_gmm_metrics.csv", index=False)
    comparison.to_csv(output_tables_dir / "04_model_comparison.csv", index=False)
    cluster_profiles.to_csv(output_tables_dir / "04_cluster_profiles.csv", index=False)
    segment_assignments.to_csv(segment_assignments_path, index=False)

    # Save recommended model artefacts.
    if recommended_method == "kmeans":
        k = int(recommended_solution.replace("kmeans_k", ""))
        recommended_model = KMeans(n_clusters=k, n_init=20, random_state=RANDOM_SEED).fit(prep.scaled_array)
    else:
        recommended_model = gmm_model_map[recommended_solution]
    joblib.dump(recommended_model, output_models_dir / f"04_recommended_{recommended_solution}.joblib")
    joblib.dump(prep.scaler, output_models_dir / "04_clustering_scaler.joblib")
    pca_components, pca_model = fit_pca_for_visualisation(prep.scaled_array)
    joblib.dump(pca_model, output_models_dir / "04_clustering_pca_2d.joblib")

    # Figures.
    fig_kmeans = output_figures_dir / "04_kmeans_metric_comparison.png"
    fig_gmm = output_figures_dir / "04_gmm_aic_bic.png"
    fig_sizes = output_figures_dir / "04_recommended_cluster_size_share.png"
    fig_response = output_figures_dir / "04_recommended_response_rate_by_cluster.png"
    fig_pca = output_figures_dir / "04_recommended_pca_scatter.png"

    save_kmeans_metrics_plot(kmeans_metrics, fig_kmeans)
    save_gmm_aic_bic_plot(gmm_metrics, fig_gmm)
    save_cluster_size_comparison(segment_assignments, recommended_solution, fig_sizes)
    save_response_rate_by_cluster(prep.eval_df, segment_assignments, recommended_solution, fig_response)
    save_pca_cluster_plot(pca_components, segment_assignments, recommended_solution, fig_pca)

    figure_paths = [fig_kmeans, fig_gmm, fig_sizes, fig_response, fig_pca]

    write_stage_markdown(
        output_path=output_stage_dir / "04-clustering.md",
        input_path=input_path,
        eda_output_path=eda_output_path,
        decisions_path=decisions_path,
        row_count_used=len(prep.eval_df),
        prep_dropped_rows=prep.dropped_rows,
        prep_dropped_row_pct=prep.dropped_row_pct,
        feature_table=prep.feature_table,
        kmeans_metrics=kmeans_metrics,
        gmm_metrics=gmm_metrics,
        comparison=comparison,
        recommended_method=recommended_method,
        recommended_solution=recommended_solution,
        cluster_profiles=cluster_profiles,
        figure_paths=figure_paths,
    )

    print("Stage 04 clustering completed.")
    print(f"Input: {input_path.as_posix()}")
    print(f"Recommended solution: {recommended_solution} ({recommended_method})")
    print("Saved tables:")
    print(f"- {(output_tables_dir / '04_clustering_input_features.csv').as_posix()}")
    print(f"- {(output_tables_dir / '04_kmeans_metrics.csv').as_posix()}")
    print(f"- {(output_tables_dir / '04_gmm_metrics.csv').as_posix()}")
    print(f"- {(output_tables_dir / '04_model_comparison.csv').as_posix()}")
    print(f"- {(output_tables_dir / '04_cluster_profiles.csv').as_posix()}")
    print(f"- {segment_assignments_path.as_posix()}")
    print("Saved models:")
    print(f"- {(output_models_dir / f'04_recommended_{recommended_solution}.joblib').as_posix()}")
    print(f"- {(output_models_dir / '04_clustering_scaler.joblib').as_posix()}")
    print(f"- {(output_models_dir / '04_clustering_pca_2d.joblib').as_posix()}")
    print("Saved figures:")
    for figure_path in figure_paths:
        print(f"- {figure_path.as_posix()}")
    print(f"Stage summary: {(output_stage_dir / '04-clustering.md').as_posix()}")


if __name__ == "__main__":
    main()

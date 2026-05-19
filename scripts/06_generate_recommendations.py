from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.reporting import (
    build_kpi_guidance,
    build_recommendation_matrix,
    build_segment_evidence_summary,
    load_stage05_segment_inputs,
    write_final_report_markdown,
    write_stage06_summary_markdown,
)


def main() -> None:
    profile_summary_path = REPO_ROOT / "outputs" / "tables" / "05_segment_profile_summary.csv"
    response_summary_path = REPO_ROOT / "outputs" / "tables" / "05_segment_response_summary.csv"
    channel_summary_path = REPO_ROOT / "outputs" / "tables" / "05_segment_channel_summary.csv"
    product_summary_path = REPO_ROOT / "outputs" / "tables" / "05_segment_product_summary.csv"
    stage05_summary_path = REPO_ROOT / "outputs" / "stage-outputs" / "05-segment-profiling.md"

    output_tables_dir = REPO_ROOT / "outputs" / "tables"
    output_stage_dir = REPO_ROOT / "outputs" / "stage-outputs"
    reports_dir = REPO_ROOT / "reports"

    output_tables_dir.mkdir(parents=True, exist_ok=True)
    output_stage_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    required_inputs = [
        profile_summary_path,
        response_summary_path,
        channel_summary_path,
        product_summary_path,
        stage05_summary_path,
    ]
    missing_inputs = [path for path in required_inputs if not path.exists()]
    if missing_inputs:
        missing_str = "\n".join([f"- {path.as_posix()}" for path in missing_inputs])
        raise FileNotFoundError(f"Missing required stage 05 input(s):\n{missing_str}")

    segment_df = load_stage05_segment_inputs(
        profile_summary_path=profile_summary_path,
        response_summary_path=response_summary_path,
        channel_summary_path=channel_summary_path,
        product_summary_path=product_summary_path,
    )

    recommendation_matrix = build_recommendation_matrix(segment_df)
    kpi_guidance = build_kpi_guidance(segment_df)
    segment_evidence = build_segment_evidence_summary(segment_df)

    recommendation_matrix_path = output_tables_dir / "06_recommendation_matrix.csv"
    kpi_guidance_path = output_tables_dir / "06_kpi_guidance.csv"
    stage06_summary_path = output_stage_dir / "06-recommendations.md"
    final_report_path = reports_dir / "final_report.md"

    recommendation_matrix.to_csv(recommendation_matrix_path, index=False)
    kpi_guidance.to_csv(kpi_guidance_path, index=False)

    write_stage06_summary_markdown(
        output_path=stage06_summary_path,
        input_paths=[
            stage05_summary_path,
            profile_summary_path,
            response_summary_path,
            channel_summary_path,
            product_summary_path,
        ],
        segment_evidence=segment_evidence,
        recommendation_matrix=recommendation_matrix,
        kpi_guidance=kpi_guidance,
    )

    write_final_report_markdown(
        output_path=final_report_path,
        segment_evidence=segment_evidence,
        recommendation_matrix=recommendation_matrix,
        kpi_guidance=kpi_guidance,
    )

    print("Stage 06 recommendations and final report generation completed.")
    print("Saved outputs:")
    print(f"- {recommendation_matrix_path.as_posix()}")
    print(f"- {kpi_guidance_path.as_posix()}")
    print(f"- {stage06_summary_path.as_posix()}")
    print(f"- {final_report_path.as_posix()}")


if __name__ == "__main__":
    main()

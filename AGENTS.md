# Project

This is a customer segmentation analysis project using a marketing campaign dataset.

The goal is to produce commercially useful customer segments and marketing recommendations, not just a technical clustering exercise.

# Staged approach

This project is being completed in stages.

For each task:
- Read the relevant file in `project/stages/`
- Complete only the current stage
- Do not jump ahead to later stages unless explicitly instructed
- Do not write the final report until the final-report stage

After completing a stage, produce reviewable outputs

# Guide to the repo

Use the repo as follows:

- `data/raw/` contains the original dataset and must not be modified
- `data/processed/` contains cleaned or feature-engineered datasets
- `src/` contains reusable Python functions
- `scripts/` contains runnable stage scripts
- `outputs/stage-outputs/` contains generated markdown summaries for review
- `outputs/tables/` contains generated CSV summary tables
- `outputs/models/` contains saved model artefacts
- `reports/figures/` contains generated charts
- `reports/final_report.md` contains the final business-facing report
- `project/` contains planning notes, stage briefs, decisions, review notes, and next steps

# Rules

- Keep the raw data unchanged
- Reproducible scripts, not one-off manual analysis
- Use clear feature names
- Explain assumptions
- Complete only the current stage.
- Do not modify data/raw/.
- Use scripts to generate reviewable markdown outputs.
- Keep reusable logic in src/.
- Prioritise commercially interpretable segmentation.

# Coding standards

- Use Python
- Use `pathlib` for paths
- Keep reusable logic in `src/`
- Keep runnable workflows in `scripts/`
- Avoid hard-coded absolute paths
# Stage 05: Segment Profiling

## Status

Complete

## Goal

Profile the three customer clusters from the recommended K-means solution and turn them into clear, commercially useful customer segments.

The goal is to move from technical cluster labels:

- Cluster 0
- Cluster 1
- Cluster 2

to interpretable segment profiles that explain:

- who the customers are
- how they behave
- how valuable they are
- how responsive they are
- how they differ from each other
- what provisional segment names best describe them

This stage should focus on understanding and describing the segments.

## Context

Stage 04 recommended using the `kmeans_k3` solution.

The three clusters appear to be reasonably balanced and commercially interpretable:

- Cluster 0: high income, high spend, high purchases, low household children, high catalogue share, highest response rate
- Cluster 1: mid-value, high household children, wine-heavy, web/store-oriented, more deal-sensitive
- Cluster 2: low income, low spend, low purchase volume, store-heavy, deal-sensitive, lowest previous campaign acceptance

Use these as hypotheses only. Validate them through profiling before finalising segment names.

Rule:

Do not rerun clustering unless there is a clear error in the previous stage output. This stage should use the recommended `kmeans_k3` assignments from Stage 04.

## Inputs

- `data/processed/marketing_campaign_processed_features_engineered.csv`
- `outputs/segment_assignments.csv`
- `outputs/stage-outputs/04-clustering.md`
- `outputs/tables/04_cluster_profiles.csv`
- `outputs/tables/04_model_comparison.csv`

## Instructions for Codex

Complete this stage only.

Create a reproducible segment profiling script:

- `scripts/05_profile_segments.py`

The script should join the recommended K-means segment assignments back to the engineered customer dataset using `ID`.

Use the recommended solution from Stage 04:

- method: `kmeans`
- solution: `kmeans_k3`

Then create clear profile tables, figures, and a concise written summary for review.

## Profiling requirements

For each segment, calculate:

- customer count
- customer share
- average and median `Income`
- average and median `Total_Spend`
- average and median `Total_Purchases`
- average and median `Average_Spend_Per_Purchase`
- average `Recency`
- average `Age`
- average `Customer_Tenure_Years`
- average `Household_Children`
- percentage with children
- response rate
- average `Campaign_Acceptance_Total`
- percentage with any previous campaign acceptance
- complaint rate, if useful

Also profile channel behaviour:

- `Web_Purchase_Share`
- `Catalog_Purchase_Share`
- `Store_Purchase_Share`
- `Deal_Purchase_Share`
- average `NumWebPurchases`
- average `NumCatalogPurchases`
- average `NumStorePurchases`
- average `NumWebVisitsMonth`

Also profile product preferences:

- average spend by product category:
  - `MntWines`
  - `MntFruits`
  - `MntMeatProducts`
  - `MntFishProducts`
  - `MntSweetProducts`
  - `MntGoldProds`
- product category spend shares:
  - `Wine_Spend_Share`
  - `Meat_Spend_Share`
  - `Fish_Spend_Share`
  - `Fruit_Spend_Share`
  - `Sweet_Spend_Share`
  - `Gold_Spend_Share`

## Segment comparison requirements

Create comparison tables that make the segments easy to interpret.

Include:

- absolute segment profile table
- indexed profile table where overall average = 100
- segment ranking table for key business metrics
- response and campaign acceptance summary by segment
- channel mix summary by segment
- product preference summary by segment

The indexed table should help show which segments are above or below average.

For example:

- Total spend index
- Income index
- Response rate index
- Catalogue share index
- Deal share index
- Household children index

## Provisional segment names

Suggest provisional names for the three clusters, for me to evaluate.

Use names that are commercially meaningful and easy for a marketing stakeholder to understand.

Based on Stage 04, consider names along these lines, but validate them against the full profile:

- Cluster 0: `Affluent Premium Responders`
- Cluster 1: `Mid-Value Family Wine Buyers`
- Cluster 2: `Low-Value Deal-Oriented Shoppers`

These names are provisional. If the profiling output supports better names, use better names.

For each segment, write a short profile containing:

- provisional segment name
- size/share
- defining characteristics
- value level
- responsiveness
- channel behaviour
- product preferences
- risks or caveats

## Figures

Create a small set of useful figures in `reports/figures/`.

Useful figures may include:

- segment size/share bar chart
- average total spend by segment
- response rate by segment
- income and spend comparison by segment
- channel share by segment
- product category spend share by segment
- children/no-children rate by segment

Keep figures clear and reviewable. Do not create excessive charts.

## Do not

- Do not rerun clustering.
- Do not change segment assignments.
- Do not write final marketing recommendations.
- Do not modify raw data.
- Do not use technical names like “Cluster 0” as the final segment names without interpretation.
- Do not overstate causality. These are descriptive segments.

## Deliverables

Create or update:

- `scripts/05_profile_segments.py`
- `src/profiling.py`, if useful
- `src/plots.py`, if useful
- `outputs/stage-outputs/05-segment-profiling.md`
- `outputs/tables/05_segment_profile_summary.csv`
- `outputs/tables/05_segment_profile_indexed.csv`
- `outputs/tables/05_segment_response_summary.csv`
- `outputs/tables/05_segment_channel_summary.csv`
- `outputs/tables/05_segment_product_summary.csv`
- `outputs/tables/05_segment_name_recommendations.csv`
- relevant figures in `reports/figures/`

## Output summary

Write a concise markdown summary to:

- `outputs/stage-outputs/05-segment-profiling.md`

The summary should include:

- input files used
- segment assignment source
- row count profiled
- confirmation that the `kmeans_k3` solution was used
- segment sizes
- provisional segment names
- profile of each segment
- key differences between segments
- campaign response differences by segment
- product and channel differences by segment
- caveats
- recommended next steps for the recommendations stage

## Definition of done

- [ ] `python scripts/05_profile_segments.py` runs successfully from the repo root.
- [ ] The script uses the recommended `kmeans_k3` segment assignments from Stage 04.
- [ ] Segment assignments are joined to the engineered dataset by `ID`.
- [ ] Segment profile tables are saved under `outputs/tables/`.
- [ ] Segment figures are saved under `reports/figures/`.
- [ ] A concise review summary is saved to `outputs/stage-outputs/05-segment-profiling.md`.
- [ ] Each segment has a provisional business-friendly name.
- [ ] The summary clearly explains how the segments differ.
- [ ] The output is ready to support Stage 06 marketing recommendations.

## Review notes

The conclusions of the segment profiling stage are sound (and match some of the hypothesised groups after the EDA stage). So:

1. The client should treat these three groups as marketing segments, because they are behaviourally different, have different buying patterns, different underlying priorities, and will respond positively to different styles of campaign. 2. Retitle them: High-value premium buyers, Value-conscious family shoppers, Low-value deal seekers.

2. The segments should be retitled: 0 = High-value premium buyers, 1= Value-conscious family shoppers, 2= Low-value deal seekers.

## Next steps

To move on to recommendations and material for the final report ASAP - running low-ish on time.
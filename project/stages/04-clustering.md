# Stage 04: Clustering

## Status

Completed

## Goal

Create candidate customer segments using two clustering approaches:

1. K-means
2. Gaussian Mixture Models

Compare the results and recommend which clustering solution should be carried forward into segment profiling.

The goal is not just to optimise a statistical metric, but to identify a segmentation that is interpretable, commercially useful, and suitable for marketing recommendations.

## Context

Previous stages created a cleaned and feature-engineered customer dataset.

EDA suggested that useful segmentation themes may include:

- customer value: spend, income, average spend per purchase
- engagement: recency, total purchases, web visits
- channel behaviour: web, catalogue, store, deal share
- product preferences: wine, meat, fish, fruit, sweet, gold shares
- household composition: children / no children
- campaign responsiveness, to be used for evaluation only

Rule:

Do not use campaign response variables to create the clusters. Use them only after clustering to evaluate whether the clusters are commercially useful.

## Inputs

- `data/processed/marketing_campaign_processed_features_engineered.csv`
- `outputs/stage-outputs/03-eda.md`
- `project/decisions.md`

## Instructions for Codex

Complete this stage only.

Create a reproducible clustering script:

- `scripts/04_run_clustering.py`

The script should prepare the data, run K-means and Gaussian Mixture Models, compare candidate solutions, and save reviewable outputs.

## Preprocessing requirements

Prepare a modelling dataset suitable for clustering.

Use customer-level features such as:

- `Age`
- `Income`
- `Customer_Tenure`
- `Recency`
- `Total_Spend`
- `Total_Purchases`
- `Average_Spend_Per_Purchase`
- `NumWebVisitsMonth`
- `Household_Children` or `Has_Children`
- `Web_Purchase_Share`
- `Catalog_Purchase_Share`
- `Store_Purchase_Share`
- `Deal_Purchase_Share`
- product category spend-share features

Do not use these as clustering inputs:

- `ID`
- `Response`
- `AcceptedCmp1`
- `AcceptedCmp2`
- `AcceptedCmp3`
- `AcceptedCmp4`
- `AcceptedCmp5`
- `Campaign_Acceptance_Total`
- `Z_CostContact`
- `Z_Revenue`

Preprocessing should include:

- handle missing values safely
- handle infinite values caused by ratio features
- document any rows dropped, if any
- use `log1p` transformations for highly skewed magnitude features where appropriate, for example:
  - `Income`
  - `Total_Spend`
  - `Total_Purchases`
  - `Average_Spend_Per_Purchase`
  - `NumWebVisitsMonth`
- scale numeric features before clustering
- use a fixed random seed for reproducibility
- save a table listing the final clustering input features

Avoid including both too many raw spend variables and spend-share variables if this creates unnecessary duplication. Prefer a compact, interpretable feature set.

## K-means requirements

Run K-means for candidate cluster counts:

- `k = 3`
- `k = 4`
- `k = 5`
- `k = 6`

For each candidate solution, calculate and save:

- inertia
- silhouette score
- Calinski-Harabasz score
- Davies-Bouldin score
- cluster sizes
- minimum cluster share
- notes on interpretability, if possible

## Gaussian Mixture Model requirements

Run Gaussian Mixture Models for candidate component counts:

- `n_components = 3`
- `n_components = 4`
- `n_components = 5`
- `n_components = 6`

For each candidate solution, calculate and save:

- AIC
- BIC
- silhouette score using hard assignments
- cluster/component sizes
- minimum cluster share
- average maximum assignment probability
- percentage of customers with max assignment probability below 0.60
- percentage of customers with max assignment probability below 0.70

Use the GMM probabilities to assess whether customers are clearly assigned or whether the segmentation is fuzzy.

## Comparison requirements

Compare K-means and GMM outputs.

The comparison should consider:

- statistical metrics
- cluster/component sizes
- interpretability
- whether segments are commercially distinct
- whether GMM soft probabilities add useful information
- whether either method creates very small or unstable-looking clusters

Use campaign response variables only after clusters are created to evaluate the solutions.

For each candidate solution, profile clusters/components using:

- average `Total_Spend`
- average `Income`
- average `Recency`
- average `Total_Purchases`
- average `Average_Spend_Per_Purchase`
- average `Household_Children`
- response rate
- previous campaign acceptance rate or average `Campaign_Acceptance_Total`
- key channel shares
- key product category shares

The output should recommend one solution to carry forward to Stage 05.

This recommendation should be based on both metrics and commercial interpretability.

## Do not

- Do not perform final segment naming.
- Do not write final marketing recommendations.
- Do not use `Response` or previous campaign variables as clustering inputs.
- Do not modify raw data.
- Do not overcomplicate the analysis if a simple solution is clearer.

## Deliverables

Create or update:

- `scripts/04_run_clustering.py`
- `src/clustering.py`, if useful
- `src/plots.py`, if useful
- `outputs/stage-outputs/04-clustering.md`
- `outputs/tables/04_clustering_input_features.csv`
- `outputs/tables/04_kmeans_metrics.csv`
- `outputs/tables/04_gmm_metrics.csv`
- `outputs/tables/04_model_comparison.csv`
- `outputs/tables/04_cluster_profiles.csv`
- `outputs/segment_assignments.csv`
- relevant figures in `reports/figures/`
- model artefacts in `outputs/models/`, if appropriate

Useful figures may include:

- K-means metric comparison by `k`
- GMM AIC/BIC by number of components
- cluster size comparison
- response rate by cluster for the recommended solution
- 2D PCA visualisation of the recommended solution, if useful

## Output summary

Write a concise markdown summary to:

- `outputs/stage-outputs/04-clustering.md`

The summary should include:

- input file used
- row count used for clustering
- preprocessing steps applied
- final clustering features used
- K-means candidate results
- GMM candidate results
- comparison between methods
- recommended solution to carry forward
- reasons for the recommendation
- any risks, caveats, or unresolved issues

## Definition of done

- [ ] `python scripts/04_run_clustering.py` runs successfully from the repo root.
- [ ] Clustering inputs are documented and saved.
- [ ] K-means candidates for 3 to 6 clusters are run and compared.
- [ ] GMM candidates for 3 to 6 components are run and compared.
- [ ] Response variables are excluded from clustering inputs.
- [ ] Response variables are used only for post-clustering evaluation.
- [ ] Metrics and cluster profile tables are saved under `outputs/tables/`.
- [ ] Segment assignments are saved to `outputs/segment_assignments.csv`.
- [ ] A concise review summary is saved to `outputs/stage-outputs/04-clustering.md`.
- [ ] The summary recommends one clustering solution to carry forward to Stage 05.

## Review notes

K means produces three very neat, clear groups, while GMM creates smaller niches.
For this exercise, where clear groups are an advantage (and it's a small toy dataset), let's go with K means.

## Next steps

Segment profiling based on the clustering.
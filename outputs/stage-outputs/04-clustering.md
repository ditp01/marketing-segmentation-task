# Stage 04 Clustering

## Inputs and Row Count
- Input dataset: `C:/dev/marketing-segmentation-task/data/processed/marketing_campaign_processed_features_engineered.csv`
- EDA summary used: `C:/dev/marketing-segmentation-task/outputs/stage-outputs/03-eda.md`
- Decision context file not found: `C:/dev/marketing-segmentation-task/project/decisions.md`.
- Rows used for clustering: 2212

## Preprocessing Applied
- Fixed random seed: `42`
- Candidate base features (before transformation): Age, Income, Customer_Tenure_Years, Recency, Total_Spend, Total_Purchases, Average_Spend_Per_Purchase, NumWebVisitsMonth, Household_Children, Web_Purchase_Share, Catalog_Purchase_Share, Store_Purchase_Share, Deal_Purchase_Share, Wine_Spend_Share, Meat_Spend_Share, Fish_Spend_Share, Fruit_Spend_Share, Sweet_Spend_Share, Gold_Spend_Share
- Explicitly excluded from clustering inputs: ID, Response, AcceptedCmp1, AcceptedCmp2, AcceptedCmp3, AcceptedCmp4, AcceptedCmp5, Campaign_Acceptance_Total, Z_CostContact, Z_Revenue
- `log1p` applied to skewed magnitude features (Income, Total_Spend, Total_Purchases, Average_Spend_Per_Purchase, NumWebVisitsMonth).
- Infinite values replaced with missing and rows with missing model features dropped.
- Dropped rows during preprocessing: 0 (0.00%).
- Numeric model features standardized with `StandardScaler` before KMeans/GMM.

Final clustering input feature table:
```
          feature_original              feature_model_input  log1p_applied  excluded_from_clustering                                                    notes
                       Age                        log1p_Age          False                     False                               Used as-is before scaling.
                    Income                     log1p_Income           True                     False Magnitude feature transformed with log1p to reduce skew.
     Customer_Tenure_Years      log1p_Customer_Tenure_Years          False                     False                               Used as-is before scaling.
                   Recency                    log1p_Recency          False                     False                               Used as-is before scaling.
               Total_Spend                log1p_Total_Spend           True                     False Magnitude feature transformed with log1p to reduce skew.
           Total_Purchases            log1p_Total_Purchases           True                     False Magnitude feature transformed with log1p to reduce skew.
Average_Spend_Per_Purchase log1p_Average_Spend_Per_Purchase           True                     False Magnitude feature transformed with log1p to reduce skew.
         NumWebVisitsMonth          log1p_NumWebVisitsMonth           True                     False Magnitude feature transformed with log1p to reduce skew.
        Household_Children         log1p_Household_Children          False                     False                               Used as-is before scaling.
        Web_Purchase_Share         log1p_Web_Purchase_Share          False                     False                               Used as-is before scaling.
    Catalog_Purchase_Share     log1p_Catalog_Purchase_Share          False                     False                               Used as-is before scaling.
      Store_Purchase_Share       log1p_Store_Purchase_Share          False                     False                               Used as-is before scaling.
       Deal_Purchase_Share        log1p_Deal_Purchase_Share          False                     False                               Used as-is before scaling.
          Wine_Spend_Share           log1p_Wine_Spend_Share          False                     False                               Used as-is before scaling.
          Meat_Spend_Share           log1p_Meat_Spend_Share          False                     False                               Used as-is before scaling.
          Fish_Spend_Share           log1p_Fish_Spend_Share          False                     False                               Used as-is before scaling.
         Fruit_Spend_Share          log1p_Fruit_Spend_Share          False                     False                               Used as-is before scaling.
         Sweet_Spend_Share          log1p_Sweet_Spend_Share          False                     False                               Used as-is before scaling.
          Gold_Spend_Share           log1p_Gold_Spend_Share          False                     False                               Used as-is before scaling.
```

## KMeans Candidate Results
```
method  solution  n_clusters      inertia  silhouette_score  calinski_harabasz_score  davies_bouldin_score         cluster_size_distribution  min_cluster_size  min_cluster_share  response_rate_range  total_spend_mean_range                                              interpretability_note
kmeans kmeans_k3           3 28978.486156          0.163938               497.375465              1.783190                 0:706|1:835|2:671               671           0.303345             0.135277             1165.613813                          Cluster sizes appear reasonably balanced.
kmeans kmeans_k4           4 26533.117082          0.151740               429.811311              1.924084           0:706|1:621|2:490|3:395               395           0.178571             0.167758             1188.105150                          Cluster sizes appear reasonably balanced.
kmeans kmeans_k5           5 24753.045623          0.154022               385.061952              1.548039       0:623|1:387|2:708|3:493|4:1                 1           0.000452             0.235955             1187.918880 Very small cluster detected (<5%): risk of unstable niche segment.
kmeans kmeans_k6           6 23762.354187          0.139917               339.141605              1.658796 0:543|1:334|2:619|3:393|4:322|5:1                 1           0.000452             0.232633             1200.179178 Very small cluster detected (<5%): risk of unstable niche segment.
```

## GMM Candidate Results
```
method solution  n_components          aic         bic  silhouette_score          cluster_size_distribution  min_cluster_size  min_cluster_share  avg_max_assignment_probability  pct_max_assignment_prob_below_0_60  pct_max_assignment_prob_below_0_70  response_rate_range  total_spend_mean_range                                              interpretability_note
   gmm   gmm_n3             3  6173.571805 9759.911141          0.207744                  0:21|1:1208|2:983                21           0.009494                        0.993138                            0.180832                            0.813743             0.201987              939.141133 Very small cluster detected (<5%): risk of unstable niche segment.
   gmm   gmm_n4             4  2591.643865 7375.330197          0.113400             0:712|1:825|2:646|3:29                29           0.013110                        0.985299                            0.994575                            2.034358             0.212768             1327.126344 Very small cluster detected (<5%): risk of unstable niche segment.
   gmm   gmm_n5             5 -1553.864225 4427.169103          0.091514       0:752|1:482|2:478|3:481|4:19                19           0.008590                        0.985260                            0.858951                            1.537071             0.317427             1325.339294 Very small cluster detected (<5%): risk of unstable niche segment.
   gmm   gmm_n6             6 -6240.360745  938.019579          0.071727 0:385|1:666|2:123|3:592|4:70|5:376                70           0.031646                        0.986285                            0.904159                            1.582278             0.303896             1403.162053 Very small cluster detected (<5%): risk of unstable niche segment.
```

## Model Comparison
```
method  solution  model_complexity  silhouette_score  min_cluster_share  response_rate_range  total_spend_mean_range  davies_bouldin_score  calinski_harabasz_score      inertia          aic         bic  avg_max_assignment_probability  pct_max_assignment_prob_below_0_70                                              interpretability_note  composite_score  overall_rank  method_rank  recommended_solution
kmeans kmeans_k3                 3          0.163938           0.303345             0.135277             1165.613813              1.783190               497.375465 28978.486156          NaN         NaN                             NaN                                 NaN                          Cluster sizes appear reasonably balanced.         5.540676             1            1                  True
kmeans kmeans_k5                 5          0.154022           0.000452             0.235955             1187.918880              1.548039               385.061952 24753.045623          NaN         NaN                             NaN                                 NaN Very small cluster detected (<5%): risk of unstable niche segment.         4.984096             2            2                 False
   gmm    gmm_n6                 6          0.071727           0.031646             0.303896             1403.162053                   NaN                      NaN          NaN -6240.360745  938.019579                        0.986285                            1.582278 Very small cluster detected (<5%): risk of unstable niche segment.         4.529204             3            1                 False
kmeans kmeans_k4                 4          0.151740           0.178571             0.167758             1188.105150              1.924084               429.811311 26533.117082          NaN         NaN                             NaN                                 NaN                          Cluster sizes appear reasonably balanced.         4.464181             4            3                 False
   gmm    gmm_n3                 3          0.207744           0.009494             0.201987              939.141133                   NaN                      NaN          NaN  6173.571805 9759.911141                        0.993138                            0.813743 Very small cluster detected (<5%): risk of unstable niche segment.         4.396087             5            2                 False
kmeans kmeans_k6                 6          0.139917           0.000452             0.232633             1200.179178              1.658796               339.141605 23762.354187          NaN         NaN                             NaN                                 NaN Very small cluster detected (<5%): risk of unstable niche segment.         4.303844             6            4                 False
   gmm    gmm_n5                 5          0.091514           0.008590             0.317427             1325.339294                   NaN                      NaN          NaN -1553.864225 4427.169103                        0.985260                            1.537071 Very small cluster detected (<5%): risk of unstable niche segment.         4.016524             7            3                 False
   gmm    gmm_n4                 4          0.113400           0.013110             0.212768             1327.126344                   NaN                      NaN          NaN  2591.643865 7375.330197                        0.985299                            2.034358 Very small cluster detected (<5%): risk of unstable niche segment.         2.884958             8            4                 False
```

KMeans vs GMM comparison notes:
- Best KMeans candidate: `kmeans_k3` | silhouette `0.1639` | min cluster share `30.33%`.
- Best GMM candidate: `gmm_n6` | silhouette `0.0717` | min cluster share `3.16%`.
- GMM assignment certainty (best GMM): avg max probability `0.9863`, below 0.70 for `1.58%` of customers.
- GMM produced smaller niche components across candidates, while KMeans offered more balanced cluster sizes for practical campaign targeting.

## Recommended Solution
- Recommended method: `kmeans`
- Recommended solution: `kmeans_k3`
- Composite score: 5.5407
- Silhouette score: 0.1639
- Minimum cluster share: 30.33%
- Response-rate range across clusters: 13.53 percentage points
- Total spend mean range across clusters: 1165.61
- Interpretability note: Cluster sizes appear reasonably balanced.

Recommended solution profile table:
```
method  solution  cluster  cluster_size  cluster_share  avg_Total_Spend   avg_Income  avg_Recency  avg_Total_Purchases  avg_Average_Spend_Per_Purchase  avg_Household_Children  avg_Response  avg_Campaign_Acceptance_Total  avg_Web_Purchase_Share  avg_Catalog_Purchase_Share  avg_Store_Purchase_Share  avg_Deal_Purchase_Share  avg_Wine_Spend_Share  avg_Meat_Spend_Share  avg_Fish_Spend_Share  avg_Fruit_Spend_Share  avg_Sweet_Spend_Share  avg_Gold_Spend_Share
kmeans kmeans_k3        0           706       0.319168      1243.060907 73225.791785    49.930595            19.172805                       66.279618                0.338527      0.235127                       0.562323                0.266452                    0.293901                  0.439647                 0.085334              0.424960              0.317300              0.078451               0.055614               0.058132              0.065543
kmeans kmeans_k3        1           835       0.377486       495.459880 51905.653892    47.802395            12.856287                       32.762340                1.349701      0.119760                       0.257485                0.384164                    0.133965                  0.481871                 0.290710              0.653975              0.182527              0.028940               0.020784               0.020074              0.093700
kmeans kmeans_k3        2           671       0.303345        77.447094 29648.672131    49.575261             5.256334                       12.947394                1.087928      0.099851                       0.071535                0.325643                    0.067134                  0.598281                 0.362542              0.252221              0.260183              0.117519               0.078677               0.081287              0.210114
```

## Risks and Caveats
- No major preprocessing or stability risks identified for the recommended solution.

## Generated Figures
- `C:/dev/marketing-segmentation-task/reports/figures/04_kmeans_metric_comparison.png`
- `C:/dev/marketing-segmentation-task/reports/figures/04_gmm_aic_bic.png`
- `C:/dev/marketing-segmentation-task/reports/figures/04_recommended_cluster_size_share.png`
- `C:/dev/marketing-segmentation-task/reports/figures/04_recommended_response_rate_by_cluster.png`
- `C:/dev/marketing-segmentation-task/reports/figures/04_recommended_pca_scatter.png`

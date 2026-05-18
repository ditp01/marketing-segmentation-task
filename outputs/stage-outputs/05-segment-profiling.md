# Stage 05 Segment Profiling

## Inputs Used
- Engineered dataset: `C:/dev/marketing-segmentation-task/data/processed/marketing_campaign_processed_features_engineered.csv`
- Segment assignments: `C:/dev/marketing-segmentation-task/outputs/segment_assignments.csv`
- Stage 04 summary: `C:/dev/marketing-segmentation-task/outputs/stage-outputs/04-clustering.md`
- Segment assignment source: `kmeans` / `kmeans_k3` from Stage 04.
- Row count profiled: 2212

## Segment Size Summary
```
 segment_id  customer_count  customer_share_pct
          0             706           31.916817
          1             835           37.748644
          2             671           30.334539
```

## Provisional Segment Names
```
 segment_id         provisional_segment_name  size_share_pct value_level  response_rate_pct          response_level                                              channel_behaviour_summary                         product_preference_summary                                             defining_characteristics                                                                           risks_or_caveats
          0      Affluent Premium Responders       31.916817  High value          23.512748     High responsiveness Web share 0.27, catalog share 0.29, store share 0.44, deal share 0.09. Wine share 0.42, meat share 0.32, gold share 0.07. Income 73226, total spend 1243, purchases 19.2, children rate 32.2%. Profile is descriptive only; validate stability with future data and campaign experiments.
          1     Mid-Value Family Wine Buyers       37.748644   Mid value          11.976048 Moderate responsiveness Web share 0.38, catalog share 0.13, store share 0.48, deal share 0.29. Wine share 0.65, meat share 0.18, gold share 0.09.  Income 51906, total spend 495, purchases 12.9, children rate 95.2%. Profile is descriptive only; validate stability with future data and campaign experiments.
          2 Low-Value Deal-Oriented Shoppers       30.334539   Low value           9.985097      Low responsiveness Web share 0.33, catalog share 0.07, store share 0.60, deal share 0.36. Wine share 0.25, meat share 0.26, gold share 0.21.    Income 29649, total spend 77, purchases 5.3, children rate 83.2%. Profile is descriptive only; validate stability with future data and campaign experiments.
```

## Absolute Segment Profile
```
 segment_id  customer_count   avg_income  median_income  avg_total_spend  median_total_spend  avg_total_purchases  median_total_purchases  avg_spend_per_purchase  median_spend_per_purchase  avg_recency   avg_age  avg_customer_tenure_years  avg_household_children  pct_with_children  response_rate_pct  avg_campaign_acceptance_total  pct_any_previous_campaign_acceptance  complaint_rate_pct  avg_web_purchase_share  avg_catalog_purchase_share  avg_store_purchase_share  avg_deal_purchase_share  avg_num_web_purchases  avg_num_catalog_purchases  avg_num_store_purchases  avg_num_web_visits_month  avg_mnt_wines  avg_mnt_fruits  avg_mnt_meat_products  avg_mnt_fish_products  avg_mnt_sweet_products  avg_mnt_gold_prods  avg_wine_spend_share  avg_meat_spend_share  avg_fish_spend_share  avg_fruit_spend_share  avg_sweet_spend_share  avg_gold_spend_share  customer_share_pct  rank_total_spend_desc  rank_income_desc  rank_response_rate_desc  rank_total_purchases_desc  rank_deal_share_desc
          0             706 73225.791785        73452.0      1243.060907              1196.0            19.172805                    19.0               66.279618                  68.348485    49.930595 46.196884                   0.954835                0.338527          32.152975          23.512748                       0.562323                             33.569405            0.849858                0.266452                    0.293901                  0.439647                 0.085334               5.107649                   5.689802                 8.375354                  2.964589     545.586402       62.682720             407.050992              90.164306               64.691218           72.885269              0.424960              0.317300              0.078451               0.055614               0.058132              0.065543           31.916817                      1                 1                        1                          1                     3
          1             835 51905.653892        51287.0       495.459880               393.0            12.856287                    13.0               32.762340                  29.384615    47.802395 48.411976                   1.016880                1.349701          95.209581          11.976048                       0.257485                             20.718563            0.718563                0.384164                    0.133965                  0.481871                 0.290710               5.008383                   1.953293                 5.894611                  6.256287     333.578443       11.540120              82.405988              15.382036               11.285030           41.268263              0.653975              0.182527              0.028940               0.020784               0.020074              0.093700           37.748644                      2                 2                        2                          2                     2
          2             671 29648.672131        29298.0        77.447094                53.0             5.256334                     5.0               12.947394                  10.750000    49.575261 39.779434                   0.922399                1.087928          83.159463           9.985097                       0.071535                              7.153502            1.192250                0.325643                    0.067134                  0.598281                 0.362542               1.870343                   0.391952                 2.994039                  6.637854      17.248882        6.484352              19.795827              10.102832                7.052161           16.763040              0.252221              0.260183              0.117519               0.078677               0.081287              0.210114           30.334539                      3                 3                        3                          3                     1
```

## Indexed Segment Profile (Overall = 100)
```
                    metric  overall_value  segment_0_value  segment_0_index  segment_1_value  segment_1_index  segment_2_value  segment_2_index
                    Income   51958.810579     73225.791785       140.930462     51905.653892        99.897695     29648.672131        57.061876
               Total_Spend     607.268083      1243.060907       204.697224       495.459880        81.588329        77.447094        12.753361
           Total_Purchases      12.566908        19.172805       152.565809        12.856287       102.302712         5.256334        41.826788
Average_Spend_Per_Purchase      37.449216        66.279618       176.985329        32.762340        87.484717        12.947394        34.573204
         Response_Rate_Pct      15.157964        23.512748       155.118112        11.976048        79.008287         9.985097        65.873601
    Catalog_Purchase_Share       0.164739         0.293901       178.404208         0.133965        81.319840         0.067134        40.751957
       Deal_Purchase_Share       0.246951         0.085334        34.555035         0.290710       117.719984         0.362542       146.807689
        Household_Children       0.947559         0.338527        35.726218         1.349701       142.439777         1.087928       114.813825
```

## Response and Campaign Summary
```
 segment_id  customer_count  customer_share_pct  response_rate_pct  avg_campaign_acceptance_total  pct_any_previous_campaign_acceptance  complaint_rate_pct  AcceptedCmp1_rate_pct  AcceptedCmp2_rate_pct  AcceptedCmp3_rate_pct  AcceptedCmp4_rate_pct  AcceptedCmp5_rate_pct
          0             706           31.916817          23.512748                       0.562323                             33.569405            0.849858              16.572238               2.266289               7.365439              10.056657              19.971671
          1             835           37.748644          11.976048                       0.257485                             20.718563            0.718563               2.994012               1.676647               7.544910              11.137725               2.395210
          2             671           30.334539           9.985097                       0.071535                              7.153502            1.192250               0.000000               0.000000               7.153502               0.000000               0.000000
```

## Channel Mix Summary
```
 segment_id  avg_web_purchase_share  avg_catalog_purchase_share  avg_store_purchase_share  avg_deal_purchase_share  avg_num_web_purchases  avg_num_catalog_purchases  avg_num_store_purchases  avg_num_web_visits_month
          0                0.266452                    0.293901                  0.439647                 0.085334               5.107649                   5.689802                 8.375354                  2.964589
          1                0.384164                    0.133965                  0.481871                 0.290710               5.008383                   1.953293                 5.894611                  6.256287
          2                0.325643                    0.067134                  0.598281                 0.362542               1.870343                   0.391952                 2.994039                  6.637854
```

## Product Preference Summary
```
 segment_id  avg_mnt_wines  avg_mnt_fruits  avg_mnt_meat_products  avg_mnt_fish_products  avg_mnt_sweet_products  avg_mnt_gold_prods  avg_wine_spend_share  avg_fruit_spend_share  avg_meat_spend_share  avg_fish_spend_share  avg_sweet_spend_share  avg_gold_spend_share top_category_by_avg_spend top_category_by_spend_share
          0     545.586402       62.682720             407.050992              90.164306               64.691218           72.885269              0.424960               0.055614              0.317300              0.078451               0.058132              0.065543                      wine                        wine
          1     333.578443       11.540120              82.405988              15.382036               11.285030           41.268263              0.653975               0.020784              0.182527              0.028940               0.020074              0.093700                      wine                        wine
          2      17.248882        6.484352              19.795827              10.102832                7.052161           16.763040              0.252221               0.078677              0.260183              0.117519               0.081287              0.210114                      meat                        meat
```

## Segment Narratives
### Segment 0: Affluent Premium Responders
- Size/share: 706 customers (31.92%).
- Defining characteristics: income 73226, total spend 1243, total purchases 19.2, household children 0.34.
- Value level: High value.
- Responsiveness: Higher responsiveness (response rate 23.51%, avg campaign acceptance total 0.56).
- Channel behaviour: web 0.27, catalog 0.29, store 0.44, deal 0.09.
- Product preferences: top category by avg spend `wine`, top by spend share `wine`.
- Caveat: Profile is descriptive only; validate stability with future data and campaign experiments.

### Segment 1: Mid-Value Family Wine Buyers
- Size/share: 835 customers (37.75%).
- Defining characteristics: income 51906, total spend 495, total purchases 12.9, household children 1.35.
- Value level: Mid value.
- Responsiveness: Moderate responsiveness (response rate 11.98%, avg campaign acceptance total 0.26).
- Channel behaviour: web 0.38, catalog 0.13, store 0.48, deal 0.29.
- Product preferences: top category by avg spend `wine`, top by spend share `wine`.
- Caveat: Profile is descriptive only; validate stability with future data and campaign experiments.

### Segment 2: Low-Value Deal-Oriented Shoppers
- Size/share: 671 customers (30.33%).
- Defining characteristics: income 29649, total spend 77, total purchases 5.3, household children 1.09.
- Value level: Low value.
- Responsiveness: Lower responsiveness (response rate 9.99%, avg campaign acceptance total 0.07).
- Channel behaviour: web 0.33, catalog 0.07, store 0.60, deal 0.36.
- Product preferences: top category by avg spend `meat`, top by spend share `meat`.
- Caveat: Profile is descriptive only; validate stability with future data and campaign experiments.

## Key Differences Across Segments
- Response-rate spread: 13.53 percentage points.
- Average total spend spread: 1165.61.
- Deal-share spread: 0.28.
- Segments differ materially on value, household composition, channel mix, and campaign responsiveness.

## Caveats
- Segment labels are provisional and descriptive, not causal.
- Profiles are based on one dataset snapshot and should be validated with future campaign outcomes.

## Recommended Next Steps for Stage 06
- Translate each segment profile into targeted campaign objectives and message strategies.
- Prioritise segments by expected commercial uplift and execution feasibility.
- Define segment-specific channel and offer hypotheses to test.

## Generated Figures
- `C:/dev/marketing-segmentation-task/reports/figures/05_segment_size_share.png`
- `C:/dev/marketing-segmentation-task/reports/figures/05_avg_total_spend_by_segment.png`
- `C:/dev/marketing-segmentation-task/reports/figures/05_response_rate_by_segment.png`
- `C:/dev/marketing-segmentation-task/reports/figures/05_income_vs_spend_by_segment.png`
- `C:/dev/marketing-segmentation-task/reports/figures/05_channel_share_by_segment.png`
- `C:/dev/marketing-segmentation-task/reports/figures/05_product_spend_share_by_segment.png`
- `C:/dev/marketing-segmentation-task/reports/figures/05_children_rate_by_segment.png`

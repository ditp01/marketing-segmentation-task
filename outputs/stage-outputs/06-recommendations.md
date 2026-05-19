# Stage 06 Recommendations

## Inputs Used
- `C:/dev/marketing-segmentation-task/outputs/stage-outputs/05-segment-profiling.md`
- `C:/dev/marketing-segmentation-task/outputs/tables/05_segment_profile_summary.csv`
- `C:/dev/marketing-segmentation-task/outputs/tables/05_segment_response_summary.csv`
- `C:/dev/marketing-segmentation-task/outputs/tables/05_segment_channel_summary.csv`
- `C:/dev/marketing-segmentation-task/outputs/tables/05_segment_product_summary.csv`

## Overall Recommendation
- Use the three identified K-means groups as operational marketing segments.
- Apply fixed segment names: Segment 0 = High-Value Premium Buyers, Segment 1 = Value-Conscious Family Shoppers, Segment 2 = Low-Value Deal Seekers.
- Prioritise Segment 0 for high-margin growth, Segment 1 for basket-size expansion, and Segment 2 for selective low-cost reactivation.

## Why These Three Segments Should Be Used
- Average total spend differs by 16.1x between highest- and lowest-value segments.
- Response rate spread is 13.52 percentage points across segments.
- Deal purchase share spread is 27.72 percentage points, indicating materially different price sensitivity.
- Profiles also differ on channel usage and product category mix, supporting differentiated campaign treatment.

Evidence snapshot:
```
 segment_id                    segment_name  customer_count customer_share_pct avg_total_spend avg_total_purchases response_rate_pct deal_purchase_share_pct
          0       High-Value Premium Buyers             706             31.92%          1243.1                19.2            23.51%                   8.53%
          1 Value-Conscious Family Shoppers             835             37.75%           495.5                12.9            11.98%                  29.07%
          2          Low-Value Deal Seekers             671             30.33%            77.4                 5.3             9.99%                  36.25%
```

## Recommendation Matrix
```
                              segment_name                                                                     short_segment_description                                                                marketing_objective                                                                                   messaging_strategy                                                                                                 offer_strategy                                                                          channel_strategy                                                      product_focus                                                                         suggested_kpis
      Segment 0: High-Value Premium Buyers            Highest-value segment with strong spend, high response, and low reliance on deals.                       Protect and grow high-margin revenue from premium loyalists.            Use premium, quality-led messaging centered on provenance, exclusivity, and early access.                            Prioritise personalised premium bundles and loyalty perks; avoid broad discounting. Lead with catalog/direct and store support, backed by targeted email and web retargeting.                 Wine, meat, premium bundles, and exclusive ranges.    Response >= 24.0%, Avg spend >= 1250.0, Deal share target <= 10.0% (baseline 8.5%).
Segment 1: Value-Conscious Family Shoppers Mid-value family segment with solid spend and moderate response, but higher deal sensitivity.       Grow basket value and frequency without over-subsidising existing purchases. Use practical value messaging: family bundles, convenience, multi-buy, and seasonal household needs.                       Use targeted discounts and bundle offers to drive basket growth, not blanket price cuts.                    Prioritise web and store journeys, with selective promotional support.    Wine-led baskets, family bundles, and household meal solutions. Response >= 13.0%, Avg spend >= 545.0, Deal share target 28.0%-33.0% (baseline 29.1%).
         Segment 2: Low-Value Deal Seekers                Low-value, price-sensitive segment with low response and high deal dependence. Defend profitability while selectively reactivating commercially viable customers.                               Use simple, deal-led reactivation messaging with clear everyday value. Limit activity to low-cost automated campaigns and entry-level promotions where incremental gain is plausible.                          Focus on store-led promotions and low-cost digital reactivation. Entry-level bundles, meat/value essentials, and promotional packs.  Response >= 10.5%, Avg spend >= 90.0, Deal share target 34.0%-40.0% (baseline 36.3%).
```

## KPI Guidance
```
                              segment_name                            kpi_name                            baseline_value                                                           target_guidance                    data_status                                                                 notes
      Segment 0: High-Value Premium Buyers                       response_rate                                     23.5%                                                                  >= 24.0%           available_in_dataset                     Directly observed from stage-05 response summary.
      Segment 0: High-Value Premium Buyers                 average_total_spend                                    1243.1                                                                 >= 1250.0           available_in_dataset                                     Use as core commercial value KPI.
      Segment 0: High-Value Premium Buyers          average_spend_per_purchase                                      66.3                                                                   >= 67.0           available_in_dataset              Useful for testing premium or bundle positioning impact.
      Segment 0: High-Value Premium Buyers                      purchase_count                                      19.2                                                                   >= 19.5           available_in_dataset                            Proxy for frequency and repeat engagement.
      Segment 0: High-Value Premium Buyers                         channel_mix   Web 26.6% | Catalog 29.4% | Store 44.0%                                        Catalog + Store >= 72%; Web 24-30%           available_in_dataset         Channel shares indicate preferred route to market by segment.
      Segment 0: High-Value Premium Buyers              product_category_spend       Wine 545.6 | Meat 407.1 | Gold 72.9                                           Wine >= 550.0 and Meat >= 410.0           available_in_dataset           Category mix helps align assortment and messaging strategy.
      Segment 0: High-Value Premium Buyers                 deal_purchase_share                                      8.5%                                                                  <= 10.0%           available_in_dataset                           Tracks discount dependency and margin risk.
      Segment 0: High-Value Premium Buyers            campaign_acceptance_rate                                      0.56                                                                   >= 0.60           available_in_dataset         Average accepted campaigns per customer from historical data.
      Segment 0: High-Value Premium Buyers                      complaint_rate                                     0.85%                                                                   <= 1.0%           available_in_dataset Safeguard to prevent value strategy from harming customer experience.
      Segment 0: High-Value Premium Buyers                             recency                                 49.9 days                                                              <= 50.0 days           available_in_dataset              Lower recency indicates more recent purchasing activity.
      Segment 0: High-Value Premium Buyers incremental_spend_uplift_vs_holdout      Not available in historical snapshot >= +5% incremental spend vs holdout with no deal-share increase above 1pp provisional_requires_more_data            Requires controlled holdout test to isolate causal uplift.
      Segment 0: High-Value Premium Buyers     net_margin_per_discounted_order Not available (cost/margin inputs absent)                         Maintain positive net margin per discounted order provisional_requires_more_data          Requires COGS, discount depth, and contribution margin data.
Segment 1: Value-Conscious Family Shoppers                       response_rate                                     12.0%                                                                  >= 13.0%           available_in_dataset                     Directly observed from stage-05 response summary.
Segment 1: Value-Conscious Family Shoppers                 average_total_spend                                     495.5                                                                  >= 545.0           available_in_dataset                                     Use as core commercial value KPI.
Segment 1: Value-Conscious Family Shoppers          average_spend_per_purchase                                      32.8                                                                   >= 35.0           available_in_dataset              Useful for testing premium or bundle positioning impact.
Segment 1: Value-Conscious Family Shoppers                      purchase_count                                      12.9                                                                   >= 13.5           available_in_dataset                            Proxy for frequency and repeat engagement.
Segment 1: Value-Conscious Family Shoppers                         channel_mix   Web 38.4% | Catalog 13.4% | Store 48.2%                                        Web + Store >= 84%; Catalog 10-16%           available_in_dataset         Channel shares indicate preferred route to market by segment.
Segment 1: Value-Conscious Family Shoppers              product_category_spend        Wine 333.6 | Meat 82.4 | Gold 41.3                                            Wine >= 340.0 and Meat >= 90.0           available_in_dataset           Category mix helps align assortment and messaging strategy.
Segment 1: Value-Conscious Family Shoppers                 deal_purchase_share                                     29.1%                                                               28.0%-33.0%           available_in_dataset                           Tracks discount dependency and margin risk.
Segment 1: Value-Conscious Family Shoppers            campaign_acceptance_rate                                      0.26                                                                   >= 0.30           available_in_dataset         Average accepted campaigns per customer from historical data.
Segment 1: Value-Conscious Family Shoppers                      complaint_rate                                     0.72%                                                                   <= 1.0%           available_in_dataset Safeguard to prevent value strategy from harming customer experience.
Segment 1: Value-Conscious Family Shoppers                             recency                                 47.8 days                                                              <= 45.0 days           available_in_dataset              Lower recency indicates more recent purchasing activity.
Segment 1: Value-Conscious Family Shoppers incremental_spend_uplift_vs_holdout      Not available in historical snapshot            >= +8% incremental basket value vs holdout in promoted cohorts provisional_requires_more_data            Requires controlled holdout test to isolate causal uplift.
Segment 1: Value-Conscious Family Shoppers     net_margin_per_discounted_order Not available (cost/margin inputs absent)                  Promotions must deliver non-negative gross margin uplift provisional_requires_more_data          Requires COGS, discount depth, and contribution margin data.
         Segment 2: Low-Value Deal Seekers                       response_rate                                     10.0%                                                                  >= 10.5%           available_in_dataset                     Directly observed from stage-05 response summary.
         Segment 2: Low-Value Deal Seekers                 average_total_spend                                      77.4                                                                   >= 90.0           available_in_dataset                                     Use as core commercial value KPI.
         Segment 2: Low-Value Deal Seekers          average_spend_per_purchase                                      12.9                                                                   >= 13.5           available_in_dataset              Useful for testing premium or bundle positioning impact.
         Segment 2: Low-Value Deal Seekers                      purchase_count                                       5.3                                                                    >= 5.8           available_in_dataset                            Proxy for frequency and repeat engagement.
         Segment 2: Low-Value Deal Seekers                         channel_mix    Web 32.6% | Catalog 6.7% | Store 59.8%                                  Store >= 58%; Catalog <= 10%; Web 28-35%           available_in_dataset         Channel shares indicate preferred route to market by segment.
         Segment 2: Low-Value Deal Seekers              product_category_spend         Wine 17.2 | Meat 19.8 | Gold 16.8                                             Meat >= 22.0 and Wine >= 20.0           available_in_dataset           Category mix helps align assortment and messaging strategy.
         Segment 2: Low-Value Deal Seekers                 deal_purchase_share                                     36.3%                                                               34.0%-40.0%           available_in_dataset                           Tracks discount dependency and margin risk.
         Segment 2: Low-Value Deal Seekers            campaign_acceptance_rate                                      0.07                                                                   >= 0.09           available_in_dataset         Average accepted campaigns per customer from historical data.
         Segment 2: Low-Value Deal Seekers                      complaint_rate                                     1.19%                                                                   <= 1.5%           available_in_dataset Safeguard to prevent value strategy from harming customer experience.
         Segment 2: Low-Value Deal Seekers                             recency                                 49.6 days                                                              <= 48.0 days           available_in_dataset              Lower recency indicates more recent purchasing activity.
         Segment 2: Low-Value Deal Seekers incremental_spend_uplift_vs_holdout      Not available in historical snapshot                >= +10% incremental spend in contacted reactivation cohort provisional_requires_more_data            Requires controlled holdout test to isolate causal uplift.
         Segment 2: Low-Value Deal Seekers     net_margin_per_discounted_order Not available (cost/margin inputs absent)       Discount activity should be retained only if net margin is positive provisional_requires_more_data          Requires COGS, discount depth, and contribution margin data.
```

KPI data availability split:
```
                   data_status  kpi_count
          available_in_dataset         30
provisional_requires_more_data          6
```

## Limitations
- Segment profiles are descriptive and based on one historical data snapshot; they are not causal proof.
- Incrementality and profitability KPIs are provisional until holdout testing and margin data are available.
- Recommended targets should be tuned after first campaign test cycles by segment.

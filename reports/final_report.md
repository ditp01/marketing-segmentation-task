# Marketing Segmentation Final Report

Generated on: 2026-05-19

## Executive Summary
- Three behaviourally distinct customer segments were identified and should be used as the go-forward campaign segmentation framework.
- Segment 0 (High-Value Premium Buyers) should receive premium-led, low-discount treatment to protect margin and grow high-value revenue.
- Segment 1 (Value-Conscious Family Shoppers) should receive practical value and bundle-led propositions to increase basket size and purchase frequency.
- Segment 2 (Low-Value Deal Seekers) should be managed with selective low-cost reactivation and strict profitability controls.

## Segment Evidence Snapshot
| segment_id | segment_name | customer_count | customer_share_pct | avg_total_spend | avg_total_purchases | response_rate_pct | deal_purchase_share_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | High-Value Premium Buyers | 706 | 31.92% | 1243.1 | 19.2 | 23.51% | 8.53% |
| 1 | Value-Conscious Family Shoppers | 835 | 37.75% | 495.5 | 12.9 | 11.98% | 29.07% |
| 2 | Low-Value Deal Seekers | 671 | 30.33% | 77.4 | 5.3 | 9.99% | 36.25% |

## Recommendation Matrix
| segment_name | short_segment_description | marketing_objective | messaging_strategy | offer_strategy | channel_strategy | product_focus | suggested_kpis |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Segment 0: High-Value Premium Buyers | Highest-value segment with strong spend, high response, and low reliance on deals. | Protect and grow high-margin revenue from premium loyalists. | Use premium, quality-led messaging centered on provenance, exclusivity, and early access. | Prioritise personalised premium bundles and loyalty perks; avoid broad discounting. | Lead with catalog/direct and store support, backed by targeted email and web retargeting. | Wine, meat, premium bundles, and exclusive ranges. | Response >= 24.0%, Avg spend >= 1250.0, Deal share target <= 10.0% (baseline 8.5%). |
| Segment 1: Value-Conscious Family Shoppers | Mid-value family segment with solid spend and moderate response, but higher deal sensitivity. | Grow basket value and frequency without over-subsidising existing purchases. | Use practical value messaging: family bundles, convenience, multi-buy, and seasonal household needs. | Use targeted discounts and bundle offers to drive basket growth, not blanket price cuts. | Prioritise web and store journeys, with selective promotional support. | Wine-led baskets, family bundles, and household meal solutions. | Response >= 13.0%, Avg spend >= 545.0, Deal share target 28.0%-33.0% (baseline 29.1%). |
| Segment 2: Low-Value Deal Seekers | Low-value, price-sensitive segment with low response and high deal dependence. | Defend profitability while selectively reactivating commercially viable customers. | Use simple, deal-led reactivation messaging with clear everyday value. | Limit activity to low-cost automated campaigns and entry-level promotions where incremental gain is plausible. | Focus on store-led promotions and low-cost digital reactivation. | Entry-level bundles, meat/value essentials, and promotional packs. | Response >= 10.5%, Avg spend >= 90.0, Deal share target 34.0%-40.0% (baseline 36.3%). |

## KPI Plan
Priority KPI targets:
| segment_name | kpi_name | baseline_value | target_guidance | data_status | notes |
| --- | --- | --- | --- | --- | --- |
| Segment 0: High-Value Premium Buyers | response_rate | 23.5% | >= 24.0% | available_in_dataset | Directly observed from stage-05 response summary. |
| Segment 0: High-Value Premium Buyers | average_total_spend | 1243.1 | >= 1250.0 | available_in_dataset | Use as core commercial value KPI. |
| Segment 0: High-Value Premium Buyers | deal_purchase_share | 8.5% | <= 10.0% | available_in_dataset | Tracks discount dependency and margin risk. |
| Segment 0: High-Value Premium Buyers | campaign_acceptance_rate | 0.56 | >= 0.60 | available_in_dataset | Average accepted campaigns per customer from historical data. |
| Segment 0: High-Value Premium Buyers | complaint_rate | 0.85% | <= 1.0% | available_in_dataset | Safeguard to prevent value strategy from harming customer experience. |
| Segment 1: Value-Conscious Family Shoppers | response_rate | 12.0% | >= 13.0% | available_in_dataset | Directly observed from stage-05 response summary. |
| Segment 1: Value-Conscious Family Shoppers | average_total_spend | 495.5 | >= 545.0 | available_in_dataset | Use as core commercial value KPI. |
| Segment 1: Value-Conscious Family Shoppers | deal_purchase_share | 29.1% | 28.0%-33.0% | available_in_dataset | Tracks discount dependency and margin risk. |
| Segment 1: Value-Conscious Family Shoppers | campaign_acceptance_rate | 0.26 | >= 0.30 | available_in_dataset | Average accepted campaigns per customer from historical data. |
| Segment 1: Value-Conscious Family Shoppers | complaint_rate | 0.72% | <= 1.0% | available_in_dataset | Safeguard to prevent value strategy from harming customer experience. |
| Segment 2: Low-Value Deal Seekers | response_rate | 10.0% | >= 10.5% | available_in_dataset | Directly observed from stage-05 response summary. |
| Segment 2: Low-Value Deal Seekers | average_total_spend | 77.4 | >= 90.0 | available_in_dataset | Use as core commercial value KPI. |
| Segment 2: Low-Value Deal Seekers | deal_purchase_share | 36.3% | 34.0%-40.0% | available_in_dataset | Tracks discount dependency and margin risk. |
| Segment 2: Low-Value Deal Seekers | campaign_acceptance_rate | 0.07 | >= 0.09 | available_in_dataset | Average accepted campaigns per customer from historical data. |
| Segment 2: Low-Value Deal Seekers | complaint_rate | 1.19% | <= 1.5% | available_in_dataset | Safeguard to prevent value strategy from harming customer experience. |

KPI availability split:
| data_status | kpi_count |
| --- | --- |
| available_in_dataset | 30 |
| provisional_requires_more_data | 6 |

## Limitations and Controls
- Profiles and KPI baselines are historical and descriptive; they should be validated through campaign experiments.
- Incremental uplift and net margin KPIs are provisional until holdout-test outcomes and cost/margin data are integrated.
- To avoid over-discounting, deal-led tactics should be monitored with margin guardrails by segment.

## Recommended Next Actions
1. Launch segmented campaign pilots for each segment with explicit holdout groups.
2. Track KPI movement weekly against the segment-specific targets in `outputs/tables/06_kpi_guidance.csv`.
3. Recalibrate targets after the first campaign cycle using observed incremental and margin outcomes.

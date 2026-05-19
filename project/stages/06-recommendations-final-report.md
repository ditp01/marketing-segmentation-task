# Stage 6: Recommendations and Final Report

## Status

Not started

## Goal

The goal of this stage is to take the conclusion of the analysis so far - the segment profiling - and produce recommendations and a draft of a final report, following the context and guidance below.

## Context

The analysis up to this point has pretty clearly pointed us towards three segments. Now, based on the analysis generated in previous steps, we need to consolidate this information into a draft set of recommendation tables for evaluation and further use in client-facing material.

Stage 05 profiled three recommended K-means customer segments - read that stage outputs before proceeding.

Use the following final segment names:

- Segment 0: High-Value Premium Buyers
- Segment 1: Value-Conscious Family Shoppers
- Segment 2: Low-Value Deal Seekers

## Inputs

- `outputs/stage-outputs/05-segment-profiling.md`
- `outputs/tables/05_segment_profile_summary.csv`
- `outputs/tables/05_segment_response_summary.csv`
- `outputs/tables/05_segment_channel_summary.csv`
- `outputs/tables/05_segment_product_summary.csv`

## Instructions for Codex

Complete this stage only.

The conclusions of the segment profiling stage are sound (and match some of the hypothesised groups after the EDA stage). So:

1. The client should treat these three groups as marketing segments, because they are behaviourally different, have different buying patterns, different underlying priorities, and will respond positively to different styles of campaign. 2. Retitle them: High-value premium buyers, Value-conscious family shoppers, Low-value deal seekers.

2. The segments should be retitled: 0 = High-value premium buyers, 1= Value-conscious family shoppers, 2= Low-value deal seekers.

3. Recommendations should take the form of a simple table (output both CSV and .md versions) that contains these variables:

- segment name
- short segment description
- marketing objective
- messaging strategy
- offer strategy
- channel strategy
- product focus
- suggested KPIs

Suggested strategies for each group:

Group 0

- Treat as the highest-value premium audience.
- Use premium, quality-led messaging rather than discount-led messaging.
- Focus on wine, meat, premium bundles, exclusivity, loyalty, early access, and personalised recommendations.
- Use catalogue/direct channels strongly, supported by email or web retargeting.
- Avoid unnecessary discounting because this segment has high spend and low deal share.

Group 1

- Treat as a mid-value, family-oriented growth segment.
- Use practical value messaging: family offers, bundles, convenience, multi-buy, seasonal household shopping.
- Wine is still important, but offers should be more value-conscious than premium.
- Use web and store channels, supported by targeted discounts.
- This segment is more deal-sensitive, so promotions may be useful, but should be designed to increase basket size rather than simply subsidise existing purchases.

Group 2

- Treat as a low-value, price-sensitive segment.
- Avoid expensive broad campaigns.
- Use low-cost, automated, deal-led campaigns only where commercially justified.
- Focus on simple offers, entry-level bundles, store-led promotions, and reactivation messaging.
- Monitor whether discounts create incremental spend or simply attract low-margin purchases.

When suggesting KPIs, suggest specific values grounded in the evidence in the dataset. Where a KPI requires more data, mark the suggestion as provisional pending more data. Here are the variables we can use as KPIs for each group:

- response rate
- average total spend
- average spend per purchase
- purchase count
- channel mix
- product category spend
- deal purchase share
- campaign acceptance rate
- complaint rate
- recency

## Deliverables

Create or update:

- `outputs/stage-outputs/06-recommendations.md`
- `outputs/tables/06_recommendation_matrix.csv`
- `outputs/tables/06_kpi_guidance.csv`

Update:

- `reports/final_report.md`

## Output summary

Write a concise markdown summary to:

- `outputs/stage-outputs/06-recommendations.md`

The summary should include:

- overall recommendation
- explanation of why the three segments should be used
- recommendation matrix
- KPI guidance
- limitations

## Definition of done

- [ ] Recommendations are provided for all three named segments.
- [ ] Recommendations are clearly linked to the segment profiles.
- [ ] Suggested KPIs distinguish between what is available in the dataset and what would require extra data.
- [ ] A concise recommendation matrix is saved under `outputs/tables/`.
- [ ] A reviewable markdown summary is saved to `outputs/stage-outputs/06-recommendations.md`.

## Review notes

_To be completed after reviewing Codex output._

## Next steps

_To be completed before moving to the next stage._
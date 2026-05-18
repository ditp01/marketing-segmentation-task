# Stage XX: Stage Name

## Status

Not started

## Goal

Create derived features: age, tenure, total spend, total purchases, campaign acceptance total, household children, channel shares, category spend shares, using this logic:

- `Age`
  - Derive from `Year_Birth`.
  - Use a documented reference year rather than the current system year. For this dataset, use the latest customer enrolment year or another fixed analysis year chosen in the script.
  - Flag or exclude implausible ages identified during the data audit.

- `Customer_Tenure`
  - Derive from `Dt_Customer`.
  - Parse `Dt_Customer` as a date.
  - Calculate tenure as the number of days, months, or years between the customer enrolment date and a documented reference date.
  - Use the maximum observed `Dt_Customer` as the default reference date unless another reference date is explicitly chosen.

- `Total_Spend`
  - Sum all product spend columns:
    - `MntWines`
    - `MntFruits`
    - `MntMeatProducts`
    - `MntFishProducts`
    - `MntSweetProducts`
    - `MntGoldProds`
  - Use this as the main proxy for observed customer value.

- `Total_Purchases`
  - Sum purchase counts across channels:
    - `NumWebPurchases`
    - `NumCatalogPurchases`
    - `NumStorePurchases`
  - Do not include `NumDealsPurchases` in this total, because it is a type of purchase behaviour rather than a separate channel.

- `Campaign_Acceptance_Total`
  - Sum previous campaign acceptance fields:
    - `AcceptedCmp1`
    - `AcceptedCmp2`
    - `AcceptedCmp3`
    - `AcceptedCmp4`
    - `AcceptedCmp5`
  - Use this for profiling and evaluating segments, not as a clustering input.

- `Household_Children`
  - Sum:
    - `Kidhome`
    - `Teenhome`
  - Optionally also create a binary flag:
    - `Has_Children = Household_Children > 0`

- `Channel_Shares`
  - Calculate the proportion of purchases made through each channel:
    - `Web_Purchase_Share = NumWebPurchases / Total_Purchases`
    - `Catalog_Purchase_Share = NumCatalogPurchases / Total_Purchases`
    - `Store_Purchase_Share = NumStorePurchases / Total_Purchases`
  - Handle customers with `Total_Purchases = 0` safely by setting shares to 0 or `NaN`, and document the choice.

- `Deal_Purchase_Share`
  - Calculate:
    - `Deal_Purchase_Share = NumDealsPurchases / Total_Purchases`
  - Handle zero-purchase customers safely.
  - This should help identify deal-sensitive customers.

- `Category_Spend_Shares`
  - Calculate each product category as a share of `Total_Spend`:
    - `Wine_Spend_Share = MntWines / Total_Spend`
    - `Fruit_Spend_Share = MntFruits / Total_Spend`
    - `Meat_Spend_Share = MntMeatProducts / Total_Spend`
    - `Fish_Spend_Share = MntFishProducts / Total_Spend`
    - `Sweet_Spend_Share = MntSweetProducts / Total_Spend`
    - `Gold_Spend_Share = MntGoldProds / Total_Spend`
  - Handle customers with `Total_Spend = 0` safely by setting shares to 0 or `NaN`, and document the choice.

- `Average_Spend_Per_Purchase`
  - Calculate:
    - `Average_Spend_Per_Purchase = Total_Spend / Total_Purchases`
  - Handle zero-purchase customers safely.
  - This can be used as a rough indicator of basket value.

- `Web_Engagement_Ratio`, optional
  - Consider creating a simple web conversion proxy:
    - `Web_Purchases_Per_Web_Visit = NumWebPurchases / NumWebVisitsMonth`
  - Handle customers with zero web visits safely.
  - Use cautiously, because the time windows for purchases and web visits may not be directly comparable.


## Context

Relevant background from previous stages, if any.

## Inputs

Files Codex should read or use.

Examples:
- `data/raw/marketing_campaign.csv`
- `data/processed/customers_features.csv`
- `project/decisions.md`
- `outputs/stage-outputs/previous-stage.md`

## Instructions for Codex

Complete this stage only.

Specific instructions:
- 
- 
- 

Do not:
- 
- 

## Deliverables

Expected files to create or update.

Examples:
- `scripts/01_data_audit.py`
- `src/load_data.py`
- `outputs/stage-outputs/01-data-audit.md`
- `outputs/tables/data_quality_summary.csv`

## Definition of done

- [ ] Script runs end to end
- [ ] Outputs are saved in the expected locations
- [ ] Stage output markdown is clear enough for review
- [ ] Assumptions or data issues are documented
- [ ] No unnecessary later-stage work has been done

## Review notes

_To be completed after reviewing Codex output._

## Next steps

_To be completed before moving to the next stage._
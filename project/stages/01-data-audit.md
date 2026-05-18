# Stage 1: Data Audit

## Status

Not started

## Goal

The objective of this stage is to examine the dataset and audit it, before further cleaning and/or feature engineering.
At this point let's keep it simple, with a reproducible data audit script that checks the following:

- dataset shape
- column names and data types
- missing values
- duplicate rows and duplicate `Id`s
- constant and near-constant columns
- numeric summaries and implausible values
- categorical levels and rare categories
- binary variable validity and response rates
- date range and parsing for `Dt_Customer`
- logical consistency across spend and purchase variables
- likely outliers relevant to clustering

For any missing variables, identify the scale of the missing data.
Exploratory: for any customers missing any data, identify any unusual behavioural features

## Context

This is the first stage of analysis, so no prior context, other than this run-down of variables:

Id: Unique identifier for each individual in the dataset.
Year_Birth: The birth year of the individual.
Education: The highest level of education attained by the individual.
Marital_Status: The marital status of the individual.
Income: The annual income of the individual.
Kidhome: The number of young children in the household.
Teenhome: The number of teenagers in the household.
Dt_Customer: The date when the customer was first enrolled or became a part of the company's database.
Recency: The number of days since the last purchase or interaction.
MntWines: The amount spent on wines.
MntFruits: The amount spent on fruits.
MntMeatProducts: The amount spent on meat products.
MntFishProducts: The amount spent on fish products.
MntSweetProducts: The amount spent on sweet products.
MntGoldProds: The amount spent on gold products.
NumDealsPurchases: The number of purchases made with a discount or as part of a deal.
NumWebPurchases: The number of purchases made through the company's website.
NumCatalogPurchases: The number of purchases made through catalogs.
NumStorePurchases: The number of purchases made in physical stores.
NumWebVisitsMonth: The number of visits to the company's website in a month.
AcceptedCmp3: Binary indicator (1 or 0) whether the individual accepted the third marketing campaign.
AcceptedCmp4: Binary indicator (1 or 0) whether the individual accepted the fourth marketing campaign.
AcceptedCmp5: Binary indicator (1 or 0) whether the individual accepted the fifth marketing campaign.
AcceptedCmp1: Binary indicator (1 or 0) whether the individual accepted the first marketing campaign.
AcceptedCmp2: Binary indicator (1 or 0) whether the individual accepted the second marketing campaign.
Complain: Binary indicator (1 or 0) whether the individual has made a complaint.
Z_CostContact: A constant cost associated with contacting a customer.
Z_Revenue: A constant revenue associated with a successful campaign response.
Response: Binary indicator (1 or 0) whether the individual responded to the marketing campaign.


## Inputs

- `data/raw/marketing_campaign.csv`

## Instructions for Codex

Complete this stage only.

## Deliverables

Expected files to create or update.

Create or update:

- `scripts/01_data_audit.py`
- `src/load_data.py`, if useful
- `src/audit.py`, if useful
- `outputs/stage-outputs/01-data-audit.md`
- `outputs/tables/data_quality_summary.csv`
- `outputs/tables/missing_values.csv`
- `outputs/tables/numeric_summary.csv`
- `outputs/tables/categorical_summary.csv`

## Definition of done

- [ ] `python scripts/01_data_audit.py` runs from the repo root
- [ ] the script does not modify `data/raw/marketing_campaign.csv`
- [ ] `outputs/stage-outputs/01-data-audit.md` is created
- [ ] key audit tables are saved under `outputs/tables/`
- [ ] missing values are reported
- [ ] duplicate rows and duplicate `Id`s are checked
- [ ] constant columns are identified
- [ ] categorical levels are summarised
- [ ] binary variables are validated
- [ ] numeric plausibility checks are included
- [ ] date range for `Dt_Customer` is reported
- [ ] issues requiring decisions in Stage 02 are clearly listed


## Review notes

Decisions based on my review of the audit outputs:

- The 24 missing `Income` values - delete those cases. Less than 1% of dataset, and uncertain why blank (interesting to note the lower Wine spend)
- Delete the `Income = 666666` outlier.
- Handle implausible `Year_Birth` values before deriving age - again, drop the cases for this run. I'm aware there are other options (capping, etc) but there are very few cases that fall into this category.
- Drop `Z_CostContact` and `Z_Revenue` from modelling because they are constant.
- Keep `ID` only as an identifier.
- Exclude `Response` and `AcceptedCmp1-5` from clustering inputs; reserve them for segment evaluation.
- Rare `Marital_Status` items: `Alone`, `Absurd`, `YOLO`. For these, I'd like to convert them to `Unknown`. I suspect that responding like that to the question may actually tell us something behavioural about the respondents.

## Next steps

1. Create a new marketing_campaign_processed.csv file in data/processed, with the following changes:
2. Drop cases/modify categories as outlined above.

# Stage XX: Stage Name

## Status

Not started

## Goal

Generate exploratory analysis to understand customer value, behaviour, channel usage, and campaign response before clustering.

## Context

See previous exploration in 01 and 02 project stages and the outputs folder.

## Inputs

- `data/processed/marketing_campaign_processed_features_engineered.csv`

## Instructions for Codex

Create `scripts/03_run_eda.py` to generate a small set of useful EDA tables and charts.

Focus on:
- customer value: `Total_Spend`, `Income`, `Average_Spend_Per_Purchase`
- engagement: `Recency`, `Total_Purchases`, `NumWebVisitsMonth`
- channels: web, catalogue, store purchase behaviour and channel shares
- product preferences: spend by product category and category spend shares
- household composition: children vs no children
- campaign response: `Response`, previous campaign acceptances, and response by key customer groups

Create clear, reviewable outputs rather than exhaustive analysis.

Do not:
- perform clustering
- create final segment names
- write final recommendations
- modify raw data

## Deliverables

- `scripts/03_run_eda.py`
- supporting functions in `src/eda.py` or `src/plots.py`, if useful
- `outputs/stage-outputs/03-eda.md`
- EDA summary tables in `outputs/tables/`
- EDA charts in `reports/figures/`

Create concise tables including:

- overall KPI summary
- response rate summary
- spend summary by response
- channel summary by response
- household summary by response
- top product category spend summary
- correlation table for key numeric variables

## Suggested charts

Create a small number of useful charts:

- distribution of `Total_Spend`
- distribution of `Income`, ideally with outliers handled or noted
- response rate by income/spend bands
- average spend by product category
- channel usage summary
- recency vs total spend, coloured or split by response if practical

## Definition of done

- [ ] `python scripts/03_run_eda.py` runs successfully from the repo root.
- [ ] Key EDA tables are saved under `outputs/tables/`.
- [ ] Key charts are saved under `reports/figures/`.
- [ ] A concise review summary is saved to `outputs/stage-outputs/03-eda.md`.
- [ ] The summary highlights the most useful patterns for segmentation and campaign targeting.
- [ ] The output identifies sensible variables or themes to carry into clustering.


## Review notes

After reading the EDA outputs, here are some possible segments based on the patterns emerging before clustering:

1. High-value high-income responders
High income/spend, strong wine/meat spend, high catalogue use, high response.

2. Family/value-oriented customers
Children at home, lower spend, more deal-sensitive, lower response.

3. Low-value browsers or low-engagement customers
Low spend, low purchase volume, possibly high web visits but weak conversion.

4. Lapsed or lower-recency customers
Historical customers but less recent, could be used for win-back targeting.


## Next steps

Move on to clustering approaches to see if these segments can be validated or further segments can be identified through unsupervised techniques.
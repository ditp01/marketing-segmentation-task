# Stage 02 Feature Engineering

## Input and Output
- Input dataset: `C:/dev/marketing-segmentation-task/data/processed/marketing_campaign_processed.csv`
- Output dataset: `C:/dev/marketing-segmentation-task/data/processed/marketing_campaign_processed_features_engineered.csv`
- Input shape: 2212 rows x 27 columns
- Output shape: 2212 rows x 48 columns

## Assumptions and Handling Choices
- `Dt_Customer` reference date: 2014-06-29 (max observed date).
- Age reference year: 2014.
- Age plausibility check: 18 to 100 years.
- Missing income handling: inherited from Stage 01 preprocessing (rows already removed in input file).
- Division-by-zero handling: all ratio/share features are set to `0` when denominator is `0`.
- `Response` and `AcceptedCmp1-5` are retained for evaluation but excluded from clustering inputs.

## Features Created
```
                    feature  created   dtype                                                     description  recommended_for_clustering
                        Age     True   int64                                Reference year minus Year_Birth.                        True
         Age_Plausible_Flag     True   int64                         1 if Age is between 18 and 100, else 0.                        True
       Customer_Tenure_Days     True   int64                    Days between Dt_Customer and reference date.                        True
      Customer_Tenure_Years     True float64                         Customer_Tenure_Days divided by 365.25.                        True
                Total_Spend     True   int64                                Sum of all Mnt* spend variables.                        True
            Total_Purchases     True   int64                 Sum of web, catalog, and store purchase counts.                        True
  Campaign_Acceptance_Total     True   int64                            Sum of AcceptedCmp1 to AcceptedCmp5.                       False
         Household_Children     True   int64                                             Kidhome + Teenhome.                        True
               Has_Children     True   int64                             1 if Household_Children > 0 else 0.                        True
         Web_Purchase_Share     True float64     NumWebPurchases / Total_Purchases; 0 when denominator is 0.                        True
     Catalog_Purchase_Share     True float64 NumCatalogPurchases / Total_Purchases; 0 when denominator is 0.                        True
       Store_Purchase_Share     True float64   NumStorePurchases / Total_Purchases; 0 when denominator is 0.                        True
        Deal_Purchase_Share     True float64   NumDealsPurchases / Total_Purchases; 0 when denominator is 0.                        True
           Wine_Spend_Share     True float64                MntWines / Total_Spend; 0 when denominator is 0.                        True
          Fruit_Spend_Share     True float64               MntFruits / Total_Spend; 0 when denominator is 0.                        True
           Meat_Spend_Share     True float64         MntMeatProducts / Total_Spend; 0 when denominator is 0.                        True
           Fish_Spend_Share     True float64         MntFishProducts / Total_Spend; 0 when denominator is 0.                        True
          Sweet_Spend_Share     True float64        MntSweetProducts / Total_Spend; 0 when denominator is 0.                        True
           Gold_Spend_Share     True float64            MntGoldProds / Total_Spend; 0 when denominator is 0.                        True
 Average_Spend_Per_Purchase     True float64         Total_Spend / Total_Purchases; 0 when denominator is 0.                        True
Web_Purchases_Per_Web_Visit     True float64   NumWebPurchases / NumWebVisitsMonth; 0 when denominator is 0.                        True
```

## Key Validation Checks
- `Dt_Customer` parse failures: 0
- Rows with `Total_Purchases = 0`: 6
- Rows with `Total_Spend = 0`: 0
- Rows with `NumWebVisitsMonth = 0`: 10
- Mean channel-share sum for rows with `Total_Purchases > 0`: 1.0000
- Max channel-share sum for rows with `Total_Purchases = 0`: 0.0000
- Recommended clustering exclusions: ID, Response, AcceptedCmp1, AcceptedCmp2, AcceptedCmp3, AcceptedCmp4, AcceptedCmp5, Campaign_Acceptance_Total
- Campaign evaluation columns retained: AcceptedCmp1, AcceptedCmp2, AcceptedCmp3, AcceptedCmp4, AcceptedCmp5

## Engineered Feature Descriptive Statistics
```
                    feature  non_missing_count  missing_count  missing_pct  zero_count  zero_pct       mean        std  min       p01       p05        p25        p50         p75         p95         p99         max
                        Age             2212.0              0          0.0           0  0.000000  45.086347  11.701599 18.0 22.000000 26.000000  37.000000  44.000000   55.000000   64.000000   68.890000   74.000000
         Age_Plausible_Flag             2212.0              0          0.0           0  0.000000   1.000000   0.000000  1.0  1.000000  1.000000   1.000000   1.000000    1.000000    1.000000    1.000000    1.000000
 Average_Spend_Per_Purchase             2212.0              0          0.0           6  0.271248  37.449216  30.088587  0.0  4.027500  6.333333  13.000000  29.839744   49.166667  101.647368  127.987778  187.666667
  Campaign_Acceptance_Total             2212.0              0          0.0        1754 79.294756   0.298373   0.679570  0.0  0.000000  0.000000   0.000000   0.000000    0.000000    2.000000    3.000000    4.000000
     Catalog_Purchase_Share             2212.0              0          0.0         575 25.994575   0.164739   0.140626  0.0  0.000000  0.000000   0.000000   0.150000    0.250000    0.416667    0.523810    1.000000
       Customer_Tenure_Days             2212.0              0          0.0           2  0.090416 353.714286 202.494886  0.0  7.000000 38.000000 180.000000 356.000000  529.000000  667.000000  691.000000  699.000000
      Customer_Tenure_Years             2212.0              0          0.0           2  0.090416   0.968417   0.554401  0.0  0.019165  0.104038   0.492813   0.974675    1.448323    1.826146    1.891855    1.913758
        Deal_Purchase_Share             2212.0              0          0.0          46  2.079566   0.246951   0.358038  0.0  0.000000  0.041667   0.083333   0.200000    0.333333    0.571429    0.666667   15.000000
           Fish_Spend_Share             2212.0              0          0.0         379 17.133816   0.071612   0.078036  0.0  0.000000  0.000000   0.012571   0.048193    0.104720    0.224577    0.356681    0.590909
          Fruit_Spend_Share             2212.0              0          0.0         394 17.811935   0.049462   0.055776  0.0  0.000000  0.000000   0.008976   0.029774    0.070175    0.166667    0.255590    0.445545
           Gold_Spend_Share             2212.0              0          0.0          61  2.757685   0.120027   0.108832  0.0  0.000000  0.009361   0.038033   0.085714    0.169768    0.343489    0.447854    0.894150
               Has_Children             2212.0              0          0.0         632 28.571429   0.714286   0.451856  0.0  0.000000  0.000000   0.000000   1.000000    1.000000    1.000000    1.000000    1.000000
         Household_Children             2212.0              0          0.0         632 28.571429   0.947559   0.749466  0.0  0.000000  0.000000   0.000000   1.000000    1.000000    2.000000    3.000000    3.000000
           Meat_Spend_Share             2212.0              0          0.0           1  0.045208   0.249099   0.125777  0.0  0.038973  0.072164   0.156217   0.233289    0.328227    0.470772    0.587694    0.997110
       Store_Purchase_Share             2212.0              0          0.0          14  0.632911   0.503707   0.151106  0.0  0.190476  0.272727   0.400000   0.500000    0.600000    0.750000    1.000000    1.000000
          Sweet_Spend_Share             2212.0              0          0.0         412 18.625678   0.050790   0.060955  0.0  0.000000  0.000000   0.008629   0.033333    0.070719    0.163762    0.254045    0.945848
            Total_Purchases             2212.0              0          0.0           6  0.271248  12.566908   7.205427  0.0  3.000000  3.000000   6.000000  12.000000   18.250000   24.000000   27.890000   32.000000
                Total_Spend             2212.0              0          0.0           0  0.000000 607.268083 602.513364  5.0 13.000000 22.000000  69.000000 397.000000 1048.000000 1774.700000 2126.000000 2525.000000
         Web_Purchase_Share             2212.0              0          0.0          48  2.169982   0.328842   0.122092  0.0  0.000000  0.142857   0.250000   0.333333    0.400000    0.500000    0.598706    1.000000
Web_Purchases_Per_Web_Visit             2212.0              0          0.0          54  2.441230   1.077201   1.211612  0.0  0.000000  0.125000   0.333333   0.750000    1.500000    3.000000    4.000000   27.000000
           Wine_Spend_Share             2212.0              0          0.0          13  0.587703   0.459010   0.228604  0.0  0.017122  0.065612   0.290067   0.458224    0.641164    0.830769    0.914756    0.963303
```

## Missing Values After Feature Engineering
No rows.

## Recommended Next Steps for EDA
- Review skew/outliers in `Total_Spend`, `Average_Spend_Per_Purchase`, and spend-share features.
- Evaluate correlation and redundancy among spending and purchase-ratio features.
- Confirm final clustering feature set excludes identifier and outcome/evaluation variables.

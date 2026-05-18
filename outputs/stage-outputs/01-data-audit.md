# Stage 01 Data Audit

## Dataset Overview
- Source file: `C:/dev/marketing-segmentation-task/data/raw/marketing_campaign.csv`
- Dataset shape: 2240 rows x 29 columns
- Missing cells: 24 / 64960 (0.04%)
- Rows with any missing value: 24

## Columns and Data Types
```
             column   dtype
       AcceptedCmp1   int64
       AcceptedCmp2   int64
       AcceptedCmp3   int64
       AcceptedCmp4   int64
       AcceptedCmp5   int64
           Complain   int64
        Dt_Customer     str
          Education     str
                 ID   int64
             Income float64
            Kidhome   int64
     Marital_Status     str
    MntFishProducts   int64
          MntFruits   int64
       MntGoldProds   int64
    MntMeatProducts   int64
   MntSweetProducts   int64
           MntWines   int64
NumCatalogPurchases   int64
  NumDealsPurchases   int64
  NumStorePurchases   int64
    NumWebPurchases   int64
  NumWebVisitsMonth   int64
            Recency   int64
           Response   int64
           Teenhome   int64
         Year_Birth   int64
      Z_CostContact   int64
          Z_Revenue   int64
```

## Missing Values
```
column  missing_count  missing_pct  non_missing_count
Income             24     1.071429               2216
```

## Duplicates
- Duplicate full rows: 0
- ID column used: `ID`
- Duplicate `ID` rows: 0
- Unique duplicated `ID` values: 0

## Constant and Near-Constant Columns
```
       column  non_null_unique_count top_value  top_count    top_pct  is_constant  is_near_constant
 AcceptedCmp2                      2         0       2210  98.660714        False              True
     Complain                      2         0       2219  99.062500        False              True
Z_CostContact                      1         3       2240 100.000000         True             False
    Z_Revenue                      1        11       2240 100.000000         True             False
```

## Numeric Summary and Implausible Value Checks
```
             column  count  missing_count  missing_pct         mean          std    min     p01      p05      p25     p50      p75      p95      p99      max     iqr  lower_bound  upper_bound  outlier_count  outlier_pct  negative_count
       AcceptedCmp1 2240.0              0     0.000000     0.064286     0.245316    0.0    0.00     0.00     0.00     0.0     0.00     1.00     1.00      1.0     0.0          0.0          0.0              0     0.000000               0
       AcceptedCmp2 2240.0              0     0.000000     0.013393     0.114976    0.0    0.00     0.00     0.00     0.0     0.00     0.00     1.00      1.0     0.0          0.0          0.0              0     0.000000               0
       AcceptedCmp3 2240.0              0     0.000000     0.072768     0.259813    0.0    0.00     0.00     0.00     0.0     0.00     1.00     1.00      1.0     0.0          0.0          0.0              0     0.000000               0
       AcceptedCmp4 2240.0              0     0.000000     0.074554     0.262728    0.0    0.00     0.00     0.00     0.0     0.00     1.00     1.00      1.0     0.0          0.0          0.0              0     0.000000               0
       AcceptedCmp5 2240.0              0     0.000000     0.072768     0.259813    0.0    0.00     0.00     0.00     0.0     0.00     1.00     1.00      1.0     0.0          0.0          0.0              0     0.000000               0
           Complain 2240.0              0     0.000000     0.009375     0.096391    0.0    0.00     0.00     0.00     0.0     0.00     0.00     0.00      1.0     0.0          0.0          0.0              0     0.000000               0
                 ID 2240.0              0     0.000000  5592.159821  3246.662198    0.0  123.78   576.85  2828.25  5458.5  8427.75 10675.05 11074.61  11191.0  5599.5      -5571.0      16827.0              0     0.000000               0
             Income 2216.0             24     1.071429 52247.251354 25173.076661 1730.0 7579.20 18985.50 35303.00 51381.5 68522.00 84130.00 94458.80 666666.0 33219.0     -14525.5     118350.5              8     0.361011               0
            Kidhome 2240.0              0     0.000000     0.444196     0.538398    0.0    0.00     0.00     0.00     0.0     1.00     1.00     2.00      2.0     1.0         -1.5          2.5              0     0.000000               0
    MntFishProducts 2240.0              0     0.000000    37.525446    54.628979    0.0    0.00     0.00     3.00    12.0    50.00   168.05   226.22    259.0    47.0        -67.5        120.5            223     9.955357               0
          MntFruits 2240.0              0     0.000000    26.302232    39.773434    0.0    0.00     0.00     1.00     8.0    33.00   123.00   172.00    199.0    32.0        -47.0         81.0            227    10.133929               0
       MntGoldProds 2240.0              0     0.000000    44.021875    52.167439    0.0    0.00     1.00     9.00    24.0    56.00   165.05   227.00    362.0    47.0        -61.5        126.5            207     9.241071               0
    MntMeatProducts 2240.0              0     0.000000   166.950000   225.715373    0.0    2.00     4.00    16.00    67.0   232.00   687.10   915.00   1725.0   216.0       -308.0        556.0            175     7.812500               0
   MntSweetProducts 2240.0              0     0.000000    27.062946    41.280498    0.0    0.00     0.00     1.00     8.0    33.00   126.00   177.22    263.0    32.0        -47.0         81.0            248    11.071429               0
           MntWines 2240.0              0     0.000000   303.935714   336.597393    0.0    1.00     3.00    23.75   173.5   504.25  1000.00  1285.00   1493.0   480.5       -697.0       1225.0             35     1.562500               0
NumCatalogPurchases 2240.0              0     0.000000     2.662054     2.923101    0.0    0.00     0.00     0.00     2.0     4.00     9.00    10.61     28.0     4.0         -6.0         10.0             23     1.026786               0
  NumDealsPurchases 2240.0              0     0.000000     2.325000     1.932238    0.0    0.00     1.00     1.00     2.0     3.00     6.00    10.00     15.0     2.0         -2.0          6.0             86     3.839286               0
  NumStorePurchases 2240.0              0     0.000000     5.790179     3.250958    0.0    2.00     2.00     3.00     5.0     8.00    12.00    13.00     13.0     5.0         -4.5         15.5              0     0.000000               0
    NumWebPurchases 2240.0              0     0.000000     4.084821     2.778714    0.0    0.00     1.00     2.00     4.0     6.00     9.00    11.00     27.0     4.0         -4.0         12.0              4     0.178571               0
  NumWebVisitsMonth 2240.0              0     0.000000     5.316518     2.426645    0.0    1.00     1.00     3.00     6.0     7.00     8.00     9.00     20.0     4.0         -3.0         13.0              8     0.357143               0
```

Implausible value checks:
```
                               check  issue_count  issue_pct
                   income_above_300k            1   0.044643
          likely_over_100_year_birth            3   0.133929
          likely_under_18_year_birth            0   0.000000
                     negative_income            0   0.000000
 rows_with_any_negative_num_variable            0   0.000000
        rows_with_any_negative_spend            0   0.000000
year_birth_outside_1900_current_year            2   0.089286
                         zero_income            0   0.000000
```

## Categorical Levels and Rare Categories
```
        column      level  count       pct  is_rare  is_missing_level
     Education Graduation   1127 50.312500    False             False
     Education        PhD    486 21.696429    False             False
     Education     Master    370 16.517857    False             False
     Education   2n Cycle    203  9.062500    False             False
     Education      Basic     54  2.410714    False             False
Marital_Status    Married    864 38.571429    False             False
Marital_Status   Together    580 25.892857    False             False
Marital_Status     Single    480 21.428571    False             False
Marital_Status   Divorced    232 10.357143    False             False
Marital_Status      Widow     77  3.437500    False             False
Marital_Status      Alone      3  0.133929     True             False
Marital_Status     Absurd      2  0.089286     True             False
Marital_Status       YOLO      2  0.089286     True             False
```

## Binary Variable Validity and Response Rates
```
      column  present  invalid_value_count  invalid_value_pct  zero_count  one_count  positive_rate_pct  missing_count
AcceptedCmp1     True                    0                0.0        2096        144           6.428571              0
AcceptedCmp2     True                    0                0.0        2210         30           1.339286              0
AcceptedCmp3     True                    0                0.0        2077        163           7.276786              0
AcceptedCmp4     True                    0                0.0        2073        167           7.455357              0
AcceptedCmp5     True                    0                0.0        2077        163           7.276786              0
    Complain     True                    0                0.0        2219         21           0.937500              0
    Response     True                    0                0.0        1906        334          14.910714              0
```

## Date Parsing (`Dt_Customer`)
- Parse failures: 0 (0.00%)
- Date range: 2012-07-30 to 2014-06-29

## Logical Consistency Checks
```
                            check  issue_count  issue_pct                                                        description
         negative_purchase_counts            0   0.000000                    Rows with at least one negative purchase count.
            negative_spend_values            0   0.000000                       Rows with at least one negative spend value.
       recency_out_of_range_0_365            0   0.000000                          Rows where Recency is outside 0-365 days.
  spend_positive_but_no_purchases            6   0.267857 Rows with positive total spend but zero purchases across channels.
spend_zero_but_purchases_positive            0   0.000000              Rows with zero total spend but at least one purchase.
```

## Likely Outliers Relevant to Clustering
```
             column  outlier_count  outlier_pct      p95      p99      max
   MntSweetProducts            248    11.071429   126.00   177.22    263.0
          MntFruits            227    10.133929   123.00   172.00    199.0
    MntFishProducts            223     9.955357   168.05   226.22    259.0
       MntGoldProds            207     9.241071   165.05   227.00    362.0
    MntMeatProducts            175     7.812500   687.10   915.00   1725.0
  NumDealsPurchases             86     3.839286     6.00    10.00     15.0
           MntWines             35     1.562500  1000.00  1285.00   1493.0
NumCatalogPurchases             23     1.026786     9.00    10.61     28.0
             Income              8     0.361011 84130.00 94458.80 666666.0
  NumWebVisitsMonth              8     0.357143     8.00     9.00     20.0
    NumWebPurchases              4     0.178571     9.00    11.00     27.0
         Year_Birth              3     0.133929  1988.00  1992.00   1996.0
```

## Exploratory Check: Customers Missing Any Data
- Customers missing any variable: 24 (1.07%)
```
            feature  mean_missing_any  mean_not_missing_any  difference  pct_difference
             Income               NaN          52247.251354         NaN             NaN
    MntFishProducts         27.166667             37.637635  -10.470969      -27.820474
          MntFruits         21.333333             26.356047   -5.022714      -19.057158
       MntGoldProds         49.250000             43.965253    5.284747       12.020282
    MntMeatProducts        162.708333            166.995939   -4.287605       -2.567491
   MntSweetProducts         30.208333             27.028881    3.179452       11.763167
           MntWines        197.208333            305.091606 -107.883273      -35.360944
NumCatalogPurchases          1.833333              2.671029   -0.837696      -31.362280
  NumStorePurchases          4.791667              5.800993   -1.009326      -17.399196
    NumWebPurchases          4.041667              4.085289   -0.043622       -1.067786
            Recency         58.041667             49.012635    9.029031       18.421844
```

## Issues Requiring Decisions in Stage 02
- `Income` has missing values (24 rows, 1.07%). Decide imputation strategy in Stage 02.
- Constant columns detected (`Z_CostContact`, `Z_Revenue`). Drop as non-informative.
- Near-constant columns detected (`AcceptedCmp2`, `Complain`).
- 3 categorical levels are rare (<1%). Decide whether to combine levels in Stage 02.
- Potential clustering outliers detected in numeric features; decide winsorisation/capping/transformation strategy.

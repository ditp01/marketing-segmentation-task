# Stage 03 EDA

## Dataset and Scope
- Input file: `C:/dev/marketing-segmentation-task/data/processed/marketing_campaign_processed_features_engineered.csv`
- Rows: 2212 | Columns: 48
- Key correlation variables reviewed: Income, Total_Spend, Average_Spend_Per_Purchase, Recency, Total_Purchases, NumWebVisitsMonth, Campaign_Acceptance_Total, Response

## Overall KPI Summary
```
                       metric        value
               customer_count 2.212000e+03
            response_rate_pct 1.505425e+01
              total_spend_sum 1.343277e+06
              avg_total_spend 6.072681e+02
           median_total_spend 3.970000e+02
                   avg_income 5.195881e+04
          avg_total_purchases 1.256691e+01
             avg_recency_days 4.901944e+01
avg_campaign_acceptance_total 2.983725e-01
        has_children_rate_pct 7.142857e+01
```

## Response and Behaviour Summaries
Response rates:
```
                        metric  positive_count  positive_rate_pct
                      Response             333          15.054250
                  AcceptedCmp1             142           6.419530
                  AcceptedCmp2              30           1.356239
                  AcceptedCmp3             163           7.368897
                  AcceptedCmp4             164           7.414105
                  AcceptedCmp5             161           7.278481
Any_Previous_Campaign_Accepted             458          20.705244
```

Spend summary by response:
```
 Response response_label  customer_count   avg_income  median_income  avg_total_spend  median_total_spend  avg_spend_per_purchase  median_spend_per_purchase
        0  Non-Responder            1879 50496.576370        50150.0       540.208622               315.0               34.124973                  27.727273
        1      Responder             333 60209.675676        64090.0       985.660661              1053.0               56.206730                  46.388889
```

Channel summary by response:
```
 Response response_label  Total_Purchases  NumWebPurchases  NumCatalogPurchases  NumStorePurchases  Web_Purchase_Share  Catalog_Purchase_Share  Store_Purchase_Share  Deal_Purchase_Share  avg_num_web_visits_month
        0  Non-Responder        12.072911         3.913784             2.401277           5.757850            0.326067                0.150335              0.520405             0.253947                  5.324109
        1      Responder        15.354354         5.072072             4.201201           6.081081            0.344502                0.246016              0.409482             0.207471                  5.306306
```

Household summary by response:
```
 Response response_label  customer_count  avg_household_children  median_household_children  has_children_rate_pct  avg_total_spend  avg_response_recency
        0  Non-Responder            1879                1.000532                        1.0              75.306014       540.208622             51.457158
        1      Responder             333                0.648649                        0.0              49.549550       985.660661             35.264264
```

Top product category spend summary:
```
product_category  avg_spend_overall  avg_spend_non_responder  avg_spend_responder  responder_minus_non_responder
        MntWines         305.287523               270.316658           502.615616                     232.298958
 MntMeatProducts         167.029837               144.569452           293.765766                     149.196314
    MntGoldProds          43.925859                40.855242            61.252252                      20.397010
 MntFishProducts          37.648734                35.155934            51.714715                      16.558781
MntSweetProducts          27.046564                25.039383            38.372372                      13.332990
       MntFruits          26.329566                24.271953            37.939940                      13.667987
```

Correlation table (key numeric variables):
```
                  variable    Income  Total_Spend  Average_Spend_Per_Purchase   Recency  Total_Purchases  NumWebVisitsMonth  Campaign_Acceptance_Total  Response
                    Income  1.000000     0.792740                    0.727078  0.007965         0.742691          -0.650257                   0.365986  0.161387
               Total_Spend  0.792740     1.000000                    0.918067  0.020479         0.823361          -0.498769                   0.456456  0.264443
Average_Spend_Per_Purchase  0.727078     0.918067                    1.000000  0.016630         0.630486          -0.440754                   0.433835  0.262501
                   Recency  0.007965     0.020479                    0.016630  1.000000         0.007462          -0.018965                  -0.013471 -0.200114
           Total_Purchases  0.742691     0.823361                    0.630486  0.007462         1.000000          -0.427457                   0.306644  0.162893
         NumWebVisitsMonth -0.650257    -0.498769                   -0.440754 -0.018965        -0.427457           1.000000                  -0.164944 -0.002625
 Campaign_Acceptance_Total  0.365986     0.456456                    0.433835 -0.013471         0.306644          -0.164944                   1.000000  0.427297
                  Response  0.161387     0.264443                    0.262501 -0.200114         0.162893          -0.002625                   0.427297  1.000000
```

Response by income band:
```
   Income_Band  customer_count  response_rate_pct  avg_total_spend  avg_total_purchases
 Q1 Low Income             443          10.158014        73.124153             5.277652
            Q2             442          13.122172       157.762443             7.199095
            Q3             442          10.859729       442.751131            12.726244
            Q4             442          10.859729       949.309955            18.180995
Q5 High Income             443          30.248307      1412.778781            19.451467
```

Response by spend band:
```
   Spend_Band  customer_count  response_rate_pct   avg_income  avg_total_purchases
 Q1 Low Spend             444           4.279279 30836.500000             4.058559
           Q2             443          13.544018 35946.446953             6.241535
           Q3             440          12.045455 50429.106818            13.097727
           Q4             443          11.512415 66163.004515            19.399549
Q5 High Spend             442          33.936652 76511.739819            20.076923
```

## Key Patterns for Segmentation
- Responders spend more on average (`+445.45` in `Total_Spend`) and have higher spend per purchase (`+22.08`).
- Highest response by income band: `Q5 High Income` at `30.25%`.
- Highest response by spend band: `Q5 High Spend` at `33.94%`.
- Highest average product spend category is `MntWines` (`305.29`).
- Strongest linear relationship with `Response` among reviewed variables: `Campaign_Acceptance_Total` (`corr=0.427`).

## Notes
- Income distribution chart is clipped at P99 (`94384.00`) for readability; raw values are unchanged.
- This stage is exploratory only: no clustering or segment naming performed.

## Recommended Variables/Themes for Clustering Stage
- Value: `Total_Spend`, `Average_Spend_Per_Purchase`, `Income`.
- Engagement: `Recency`, `Total_Purchases`, `NumWebVisitsMonth`.
- Channel behaviour: channel share features and `Deal_Purchase_Share`.
- Product preference: product spend shares.
- Household context: `Has_Children` / `Household_Children`.

## Generated Figures
- `C:/dev/marketing-segmentation-task/reports/figures/03_total_spend_distribution.png`
- `C:/dev/marketing-segmentation-task/reports/figures/03_income_distribution_clipped_p99.png`
- `C:/dev/marketing-segmentation-task/reports/figures/03_response_rate_by_income_and_spend_bands.png`
- `C:/dev/marketing-segmentation-task/reports/figures/03_average_spend_by_product_category.png`
- `C:/dev/marketing-segmentation-task/reports/figures/03_channel_usage_summary.png`
- `C:/dev/marketing-segmentation-task/reports/figures/03_recency_vs_total_spend_by_response.png`

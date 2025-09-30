# BigQuery-Ecommerce-Analysis
## Data
BigQuery open dataset of a fictitious eCommerce 
clothing site TheLook. The dataset contains information 
about customers, products, orders, logistics, web events 
and digital marketing campaigns. The contents of the dataset are synthetic, and are provided
to industry practitioners for the purpose of product 
discovery, testing, and evaluation.

Because of its artificial nature this dataset have some
limitations or rather simplifications. Most of the items 
were sold only once and its relative revenue contribution 
often equals its sale price.

## Project Overview
I built a pipeline to:
1. Extract Ecommerce store data from **Google BigQuery**.
2. Transform and aggregate metrics with **SQL and Python (pandas)**.
3. Visualize key metrics using **Plotly**.
4. Present results in structured tables and charts.

Resulting data could be used to:
1. Make adjustments for the seasonality in future projections 
2. Find underselling items
3. Focus on specific platform for customer acquisition based on conversion rates and revenue 
4. Create customer cohorts for tailored marketing campaigns

## Results
Data aggrigated by different dimensions:
1. **Time-Based Dimensions (time_based_metrics.csv)**

Metrics: Revenue, AOV, Unique Users, Conversion Rate

![alt text](https://github.com/bgl-d/BigQuery-Ecommerce-Analysis/blob/main/graphs/Revenue%20in%20the%20first%20half%20of%202025.png) Revenue in the first half of 2025
(picture) Traffic in the first half of 2025
(picture) Conversion rates in the first half of 2025

2. **Product Dimensions (products_metrics.csv)**

Metrics: Revenue, ItemsSold, Contribution to Overall Revenue

(picture) Top selling items in 2025 with relative revenue

3. **Acquisition Channels Dimensions (acquisition_channels_metrics.csv)**

Metrics: Traffic, Unique Users, Conversion Rate

(picture) Traffic
(picture) Conversion rates

4. **Customer Dimensions (customer_metrics.csv)**:

Metrics: Revenue, Recency, NumOrders, AvgPurchaseInterval

(picture) NumOrders
(picture) AvgPurchaseInterval











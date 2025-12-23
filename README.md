# BigQuery-Ecommerce-Analysis
## Data
[BigQuery open dataset](https://console.cloud.google.com/bigquery(cameo:product/bigquery-public-data/thelook-ecommerce)?project=single-router-450810-i0) of a fictitious eCommerce 
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
This project involves basic data manipulation for reporting and analysis purposes. 
1. Extract data from **Google BigQuery** with BigQuery Python client library and BigQuery API.
2. Transform and aggregate metrics with **SQL and Python (pandas)**.
3. Visualize key metrics using **Plotly**.
4. Save results in tables and charts.

## Results
Data aggrigated by different dimensions:
1. **Time-Based Dimensions ([time_based_metrics.csv](https://github.com/bgl-d/BigQuery-Ecommerce-Analysis/blob/main/data/time_based_dimension.csv))**

Metrics: Revenue, AOV, Unique Users, Conversion Rate
![alt text](https://github.com/bgl-d/BigQuery-Ecommerce-Analysis/blob/main/graphs/Revenue%20by%20month%20in%20the%20first%20half%20of%202025.png)
![alt text](https://github.com/bgl-d/BigQuery-Ecommerce-Analysis/blob/main/graphs/Conversion%20rates%20in%20the%20first%20half%20of%202025.png)

We can clearly see suspected sesasonality around major holidays. 

2. **Product Dimensions ([products_metrics.csv](https://github.com/bgl-d/BigQuery-Ecommerce-Analysis/blob/main/data/products_dimension.csv))**

Metrics: Revenue, ItemsSold, Contribution to Overall Revenue

![alt text](https://github.com/bgl-d/BigQuery-Ecommerce-Analysis/blob/main/graphs/Products%20revenue.png)
![alt text](https://github.com/bgl-d/BigQuery-Ecommerce-Analysis/blob/main/graphs/Product%20categories%20by%20revenue.png)

3. **Acquisition Channels Dimensions ([acquisition_channels_metrics.csv](https://github.com/bgl-d/BigQuery-Ecommerce-Analysis/blob/main/data/acquisition_channels_dimension.csv)**

Metrics: Traffic, Unique Users, Conversion Rate

![alt text](https://github.com/bgl-d/BigQuery-Ecommerce-Analysis/blob/main/graphs/Traffic%20by%20acquisition%20channel%20in%202025.png)
![alt text](https://github.com/bgl-d/BigQuery-Ecommerce-Analysis/blob/main/graphs/Conversion%20rate%20by%20acquisition%20channel%20in%202025.png)

4. **Customer Dimensions ([customer_metrics.csv](https://github.com/bgl-d/BigQuery-Ecommerce-Analysis/blob/main/data/customers_dimension.csv)**:

Metrics: Revenue, Recency, number of orders, average time between purchases

![alt text](https://github.com/bgl-d/BigQuery-Ecommerce-Analysis/blob/main/graphs/Number%20of%20orders%20by%20an%20individual%20customer.png)
![alt text](https://github.com/bgl-d/BigQuery-Ecommerce-Analysis/blob/main/graphs/Average%20interval%20between%20purchases%20in%20days.png)

**Resulting data could be used for:**
1. Adjustments for the seasonality in future projections or marketing campaigns
2. Finding underselling items
3. Focusing on specific platform for customer acquisition based on conversion rates and revenue
4. Creating customer cohorts for tailored marketing campaigns










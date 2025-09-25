import pandas as pd
from src.load_data import load_data

def seasonality(granularity, start_date, end_date):
    seasonality_query = f'''
                            WITH orders AS (
                              SELECT
                                FORMAT_DATE('{granularity}', created_at) AS Period,
                                SUM(sale_price) AS Revenue,
                                SUM(sale_price)/COUNT(DISTINCT order_id) AS AOV,
                                COUNT(DISTINCT user_id) AS UniqueUsers
                              FROM `bigquery-public-data.thelook_ecommerce.order_items`
                              WHERE status = 'Complete' AND DATE(created_at) BETWEEN '{start_date}' AND '{end_date}'
                              GROUP BY Period
                            ),
                            traffic AS (
                              SELECT 
                                FORMAT_DATE('{granularity}', created_at) AS Period,
                                (COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN session_id END)*100/
                                COUNT(DISTINCT session_id)) AS ConversionRate
                              FROM `bigquery-public-data.thelook_ecommerce.events`
                              WHERE DATE(created_at) BETWEEN '{start_date}' AND '{end_date}'
                              GROUP BY Period
                            )
                            
                            SELECT 
                              o.Period,
                              o.Revenue,
                              o.AOV,
                              o.UniqueUsers,
                              t.ConversionRate
                            FROM orders AS o
                            LEFT JOIN traffic AS t
                              ON o.Period = t.Period
                            ORDER BY o.Period
    '''
    metrics_by_month = load_data(seasonality_query)
    print(metrics_by_month)


def products(start_date, end_date):
    products_query = f'''
                            WITH product_name_fix AS (
                                SELECT CASE WHEN product_name IS NULL OR product_name = '' THEN CAST(o.product_id AS STRING)
                                            ELSE product_name
                                       END AS product_name,
                                       o.product_id
                                FROM `bigquery-public-data.thelook_ecommerce.order_items` AS o
                                LEFT JOIN `bigquery-public-data.thelook_ecommerce.inventory_items` AS inv
                                  ON o.product_id = inv.product_id
                                GROUP BY product_name, product_id
                            )
                            
                            SELECT
                              n.product_name,
                              SUM(o.sale_price) AS Revenue,
                              SUM(o.sale_price) / COUNT(o.order_id) AS AOV,
                              SUM(o.sale_price) * 100 / SUM(SUM(o.sale_price)) OVER() AS Contribution_to_Revenue
                            FROM `bigquery-public-data.thelook_ecommerce.order_items` AS o
                            JOIN product_name_fix AS n
                              ON o.product_id = n.product_id
                            WHERE o.status = 'Complete' 
                              AND DATE(o.created_at) BETWEEN '{start_date}' AND '{end_date}'
                            GROUP BY n.product_name
                            ORDER BY Revenue DESC
    '''
    metrics_by_products = load_data(products_query)
    print(metrics_by_products.head())


def acquisition_channels(start_date, end_date):
    acquisition_channels_query = f'''
                                SELECT traffic_source,
                                  COUNT(DISTINCT session_id) as GeneratedTraffic,
                                  COUNT(DISTINCT user_id) as UniqueUsers,
                                  (COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN session_id END)*100/
                                  COUNT(DISTINCT session_id)) AS ConversionRate,                                  
                                FROM `bigquery-public-data.thelook_ecommerce.events`                                
                                WHERE DATE(created_at) BETWEEN '{start_date}' AND '{end_date}'
                                GROUP BY traffic_source
                                ORDER BY GeneratedTraffic DESC
    '''
    acquisition_channels_metrics = load_data(acquisition_channels_query)
    print(acquisition_channels_metrics)


def customers(start_date, end_date):
    customers_query = f'''
                            SELECT user_id,
                                SUM(sale_price) as CustomerRevenue
                            FROM `bigquery-public-data.thelook_ecommerce.order_items`
                            WHERE DATE(created_at) BETWEEN '{start_date}' AND '{end_date}'
                            GROUP BY user_id
                            ORDER BY CustomerRevenue DESC
                            LIMIT 1000
    '''
    customers_metrics = load_data(customers_query)
    print(customers_metrics.head())

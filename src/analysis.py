import pandas as pd
from src.load_data import load_data


def time_based(granularity, start_date, end_date):
    time_based_query = f'''
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
                            JOIN traffic AS t
                              ON o.Period = t.Period
                            ORDER BY o.Period
    '''
    time_based_dimension = load_data(time_based_query)
    time_based_dimension.to_csv('data/time_based_dimension.csv')
    return time_based_dimension


def products(start_date, end_date):
    products_query = f'''
                            WITH product_name_fix AS (
                                SELECT CASE WHEN product_name IS NULL OR product_name = '' THEN CAST(o.product_id AS STRING)
                                            ELSE product_name
                                       END AS product_name,
                                       o.product_id,
                                       product_category
                                FROM `bigquery-public-data.thelook_ecommerce.order_items` AS o
                                LEFT JOIN `bigquery-public-data.thelook_ecommerce.inventory_items` AS inv
                                  ON o.product_id = inv.product_id
                                GROUP BY product_name, product_id, product_category
                            )
                            
                            SELECT
                              n.product_name,
                              n.product_category,
                              SUM(o.sale_price) AS Revenue,
                              COUNT(o.order_id) AS ItemsSold,
                              SUM(o.sale_price) * 100 / SUM(SUM(o.sale_price)) OVER() AS Contribution_to_Revenue
                            FROM `bigquery-public-data.thelook_ecommerce.order_items` AS o
                            JOIN product_name_fix AS n
                              ON o.product_id = n.product_id
                            WHERE o.status = 'Complete' 
                              AND DATE(o.created_at) BETWEEN '{start_date}' AND '{end_date}'
                            GROUP BY n.product_name, n.product_category
                            ORDER BY Revenue DESC
    '''
    products_dimension = load_data(products_query)
    products_dimension.to_csv('data/products_dimension.csv')
    return products_dimension


def acquisition_channels(granularity, start_date, end_date):
    acquisition_channels_query = f'''
                                SELECT traffic_source,
                                  COUNT(DISTINCT session_id) as GeneratedTraffic,
                                  COUNT(DISTINCT user_id) as UniqueUsers,
                                  (COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN session_id END)*100/
                                  COUNT(DISTINCT session_id)) AS ConversionRate,
                                  FORMAT_DATE('{granularity}', created_at) AS Period                               
                                FROM `bigquery-public-data.thelook_ecommerce.events`                                
                                WHERE DATE(created_at) BETWEEN '{start_date}' AND '{end_date}'
                                GROUP BY traffic_source, Period
                                ORDER BY GeneratedTraffic DESC
    '''
    acquisition_channels_dimension = load_data(acquisition_channels_query)
    acquisition_channels_dimension.to_csv('data/acquisition_channels_dimension.csv')
    return acquisition_channels_dimension


def customers():
    customers_query = f'''
                            WITH last_purchase AS(
                              SELECT user_id, created_at, traffic_source
                              FROM (SELECT *,
                                      ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY created_at DESC) AS row_num,
                                    FROM `bigquery-public-data.thelook_ecommerce.events`
                                    WHERE event_type = 'purchase'
                              )
                              WHERE row_num = 1
                            ),
                            revenue AS(
                              SELECT user_id,
                                SUM(sale_price) as CustomerRevenue,
                                COUNT(order_id) as NumOrders,
                                status
                              FROM `bigquery-public-data.thelook_ecommerce.order_items`
                              GROUP BY user_id, status
                            ),
                            date_dif AS(
                              SELECT user_id, sum(day_dif)/NULLIF(COUNT(order_id)-1, 0) as AvgPurchaseInterval
                              FROM (
                                SELECT *, DATE_diff(created_at, LAG(created_at, 1) OVER (PARTITION BY user_id order by created_at), 
                                day) as day_dif
                                FROM `bigquery-public-data.thelook_ecommerce.orders` 
                                WHERE status = 'Complete'
                              )
                              GROUP BY user_id
                            )
                            
                            SELECT
                              u.first_name,
                              u.last_name,
                              u.city,
                              u.country,
                              r.CustomerRevenue,
                              r.NumOrders,
                              u.traffic_source as FirstTouchTrafficSource,
                              l.created_at as Recency,
                              d.AvgPurchaseInterval
                            FROM `bigquery-public-data.thelook_ecommerce.users` as u
                            JOIN last_purchase as l
                              ON u.id = l.user_id
                            JOIN revenue AS r
                              ON u.id = r.user_id
                            JOIN date_dif AS d
                              ON u.id = d.user_id
                            WHERE r.status = 'Complete'
                            ORDER BY CustomerRevenue DESC
    '''
    customers_dimension = load_data(customers_query)
    customers_dimension.to_csv('data/customers_dimension.csv')
    return customers_dimension

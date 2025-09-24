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
                                COUNT(session_id)) AS ConversionRate
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
                        '''
    metrics_by_month = load_data(seasonality_query)
    print(metrics_by_month)


def products(start_date, end_date):
    products_query = f'''
                            SELECT 
                              inv.product_name,
                              sum(o.sale_price) as Revenue,
                              sum(o.sale_price)/count(o.order_id) as AOV,
                              sum(o.sale_price) * 100 / SUM(SUM(o.sale_price)) OVER() as Contribution_to_Revenue
                            FROM `bigquery-public-data.thelook_ecommerce.order_items` AS o
                            LEFT JOIN (select product_name, id
                                        FROM `bigquery-public-data.thelook_ecommerce.inventory_items`
                                        WHERE created_at BETWEEN '{start_date}' AND '{end_date}'
                                        GROUP BY product_name, id) AS inv 
                                ON o.product_id = inv.id
                            WHERE o.status = 'Complete' AND DATE(o.created_at) BETWEEN '{start_date}' AND '{end_date}'
                            GROUP BY inv.product_name
                            ORDER BY sum(o.sale_price) DESC
                        '''
    metrics_by_products = load_data(products_query)
    print(metrics_by_products.head())


def acquisition_channels(start_date, end_date):
    acquisition_channels_query = f'''
                                WITH first_touch AS(
                                  SELECT user_id, 
                                    min(created_at) as first_touch
                                  FROM `bigquery-public-data.thelook_ecommerce.events`
                                  WHERE DATE(created_at) BETWEEN '{start_date}' AND '{end_date}'
                                  GROUP BY user_id
                                  
                                ),
                                first_touch_source AS(
                                  SELECT f.user_id, 
                                    e.traffic_source
                                  FROM first_touch as f
                                  JOIN `bigquery-public-data.thelook_ecommerce.events` as e
                                    ON f.user_id = e.user_id AND f.first_touch = e.created_at
                                )
    
                                SELECT f_s.traffic_source,
                                  COUNT(DISTINCT e.session_id) as GeneratedTraffic,
                                  COUNT(DISTINCT e.user_id) as UniqueUsers,
                                  (COUNT(DISTINCT CASE WHEN e.event_type = 'purchase' THEN e.session_id END)*100/
                                  COUNT(e.session_id)) AS ConversionRate,
                                  COUNT(f_s.user_id) as NumberOfFirstTouches
                                FROM `bigquery-public-data.thelook_ecommerce.events` AS e
                                JOIN first_touch_source as f_s
                                    ON e.user_id = f_s.user_id
                                WHERE DATE(e.created_at) BETWEEN '{start_date}' AND '{end_date}'
                                GROUP BY f_s.traffic_source
                                ORDER BY COUNT(DISTINCT e.session_id) DESC
                            '''
    acquisition_channels_metrics = load_data(acquisition_channels_query)
    print(acquisition_channels_metrics.head())

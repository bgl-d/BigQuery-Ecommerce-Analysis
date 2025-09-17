from src.load_data import load_data
from src.data_preprocessing import data_inspection
from src.analysis import sales_metrics, traffic_metrics, merge_metrics
import pandas as pd
import numpy as np
import plotly.express as px


def main():
    # Terminal display settings
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 400)
    np.set_printoptions(linewidth=400)

    # Querying data from bigquery
    orders_query = '''
                    SELECT o.order_id,
                        o.user_id,
                        o.product_id,
                        DATE(o.created_at) AS date,
                        FORMAT_DATE('%Y-%m', o.created_at) AS month,
                        FORMAT_DATE('%Y', o.created_at) AS year,
                        o.status,
                        o.sale_price * num_o.num_of_item AS sales,
                        inv.product_name
                    FROM `bigquery-public-data.thelook_ecommerce.order_items` AS o
                    LEFT JOIN 
                        `bigquery-public-data.thelook_ecommerce.orders` AS num_o ON o.order_id = num_o.order_id
                    LEFT JOIN
                        `bigquery-public-data.thelook_ecommerce.inventory_items` AS inv ON o.product_id = inv.product_id
                    WHERE DATE(o.created_at) <= current_date AND o.status = 'Complete'
                '''

    sessions_query = '''
                        SELECT session_id,
                            user_id,
                            DATE(created_at) as date,
                            FORMAT_DATE('%Y-%m', created_at) AS month,
                            FORMAT_DATE('%Y', created_at) AS year,
                            city,
                            state,
                            traffic_source,
                            event_type
                        FROM `bigquery-public-data.thelook_ecommerce.events`
                        WHERE DATE(created_at) < current_date
                    '''
    # Load data
    df_traffic = load_data(sessions_query)
    df_sales = load_data(orders_query)

    # Data cleaning
    df_traffic = data_inspection(df_traffic)
    df_sales = data_inspection(df_sales)

    # Calculate key metrics at the end of previous month
    dimension = 'month'
    df_sales_metrics = sales_metrics(df_sales, dimension)
    df_traffic_metrics = traffic_metrics(df_traffic, [dimension])
    df_metrics = merge_metrics(df_sales_metrics, df_traffic_metrics)

    # Visualising key metrics
    fig = px.line(df_metrics[df_metrics.index < '2025-09-01'],
                  x=df_metrics[df_metrics.index < '2025-09-01'].index,
                  y='revenue')
    fig.show()


if __name__ == '__main__':
    main()

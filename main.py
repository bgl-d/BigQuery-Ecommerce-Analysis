from src.load_data import load_data
from src.data_preprocessing import data_inspection
from src.analysis import metrics
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
                            city,
                            state,
                            traffic_source,
                            event_type
                        FROM `bigquery-public-data.thelook_ecommerce.events`
                        WHERE DATE(created_at) < current_date
                    '''
    # Load data
    df_sessions = load_data(sessions_query)
    df_orders = load_data(orders_query)

    # Data cleaning
    df_sessions = data_inspection(df_sessions)
    df_orders = data_inspection(df_orders)

    # Calculate key metrics at the end of previous month
    df_metrics = metrics(df_orders, df_sessions)
    print(df_metrics[df_metrics.index.year == 2025])

    # Visualising key metrics
    fig = px.line(df_metrics[df_metrics.index < '2025-09-01'],
                  x=df_metrics[df_metrics.index < '2025-09-01'].index,
                  y='revenue')
    fig.show()


if __name__ == '__main__':
    main()

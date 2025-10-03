from src.analysis import time_based, products, acquisition_channels, customers
import pandas as pd
import numpy as np
import plotly.express as px


def main():
    # Terminal display settings
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 400)
    np.set_printoptions(linewidth=400)

    # Choose period
    start_date = '2025-01-01'
    end_date = '2025-06-30'

    # Aggregate data and calculate metrics
    # Time-based data
    time_based_dimension = time_based('%Y-%m', start_date, end_date)

    # Product data
    products_dimension = products(start_date, end_date)

    # Acquisition channels data
    acquisition_channels_dimension = acquisition_channels(start_date, end_date)

    # Customer data
    customers_dimension = customers()

    # Charts
    # Revenue and traffic in 2025
    revenue_fig = px.histogram(time_based_dimension,
                       x='Period',
                       y='Revenue', nbins=8)
    revenue_fig.update_layout(bargap=0.2)
    traffic_by_month_fig = px.histogram(time_based_dimension,
                            x='Period',
                            y='GeneratedTraffic', color='traffic_source', barmode='group', nbins=8)
    revenue_fig.show()
    traffic_by_month_fig.show()

    # Acquisitions channels
    channel_traffic_fig = px.histogram(acquisition_channels_dimension,
                                       x='traffic_source',
                                       y='ConversionRate')
    channel_traffic_fig.show()

    # Average number days between purchases
    customers_fig = px.histogram(customers_dimension,
                                 x='AvgPurchaseInterval')
    customers_fig.show()

    # Total number of orders from an individual customer
    customers_fig2 = px.histogram(customers_dimension,
                                 x='NumOrders')
    customers_fig2.update_layout(bargap=0.1)
    customers_fig2.show()

    # Top 10 product categories
    categories = (products_dimension[['product_category', 'Revenue']].groupby('product_category').sum()
                  .sort_values(by='Revenue', ascending=False).reset_index())
    categories_fig = px.histogram(categories.head(10),
                                  x='product_category',
                                  y='Revenue')
    categories_fig.show()

    # 10 top-selling items
    products_fig = px.histogram(products_dimension.head(10),
                                x='product_name',
                                y='Revenue')
    products_fig.show()


if __name__ == '__main__':
    main()

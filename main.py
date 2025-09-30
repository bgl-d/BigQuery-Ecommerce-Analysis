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

    # Calculate time-based metrics
    time_based_dimension = time_based('%Y-%m', start_date, end_date)

    # Calculate product metrics
    product_metrics = products(start_date, end_date)

    # Calculate acquisition channel metrics
    acquisition_channels_dimension = acquisition_channels('%Y-%m', start_date, end_date)

    # Calculate customer metrics
    customers_dimension = customers()

    # Visualisations
    revenue_fig = px.histogram(time_based_dimension,
                       x='Period',
                       y='Revenue', nbins=8)
    revenue_fig.update_layout(bargap=0.2)
    revenue_fig.show()

    acquisition_channels_fig = px.histogram(acquisition_channels_dimension,
                            x='Period',
                            y='GeneratedTraffic', color='traffic_source', barmode='group', nbins=8)
    acquisition_channels_fig.show()

    customers_fig = px.histogram(customers_dimension,
                                 x='AvgPurchaseInterval')
    customers_fig2 = px.histogram(customers_dimension,
                                 x='NumOrders')
    customers_fig2.update_layout(bargap=0.1)
    customers_fig.show()
    customers_fig2.show()


if __name__ == '__main__':
    main()

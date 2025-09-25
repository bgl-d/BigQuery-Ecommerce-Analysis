from src.analysis import seasonality, products, acquisition_channels, customers
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

    # Metrics by month
    metrics_by_period = seasonality('%Y-%m', start_date, end_date)

    # Metrics by product
    metrics_by_products = products(start_date, end_date)

    # Metrics by acquisition channel
    acquisition_channels_metrics = acquisition_channels('%Y-%m', start_date, end_date)

    # Customer metrics
    customers_metrics = customers(start_date, end_date)

    # Visualising key metrics
    fig = px.histogram(metrics_by_period,
                       x=metrics_by_period['Period'],
                       y='Revenue')
    fig.show()
    fig_hist = px.histogram(acquisition_channels_metrics,
                            x='Period',
                            y='GeneratedTraffic', color='traffic_source', barmode='group')
    fig_hist.show()


if __name__ == '__main__':
    main()

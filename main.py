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
    customers_metrics = customers()

    # Visualising key metrics
    revenue_fig = px.histogram(metrics_by_period,
                       x='Period',
                       y='Revenue', nbins=8)
    revenue_fig.update_layout(bargap=0.2)
    revenue_fig.show()


    acquisition_channels_fig = px.histogram(acquisition_channels_metrics,
                            x='Period',
                            y='GeneratedTraffic', color='traffic_source', barmode='group', nbins=8)
    acquisition_channels_fig.show()

    customers_fig = px.histogram(customers_metrics,
                                 x='AvgRepeatPurchaseInterval')
    customers_fig2 = px.histogram(customers_metrics,
                                 x='NumOrders')
    customers_fig2.update_layout(bargap=0.1)
    customers_fig.show()
    customers_fig2.show()




if __name__ == '__main__':
    main()

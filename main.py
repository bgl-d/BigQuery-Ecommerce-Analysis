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
    seasonality('%Y-%m', start_date, end_date)

    # Metrics by product
    products(start_date, end_date)

    # Metrics by acquisition channel
    acquisition_channels(start_date, end_date)

    # Customer metrics
    customers(start_date, end_date)


if __name__ == '__main__':
    main()

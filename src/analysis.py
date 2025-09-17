import pandas as pd


def sales_metrics(df_sales, dimension):
    # Calculate total sales, number of orders, AOV
    order_metrics = df_sales.groupby(dimension).agg(
        num_orders=('order_id', 'nunique'),
        revenue=('sales', 'sum')
    )
    order_metrics['aov'] = order_metrics['revenue'] / order_metrics['num_orders']

    # Top-selling products
    revenue_per_item = df_sales.groupby([dimension, 'product_name']).agg(
        top_product_revenue=('sales', 'sum')
    )
    bestseller = (revenue_per_item.loc[revenue_per_item
                  .groupby(dimension)['top_product_revenue'].idxmax()]
                  .reset_index('product_name'))
    bestseller = bestseller.rename(columns={'product_name': 'bestseller'})
    grouped_sales = pd.merge(order_metrics, bestseller, on=dimension, how='left')
    return grouped_sales


def traffic_metrics(df_traffic, dimension):
    # Calculate number of sessions, conversion rate, cart abandonment rate
    grouped_traffic = df_traffic.groupby(dimension).agg(
        num_sessions=('session_id', 'nunique'),
        num_purchases=('event_type', lambda x: (x == 'purchase').sum()),
        num_created_carts=('event_type', lambda x: (x == 'cart').sum())
    )
    grouped_traffic['cvr'] = grouped_traffic['num_purchases'] * 100 / grouped_traffic['num_sessions']
    grouped_traffic['car'] = ((grouped_traffic['num_created_carts'] - grouped_traffic['num_purchases']) * 100
                              / grouped_traffic['num_sessions'])
    return grouped_traffic


def merge_metrics(sales, traffic):
    df_metrics = pd.merge(sales, traffic, left_index=True, right_index=True)
    return df_metrics

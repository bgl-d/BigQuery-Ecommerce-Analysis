import pandas as pd


def metrics(df_orders, df_sessions):
    # Calculate total sales, number of orders, AOV
    order_metrics = df_orders.groupby(pd.Grouper(key='date', freq='ME')).agg(
        num_orders=('order_id', 'nunique'),
        revenue=('sales', 'sum')
    )
    order_metrics['aov'] = order_metrics['revenue'] / order_metrics['num_orders']

    # Calculate number of sessions, conversion rate, cart abandonment rate
    session_metrics = df_sessions.groupby(pd.Grouper(key='date', freq='ME')).agg(
        num_sessions=('session_id', 'nunique'),
        num_purchases=('event_type', lambda x: (x == 'purchase').sum()),
        num_created_carts=('event_type', lambda x: (x == 'cart').sum()),
        organic_traffic=('traffic_source', lambda x: (x == 'Organic').sum()),
        adwords_traffic=('traffic_source', lambda x: (x == 'Adwords').sum()),
        facebook_traffic=('traffic_source', lambda x: (x == 'Facebook').sum()),
        email_traffic=('traffic_source', lambda x: (x == 'Email').sum()),
        youtube_traffic=('traffic_source', lambda x: (x == 'YouTube').sum()),
    )
    session_metrics['cvr'] = session_metrics['num_purchases'] * 100 / session_metrics['num_sessions']
    session_metrics['car'] = ((session_metrics['num_created_carts'] - session_metrics['num_purchases']) * 100
                              / session_metrics['num_sessions'])
    df_metrics = pd.merge(order_metrics, session_metrics, left_index=True, right_index=True)

    # Top-selling products
    revenue_per_item = (df_orders.groupby([pd.Grouper(key='date', freq='ME'), 'product_name']).agg(
        top_product_revenue=('sales', 'sum')
    ))
    bestseller = (revenue_per_item.loc[revenue_per_item
                   .groupby('date')['top_product_revenue'].idxmax()]
                   .reset_index('product_name'))
    bestseller = bestseller.rename(columns={'product_name': 'bestseller'})
    df_metrics = pd.merge(df_metrics, bestseller, on='date', how='left')
    df_metrics.to_csv('data/metrics.csv')
    return df_metrics

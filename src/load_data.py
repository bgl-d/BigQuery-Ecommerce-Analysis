from google.cloud import bigquery
import os
import pandas as pd
from sql_metadata.compat import get_query_tables


def load_data(query):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'Cloud_key_file.json'

    # Initialize a BigQuery client
    client = bigquery.Client()

    # Execute the query and load results into a Pandas DataFrame
    df = client.query(query)
    df = df.to_dataframe()

    # Save table data in .csv file
    df.name = get_query_tables(query)[0].rsplit('.', 1)[-1]
    df['date'] = pd.to_datetime(df['date'])
    return df

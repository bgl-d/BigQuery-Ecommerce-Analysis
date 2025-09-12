def data_inspection(df):
    print('-' * 20)
    print(df.name)
    print('-' * 20)

    # Check for data type errors
    print(df.info(), '\n')

    # Check for missing values
    print('Missing values: ', '\n', df.isnull().sum(), '\n')

    # Duplicates
    if df.duplicated().sum() != 0:
        df = df.drop_duplicates()

    # Sort by dates
    df = df.sort_values('date')

    # Days between purchases, website visits
    df['previous_visit'] = df.groupby(['user_id'])['date'].shift()
    df['days_bw_visits'] = df['date'] - df['previous_visit']
    df['days_bw_visits'] = df['days_bw_visits'].apply(lambda x: x.days)
    df['AvgDaysBetween'] = df[df['days_bw_visits'] > 0].groupby('user_id')['days_bw_visits'].mean()
    return df

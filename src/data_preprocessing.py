def data_inspection(df):
    print('-' * 20)
    print(df.name)
    print('-' * 20)

    # Check for data type errors
    print(df.info() , '\n')

    # Check for missing values
    print('Missing values: ', '\n', df.isnull().sum(), '\n')

    # Duplicates
    if df.duplicated().sum() != 0:
        df = df.drop_duplicates()
    return df

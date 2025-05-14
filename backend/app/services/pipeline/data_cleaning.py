import pandas as pd


def clean_global_stats_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and transforms dataframe containing global statistics data.

    Steps:
    - Convert date strings to datetime objects.
    - Strip whitespace from column names.
    -Ensure numeric columns are properly formatted.
    - Handle misisng values.

    Args:
        df (pd.DataFrame): Raw dataframe loaded from the CSV

    Returns:
        pd.DataFrame: The cleaned DataFrame ready for further processing or
        insertion into the database.
    """

    df['item_date_published'] = pd.to_datetime(df['item_date_published'], errors='coerce')

    df = df.dropna(subset=['item_date_published'])

    df['country'] = df['country'].str.strip()

    numeric_columns = ['num_newspaper', 'num_feeds', 'av_sents', 'num_news']

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df[numeric_columns] = df[numeric_columns].fillna(0)

    return df

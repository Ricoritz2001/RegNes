import pandas as pd


def transform_data(
    global_df: pd.DataFrame, 
    regional_df: pd.DataFrame, 
    regions_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Transforms and merges global and regional datasets:
      1. Standardize country names.
      2. Merge regional data with region metadata.
      3. Aggregate regional metrics by date.
      4. Merge aggregated regional metrics back into global stats.

    Args:
        global_df (pd.DataFrame): Global statistics DataFrame.
        regional_df (pd.DataFrame): Regional metrics DataFrame.
        regions_df (pd.DataFrame): Regions metadata DataFrame.
    
    Returns:
        pd.DataFrame: A merged DataFrame ready for database insertion or API serving.
    """
    # 1. Standardize country names
    global_df['country'] = global_df['country'].str.title()
    regional_df['Country'] = regional_df['Country'].str.title()
    
    # 2. Merge regional data with region metadata
    combined = regional_df.merge(
        regions_df, 
        left_on='region_id', 
        right_on='region_id', 
        how='left'
    )
    
    # 3. Aggregate regional metrics by date
    regional_agg = (
        combined
        .groupby('item_date_published')
        .agg({
            'val_av': 'mean',
            'happiness_av': 'mean',
            'rauh_sents_av': 'mean'
        })
        .rename(columns={
            'val_av': 'val_mean',
            'happiness_av': 'happiness_mean',
            'rauh_sents_av': 'sentiment_mean'
        })
        .reset_index()
    )
    
    # 4. Merge aggregated regional metrics into global stats
    merged_df = global_df.merge(
        regional_agg, 
        on='item_date_published', 
        how='left'
    )
    
    return merged_df

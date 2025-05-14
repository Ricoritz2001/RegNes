import pandas as pd
import numpy as np


def validate_region_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validates the regions DataFrame:
      - Required columns exist.
      - region_id is integer & unique.
      - region_name and country are non-empty strings.
    """
    required = ["region_id", "region_name", "country"]
    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f"Regions missing required columns: {missing}")

    # region_id
    if not pd.api.types.is_integer_dtype(df["region_id"]):
        raise ValueError("region_id must be integer")
    if df["region_id"].duplicated().any():
        raise ValueError("region_id contains duplicates")

    # region_name / country
    for col in ["region_name", "country"]:
        if not pd.api.types.is_string_dtype(df[col]):
            raise ValueError(f"{col} must be string")
        if (df[col].str.strip() == "").any():
            raise ValueError(f"{col} contains empty values")

    return df


def validate_regional_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validates the regional_data DataFrame:
      - Required columns exist.
      - region_id is integer and non-negative.
      - item_date_published is datetime.
      - num_papers & num_news are non-negative integers.
      - share & average columns are floats.
      - num_words is a non-negative float.
      - Infinite values in float cols are replaced with NaN → 0.
    """
    required = [
        "region_id",
        "item_date_published",
        "num_words",
        "rauh_sents_share",
        "rauh_sents_av",
        "happiness_share",
        "happiness_av",
        "val_share",
        "val_av",
        "num_papers",
        "num_news",
    ]
    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f"RegionalData missing required columns: {missing}")

    # Clean out infinities before any numeric checks
    float_cols = [
        "num_words",
        "rauh_sents_share", "rauh_sents_av",
        "happiness_share", "happiness_av",
        "val_share", "val_av",
    ]
    df[float_cols] = df[float_cols].replace([np.inf, -np.inf], np.nan).fillna(0)

    # region_id
    if not pd.api.types.is_integer_dtype(df["region_id"]):
        raise ValueError("region_id must be integer")
    if (df["region_id"] < 0).any():
        raise ValueError("region_id contains negative values")

    # item_date_published
    if not pd.api.types.is_datetime64_any_dtype(df["item_date_published"]):
        raise ValueError("item_date_published must be datetime")

    # counts: non-negative ints
    for col in ["num_papers", "num_news"]:
        if not pd.api.types.is_integer_dtype(df[col]):
            raise ValueError(f"{col} must be integer")
        if (df[col] < 0).any():
            raise ValueError(f"{col} contains negative values")

    # shares & averages: just ensure float dtype
    for col in [
        "rauh_sents_share", "rauh_sents_av",
        "happiness_share", "happiness_av",
        "val_share", "val_av",
    ]:
        if not pd.api.types.is_float_dtype(df[col]):
            raise ValueError(f"{col} must be float")

    # num_words: non-negative float
    if not pd.api.types.is_float_dtype(df["num_words"]):
        raise ValueError("num_words must be float")
    if (df["num_words"] < 0).any():
        raise ValueError("num_words contains negative values")

    return df


def validate_global_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validates global_stats DataFrame:
      - Ensures required columns exist.
      - item_date_published is datetime.
      - Numeric count columns are non-negative.
      - country has no empty strings.
      (av_sents is allowed to be negative.)
    """
    required = [
        "item_date_published",
        "country",
        "num_newspaper",
        "num_feeds",
        "av_sents",
        "num_news",
    ]
    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Date check
    if not pd.api.types.is_datetime64_any_dtype(df["item_date_published"]):
        raise ValueError("item_date_published must be datetime")

    # Only enforce non-negative on count columns:
    for col in ["num_newspaper", "num_feeds", "num_news"]:
        if (df[col] < 0).any():
            raise ValueError(f"column {col} contains negative values")

    # country must be non-empty
    if (df["country"].str.strip() == "").any():
        raise ValueError("Empty country value found")

    return df

import os
import pandas as pd
from flask import current_app
from app import db
from sqlalchemy import delete
from app.models.data_models import Regions, RegionalData, GlobalStats
from app.services.pipeline.data_readers import read_region_names, read_regional_news, read_global_stats
from app.services.pipeline.data_cleaning import clean_global_stats_df
from app.services.pipeline.data_validation import (
    validate_global_stats,
    validate_region_names,
    validate_regional_data,
)


def ingest(data_folder: str):
    # Clear existing data 
    db.session.execute(delete(RegionalData))
    db.session.execute(delete(GlobalStats))
    db.session.execute(delete(Regions))
    db.session.commit()

    # Ingest Regions 
    regions_fp = os.path.join(data_folder, "region_names.xlsx")
    df_regions = read_region_names(regions_fp)
    df_regions = df_regions.rename(columns={
        "Region": "region_id",
        "ROR.NAME": "region_name",
        "Country": "country",
    })
    df_regions["region_id"] = pd.to_numeric(df_regions["region_id"],
                                            errors="coerce")
    df_regions = df_regions.dropna(subset=["region_id"])
    df_regions["region_id"] = df_regions["region_id"].astype(int)
    df_regions["region_name"] = df_regions["region_name"].str.strip()
    df_regions["country"] = df_regions["country"].str.strip()
    df_regions = validate_region_names(df_regions)

    db.session.bulk_insert_mappings(
        Regions,
        df_regions[["region_id", "region_name", "country"]]
            .drop_duplicates()
            .to_dict(orient="records")
    )
    db.session.commit()

    # ─── 3) Ingest Regional Data ──────────────────────────────
    regional_fp = os.path.join(data_folder, "Regional_news.csv")
    df_regional = read_regional_news(regional_fp)
    for col in [
        "num_words", "rauh_sents_share", "rauh_sents_av",
        "Happiness_share", "Happiness_av",
        "Val_share", "Val_av",
        "num_papers", "num_news"
    ]:
        df_regional[col] = pd.to_numeric(df_regional[col], errors="coerce"
                                         ).fillna(0)

    df_regional = df_regional.rename(columns={
        "Region": "region_id",
        "Happiness_share": "happiness_share",
        "Happiness_av":    "happiness_av",
        "Val_share":       "val_share",
        "Val_av":          "val_av",
    })
    df_regional["region_id"] = pd.to_numeric(df_regional["region_id"],
                                             errors="coerce")
    df_regional = df_regional.dropna(subset=["region_id"])
    df_regional["region_id"] = df_regional["region_id"].astype(int)
    df_regional = validate_regional_data(df_regional)

    regional_records = df_regional[[
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
    ]].to_dict(orient="records")
    db.session.bulk_insert_mappings(RegionalData, regional_records)
    db.session.commit()

    # ─── 4) Ingest Global Stats ───────────────────────────────
    global_fp = os.path.join(data_folder, "global.stats.csv")
    df_global = read_global_stats(global_fp)
    df_global = df_global.rename(columns={
        "Country":       "country",
        "num.newspaper": "num_newspaper",
        "num.feeds":     "num_feeds",
        "av.sents":      "av_sents",
        "num.news":      "num_news",
    })
    df_global = clean_global_stats_df(df_global)
    df_global = validate_global_stats(df_global)

    global_records = df_global[[
        "country",
        "item_date_published",
        "num_newspaper",
        "num_feeds",
        "av_sents",
        "num_news",
    ]].to_dict(orient="records")
    db.session.bulk_insert_mappings(GlobalStats, global_records)
    db.session.commit()

    print("Data ingestion complete.")

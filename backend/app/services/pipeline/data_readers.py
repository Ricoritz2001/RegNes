import os
import pandas as pd


def read_region_names(path: str) -> pd.DataFrame:
    """
    Reads the region names file, whether it's a TSV or an Excel workbook.
    Expects columns: Region, ROR.NAME, Country
    """
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xls", ".xlsx"):
        # your file is actually an Excel sheet
        return pd.read_excel(path, engine="openpyxl")
    # fallback to tab-delimited text
    return pd.read_csv(
        path,
        sep="\t",
        quotechar='"',
        dtype={
            "Region": int,
            "ROR.NAME": str,
            "Country": str,
        },
        engine="c",
    )


def read_regional_news(path: str) -> pd.DataFrame:
    """
    Reads only the columns we need from the comma-delimited Regional_news.csv.
    This prevents stray values (like 'Deutschland' in Country) from
    shifting columns.
    """
    return pd.read_csv(
        path,
        sep=",",
        quotechar='"',
        usecols=[
            "Region",
            "item_date_published",
            "num_words",
            "rauh_sents_share",
            "rauh_sents_av",
            "Happiness_share",
            "Happiness_av",
            "Val_share",
            "Val_av",
            "num_papers",
            "num_news",
        ],
        parse_dates=["item_date_published"],
        engine="c",
    )


def read_global_stats(path: str) -> pd.DataFrame:
    """
    Reads only the six columns we care about from the semicolon-delimited
    global_stats file, using the Python engine to cope with the extra
    row-id column.
    """
    return pd.read_csv(
        path,
        sep=";",
        quotechar='"',
        usecols=[
            "Country",
            "item_date_published",
            "num.newspaper",
            "num.feeds",
            "av.sents",
            "num.news",
        ],
        parse_dates=["item_date_published"],
        engine="python",
    )

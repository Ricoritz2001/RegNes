import os
import geopandas as gpd
import pandas as pd
from flask import current_app
from sqlalchemy import func
from app import db
from app.models.data_models import RegionalData


def generate_regions_geojson() -> str:
    """
    Generates a GeoJSON file that maps regions to their most recent sentiment
    data.

    Steps:
    1. Load the shapefile containing region boundaries.
    2. Ensure it uses a GPS-compatible coordinate system (WGS84).
    3. Extract and convert the region identifier (region_id) from the
        shapefile.
    4. Query the latest sentiment values per region from the database.
    5. Merge the sentiment data into the shapefile's geometry data.
    6. Save the result as GeoJSON and return it as a JSON string.
    """

    # 1) Locate shapefile in the configured raw shapefile directory
    shp_dir = current_app.config["RAW_SHP_DIR"]
    shp_files = [f for f in os.listdir(shp_dir) if f.lower().endswith(".shp")]
    if not shp_files:
        raise FileNotFoundError(f"No .shp file found in {shp_dir}")
    shp_path = os.path.join(shp_dir, shp_files[0])

    # 2) Read shapefile into a GeoDataFrame
    gdf = gpd.read_file(shp_path)

    # 2b) Ensure GeoDataFrame is using WGS84 (EPSG:4326) for lat/lon compatibility
    if gdf.crs is None:
        raise ValueError("Shapefile has no coordinate reference system (CRS) defined.")
    if gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs(epsg=4326)

    # 3) Extract 'region_id' from the 'ROR1217' column
    if "ROR1217" not in gdf.columns:
        raise KeyError(f"Expected 'ROR1217' column in shapefile, found: {gdf.columns.tolist()}")
    gdf["region_id"] = pd.to_numeric(gdf["ROR1217"], errors="coerce").astype("Int64")

    # 4) Query the most recent sentiment records per region from the database
    subq = (
        db.session.query(
            RegionalData.region_id,
            func.max(RegionalData.item_date_published).label("latest_ts")
        )
        .group_by(RegionalData.region_id)
        .subquery()
    )

    latest_rows = (
        db.session.query(RegionalData)
          .join(
              subq,
              (RegionalData.region_id == subq.c.region_id) &
              (RegionalData.item_date_published == subq.c.latest_ts)
          )
        .all()
    )

    # Convert the SQLAlchemy result into a DataFrame for merging
    df = pd.DataFrame([{
        "region_id": row.region_id,
        "rauh_sents_av": row.rauh_sents_av,
        "happiness_av": row.happiness_av,
        "val_av": row.val_av
    } for row in latest_rows]).set_index("region_id")

    # 5) Merge the sentiment data into the GeoDataFrame by region_id
    gdf = gdf.merge(df, on="region_id", how="left")

    # 6) Write the final GeoDataFrame as GeoJSON to disk and return the content
    out_path = current_app.config["PROCESSED_GEOJSON"]
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    print("DEBUG: Writing GeoJSON to:", out_path)
    gdf.to_file(out_path, driver="GeoJSON")

    return gdf.to_json()

import os
from io import StringIO

import pytest
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

from app.services.data_ingestion import read_csv, read_excel, read_complete_shapefile

def test_read_csv_with_semicolon_and_comma(tmp_path):
    # Create a sample CSV with both commas and semicolons
    data = "a;b,c\n1;2,3\n4;5,6"
    file = tmp_path / "mixed.csv"
    file.write_text(data, encoding="utf-8")

    df = read_csv(str(file))
    # Expect pandas to split on both ; and ,
    assert list(df.columns) == ["a", "b", "c"]
    # Values should be parsed correctly
    assert df.loc[0, "a"] == "1"
    assert df.loc[0, "b"] == "2"
    assert df.loc[0, "c"] == "3"

def test_read_excel(tmp_path):
    # Create a sample DataFrame and write to Excel
    df_in = pd.DataFrame({
        "region_id": [1, 2],
        "region_name": ["A", "B"]
    })
    file = tmp_path / "regions.xlsx"
    df_in.to_excel(str(file), index=False)

    df_out = read_excel(str(file))
    # Columns and values should round‑trip
    assert list(df_out.columns) == ["region_id", "region_name"]
    pd.testing.assert_frame_equal(df_in, df_out)

def test_read_complete_shapefile(tmp_path):
    # Create a simple GeoDataFrame and write a shapefile
    gdf_in = gpd.GeoDataFrame(
        {"id": [1], "value": [42]},
        geometry=[Point(0, 0)],
        crs="EPSG:4326"
    )
    shp_folder = tmp_path / "shapefiles"
    shp_folder.mkdir()
    base = "test_region"
    # GeoPandas will write .shp, .shx, .dbf, .prj, etc.
    gdf_in.to_file(str(shp_folder / f"{base}.shp"))

    # Now read it back
    gdf_out = read_complete_shapefile(str(shp_folder), base)
    # Check that we got the same schema and one row
    assert list(gdf_out.columns).count("geometry") == 1
    assert gdf_out.loc[0, "value"] == 42
    # Geometry should match
    assert gdf_out.geometry.iloc[0].equals(Point(0, 0))

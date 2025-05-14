import os
import json
import geopandas as gpd
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from sqlalchemy import func
from app import db
from app.models.data_models import RegionalData, Regions

bp = Blueprint('heatmap', __name__, url_prefix='/api/map/heat')

METRIC_MAP = {
    'sentiment_mean': RegionalData.rauh_sents_av,
    'valenz_mean': RegionalData.val_av,
    'happiness_mean': RegionalData.happiness_av
}

@bp.route('', methods=["GET"])
def heatmap():
    """
    GET /api/map/heat
    Query parameters:
        - metric (str): one of the keys in METRIC_MAP
        - date (optional): YYYY-MM-DD. Defaults to the latest available date.

    Returns:
        GeoJSON FeatureCollection with:
        - geometry
        - region_id
        - region name (from DB)
        - selected metric value
    """

    # Metric validation
    metric_key = request.args.get('metric')
    if metric_key not in METRIC_MAP:
        return jsonify({"error": "Invalid metric key"}), 400

    # Date handling
    date_str = request.args.get('date')
    if date_str:
        try:
            target_date = datetime.fromisoformat(date_str).date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
    else:
        latest = db.session.query(func.max(RegionalData.item_date_published)).scalar()
        if not latest:
            return jsonify({"error": "No data available."}), 404
        target_date = latest

    # Query metric values
    metric_col = METRIC_MAP[metric_key].label('value')
    value_rows = (
        db.session.query(RegionalData.region_id, metric_col)
        .filter(RegionalData.item_date_published == target_date)
        .all()
    )
    value_map = {rid: val for rid, val in value_rows}

    # Query region names
    name_rows = db.session.query(Regions.region_id, Regions.region_name).all()
    name_map = {rid: name for rid, name in name_rows}

    # Load shapefile
    shp_path = os.path.join(current_app.root_path, 'data', 'raw', 'shapefiles', 'Deutsch.shp')
    try:
        regions_gdf = gpd.read_file(shp_path)[['ROR1217', 'geometry']]
    except Exception as e:
        return jsonify({"error": f"Error reading shapefile: {str(e)}"}), 500

    regions_gdf = regions_gdf.rename(columns={'ROR1217': 'region_id'}).set_index('region_id')

    # Merge values and names
    regions_gdf['value'] = regions_gdf.index.map(lambda rid: value_map.get(rid, 0))
    regions_gdf['NAME'] = regions_gdf.index.map(lambda rid: name_map.get(rid, "Unknown"))

    # Return GeoJSON with metadata
    geojson = json.loads(regions_gdf.to_json())
    return jsonify({
        "date": target_date.isoformat(),
        "type": geojson["type"],
        "features": geojson["features"]
    }), 200

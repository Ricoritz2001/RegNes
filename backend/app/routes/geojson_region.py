# app/routes/geojson_region.py

from flask import Blueprint, Response
from app.services.geojson import generate_regions_geojson
from app import db

bp = Blueprint("geojson_region", __name__, url_prefix="/api/geojson")

@bp.route("/regions-with-sentiment")
def regions_with_sentiment():
    # Always regenerate the GeoJSON on each request
    geojson_str = generate_regions_geojson()
    return Response(geojson_str, mimetype="application/json")

# app/routes/trends.py

from flask import Blueprint, jsonify, request
from datetime import datetime, date
from sqlalchemy import func
from app import db
from app.models.data_models import RegionalData, GlobalStats, Regions

bp = Blueprint('trends', __name__, url_prefix='/api/trends')


def _parse_dates():
    """
    Parse optional query params ?from & ?to in YYYY-MM-DD.
    Defaults: from 2019-01-01, to today.
    Returns (start_dt, end_dt, error_response, status_code).
    """
    try:
        start = datetime.fromisoformat(request.args.get('from', '2019-01-01'))
        end = datetime.fromisoformat(request.args.get('to',   date.today().isoformat()))
    except ValueError:
        return None, None, jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
    return start, end, None, None


@bp.route('/regional', methods=['GET'])
def regional_trends():
    """
    GET /trends/regional
      - regions (required): comma-separated region IDs, e.g. regions=101,102
      - from, to  (optional, YYYY-MM-DD)
    Returns a list of daily values for each region:
      [
        {
          "date": "2025-04-01",
          "region_id": 101,
          "region_name": "Schleswig-Holstein Mitte",
          "rauh": 0.12,
          "happiness": 0.20,
          "valenz": 0.05
        },
        ...
      ]
    """
    start, end, err, code = _parse_dates()
    if err:
        return err, code

    raw = request.args.get('regions')
    if not raw:
        return jsonify({"error": "No regions specified."}), 400
    try:
        region_ids = [int(r) for r in raw.split(',')]
    except ValueError:
        return jsonify({"error": "Invalid region IDs. Must be integers."}), 400

    rows = (
        db.session.query(
            func.date(RegionalData.item_date_published).label('date'),
            RegionalData.region_id,
            Regions.region_name.label('region_name'),
            RegionalData.rauh_sents_av.label('rauh'),
            RegionalData.happiness_av.label('happiness'),
            RegionalData.val_av.label('valenz')
        )
        .join(Regions, RegionalData.region_id == Regions.region_id)
        .filter(
            RegionalData.item_date_published.between(start, end),
            RegionalData.region_id.in_(region_ids)
        )
        .order_by(RegionalData.item_date_published)
        .all()
    )

    result = []
    for r in rows:
        date_str = r.date if isinstance(r.date, str) else r.date.isoformat()
        result.append({
            "date":        date_str,
            "region_id":   r.region_id,
            "region_name": r.region_name,
            "rauh":        float(r.rauh),
            "happiness":   float(r.happiness),
            "valenz":      float(r.valenz),
        })

    return jsonify(result), 200


@bp.route('/global', methods=['GET'])
def global_trends():
    """
    GET /trends/global
      • countries (required): comma-separated country names, e.g. countries=Schweiz,Österreich
      • metric       (optional): one of sentiment, happiness, valenz (defaults to sentiment)
      • from, to     (optional, YYYY-MM-DD)
    Returns a list of daily values for each country:
      [
        {
          "date": "2025-04-01",
          "country": "Schweiz",
          "<metric>": 0.07
        },
      ]
    """
    start, end, err, code = _parse_dates()
    if err:
        return err, code

    raw = request.args.get('countries')
    if not raw:
        return jsonify({"error": "No countries specified."}), 400
    countries = [c.strip() for c in raw.split(',')]

    metric = request.args.get('metric', 'sentiment')
    col_map = {
        'sentiment': GlobalStats.av_sents.label('value'),
    }
    if metric not in col_map:
        return jsonify({"error": f"Invalid metric '{metric}'. Must be one of: {', '.join(col_map.keys())}."}), 400
    value_col = col_map[metric]

    rows = (
        db.session.query(
            func.date(GlobalStats.item_date_published).label('date'),
            GlobalStats.country,
            value_col
        )
        .filter(
            GlobalStats.item_date_published.between(start, end),
            GlobalStats.country.in_(countries)
        )
        .order_by(GlobalStats.item_date_published, GlobalStats.country)
        .all()
    )

    result = []
    for r in rows:
        date_str = r.date if isinstance(r.date, str) else r.date.isoformat()
        result.append({
            "date":    date_str,
            "country": r.country,
            metric:    float(r.value)
        })

    return jsonify(result), 200


@bp.route('/regions', methods=['GET'])
def list_regions():
    """
    GET /trends/regions
    Returns:
      [
        { "region_id": 101, "region_name": "Schleswig-Holstein Mitte" },
        ...
      ]
    """
    rows = (
        db.session.query(
            Regions.region_id,
            Regions.region_name
        )
        .order_by(Regions.region_name)
        .all()
    )
    result = [
        {"region_id": rid, "region_name": name}
        for rid, name in rows
    ]
    return jsonify(result), 200

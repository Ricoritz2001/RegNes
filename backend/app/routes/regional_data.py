from flask import Blueprint, jsonify, request
from datetime import datetime, date
from app import db
from app.models.data_models import RegionalData, Regions

bp = Blueprint('regions', __name__, url_prefix='/api/regions')

METRIC_MAP = {
    'sentiment_readership': RegionalData.rauh_sents_share,
    'sentiment_mean': RegionalData.rauh_sents_av,
    'valenz_readership': RegionalData.val_share,
    'valenz_mean': RegionalData.val_av,
    'happiness readership': RegionalData.happiness_share,
    'happiness_mean': RegionalData.happiness_av
}

@bp.route('/region/<int:region_id>', methods=['GET'])
def region_details(region_id):
    """
    Retrieve time-series metrics for a specific region.

    Path paramter:
       region_id (int): Identifier of the region.

    Query paramters:
        metrics(str):
            comma-separated list of metrics to retrieve.
             'sentiment_readership', 'sentiment_mean',
             'valenz_readership', 'valenz_mean',
             'happiness readership', 'happiness_mean'
            Defaults to all metrics
        from (str):
            start date in YYYY-MM-DD format.
            Defaults to '2019-01-01'.
        to (str):
            End date in YYYY-MM-DD format.
            Defaults to today.

    Returns:
        JSON response containing the region's metrics data.
        The response includes:
            - region_id: ID of the region
            - region_name: Name of the region
            - data: List of dictionaries with date and metric values

     Response codes:
        200 OK: Successful retrieval of data.
        400 Bad Request: Invalid query paramters.
        404 Not Found: Region not found.

    """

    region = db.session.get(Regions, region_id)
    if not region:
        return jsonify({"error": "Region not found"}), 404

    metrics_param = request.args.get('metrics')
    if metrics_param:
        requested = [m.strip() for m in metrics_param.split(',')]
        invalid = [m for m in requested if m not in METRIC_MAP]
        if invalid:
            return jsonify({"error": f"Invalid metric names: {invalid}"}), 400
        metrics = requested
    else:
        metrics = list(METRIC_MAP.keys())
  
    try:
        start_date = datetime.fromisoformat(request.args.get('from', '2019-01-01'))
    except ValueError:
        return jsonify({"error": "Invalid date format for 'from'"}), 400

    to_param = request.args.get('to')
    if to_param:
        try:
            end_date = datetime.fromisoformat(to_param)
        except ValueError:
            return jsonify({"error": "Invalid date format for 'to'"}), 400
    else:
        end_date = datetime.combine(date.today(), datetime.min.time())

    cols = [RegionalData.item_date_published]
    cols += [METRIC_MAP[m] for m in metrics]

    rows = (
        db.session.query(*cols)
        .filter(
            RegionalData.region_id == region_id,
            RegionalData.item_date_published >= start_date,
            RegionalData.item_date_published <= end_date
        )
        .order_by(RegionalData.item_date_published)
        .all()
    )

    data = []
    for row in rows:
        entry = {'date': row[0].date().isoformat()}
        for idx, key in enumerate(metrics, start=1):
            entry[key] = row[idx]
        data.append(entry)
    
    return jsonify({
        "region_id": region.region_id,
        "region_name": region.region_name,
        "data": data
    })

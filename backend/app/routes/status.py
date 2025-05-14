from flask import Blueprint, jsonify, current_app
from datetime import date
from app import db
from app.models.data_models import GlobalStats
from sqlalchemy import func

bp = Blueprint('status', __name__, url_prefix="/api/status")

@bp.route("", methods=["GET"])
def get_status():
    """
    Retrieves all dashboard metrics

    Returns a JSON object that contains:
    - last_update (str | null): ISO format date of the last update or null
    if no updates
    - total_news (int): cumulative number of news articles
    - channels_count (int): number of feeds(channels) tracked in the latest
    record
    - sources_count (int): number of newspaper sources tracked in latest record
    - news_today (int): Count of news articles published today
    - sentiment_today (float | null): Average sentiment for news articles
    published today or null if no articles were published

    Filtering: 
    - Considers records from 2019 and onwars, reads latest row explicitly,
    no query parameter is needed.


    Resposnse code:
    - 200 OK on success
    """
    current_app.logger.info(" get_status() called")
    try:
        # Cumulative total_news
        total_news = db.session \
            .query(func.coalesce(func.sum(GlobalStats.num_news), 0)) \
            .scalar()

        # Latest snapshot
        latest = (
            db.session
            .query(GlobalStats)
            .order_by(GlobalStats.item_date_published.desc())
            .first()
        )

        if latest:
            last_update = latest.item_date_published.date().isoformat()
            channels_count = latest.num_feeds
            sources_count = latest.num_newspaper
        else:
            last_update = None
            channels_count = sources_count = 0

        # Today numbers there is no data for current date.
        today = date.today()
        today_rec = (
            db.session
            .query(GlobalStats)
            .filter(GlobalStats.item_date_published == today)
            .first()
        )

        if today_rec:
            news_today = today_rec.num_news
            sentiment_today = today_rec.av_sents
        else:
            news_today = 0
            sentiment_today = None

        return jsonify({
            "last_update":    last_update,
            "total_news":     int(total_news),
            "channels_count": channels_count,
            "sources_count":  sources_count,
            "news_today":     news_today,
            "sentiment_today": sentiment_today
        }), 200

    except Exception as e:
        # Log full traceback to the console
        current_app.logger.exception("Exception in GET /api/status")
        # Also return it in the JSON so you can see it in the browser
        return jsonify({
            "error": str(e),
            "type": type(e).__name__
        }), 500

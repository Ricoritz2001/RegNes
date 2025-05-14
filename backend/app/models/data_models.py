from app import db
from datetime import datetime, timezone
from sqlalchemy import func


class GlobalStats(db.Model):
    __tablename__ = "global_stats"

    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String, default="Germany", index=True)
    item_date_published = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
        index=True
    )
    num_newspaper = db.Column(db.Integer, default=0)
    num_feeds = db.Column(db.Integer, default=0)
    av_sents = db.Column(db.Float, default=0.0)
    num_news = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<GlobalStats {self.id}, {self.country}, {self.item_date_published}>"


class RegionalData(db.Model):
    __tablename__ = "regional_data"

    id = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer, db.ForeignKey("regions.region_id"),
                          index=True)
    item_date_published = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
        index=True
    )
    num_words = db.Column(db.Float, default=0.0)
    rauh_sents_share = db.Column(db.Float, default=0.0)
    rauh_sents_av = db.Column(db.Float, default=0.0)
    happiness_share = db.Column(db.Float, default=0.0)
    happiness_av = db.Column(db.Float, default=0.0)
    val_share = db.Column(db.Float, default=0.0)
    val_av = db.Column(db.Float, default=0.0)
    num_papers = db.Column(db.Integer, default=0)
    num_news = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<RegionalData {self.id}, Region {self.region_id}>"


class Regions(db.Model):
    __tablename__ = "regions"

    region_id = db.Column(db.Integer, primary_key=True)
    region_name = db.Column(db.String, default="None")
    country = db.Column(db.String, default="None")

    def __repr__(self):
        return f"<Regions {self.region_id}, {self.region_name}, {self.country}>"

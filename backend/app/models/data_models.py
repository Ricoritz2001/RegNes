from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

class Base(DeclarativeBase):
    pass

class GlobalStats(Base):
    __tablename__ = "global_stats"
    
    id: Mapped[int] =  mapped_column(primary_key=True)
    country: Mapped[str] = mapped_column(default = "Germany")
    item_date_published: Mapped[str] = mapped_column(default = "0")
    num_newspaper: Mapped[int] = mapped_column(int ,default = 0)
    num_feeds: Mapped[int] = mapped_column(default = 0)
    av_sents: Mapped[float] = mapped_column(default = 0.0)
    num_news: Mapped[int] = mapped_column(default = 0)
    
    def __repr__(self):
        return f"GlobalStats(id={self.id!r}, country={self.country!r}, item_date_published{self.item_date_published!r}, num_newspaper={self.num_newspaper!r}, num_feeds={self.num_feeds!r}, av_sents={self.av_sents!r}, num_news={self.num_news!r})"
    
class RegionalData(Base):
    __tablename__ = "regional_data"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    region_id: Mapped[int] = mapped_column(ForeignKey("region.id"))
    item_date_published: Mapped[str] = mapped_column(default = "0")
    num_words: Mapped[float] = mapped_column(default = 0.0)
    rauh_sents_share: Mapped[float] = mapped_column(default = 0.0)
    rauh_sents_av: Mapped[float] = mapped_column(default = 0.0)
    happiness_share

    
    
    
    
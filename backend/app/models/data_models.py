from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, DateTime


class Base(DeclarativeBase):
    pass


class GlobalStats(Base):
    __tablename__ = "global_stats"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    country: Mapped[str] = mapped_column(default="Germany", index=True)
    item_date_published: Mapped[DateTime] = mapped_column(default="0", index=True)
    num_newspaper: Mapped[int] = mapped_column(default=0)
    num_feeds: Mapped[int] = mapped_column(default=0)
    av_sents: Mapped[float] = mapped_column(default=0.0)
    num_news: Mapped[int] = mapped_column(default=0)
    
    def __repr__(self) -> str:
        return f"GlobalStats(id={self.id!r}, country={self.country!r}, item_date_published{self.item_date_published!r}, num_newspaper={self.num_newspaper!r}, num_feeds={self.num_feeds!r}, av_sents={self.av_sents!r}, num_news={self.num_news!r})"
  
  
class RegionalData(Base):
    __tablename__ = "regional_data"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.region_id"), index=True)
    item_date_published: Mapped[DateTime] = mapped_column(default="0",)
    num_words: Mapped[float] = mapped_column(default=0.0)
    rauh_sents_share: Mapped[float] = mapped_column(default=0.0)
    rauh_sents_av: Mapped[float] = mapped_column(default=0.0)
    happiness_share: Mapped[float] = mapped_column(default=0.0)
    happiness_av: Mapped[float] = mapped_column(default=0.0)
    val_share: Mapped[float] = mapped_column(default=0.0)
    val_av: Mapped[float] = mapped_column(default=0.0)
    num_papers: Mapped[int] = mapped_column(default=0)
    
    def __repr__(self) -> str:
        return f"RegionalData(id={self.id!r}, region_id={self.region_id!r}, item_date_published={self.item_date_published!r}, num_words={self.num_words!r}, rauh_sents_share={self.rauh_sents_share!r}, rauh_sents_av={self.rauh_sents_av!r}, happiness_share={self.happiness_share!r}, happiness_av={self.happiness_av!r}, val_share={self.val_share!r}, val_av={self.val_av!r}, num_papers={self.num_papers!r})"


class Regions(Base):
    __tablename__ = "regions"
   
    region_id: Mapped[int] = mapped_column(primary_key=True)
    region_name: Mapped[str] = mapped_column(default="None")
    country: Mapped[str] = mapped_column(default="None")
    
    def __repr__(self) -> str:
        return f"Regions(region_id={self.region_id!r}, region_name={self.region_name!r}, country={self.country!r})"
    

    

    
    
    
    
import json
from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Index

from app.database import Base


class CompanyScore(Base):
    __tablename__ = "company_scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), nullable=False, index=True, unique=True)
    company_name = Column(String(200), nullable=False)
    sector = Column(String(100), nullable=False, index=True)
    market_cap = Column(Float)
    current_price = Column(Float)
    daily_change_pct = Column(Float)

    # 6 ability scores (0-100)
    growth_score = Column(Float, default=50.0)
    stability_score = Column(Float, default=50.0)
    cashflow_score = Column(Float, default=50.0)
    efficiency_score = Column(Float, default=50.0)
    momentum_score = Column(Float, default=50.0)
    earnings_score = Column(Float, default=50.0)

    total_score = Column(Float, default=50.0)
    grade = Column(String(1), default="C")
    emotional_tag = Column(String(100), default="")

    # Raw financials stored as JSON string
    raw_metrics = Column(Text, default="{}")

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_sector_total", "sector", "total_score"),
    )

    @property
    def raw_metrics_dict(self) -> dict:
        return json.loads(self.raw_metrics) if self.raw_metrics else {}

    @raw_metrics_dict.setter
    def raw_metrics_dict(self, value: dict):
        self.raw_metrics = json.dumps(value)

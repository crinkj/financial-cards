from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CardSummary(BaseModel):
    ticker: str
    company_name: str
    sector: str
    grade: str
    total_score: float
    current_price: Optional[float] = None
    daily_change_pct: Optional[float] = None

    model_config = {"from_attributes": True}


class AbilityScores(BaseModel):
    growth: float
    stability: float
    cashflow: float
    efficiency: float
    momentum: float
    earnings: float


class CardDetail(BaseModel):
    ticker: str
    company_name: str
    sector: str
    market_cap: Optional[float] = None
    current_price: Optional[float] = None
    daily_change_pct: Optional[float] = None
    scores: AbilityScores
    total_score: float
    grade: str
    emotional_tag: str
    raw_metrics: dict
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class RankingEntry(BaseModel):
    rank: int
    ticker: str
    company_name: str
    sector: str
    total_score: float
    grade: str

    model_config = {"from_attributes": True}


class SectorChampion(BaseModel):
    sector: str
    ticker: str
    company_name: str
    total_score: float
    grade: str

    model_config = {"from_attributes": True}

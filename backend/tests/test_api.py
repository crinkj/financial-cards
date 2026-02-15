"""Integration tests for API endpoints."""
import json
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models.score import CompanyScore

# Use in-memory SQLite with shared cache so all connections see the same DB
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    # Seed test data
    companies = [
        CompanyScore(
            ticker="AAPL", company_name="Apple Inc.", sector="Technology",
            market_cap=2_800_000_000_000, current_price=195.0, daily_change_pct=1.2,
            growth_score=72, stability_score=68, cashflow_score=85,
            efficiency_score=78, momentum_score=70, earnings_score=65,
            total_score=74.5, grade="A", emotional_tag="현금 부자",
            raw_metrics=json.dumps({"return_on_equity": 0.30, "debt_to_equity": 150}),
            updated_at=datetime.utcnow(),
        ),
        CompanyScore(
            ticker="MSFT", company_name="Microsoft Corp", sector="Technology",
            market_cap=2_900_000_000_000, current_price=410.0, daily_change_pct=0.8,
            growth_score=68, stability_score=75, cashflow_score=80,
            efficiency_score=82, momentum_score=72, earnings_score=70,
            total_score=75.2, grade="A", emotional_tag="효율의 달인",
            raw_metrics=json.dumps({"return_on_equity": 0.35, "debt_to_equity": 40}),
            updated_at=datetime.utcnow(),
        ),
        CompanyScore(
            ticker="JPM", company_name="JPMorgan Chase", sector="Financials",
            market_cap=500_000_000_000, current_price=190.0, daily_change_pct=-0.3,
            growth_score=55, stability_score=60, cashflow_score=58,
            efficiency_score=62, momentum_score=50, earnings_score=68,
            total_score=58.0, grade="B", emotional_tag="수익 머신",
            raw_metrics=json.dumps({"return_on_equity": 0.15}),
            updated_at=datetime.utcnow(),
        ),
    ]
    db.add_all(companies)
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


def test_health():
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_list_cards():
    resp = client.get("/api/cards")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 3
    # Should be ordered by total_score desc
    assert data[0]["ticker"] == "MSFT"


def test_list_cards_filter_sector():
    resp = client.get("/api/cards?sector=Financials")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["ticker"] == "JPM"


def test_list_cards_search():
    resp = client.get("/api/cards?search=apple")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["ticker"] == "AAPL"


def test_get_card():
    resp = client.get("/api/cards/AAPL")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "AAPL"
    assert data["scores"]["growth"] == 72
    assert data["scores"]["cashflow"] == 85
    assert data["grade"] == "A"
    assert "return_on_equity" in data["raw_metrics"]


def test_get_card_not_found():
    resp = client.get("/api/cards/ZZZZ")
    assert resp.status_code == 404


def test_top10():
    resp = client.get("/api/rankings/top10")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 3
    assert data[0]["rank"] == 1
    assert data[0]["ticker"] == "MSFT"
    assert data[2]["rank"] == 3


def test_sector_champions():
    resp = client.get("/api/rankings/sectors")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2  # Technology + Financials
    sectors = {d["sector"] for d in data}
    assert "Technology" in sectors
    assert "Financials" in sectors


def test_list_sectors():
    resp = client.get("/api/rankings/sectors/list")
    assert resp.status_code == 200
    data = resp.json()
    assert "Technology" in data
    assert "Financials" in data

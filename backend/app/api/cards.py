import json
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.score import CompanyScore
from app.schemas.card import CardSummary, CardDetail, AbilityScores

router = APIRouter(prefix="/api/cards", tags=["cards"])


@router.post("/batch-update")
def trigger_batch_update(background_tasks: BackgroundTasks):
    from app.scripts.batch_update import run_batch_update
    background_tasks.add_task(run_batch_update)
    return {"status": "Batch update started in background"}


@router.get("", response_model=list[CardSummary])
def list_cards(
    sector: Optional[str] = Query(None, description="Filter by sector"),
    search: Optional[str] = Query(None, description="Search by ticker or company name"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    query = db.query(CompanyScore)
    if sector:
        query = query.filter(CompanyScore.sector == sector)
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            (CompanyScore.ticker.ilike(pattern)) | (CompanyScore.company_name.ilike(pattern))
        )
    query = query.order_by(CompanyScore.total_score.desc())
    results = query.offset(skip).limit(limit).all()
    return results


@router.get("/{ticker}", response_model=CardDetail)
def get_card(ticker: str, db: Session = Depends(get_db)):
    company = db.query(CompanyScore).filter(CompanyScore.ticker == ticker.upper()).first()
    if not company:
        raise HTTPException(status_code=404, detail=f"Card not found for ticker: {ticker}")

    raw = json.loads(company.raw_metrics) if company.raw_metrics else {}

    return CardDetail(
        ticker=company.ticker,
        company_name=company.company_name,
        sector=company.sector,
        market_cap=company.market_cap,
        current_price=company.current_price,
        daily_change_pct=company.daily_change_pct,
        scores=AbilityScores(
            growth=company.growth_score,
            stability=company.stability_score,
            cashflow=company.cashflow_score,
            efficiency=company.efficiency_score,
            momentum=company.momentum_score,
            earnings=company.earnings_score,
        ),
        total_score=company.total_score,
        grade=company.grade,
        emotional_tag=company.emotional_tag,
        raw_metrics=raw,
        updated_at=company.updated_at,
    )

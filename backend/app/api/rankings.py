from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.score import CompanyScore
from app.schemas.card import RankingEntry, SectorChampion

router = APIRouter(prefix="/api/rankings", tags=["rankings"])


@router.get("/top10", response_model=list[RankingEntry])
def get_top10(db: Session = Depends(get_db)):
    results = (
        db.query(CompanyScore)
        .order_by(CompanyScore.total_score.desc())
        .limit(10)
        .all()
    )
    return [
        RankingEntry(
            rank=i + 1,
            ticker=r.ticker,
            company_name=r.company_name,
            sector=r.sector,
            total_score=r.total_score,
            grade=r.grade,
        )
        for i, r in enumerate(results)
    ]


@router.get("/sectors", response_model=list[SectorChampion])
def get_sector_champions(db: Session = Depends(get_db)):
    # Subquery: max total_score per sector
    subq = (
        db.query(
            CompanyScore.sector,
            func.max(CompanyScore.total_score).label("max_score"),
        )
        .group_by(CompanyScore.sector)
        .subquery()
    )

    results = (
        db.query(CompanyScore)
        .join(
            subq,
            (CompanyScore.sector == subq.c.sector)
            & (CompanyScore.total_score == subq.c.max_score),
        )
        .order_by(CompanyScore.total_score.desc())
        .all()
    )

    return [
        SectorChampion(
            sector=r.sector,
            ticker=r.ticker,
            company_name=r.company_name,
            total_score=r.total_score,
            grade=r.grade,
        )
        for r in results
    ]


@router.get("/sectors/list", response_model=list[str])
def list_sectors(db: Session = Depends(get_db)):
    results = db.query(CompanyScore.sector).distinct().order_by(CompanyScore.sector).all()
    return [r[0] for r in results]

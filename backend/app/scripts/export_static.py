"""
Export DB data to static JSON files for GitHub Pages deployment.

Usage:
    cd backend
    python -m app.scripts.export_static
"""
import json
import sys
import os

from sqlalchemy import func

from app.database import SessionLocal, init_db
from app.models.score import CompanyScore


def run_export():
    init_db()
    db = SessionLocal()

    out_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "frontend", "public", "data")
    os.makedirs(out_dir, exist_ok=True)

    # 1. All cards
    all_cards = db.query(CompanyScore).order_by(CompanyScore.total_score.desc()).all()
    cards_list = []
    cards_detail = {}

    for c in all_cards:
        summary = {
            "ticker": c.ticker,
            "company_name": c.company_name,
            "sector": c.sector,
            "grade": c.grade,
            "total_score": c.total_score,
            "current_price": c.current_price,
            "daily_change_pct": c.daily_change_pct,
        }
        cards_list.append(summary)

        raw = json.loads(c.raw_metrics) if c.raw_metrics else {}
        detail = {
            "ticker": c.ticker,
            "company_name": c.company_name,
            "sector": c.sector,
            "market_cap": c.market_cap,
            "current_price": c.current_price,
            "daily_change_pct": c.daily_change_pct,
            "scores": {
                "growth": c.growth_score,
                "stability": c.stability_score,
                "cashflow": c.cashflow_score,
                "efficiency": c.efficiency_score,
                "momentum": c.momentum_score,
                "earnings": c.earnings_score,
            },
            "total_score": c.total_score,
            "grade": c.grade,
            "emotional_tag": c.emotional_tag,
            "raw_metrics": raw,
            "updated_at": c.updated_at.isoformat() if c.updated_at else None,
        }
        cards_detail[c.ticker] = detail

    with open(os.path.join(out_dir, "cards.json"), "w") as f:
        json.dump(cards_list, f)
    print(f"Exported {len(cards_list)} card summaries")

    with open(os.path.join(out_dir, "cards_detail.json"), "w") as f:
        json.dump(cards_detail, f)
    print(f"Exported {len(cards_detail)} card details")

    # 2. Top 10
    top10 = db.query(CompanyScore).order_by(CompanyScore.total_score.desc()).limit(10).all()
    top10_list = [
        {
            "rank": i + 1,
            "ticker": c.ticker,
            "company_name": c.company_name,
            "sector": c.sector,
            "total_score": c.total_score,
            "grade": c.grade,
        }
        for i, c in enumerate(top10)
    ]
    with open(os.path.join(out_dir, "top10.json"), "w") as f:
        json.dump(top10_list, f)
    print("Exported top 10")

    # 3. Sector champions
    subq = (
        db.query(
            CompanyScore.sector,
            func.max(CompanyScore.total_score).label("max_score"),
        )
        .group_by(CompanyScore.sector)
        .subquery()
    )
    champs = (
        db.query(CompanyScore)
        .join(subq, (CompanyScore.sector == subq.c.sector) & (CompanyScore.total_score == subq.c.max_score))
        .order_by(CompanyScore.total_score.desc())
        .all()
    )
    champs_list = [
        {
            "sector": c.sector,
            "ticker": c.ticker,
            "company_name": c.company_name,
            "total_score": c.total_score,
            "grade": c.grade,
        }
        for c in champs
    ]
    with open(os.path.join(out_dir, "sectors.json"), "w") as f:
        json.dump(champs_list, f)
    print(f"Exported {len(champs_list)} sector champions")

    # 4. Sector list
    sectors = [r[0] for r in db.query(CompanyScore.sector).distinct().order_by(CompanyScore.sector).all()]
    with open(os.path.join(out_dir, "sectors_list.json"), "w") as f:
        json.dump(sectors, f)
    print(f"Exported {len(sectors)} sectors")

    db.close()
    print(f"\nAll files written to {os.path.abspath(out_dir)}")


if __name__ == "__main__":
    run_export()

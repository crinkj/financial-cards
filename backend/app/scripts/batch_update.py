"""
Batch update script: fetches financial data, computes scores, and writes to DB.
Run manually or via cron for daily updates.

Usage:
    cd backend
    python -m app.scripts.batch_update
"""
import json
import logging
import sys
from datetime import datetime

from app.database import SessionLocal, init_db
from app.models.score import CompanyScore
from app.services.data_ingestion import fetch_all_companies
from app.services.scoring_engine import score_companies

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def run_batch_update():
    logger.info("Starting batch update...")
    init_db()

    # Step 1: Fetch data
    logger.info("Fetching company data from yfinance...")
    raw_data = fetch_all_companies()
    if not raw_data:
        logger.error("No data fetched. Aborting.")
        return

    logger.info(f"Fetched {len(raw_data)} companies. Computing scores...")

    # Step 2: Score
    scored_data = score_companies(raw_data)

    # Step 3: Write to DB
    db = SessionLocal()
    try:
        updated = 0
        created = 0
        for item in scored_data:
            existing = db.query(CompanyScore).filter(CompanyScore.ticker == item["ticker"]).first()
            if existing:
                existing.company_name = item["company_name"]
                existing.sector = item["sector"]
                existing.market_cap = item.get("market_cap")
                existing.current_price = item.get("current_price")
                existing.daily_change_pct = item.get("daily_change_pct")
                existing.growth_score = item["growth_score"]
                existing.stability_score = item["stability_score"]
                existing.cashflow_score = item["cashflow_score"]
                existing.efficiency_score = item["efficiency_score"]
                existing.momentum_score = item["momentum_score"]
                existing.earnings_score = item["earnings_score"]
                existing.total_score = item["total_score"]
                existing.grade = item["grade"]
                existing.emotional_tag = item["emotional_tag"]
                existing.raw_metrics = json.dumps(item.get("raw_metrics", {}))
                existing.updated_at = datetime.utcnow()
                updated += 1
            else:
                record = CompanyScore(
                    ticker=item["ticker"],
                    company_name=item["company_name"],
                    sector=item["sector"],
                    market_cap=item.get("market_cap"),
                    current_price=item.get("current_price"),
                    daily_change_pct=item.get("daily_change_pct"),
                    growth_score=item["growth_score"],
                    stability_score=item["stability_score"],
                    cashflow_score=item["cashflow_score"],
                    efficiency_score=item["efficiency_score"],
                    momentum_score=item["momentum_score"],
                    earnings_score=item["earnings_score"],
                    total_score=item["total_score"],
                    grade=item["grade"],
                    emotional_tag=item["emotional_tag"],
                    raw_metrics=json.dumps(item.get("raw_metrics", {})),
                    updated_at=datetime.utcnow(),
                )
                db.add(record)
                created += 1

        db.commit()
        logger.info(f"Batch update complete: {created} created, {updated} updated")
    except Exception as e:
        db.rollback()
        logger.error(f"Error during batch update: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_batch_update()

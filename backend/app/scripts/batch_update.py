"""
Batch update script: fetches financial data, computes scores, and writes to DB.

Three-phase approach to avoid Yahoo Finance rate limits:
  Phase 1: Batch price download (1-2 HTTP requests for all tickers)
  Phase 2: Check fundamentals cache, only fetch stale tickers
  Phase 3: Merge, score, and write to DB

Usage:
    cd backend
    python -m app.scripts.batch_update                # full update
    python -m app.scripts.batch_update --price-only   # daily price-only update
"""
import argparse
import json
import logging
import sys
from datetime import datetime

from app.config import COMPANY_TICKERS
from app.database import SessionLocal, init_db
from app.models.score import CompanyScore, FundamentalsCache
from app.services.data_ingestion import fetch_batch_price_data, fetch_fundamentals_batch
from app.services.scoring_engine import score_companies

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def get_stale_tickers(db, all_tickers: list[str], max_age_hours: int = 168) -> list[str]:
    """Return tickers whose fundamentals cache is older than max_age_hours (default 7 days)."""
    stale = []
    for ticker in all_tickers:
        cached = db.query(FundamentalsCache).filter(FundamentalsCache.ticker == ticker).first()
        if not cached or not cached.fetched_at:
            stale.append(ticker)
            continue
        age_hours = (datetime.utcnow() - cached.fetched_at).total_seconds() / 3600
        if age_hours > max_age_hours:
            stale.append(ticker)
    return stale


def update_fundamentals_cache(db, ticker: str, data: dict):
    """Upsert fundamentals into cache table."""
    existing = db.query(FundamentalsCache).filter(FundamentalsCache.ticker == ticker).first()
    if existing:
        existing.data_json = json.dumps(data)
        existing.fetched_at = datetime.utcnow()
    else:
        db.add(FundamentalsCache(
            ticker=ticker,
            data_json=json.dumps(data),
            fetched_at=datetime.utcnow(),
        ))


def load_all_fundamentals_from_cache(db, all_tickers: list[str]) -> dict[str, dict]:
    """Load all cached fundamentals as a dict keyed by ticker."""
    result = {}
    for ticker in all_tickers:
        cached = db.query(FundamentalsCache).filter(FundamentalsCache.ticker == ticker).first()
        if cached:
            result[ticker] = json.loads(cached.data_json)
    return result


def write_scores_to_db(db, scored_data: list[dict]):
    """Upsert scored company data into the CompanyScore table."""
    created = 0
    updated = 0
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
    logger.info(f"DB write complete: {created} created, {updated} updated")


def run_batch_update(price_only: bool = False, max_age_hours: int = 168):
    """
    Three-phase batch update:
      Phase 1: Batch price download (1-2 HTTP requests)
      Phase 2: Check cache, fetch stale fundamentals (only if not price_only)
      Phase 3: Merge + score + write to DB
    """
    logger.info(f"Starting batch update (price_only={price_only})...")
    init_db()
    db = SessionLocal()

    try:
        # Flatten all tickers
        all_tickers = []
        ticker_to_sector = {}
        for sector, tickers in COMPANY_TICKERS.items():
            for t in tickers:
                all_tickers.append(t)
                ticker_to_sector[t] = sector

        # Phase 1: Batch price data (1-2 HTTP requests)
        logger.info(f"Phase 1: Batch price download for {len(all_tickers)} tickers...")
        price_data = fetch_batch_price_data(all_tickers)
        logger.info(f"Got price data for {len(price_data)} tickers")

        # Phase 2: Fundamentals
        if not price_only:
            stale = get_stale_tickers(db, all_tickers, max_age_hours)
            logger.info(f"Phase 2: {len(stale)} tickers need fresh fundamentals")

            if stale:
                fresh = fetch_fundamentals_batch(stale)
                for ticker, data in fresh.items():
                    update_fundamentals_cache(db, ticker, data)
                db.commit()
                logger.info(f"Cached fundamentals for {len(fresh)} tickers")

        # Load all fundamentals from cache
        fundamentals = load_all_fundamentals_from_cache(db, all_tickers)
        logger.info(f"Loaded cached fundamentals for {len(fundamentals)} tickers")

        # Phase 3: Merge, score, write
        merged = []
        for ticker in all_tickers:
            fund = fundamentals.get(ticker, {})
            price = price_data.get(ticker, {})
            if not fund and not price:
                continue

            company = {
                "ticker": ticker,
                "sector": ticker_to_sector[ticker],
                **fund,
                **price,  # price overwrites any overlapping keys (current_price, etc.)
            }
            company["sector"] = ticker_to_sector[ticker]
            merged.append(company)

        if not merged:
            logger.error("No data to score. Aborting.")
            return

        logger.info(f"Phase 3: Scoring {len(merged)} companies...")
        scored = score_companies(merged)
        write_scores_to_db(db, scored)
        logger.info("Batch update complete!")

    except Exception as e:
        db.rollback()
        logger.error(f"Batch update failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Financial Cards batch update")
    parser.add_argument("--price-only", action="store_true",
                        help="Only update price data (skip fundamentals fetch)")
    parser.add_argument("--max-age", type=int, default=168,
                        help="Max age in hours for fundamentals cache (default: 168 = 7 days)")
    args = parser.parse_args()
    run_batch_update(price_only=args.price_only, max_age_hours=args.max_age)

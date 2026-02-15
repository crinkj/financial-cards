"""
Local data collection + remote upload script.

Run this from your local machine (residential IP) to fetch Yahoo Finance data
without getting rate-limited, then upload scored results to the Render backend.

Usage:
    cd backend
    source venv/bin/activate
    python -m app.scripts.local_fetch_and_upload \
        --api-url https://financial-cards-api.onrender.com \
        --api-key YOUR_ADMIN_KEY
"""
import argparse
import json
import logging
import sys

import requests

from app.config import COMPANY_TICKERS
from app.services.data_ingestion import fetch_batch_price_data, fetch_fundamentals_batch
from app.services.scoring_engine import score_companies

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Fetch data locally and upload to remote backend")
    parser.add_argument("--api-url", required=True, help="Backend API URL (e.g. https://financial-cards-api.onrender.com)")
    parser.add_argument("--api-key", required=True, help="Admin API key for upload endpoint")
    parser.add_argument("--price-only", action="store_true", help="Only fetch price data (skip fundamentals)")
    args = parser.parse_args()

    # Flatten tickers
    all_tickers = []
    ticker_to_sector = {}
    for sector, tickers in COMPANY_TICKERS.items():
        for t in tickers:
            all_tickers.append(t)
            ticker_to_sector[t] = sector

    # Phase 1: Batch price download (1-2 requests)
    logger.info(f"Fetching batch price data for {len(all_tickers)} tickers...")
    price_data = fetch_batch_price_data(all_tickers)
    logger.info(f"Got price data for {len(price_data)} tickers")

    # Phase 2: Fundamentals (micro-batched, from local IP)
    fundamentals = {}
    if not args.price_only:
        logger.info("Fetching fundamentals (this may take 10-15 min)...")
        fundamentals = fetch_fundamentals_batch(all_tickers, batch_size=5, base_delay=3.0)
        logger.info(f"Got fundamentals for {len(fundamentals)} tickers")

    # Phase 3: Merge
    merged = []
    for ticker in all_tickers:
        fund = fundamentals.get(ticker, {})
        price = price_data.get(ticker, {})
        if not fund and not price:
            continue
        company = {"ticker": ticker, "sector": ticker_to_sector[ticker], **fund, **price}
        merged.append(company)

    if not merged:
        logger.error("No data to score. Aborting.")
        sys.exit(1)

    # Phase 4: Score
    logger.info(f"Scoring {len(merged)} companies...")
    scored = score_companies(merged)

    # Phase 5: Prepare upload payload
    upload_records = []
    for item in scored:
        upload_records.append({
            "ticker": item["ticker"],
            "company_name": item["company_name"],
            "sector": item["sector"],
            "market_cap": item.get("market_cap"),
            "current_price": item.get("current_price"),
            "daily_change_pct": item.get("daily_change_pct"),
            "growth_score": item["growth_score"],
            "stability_score": item["stability_score"],
            "cashflow_score": item["cashflow_score"],
            "efficiency_score": item["efficiency_score"],
            "momentum_score": item["momentum_score"],
            "earnings_score": item["earnings_score"],
            "total_score": item["total_score"],
            "grade": item["grade"],
            "emotional_tag": item["emotional_tag"],
            "raw_metrics": json.dumps(item.get("raw_metrics", {})),
        })

    # Phase 6: Upload to remote backend
    logger.info(f"Uploading {len(upload_records)} records to {args.api_url}...")
    resp = requests.post(
        f"{args.api_url}/api/cards/upload-data",
        json=upload_records,
        headers={"X-Api-Key": args.api_key},
        timeout=30,
    )

    if resp.status_code == 200:
        result = resp.json()
        logger.info(f"Upload success: {result['created']} created, {result['updated']} updated")
    else:
        logger.error(f"Upload failed: {resp.status_code} - {resp.text}")
        sys.exit(1)


if __name__ == "__main__":
    main()

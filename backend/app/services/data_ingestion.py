import logging
import time
from typing import Optional

import numpy as np
import yfinance as yf

from app.config import COMPANY_TICKERS

logger = logging.getLogger(__name__)


def _safe_get(info: dict, key: str, default=None):
    val = info.get(key, default)
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return default
    return val


def fetch_company_data(ticker: str) -> Optional[dict]:
    """Fetch financial data for a single company via yfinance."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        if not info or "shortName" not in info:
            logger.warning(f"No data found for {ticker}")
            return None

        # Get historical data for momentum / volatility
        hist = stock.history(period="1y")
        if hist.empty:
            logger.warning(f"No price history for {ticker}")
            return None

        # Price and change
        current_price = _safe_get(info, "currentPrice") or _safe_get(info, "regularMarketPrice", 0)
        prev_close = _safe_get(info, "previousClose") or _safe_get(info, "regularMarketPreviousClose", 0)
        daily_change_pct = ((current_price - prev_close) / prev_close * 100) if prev_close else 0

        # Compute 90-day volatility (annualized)
        recent_90 = hist.tail(90)
        daily_returns = recent_90["Close"].pct_change().dropna()
        volatility_90d = float(daily_returns.std() * np.sqrt(252)) if len(daily_returns) > 10 else 0.3

        # Momentum: 6-month price return
        if len(hist) > 126:
            price_6m_ago = float(hist["Close"].iloc[-126])
            momentum_6m = (current_price - price_6m_ago) / price_6m_ago if price_6m_ago > 0 else 0
        else:
            momentum_6m = 0

        # 52-week high relative position
        high_52w = _safe_get(info, "fiftyTwoWeekHigh", current_price)
        pct_from_high = (current_price / high_52w) if high_52w > 0 else 0.5

        data = {
            "ticker": ticker,
            "company_name": info.get("shortName", ticker),
            "sector": info.get("sector", "Unknown"),
            "market_cap": _safe_get(info, "marketCap", 0),
            "current_price": current_price,
            "daily_change_pct": round(daily_change_pct, 2),
            # Growth metrics
            "revenue_growth": _safe_get(info, "revenueGrowth", 0),
            "earnings_growth": _safe_get(info, "earningsGrowth", 0),
            "revenue_per_share": _safe_get(info, "revenuePerShare", 0),
            "earnings_quarterly_growth": _safe_get(info, "earningsQuarterlyGrowth", 0),
            # Stability metrics
            "debt_to_equity": _safe_get(info, "debtToEquity", 0),
            "current_ratio": _safe_get(info, "currentRatio", 1),
            "quick_ratio": _safe_get(info, "quickRatio", 1),
            "interest_coverage": _safe_get(info, "interestCoverage", 0),  # may not always be available
            # Cash flow metrics
            "free_cashflow": _safe_get(info, "freeCashflow", 0),
            "operating_cashflow": _safe_get(info, "operatingCashflow", 0),
            "fcf_per_share": (
                _safe_get(info, "freeCashflow", 0) / _safe_get(info, "sharesOutstanding", 1)
                if _safe_get(info, "sharesOutstanding", 0) > 0
                else 0
            ),
            # Efficiency metrics
            "return_on_equity": _safe_get(info, "returnOnEquity", 0),
            "return_on_assets": _safe_get(info, "returnOnAssets", 0),
            "operating_margins": _safe_get(info, "operatingMargins", 0),
            "profit_margins": _safe_get(info, "profitMargins", 0),
            "gross_margins": _safe_get(info, "grossMargins", 0),
            # Momentum metrics
            "momentum_6m": momentum_6m,
            "pct_from_52w_high": pct_from_high,
            "beta": _safe_get(info, "beta", 1.0),
            "volatility_90d": volatility_90d,
            # Earnings metrics
            "trailing_pe": _safe_get(info, "trailingPE", 0),
            "forward_pe": _safe_get(info, "forwardPE", 0),
            "peg_ratio": _safe_get(info, "pegRatio", 0),
            "trailing_eps": _safe_get(info, "trailingEps", 0),
            "forward_eps": _safe_get(info, "forwardEps", 0),
            "dividend_yield": _safe_get(info, "dividendYield", 0),
        }
        return data

    except Exception as e:
        logger.error(f"Error fetching data for {ticker}: {e}")
        return None


def fetch_all_companies() -> list[dict]:
    """Fetch data for all curated companies, grouped by sector."""
    all_data = []
    for sector, tickers in COMPANY_TICKERS.items():
        for ticker in tickers:
            logger.info(f"Fetching {ticker} ({sector})...")
            data = fetch_company_data(ticker)
            if data:
                # Override sector with our curated mapping for consistency
                data["sector"] = sector
                all_data.append(data)
            time.sleep(2)  # Rate limit: avoid Yahoo Finance 429 errors
        time.sleep(5)  # Extra pause between sectors
    logger.info(f"Fetched data for {len(all_data)} companies")
    return all_data

import logging
import random
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


# ---------------------------------------------------------------------------
# Track 1: Batch price data (1-2 HTTP requests for ALL tickers)
# ---------------------------------------------------------------------------

def fetch_batch_price_data(tickers: list[str]) -> dict[str, dict]:
    """Fetch 1Y price history for all tickers via a single yf.download() call.

    Returns dict keyed by ticker with price-derived metrics.
    This makes only 1-2 HTTP requests regardless of ticker count.
    """
    logger.info(f"Batch downloading price data for {len(tickers)} tickers...")
    df = yf.download(tickers, period="1y", group_by="ticker", threads=True)

    results = {}
    for ticker in tickers:
        try:
            ticker_df = df[ticker] if len(tickers) > 1 else df
            close = ticker_df["Close"].dropna()
            if len(close) < 10:
                continue

            current_price = float(close.iloc[-1])
            prev_close = float(close.iloc[-2]) if len(close) > 1 else current_price
            daily_change_pct = ((current_price - prev_close) / prev_close * 100) if prev_close else 0

            recent_90 = close.tail(90)
            daily_returns = recent_90.pct_change().dropna()
            volatility_90d = float(daily_returns.std() * np.sqrt(252)) if len(daily_returns) > 10 else 0.3

            if len(close) > 126:
                price_6m_ago = float(close.iloc[-126])
                momentum_6m = (current_price - price_6m_ago) / price_6m_ago if price_6m_ago > 0 else 0
            else:
                momentum_6m = 0

            high_52w = float(close.max())
            pct_from_high = current_price / high_52w if high_52w > 0 else 0.5

            results[ticker] = {
                "current_price": round(current_price, 2),
                "daily_change_pct": round(daily_change_pct, 2),
                "volatility_90d": round(volatility_90d, 4),
                "momentum_6m": round(momentum_6m, 4),
                "pct_from_52w_high": round(pct_from_high, 4),
            }
        except Exception as e:
            logger.warning(f"Price extraction failed for {ticker}: {e}")

    logger.info(f"Got price data for {len(results)}/{len(tickers)} tickers")
    return results


# ---------------------------------------------------------------------------
# Track 2: Fundamentals with micro-batching + exponential backoff
# ---------------------------------------------------------------------------

def fetch_fundamentals_batch(
    tickers: list[str],
    batch_size: int = 5,
    base_delay: float = 3.0,
    max_retries: int = 3,
) -> dict[str, dict]:
    """Fetch fundamental data in small batches with exponential backoff on 429s.

    Returns dict keyed by ticker with fundamental metrics.
    """
    results = {}
    batches = [tickers[i:i + batch_size] for i in range(0, len(tickers), batch_size)]

    for batch_idx, batch in enumerate(batches):
        logger.info(f"Fundamentals batch {batch_idx + 1}/{len(batches)}: {batch}")

        for ticker in batch:
            retries = 0
            while retries <= max_retries:
                try:
                    stock = yf.Ticker(ticker)
                    info = stock.info

                    if not info or "shortName" not in info:
                        logger.warning(f"No fundamental data for {ticker}")
                        break

                    results[ticker] = {
                        "company_name": info.get("shortName", ticker),
                        "sector": info.get("sector", "Unknown"),
                        "market_cap": _safe_get(info, "marketCap", 0),
                        "revenue_growth": _safe_get(info, "revenueGrowth", 0),
                        "earnings_growth": _safe_get(info, "earningsGrowth", 0),
                        "revenue_per_share": _safe_get(info, "revenuePerShare", 0),
                        "earnings_quarterly_growth": _safe_get(info, "earningsQuarterlyGrowth", 0),
                        "debt_to_equity": _safe_get(info, "debtToEquity", 0),
                        "current_ratio": _safe_get(info, "currentRatio", 1),
                        "quick_ratio": _safe_get(info, "quickRatio", 1),
                        "interest_coverage": _safe_get(info, "interestCoverage", 0),
                        "free_cashflow": _safe_get(info, "freeCashflow", 0),
                        "operating_cashflow": _safe_get(info, "operatingCashflow", 0),
                        "fcf_per_share": (
                            _safe_get(info, "freeCashflow", 0) / _safe_get(info, "sharesOutstanding", 1)
                            if _safe_get(info, "sharesOutstanding", 0) > 0
                            else 0
                        ),
                        "return_on_equity": _safe_get(info, "returnOnEquity", 0),
                        "return_on_assets": _safe_get(info, "returnOnAssets", 0),
                        "operating_margins": _safe_get(info, "operatingMargins", 0),
                        "profit_margins": _safe_get(info, "profitMargins", 0),
                        "gross_margins": _safe_get(info, "grossMargins", 0),
                        "beta": _safe_get(info, "beta", 1.0),
                        "trailing_pe": _safe_get(info, "trailingPE", 0),
                        "forward_pe": _safe_get(info, "forwardPE", 0),
                        "peg_ratio": _safe_get(info, "pegRatio", 0),
                        "trailing_eps": _safe_get(info, "trailingEps", 0),
                        "forward_eps": _safe_get(info, "forwardEps", 0),
                        "dividend_yield": _safe_get(info, "dividendYield", 0),
                    }
                    break  # success

                except Exception as e:
                    error_str = str(e)
                    if "429" in error_str or "Too Many Requests" in error_str:
                        retries += 1
                        wait_time = base_delay * (2 ** retries) + random.uniform(0, 2)
                        logger.warning(
                            f"429 for {ticker}, retry {retries}/{max_retries}, "
                            f"waiting {wait_time:.1f}s"
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(f"Error fetching fundamentals for {ticker}: {e}")
                        break

            # Jittered delay between tickers
            time.sleep(base_delay + random.uniform(0, 2))

        # Longer cooling period between batches
        inter_batch_delay = 10 + random.uniform(0, 5)
        logger.info(f"Batch cooling: {inter_batch_delay:.1f}s")
        time.sleep(inter_batch_delay)

    logger.info(f"Got fundamentals for {len(results)}/{len(tickers)} tickers")
    return results


# ---------------------------------------------------------------------------
# Legacy functions (kept for single-ticker testing)
# ---------------------------------------------------------------------------

def fetch_company_data(ticker: str) -> Optional[dict]:
    """Fetch financial data for a single company via yfinance."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        if not info or "shortName" not in info:
            logger.warning(f"No data found for {ticker}")
            return None

        hist = stock.history(period="1y")
        if hist.empty:
            logger.warning(f"No price history for {ticker}")
            return None

        current_price = _safe_get(info, "currentPrice") or _safe_get(info, "regularMarketPrice", 0)
        prev_close = _safe_get(info, "previousClose") or _safe_get(info, "regularMarketPreviousClose", 0)
        daily_change_pct = ((current_price - prev_close) / prev_close * 100) if prev_close else 0

        recent_90 = hist.tail(90)
        daily_returns = recent_90["Close"].pct_change().dropna()
        volatility_90d = float(daily_returns.std() * np.sqrt(252)) if len(daily_returns) > 10 else 0.3

        if len(hist) > 126:
            price_6m_ago = float(hist["Close"].iloc[-126])
            momentum_6m = (current_price - price_6m_ago) / price_6m_ago if price_6m_ago > 0 else 0
        else:
            momentum_6m = 0

        high_52w = _safe_get(info, "fiftyTwoWeekHigh", current_price)
        pct_from_high = (current_price / high_52w) if high_52w > 0 else 0.5

        data = {
            "ticker": ticker,
            "company_name": info.get("shortName", ticker),
            "sector": info.get("sector", "Unknown"),
            "market_cap": _safe_get(info, "marketCap", 0),
            "current_price": current_price,
            "daily_change_pct": round(daily_change_pct, 2),
            "revenue_growth": _safe_get(info, "revenueGrowth", 0),
            "earnings_growth": _safe_get(info, "earningsGrowth", 0),
            "revenue_per_share": _safe_get(info, "revenuePerShare", 0),
            "earnings_quarterly_growth": _safe_get(info, "earningsQuarterlyGrowth", 0),
            "debt_to_equity": _safe_get(info, "debtToEquity", 0),
            "current_ratio": _safe_get(info, "currentRatio", 1),
            "quick_ratio": _safe_get(info, "quickRatio", 1),
            "interest_coverage": _safe_get(info, "interestCoverage", 0),
            "free_cashflow": _safe_get(info, "freeCashflow", 0),
            "operating_cashflow": _safe_get(info, "operatingCashflow", 0),
            "fcf_per_share": (
                _safe_get(info, "freeCashflow", 0) / _safe_get(info, "sharesOutstanding", 1)
                if _safe_get(info, "sharesOutstanding", 0) > 0
                else 0
            ),
            "return_on_equity": _safe_get(info, "returnOnEquity", 0),
            "return_on_assets": _safe_get(info, "returnOnAssets", 0),
            "operating_margins": _safe_get(info, "operatingMargins", 0),
            "profit_margins": _safe_get(info, "profitMargins", 0),
            "gross_margins": _safe_get(info, "grossMargins", 0),
            "momentum_6m": momentum_6m,
            "pct_from_52w_high": pct_from_high,
            "beta": _safe_get(info, "beta", 1.0),
            "volatility_90d": volatility_90d,
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
    """Legacy: Fetch data for all companies one by one. Use batch functions instead."""
    all_data = []
    for sector, tickers in COMPANY_TICKERS.items():
        for ticker in tickers:
            logger.info(f"Fetching {ticker} ({sector})...")
            data = fetch_company_data(ticker)
            if data:
                data["sector"] = sector
                all_data.append(data)
            time.sleep(2)
        time.sleep(5)
    logger.info(f"Fetched data for {len(all_data)} companies")
    return all_data

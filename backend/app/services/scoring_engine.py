import logging
import math
from collections import defaultdict

import numpy as np

from app.config import (
    ABILITY_WEIGHTS,
    GRADE_THRESHOLDS,
    MARKET_CAP_ALPHA,
    VOLATILITY_PENALTY_THRESHOLD,
    EMOTIONAL_TAGS,
)

logger = logging.getLogger(__name__)


def _zscore_to_score(z: float) -> float:
    """Transform Z-score to 0-100 ability score."""
    return float(np.clip(50 + (z / 2) * 50, 0, 100))


def _compute_zscore(value: float, mean: float, std: float) -> float:
    """Compute Z-score, returns 0 if std is too small."""
    if std < 1e-9:
        return 0.0
    return (value - mean) / std


def _group_by_sector(companies: list[dict]) -> dict[str, list[dict]]:
    groups = defaultdict(list)
    for c in companies:
        groups[c["sector"]].append(c)
    return dict(groups)


def _sector_stats(sector_companies: list[dict], key: str) -> tuple[float, float]:
    """Return (mean, std) for a metric within a sector."""
    values = [c.get(key, 0) or 0 for c in sector_companies]
    if len(values) < 2:
        return float(np.mean(values)) if values else 0.0, 1.0
    return float(np.mean(values)), max(float(np.std(values)), 1e-9)


def compute_growth_score(company: dict, sector_companies: list[dict]) -> float:
    """Growth: revenue growth + earnings growth + quarterly growth."""
    metrics = ["revenue_growth", "earnings_growth", "earnings_quarterly_growth"]
    z_scores = []
    for metric in metrics:
        mean, std = _sector_stats(sector_companies, metric)
        z = _compute_zscore(company.get(metric, 0) or 0, mean, std)
        z_scores.append(z)
    avg_z = float(np.mean(z_scores))
    return _zscore_to_score(avg_z)


def compute_stability_score(company: dict, sector_companies: list[dict]) -> float:
    """Stability: lower debt-to-equity is better, higher current/quick ratio is better."""
    z_scores = []

    # Debt-to-equity: lower is better → invert
    mean, std = _sector_stats(sector_companies, "debt_to_equity")
    de = company.get("debt_to_equity", 0) or 0
    z = _compute_zscore(de, mean, std)
    z_scores.append(-z)  # Invert: lower debt = higher score

    # Current ratio: higher is better
    for metric in ["current_ratio", "quick_ratio"]:
        mean, std = _sector_stats(sector_companies, metric)
        z = _compute_zscore(company.get(metric, 0) or 0, mean, std)
        z_scores.append(z)

    avg_z = float(np.mean(z_scores))
    return _zscore_to_score(avg_z)


def compute_cashflow_score(company: dict, sector_companies: list[dict]) -> float:
    """Cash flow: FCF, operating cash flow (normalized by market cap)."""
    z_scores = []

    # FCF per share
    mean, std = _sector_stats(sector_companies, "fcf_per_share")
    z = _compute_zscore(company.get("fcf_per_share", 0) or 0, mean, std)
    z_scores.append(z)

    # Operating cash flow / market cap ratio
    mcap = company.get("market_cap", 1) or 1
    ocf_ratio = (company.get("operating_cashflow", 0) or 0) / mcap
    sector_ratios = [
        (c.get("operating_cashflow", 0) or 0) / max(c.get("market_cap", 1) or 1, 1)
        for c in sector_companies
    ]
    mean_r = float(np.mean(sector_ratios)) if sector_ratios else 0
    std_r = max(float(np.std(sector_ratios)), 1e-9) if len(sector_ratios) > 1 else 1.0
    z = _compute_zscore(ocf_ratio, mean_r, std_r)
    z_scores.append(z)

    avg_z = float(np.mean(z_scores))
    return _zscore_to_score(avg_z)


def compute_efficiency_score(company: dict, sector_companies: list[dict]) -> float:
    """Efficiency: ROE, ROA, operating margin, profit margin."""
    metrics = ["return_on_equity", "return_on_assets", "operating_margins", "profit_margins"]
    z_scores = []
    for metric in metrics:
        mean, std = _sector_stats(sector_companies, metric)
        z = _compute_zscore(company.get(metric, 0) or 0, mean, std)
        z_scores.append(z)
    avg_z = float(np.mean(z_scores))
    return _zscore_to_score(avg_z)


def compute_momentum_score(company: dict, sector_companies: list[dict]) -> float:
    """Momentum: 6-month return + proximity to 52-week high."""
    z_scores = []

    for metric in ["momentum_6m", "pct_from_52w_high"]:
        mean, std = _sector_stats(sector_companies, metric)
        z = _compute_zscore(company.get(metric, 0) or 0, mean, std)
        z_scores.append(z)

    avg_z = float(np.mean(z_scores))
    return _zscore_to_score(avg_z)


def compute_earnings_score(company: dict, sector_companies: list[dict]) -> float:
    """Earnings: EPS, PE ratios (inverted - lower PE = better value), dividend yield."""
    z_scores = []

    # Trailing EPS: higher is better
    mean, std = _sector_stats(sector_companies, "trailing_eps")
    z = _compute_zscore(company.get("trailing_eps", 0) or 0, mean, std)
    z_scores.append(z)

    # Forward PE: lower is better (inverted) — only if positive
    fpe = company.get("forward_pe", 0) or 0
    if fpe > 0:
        mean, std = _sector_stats(sector_companies, "forward_pe")
        z = _compute_zscore(fpe, mean, std)
        z_scores.append(-z)

    # Dividend yield: higher is better
    mean, std = _sector_stats(sector_companies, "dividend_yield")
    z = _compute_zscore(company.get("dividend_yield", 0) or 0, mean, std)
    z_scores.append(z)

    avg_z = float(np.mean(z_scores)) if z_scores else 0
    return _zscore_to_score(avg_z)


def compute_total_score(scores: dict[str, float]) -> float:
    """Weighted sum of 6 ability scores."""
    total = sum(scores[ability] * weight for ability, weight in ABILITY_WEIGHTS.items())
    return round(total, 2)


def apply_adjustments(total: float, company: dict) -> float:
    """Apply market cap adjustment and small-cap volatility penalty."""
    adjusted = total

    # Market cap adjustment: slight penalty for mega-caps to level the field
    mcap = company.get("market_cap", 0) or 0
    if mcap > 0:
        log_mcap = math.log10(mcap)
        # Normalize: log10(1T) ≈ 12, log10(1B) ≈ 9
        # Penalty scales from 0 to ~1.5 points for the largest companies
        adjusted -= max(0, (log_mcap - 10)) * MARKET_CAP_ALPHA

    # Small-cap volatility penalty
    vol = company.get("volatility_90d", 0) or 0
    if vol > VOLATILITY_PENALTY_THRESHOLD:
        penalty = (vol - VOLATILITY_PENALTY_THRESHOLD) * 10  # up to ~5 point penalty
        adjusted -= min(penalty, 5)

    return float(np.clip(adjusted, 0, 100))


def assign_grade(total_score: float) -> str:
    for grade, threshold in GRADE_THRESHOLDS.items():
        if total_score >= threshold:
            return grade
    return "D"


def assign_emotional_tag(scores: dict[str, float]) -> str:
    """Assign an emotional tag based on the company's score profile."""
    max_ability = max(scores, key=scores.get)
    max_score = scores[max_ability]
    min_score = min(scores.values())

    # Check if balanced (all scores within 15 points of each other)
    if max_score - min_score < 15:
        avg = sum(scores.values()) / len(scores)
        if avg >= 55:
            return EMOTIONAL_TAGS["balanced"]
        return EMOTIONAL_TAGS["underperformer"]

    tag_map = {
        "growth": "growth_dominant",
        "stability": "stability_dominant",
        "cashflow": "cashflow_dominant",
        "efficiency": "efficiency_dominant",
        "momentum": "momentum_dominant",
        "earnings": "earnings_dominant",
    }
    return EMOTIONAL_TAGS.get(tag_map.get(max_ability, "balanced"), EMOTIONAL_TAGS["balanced"])


def score_companies(companies: list[dict]) -> list[dict]:
    """Score all companies using sector-relative Z-scores. Returns enriched dicts."""
    sector_groups = _group_by_sector(companies)
    scored = []

    for company in companies:
        sector = company["sector"]
        sector_peers = sector_groups.get(sector, [company])

        ability_scores = {
            "growth": round(compute_growth_score(company, sector_peers), 2),
            "stability": round(compute_stability_score(company, sector_peers), 2),
            "cashflow": round(compute_cashflow_score(company, sector_peers), 2),
            "efficiency": round(compute_efficiency_score(company, sector_peers), 2),
            "momentum": round(compute_momentum_score(company, sector_peers), 2),
            "earnings": round(compute_earnings_score(company, sector_peers), 2),
        }

        total = compute_total_score(ability_scores)
        total = apply_adjustments(total, company)
        grade = assign_grade(total)
        emotional_tag = assign_emotional_tag(ability_scores)

        # Build raw_metrics for the card back
        raw_metrics = {
            "revenue_growth": company.get("revenue_growth"),
            "earnings_growth": company.get("earnings_growth"),
            "debt_to_equity": company.get("debt_to_equity"),
            "current_ratio": company.get("current_ratio"),
            "free_cashflow": company.get("free_cashflow"),
            "operating_cashflow": company.get("operating_cashflow"),
            "return_on_equity": company.get("return_on_equity"),
            "return_on_assets": company.get("return_on_assets"),
            "operating_margins": company.get("operating_margins"),
            "profit_margins": company.get("profit_margins"),
            "trailing_pe": company.get("trailing_pe"),
            "forward_pe": company.get("forward_pe"),
            "trailing_eps": company.get("trailing_eps"),
            "dividend_yield": company.get("dividend_yield"),
            "beta": company.get("beta"),
            "momentum_6m": company.get("momentum_6m"),
        }

        scored.append({
            **company,
            "growth_score": ability_scores["growth"],
            "stability_score": ability_scores["stability"],
            "cashflow_score": ability_scores["cashflow"],
            "efficiency_score": ability_scores["efficiency"],
            "momentum_score": ability_scores["momentum"],
            "earnings_score": ability_scores["earnings"],
            "total_score": round(total, 2),
            "grade": grade,
            "emotional_tag": emotional_tag,
            "raw_metrics": raw_metrics,
        })

    return scored

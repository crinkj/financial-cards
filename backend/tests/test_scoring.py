"""Unit tests for the scoring engine."""
import pytest

from app.services.scoring_engine import (
    _zscore_to_score,
    _compute_zscore,
    compute_growth_score,
    compute_stability_score,
    compute_total_score,
    apply_adjustments,
    assign_grade,
    assign_emotional_tag,
    score_companies,
)


def test_zscore_to_score_zero():
    assert _zscore_to_score(0) == 50.0


def test_zscore_to_score_positive():
    score = _zscore_to_score(2.0)
    assert score == 100.0  # clipped at 100


def test_zscore_to_score_negative():
    score = _zscore_to_score(-2.0)
    assert score == 0.0  # clipped at 0


def test_zscore_to_score_moderate():
    score = _zscore_to_score(1.0)
    assert score == 75.0


def test_compute_zscore():
    assert _compute_zscore(10, 5, 5) == 1.0
    assert _compute_zscore(5, 5, 5) == 0.0
    assert _compute_zscore(0, 5, 5) == -1.0


def test_compute_zscore_zero_std():
    assert _compute_zscore(10, 5, 0) == 0.0


def test_assign_grade():
    assert assign_grade(85) == "S"
    assert assign_grade(80) == "S"
    assert assign_grade(70) == "A"
    assert assign_grade(55) == "B"
    assert assign_grade(40) == "C"
    assert assign_grade(20) == "D"


def test_assign_emotional_tag_balanced():
    scores = {"growth": 60, "stability": 58, "cashflow": 62, "efficiency": 59, "momentum": 61, "earnings": 57}
    tag = assign_emotional_tag(scores)
    assert tag == "균형의 마스터"


def test_assign_emotional_tag_growth_dominant():
    scores = {"growth": 90, "stability": 40, "cashflow": 45, "efficiency": 50, "momentum": 55, "earnings": 35}
    tag = assign_emotional_tag(scores)
    assert tag == "성장 괴물"


SAMPLE_COMPANIES = [
    {
        "ticker": "AAA",
        "company_name": "Alpha Corp",
        "sector": "Technology",
        "market_cap": 500_000_000_000,
        "current_price": 150,
        "daily_change_pct": 1.5,
        "revenue_growth": 0.25,
        "earnings_growth": 0.30,
        "earnings_quarterly_growth": 0.20,
        "debt_to_equity": 50,
        "current_ratio": 2.0,
        "quick_ratio": 1.5,
        "interest_coverage": 15,
        "free_cashflow": 20_000_000_000,
        "operating_cashflow": 30_000_000_000,
        "fcf_per_share": 5.0,
        "return_on_equity": 0.30,
        "return_on_assets": 0.15,
        "operating_margins": 0.25,
        "profit_margins": 0.20,
        "gross_margins": 0.40,
        "momentum_6m": 0.15,
        "pct_from_52w_high": 0.95,
        "beta": 1.1,
        "volatility_90d": 0.25,
        "trailing_pe": 25,
        "forward_pe": 22,
        "peg_ratio": 1.5,
        "trailing_eps": 6.0,
        "forward_eps": 7.0,
        "dividend_yield": 0.01,
    },
    {
        "ticker": "BBB",
        "company_name": "Beta Inc",
        "sector": "Technology",
        "market_cap": 100_000_000_000,
        "current_price": 80,
        "daily_change_pct": -0.5,
        "revenue_growth": 0.10,
        "earnings_growth": 0.05,
        "earnings_quarterly_growth": 0.08,
        "debt_to_equity": 100,
        "current_ratio": 1.2,
        "quick_ratio": 0.8,
        "interest_coverage": 5,
        "free_cashflow": 5_000_000_000,
        "operating_cashflow": 8_000_000_000,
        "fcf_per_share": 2.0,
        "return_on_equity": 0.12,
        "return_on_assets": 0.06,
        "operating_margins": 0.15,
        "profit_margins": 0.10,
        "gross_margins": 0.30,
        "momentum_6m": -0.05,
        "pct_from_52w_high": 0.70,
        "beta": 1.3,
        "volatility_90d": 0.35,
        "trailing_pe": 35,
        "forward_pe": 30,
        "peg_ratio": 3.0,
        "trailing_eps": 2.3,
        "forward_eps": 2.7,
        "dividend_yield": 0.005,
    },
]


def test_score_companies_returns_all():
    results = score_companies(SAMPLE_COMPANIES)
    assert len(results) == 2


def test_score_companies_has_required_fields():
    results = score_companies(SAMPLE_COMPANIES)
    for r in results:
        assert "growth_score" in r
        assert "stability_score" in r
        assert "cashflow_score" in r
        assert "efficiency_score" in r
        assert "momentum_score" in r
        assert "earnings_score" in r
        assert "total_score" in r
        assert "grade" in r
        assert "emotional_tag" in r
        assert 0 <= r["total_score"] <= 100


def test_score_companies_better_company_scores_higher():
    results = score_companies(SAMPLE_COMPANIES)
    alpha = next(r for r in results if r["ticker"] == "AAA")
    beta = next(r for r in results if r["ticker"] == "BBB")
    # Alpha has better fundamentals across the board
    assert alpha["growth_score"] > beta["growth_score"]


def test_apply_adjustments_mega_cap_penalty():
    mega = apply_adjustments(70, {"market_cap": 2_000_000_000_000, "volatility_90d": 0.2})
    small = apply_adjustments(70, {"market_cap": 5_000_000_000, "volatility_90d": 0.2})
    assert mega < small  # Mega-cap gets penalized more


def test_apply_adjustments_volatility_penalty():
    low_vol = apply_adjustments(70, {"market_cap": 50_000_000_000, "volatility_90d": 0.3})
    high_vol = apply_adjustments(70, {"market_cap": 50_000_000_000, "volatility_90d": 0.7})
    assert high_vol < low_vol

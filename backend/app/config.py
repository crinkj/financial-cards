import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./financial_cards.db")

# Curated company list (~100 companies across major sectors)
COMPANY_TICKERS = {
    "Technology": [
        "AAPL", "MSFT", "GOOGL", "META", "NVDA", "TSLA", "AMD", "INTC",
        "CRM", "ADBE", "ORCL", "CSCO", "AVGO", "TXN", "QCOM",
    ],
    "Healthcare": [
        "JNJ", "UNH", "PFE", "ABBV", "MRK", "TMO", "ABT", "LLY",
        "BMY", "AMGN", "GILD", "MDT", "ISRG", "DHR",
    ],
    "Financials": [
        "JPM", "BAC", "WFC", "GS", "MS", "BLK", "C", "AXP",
        "SCHW", "USB", "PNC", "TFC", "COF", "CME",
    ],
    "Consumer Discretionary": [
        "AMZN", "HD", "MCD", "NKE", "SBUX", "LOW", "TJX", "BKNG",
        "CMG", "ABNB", "ORLY", "ROST",
    ],
    "Consumer Staples": [
        "PG", "KO", "PEP", "COST", "WMT", "PM", "MO", "CL",
        "MDLZ", "GIS", "KHC", "STZ",
    ],
    "Energy": [
        "XOM", "CVX", "COP", "SLB", "EOG", "MPC", "PSX", "VLO",
        "OXY", "HAL",
    ],
    "Industrials": [
        "CAT", "HON", "UPS", "BA", "RTX", "GE", "LMT", "DE",
        "MMM", "UNP", "FDX", "WM",
    ],
    "Communication Services": [
        "GOOG", "DIS", "CMCSA", "NFLX", "T", "VZ", "TMUS", "EA",
        "ATVI", "MTCH",
    ],
    "Utilities": [
        "NEE", "DUK", "SO", "D", "AEP", "SRE", "EXC",
    ],
    "Real Estate": [
        "AMT", "PLD", "CCI", "EQIX", "SPG", "O", "PSA",
    ],
}

# Scoring weights for total score
ABILITY_WEIGHTS = {
    "growth": 0.25,
    "stability": 0.20,
    "cashflow": 0.15,
    "efficiency": 0.15,
    "momentum": 0.15,
    "earnings": 0.10,
}

# Grade thresholds (total_score)
GRADE_THRESHOLDS = {
    "S": 80,
    "A": 65,
    "B": 50,
    "C": 35,
    # Below 35 = D
}

# Market cap adjustment alpha
MARKET_CAP_ALPHA = 0.5

# Small-cap volatility penalty threshold (90-day annualized vol)
VOLATILITY_PENALTY_THRESHOLD = 0.50

# Emotional tags based on dominant abilities
EMOTIONAL_TAGS = {
    "growth_dominant": "성장 괴물",        # Growth Monster
    "stability_dominant": "철벽 방어",      # Iron Wall Defense
    "cashflow_dominant": "현금 부자",       # Cash Rich
    "efficiency_dominant": "효율의 달인",    # Efficiency Master
    "momentum_dominant": "질주 본능",       # Sprint Instinct
    "earnings_dominant": "수익 머신",       # Earnings Machine
    "balanced": "균형의 마스터",            # Balance Master
    "underperformer": "잠재력 충전 중",     # Charging Potential
}

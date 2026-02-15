import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./financial_cards.db")

# ---------------------------------------------------------------------------
# US Stocks (~200 companies across major sectors)
# ---------------------------------------------------------------------------
US_TICKERS = {
    "Technology": [
        "AAPL", "MSFT", "GOOGL", "META", "NVDA", "TSLA", "AMD", "INTC",
        "CRM", "ADBE", "ORCL", "CSCO", "AVGO", "TXN", "QCOM", "NOW",
        "SHOP", "SQ", "SNOW", "PLTR", "UBER", "PANW", "CRWD", "DDOG",
        "MU", "ANET", "MRVL", "KLAC", "LRCX", "SNPS",
    ],
    "Healthcare": [
        "JNJ", "UNH", "PFE", "ABBV", "MRK", "TMO", "ABT", "LLY",
        "BMY", "AMGN", "GILD", "MDT", "ISRG", "DHR", "VRTX", "REGN",
        "ZTS", "DXCM", "IDXX", "EW", "A", "IQV", "BIIB", "MRNA",
    ],
    "Financials": [
        "JPM", "BAC", "WFC", "GS", "MS", "BLK", "C", "AXP",
        "SCHW", "USB", "PNC", "TFC", "COF", "CME", "ICE", "MCO",
        "SPGI", "AON", "MMC", "CB", "AIG", "MET", "PRU", "TRV",
    ],
    "Consumer Discretionary": [
        "AMZN", "HD", "MCD", "NKE", "SBUX", "LOW", "TJX", "BKNG",
        "CMG", "ABNB", "ORLY", "ROST", "MAR", "HLT", "DHI", "LEN",
        "F", "GM", "LULU", "DECK", "EBAY", "ETSY",
    ],
    "Consumer Staples": [
        "PG", "KO", "PEP", "COST", "WMT", "PM", "MO", "CL",
        "MDLZ", "GIS", "KHC", "STZ", "KDP", "SYY", "HSY", "MKC",
        "CLX", "K", "CAG", "TSN",
    ],
    "Energy": [
        "XOM", "CVX", "COP", "SLB", "EOG", "MPC", "PSX", "VLO",
        "OXY", "HAL", "DVN", "FANG", "HES", "WMB", "KMI", "OKE",
    ],
    "Industrials": [
        "CAT", "HON", "UPS", "BA", "RTX", "GE", "LMT", "DE",
        "MMM", "UNP", "FDX", "WM", "EMR", "ITW", "GD", "NOC",
        "CSX", "NSC", "PCAR", "ETN", "ROK", "FAST",
    ],
    "Communication Services": [
        "GOOG", "DIS", "CMCSA", "NFLX", "T", "VZ", "TMUS", "EA",
        "TTWO", "MTCH", "RBLX", "SPOT", "PINS", "SNAP",
    ],
    "Utilities": [
        "NEE", "DUK", "SO", "D", "AEP", "SRE", "EXC", "XEL",
        "WEC", "ED", "ES", "AWK",
    ],
    "Real Estate": [
        "AMT", "PLD", "CCI", "EQIX", "SPG", "O", "PSA", "DLR",
        "WELL", "AVB", "EQR", "VICI",
    ],
}

# ---------------------------------------------------------------------------
# Korean Stocks (KOSPI .KS / KOSDAQ .KQ) - ~80 companies
# ---------------------------------------------------------------------------
KR_TICKERS = {
    "KR_Technology": [
        "005930.KS",  # Samsung Electronics
        "000660.KS",  # SK Hynix
        "035420.KS",  # Naver
        "035720.KS",  # Kakao
        "006400.KS",  # Samsung SDI
        "066570.KS",  # LG Electronics
        "034730.KS",  # SK Inc
        "036570.KS",  # NCsoft
        "263750.KS",  # Pearl Abyss
        "042700.KQ",  # Hanmi Semiconductor
        "403870.KQ",  # HPSP
        "247540.KS",  # Ecopro BM
        "086520.KS",  # Ecopro
        "377300.KS",  # Kakao Pay
        "352820.KS",  # Hive
    ],
    "KR_Financials": [
        "105560.KS",  # KB Financial
        "055550.KS",  # Shinhan Financial
        "086790.KS",  # Hana Financial
        "316140.KS",  # Woori Financial
        "024110.KS",  # Industrial Bank of Korea
        "000810.KS",  # Samsung Fire & Marine
        "032830.KS",  # Samsung Life
        "005830.KS",  # DB Insurance
        "138930.KS",  # BNK Financial
    ],
    "KR_Automotive": [
        "005380.KS",  # Hyundai Motor
        "000270.KS",  # Kia
        "012330.KS",  # Hyundai Mobis
        "018880.KS",  # Hanon Systems
        "298050.KS",  # Hyundai AutoEver
        "214370.KS",  # HL Mando
    ],
    "KR_Bio & Healthcare": [
        "207940.KS",  # Samsung Biologics
        "068270.KS",  # Celltrion
        "326030.KS",  # SK Biopharmaceuticals
        "196170.KQ",  # Alteogen
        "145020.KS",  # Hugel
        "141080.KS",  # Legaland
        "091990.KQ",  # Celltrion Healthcare
    ],
    "KR_Consumer & Retail": [
        "051900.KS",  # LG H&H
        "090430.KS",  # Amorepacific
        "004170.KS",  # Shinsegae
        "023530.KS",  # Lotte Shopping
        "069960.KS",  # Hyundai Department Store
        "004990.KS",  # Lotte Corp
        "097950.KS",  # CJ Cheiljedang
    ],
    "KR_Energy & Materials": [
        "096770.KS",  # SK Innovation
        "010950.KS",  # S-Oil
        "051910.KS",  # LG Chem
        "006260.KS",  # LS Corp
        "005490.KS",  # POSCO Holdings
        "010130.KS",  # Korea Zinc
        "011170.KS",  # Lotte Chemical
    ],
    "KR_Industrial": [
        "009150.KS",  # Samsung Electro-Mechanics
        "028260.KS",  # Samsung C&T
        "000720.KS",  # Hyundai E&C
        "034220.KS",  # LG Display
        "003550.KS",  # LG Corp
        "011200.KS",  # Hyundai Merchant Marine (HMM)
        "010140.KS",  # Samsung Heavy Industries
        "042660.KS",  # Daewoo E&C (HDC)
    ],
}

# Combined ticker list
COMPANY_TICKERS = {**US_TICKERS, **KR_TICKERS}

# ---------------------------------------------------------------------------
# Scoring configuration
# ---------------------------------------------------------------------------

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

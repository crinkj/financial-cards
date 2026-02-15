# 🎴 Game-Based Financial Card App – Quant Design Document

## 0. Product Vision

A financial education platform that transforms real companies into game-style cards.
Each company is scored using real financial data and displayed as a collectible battle card.

Goal:
- Make financial literacy accessible
- Translate complex financial metrics into intuitive power stats
- Combine education + entertainment

---

# 1️⃣ Ability System Design (Quant-Based)

All scores are normalized to 0–100.
Primary comparison baseline: Sector-relative Z-score.

Z-score normalization:

Z = (X - μ_sector) / σ_sector

Score transformation (clipped at ±2σ):

Score = 50 + (Z / 2) * 50
Score is clipped to [0, 100]

---

## 1. ⚔️ 공격력 (Growth Power)

**Financial Metrics**
- Revenue CAGR (3Y)
- EPS CAGR (3Y)

**Formula**
Growth_raw = 0.6 * Revenue_CAGR + 0.4 * EPS_CAGR
Growth_score = Sector_Z_Normalize(Growth_raw)

**Range**: 0–100

**User Explanation**
"이 회사는 최근 몇 년 동안 얼마나 빠르게 성장하고 있나요?"

---

## 2. 🛡 방어력 (Financial Stability)

**Financial Metrics**
- Debt-to-Equity Ratio
- Interest Coverage Ratio

**Formula**
Def_raw = -0.5 * D/E + 0.5 * InterestCoverage
Def_score = Sector_Z_Normalize(Def_raw)

**Range**: 0–100

**User Explanation**
"빚이 적고 위기에서도 버틸 수 있는 기업인가요?"

---

## 3. 🔥 마력 (Cash Flow Power)

**Financial Metrics**
- Free Cash Flow Margin
- 3Y FCF Growth

**Formula**
Magic_raw = 0.7 * FCF_Margin + 0.3 * FCF_Growth
Magic_score = Sector_Z_Normalize(Magic_raw)

**User Explanation**
"이 회사는 실제로 돈을 잘 벌고 있나요?"

---

## 4. 🧠 지능 (Capital Efficiency)

**Financial Metrics**
- ROE
- ROIC

**Formula**
IQ_raw = 0.5 * ROE + 0.5 * ROIC
IQ_score = Sector_Z_Normalize(IQ_raw)

**User Explanation**
"투입한 자본을 얼마나 효율적으로 사용하나요?"

---

## 5. ⚡ 스피드 (Momentum Acceleration)

**Financial Metrics**
- Latest YoY Revenue Growth
- Revenue Growth Acceleration (Δ Growth)

**Formula**
Speed_raw = 0.7 * YoY_Growth + 0.3 * Acceleration
Speed_score = Sector_Z_Normalize(Speed_raw)

**User Explanation**
"최근에 더 빨라지고 있나요?"

---

## 6. ❤️ 체력 (Earnings Stability)

**Financial Metrics**
- Operating Margin StdDev (5Y)
- Earnings Consistency Ratio

**Formula**
Stamina_raw = -StdDev_OpMargin + Consistency
Stamina_score = Sector_Z_Normalize(Stamina_raw)

**User Explanation**
"실적이 안정적인가요, 들쭉날쭉한가요?"

---

# 2️⃣ Total Grade Calculation

## Weighted Sum

Total_score =
0.25 * 공격력 +
0.20 * 방어력 +
0.15 * 마력 +
0.15 * 지능 +
0.15 * 스피드 +
0.10 * 체력

---

## Grade Threshold

| Grade | Score |
|--------|--------|
| S | 85+ |
| A | 70–84 |
| B | 55–69 |
| C | 40–54 |
| D | <40 |

---

## Market Cap Adjustment

Mega Cap bias correction:

Adj_score = Total_score - log(MarketCap) * α

Small cap volatility penalty:

If 90d_volatility > threshold:
Score *= 0.95

---

## Sector vs Market Mode

- Default: Sector-relative scoring
- Optional: Market-wide ranking mode

---

# 3️⃣ UX Design

## Front Card

- Company Name
- Sector Icon
- Total Grade (Large Badge)
- Radar Chart (6 stats)
- Current Price + Daily Change

Emotional Hook:
"🔥 S등급 성장 괴물" 같은 한 줄 태그

---

## Back Card

- Revenue / Net Income Summary
- 3Y CAGR
- Debt Ratio
- ROE
- FCF
- AI-generated plain-language summary

---

# 4️⃣ Game Mechanics

## Daily Top 10
- Highest total score today

## Sector Champion
- #1 score per sector

## Portfolio Battle Power

Portfolio_power = Σ(weighted_score × portfolio_weight)

## Friend Comparison
- Rank system
- Shareable card image

---

# 5️⃣ Education Layer

- Tap stat → metric explanation
- Mini quiz unlocks badge
- Simulated portfolio battle mode

---

# 6️⃣ Monetization Strategy

## Free Tier
- Basic scores
- Top 100 companies

## Premium ($9.99/month)
- Full market access
- Historical score tracking
- AI card recommendations
- Deep factor breakdown

## API Sales
- Fintech integration
- Quant signal feed

---

# Technical Implementation Notes

- Daily batch recompute (Airflow)
- Feature store table for stats
- Precomputed score table for fast API response
- Redis caching for hot cards

---

# Positioning

"Bloomberg meets Pokémon for finance beginners."
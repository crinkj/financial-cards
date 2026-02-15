export type Lang = 'ko' | 'en';

export const translations = {
  // Navigation
  nav_cards: { en: 'Collection', ko: '콜렉션' },
  nav_rankings: { en: 'Arena', ko: '아레나' },
  app_title: { en: 'Stockmon', ko: '스톡몬' },

  // Home page
  hero_title: { en: 'Gotta Catch \'Em All!', ko: '모두 잡아라!' },
  hero_subtitle: {
    en: 'Real stocks. Battle stats. Collect the market.',
    ko: '실제 주식. 배틀 스탯. 시장을 수집하라.',
  },
  search_placeholder: { en: 'Search Stockmon...', ko: '스톡몬 검색...' },
  all_sectors: { en: 'All Types', ko: '전체 타입' },
  score_label: { en: 'PWR', ko: '전투력' },
  loading_cards: { en: 'Summoning Stockmons...', ko: '스톡몬 소환 중...' },
  error_load_cards: {
    en: 'Connection lost! Check if the server is running.',
    ko: '연결 실패! 서버가 실행 중인지 확인하세요.',
  },
  empty_cards: {
    en: 'No Stockmons found. Run batch update to discover them.',
    ko: '스톡몬을 찾을 수 없습니다. 배치 업데이트를 실행하세요.',
  },

  // Card front
  total_score: { en: 'POWER', ko: '전투력' },

  // Card back
  back_score: { en: 'PWR', ko: '전투력' },
  back_growth: { en: 'Growth', ko: '성장' },
  back_revenue_growth: { en: 'Revenue Growth', ko: '매출 성장률' },
  back_earnings_growth: { en: 'Earnings Growth', ko: '이익 성장률' },
  back_stability: { en: 'Stability', ko: '안정성' },
  back_debt_equity: { en: 'Debt/Equity', ko: '부채비율' },
  back_current_ratio: { en: 'Current Ratio', ko: '유동비율' },
  back_cashflow: { en: 'Cash Flow', ko: '현금흐름' },
  back_fcf: { en: 'Free Cash Flow', ko: '잉여현금흐름' },
  back_ocf: { en: 'Operating CF', ko: '영업현금흐름' },
  back_efficiency: { en: 'Efficiency', ko: '효율성' },
  back_roe: { en: 'ROE', ko: 'ROE' },
  back_roa: { en: 'ROA', ko: 'ROA' },
  back_op_margin: { en: 'Operating Margin', ko: '영업이익률' },
  back_profit_margin: { en: 'Profit Margin', ko: '순이익률' },
  back_valuation: { en: 'Valuation', ko: '밸류에이션' },
  back_trailing_pe: { en: 'Trailing P/E', ko: 'Trailing P/E' },
  back_forward_pe: { en: 'Forward P/E', ko: 'Forward P/E' },
  back_trailing_eps: { en: 'Trailing EPS', ko: 'Trailing EPS' },
  back_dividend_yield: { en: 'Dividend Yield', ko: '배당수익률' },
  back_tap_flip: { en: 'Tap to flip', ko: '탭하여 뒤집기' },

  // Radar chart labels
  radar_growth: { en: 'Growth', ko: '성장' },
  radar_stability: { en: 'Stability', ko: '안정' },
  radar_cashflow: { en: 'CashFlow', ko: '현금' },
  radar_efficiency: { en: 'Efficiency', ko: '효율' },
  radar_momentum: { en: 'Momentum', ko: '모멘텀' },
  radar_earnings: { en: 'Earnings', ko: '수익' },
  // Radar sub-labels (game-style)
  radar_sub_growth: { en: 'ATK', ko: '공격력' },
  radar_sub_stability: { en: 'DEF', ko: '방어력' },
  radar_sub_cashflow: { en: 'MP', ko: '마력' },
  radar_sub_efficiency: { en: 'INT', ko: '지능' },
  radar_sub_momentum: { en: 'SPD', ko: '스피드' },
  radar_sub_earnings: { en: 'HP', ko: '체력' },

  // Rankings
  daily_top_10: { en: 'Top 10 Legends', ko: '레전드 Top 10' },
  sector_champions: { en: 'Type Champions', ko: '타입 챔피언' },
  rankings_title: { en: 'Arena', ko: '아레나' },
  rankings_subtitle: { en: 'Who\'s the strongest Stockmon?', ko: '가장 강한 스톡몬은?' },
  error_load_rankings: {
    en: 'Failed to load arena.',
    ko: '아레나를 불러오지 못했습니다.',
  },

  // Sector names (game "type" style)
  sector_technology: { en: 'Tech', ko: '테크' },
  sector_healthcare: { en: 'Health', ko: '헬스' },
  sector_financials: { en: 'Finance', ko: '금융' },
  sector_consumer_disc: { en: 'Consumer', ko: '소비재' },
  sector_consumer_staples: { en: 'Staples', ko: '필수재' },
  sector_energy: { en: 'Energy', ko: '에너지' },
  sector_industrials: { en: 'Industry', ko: '산업' },
  sector_communication: { en: 'Comms', ko: '통신' },
  sector_utilities: { en: 'Utility', ko: '유틸' },
  sector_real_estate: { en: 'Realty', ko: '부동산' },
  sector_kr_technology: { en: 'KR Tech', ko: '한국 테크' },
  sector_kr_financials: { en: 'KR Finance', ko: '한국 금융' },
  sector_kr_automotive: { en: 'KR Auto', ko: '한국 자동차' },
  sector_kr_bio: { en: 'KR Bio', ko: '한국 바이오' },
  sector_kr_consumer: { en: 'KR Consumer', ko: '한국 소비재' },
  sector_kr_energy: { en: 'KR Energy', ko: '한국 에너지' },
  sector_kr_industrial: { en: 'KR Industry', ko: '한국 산업' },
} as const;

export type TranslationKey = keyof typeof translations;

// Sector name translation mapping (API sector string → translation key)
const SECTOR_KEY_MAP: Record<string, TranslationKey> = {
  'Technology': 'sector_technology',
  'Healthcare': 'sector_healthcare',
  'Financials': 'sector_financials',
  'Consumer Discretionary': 'sector_consumer_disc',
  'Consumer Staples': 'sector_consumer_staples',
  'Energy': 'sector_energy',
  'Industrials': 'sector_industrials',
  'Communication Services': 'sector_communication',
  'Utilities': 'sector_utilities',
  'Real Estate': 'sector_real_estate',
  'KR_Technology': 'sector_kr_technology',
  'KR_Financials': 'sector_kr_financials',
  'KR_Automotive': 'sector_kr_automotive',
  'KR_Bio & Healthcare': 'sector_kr_bio',
  'KR_Consumer & Retail': 'sector_kr_consumer',
  'KR_Energy & Materials': 'sector_kr_energy',
  'KR_Industrial': 'sector_kr_industrial',
};

export function translateSector(sector: string, lang: Lang): string {
  const key = SECTOR_KEY_MAP[sector];
  if (!key) return sector;
  return translations[key][lang];
}

// Emotional tag translation (backend stores Korean)
const EMOTIONAL_TAG_EN: Record<string, string> = {
  '성장 괴물': 'Growth Monster',
  '철벽 방어': 'Iron Wall',
  '현금 부자': 'Cash King',
  '효율의 달인': 'Efficiency Lord',
  '질주 본능': 'Speed Demon',
  '수익 머신': 'Profit Machine',
  '균형의 마스터': 'Balance Master',
  '잠재력 충전 중': 'Charging Up...',
};

export function translateEmotionalTag(tag: string, lang: Lang): string {
  if (lang === 'ko') return tag;
  return EMOTIONAL_TAG_EN[tag] || tag;
}

// Grade border gradient CSS (for game card frames)
export const GRADE_BORDER_GRADIENT: Record<string, string> = {
  S: 'from-yellow-300 via-amber-500 to-yellow-300',
  A: 'from-purple-400 via-fuchsia-500 to-purple-400',
  B: 'from-blue-400 via-cyan-500 to-blue-400',
  C: 'from-green-400 via-emerald-500 to-green-400',
  D: 'from-gray-400 via-slate-500 to-gray-400',
};

// Sector type color pills
export const SECTOR_TYPE_COLORS: Record<string, string> = {
  'Technology': 'bg-blue-500/30 text-blue-300 border-blue-500/50',
  'Healthcare': 'bg-pink-500/30 text-pink-300 border-pink-500/50',
  'Financials': 'bg-emerald-500/30 text-emerald-300 border-emerald-500/50',
  'Consumer Discretionary': 'bg-orange-500/30 text-orange-300 border-orange-500/50',
  'Consumer Staples': 'bg-lime-500/30 text-lime-300 border-lime-500/50',
  'Energy': 'bg-yellow-500/30 text-yellow-300 border-yellow-500/50',
  'Industrials': 'bg-slate-400/30 text-slate-300 border-slate-400/50',
  'Communication Services': 'bg-violet-500/30 text-violet-300 border-violet-500/50',
  'Utilities': 'bg-cyan-500/30 text-cyan-300 border-cyan-500/50',
  'Real Estate': 'bg-amber-500/30 text-amber-300 border-amber-500/50',
  'KR_Technology': 'bg-blue-600/30 text-blue-200 border-blue-600/50',
  'KR_Financials': 'bg-emerald-600/30 text-emerald-200 border-emerald-600/50',
  'KR_Automotive': 'bg-red-500/30 text-red-300 border-red-500/50',
  'KR_Bio & Healthcare': 'bg-pink-600/30 text-pink-200 border-pink-600/50',
  'KR_Consumer & Retail': 'bg-orange-600/30 text-orange-200 border-orange-600/50',
  'KR_Energy & Materials': 'bg-yellow-600/30 text-yellow-200 border-yellow-600/50',
  'KR_Industrial': 'bg-slate-500/30 text-slate-200 border-slate-500/50',
};

export interface CardSummary {
  ticker: string;
  company_name: string;
  sector: string;
  grade: string;
  total_score: number;
  current_price: number | null;
  daily_change_pct: number | null;
}

export interface AbilityScores {
  growth: number;
  stability: number;
  cashflow: number;
  efficiency: number;
  momentum: number;
  earnings: number;
}

export interface CardDetail {
  ticker: string;
  company_name: string;
  sector: string;
  market_cap: number | null;
  current_price: number | null;
  daily_change_pct: number | null;
  scores: AbilityScores;
  total_score: number;
  grade: string;
  emotional_tag: string;
  raw_metrics: Record<string, number | null>;
  updated_at: string | null;
}

export interface RankingEntry {
  rank: number;
  ticker: string;
  company_name: string;
  sector: string;
  total_score: number;
  grade: string;
}

export interface SectorChampion {
  sector: string;
  ticker: string;
  company_name: string;
  total_score: number;
  grade: string;
}

export type Grade = 'S' | 'A' | 'B' | 'C' | 'D';

export const GRADE_COLORS: Record<Grade, string> = {
  S: '#ffd700',
  A: '#a855f7',
  B: '#3b82f6',
  C: '#22c55e',
  D: '#6b7280',
};

export const GRADE_BG_CLASSES: Record<Grade, string> = {
  S: 'bg-yellow-500/20 border-yellow-500 shadow-glow-gold',
  A: 'bg-purple-500/20 border-purple-500 shadow-glow-purple',
  B: 'bg-blue-500/20 border-blue-500 shadow-glow-blue',
  C: 'bg-green-500/20 border-green-500 shadow-glow-green',
  D: 'bg-gray-500/20 border-gray-500',
};

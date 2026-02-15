import { CardSummary, CardDetail, RankingEntry, SectorChampion } from '@/types/card';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

async function fetchJSON<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

export async function getCards(params?: {
  sector?: string;
  search?: string;
  skip?: number;
  limit?: number;
}): Promise<CardSummary[]> {
  const searchParams = new URLSearchParams();
  if (params?.sector) searchParams.set('sector', params.sector);
  if (params?.search) searchParams.set('search', params.search);
  if (params?.skip) searchParams.set('skip', String(params.skip));
  if (params?.limit) searchParams.set('limit', String(params.limit));
  const qs = searchParams.toString();
  return fetchJSON<CardSummary[]>(`/api/cards${qs ? `?${qs}` : ''}`);
}

export async function getCard(ticker: string): Promise<CardDetail> {
  return fetchJSON<CardDetail>(`/api/cards/${ticker}`);
}

export async function getTop10(): Promise<RankingEntry[]> {
  return fetchJSON<RankingEntry[]>('/api/rankings/top10');
}

export async function getSectorChampions(): Promise<SectorChampion[]> {
  return fetchJSON<SectorChampion[]>('/api/rankings/sectors');
}

export async function getSectors(): Promise<string[]> {
  return fetchJSON<string[]>('/api/rankings/sectors/list');
}

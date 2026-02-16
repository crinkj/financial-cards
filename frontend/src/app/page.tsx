'use client';

import { useEffect, useState, useCallback } from 'react';
import { CardDetail, CardSummary, Grade, GRADE_COLORS } from '@/types/card';
import { getCards, getCard, getSectors } from '@/lib/api';
import CardFlip from '@/components/Card/CardFlip';
import GradeBadge from '@/components/GradeBadge';
import { useLanguage } from '@/lib/LanguageContext';
import { translateSector, SECTOR_TYPE_COLORS } from '@/lib/i18n';

export default function HomePage() {
  const { t, lang } = useLanguage();
  const [cards, setCards] = useState<CardSummary[]>([]);
  const [selectedCard, setSelectedCard] = useState<CardDetail | null>(null);
  const [sectors, setSectors] = useState<string[]>([]);
  const [selectedSector, setSelectedSector] = useState<string>('');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const fetchCards = useCallback(async () => {
    setLoading(true);
    setError(false);
    try {
      const params: { sector?: string; search?: string } = {};
      if (selectedSector) params.sector = selectedSector;
      if (searchQuery) params.search = searchQuery;
      const data = await getCards(params);
      setCards(data);
    } catch (err) {
      setError(true);
    } finally {
      setLoading(false);
    }
  }, [selectedSector, searchQuery]);

  useEffect(() => {
    fetchCards();
  }, [fetchCards]);

  useEffect(() => {
    getSectors().then(setSectors).catch(() => {});
  }, []);

  const handleCardClick = async (ticker: string) => {
    try {
      const detail = await getCard(ticker);
      setSelectedCard(detail);
    } catch {
      // ignore
    }
  };

  return (
    <div>
      {/* Hero */}
      <div className="text-center mb-14 pt-10 relative">
        {/* Subtle rising line background */}
        <svg
          className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[200px] opacity-[0.035]"
          viewBox="0 0 500 200"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M0 180 L100 140 L200 155 L300 80 L400 100 L500 20"
            stroke="#10B981"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="rising-line"
          />
        </svg>

        {/* Logo */}
        <div className="inline-block mb-5 relative z-10">
          <svg width={52} height={52} viewBox="0 0 32 32" fill="none">
            <path d="M4 24 L12 18 L18 20 L26 8" stroke="#10B981" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
            <path d="M22 8 L26 8 L26 12" stroke="#10B981" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </div>

        {/* Title */}
        <h1 className="text-white font-black text-3xl sm:text-5xl mb-3 tracking-tight leading-tight relative z-10">
          {lang === 'ko' ? (
            <>내 투자, <span className="text-emerald-500">영차</span>로 끌어올리다</>
          ) : (
            <>Lift Your Investment<br className="sm:hidden" /> with <span className="text-emerald-500">Youngcha</span></>
          )}
        </h1>

        <p className="text-slate-400 text-sm sm:text-base max-w-lg mx-auto font-medium relative z-10">
          {t('hero_subtitle')}
        </p>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3 mb-8">
        <div className="relative flex-1">
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
              <circle cx="10.5" cy="10.5" r="7.5" /><path d="M18 18 L22 22" />
            </svg>
          </span>
          <input
            type="text"
            placeholder={t('search_placeholder')}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-slate-800/60 border border-slate-700 rounded-xl pl-9 pr-4 py-2.5 text-white text-sm placeholder:text-slate-500 focus:outline-none focus:border-emerald-500/50 focus:bg-slate-800 transition-all"
          />
        </div>
        <select
          value={selectedSector}
          onChange={(e) => setSelectedSector(e.target.value)}
          className="bg-slate-800/60 border border-slate-700 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-emerald-500/50 transition-all"
        >
          <option value="">{t('all_sectors')}</option>
          {sectors.map((s) => (
            <option key={s} value={s}>{translateSector(s, lang)}</option>
          ))}
        </select>
      </div>

      {/* Card Detail Modal */}
      {selectedCard && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 modal-backdrop p-4"
          onClick={() => setSelectedCard(null)}
        >
          <div
            className="card-float"
            onClick={(e) => e.stopPropagation()}
          >
            <CardFlip card={selectedCard} />
          </div>
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="text-center py-24">
          <div className="inline-block loader-spin text-emerald-500">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
              <path d="M12 2 A10 10 0 0 1 22 12" />
            </svg>
          </div>
          <p className="text-slate-500 text-sm mt-4 font-medium">{t('loading_cards')}</p>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="text-center py-24">
          <p className="text-red-400 text-sm font-medium">{t('error_load_cards')}</p>
        </div>
      )}

      {/* Card Grid */}
      {!loading && !error && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {cards.map((card, index) => {
            const grade = card.grade as Grade;
            const color = GRADE_COLORS[grade] || GRADE_COLORS.D;
            const priceChange = card.daily_change_pct ?? 0;
            const isPositive = priceChange >= 0;
            const typeColor = SECTOR_TYPE_COLORS[card.sector] || 'bg-white/10 text-white/60 border-white/20';

            return (
              <div
                key={card.ticker}
                className="card-grid-item rounded-2xl cursor-pointer group transition-all hover:shadow-card-hover"
                style={{
                  animationDelay: `${index * 0.04}s`,
                  background: '#1E293B',
                  border: '1px solid rgba(51, 65, 85, 0.6)',
                }}
                onClick={() => handleCardClick(card.ticker)}
              >
                <div className="p-4 transition-all group-hover:scale-[1.01]">
                  <div className="flex items-start justify-between mb-3">
                    <div className="min-w-0 flex-1">
                      <h3 className="text-white font-semibold text-sm truncate leading-tight">
                        {card.company_name} <span className="text-slate-500">({card.ticker})</span>
                      </h3>
                      <div className="mt-1.5">
                        <span className={`type-pill ${typeColor}`}>
                          {translateSector(card.sector, lang)}
                        </span>
                      </div>
                    </div>
                    <GradeBadge grade={grade} size="sm" />
                  </div>

                  <div className="flex items-end justify-between">
                    <div>
                      <p className="text-slate-500 text-[9px] uppercase tracking-wider font-semibold">
                        {t('score_label')}
                      </p>
                      <p className="font-black text-2xl" style={{ color }}>
                        {card.total_score.toFixed(1)}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-slate-300 font-mono text-sm font-semibold">
                        ${card.current_price?.toFixed(2) ?? '—'}
                      </p>
                      <p className={`text-xs font-bold ${isPositive ? 'text-emerald-400 price-up' : 'text-red-400 price-down'}`}>
                        {isPositive ? '+' : ''}{priceChange.toFixed(2)}%
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {!loading && !error && cards.length === 0 && (
        <div className="text-center py-24">
          <p className="text-slate-500 text-sm">{t('empty_cards')}</p>
        </div>
      )}
    </div>
  );
}

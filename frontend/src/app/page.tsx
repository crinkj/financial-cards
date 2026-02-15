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
      <div className="text-center mb-10 pt-4">
        <div className="inline-block mb-3">
          <span className="text-5xl">⚡</span>
        </div>
        <h1 className="text-gradient-gold font-black text-4xl sm:text-5xl mb-3 tracking-tight">
          {t('hero_title')}
        </h1>
        <p className="text-white/40 text-sm max-w-md mx-auto">
          {t('hero_subtitle')}
        </p>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3 mb-8">
        <div className="relative flex-1">
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-white/30 text-sm">🔍</span>
          <input
            type="text"
            placeholder={t('search_placeholder')}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-white/5 border border-white/10 rounded-xl pl-9 pr-4 py-2.5 text-white text-sm placeholder:text-white/30 focus:outline-none focus:border-amber-500/50 focus:bg-white/[0.07] transition-all"
          />
        </div>
        <select
          value={selectedSector}
          onChange={(e) => setSelectedSector(e.target.value)}
          className="bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-amber-500/50 transition-all"
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
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 modal-backdrop p-4"
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
          <div className="inline-block text-4xl loader-game">⚡</div>
          <p className="text-white/40 text-sm mt-4 font-medium">{t('loading_cards')}</p>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="text-center py-24">
          <span className="text-3xl">💥</span>
          <p className="text-red-400 text-sm mt-3 font-medium">{t('error_load_cards')}</p>
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
            const glowClass = `glow-${grade.toLowerCase()}`;
            const typeColor = SECTOR_TYPE_COLORS[card.sector] || 'bg-white/10 text-white/60 border-white/20';

            return (
              <div
                key={card.ticker}
                className={`card-grid-item card-border-glow ${glowClass} relative rounded-2xl cursor-pointer group`}
                style={{ animationDelay: `${index * 0.05}s` }}
                onClick={() => handleCardClick(card.ticker)}
              >
                <div
                  className="relative z-10 rounded-2xl p-4 transition-all group-hover:scale-[1.02]"
                  style={{
                    background: `linear-gradient(145deg, ${color}0c 0%, #0f0f23 40%, #13132b 100%)`,
                  }}
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="min-w-0 flex-1">
                      <h3 className="text-white font-bold text-sm truncate leading-tight">
                        {card.company_name} <span className="text-white/35">({card.ticker})</span>
                      </h3>
                      <div className="mt-1">
                        <span className={`type-pill ${typeColor}`}>
                          {translateSector(card.sector, lang)}
                        </span>
                      </div>
                    </div>
                    <GradeBadge grade={grade} size="sm" />
                  </div>

                  <div className="flex items-end justify-between">
                    <div>
                      <p className="text-white/40 text-[9px] uppercase tracking-wider font-bold">
                        {t('score_label')}
                      </p>
                      <p className="font-black text-2xl" style={{ color }}>
                        {card.total_score.toFixed(1)}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-white/60 font-mono text-sm font-bold">
                        ${card.current_price?.toFixed(2) ?? '—'}
                      </p>
                      <p className={`text-xs font-black ${isPositive ? 'text-green-400 price-up' : 'text-red-400 price-down'}`}>
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
          <span className="text-3xl">🔮</span>
          <p className="text-white/40 text-sm mt-3">{t('empty_cards')}</p>
        </div>
      )}
    </div>
  );
}

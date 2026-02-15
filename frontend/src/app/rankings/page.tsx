'use client';

import { useEffect, useState } from 'react';
import { RankingEntry, SectorChampion as SectorChampionType } from '@/types/card';
import { getTop10, getSectorChampions } from '@/lib/api';
import DailyTop10 from '@/components/Rankings/DailyTop10';
import SectorChampions from '@/components/Rankings/SectorChampion';
import { useLanguage } from '@/lib/LanguageContext';

type Tab = 'top10' | 'sectors';

export default function RankingsPage() {
  const { t } = useLanguage();
  const [activeTab, setActiveTab] = useState<Tab>('top10');
  const [top10, setTop10] = useState<RankingEntry[]>([]);
  const [champions, setChampions] = useState<SectorChampionType[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    setLoading(true);
    setError(false);
    Promise.all([getTop10(), getSectorChampions()])
      .then(([t, c]) => {
        setTop10(t);
        setChampions(c);
      })
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <div className="text-center mb-8 pt-2">
        <span className="text-4xl">🏟️</span>
        <h1 className="text-gradient-gold font-black text-3xl mt-2">{t('rankings_title')}</h1>
        <p className="text-white/40 text-sm mt-1">{t('rankings_subtitle')}</p>
      </div>

      {/* Tabs */}
      <div className="flex justify-center gap-2 mb-8">
        {(['top10', 'sectors'] as Tab[]).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-5 py-2.5 rounded-xl text-sm font-bold transition-all ${
              activeTab === tab
                ? 'bg-gradient-to-r from-amber-500/20 to-orange-500/20 text-amber-400 border border-amber-500/30'
                : 'bg-white/5 text-white/40 hover:text-white/60 border border-transparent'
            }`}
          >
            {tab === 'top10' ? `🏆 ${t('daily_top_10')}` : `⚔️ ${t('sector_champions')}`}
          </button>
        ))}
      </div>

      {loading && (
        <div className="text-center py-24">
          <div className="inline-block text-4xl loader-game">⚡</div>
        </div>
      )}

      {error && (
        <div className="text-center py-24">
          <span className="text-3xl">💥</span>
          <p className="text-red-400 text-sm mt-3">{t('error_load_rankings')}</p>
        </div>
      )}

      {!loading && !error && (
        <>
          {activeTab === 'top10' && <DailyTop10 rankings={top10} />}
          {activeTab === 'sectors' && <SectorChampions champions={champions} />}
        </>
      )}
    </div>
  );
}

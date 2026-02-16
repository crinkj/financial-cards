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
      <div className="text-center mb-8 pt-6">
        <h1 className="text-white font-black text-3xl">{t('rankings_title')}</h1>
        <p className="text-slate-400 text-sm mt-1">{t('rankings_subtitle')}</p>
      </div>

      {/* Tabs */}
      <div className="flex justify-center gap-2 mb-8">
        {(['top10', 'sectors'] as Tab[]).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-5 py-2.5 rounded-xl text-sm font-semibold transition-all ${
              activeTab === tab
                ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                : 'bg-slate-800/60 text-slate-400 hover:text-slate-300 border border-slate-700'
            }`}
          >
            {tab === 'top10' ? t('daily_top_10') : t('sector_champions')}
          </button>
        ))}
      </div>

      {loading && (
        <div className="text-center py-24">
          <div className="inline-block loader-spin text-emerald-500">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
              <path d="M12 2 A10 10 0 0 1 22 12" />
            </svg>
          </div>
        </div>
      )}

      {error && (
        <div className="text-center py-24">
          <p className="text-red-400 text-sm">{t('error_load_rankings')}</p>
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

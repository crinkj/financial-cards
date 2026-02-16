'use client';

import { RankingEntry, Grade, GRADE_COLORS } from '@/types/card';
import GradeBadge from '@/components/GradeBadge';
import { useLanguage } from '@/lib/LanguageContext';
import { translateSector, SECTOR_TYPE_COLORS } from '@/lib/i18n';

interface DailyTop10Props {
  rankings: RankingEntry[];
}

function RankBadge({ rank }: { rank: number }) {
  if (rank === 1) {
    return (
      <div className="w-10 h-10 rounded-xl bg-emerald-500 flex items-center justify-center font-black text-lg text-white rank-shine">
        {rank}
      </div>
    );
  }
  if (rank === 2) {
    return (
      <div className="w-10 h-10 rounded-xl bg-slate-400 flex items-center justify-center font-black text-lg text-slate-900">
        {rank}
      </div>
    );
  }
  if (rank === 3) {
    return (
      <div className="w-10 h-10 rounded-xl bg-amber-600 flex items-center justify-center font-black text-lg text-white">
        {rank}
      </div>
    );
  }
  return (
    <div className="w-10 h-10 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center font-bold text-lg text-slate-400">
      {rank}
    </div>
  );
}

export default function DailyTop10({ rankings }: DailyTop10Props) {
  const { t, lang } = useLanguage();

  return (
    <div className="space-y-3 max-w-2xl mx-auto">
      {rankings.map((entry, index) => {
        const grade = entry.grade as Grade;
        const color = GRADE_COLORS[grade] || GRADE_COLORS.D;
        const typeColor = SECTOR_TYPE_COLORS[entry.sector] || 'bg-white/10 text-white/60 border-white/20';

        return (
          <div
            key={entry.ticker}
            className="card-grid-item flex items-center gap-4 rounded-xl px-4 py-3 transition-all hover:scale-[1.01]"
            style={{
              animationDelay: `${index * 0.05}s`,
              background: '#1E293B',
              border: '1px solid rgba(51, 65, 85, 0.6)',
            }}
          >
            <RankBadge rank={entry.rank} />
            <div className="flex-1 min-w-0">
              <p className="text-white font-semibold text-sm truncate">
                {entry.company_name} <span className="text-slate-500">({entry.ticker})</span>
              </p>
              <span className={`type-pill ${typeColor} mt-0.5 inline-block`}>
                {translateSector(entry.sector, lang)}
              </span>
            </div>
            <div className="text-right mr-2">
              <p className="font-black text-lg" style={{ color }}>
                {entry.total_score.toFixed(1)}
              </p>
            </div>
            <GradeBadge grade={grade} size="sm" />
          </div>
        );
      })}
    </div>
  );
}

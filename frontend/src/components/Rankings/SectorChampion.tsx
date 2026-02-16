'use client';

import { SectorChampion as SectorChampionType, Grade, GRADE_COLORS } from '@/types/card';
import GradeBadge from '@/components/GradeBadge';
import { useLanguage } from '@/lib/LanguageContext';
import { translateSector, SECTOR_TYPE_COLORS } from '@/lib/i18n';

interface SectorChampionsProps {
  champions: SectorChampionType[];
}

export default function SectorChampions({ champions }: SectorChampionsProps) {
  const { t, lang } = useLanguage();

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 max-w-3xl mx-auto">
      {champions.map((champ, index) => {
        const grade = champ.grade as Grade;
        const color = GRADE_COLORS[grade] || GRADE_COLORS.D;
        const typeColor = SECTOR_TYPE_COLORS[champ.sector] || 'bg-white/10 text-white/60 border-white/20';

        return (
          <div
            key={champ.sector}
            className="card-grid-item rounded-xl p-4 transition-all hover:scale-[1.01]"
            style={{
              animationDelay: `${index * 0.05}s`,
              background: '#1E293B',
              border: '1px solid rgba(51, 65, 85, 0.6)',
            }}
          >
            {/* Sector header */}
            <div className="flex items-center gap-2 mb-3">
              <span className={`type-pill ${typeColor}`}>
                {translateSector(champ.sector, lang)}
              </span>
              <div className="flex-1" />
              <span className="text-[10px] text-slate-600 font-semibold uppercase tracking-wider">Leader</span>
            </div>

            {/* Champion info */}
            <div className="flex items-center justify-between">
              <div className="min-w-0 flex-1">
                <p className="text-white font-semibold text-sm truncate">
                  {champ.company_name} <span className="text-slate-500">({champ.ticker})</span>
                </p>
              </div>
              <div className="flex items-center gap-3 ml-2">
                <span className="font-black text-lg" style={{ color }}>
                  {champ.total_score.toFixed(1)}
                </span>
                <GradeBadge grade={grade} size="sm" />
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}

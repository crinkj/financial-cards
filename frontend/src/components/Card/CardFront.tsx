import { CardDetail, Grade, GRADE_COLORS } from '@/types/card';
import GradeBadge from '@/components/GradeBadge';
import RadarChart from '@/components/RadarChart';
import { useLanguage } from '@/lib/LanguageContext';
import { translateSector, translateEmotionalTag, SECTOR_TYPE_COLORS } from '@/lib/i18n';

interface CardFrontProps {
  card: CardDetail;
}

export default function CardFront({ card }: CardFrontProps) {
  const { t, lang } = useLanguage();
  const grade = card.grade as Grade;
  const priceChange = card.daily_change_pct ?? 0;
  const isPositive = priceChange >= 0;
  const color = GRADE_COLORS[grade] || GRADE_COLORS.D;
  const glowClass = `glow-${grade.toLowerCase()}`;
  const isHolo = grade === 'S';
  const typeColor = SECTOR_TYPE_COLORS[card.sector] || 'bg-white/10 text-white/60 border-white/20';

  return (
    <div className={`relative w-full h-full rounded-2xl overflow-hidden card-border-glow ${glowClass} ${isHolo ? 'card-holo' : ''}`}>
      <div
        className="w-full h-full rounded-2xl p-5 flex flex-col relative z-10"
        style={{
          background: `linear-gradient(160deg, ${color}08 0%, #0F172A 30%, #1E293B 70%, ${color}05 100%)`,
        }}
      >
        {/* Header: Name + Grade */}
        <div className="flex items-start justify-between mb-1">
          <div className="flex-1 min-w-0">
            <h3 className="text-white font-bold text-base leading-tight truncate">
              {card.company_name} <span className="text-slate-500 font-semibold">({card.ticker})</span>
            </h3>
            <div className="mt-1">
              <span className={`type-pill ${typeColor}`}>
                {translateSector(card.sector, lang)}
              </span>
            </div>
          </div>
          <GradeBadge grade={grade} size="lg" pulse />
        </div>

        {/* Radar Chart */}
        <div className="flex-1 flex items-center justify-center my-1">
          <RadarChart scores={card.scores} grade={grade} size={190} />
        </div>

        {/* Score */}
        <div className="text-center mb-2">
          <span className="text-slate-500 text-[10px] uppercase tracking-widest font-semibold">
            {t('total_score')}
          </span>
          <p
            className="font-black text-3xl score-animate"
            style={{ color }}
          >
            {card.total_score.toFixed(1)}
          </p>
        </div>

        {/* Price Bar */}
        <div
          className="flex items-center justify-between text-sm rounded-lg px-3 py-1.5"
          style={{ backgroundColor: `${color}08`, border: `1px solid ${color}15` }}
        >
          <span className="text-slate-300 font-mono font-semibold">
            ${card.current_price?.toFixed(2) ?? '—'}
          </span>
          <span className={`font-bold ${isPositive ? 'text-emerald-400 price-up' : 'text-red-400 price-down'}`}>
            {isPositive ? '+' : ''}{priceChange.toFixed(2)}%
          </span>
        </div>

        {/* Emotional Tag */}
        {card.emotional_tag && (
          <p className="text-center text-xs mt-2 font-semibold" style={{ color: `${color}88` }}>
            {translateEmotionalTag(card.emotional_tag, lang)}
          </p>
        )}
      </div>
    </div>
  );
}

import { CardDetail, Grade, GRADE_COLORS } from '@/types/card';
import { useLanguage } from '@/lib/LanguageContext';

interface CardBackProps {
  card: CardDetail;
}

function formatMetric(value: number | null | undefined, type: 'pct' | 'ratio' | 'dollar' | 'number' = 'number'): string {
  if (value === null || value === undefined) return '—';
  switch (type) {
    case 'pct':
      return `${(value * 100).toFixed(1)}%`;
    case 'ratio':
      return value.toFixed(2);
    case 'dollar':
      if (Math.abs(value) >= 1e9) return `$${(value / 1e9).toFixed(1)}B`;
      if (Math.abs(value) >= 1e6) return `$${(value / 1e6).toFixed(1)}M`;
      return `$${value.toFixed(0)}`;
    default:
      return value.toFixed(2);
  }
}

function MetricRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between py-1 border-b border-white/5">
      <span className="text-white/40 text-[11px]">{label}</span>
      <span className="text-white font-mono text-[11px] font-bold">{value}</span>
    </div>
  );
}

function SectionLabel({ label, color }: { label: string; color: string }) {
  return (
    <div className="flex items-center gap-2 mt-2.5 mb-1">
      <div className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: color }} />
      <p className="text-[10px] uppercase tracking-wider font-bold" style={{ color: `${color}cc` }}>
        {label}
      </p>
    </div>
  );
}

export default function CardBack({ card }: CardBackProps) {
  const { t } = useLanguage();
  const m = card.raw_metrics;
  const grade = card.grade as Grade;
  const color = GRADE_COLORS[grade] || GRADE_COLORS.D;
  const glowClass = `glow-${grade.toLowerCase()}`;

  return (
    <div className={`relative w-full h-full rounded-2xl overflow-hidden card-border-glow ${glowClass}`}>
      <div
        className="w-full h-full rounded-2xl p-5 flex flex-col relative z-10"
        style={{
          background: `linear-gradient(160deg, ${color}08 0%, #0f0f23 20%, #12122a 100%)`,
        }}
      >
        {/* Header */}
        <div className="flex items-center justify-between mb-2 pb-2 border-b border-white/10">
          <div className="min-w-0 flex-1">
            <h3 className="text-white font-black text-sm truncate">
              {card.company_name} <span className="text-white/40">({card.ticker})</span>
            </h3>
          </div>
          <div
            className="text-xs font-black px-2.5 py-1 rounded-lg ml-2 shrink-0"
            style={{ color, backgroundColor: `${color}18`, border: `1px solid ${color}33` }}
          >
            {t('back_score')} {card.total_score.toFixed(1)}
          </div>
        </div>

        {/* Key Financials */}
        <div className="flex-1 overflow-y-auto pr-1">
          <SectionLabel label={t('back_growth')} color="#f59e0b" />
          <MetricRow label={t('back_revenue_growth')} value={formatMetric(m.revenue_growth, 'pct')} />
          <MetricRow label={t('back_earnings_growth')} value={formatMetric(m.earnings_growth, 'pct')} />

          <SectionLabel label={t('back_stability')} color="#3b82f6" />
          <MetricRow label={t('back_debt_equity')} value={formatMetric(m.debt_to_equity, 'ratio')} />
          <MetricRow label={t('back_current_ratio')} value={formatMetric(m.current_ratio, 'ratio')} />

          <SectionLabel label={t('back_cashflow')} color="#22c55e" />
          <MetricRow label={t('back_fcf')} value={formatMetric(m.free_cashflow, 'dollar')} />
          <MetricRow label={t('back_ocf')} value={formatMetric(m.operating_cashflow, 'dollar')} />

          <SectionLabel label={t('back_efficiency')} color="#a855f7" />
          <MetricRow label={t('back_roe')} value={formatMetric(m.return_on_equity, 'pct')} />
          <MetricRow label={t('back_roa')} value={formatMetric(m.return_on_assets, 'pct')} />
          <MetricRow label={t('back_op_margin')} value={formatMetric(m.operating_margins, 'pct')} />
          <MetricRow label={t('back_profit_margin')} value={formatMetric(m.profit_margins, 'pct')} />

          <SectionLabel label={t('back_valuation')} color="#06b6d4" />
          <MetricRow label={t('back_trailing_pe')} value={formatMetric(m.trailing_pe, 'ratio')} />
          <MetricRow label={t('back_forward_pe')} value={formatMetric(m.forward_pe, 'ratio')} />
          <MetricRow label={t('back_trailing_eps')} value={formatMetric(m.trailing_eps, 'ratio')} />
          <MetricRow label={t('back_dividend_yield')} value={formatMetric(m.dividend_yield, 'pct')} />
        </div>

        {/* Footer */}
        <p className="text-center text-white/20 text-[10px] mt-2 font-medium">
          {t('back_tap_flip')}
        </p>
      </div>
    </div>
  );
}

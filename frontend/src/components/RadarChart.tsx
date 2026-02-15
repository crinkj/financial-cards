'use client';

import { Radar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
} from 'chart.js';
import { AbilityScores, Grade, GRADE_COLORS } from '@/types/card';
import { useLanguage } from '@/lib/LanguageContext';

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip);

interface RadarChartProps {
  scores: AbilityScores;
  grade: Grade;
  size?: number;
}

export default function RadarChart({ scores, grade, size = 220 }: RadarChartProps) {
  const { t } = useLanguage();
  const color = GRADE_COLORS[grade] || GRADE_COLORS.D;

  const labels = [
    `${t('radar_growth')}\n${t('radar_sub_growth')}`,
    `${t('radar_stability')}\n${t('radar_sub_stability')}`,
    `${t('radar_cashflow')}\n${t('radar_sub_cashflow')}`,
    `${t('radar_efficiency')}\n${t('radar_sub_efficiency')}`,
    `${t('radar_momentum')}\n${t('radar_sub_momentum')}`,
    `${t('radar_earnings')}\n${t('radar_sub_earnings')}`,
  ];

  const data = {
    labels,
    datasets: [
      {
        data: [
          scores.growth,
          scores.stability,
          scores.cashflow,
          scores.efficiency,
          scores.momentum,
          scores.earnings,
        ],
        backgroundColor: `${color}33`,
        borderColor: color,
        borderWidth: 2,
        pointBackgroundColor: color,
        pointBorderColor: '#fff',
        pointBorderWidth: 1,
        pointRadius: 3,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: (context: any) => `${context.parsed.r.toFixed(1)}`,
        },
      },
    },
    scales: {
      r: {
        min: 0,
        max: 100,
        ticks: {
          stepSize: 25,
          display: false,
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
        angleLines: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
        pointLabels: {
          color: 'rgba(255, 255, 255, 0.7)',
          font: { size: 10 },
        },
      },
    },
  };

  return (
    <div style={{ width: size, height: size, margin: '0 auto' }}>
      <Radar data={data} options={options} />
    </div>
  );
}

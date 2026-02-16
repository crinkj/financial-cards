import { Grade, GRADE_COLORS } from '@/types/card';

interface GradeBadgeProps {
  grade: Grade;
  size?: 'sm' | 'md' | 'lg';
  pulse?: boolean;
}

const SIZE_CLASSES = {
  sm: 'w-8 h-8 text-xs',
  md: 'w-12 h-12 text-lg',
  lg: 'w-16 h-16 text-2xl',
};

export default function GradeBadge({ grade, size = 'md', pulse = false }: GradeBadgeProps) {
  const color = GRADE_COLORS[grade] || GRADE_COLORS.D;
  const isTop = grade === 'S' || grade === 'A';

  return (
    <div
      className={`${SIZE_CLASSES[size]} rounded-lg flex items-center justify-center font-black border ${
        pulse && isTop ? 'badge-pulse' : ''
      }`}
      style={{
        borderColor: `${color}50`,
        color: color,
        backgroundColor: `${color}10`,
        boxShadow: isTop ? `0 0 12px ${color}33` : 'none',
        '--badge-color': `${color}66`,
      } as React.CSSProperties}
    >
      {grade}
    </div>
  );
}

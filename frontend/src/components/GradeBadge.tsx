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
      className={`${SIZE_CLASSES[size]} rounded-lg flex items-center justify-center font-black border-2 ${
        pulse && isTop ? 'badge-pulse' : ''
      }`}
      style={{
        borderColor: color,
        color: color,
        backgroundColor: `${color}18`,
        boxShadow: isTop ? `0 0 16px ${color}66, inset 0 0 8px ${color}22` : `0 0 8px ${color}33`,
        '--badge-color': `${color}88`,
      } as React.CSSProperties}
    >
      {grade}
    </div>
  );
}

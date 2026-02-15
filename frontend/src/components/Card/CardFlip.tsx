'use client';

import { useState } from 'react';
import { CardDetail } from '@/types/card';
import CardFront from './CardFront';
import CardBack from './CardBack';

interface CardFlipProps {
  card: CardDetail;
}

export default function CardFlip({ card }: CardFlipProps) {
  const [isFlipped, setIsFlipped] = useState(false);

  return (
    <div
      className="w-[320px] h-[480px] cursor-pointer"
      style={{ perspective: '1000px' }}
      onClick={() => setIsFlipped(!isFlipped)}
    >
      <div
        className="relative w-full h-full transition-transform duration-500"
        style={{
          transformStyle: 'preserve-3d',
          transform: isFlipped ? 'rotateY(180deg)' : 'rotateY(0deg)',
        }}
      >
        {/* Front */}
        <div
          className="absolute inset-0"
          style={{ backfaceVisibility: 'hidden' }}
        >
          <CardFront card={card} />
        </div>

        {/* Back */}
        <div
          className="absolute inset-0"
          style={{
            backfaceVisibility: 'hidden',
            transform: 'rotateY(180deg)',
          }}
        >
          <CardBack card={card} />
        </div>
      </div>
    </div>
  );
}

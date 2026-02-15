'use client';

import Link from 'next/link';
import { useLanguage, LanguageToggle } from '@/lib/LanguageContext';

export default function NavBar() {
  const { t } = useLanguage();

  return (
    <nav className="sticky top-0 z-50 bg-black/60 backdrop-blur-xl border-b border-white/5">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2 group">
          <span className="text-2xl group-hover:scale-110 transition-transform">⚡</span>
          <span className="text-gradient-gold font-black text-xl tracking-tight">
            {t('app_title')}
          </span>
        </Link>
        <div className="flex items-center gap-1">
          <Link
            href="/"
            className="px-3 py-1.5 rounded-lg text-white/60 hover:text-white hover:bg-white/10 text-sm font-bold transition-all"
          >
            {t('nav_cards')}
          </Link>
          <Link
            href="/rankings"
            className="px-3 py-1.5 rounded-lg text-white/60 hover:text-white hover:bg-white/10 text-sm font-bold transition-all"
          >
            {t('nav_rankings')}
          </Link>
          <div className="ml-2">
            <LanguageToggle />
          </div>
        </div>
      </div>
    </nav>
  );
}

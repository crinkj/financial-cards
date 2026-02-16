'use client';

import Link from 'next/link';
import { useLanguage, LanguageToggle } from '@/lib/LanguageContext';

function LogoIcon({ size = 24 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path
        d="M4 24 L12 18 L18 20 L26 8"
        stroke="#10B981"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M22 8 L26 8 L26 12"
        stroke="#10B981"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export default function NavBar() {
  const { t } = useLanguage();

  return (
    <nav className="sticky top-0 z-50 bg-[#0F172A]/80 backdrop-blur-xl border-b border-slate-800">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2 group">
          <div className="group-hover:scale-110 transition-transform">
            <LogoIcon size={28} />
          </div>
          <span className="text-emerald-500 font-black text-xl tracking-tight">
            {t('app_title')}
          </span>
        </Link>
        <div className="flex items-center gap-1">
          <Link
            href="/"
            className="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 text-sm font-medium transition-all"
          >
            {t('nav_cards')}
          </Link>
          <Link
            href="/rankings"
            className="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 text-sm font-medium transition-all"
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

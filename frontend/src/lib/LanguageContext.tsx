'use client';

import { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react';
import { Lang, translations, TranslationKey } from './i18n';

interface LanguageContextValue {
  lang: Lang;
  setLang: (lang: Lang) => void;
  t: (key: TranslationKey) => string;
}

const LanguageContext = createContext<LanguageContextValue | null>(null);

const STORAGE_KEY = 'financial-cards-lang';

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>('en');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY) as Lang | null;
    if (saved === 'ko' || saved === 'en') {
      setLangState(saved);
    }
    setMounted(true);
  }, []);

  const setLang = useCallback((newLang: Lang) => {
    setLangState(newLang);
    localStorage.setItem(STORAGE_KEY, newLang);
  }, []);

  const t = useCallback(
    (key: TranslationKey): string => {
      return translations[key]?.[lang] ?? key;
    },
    [lang]
  );

  // Prevent hydration mismatch by rendering children only after mount
  if (!mounted) {
    return <>{children}</>;
  }

  return (
    <LanguageContext.Provider value={{ lang, setLang, t }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage(): LanguageContextValue {
  const ctx = useContext(LanguageContext);
  if (!ctx) {
    // Fallback for SSR / before mount
    return {
      lang: 'en',
      setLang: () => {},
      t: (key: TranslationKey) => translations[key]?.en ?? key,
    };
  }
  return ctx;
}

export function LanguageToggle() {
  const { lang, setLang } = useLanguage();

  return (
    <button
      onClick={() => setLang(lang === 'en' ? 'ko' : 'en')}
      className="px-2 py-1 rounded-md bg-white/10 hover:bg-white/20 text-white text-xs font-medium transition-colors"
      title={lang === 'en' ? 'Switch to Korean' : 'Switch to English'}
    >
      {lang === 'en' ? '한국어' : 'EN'}
    </button>
  );
}

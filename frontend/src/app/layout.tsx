import type { Metadata } from 'next';
import './globals.css';
import NavBar from '@/components/NavBar';
import { LanguageProvider } from '@/lib/LanguageContext';

export const metadata: Metadata = {
  title: '영차 | Youngcha',
  description: '내 투자, 영차로 끌어올리다. 위험은 낮추고, 방향은 올리고.',
  manifest: '/manifest.json',
  themeColor: '#10B981',
  viewport: 'width=device-width, initial-scale=1, maximum-scale=1',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="antialiased">
        <LanguageProvider>
          <NavBar />
          <main className="max-w-6xl mx-auto px-4 py-6">
            {children}
          </main>
        </LanguageProvider>
      </body>
    </html>
  );
}

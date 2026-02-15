import type { Metadata } from 'next';
import './globals.css';
import NavBar from '@/components/NavBar';
import { LanguageProvider } from '@/lib/LanguageContext';

export const metadata: Metadata = {
  title: 'Stockmon',
  description: 'Real stocks. Battle stats. Collect the market.',
  manifest: '/manifest.json',
  themeColor: '#ffd700',
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

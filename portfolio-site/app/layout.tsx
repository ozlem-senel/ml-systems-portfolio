import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Header from '@/components/Header'
import Footer from '@/components/Footer'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Özlem Senel - ML Engineer & Data Scientist',
  description: 'Portfolio showcasing production ML systems, data engineering pipelines, and end-to-end machine learning projects for gaming analytics.',
  keywords: ['machine learning', 'data science', 'ML engineer', 'data engineering', 'gaming analytics', 'PyTorch', 'Python'],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Header />
        <main className="min-h-screen">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  )
}

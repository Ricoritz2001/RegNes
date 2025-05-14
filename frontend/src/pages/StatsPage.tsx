// src/pages/StatsPage.tsx
import React from 'react'
import { useStatus } from '../hooks/useStatus'

export default function StatsPage() {
  const { data: status, loading, error } = useStatus()

  // loading / error states
  if (loading) {
    return (
      <section className="min-h-screen bg-gradient-to-r from-cyan-700 via-cyan-500 to-blue-400 flex items-center justify-center">
        <p className="text-white text-2xl">Loading dashboard stats…</p>
      </section>
    )
  }
  if (error) {
    return (
      <section className="min-h-screen bg-gradient-to-r from-cyan-700 via-cyan-500 to-blue-400 flex items-center justify-center">
        <p className="text-red-300 text-2xl">Error: {error}</p>
      </section>
    )
  }
  if (!status) {
    return (
      <section className="min-h-screen bg-gradient-to-r from-cyan-700 via-cyan-500 to-blue-400 flex items-center justify-center">
        <p className="text-white text-2xl">No data available</p>
      </section>
    )
  }

  // build the array with real values
  const statsItems = [
    { title: 'Last Update',           value: status.last_update ?? '—' },
    { title: 'Total News',            value: status.total_news.toLocaleString() },
    { title: 'Current Channels',      value: status.channels_count },
    { title: 'Current Sources',       value: status.sources_count },
    { title: 'News Today',            value: status.news_today },
    {
      title: 'Mean Sentiment Today',
      value:
        status.sentiment_today != null
          ? status.sentiment_today.toFixed(3)
          : '—',
    },
  ]

  return (
    <section className="min-h-screen bg-gradient-to-r from-cyan-700 via-cyan-500 to-blue-400 flex items-center">
      <div className="container mx-auto px-4 py-16">
        <h1 className="text-6xl font-bold text-white text-center mb-12">
          <span className="bg-gradient-to-r from-cyan-400 via-purple-500 to-pink-500 bg-clip-text text-transparent">
            RegNeS
          </span>
          -DB dashboard
        </h1>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          {statsItems.map(({ title, value }) => (
            <div
              key={title}
              className="bg-white p-6 rounded-lg shadow-md flex flex-col items-center"
            >
              <h2 className="text-xl font-semibold mb-2 text-gray-800">
                {title}
              </h2>
              <p className="text-4xl font-bold text-cyan-700">{value}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

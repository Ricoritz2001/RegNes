import { useState, useEffect } from 'react'
import { ChartDataset } from 'chart.js'
import { getGlobalTrends } from '../services/api'

export function useGlobalSentiment(countries: string[]) {
  const [labels, setLabels]     = useState<string[]>([])
  const [datasets, setDatasets] = useState<ChartDataset<'line'>[]>([])

  useEffect(() => {
    if (!countries.length) {
      setLabels([])
      setDatasets([])
      return
    }

    (async () => {
      const raw = await getGlobalTrends(countries, 'sentiment')
      const dates = Array.from(new Set(raw.map(r => r.date))).sort()
      setLabels(dates)

      const map: Record<string, (number|null)[]> = {}
      countries.forEach((c) => {
        map[c] = dates.map(date => {
          const rec = raw.find(r => r.date === date && r.country === c)
          return rec ? rec.sentiment : null
        })
      })

      const COLORS = [
        '#3366CC','#DC3912','#FF9900',
        '#109618','#990099','#0099C6'
      ]
      const ds: ChartDataset<'line'>[] = countries.map((c, i) => ({
        label:       c,
        data:        map[c],
        fill:        false,
        tension:     0.4,
        borderColor: COLORS[i % COLORS.length],
      }))

      setDatasets(ds)
    })()
  }, [countries])

  return { labels, datasets }
}

// src/hooks/useTrends.ts
import { useState, useEffect } from 'react'
import { ChartDataset } from 'chart.js'
import { getGlobalTrends, getRegionalTrends } from '../services/api'

export type Indicator = 'sentiment' | 'happiness' | 'valenz'

export function useTrends({
  indicator,
  countries,    // for global
  regions       // for regional
}: {
  indicator: Indicator
  countries?: string[]
  regions?: number[]
}): {
  labels: string[]
  datasets: ChartDataset<'line'>[]
} {
  const [labels, setLabels]     = useState<string[]>([])
  const [datasets, setDatasets] = useState<ChartDataset<'line'>[]>([])

  useEffect(() => {
    const fetchData = async () => {
      // GLOBAL
      if (countries && countries.length) {
        const raw = await getGlobalTrends(countries, indicator)
        console.log('🌐 raw global data:', raw)
        const dates = Array.from(new Set(raw.map(r => r.date))).sort()
        setLabels(dates)

        const map: Record<string, (number|null)[]> = {}
        countries.forEach(c => {
          map[c] = dates.map(d => {
            const rec = raw.find(x => x.date === d && x.country === c)
            return rec ? (rec[indicator] as number) : null
          })
        })

        const COLORS = ['#3366CC','#DC3912','#FF9900','#109618','#990099','#0099C6']
        setDatasets(
          countries.map((c,i) => ({
            label:       c,
            data:        map[c],
            fill:        false,
            tension:     0.4,
            borderColor: COLORS[i % COLORS.length],
          }))
        )
      }

      // REGIONAL (unchanged)
      else if (regions && regions.length) {
        const raw = await getRegionalTrends(regions)
        const dates = Array.from(new Set(raw.map(r => r.date))).sort()
        console.log('📅 pivoted dates:', dates)
        setLabels(dates)

        const map: Record<number, (number|null)[]> = {}
        regions.forEach(id => {
          map[id] = dates.map(d => {
            const rec = raw.find(x => x.date === d && x.region_id === id)
            if (!rec) return null;
          
            if (indicator === 'sentiment') return rec.rauh;
            return rec[indicator];
          });
          
        })

        const COLORS = ['#3366CC','#DC3912','#FF9900','#109618','#990099','#0099C6']
        setDatasets(
          regions.map((id,i) => ({
            label:       String(id),
            data:        map[id],
            fill:        false,
            tension:     0.4,
            borderColor: COLORS[i % COLORS.length],
          }))
        )
      }

      else {
        setLabels([])
        setDatasets([])
      }
    }

    fetchData()
  }, [indicator, countries?.join(','), regions?.join(',')])

  return { labels, datasets }
}

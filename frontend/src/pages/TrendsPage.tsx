// src/pages/TrendsPage.tsx
import React, { useState, useEffect } from 'react'
import { Card, Select } from 'antd'
import { useTrends, Indicator } from '../hooks/useTrends'
import { getRegions, Region } from '../services/api'
import { TrendChart } from '../components/TrendChart'

type Country = 'Deutschland' | 'Schweiz' | 'Österreich'
const ALL_COUNTRIES: Country[] = ['Deutschland', 'Schweiz', 'Österreich']

const METRIC_OPTIONS: { label: string; value: Indicator }[] = [
  { label: 'Sentiment', value: 'sentiment' },
  { label: 'Happiness', value: 'happiness' },
  { label: 'Valenz', value: 'valenz' },
]

const countryOptions = ALL_COUNTRIES.map((c) => ({
  label: c,
  value: c as Country,
}))

export const TrendsPage: React.FC = () => {
  // Global chart state
  const [visibleCountries, setVisibleCountries] = useState<Country[]>(ALL_COUNTRIES)
  const { labels: gLabels, datasets: gDatasets } = useTrends({
    indicator: 'sentiment',
    countries: visibleCountries,
    regions: undefined,
  })

  // Regional chart state
  const [regions, setRegions] = useState<Region[]>([])
  const [selectedRegion, setSelectedRegion] = useState<number | undefined>()
  const [regionMetric, setRegionMetric] = useState<Indicator>('sentiment')
  const { labels: rLabels, datasets: rDatasets } = useTrends({
    indicator: regionMetric,
    countries: undefined,
    regions: selectedRegion ? [selectedRegion] : [],
  })

  useEffect(() => {
    getRegions().then(setRegions)
  }, [])

  return (
    <div className="pt-20 px-8">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Global Sentiment */}
        <Card title="Global Sentiment" className="shadow-lg">
          <div className="mb-4">
            <Select
              mode="multiple"
              allowClear
              options={countryOptions}
              value={visibleCountries}
              onChange={(vals: Country[]) => setVisibleCountries(vals)}
              style={{ width: '100%' }}
            />
          </div>
          <div className="h-64 bg-gray-50 p-4 rounded">
            <TrendChart
              labels={gLabels}
              datasets={gDatasets}
              height={240}
            />
          </div>
        </Card>

        {/* Regional Trends */}
        <Card title="Regional Trends" className="shadow-lg">
          <div className="mb-4 flex flex-col md:flex-row gap-4">
            <Select<Indicator>
              options={METRIC_OPTIONS}
              value={regionMetric}
              onChange={setRegionMetric}
              style={{ width: '100%', maxWidth: 240 }}
            />
            <Select<number>
              options={regions.map((r) => ({
                label: r.region_name,
                value: r.region_id,
              }))}
              value={selectedRegion}
              onChange={(val) => setSelectedRegion(val)}
              placeholder="Select region"
              style={{ width: '100%', maxWidth: 240 }}
            />
          </div>
          <div className="h-64 bg-gray-50 p-4 rounded">
            <TrendChart
              labels={rLabels}
              datasets={rDatasets}
              height={240}
            />
          </div>
        </Card>
      </div>
    </div>
  )
}

// src/services/api.ts
import axios from 'axios'

//
// — Supported metrics —
//
export type Indicator = 'sentiment' | 'happiness' | 'valenz'

//
// — Axios instance —
//
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

//
// — Status endpoint —
//
export interface StatusResponse {
  last_update:     string | null
  total_news:      number
  channels_count:  number
  sources_count:   number
  news_today:      number
  sentiment_today: number | null
}
export function getStatus(): Promise<StatusResponse> {
  return api.get<StatusResponse>('/status').then(r => r.data)
}

//
// — Regions list —
//
export interface Region {
  region_id:   number
  region_name: string
}
export function getRegions(): Promise<Region[]> {
  // Updated to hit the /trends/regions endpoint
  return api.get<Region[]>('/trends/regions').then(r => r.data)
}

//
// — Global trends —
//
export interface GlobalTrend {
  date:      string   
  country:   string
  sentiment: number
  happiness: number
  valenz:    number

  // allow dynamic indexing by metric name
  [key: string]: string | number
}
/**
 * Fetch full time series for given countries & metric.
 */
export function getGlobalTrends(
  countries: string[],
  metric: Indicator
): Promise<GlobalTrend[]> {
  const qsCountries = encodeURIComponent(countries.join(','))
  return api
    .get<GlobalTrend[]>(
      `/trends/global?countries=${qsCountries}&metric=${metric}`
    )
    .then(r => r.data)
}

//
// — Regional trends —
//
export interface RegionalTrend {
  date:        string   
  region_id:   number
  region_name: string
  rauh:        number
  happiness:   number
  valenz:      number

  // allow dynamic indexing by metric name
  [key: string]: string | number
}
export function getRegionalTrends(
  regions: number[]
): Promise<RegionalTrend[]> {
  const qsRegions = encodeURIComponent(regions.join(','))
  return api
    .get<RegionalTrend[]>(`/trends/regional?regions=${qsRegions}`)
    .then(r => r.data)
}

export async function fetchRegionsWithSentiment(metric: string): Promise<{
  features: GeoJSON.Feature[];
  date: string;
}> {
  const res = await fetch(`/api/map/heat?metric=${metric}`);
  if (!res.ok) {
    throw new Error(`Failed to load regions GeoJSON (${res.status})`);
  }

  const data = await res.json();
  return {
    features: data.features,
    date: data.date
  };
}


// src/components/TrendChart.tsx
import React from 'react'
import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import type { ChartDataset } from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

interface TrendChartProps {
  labels:   string[]
  datasets: ChartDataset<'line'>[]
  title?:   string
  height?:  number  // optional pixel height
}

export const TrendChart: React.FC<TrendChartProps> = ({
  labels,
  datasets,
  title,
  height = 300    // default height
}) => {
  const data = { labels, datasets }
  const options = {
    responsive:      true,
    maintainAspectRatio: false as const,  // allow fixed height
    plugins: {
      legend: { position: 'top' as const },
      title:  { display: !!title, text: title }
    },
    scales: {
      x: { title: { display: true, text: 'Date' } },
      y: { title: { display: true, text: 'Value' } }
    }
  }

  return <Line data={data} options={options} height={height} />
}

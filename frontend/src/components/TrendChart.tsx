import React from 'react'
import { Chart } from 'react-chartjs-2'
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
  height?:  number
}

export const TrendChart: React.FC<TrendChartProps> = ({
  labels,
  datasets,
  title,
  height = 300
}) => {
  const data = { labels, datasets }

  const options = {
    responsive: true,
    maintainAspectRatio: false as const,
    plugins: {
      legend: { position: 'top' as const },
      title: { display: !!title, text: title }
    },
    scales: {
      x: { title: { display: true, text: 'Date' } },
      y: { title: { display: true, text: 'Value' } }
    }
  }

  return <Chart type="line" data={data} options={options} height={height} />
}

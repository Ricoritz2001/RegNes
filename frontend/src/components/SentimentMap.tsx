import { useState, useEffect } from 'react';
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import { fetchRegionsWithSentiment } from '../services/api';
import * as d3 from 'd3';
import 'leaflet/dist/leaflet.css'; 

const METRIC_OPTIONS = [
  { label: 'Sentiment', value: 'sentiment_mean' },
  { label: 'Happiness', value: 'happiness_mean' },
  { label: 'Valenz', value: 'valenz_mean' }
];

export default function SentimentMap() {
  const [geoData, setGeoData] = useState<GeoJSON.Feature[]>([]);
  const [mapDate, setMapDate] = useState<string>('');
  const [selectedMetric, setSelectedMetric] = useState<string>('sentiment_mean');

  useEffect(() => {
    fetchRegionsWithSentiment(selectedMetric)
      .then(({ features, date }) => {
        setGeoData(features);
        setMapDate(date);
        console.log(`[Map] Loaded ${features.length} features for ${selectedMetric}`);
        console.log("Sample feature:", features[0]?.properties);
      })
      .catch(console.error);
  }, [selectedMetric]);

  const colorScale = d3.scaleSequential(d3.interpolateRdYlBu).domain([1, 0]);

  const styleRegion = (feature: any) => {
    const val = feature.properties.value ?? 0;
    return {
      fillColor: colorScale(val),
      color: '#333',
      weight: 1,
      fillOpacity: 0.8
    };
  };

  return (
    <div className="space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between text-sm text-gray-600 space-y-1 sm:space-y-0">
        <div>
          Showing data for: <strong>{mapDate}</strong>
        </div>
        <div className="text-gray-500">
          Map tiles &copy; <a
            href="https://www.openstreetmap.org/copyright"
            target="_blank"
            rel="noopener noreferrer"
            className="underline"
          >
            OpenStreetMap
          </a> contributors
        </div>
        <select
          className="border px-3 py-1 rounded sm:ml-4"
          value={selectedMetric}
          onChange={(e) => setSelectedMetric(e.target.value)}
        >
          {METRIC_OPTIONS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </div>

      {/* Map */}
      <div className="w-full h-[800px] bg-gray-200 rounded-lg shadow-lg overflow-hidden">
        <MapContainer
          center={[51, 10]}
          zoom={6}
          scrollWheelZoom={true}
          style={{ width: '100%', height: '100%' }}
          attributionControl={false} 
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {geoData.length > 0 && (
            <GeoJSON
              key={selectedMetric}
              data={{
                type: 'FeatureCollection',
                features: geoData
              } as GeoJSON.FeatureCollection}
              style={styleRegion}
              onEachFeature={(feature, layer) => {
                const val = feature.properties.value ?? 0;
                const name = feature.properties.NAME || 'Unknown';
                layer.bindTooltip(
                  `Region: ${name}<br/>Value: ${val.toFixed(2)}`,
                  { sticky: true }
                );
              }}
            />
          )}
        </MapContainer>
      </div>
    </div>
  );
}

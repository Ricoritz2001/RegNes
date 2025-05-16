import SentimentMap from '../components/SentimentMap';

export default function HeatmapPage() {
  return (
    <div className="flex justify-center mt-32 px-4">
      
      <div className="relative w-full max-w-6xl h-[800px] bg-gray-200 rounded-lg shadow-lg overflow-hidden">
        <SentimentMap />
      </div>
    </div>
  );
}

// src/App.tsx
import './App.css';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import AboutPage from './pages/AboutPage';
import StatsPage from './pages/StatsPage';
import { TrendsPage } from './pages/TrendsPage';
import HeatmapPage from './pages/HeatmapPage';

function App() {
  return (
    <BrowserRouter>
      
      <Navbar />

      <Routes>
        {/* Redirect “/” to “/info” */}
        <Route path="/" element={<Navigate to="/info" replace />} />

        {/* Mount AboutPage at /info */}
        <Route path="info" element={<AboutPage />} />

        <Route path="stats" element={<StatsPage />} />

        <Route path="/charts" element={<TrendsPage />} />

        <Route path="/Heatmap" element={<HeatmapPage />} />
        
        {/* Fallback for any unknown path */}
        <Route path="*" element={<Navigate to="/info" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

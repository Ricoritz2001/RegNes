import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';

export default function Layout() {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />

      <main className="flex-1 container mx-auto px-4 py-6">
        <Outlet /> 
      </main>

      <footer className="bg-gray-100 text-center text-sm text-gray-600 py-4 mt-10">
        Powered by Ricardo
      </footer>
    </div>
  );
}

import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';

export default function Navbar() {
  const [activeLink, setActiveLink] = useState('/info');

  const navLinks = [
    { to: '/info',   label: 'About'  },
    { to: '/heatmap',  label: 'Heatmap'},
    { to: '/stats',  label: 'Stats'  },
    { to: '/charts', label: 'Charts' },
  ];

  return (
    <nav className="fixed top-0 left-0 right-0 bg-white/90 backdrop-blur-sm z-50 border-b border-gray-100 shadow-sm">
      <div className="container mx-auto flex items-center justify-between px-4 sm:px-6 lg:px-8 h-16">
        {/* Logo */}
        <div className="flex items-center gap-1 cursor-pointer">
          <div className="w-4 h-4 bg-blue-600 rounded-full" />
          <div className="w-4 h-4 bg-red-600 rounded-full" />
        </div>

        {/* Nav items */}
        <div className="hidden md:flex items-center gap-10">
          {navLinks.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              end
              onClick={() => setActiveLink(link.to)}
              className={({ isActive }) =>
                [
                  'relative text-sm font-medium transition',
                  isActive
                    ? 'text-blue-600 after:w-full'
                    : 'text-gray-600 hover:text-gray-900',
                  'after:absolute after:bottom-0 after:left-0 after:h-0.5 after:w-0 after:bg-blue-600 after:transition-all'
                ].join(' ')
              }
            >
              {link.label}
            </NavLink>
          ))}
        </div>
      </div>
    </nav>
  );
}

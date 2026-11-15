import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, Map, Calendar, Settings as SettingsIcon } from 'lucide-react';
import { useApp } from '../context/AppContext';

export default function MobileNav() {
  const location = useLocation();
  const { dueReviews } = useApp();

  const isHome = location.pathname === '/';
  const isRoadmap = location.pathname.startsWith('/roadmap');
  const isToday = location.pathname === '/today';
  const isSettings = location.pathname === '/settings';

  return (
    <nav className="mobile-bottom-bar" aria-label="Mobile Navigation">
      <Link 
        to="/" 
        className={`mobile-bottom-item ${isHome ? 'active' : ''}`}
        aria-label="Home"
      >
        <Home size={18} />
        <span className="mobile-bottom-label">Home</span>
      </Link>

      <Link 
        to="/roadmap" 
        className={`mobile-bottom-item ${isRoadmap ? 'active' : ''}`}
        aria-label="Roadmap"
      >
        <Map size={18} />
        <span className="mobile-bottom-label">Roadmap</span>
      </Link>

      <Link 
        to="/today" 
        className={`mobile-bottom-item ${isToday ? 'active' : ''}`}
        aria-label="Today"
        style={{ position: 'relative' }}
      >
        <Calendar size={18} />
        <span className="mobile-bottom-label">Today</span>
        {dueReviews.length > 0 && (
          <span className="mobile-bottom-badge">
            {dueReviews.length}
          </span>
        )}
      </Link>

      <Link 
        to="/settings" 
        className={`mobile-bottom-item ${isSettings ? 'active' : ''}`}
        aria-label="Settings"
      >
        <SettingsIcon size={18} />
        <span className="mobile-bottom-label">Settings</span>
      </Link>
    </nav>
  );
}

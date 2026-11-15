import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, Map, Calendar, Settings as SettingsIcon } from 'lucide-react';
import { useApp } from '../context/AppContext';

export default function MobileNav() {
  const location = useLocation();
  const { dueReviews } = useApp();

  return (
    <nav className="mobile-bottom-bar">
      <Link 
        to="/" 
        className={`mobile-bottom-item ${location.pathname === '/' ? 'active' : ''}`}
      >
        <Home size={19} />
        <span>Home</span>
      </Link>

      <Link 
        to="/roadmap" 
        className={`mobile-bottom-item ${location.pathname.startsWith('/roadmap') ? 'active' : ''}`}
      >
        <Map size={19} />
        <span>Roadmap</span>
      </Link>

      <Link 
        to="/today" 
        className={`mobile-bottom-item ${location.pathname === '/today' ? 'active' : ''}`}
        style={{ position: 'relative' }}
      >
        <Calendar size={19} />
        <span>Today</span>
        {dueReviews.length > 0 && (
          <span style={{
            position: 'absolute',
            top: 4,
            right: 18,
            width: 8,
            height: 8,
            borderRadius: '50%',
            background: 'var(--revisit-color)'
          }} />
        )}
      </Link>

      <Link 
        to="/settings" 
        className={`mobile-bottom-item ${location.pathname === '/settings' ? 'active' : ''}`}
      >
        <SettingsIcon size={19} />
        <span>Settings</span>
      </Link>
    </nav>
  );
}

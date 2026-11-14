import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { Home, Map, Calendar, Settings } from 'lucide-react';

export default function MobileNav() {
  const location = useLocation();
  const { dueReviews } = useApp();

  return (
    <nav className="mobile-nav">
      <Link to="/" className={`mobile-nav-item ${location.pathname === '/' ? 'active' : ''}`}>
        <Home size={20} />
        <span>Home</span>
      </Link>
      <Link to="/roadmap" className={`mobile-nav-item ${location.pathname.startsWith('/roadmap') ? 'active' : ''}`}>
        <Map size={20} />
        <span>Roadmap</span>
      </Link>
      <Link to="/today" className={`mobile-nav-item ${location.pathname === '/today' ? 'active' : ''}`} style={{ position: 'relative' }}>
        <Calendar size={20} />
        <span>Today</span>
        {dueReviews.length > 0 && (
          <span style={{
            position: 'absolute',
            top: '6px',
            right: '25%',
            background: 'var(--danger)',
            color: '#fff',
            fontSize: '0.65rem',
            fontWeight: 700,
            width: '16px',
            height: '16px',
            borderRadius: '9999px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            {dueReviews.length}
          </span>
        )}
      </Link>
      <Link to="/settings" className={`mobile-nav-item ${location.pathname === '/settings' ? 'active' : ''}`}>
        <Settings size={20} />
        <span>Settings</span>
      </Link>
    </nav>
  );
}


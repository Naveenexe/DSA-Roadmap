import React, { useState, useRef, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import ChainlineLogo from './ChainlineLogo';
import { 
  Flame, 
  Sun, 
  Sunset, 
  Moon, 
  Settings as SettingsIcon, 
  LogOut, 
  User, 
  Calendar, 
  Map, 
  Home as HomeIcon,
  ChevronDown
} from 'lucide-react';

export default function Navbar({ onOpenAuth }) {
  const { user, logout, streak, dueReviews, theme, setTheme, updateSettings } = useApp();
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef(null);

  // Close menu on click outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setMenuOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleThemeSelect = (newTheme) => {
    setTheme(newTheme);
    if (user) {
      updateSettings({ theme: newTheme });
    }
  };

  return (
    <header className="topbar-wrapper">
      <div className="topbar-pill">
        {/* Brand Link */}
        <Link to="/" style={{ display: 'inline-flex', alignItems: 'center' }}>
          <ChainlineLogo size={28} showText={true} />
        </Link>

        {/* Central Navigation Pills (Desktop) */}
        <nav className="nav-pill-group">
          <Link to="/" className={`nav-pill ${location.pathname === '/' ? 'active' : ''}`}>
            <HomeIcon size={16} />
            <span>Home</span>
          </Link>
          <Link to="/roadmap" className={`nav-pill ${location.pathname.startsWith('/roadmap') ? 'active' : ''}`}>
            <Map size={16} />
            <span>Roadmap</span>
          </Link>
          <Link to="/today" className={`nav-pill ${location.pathname === '/today' ? 'active' : ''}`}>
            <Calendar size={16} />
            <span>Today</span>
            {dueReviews.length > 0 && (
              <span style={{
                background: 'var(--revisit-color)',
                color: '#FFFFFF',
                fontSize: '0.72rem',
                fontWeight: 700,
                padding: '0.1rem 0.45rem',
                borderRadius: 'var(--radius-pill)'
              }}>
                {dueReviews.length}
              </span>
            )}
          </Link>
          <Link to="/settings" className={`nav-pill ${location.pathname === '/settings' ? 'active' : ''}`}>
            <SettingsIcon size={16} />
            <span>Settings</span>
          </Link>
        </nav>

        {/* Right Actions */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
          {/* Daily Streak Chip (Section 3 #2: flame + number + 'days') */}
          <div className="streak-chip" title={`${streak} days streak`}>
            <Flame size={16} fill="currentColor" />
            <span>{streak} {streak === 1 ? 'day' : 'days'}</span>
          </div>

          {/* Three-Mode Glass Switcher: Sun, Sunset, Moon (always visible on desktop/tablet) */}
          <div className="topbar-mode-switch" role="group" aria-label="Theme mode switcher">
            <button
              type="button"
              onClick={() => handleThemeSelect('light')}
              className={`mode-switch-btn ${theme === 'light' ? 'active' : ''}`}
              title="Light (Daylight)"
              aria-label="Light mode"
            >
              <Sun size={14} />
            </button>
            <button
              type="button"
              onClick={() => handleThemeSelect('evening')}
              className={`mode-switch-btn ${theme === 'evening' ? 'active' : ''}`}
              title="Evening (Dusk)"
              aria-label="Evening mode"
            >
              <Sunset size={14} />
            </button>
            <button
              type="button"
              onClick={() => handleThemeSelect('dark')}
              className={`mode-switch-btn ${theme === 'dark' ? 'active' : ''}`}
              title="Dark (Midnight)"
              aria-label="Dark mode"
            >
              <Moon size={14} />
            </button>
          </div>

          {/* User Account / Avatar Menu (Section 3 #3 & FR-31) */}
          {user ? (
            <div style={{ position: 'relative' }} ref={menuRef}>
              <button 
                onClick={() => setMenuOpen(!menuOpen)}
                className="btn-secondary"
                style={{ 
                  padding: '0.35rem 0.75rem', 
                  borderRadius: 'var(--radius-pill)',
                  display: 'inline-flex', 
                  alignItems: 'center', 
                  gap: '0.45rem',
                  fontSize: '0.85rem'
                }}
                aria-label="User Account Menu"
              >
                <div style={{
                  width: 26,
                  height: 26,
                  borderRadius: '50%',
                  background: 'var(--accent)',
                  color: 'var(--accent-text)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '0.75rem',
                  fontWeight: 700
                }}>
                  {user.display_name ? user.display_name.charAt(0).toUpperCase() : user.username.charAt(0).toUpperCase()}
                </div>
                <span style={{ maxWidth: 110, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', fontWeight: 600 }}>
                  {user.display_name || user.username}
                </span>
                <ChevronDown size={14} style={{ opacity: 0.6 }} />
              </button>

              {/* Dropdown Menu */}
              {menuOpen && (
                <div 
                  className="glass-card" 
                  style={{
                    position: 'absolute',
                    top: 'calc(100% + 8px)',
                    right: 0,
                    width: 240,
                    padding: '12px',
                    borderRadius: 'var(--radius-inner)',
                    zIndex: 100,
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '6px'
                  }}
                >
                  {/* User info */}
                  <div style={{ padding: '6px 10px', borderBottom: '1px solid var(--glass-border)', marginBottom: '4px' }}>
                    <div style={{ fontWeight: 700, fontSize: '0.9rem', color: 'var(--text-color)' }}>
                      {user.display_name || user.username}
                    </div>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                      @{user.username}
                    </div>
                  </div>

                  {/* Mode switcher (Light, Evening, Dark) */}
                  <div style={{ padding: '4px 8px' }}>
                    <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                      Theme Mode
                    </span>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '4px', marginTop: '6px' }}>
                      <button
                        onClick={() => handleThemeSelect('light')}
                        style={{
                          padding: '6px',
                          borderRadius: 'var(--radius-pill)',
                          border: '1px solid',
                          borderColor: theme === 'light' ? 'var(--accent)' : 'var(--glass-border)',
                          background: theme === 'light' ? 'var(--accent)' : 'var(--glass-surface)',
                          color: theme === 'light' ? 'var(--accent-text)' : 'var(--text-color)',
                          fontSize: '0.72rem',
                          fontWeight: 600,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          gap: '2px'
                        }}
                      >
                        <Sun size={12} />
                        <span>Light</span>
                      </button>
                      <button
                        onClick={() => handleThemeSelect('evening')}
                        style={{
                          padding: '6px',
                          borderRadius: 'var(--radius-pill)',
                          border: '1px solid',
                          borderColor: theme === 'evening' ? 'var(--accent)' : 'var(--glass-border)',
                          background: theme === 'evening' ? 'var(--accent)' : 'var(--glass-surface)',
                          color: theme === 'evening' ? 'var(--accent-text)' : 'var(--text-color)',
                          fontSize: '0.72rem',
                          fontWeight: 600,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          gap: '2px'
                        }}
                      >
                        <Sunset size={12} />
                        <span>Dusk</span>
                      </button>
                      <button
                        onClick={() => handleThemeSelect('dark')}
                        style={{
                          padding: '6px',
                          borderRadius: 'var(--radius-pill)',
                          border: '1px solid',
                          borderColor: theme === 'dark' ? 'var(--accent)' : 'var(--glass-border)',
                          background: theme === 'dark' ? 'var(--accent)' : 'var(--glass-surface)',
                          color: theme === 'dark' ? 'var(--accent-text)' : 'var(--text-color)',
                          fontSize: '0.72rem',
                          fontWeight: 600,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          gap: '2px'
                        }}
                      >
                        <Moon size={12} />
                        <span>Dark</span>
                      </button>
                    </div>
                  </div>

                  {/* Settings Link */}
                  <Link 
                    to="/settings" 
                    onClick={() => setMenuOpen(false)}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.5rem',
                      padding: '8px 10px',
                      borderRadius: 'var(--radius-pill)',
                      fontSize: '0.85rem',
                      fontWeight: 600,
                      color: 'var(--text-color)',
                      transition: 'background 150ms ease'
                    }}
                    onMouseEnter={(e) => e.currentTarget.style.background = 'var(--glass-strong)'}
                    onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
                  >
                    <SettingsIcon size={15} />
                    <span>Settings</span>
                  </Link>

                  {/* Log Out Button */}
                  <button
                    onClick={() => {
                      setMenuOpen(false);
                      logout();
                    }}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.5rem',
                      padding: '8px 10px',
                      borderRadius: 'var(--radius-pill)',
                      fontSize: '0.85rem',
                      fontWeight: 600,
                      color: '#EF4444',
                      transition: 'background 150ms ease',
                      width: '100%',
                      textAlign: 'left'
                    }}
                    onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(239, 68, 68, 0.12)'}
                    onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
                  >
                    <LogOut size={15} />
                    <span>Log Out</span>
                  </button>
                </div>
              )}
            </div>
          ) : (
            <button 
              onClick={onOpenAuth} 
              className="btn-primary"
              style={{ padding: '0.45rem 1rem', fontSize: '0.85rem' }}
            >
              Sign In
            </button>
          )}
        </div>
      </div>
    </header>
  );
}

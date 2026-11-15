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
  ChevronDown,
  LogIn
} from 'lucide-react';

export default function Navbar({ onOpenAuth }) {
  const { user, logout, streak, dueReviews, theme, setTheme, updateSettings, language, updateLanguage } = useApp();
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

        {/* Central Navigation Pills (Desktop only, hidden on mobile) */}
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
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          {/* Daily Streak Chip (Section 3 #2: flame + number + 'days') */}
          <div className="streak-chip" title={`${streak} days streak`}>
            <Flame size={15} fill="currentColor" />
            <span className="streak-chip-text">{streak} {streak === 1 ? 'day' : 'days'}</span>
            <span className="streak-chip-short">{streak}</span>
          </div>

          {/* Three-Mode Glass Switcher: Sun, Sunset, Moon (Desktop/Tablet topbar) */}
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

          {/* User Account / Avatar Button (Mobile & Desktop) */}
          <div style={{ position: 'relative' }} ref={menuRef}>
            {user ? (
              <button 
                onClick={() => setMenuOpen(!menuOpen)}
                className="btn-secondary avatar-btn"
                style={{ 
                  padding: '0.35rem 0.65rem', 
                  borderRadius: 'var(--radius-pill)',
                  display: 'inline-flex', 
                  alignItems: 'center', 
                  gap: '0.45rem',
                  fontSize: '0.85rem',
                  minHeight: '44px'
                }}
                aria-label="User Account Menu"
              >
                <div style={{
                  width: 28,
                  height: 28,
                  borderRadius: '50%',
                  background: 'var(--accent)',
                  color: 'var(--accent-text)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '0.8rem',
                  fontWeight: 700
                }}>
                  {user.display_name ? user.display_name.charAt(0).toUpperCase() : user.username.charAt(0).toUpperCase()}
                </div>
                <span className="navbar-username" style={{ maxWidth: 90, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', fontWeight: 600 }}>
                  {user.display_name || user.username}
                </span>
                <ChevronDown size={14} style={{ opacity: 0.6 }} />
              </button>
            ) : (
              <>
                {/* Desktop Sign In button */}
                <button 
                  onClick={onOpenAuth} 
                  className="btn-primary desktop-signin-btn"
                  style={{ padding: '0.45rem 1rem', fontSize: '0.85rem', minHeight: '44px' }}
                >
                  Sign In
                </button>
                {/* Mobile avatar button when logged out */}
                <button
                  onClick={() => setMenuOpen(!menuOpen)}
                  className="btn-secondary mobile-avatar-btn"
                  style={{
                    width: 44,
                    height: 44,
                    borderRadius: '50%',
                    padding: 0,
                    display: 'none',
                    alignItems: 'center',
                    justifyContent: 'center',
                    minHeight: '44px'
                  }}
                  aria-label="Account and Settings Menu"
                >
                  <User size={18} />
                </button>
              </>
            )}

            {/* Dropdown Menu (SRS 2.0 Part 2: Avatar menu holds Light/Evening/Dark, Java/Python, Settings, Log out) */}
            {menuOpen && (
              <div 
                className="glass-card avatar-dropdown-menu" 
                style={{
                  position: 'absolute',
                  top: 'calc(100% + 8px)',
                  right: 0,
                  width: 250,
                  padding: '12px',
                  borderRadius: 'var(--radius-inner)',
                  zIndex: 100,
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '8px',
                  boxShadow: '0 12px 36px rgba(0,0,0,0.25)'
                }}
              >
                {/* User info if logged in, or Sign in prompt if logged out */}
                {user ? (
                  <div style={{ padding: '6px 8px', borderBottom: '1px solid var(--glass-border)' }}>
                    <div style={{ fontWeight: 700, fontSize: '0.9rem', color: 'var(--text-color)' }}>
                      {user.display_name || user.username}
                    </div>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                      @{user.username}
                    </div>
                  </div>
                ) : (
                  <div style={{ padding: '6px 8px', borderBottom: '1px solid var(--glass-border)' }}>
                    <button
                      type="button"
                      onClick={() => {
                        setMenuOpen(false);
                        onOpenAuth();
                      }}
                      className="btn-primary"
                      style={{ width: '100%', minHeight: '44px', fontSize: '0.85rem' }}
                    >
                      <LogIn size={15} />
                      <span>Sign In / Create</span>
                    </button>
                  </div>
                )}

                {/* Mode switcher (Light, Evening, Dark) */}
                <div style={{ padding: '4px 6px' }}>
                  <span style={{ fontSize: '0.72rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                    Theme Mode
                  </span>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '4px', marginTop: '6px' }}>
                    <button
                      type="button"
                      onClick={() => handleThemeSelect('light')}
                      style={{
                        padding: '8px 4px',
                        minHeight: '44px',
                        borderRadius: 'var(--radius-pill)',
                        border: '1px solid',
                        borderColor: theme === 'light' ? 'var(--accent)' : 'var(--glass-border)',
                        background: theme === 'light' ? 'var(--accent)' : 'var(--glass-surface)',
                        color: theme === 'light' ? 'var(--accent-text)' : 'var(--text-color)',
                        fontSize: '0.75rem',
                        fontWeight: 600,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '3px'
                      }}
                    >
                      <Sun size={13} />
                      <span>Light</span>
                    </button>
                    <button
                      type="button"
                      onClick={() => handleThemeSelect('evening')}
                      style={{
                        padding: '8px 4px',
                        minHeight: '44px',
                        borderRadius: 'var(--radius-pill)',
                        border: '1px solid',
                        borderColor: theme === 'evening' ? 'var(--accent)' : 'var(--glass-border)',
                        background: theme === 'evening' ? 'var(--accent)' : 'var(--glass-surface)',
                        color: theme === 'evening' ? 'var(--accent-text)' : 'var(--text-color)',
                        fontSize: '0.75rem',
                        fontWeight: 600,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '3px'
                      }}
                    >
                      <Sunset size={13} />
                      <span>Dusk</span>
                    </button>
                    <button
                      type="button"
                      onClick={() => handleThemeSelect('dark')}
                      style={{
                        padding: '8px 4px',
                        minHeight: '44px',
                        borderRadius: 'var(--radius-pill)',
                        border: '1px solid',
                        borderColor: theme === 'dark' ? 'var(--accent)' : 'var(--glass-border)',
                        background: theme === 'dark' ? 'var(--accent)' : 'var(--glass-surface)',
                        color: theme === 'dark' ? 'var(--accent-text)' : 'var(--text-color)',
                        fontSize: '0.75rem',
                        fontWeight: 600,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '3px'
                      }}
                    >
                      <Moon size={13} />
                      <span>Dark</span>
                    </button>
                  </div>
                </div>

                {/* Java | Python Switcher */}
                <div style={{ padding: '4px 6px' }}>
                  <span style={{ fontSize: '0.72rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                    Code Language
                  </span>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '4px', marginTop: '6px' }}>
                    <button
                      type="button"
                      onClick={() => updateLanguage('java')}
                      style={{
                        padding: '8px 4px',
                        minHeight: '44px',
                        borderRadius: 'var(--radius-pill)',
                        border: '1px solid',
                        borderColor: language === 'java' ? 'var(--accent)' : 'var(--glass-border)',
                        background: language === 'java' ? 'var(--accent)' : 'var(--glass-surface)',
                        color: language === 'java' ? 'var(--accent-text)' : 'var(--text-color)',
                        fontSize: '0.78rem',
                        fontWeight: 700,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center'
                      }}
                    >
                      Java
                    </button>
                    <button
                      type="button"
                      onClick={() => updateLanguage('python')}
                      style={{
                        padding: '8px 4px',
                        minHeight: '44px',
                        borderRadius: 'var(--radius-pill)',
                        border: '1px solid',
                        borderColor: language === 'python' ? 'var(--accent)' : 'var(--glass-border)',
                        background: language === 'python' ? 'var(--accent)' : 'var(--glass-surface)',
                        color: language === 'python' ? 'var(--accent-text)' : 'var(--text-color)',
                        fontSize: '0.78rem',
                        fontWeight: 700,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center'
                      }}
                    >
                      Python
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
                    padding: '10px 12px',
                    borderRadius: 'var(--radius-pill)',
                    fontSize: '0.85rem',
                    fontWeight: 600,
                    color: 'var(--text-color)',
                    minHeight: '44px',
                    transition: 'background 150ms ease'
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.background = 'var(--glass-strong)'}
                  onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
                >
                  <SettingsIcon size={16} />
                  <span>Settings</span>
                </Link>

                {/* Log Out Button if logged in */}
                {user && (
                  <button
                    type="button"
                    onClick={() => {
                      setMenuOpen(false);
                      logout();
                    }}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.5rem',
                      padding: '10px 12px',
                      borderRadius: 'var(--radius-pill)',
                      fontSize: '0.85rem',
                      fontWeight: 600,
                      color: '#EF4444',
                      minHeight: '44px',
                      transition: 'background 150ms ease',
                      width: '100%',
                      textAlign: 'left'
                    }}
                    onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(239, 68, 68, 0.12)'}
                    onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
                  >
                    <LogOut size={16} />
                    <span>Log Out</span>
                  </button>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}

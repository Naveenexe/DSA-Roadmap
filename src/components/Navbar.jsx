import React, { useState, useRef, useEffect } from 'react';
import { createPortal } from 'react-dom';
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
  ChevronRight,
  LogIn,
  X
} from 'lucide-react';

export default function Navbar({ onOpenAuth }) {
  const { user, logout, streak, dueReviews, theme, setTheme, updateSettings, language, updateLanguage } = useApp();
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef(null);

  // Responsive mobile tracker
  const [isMobile, setIsMobile] = useState(() => {
    if (typeof window !== 'undefined') {
      return window.innerWidth < 768;
    }
    return false;
  });

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Close menu on click outside (desktop dropdown) or Escape key (both)
  useEffect(() => {
    function handleClickOutside(event) {
      if (!isMobile && menuRef.current && !menuRef.current.contains(event.target)) {
        setMenuOpen(false);
      }
    }

    function handleKeyDown(event) {
      if (event.key === 'Escape') {
        setMenuOpen(false);
      }
    }

    if (menuOpen) {
      // Lock scroll while avatar sheet is open on phones (Bug 2 #2)
      if (isMobile) {
        document.body.style.overflow = 'hidden';
      }
      document.addEventListener('mousedown', handleClickOutside);
      window.addEventListener('keydown', handleKeyDown);
    } else {
      document.body.style.overflow = '';
    }

    return () => {
      document.body.style.overflow = '';
      document.removeEventListener('mousedown', handleClickOutside);
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [menuOpen, isMobile]);

  const handleThemeSelect = (newTheme) => {
    setTheme(newTheme);
    if (user) {
      updateSettings({ theme: newTheme });
    }
  };

  // Content inside Avatar Menu (Shared between desktop dropdown and mobile sheet)
  const renderMenuContent = () => (
    <>
      {/* Drag handle (visible on mobile bottom sheet only) */}
      <div className="avatar-menu-handle" />

      {/* Header row with title and Close button */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingBottom: '4px' }}>
        <span style={{
          fontSize: '0.8rem',
          fontFamily: 'var(--font-mono)',
          fontWeight: 700,
          color: 'var(--text-muted)',
          textTransform: 'uppercase',
          letterSpacing: '0.08em'
        }}>
          {user ? `@${user.username}` : 'Menu'}
        </span>
        <button
          type="button"
          onClick={() => setMenuOpen(false)}
          className="icon-circle-btn"
          style={{ width: 36, height: 36, minWidth: 36, minHeight: 36 }}
          aria-label="Close menu"
        >
          <X size={16} />
        </button>
      </div>

      {/* 1. Account Row (Sign In / Create account, or username and Log out) */}
      {user ? (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '12px',
          padding: '12px 14px',
          borderRadius: 'var(--radius-inner)',
          background: 'var(--glass-surface)',
          border: '1px solid var(--glass-border)',
          minHeight: '44px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', minWidth: 0, flex: 1 }}>
            <div style={{
              width: 34,
              height: 34,
              borderRadius: '50%',
              background: 'var(--accent)',
              color: 'var(--accent-text)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: 700,
              fontSize: '0.9rem',
              flexShrink: 0
            }}>
              {user.display_name ? user.display_name.charAt(0).toUpperCase() : user.username.charAt(0).toUpperCase()}
            </div>
            <div style={{ overflow: 'hidden' }}>
              <div style={{ fontWeight: 700, fontSize: '0.92rem', color: 'var(--text-color)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                {user.display_name || user.username}
              </div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                @{user.username}
              </div>
            </div>
          </div>
          <button
            type="button"
            onClick={() => {
              setMenuOpen(false);
              logout();
            }}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              padding: '8px 14px',
              minHeight: '44px',
              borderRadius: 'var(--radius-pill)',
              border: '1px solid rgba(239, 68, 68, 0.35)',
              background: 'rgba(239, 68, 68, 0.12)',
              color: '#EF4444',
              fontWeight: 600,
              fontSize: '0.85rem',
              flexShrink: 0,
              cursor: 'pointer'
            }}
          >
            <LogOut size={15} />
            <span>Log Out</span>
          </button>
        </div>
      ) : (
        <button
          type="button"
          onClick={() => {
            setMenuOpen(false);
            onOpenAuth();
          }}
          className="btn-primary"
          style={{
            width: '100%',
            minHeight: '44px',
            fontSize: '0.92rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '8px'
          }}
        >
          <LogIn size={16} />
          <span>Sign In / Create account</span>
        </button>
      )}

      {/* 2. Theme Mode with three buttons in one row: Light, Dusk, Dark (Bug 2 #4) */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
          Theme Mode
        </span>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '8px' }}>
          <button
            type="button"
            onClick={() => handleThemeSelect('light')}
            style={{
              padding: '10px 6px',
              minHeight: '44px',
              borderRadius: 'var(--radius-pill)',
              border: '1px solid',
              borderColor: theme === 'light' ? 'var(--accent)' : 'var(--glass-border)',
              background: theme === 'light' ? 'var(--accent)' : 'var(--glass-surface)',
              color: theme === 'light' ? 'var(--accent-text)' : 'var(--text-color)',
              fontSize: '0.85rem',
              fontWeight: 600,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '6px',
              cursor: 'pointer'
            }}
          >
            <Sun size={15} />
            <span>Light</span>
          </button>
          <button
            type="button"
            onClick={() => handleThemeSelect('evening')}
            style={{
              padding: '10px 6px',
              minHeight: '44px',
              borderRadius: 'var(--radius-pill)',
              border: '1px solid',
              borderColor: theme === 'evening' ? 'var(--accent)' : 'var(--glass-border)',
              background: theme === 'evening' ? 'var(--accent)' : 'var(--glass-surface)',
              color: theme === 'evening' ? 'var(--accent-text)' : 'var(--text-color)',
              fontSize: '0.85rem',
              fontWeight: 600,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '6px',
              cursor: 'pointer'
            }}
          >
            <Sunset size={15} />
            <span>Dusk</span>
          </button>
          <button
            type="button"
            onClick={() => handleThemeSelect('dark')}
            style={{
              padding: '10px 6px',
              minHeight: '44px',
              borderRadius: 'var(--radius-pill)',
              border: '1px solid',
              borderColor: theme === 'dark' ? 'var(--accent)' : 'var(--glass-border)',
              background: theme === 'dark' ? 'var(--accent)' : 'var(--glass-surface)',
              color: theme === 'dark' ? 'var(--accent-text)' : 'var(--text-color)',
              fontSize: '0.85rem',
              fontWeight: 600,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '6px',
              cursor: 'pointer'
            }}
          >
            <Moon size={15} />
            <span>Dark</span>
          </button>
        </div>
      </div>

      {/* 3. Code Language with two equal buttons: Java, Python (Bug 2 #4) */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
          Code Language
        </span>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
          <button
            type="button"
            onClick={() => updateLanguage('java')}
            style={{
              padding: '10px',
              minHeight: '44px',
              borderRadius: 'var(--radius-pill)',
              border: '1px solid',
              borderColor: language === 'java' ? 'var(--accent)' : 'var(--glass-border)',
              background: language === 'java' ? 'var(--accent)' : 'var(--glass-surface)',
              color: language === 'java' ? 'var(--accent-text)' : 'var(--text-color)',
              fontSize: '0.88rem',
              fontWeight: 700,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer'
            }}
          >
            Java
          </button>
          <button
            type="button"
            onClick={() => updateLanguage('python')}
            style={{
              padding: '10px',
              minHeight: '44px',
              borderRadius: 'var(--radius-pill)',
              border: '1px solid',
              borderColor: language === 'python' ? 'var(--accent)' : 'var(--glass-border)',
              background: language === 'python' ? 'var(--accent)' : 'var(--glass-surface)',
              color: language === 'python' ? 'var(--accent-text)' : 'var(--text-color)',
              fontSize: '0.88rem',
              fontWeight: 700,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer'
            }}
          >
            Python
          </button>
        </div>
      </div>

      {/* 4. Settings Link as a full-width row (Bug 2 #4) */}
      <Link 
        to="/settings" 
        onClick={() => setMenuOpen(false)}
        className="btn-secondary"
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '12px 16px',
          borderRadius: 'var(--radius-pill)',
          fontSize: '0.9rem',
          fontWeight: 600,
          color: 'var(--text-color)',
          minHeight: '44px',
          width: '100%',
          boxSizing: 'border-box'
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <SettingsIcon size={18} />
          <span>Settings</span>
        </div>
        <ChevronRight size={16} style={{ opacity: 0.6 }} />
      </Link>
    </>
  );

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

            {/* Desktop Dropdown: rendered in place when >= 768px (z-index: 40) */}
            {!isMobile && menuOpen && (
              <div className="avatar-menu-container">
                {renderMenuContent()}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Mobile Bottom Sheet: Rendered in Portal to document.body when < 768px */}
      {isMobile && menuOpen && createPortal(
        <>
          <div 
            className="avatar-sheet-backdrop" 
            onClick={() => setMenuOpen(false)}
            aria-label="Close menu backdrop"
          />
          <div className="avatar-menu-container">
            {renderMenuContent()}
          </div>
        </>,
        document.body
      )}
    </header>
  );
}

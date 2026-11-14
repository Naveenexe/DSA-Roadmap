import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { 
  Home, 
  Map, 
  Calendar, 
  Settings, 
  Sun, 
  Moon, 
  ArrowRight, 
  User, 
  LogOut,
  Flame
} from 'lucide-react';

export default function Navbar({ onOpenLogin }) {
  const { user, logout, getNextUp, updateSettings, dueReviews, streak } = useApp();
  const location = useLocation();
  const navigate = useNavigate();

  const nextUpQuestion = getNextUp();

  const handleNextUp = () => {
    if (nextUpQuestion) {
      navigate(`/question/${nextUpQuestion.seq}`);
    } else {
      navigate('/roadmap');
    }
  };

  const toggleTheme = () => {
    const current = user?.theme || document.documentElement.getAttribute('data-theme') || 'dark';
    const nextTheme = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', nextTheme);
    if (user) {
      updateSettings({ theme: nextTheme });
    }
  };

  const toggleLanguage = () => {
    const nextLang = (user?.language || 'java') === 'java' ? 'python' : 'java';
    if (user) {
      updateSettings({ language: nextLang });
    }
  };

  const currentTheme = user?.theme || document.documentElement.getAttribute('data-theme') || 'dark';
  const currentLang = user?.language || 'java';

  return (
    <header className="navbar">
      <div className="nav-container">
        <Link to="/" className="brand">
          <span>DSA Roadmap</span>
          <span className="brand-badge">300</span>
        </Link>

        <nav className="nav-links">
          <Link to="/" className={`nav-item ${location.pathname === '/' ? 'active' : ''}`}>
            <Home size={17} />
            <span>Dashboard</span>
          </Link>
          <Link to="/roadmap" className={`nav-item ${location.pathname.startsWith('/roadmap') ? 'active' : ''}`}>
            <Map size={17} />
            <span>Roadmap</span>
          </Link>
          <Link to="/today" className={`nav-item ${location.pathname === '/today' ? 'active' : ''}`}>
            <Calendar size={17} />
            <span>Today</span>
            {dueReviews.length > 0 && (
              <span style={{
                background: 'var(--danger)',
                color: '#fff',
                fontSize: '0.7rem',
                fontWeight: 700,
                padding: '0.1rem 0.4rem',
                borderRadius: '9999px',
                marginLeft: '0.2rem'
              }}>
                {dueReviews.length}
              </span>
            )}
          </Link>
          <Link to="/settings" className={`nav-item ${location.pathname === '/settings' ? 'active' : ''}`}>
            <Settings size={17} />
            <span>Settings</span>
          </Link>
        </nav>

        <div className="nav-actions">
          {streak > 0 && (
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.25rem',
              color: 'var(--warning)',
              fontWeight: 700,
              fontSize: '0.85rem',
              padding: '0.3rem 0.6rem',
              background: 'var(--warning-bg)',
              borderRadius: 'var(--radius-full)'
            }} title={`${streak} day streak`}>
              <Flame size={16} fill="currentColor" />
              <span>{streak}d</span>
            </div>
          )}

          <button 
            onClick={handleNextUp} 
            className="btn-next-up"
            title={nextUpQuestion ? `Next Up: #${nextUpQuestion.seq} ${nextUpQuestion.title}` : 'All complete!'}
          >
            <span>Next up {nextUpQuestion ? `#${nextUpQuestion.seq}` : '🎉'}</span>
            <ArrowRight size={14} />
          </button>

          <button 
            onClick={toggleLanguage} 
            className="lang-badge"
            title="Switch code language (Java / Python)"
          >
            {currentLang.toUpperCase()}
          </button>

          <button 
            onClick={toggleTheme} 
            className="icon-btn"
            title="Toggle theme"
          >
            {currentTheme === 'dark' ? <Sun size={17} /> : <Moon size={17} />}
          </button>

          {user ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <Link 
                to="/settings" 
                className="icon-btn" 
                style={{ width: 'auto', padding: '0 0.6rem', gap: '0.35rem', fontSize: '0.825rem', fontWeight: 600 }}
                title={`Signed in as ${user.username}`}
              >
                <User size={15} />
                <span>{user.username}</span>
              </Link>
              <button 
                onClick={logout} 
                className="icon-btn" 
                title="Log out"
              >
                <LogOut size={16} />
              </button>
            </div>
          ) : (
            <button onClick={onOpenLogin} className="btn-primary" style={{ padding: '0.4rem 0.85rem', fontSize: '0.825rem' }}>
              Sign In
            </button>
          )}
        </div>
      </div>
    </header>
  );
}


import React, { useState, useEffect } from 'react';
import { useApp } from '../context/AppContext';
import ChainlineLogo from './ChainlineLogo';
import { 
  Flame, 
  CheckCircle2, 
  Lock, 
  User, 
  Sun, 
  Sunset, 
  Moon, 
  ArrowRight, 
  Sparkles, 
  AlertCircle,
  X
} from 'lucide-react';
import { getFriendlyErrorMessage } from '../services/api';

export default function AuthView({ isOpen, onClose, initialTab = 'signin' }) {
  const { login, register, theme, setTheme, questions } = useApp();
  const totalQuestions = questions?.length || 500;
  const [tab, setTab] = useState(initialTab); // 'signin' or 'signup'

  // Form states
  const [username, setUsername] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [pinDigits, setPinDigits] = useState(['', '', '', '']);
  const [pinRequired, setPinRequired] = useState(false);
  const [dailyGoal, setDailyGoal] = useState(2);
  const [language, setLanguage] = useState('java');
  const [selectedTheme, setSelectedTheme] = useState(theme || 'light');

  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [suggestCreate, setSuggestCreate] = useState(false);

  useEffect(() => {
    setTab(initialTab);
    setErrorMsg('');
    setSuggestCreate(false);
    setPinRequired(false);
    setPinDigits(['', '', '', '']);
    if (theme) setSelectedTheme(theme);
  }, [initialTab, isOpen, theme]);

  if (!isOpen) return null;

  const pinValue = pinDigits.join('');

  const handlePinDigitChange = (index, val) => {
    const digit = val.slice(-1).replace(/\D/g, '');
    const newDigits = [...pinDigits];
    newDigits[index] = digit;
    setPinDigits(newDigits);

    // Auto-advance
    if (digit && index < 3) {
      const nextInput = document.getElementById(`auth-pin-input-${index + 1}`);
      if (nextInput) nextInput.focus();
    }
  };

  const handlePinKeyDown = (index, e) => {
    if (e.key === 'Backspace' && !pinDigits[index] && index > 0) {
      const prevInput = document.getElementById(`auth-pin-input-${index - 1}`);
      if (prevInput) prevInput.focus();
    }
  };

  const handleThemeChangeImmediate = (newTheme) => {
    setSelectedTheme(newTheme);
    setTheme(newTheme);
  };

  const handleSignInSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setSuggestCreate(false);

    const cleanUser = username.trim().toLowerCase();
    if (!/^[a-z0-9_]{3,20}$/.test(cleanUser)) {
      setErrorMsg('Use 3 to 20 letters, numbers or underscores.');
      return;
    }

    setLoading(true);
    try {
      await login(cleanUser, pinRequired ? pinValue : null);
      if (onClose) onClose();
    } catch (err) {
      const friendly = getFriendlyErrorMessage(err.message);
      if (friendly === 'PIN_REQUIRED') {
        setPinRequired(true);
        setErrorMsg('This account requires a 4-digit PIN.');
      } else if (friendly.includes('No account with that username')) {
        setErrorMsg(friendly);
        setSuggestCreate(true);
      } else {
        setErrorMsg(friendly);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCreateSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');

    const cleanUser = username.trim().toLowerCase();
    if (!/^[a-z0-9_]{3,20}$/.test(cleanUser)) {
      setErrorMsg('Use 3 to 20 letters, numbers or underscores.');
      return;
    }

    if (pinValue && pinValue.length < 4) {
      setErrorMsg('PIN must be exactly 4 digits, or left completely blank.');
      return;
    }

    setLoading(true);
    try {
      await register({
        username: cleanUser,
        displayName: displayName.trim() || null,
        pin: pinValue.length === 4 ? pinValue : null,
        dailyGoal,
        language,
        theme: selectedTheme
      });
      if (onClose) onClose();
    } catch (err) {
      setErrorMsg(getFriendlyErrorMessage(err.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-overlay">
      <div className="auth-container-card auth-two-column-grid">
        
        {/* Close button */}
        {onClose && (
          <button 
            type="button"
            onClick={onClose}
            className="icon-circle-btn auth-close-btn"
            title="Close"
            aria-label="Close authentication modal"
          >
            <X size={18} />
          </button>
        )}

        {/* LEFT / HEADER HALF: Logo, Heading "Solve 300, in order.", preview cards */}
        <div className="auth-hero-half">
          <div className="auth-brand-row">
            <ChainlineLogo size={32} showText={true} />
          </div>

          <div>
            <h1 className="auth-hero-heading">
              Solve {totalQuestions}, <span style={{ fontStyle: 'italic', fontWeight: 800 }}>in order.</span>
            </h1>
            <p className="auth-hero-tagline">
              A curated chain of {totalQuestions} LeetCode questions, each building directly on the last.
            </p>
          </div>

          {/* Three Floating Glass Preview Cards (Desktop only, removed on phones) */}
          <div className="auth-preview-cards-container">
            {/* Preview Card 1: Progress Ring & Status */}
            <div className="glass-card" style={{ padding: '16px 20px', display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
              <div style={{ position: 'relative', width: 56, height: 56, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <svg width="56" height="56" viewBox="0 0 56 56">
                  <circle cx="28" cy="28" r="22" stroke="var(--progress-track)" strokeWidth="5" fill="none" />
                  <circle 
                    cx="28" cy="28" r="22" 
                    stroke="var(--accent)" 
                    strokeWidth="5" 
                    strokeDasharray="138.2" 
                    strokeDashoffset="99.5" 
                    strokeLinecap="round" 
                    fill="none" 
                    transform="rotate(-90 28 28)" 
                  />
                </svg>
                <span style={{ position: 'absolute', fontSize: '0.78rem', fontWeight: 700, fontFamily: 'var(--font-mono)' }}>
                  28%
                </span>
              </div>
              <div>
                <div style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-color)' }}>
                  {Math.round(totalQuestions * 0.28)} of {totalQuestions} Questions Solved
                </div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  Contiguous algorithmic chain from Foundation to Advanced
                </div>
              </div>
            </div>

            {/* Preview Card 2: Streak Chip */}
            <div className="glass-card" style={{ padding: '12px 18px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                <div className="streak-chip">
                  <Flame size={15} fill="currentColor" />
                  <span>5 days</span>
                </div>
                <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-color)' }}>
                  Daily Recall Maintained
                </span>
              </div>
              <CheckCircle2 size={18} color="var(--accent)" />
            </div>

            {/* Preview Card 3: Row of Roadmap List */}
            <div className="glass-card" style={{ padding: '12px 18px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '10px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', overflow: 'hidden' }}>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: 'var(--text-muted)' }}>#1</span>
                <span style={{ fontWeight: 600, fontSize: '0.88rem', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  Contains Duplicate
                </span>
              </div>
              <span className="diff-pill diff-pill-easy" style={{ width: 68, height: 24, fontSize: '0.72rem' }}>
                Easy
              </span>
            </div>
          </div>
        </div>

        {/* RIGHT / MAIN CARD: Full width on phones with 16px side margins */}
        <div className="glass-card auth-form-card">
          
          {/* Top Two-Part Segmented Switch: Sign in | Create account */}
          <div className="auth-tab-switch-row">
            <div className="auth-segmented-control">
              <button
                type="button"
                onClick={() => {
                  setTab('signin');
                  setErrorMsg('');
                  setSuggestCreate(false);
                }}
                className={`auth-segment-btn ${tab === 'signin' ? 'active' : ''}`}
              >
                Sign in
              </button>
              <button
                type="button"
                onClick={() => {
                  setTab('signup');
                  setErrorMsg('');
                  setSuggestCreate(false);
                }}
                className={`auth-segment-btn ${tab === 'signup' ? 'active' : ''}`}
              >
                Create account
              </button>
            </div>
          </div>

          {/* Error Message Alert */}
          {errorMsg && (
            <div className="auth-error-banner">
              <AlertCircle size={16} style={{ flexShrink: 0 }} />
              <div>
                <span>{errorMsg}</span>
                {suggestCreate && (
                  <button
                    type="button"
                    onClick={() => {
                      setTab('signup');
                      setErrorMsg('');
                      setSuggestCreate(false);
                    }}
                    style={{
                      marginLeft: '6px',
                      color: 'var(--accent)',
                      fontWeight: 700,
                      textDecoration: 'underline'
                    }}
                  >
                    Create account now →
                  </button>
                )}
              </div>
            </div>
          )}

          {/* TAB 1: SIGN IN */}
          {tab === 'signin' && (
            <form onSubmit={handleSignInSubmit} className="auth-form-body">
              <div>
                <label className="input-label">Username</label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value.toLowerCase())}
                  placeholder="e.g. codemaster_99"
                  className="glass-input auth-input"
                  required
                  autoFocus
                  autoComplete="username"
                  autoCapitalize="none"
                  spellCheck="false"
                />
              </div>

              {/* PIN boxes if required */}
              {pinRequired && (
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
                    <label className="input-label" style={{ margin: 0 }}>4-digit PIN</label>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Enter your 4 digits</span>
                  </div>
                  <div className="auth-pin-grid">
                    {[0, 1, 2, 3].map(i => (
                      <input
                        key={i}
                        id={`auth-pin-input-${i}`}
                        type="password"
                        inputMode="numeric"
                        pattern="[0-9]*"
                        maxLength={1}
                        value={pinDigits[i]}
                        onChange={(e) => handlePinDigitChange(i, e.target.value)}
                        onKeyDown={(e) => handlePinKeyDown(i, e)}
                        className="glass-input auth-pin-box"
                        required={pinRequired}
                      />
                    ))}
                  </div>
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="btn-primary auth-submit-btn"
              >
                {loading ? 'Signing in...' : 'Sign in'}
                <ArrowRight size={16} />
              </button>
            </form>
          )}

          {/* TAB 2: CREATE ACCOUNT (Stacked in 1 column on phones) */}
          {tab === 'signup' && (
            <form onSubmit={handleCreateSubmit} className="auth-form-body">
              <div>
                <label className="input-label">Username (required)</label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value.toLowerCase())}
                  placeholder="3 to 20 letters, numbers, or _"
                  className="glass-input auth-input"
                  required
                  autoCapitalize="none"
                  spellCheck="false"
                />
              </div>

              <div>
                <label className="input-label">Display Name (optional)</label>
                <input
                  type="text"
                  value={displayName}
                  onChange={(e) => setDisplayName(e.target.value)}
                  placeholder="e.g. Alex"
                  className="glass-input auth-input"
                />
              </div>

              <div>
                <label className="input-label" style={{ marginBottom: '0.35rem' }}>4-digit PIN (optional)</label>
                <div className="auth-pin-grid">
                  {[0, 1, 2, 3].map(i => (
                    <input
                      key={i}
                      id={`auth-pin-input-${i}`}
                      type="password"
                      inputMode="numeric"
                      pattern="[0-9]*"
                      maxLength={1}
                      value={pinDigits[i]}
                      onChange={(e) => handlePinDigitChange(i, e.target.value)}
                      onKeyDown={(e) => handlePinKeyDown(i, e)}
                      className="glass-input auth-pin-box"
                    />
                  ))}
                </div>
                <p style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '0.35rem', lineHeight: 1.35 }}>
                  A PIN keeps others from accessing your progress. Remember it!
                </p>
              </div>

              {/* Mode Choice: 3 Swatch Cards in 1 Row (SRS 2.0 Part 2 #3) */}
              <div>
                <label className="input-label">Color Theme Mode</label>
                <div className="auth-mode-swatch-row">
                  <button
                    type="button"
                    onClick={() => handleThemeChangeImmediate('light')}
                    className={`auth-swatch-card ${selectedTheme === 'light' ? 'active' : ''}`}
                  >
                    <div className="auth-swatch-circle light-preview" />
                    <span className="auth-swatch-label">Light</span>
                  </button>

                  <button
                    type="button"
                    onClick={() => handleThemeChangeImmediate('evening')}
                    className={`auth-swatch-card ${selectedTheme === 'evening' ? 'active' : ''}`}
                  >
                    <div className="auth-swatch-circle evening-preview" />
                    <span className="auth-swatch-label">Evening</span>
                  </button>

                  <button
                    type="button"
                    onClick={() => handleThemeChangeImmediate('dark')}
                    className={`auth-swatch-card ${selectedTheme === 'dark' ? 'active' : ''}`}
                  >
                    <div className="auth-swatch-circle dark-preview" />
                    <span className="auth-swatch-label">Dark</span>
                  </button>
                </div>
              </div>

              {/* Preferred Language: Java | Python */}
              <div>
                <label className="input-label">Preferred Code Language</label>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
                  {['java', 'python'].map(l => (
                    <button
                      key={l}
                      type="button"
                      onClick={() => setLanguage(l)}
                      style={{
                        padding: '10px 0',
                        minHeight: '44px',
                        borderRadius: 'var(--radius-pill)',
                        border: '1px solid',
                        borderColor: language === l ? 'var(--accent)' : 'var(--glass-border)',
                        background: language === l ? 'var(--accent)' : 'var(--glass-surface)',
                        color: language === l ? 'var(--accent-text)' : 'var(--text-color)',
                        fontWeight: 700,
                        fontSize: '0.85rem',
                        textTransform: 'uppercase'
                      }}
                    >
                      {l}
                    </button>
                  ))}
                </div>
              </div>

              {/* Daily Goal Chips 1 to 5 */}
              <div>
                <label className="input-label">Daily Goal (questions)</label>
                <div style={{ display: 'flex', gap: '6px' }}>
                  {[1, 2, 3, 4, 5].map(n => (
                    <button
                      key={n}
                      type="button"
                      onClick={() => setDailyGoal(n)}
                      style={{
                        flex: 1,
                        padding: '8px 0',
                        minHeight: '44px',
                        borderRadius: 'var(--radius-pill)',
                        border: '1px solid',
                        borderColor: dailyGoal === n ? 'var(--accent)' : 'var(--glass-border)',
                        background: dailyGoal === n ? 'var(--accent)' : 'var(--glass-surface)',
                        color: dailyGoal === n ? 'var(--accent-text)' : 'var(--text-color)',
                        fontWeight: 700,
                        fontSize: '0.9rem'
                      }}
                    >
                      {n}
                    </button>
                  ))}
                </div>
              </div>

              {/* Create account button at bottom */}
              <button
                type="submit"
                disabled={loading}
                className="btn-primary auth-submit-btn"
                style={{ marginTop: '0.5rem' }}
              >
                {loading ? 'Creating account...' : 'Create account'}
                <ArrowRight size={16} />
              </button>
            </form>
          )}

          {/* Under-card honest security note */}
          <div style={{
            fontSize: '0.75rem',
            color: 'var(--text-muted)',
            lineHeight: 1.45,
            borderTop: '1px solid var(--glass-border)',
            paddingTop: '0.65rem'
          }}>
            There is no password recovery. Anyone with your username and PIN can access your roadmap.
          </div>
        </div>

      </div>
    </div>
  );
}

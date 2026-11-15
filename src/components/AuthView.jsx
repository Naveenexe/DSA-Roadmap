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
  const { login, register, theme, setTheme } = useApp();
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
  }, [initialTab, isOpen]);

  if (!isOpen) return null;

  const pinValue = pinDigits.join('');

  const handlePinDigitChange = (index, val) => {
    const digit = val.slice(-1).replace(/\D/g, '');
    const newDigits = [...pinDigits];
    newDigits[index] = digit;
    setPinDigits(newDigits);

    // Auto-advance
    if (digit && index < 3) {
      const nextInput = document.getElementById(`pin-input-${index + 1}`);
      if (nextInput) nextInput.focus();
    }
  };

  const handlePinKeyDown = (index, e) => {
    if (e.key === 'Backspace' && !pinDigits[index] && index > 0) {
      const prevInput = document.getElementById(`pin-input-${index - 1}`);
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
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0, 0, 0, 0.45)',
      backdropFilter: 'blur(16px)',
      WebkitBackdropFilter: 'blur(16px)',
      zIndex: 1000,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '1rem',
      overflowY: 'auto'
    }}>
      <div style={{
        width: '100%',
        maxWidth: '1020px',
        display: 'grid',
        gridTemplateColumns: '1fr 440px',
        gap: '2.5rem',
        alignItems: 'center',
        position: 'relative'
      }} className="auth-two-column-grid">
        
        {/* Close button if modal */}
        {onClose && (
          <button 
            onClick={onClose}
            className="icon-circle-btn"
            style={{ position: 'absolute', top: -14, right: -14, zIndex: 10 }}
            title="Close"
          >
            <X size={18} />
          </button>
        )}

        {/* LEFT HALF: Hero, Tagline, & Floating Preview Cards (Section 5.2) */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }} className="auth-hero-half">
          <ChainlineLogo size={36} showText={true} />

          <div>
            <h1 style={{
              fontSize: '2.4rem',
              fontWeight: 700,
              lineHeight: 1.15,
              letterSpacing: '-0.03em',
              color: 'var(--text-color)',
              marginBottom: '0.65rem'
            }}>
              Solve 300, <span style={{ fontStyle: 'italic', fontWeight: 800 }}>in order.</span>
            </h1>
            <p style={{ fontSize: '1.05rem', color: 'var(--text-muted)', lineHeight: 1.5, maxWidth: '440px' }}>
              A chain of 300 LeetCode questions, each building directly on the last.
            </p>
          </div>

          {/* Three Floating Glass Preview Cards (Progress ring, Streak chip, Question row) */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem', marginTop: '0.5rem', maxWidth: '460px' }}>
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
                  84 of 300 Questions Solved
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

        {/* RIGHT HALF: Glass Card with Segmented Switch (Section 5.2) */}
        <div className="glass-card" style={{
          width: '100%',
          maxWidth: '440px',
          padding: '28px',
          boxShadow: '0 20px 48px rgba(0, 0, 0, 0.25)',
          display: 'flex',
          flexDirection: 'column',
          gap: '1.25rem'
        }}>
          {/* Header Row: Segmented Switch & Theme Swatches */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '0.5rem' }}>
            {/* Segmented Switch: Sign in | Create account */}
            <div style={{
              display: 'inline-flex',
              background: 'var(--progress-track)',
              borderRadius: 'var(--radius-pill)',
              padding: '3px'
            }}>
              <button
                type="button"
                onClick={() => {
                  setTab('signin');
                  setErrorMsg('');
                  setSuggestCreate(false);
                }}
                style={{
                  padding: '6px 14px',
                  borderRadius: 'var(--radius-pill)',
                  fontSize: '0.825rem',
                  fontWeight: 700,
                  background: tab === 'signin' ? 'var(--accent)' : 'transparent',
                  color: tab === 'signin' ? 'var(--accent-text)' : 'var(--text-muted)',
                  transition: 'all 150ms ease'
                }}
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
                style={{
                  padding: '6px 14px',
                  borderRadius: 'var(--radius-pill)',
                  fontSize: '0.825rem',
                  fontWeight: 700,
                  background: tab === 'signup' ? 'var(--accent)' : 'transparent',
                  color: tab === 'signup' ? 'var(--accent-text)' : 'var(--text-muted)',
                  transition: 'all 150ms ease'
                }}
              >
                Create account
              </button>
            </div>

            {/* Three Theme Swatches (Light, Evening, Dark) */}
            <div style={{ display: 'flex', gap: '4px', alignItems: 'center' }} title="Change Mode">
              <button
                type="button"
                onClick={() => handleThemeChangeImmediate('light')}
                style={{
                  width: 24,
                  height: 24,
                  borderRadius: '50%',
                  background: '#EAF3FF',
                  border: '2px solid',
                  borderColor: selectedTheme === 'light' ? 'var(--accent)' : 'transparent',
                  cursor: 'pointer'
                }}
                title="Light (Daylight)"
              />
              <button
                type="button"
                onClick={() => handleThemeChangeImmediate('evening')}
                style={{
                  width: 24,
                  height: 24,
                  borderRadius: '50%',
                  background: '#4A2F6B',
                  border: '2px solid',
                  borderColor: selectedTheme === 'evening' ? 'var(--accent)' : 'transparent',
                  cursor: 'pointer'
                }}
                title="Evening (Dusk)"
              />
              <button
                type="button"
                onClick={() => handleThemeChangeImmediate('dark')}
                style={{
                  width: 24,
                  height: 24,
                  borderRadius: '50%',
                  background: '#090C18',
                  border: '2px solid',
                  borderColor: selectedTheme === 'dark' ? 'var(--accent)' : 'transparent',
                  cursor: 'pointer'
                }}
                title="Dark (Midnight)"
              />
            </div>
          </div>

          {/* Error Message Alert */}
          {errorMsg && (
            <div style={{
              padding: '10px 14px',
              borderRadius: 'var(--radius-inner)',
              background: 'rgba(239, 68, 68, 0.12)',
              border: '1px solid rgba(239, 68, 68, 0.3)',
              color: '#EF4444',
              fontSize: '0.85rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}>
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

          {/* TAB 1: SIGN IN (Never creates an account! Per FR-1) */}
          {tab === 'signin' && (
            <form onSubmit={handleSignInSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div>
                <label className="input-label">Username</label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value.toLowerCase())}
                  placeholder="e.g. codemaster_99"
                  className="glass-input"
                  required
                  autoFocus
                />
              </div>

              {/* PIN boxes shown only if server requires PIN or previously indicated */}
              {pinRequired && (
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
                    <label className="input-label" style={{ margin: 0 }}>4-digit PIN</label>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Enter your 4 numbers</span>
                  </div>
                  <div style={{ display: 'flex', gap: '8px', justifyContent: 'center' }}>
                    {[0, 1, 2, 3].map(i => (
                      <input
                        key={i}
                        id={`pin-input-${i}`}
                        type="password"
                        maxLength={1}
                        value={pinDigits[i]}
                        onChange={(e) => handlePinDigitChange(i, e.target.value)}
                        onKeyDown={(e) => handlePinKeyDown(i, e)}
                        className="glass-input"
                        style={{ width: '48px', height: '48px', textAlign: 'center', fontSize: '1.25rem', padding: 0, fontWeight: 700 }}
                        required={pinRequired}
                      />
                    ))}
                  </div>
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="btn-primary"
                style={{ width: '100%', marginTop: '0.35rem' }}
              >
                {loading ? 'Signing in...' : 'Sign in'}
                <ArrowRight size={15} />
              </button>
            </form>
          )}

          {/* TAB 2: CREATE ACCOUNT (Per Section 5.2 & FR-1a) */}
          {tab === 'signup' && (
            <form onSubmit={handleCreateSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '0.9rem' }}>
              <div>
                <label className="input-label">Username (required)</label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value.toLowerCase())}
                  placeholder="3 to 20 letters, numbers, or _"
                  className="glass-input"
                  required
                />
              </div>

              <div>
                <label className="input-label">Display Name (optional)</label>
                <input
                  type="text"
                  value={displayName}
                  onChange={(e) => setDisplayName(e.target.value)}
                  placeholder="e.g. Alex"
                  className="glass-input"
                />
              </div>

              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.35rem' }}>
                  <label className="input-label" style={{ margin: 0 }}>4-digit PIN (optional)</label>
                </div>
                <div style={{ display: 'flex', gap: '8px', justifyContent: 'center' }}>
                  {[0, 1, 2, 3].map(i => (
                    <input
                      key={i}
                      id={`pin-input-${i}`}
                      type="password"
                      maxLength={1}
                      value={pinDigits[i]}
                      onChange={(e) => handlePinDigitChange(i, e.target.value)}
                      onKeyDown={(e) => handlePinKeyDown(i, e)}
                      className="glass-input"
                      style={{ width: '44px', height: '44px', textAlign: 'center', fontSize: '1.2rem', padding: 0, fontWeight: 700 }}
                    />
                  ))}
                </div>
                <p style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '0.3rem', lineHeight: 1.35 }}>
                  A PIN keeps others from opening your page. You cannot recover it, so remember it.
                </p>
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
                        padding: '6px 0',
                        borderRadius: 'var(--radius-pill)',
                        border: '1px solid',
                        borderColor: dailyGoal === n ? 'var(--accent)' : 'var(--glass-border)',
                        background: dailyGoal === n ? 'var(--accent)' : 'var(--glass-surface)',
                        color: dailyGoal === n ? 'var(--accent-text)' : 'var(--text-color)',
                        fontWeight: 700,
                        fontSize: '0.85rem'
                      }}
                    >
                      {n}
                    </button>
                  ))}
                </div>
              </div>

              {/* Preferred Language */}
              <div>
                <label className="input-label">Preferred Code Language</label>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
                  {['java', 'python'].map(l => (
                    <button
                      key={l}
                      type="button"
                      onClick={() => setLanguage(l)}
                      style={{
                        padding: '7px 0',
                        borderRadius: 'var(--radius-pill)',
                        border: '1px solid',
                        borderColor: language === l ? 'var(--accent)' : 'var(--glass-border)',
                        background: language === l ? 'var(--accent)' : 'var(--glass-surface)',
                        color: language === l ? 'var(--accent-text)' : 'var(--text-color)',
                        fontWeight: 700,
                        fontSize: '0.825rem',
                        textTransform: 'uppercase'
                      }}
                    >
                      {l}
                    </button>
                  ))}
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="btn-primary"
                style={{ width: '100%', marginTop: '0.25rem' }}
              >
                {loading ? 'Creating...' : 'Create account'}
                <ArrowRight size={15} />
              </button>
            </form>
          )}

          {/* Under-card honest security note (Section 5.2) */}
          <div style={{
            fontSize: '0.75rem',
            color: 'var(--text-muted)',
            lineHeight: 1.45,
            borderTop: '1px solid var(--glass-border)',
            paddingTop: '0.75rem'
          }}>
            There is no email or password. Anyone who knows your username (and PIN, if you set one) can open your page.
          </div>
        </div>

      </div>
    </div>
  );
}

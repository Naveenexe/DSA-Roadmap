import React, { useState, useEffect, useMemo } from 'react';
import { useApp } from '../context/AppContext';
import { 
  Settings as SettingsIcon, 
  Download, 
  Upload, 
  Trash2, 
  LogOut, 
  Sun, 
  Sunset, 
  Moon, 
  Code2, 
  Target, 
  ShieldAlert,
  User,
  Check,
  Plus,
  Minus,
  Sparkles,
  AlertCircle,
  X,
  Calendar,
  Briefcase
} from 'lucide-react';

export default function Settings({ onOpenAuth }) {
  const { 
    user, 
    updateSettings, 
    logout, 
    deleteAccount, 
    exportData, 
    importData, 
    theme,
    setTheme,
    language,
    updateLanguage,
    showToast,
    interviewPlan,
    updateInterviewPlan,
    clearInterviewPlan,
    companies
  } = useApp();

  const [displayName, setDisplayName] = useState(user?.display_name || '');
  const [dailyGoal, setDailyGoal] = useState(user?.daily_goal || 2);
  const [savingProfile, setSavingProfile] = useState(false);

  // Interview Plan state (SRS 3.0 Section 8.1)
  const [planDate, setPlanDate] = useState(interviewPlan?.date || '');
  const [planCompany, setPlanCompany] = useState(interviewPlan?.company || '');
  const [savingPlan, setSavingPlan] = useState(false);

  useEffect(() => {
    setPlanDate(interviewPlan?.date || '');
    setPlanCompany(interviewPlan?.company || '');
  }, [interviewPlan]);

  const todayDateStr = new Date().toISOString().split('T')[0];

  const isPlanPast = useMemo(() => {
    if (!interviewPlan?.date) return false;
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const target = new Date(interviewPlan.date + 'T00:00:00');
    target.setHours(0, 0, 0, 0);
    return target < today;
  }, [interviewPlan]);

  const handleSavePlan = async (e) => {
    e.preventDefault();
    if (!planDate) {
      showToast('Please select a target interview date', 'error');
      return;
    }
    setSavingPlan(true);
    try {
      await updateInterviewPlan(planDate, planCompany || null);
      showToast('Interview plan saved', 'success');
    } catch (_) {
      showToast('Failed to save interview plan', 'error');
    } finally {
      setSavingPlan(false);
    }
  };

  const handleClearPlan = async () => {
    try {
      await clearInterviewPlan();
      setPlanDate('');
      setPlanCompany('');
      showToast('Interview plan cleared', 'info');
    } catch (_) {
      showToast('Failed to clear plan', 'error');
    }
  };

  // Delete confirmation bottom sheet/modal
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [typedConfirm, setTypedConfirm] = useState('');
  const [deleteLoading, setDeleteLoading] = useState(false);

  const currentTheme = theme || 'light';
  const currentLang = language || 'java';

  const handleProfileSave = async (e) => {
    e.preventDefault();
    if (!user) return;
    setSavingProfile(true);
    try {
      await updateSettings({ displayName: displayName.trim() || null });
      showToast('Profile updated successfully', 'success');
    } catch (err) {
      showToast('Failed to update profile', 'error');
    } finally {
      setSavingProfile(false);
    }
  };

  const handleGoalStep = async (step) => {
    const next = Math.max(1, Math.min(10, dailyGoal + step));
    setDailyGoal(next);
    if (user) {
      await updateSettings({ dailyGoal: next });
    }
  };

  const handleThemeChange = (newTheme) => {
    setTheme(newTheme);
    if (user) {
      updateSettings({ theme: newTheme });
    }
  };

  const handleLanguageChange = (lang) => {
    updateLanguage(lang);
  };

  const handleFileImport = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      const content = event.target?.result;
      if (typeof content === 'string') {
        importData(content);
      }
    };
    reader.readAsText(file);
    e.target.value = '';
  };

  const handleDeleteAccount = async () => {
    if (!user) return;
    if (typedConfirm.trim().toLowerCase() !== user.username.toLowerCase()) {
      showToast('Typed username does not match', 'error');
      return;
    }

    setDeleteLoading(true);
    try {
      await deleteAccount();
      setShowDeleteModal(false);
      showToast('Your account and all data have been deleted', 'info');
    } catch (err) {
      showToast('Failed to delete account', 'error');
    } finally {
      setDeleteLoading(false);
    }
  };

  return (
    <div className="settings-page-root" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', maxWidth: '780px', margin: '0 auto', width: '100%' }}>
      {/* Header */}
      <div>
        <h1 style={{ 
          fontSize: '1.85rem', 
          fontWeight: 800, 
          letterSpacing: '-0.03em', 
          color: 'var(--text-color)',
          lineHeight: 1.2
        }}>
          Settings
        </h1>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
          Personalize your learning experience and manage your data.
        </p>
      </div>

      {/* 1. Profile Glass Card */}
      <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <h2 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-color)' }}>
          Profile
        </h2>

        {user ? (
          <form onSubmit={handleProfileSave} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem' }}>
              <div>
                <label className="input-label" style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.35rem' }}>
                  Username
                </label>
                <input
                  type="text"
                  value={user.username}
                  disabled
                  className="glass-input"
                  style={{ opacity: 0.7, cursor: 'not-allowed', fontFamily: 'var(--font-mono)', fontSize: '16px', minHeight: '44px' }}
                />
              </div>

              <div>
                <label className="input-label" style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.35rem' }}>
                  Display Name
                </label>
                <input
                  type="text"
                  value={displayName}
                  onChange={(e) => setDisplayName(e.target.value)}
                  placeholder="e.g. Alex"
                  maxLength={40}
                  className="glass-input"
                  style={{ fontSize: '16px', minHeight: '44px' }}
                />
              </div>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.75rem', paddingTop: '0.5rem' }}>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                {user.has_pin ? (
                  <span style={{ color: '#10B981', fontWeight: 600 }}>✓ 4-digit PIN configured</span>
                ) : (
                  <span>No PIN configured (open access by username)</span>
                )}
              </div>

              <button
                type="submit"
                disabled={savingProfile || displayName === (user.display_name || '')}
                className="btn-primary"
                style={{ padding: '0.5rem 1.25rem', fontSize: '0.85rem', minHeight: '44px' }}
              >
                {savingProfile ? 'Saving...' : 'Save Profile'}
              </button>
            </div>
          </form>
        ) : (
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem', padding: '0.5rem 0' }}>
            <div>
              <div style={{ fontWeight: 600, fontSize: '0.95rem', color: 'var(--text-color)' }}>Guest Mode</div>
              <div style={{ fontSize: '0.825rem', color: 'var(--text-muted)' }}>
                Sign in with a username to sync your progress to Supabase across devices.
              </div>
            </div>
            <button onClick={onOpenAuth} className="btn-primary" style={{ padding: '0.6rem 1.35rem', fontSize: '0.875rem', minHeight: '44px' }}>
              Sign In / Create Account
            </button>
          </div>
        )}
      </div>

      {/* 2. Daily Goal Stepper 1 to 10 */}
      <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem' }}>
          <div>
            <h2 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-color)' }}>
              Daily Goal
            </h2>
            <p style={{ fontSize: '0.825rem', color: 'var(--text-muted)' }}>
              Number of questions to solve each day (1 to 10).
            </p>
          </div>

          {/* Stepper Controls */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <button
              onClick={() => handleGoalStep(-1)}
              disabled={dailyGoal <= 1}
              className="icon-circle-btn"
              style={{ width: 44, height: 44, minWidth: 44, minHeight: 44, opacity: dailyGoal <= 1 ? 0.4 : 1 }}
              title="Decrease daily goal"
              aria-label="Decrease daily goal"
            >
              <Minus size={16} />
            </button>

            <div style={{
              width: 56,
              height: 44,
              borderRadius: 'var(--radius-inner)',
              background: 'var(--glass-surface)',
              border: '1px solid var(--glass-border)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontFamily: 'var(--font-mono)',
              fontSize: '1.25rem',
              fontWeight: 800,
              color: 'var(--text-color)'
            }}>
              {dailyGoal}
            </div>

            <button
              onClick={() => handleGoalStep(1)}
              disabled={dailyGoal >= 10}
              className="icon-circle-btn"
              style={{ width: 44, height: 44, minWidth: 44, minHeight: 44, opacity: dailyGoal >= 10 ? 0.4 : 1 }}
              title="Increase daily goal"
              aria-label="Increase daily goal"
            >
              <Plus size={16} />
            </button>
          </div>
        </div>
      </div>

      {/* 2b. Interview Date Plan (SRS 3.0 Section 8.1) */}
      <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Calendar size={20} color="var(--accent)" />
            <div>
              <h2 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-color)', margin: 0 }}>
                Interview Plan
              </h2>
              <p style={{ fontSize: '0.825rem', color: 'var(--text-muted)', margin: '2px 0 0 0' }}>
                Set your target interview date and optional target company.
              </p>
            </div>
          </div>
          {interviewPlan?.date && (
            <span style={{
              fontSize: '0.78rem',
              fontWeight: 700,
              padding: '4px 10px',
              borderRadius: 'var(--radius-pill)',
              background: isPlanPast ? 'rgba(239, 68, 68, 0.15)' : 'var(--accent-soft)',
              color: isPlanPast ? '#EF4444' : 'var(--accent)'
            }}>
              {isPlanPast ? 'Date Passed' : 'Plan Active'}
            </span>
          )}
        </div>

        {isPlanPast && (
          <div style={{
            padding: '12px 16px',
            borderRadius: 'var(--radius-inner)',
            background: 'rgba(239, 68, 68, 0.12)',
            border: '1px solid rgba(239, 68, 68, 0.35)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: '8px'
          }}>
            <div style={{ fontSize: '0.85rem', color: '#EF4444', fontWeight: 600 }}>
              Your interview date has passed.
            </div>
            <button
              type="button"
              onClick={handleClearPlan}
              className="btn-secondary"
              style={{ padding: '4px 12px', minHeight: '36px', height: '36px', fontSize: '0.8rem' }}
            >
              Clear plan
            </button>
          </div>
        )}

        <form onSubmit={handleSavePlan} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem' }}>
            {/* Target Date */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <label style={{ fontSize: '0.825rem', fontWeight: 600, color: 'var(--text-color)' }}>
                Interview Date (today or later)
              </label>
              <input
                type="date"
                min={todayDateStr}
                value={planDate}
                onChange={(e) => setPlanDate(e.target.value)}
                className="glass-input"
                style={{ width: '100%', height: '44px', fontSize: '15px', borderRadius: 'var(--radius-inner)', padding: '0 12px' }}
                required
              />
            </div>

            {/* Target Company (Optional) */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <label style={{ fontSize: '0.825rem', fontWeight: 600, color: 'var(--text-color)' }}>
                Target Company (optional)
              </label>
              <select
                value={planCompany}
                onChange={(e) => setPlanCompany(e.target.value)}
                className="glass-input"
                style={{ width: '100%', height: '44px', fontSize: '15px', borderRadius: 'var(--radius-inner)', padding: '0 12px' }}
              >
                <option value="">All companies (General roadmap)</option>
                {companies.map(c => (
                  <option key={c.slug} value={c.slug}>
                    {c.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', alignItems: 'center' }}>
            <button
              type="submit"
              disabled={savingPlan || !planDate}
              className="btn-primary"
              style={{ minHeight: '44px', padding: '0 20px', fontSize: '0.875rem' }}
            >
              {savingPlan ? 'Saving...' : 'Save Plan'}
            </button>

            {interviewPlan?.date && (
              <button
                type="button"
                onClick={handleClearPlan}
                className="btn-secondary"
                style={{ minHeight: '44px', padding: '0 16px', fontSize: '0.875rem' }}
              >
                Clear Plan
              </button>
            )}
          </div>
        </form>
      </div>

      {/* 3. Language Selection (Java | Python is a two-part control per Part 2 #8) */}
      <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
        <div>
          <h2 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-color)' }}>
            Preferred Language
          </h2>
          <p style={{ fontSize: '0.825rem', color: 'var(--text-muted)' }}>
            Default syntax displayed across question solutions and code views.
          </p>
        </div>

        {/* Two-part control for Java | Python */}
        <div className="settings-lang-control" style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: '4px',
          background: 'var(--progress-track)',
          padding: '4px',
          borderRadius: 'var(--radius-pill)',
          maxWidth: '380px',
          width: '100%'
        }}>
          <button
            type="button"
            onClick={() => handleLanguageChange('java')}
            style={{
              padding: '10px 16px',
              minHeight: '44px',
              borderRadius: 'var(--radius-pill)',
              border: 'none',
              background: currentLang === 'java' ? 'var(--accent)' : 'transparent',
              color: currentLang === 'java' ? 'var(--accent-text)' : 'var(--text-color)',
              fontWeight: 700,
              fontSize: '0.88rem',
              cursor: 'pointer',
              transition: 'all 150ms ease',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            Java
          </button>
          <button
            type="button"
            onClick={() => handleLanguageChange('python')}
            style={{
              padding: '10px 16px',
              minHeight: '44px',
              borderRadius: 'var(--radius-pill)',
              border: 'none',
              background: currentLang === 'python' ? 'var(--accent)' : 'transparent',
              color: currentLang === 'python' ? 'var(--accent-text)' : 'var(--text-color)',
              fontWeight: 700,
              fontSize: '0.88rem',
              cursor: 'pointer',
              transition: 'all 150ms ease',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            Python
          </button>
        </div>
      </div>

      {/* 4. Mode Swatch Cards: Light, Evening, Dark in one row (Part 2 #8) */}
      <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <div>
          <h2 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-color)' }}>
            Mode
          </h2>
          <p style={{ fontSize: '0.825rem', color: 'var(--text-muted)' }}>
            Choose an appearance theme. Changes apply across the entire app immediately.
          </p>
        </div>

        {/* Three Swatch Cards in one row */}
        <div className="settings-mode-swatch-row" style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '12px'
        }}>
          {/* Swatch 1: Light (Daylight) */}
          <div
            onClick={() => handleThemeChange('light')}
            className="glass-card-interactive settings-swatch-card"
            style={{
              padding: '12px',
              borderRadius: 'var(--radius-inner)',
              cursor: 'pointer',
              border: '2px solid',
              borderColor: currentTheme === 'light' ? 'var(--accent)' : 'var(--glass-border)',
              background: 'var(--glass-surface)',
              position: 'relative',
              minHeight: '44px'
            }}
          >
            <div style={{
              height: 64,
              borderRadius: '10px',
              background: 'linear-gradient(135deg, #BFE3FF 0%, #EAF3FF 100%)',
              padding: '6px',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              marginBottom: '8px',
              border: '1px solid rgba(255, 255, 255, 0.7)'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ width: 22, height: 5, borderRadius: 3, background: '#1E1B4B', opacity: 0.7 }} />
                <span style={{ width: 7, height: 7, borderRadius: '50%', background: '#1E1B4B' }} />
              </div>
              <div style={{
                background: 'rgba(255, 255, 255, 0.65)',
                borderRadius: '5px',
                padding: '3px 5px',
                display: 'flex',
                alignItems: 'center',
                gap: '4px'
              }}>
                <span style={{ width: 10, height: 3, borderRadius: 2, background: '#4338CA' }} />
                <span style={{ width: 16, height: 3, borderRadius: 2, background: '#94A3B8' }} />
              </div>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div>
                <div style={{ fontWeight: 700, fontSize: '0.85rem', color: 'var(--text-color)' }}>Light</div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Daylight</div>
              </div>
              {currentTheme === 'light' && (
                <div style={{ width: 18, height: 18, borderRadius: '50%', background: 'var(--accent)', color: 'var(--accent-text)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Check size={11} strokeWidth={3} />
                </div>
              )}
            </div>
          </div>

          {/* Swatch 2: Evening (Dusk) */}
          <div
            onClick={() => handleThemeChange('evening')}
            className="glass-card-interactive settings-swatch-card"
            style={{
              padding: '12px',
              borderRadius: 'var(--radius-inner)',
              cursor: 'pointer',
              border: '2px solid',
              borderColor: currentTheme === 'evening' ? 'var(--accent)' : 'var(--glass-border)',
              background: 'var(--glass-surface)',
              position: 'relative',
              minHeight: '44px'
            }}
          >
            <div style={{
              height: 64,
              borderRadius: '10px',
              background: 'linear-gradient(135deg, #1C1743 0%, #4A2F6B 100%)',
              padding: '6px',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              marginBottom: '8px',
              border: '1px solid rgba(255, 255, 255, 0.15)'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ width: 22, height: 5, borderRadius: 3, background: '#F3F4F6', opacity: 0.8 }} />
                <span style={{ width: 7, height: 7, borderRadius: '50%', background: '#FFC38A' }} />
              </div>
              <div style={{
                background: 'rgba(255, 255, 255, 0.12)',
                borderRadius: '5px',
                padding: '3px 5px',
                display: 'flex',
                alignItems: 'center',
                gap: '4px'
              }}>
                <span style={{ width: 10, height: 3, borderRadius: 2, background: '#FFC38A' }} />
                <span style={{ width: 16, height: 3, borderRadius: 2, background: '#8B6CFF' }} />
              </div>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div>
                <div style={{ fontWeight: 700, fontSize: '0.85rem', color: 'var(--text-color)' }}>Evening</div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Dusk</div>
              </div>
              {currentTheme === 'evening' && (
                <div style={{ width: 18, height: 18, borderRadius: '50%', background: 'var(--accent)', color: 'var(--accent-text)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Check size={11} strokeWidth={3} />
                </div>
              )}
            </div>
          </div>

          {/* Swatch 3: Dark (Midnight) */}
          <div
            onClick={() => handleThemeChange('dark')}
            className="glass-card-interactive settings-swatch-card"
            style={{
              padding: '12px',
              borderRadius: 'var(--radius-inner)',
              cursor: 'pointer',
              border: '2px solid',
              borderColor: currentTheme === 'dark' ? 'var(--accent)' : 'var(--glass-border)',
              background: 'var(--glass-surface)',
              position: 'relative',
              minHeight: '44px'
            }}
          >
            <div style={{
              height: 64,
              borderRadius: '10px',
              background: 'linear-gradient(135deg, #090C18 0%, #171B34 100%)',
              padding: '6px',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              marginBottom: '8px',
              border: '1px solid rgba(255, 255, 255, 0.12)'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ width: 22, height: 5, borderRadius: 3, background: '#E0E7FF', opacity: 0.9 }} />
                <span style={{ width: 7, height: 7, borderRadius: '50%', background: '#6366F1' }} />
              </div>
              <div style={{
                background: 'rgba(255, 255, 255, 0.08)',
                borderRadius: '5px',
                padding: '3px 5px',
                display: 'flex',
                alignItems: 'center',
                gap: '4px'
              }}>
                <span style={{ width: 10, height: 3, borderRadius: 2, background: '#818CF8' }} />
                <span style={{ width: 16, height: 3, borderRadius: 2, background: '#475569' }} />
              </div>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div>
                <div style={{ fontWeight: 700, fontSize: '0.85rem', color: 'var(--text-color)' }}>Dark</div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Midnight</div>
              </div>
              {currentTheme === 'dark' && (
                <div style={{ width: 18, height: 18, borderRadius: '50%', background: 'var(--accent)', color: 'var(--accent-text)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Check size={11} strokeWidth={3} />
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* 5. Data Management (Export & Import) */}
      <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <div>
          <h2 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-color)' }}>
            Data Management
          </h2>
          <p style={{ fontSize: '0.825rem', color: 'var(--text-muted)' }}>
            Export or import your complete roadmap progress as a portable JSON file.
          </p>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
          <button
            onClick={exportData}
            className="btn-secondary"
            style={{ padding: '0.55rem 1.15rem', fontSize: '0.85rem', minHeight: '44px' }}
          >
            <Download size={16} />
            <span>Export Progress (JSON)</span>
          </button>

          <label
            className="btn-secondary"
            style={{ padding: '0.55rem 1.15rem', fontSize: '0.85rem', cursor: 'pointer', minHeight: '44px' }}
          >
            <Upload size={16} />
            <span>Import Backup (JSON)</span>
            <input
              type="file"
              accept=".json"
              onChange={handleFileImport}
              style={{ display: 'none' }}
            />
          </label>
        </div>
      </div>

      {/* 6. Account Actions: Log Out & Delete My Data (Full-width button in danger colour per Part 2 #8) */}
      {user && (
        <div className="glass-card" style={{
          padding: '24px',
          display: 'flex',
          flexDirection: 'column',
          gap: '1.25rem',
          border: '1px solid rgba(239, 68, 68, 0.35)'
        }}>
          <div>
            <h2 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#EF4444' }}>
              Account Actions
            </h2>
            <p style={{ fontSize: '0.825rem', color: 'var(--text-muted)' }}>
              Manage session and permanent account deletion.
            </p>
          </div>

          {/* Log Out */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.75rem' }}>
            <div>
              <div style={{ fontWeight: 600, fontSize: '0.9rem', color: 'var(--text-color)' }}>Log out</div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Clear the active session from this device.</div>
            </div>
            <button
              onClick={logout}
              className="btn-secondary"
              style={{ padding: '0.5rem 1.25rem', fontSize: '0.85rem', minHeight: '44px' }}
            >
              <LogOut size={16} />
              <span>Log out</span>
            </button>
          </div>

          <div style={{ height: 1, background: 'var(--glass-border)' }} />

          {/* Delete My Data: Full-width button in danger colour (Part 2 #8) */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            <div>
              <div style={{ fontWeight: 700, fontSize: '0.95rem', color: '#EF4444' }}>Delete my data</div>
              <div style={{ fontSize: '0.825rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                Permanently delete account, progress, reviews, and activity from Supabase.
              </div>
            </div>
            
            <button
              type="button"
              onClick={() => {
                setTypedConfirm('');
                setShowDeleteModal(true);
              }}
              style={{
                width: '100%',
                minHeight: '48px',
                padding: '0.75rem 1.25rem',
                fontSize: '0.925rem',
                fontWeight: 700,
                borderRadius: 'var(--radius-pill)',
                border: '1px solid #EF4444',
                background: 'rgba(239, 68, 68, 0.15)',
                color: '#EF4444',
                cursor: 'pointer',
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '0.5rem',
                transition: 'background 150ms ease'
              }}
            >
              <Trash2 size={16} />
              <span>Delete my data</span>
            </button>
          </div>
        </div>
      )}

      {/* Delete Confirmation: Opens as bottom sheet on mobile, modal on desktop (Part 2 #8) */}
      {showDeleteModal && (
        <div className="bottom-sheet-overlay" onClick={() => setShowDeleteModal(false)}>
          <div 
            className="delete-sheet-content glass-card"
            onClick={(e) => e.stopPropagation()}
            style={{ border: '1px solid #EF4444' }}
          >
            <div className="bottom-sheet-handle" />
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#EF4444' }}>
                <ShieldAlert size={22} />
                <h3 style={{ fontSize: '1.2rem', fontWeight: 800 }}>Confirm Deletion</h3>
              </div>
              <button
                type="button"
                onClick={() => setShowDeleteModal(false)}
                className="icon-circle-btn"
                style={{ width: 36, height: 36, minWidth: 36, minHeight: 36 }}
              >
                <X size={16} />
              </button>
            </div>

            <p style={{ fontSize: '0.875rem', color: 'var(--text-color)', lineHeight: 1.55 }}>
              This will permanently delete your account <strong>{user?.username}</strong>, along with all question progress, review records, and notes. This action cannot be reversed.
            </p>

            <div>
              <label className="input-label" style={{ fontSize: '0.825rem', color: 'var(--text-muted)', marginBottom: '0.45rem' }}>
                Type your username <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--text-color)', fontWeight: 700 }}>{user?.username}</span> to confirm:
              </label>
              <input
                type="text"
                value={typedConfirm}
                onChange={(e) => setTypedConfirm(e.target.value)}
                placeholder={user?.username}
                className="glass-input"
                style={{ fontFamily: 'var(--font-mono)', fontSize: '16px', minHeight: '44px' }}
                autoFocus
              />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', marginTop: '0.5rem' }}>
              <button
                type="button"
                onClick={() => setShowDeleteModal(false)}
                className="btn-secondary"
                style={{ width: '100%', minHeight: '48px', fontSize: '0.88rem', justifyContent: 'center' }}
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleDeleteAccount}
                disabled={deleteLoading || typedConfirm.trim().toLowerCase() !== user?.username.toLowerCase()}
                style={{
                  width: '100%',
                  minHeight: '48px',
                  fontSize: '0.88rem',
                  fontWeight: 700,
                  borderRadius: 'var(--radius-pill)',
                  border: 'none',
                  background: '#EF4444',
                  color: '#FFFFFF',
                  cursor: deleteLoading || typedConfirm.trim().toLowerCase() !== user?.username.toLowerCase() ? 'not-allowed' : 'pointer',
                  opacity: deleteLoading || typedConfirm.trim().toLowerCase() !== user?.username.toLowerCase() ? 0.45 : 1,
                  display: 'inline-flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '0.45rem'
                }}
              >
                {deleteLoading ? 'Deleting...' : 'Permanently Delete'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

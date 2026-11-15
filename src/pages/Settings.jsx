import React, { useState } from 'react';
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
  AlertCircle
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
    showToast 
  } = useApp();

  const [displayName, setDisplayName] = useState(user?.display_name || '');
  const [dailyGoal, setDailyGoal] = useState(user?.daily_goal || 2);
  const [savingProfile, setSavingProfile] = useState(false);

  // Delete confirmation modal
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
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', maxWidth: '780px', margin: '0 auto', width: '100%' }}>
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

      {/* 1. Profile Glass Card (Section 5.7) */}
      <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <h2 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-color)' }}>
          Profile
        </h2>

        {user ? (
          <form onSubmit={handleProfileSave} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.35rem' }}>
                  Username
                </label>
                <input
                  type="text"
                  value={user.username}
                  disabled
                  className="input"
                  style={{ opacity: 0.7, cursor: 'not-allowed', fontFamily: 'var(--font-mono)' }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.35rem' }}>
                  Display Name
                </label>
                <input
                  type="text"
                  value={displayName}
                  onChange={(e) => setDisplayName(e.target.value)}
                  placeholder="e.g. Alex"
                  maxLength={40}
                  className="input"
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
                style={{ padding: '0.45rem 1.15rem', fontSize: '0.825rem' }}
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
            <button onClick={onOpenAuth} className="btn-primary" style={{ padding: '0.5rem 1.25rem', fontSize: '0.85rem' }}>
              Sign In / Create Account
            </button>
          </div>
        )}
      </div>

      {/* 2. Daily Goal Stepper 1 to 10 (Section 5.7) */}
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
              style={{ width: 38, height: 38, opacity: dailyGoal <= 1 ? 0.4 : 1 }}
              title="Decrease daily goal"
            >
              <Minus size={16} />
            </button>

            <div style={{
              width: 54,
              height: 38,
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
              style={{ width: 38, height: 38, opacity: dailyGoal >= 10 ? 0.4 : 1 }}
              title="Increase daily goal"
            >
              <Plus size={16} />
            </button>
          </div>
        </div>
      </div>

      {/* 3. Language Selection (Java or Python) (Section 5.7) */}
      <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
        <div>
          <h2 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-color)' }}>
            Preferred Language
          </h2>
          <p style={{ fontSize: '0.825rem', color: 'var(--text-muted)' }}>
            Default syntax displayed across question solutions and code views.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem', maxWidth: '360px' }}>
          <button
            onClick={() => handleLanguageChange('java')}
            className={currentLang === 'java' ? 'btn-primary' : 'btn-secondary'}
            style={{ padding: '0.65rem 1rem', fontSize: '0.875rem' }}
          >
            Java
          </button>
          <button
            onClick={() => handleLanguageChange('python')}
            className={currentLang === 'python' ? 'btn-primary' : 'btn-secondary'}
            style={{ padding: '0.65rem 1rem', fontSize: '0.875rem' }}
          >
            Python
          </button>
        </div>
      </div>

      {/* 4. Mode Swatch Cards: Light, Evening, Dark (Section 5.7) */}
      <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <div>
          <h2 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-color)' }}>
            Mode
          </h2>
          <p style={{ fontSize: '0.825rem', color: 'var(--text-muted)' }}>
            Choose an appearance theme. Changes apply across the entire app immediately.
          </p>
        </div>

        {/* Three Swatch Cards (Section 5.7) */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
          gap: '1rem'
        }}>
          {/* Swatch 1: Light (Daylight) */}
          <div
            onClick={() => handleThemeChange('light')}
            className="glass-card-interactive"
            style={{
              padding: '14px',
              borderRadius: 'var(--radius-inner)',
              cursor: 'pointer',
              border: '2px solid',
              borderColor: currentTheme === 'light' ? 'var(--accent)' : 'var(--glass-border)',
              background: 'var(--glass-surface)',
              position: 'relative'
            }}
          >
            {/* Miniature Preview Box */}
            <div style={{
              height: 72,
              borderRadius: '12px',
              background: 'linear-gradient(135deg, #BFE3FF 0%, #EAF3FF 100%)',
              padding: '8px',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              marginBottom: '10px',
              border: '1px solid rgba(255, 255, 255, 0.7)'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ width: 28, height: 6, borderRadius: 3, background: '#1E1B4B', opacity: 0.7 }} />
                <span style={{ width: 8, height: 8, borderRadius: '50%', background: '#1E1B4B' }} />
              </div>
              <div style={{
                background: 'rgba(255, 255, 255, 0.65)',
                borderRadius: '6px',
                padding: '4px 6px',
                display: 'flex',
                alignItems: 'center',
                gap: '4px'
              }}>
                <span style={{ width: 12, height: 4, borderRadius: 2, background: '#4338CA' }} />
                <span style={{ width: 20, height: 4, borderRadius: 2, background: '#94A3B8' }} />
              </div>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div>
                <div style={{ fontWeight: 700, fontSize: '0.875rem', color: 'var(--text-color)' }}>Light</div>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Daylight</div>
              </div>
              {currentTheme === 'light' && (
                <div style={{ width: 20, height: 20, borderRadius: '50%', background: 'var(--accent)', color: 'var(--accent-text)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Check size={12} strokeWidth={3} />
                </div>
              )}
            </div>
          </div>

          {/* Swatch 2: Evening (Dusk) */}
          <div
            onClick={() => handleThemeChange('evening')}
            className="glass-card-interactive"
            style={{
              padding: '14px',
              borderRadius: 'var(--radius-inner)',
              cursor: 'pointer',
              border: '2px solid',
              borderColor: currentTheme === 'evening' ? 'var(--accent)' : 'var(--glass-border)',
              background: 'var(--glass-surface)',
              position: 'relative'
            }}
          >
            {/* Miniature Preview Box */}
            <div style={{
              height: 72,
              borderRadius: '12px',
              background: 'linear-gradient(135deg, #1C1743 0%, #4A2F6B 100%)',
              padding: '8px',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              marginBottom: '10px',
              border: '1px solid rgba(255, 255, 255, 0.15)'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ width: 28, height: 6, borderRadius: 3, background: '#F3F4F6', opacity: 0.8 }} />
                <span style={{ width: 8, height: 8, borderRadius: '50%', background: '#FFC38A' }} />
              </div>
              <div style={{
                background: 'rgba(255, 255, 255, 0.12)',
                borderRadius: '6px',
                padding: '4px 6px',
                display: 'flex',
                alignItems: 'center',
                gap: '4px'
              }}>
                <span style={{ width: 12, height: 4, borderRadius: 2, background: '#FFC38A' }} />
                <span style={{ width: 20, height: 4, borderRadius: 2, background: 'rgba(255, 255, 255, 0.3)' }} />
              </div>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div>
                <div style={{ fontWeight: 700, fontSize: '0.875rem', color: 'var(--text-color)' }}>Evening</div>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Dusk</div>
              </div>
              {currentTheme === 'evening' && (
                <div style={{ width: 20, height: 20, borderRadius: '50%', background: 'var(--accent)', color: 'var(--accent-text)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Check size={12} strokeWidth={3} />
                </div>
              )}
            </div>
          </div>

          {/* Swatch 3: Dark (Midnight) */}
          <div
            onClick={() => handleThemeChange('dark')}
            className="glass-card-interactive"
            style={{
              padding: '14px',
              borderRadius: 'var(--radius-inner)',
              cursor: 'pointer',
              border: '2px solid',
              borderColor: currentTheme === 'dark' ? 'var(--accent)' : 'var(--glass-border)',
              background: 'var(--glass-surface)',
              position: 'relative'
            }}
          >
            {/* Miniature Preview Box */}
            <div style={{
              height: 72,
              borderRadius: '12px',
              background: 'linear-gradient(135deg, #090C18 0%, #0F1428 100%)',
              padding: '8px',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              marginBottom: '10px',
              border: '1px solid rgba(255, 255, 255, 0.12)'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ width: 28, height: 6, borderRadius: 3, background: '#E8EAF6', opacity: 0.8 }} />
                <span style={{ width: 8, height: 8, borderRadius: '50%', background: '#A5A6FF' }} />
              </div>
              <div style={{
                background: 'rgba(255, 255, 255, 0.08)',
                borderRadius: '6px',
                padding: '4px 6px',
                display: 'flex',
                alignItems: 'center',
                gap: '4px'
              }}>
                <span style={{ width: 12, height: 4, borderRadius: 2, background: '#8B8CF8' }} />
                <span style={{ width: 20, height: 4, borderRadius: 2, background: 'rgba(255, 255, 255, 0.2)' }} />
              </div>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div>
                <div style={{ fontWeight: 700, fontSize: '0.875rem', color: 'var(--text-color)' }}>Dark</div>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Midnight</div>
              </div>
              {currentTheme === 'dark' && (
                <div style={{ width: 20, height: 20, borderRadius: '50%', background: 'var(--accent)', color: 'var(--accent-text)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Check size={12} strokeWidth={3} />
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* 5. Export and Import Progress (Section 5.7) */}
      <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <div>
          <h2 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-color)' }}>
            Data Backup & Export
          </h2>
          <p style={{ fontSize: '0.825rem', color: 'var(--text-muted)' }}>
            Export or restore your full roadmap progress, scheduled reviews, and personal notes.
          </p>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
          <button
            onClick={exportData}
            className="btn-secondary"
            style={{ flex: '1 1 180px', padding: '0.65rem 1rem', fontSize: '0.85rem' }}
          >
            <Download size={16} />
            <span>Export Backup (JSON)</span>
          </button>

          <label
            className="btn-secondary"
            style={{ flex: '1 1 180px', padding: '0.65rem 1rem', fontSize: '0.85rem', cursor: 'pointer', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}
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

      {/* 6. Account Actions: Log Out & Delete My Data (Section 5.7) */}
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
              style={{ padding: '0.45rem 1rem', fontSize: '0.825rem' }}
            >
              <LogOut size={15} />
              <span>Log out</span>
            </button>
          </div>

          <div style={{ height: 1, background: 'var(--glass-border)' }} />

          {/* Delete My Data (Outlined in danger color per Section 5.7) */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.75rem' }}>
            <div>
              <div style={{ fontWeight: 600, fontSize: '0.9rem', color: '#EF4444' }}>Delete my data</div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                Permanently delete account, progress, reviews, and activity from Supabase (FR-30, Section 9 #14).
              </div>
            </div>
            <button
              onClick={() => {
                setTypedConfirm('');
                setShowDeleteModal(true);
              }}
              style={{
                padding: '0.45rem 1rem',
                fontSize: '0.825rem',
                fontWeight: 600,
                borderRadius: 'var(--radius-pill)',
                border: '1px solid #EF4444',
                background: 'rgba(239, 68, 68, 0.12)',
                color: '#EF4444',
                cursor: 'pointer',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.45rem'
              }}
            >
              <Trash2 size={15} />
              <span>Delete my data</span>
            </button>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal (Section 5.7: typed confirmation) */}
      {showDeleteModal && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0, 0, 0, 0.65)',
          backdropFilter: 'blur(16px)',
          WebkitBackdropFilter: 'blur(16px)',
          zIndex: 1000,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '1rem'
        }}>
          <div className="glass-card" style={{
            maxWidth: '460px',
            width: '100%',
            padding: '24px',
            display: 'flex',
            flexDirection: 'column',
            gap: '1rem',
            border: '1px solid #EF4444'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#EF4444' }}>
              <ShieldAlert size={22} />
              <h3 style={{ fontSize: '1.2rem', fontWeight: 800 }}>Confirm Deletion</h3>
            </div>

            <p style={{ fontSize: '0.875rem', color: 'var(--text-color)', lineHeight: 1.55 }}>
              This will permanently delete your account <strong>{user?.username}</strong>, along with all question progress, review records, and notes. This action cannot be reversed.
            </p>

            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.45rem' }}>
                Type your username <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--text-color)' }}>{user?.username}</span> to confirm:
              </label>
              <input
                type="text"
                value={typedConfirm}
                onChange={(e) => setTypedConfirm(e.target.value)}
                placeholder={user?.username}
                className="input"
                style={{ fontFamily: 'var(--font-mono)' }}
                autoFocus
              />
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '0.5rem' }}>
              <button
                onClick={() => setShowDeleteModal(false)}
                className="btn-secondary"
                style={{ padding: '0.45rem 1rem', fontSize: '0.85rem' }}
              >
                Cancel
              </button>
              <button
                onClick={handleDeleteAccount}
                disabled={deleteLoading || typedConfirm.trim().toLowerCase() !== user?.username.toLowerCase()}
                style={{
                  padding: '0.45rem 1.15rem',
                  fontSize: '0.85rem',
                  fontWeight: 600,
                  borderRadius: 'var(--radius-pill)',
                  border: 'none',
                  background: '#EF4444',
                  color: '#FFFFFF',
                  cursor: deleteLoading || typedConfirm.trim().toLowerCase() !== user?.username.toLowerCase() ? 'not-allowed' : 'pointer',
                  opacity: deleteLoading || typedConfirm.trim().toLowerCase() !== user?.username.toLowerCase() ? 0.45 : 1
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

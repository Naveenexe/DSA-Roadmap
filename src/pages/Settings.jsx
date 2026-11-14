import React, { useState } from 'react';
import { useApp } from '../context/AppContext';
import { 
  Settings as SettingsIcon, 
  Download, 
  Upload, 
  Trash2, 
  LogOut, 
  Sun, 
  Moon, 
  Code2, 
  Target, 
  ShieldAlert,
  Database
} from 'lucide-react';

export default function Settings({ onOpenLogin }) {
  const { 
    user, 
    updateSettings, 
    logout, 
    deleteAccount, 
    exportData, 
    importData, 
    showToast 
  } = useApp();

  const [dailyGoal, setDailyGoal] = useState(user?.daily_goal || 2);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const handleGoalChange = (val) => {
    const num = parseInt(val, 10);
    setDailyGoal(num);
    if (user) {
      updateSettings({ dailyGoal: num });
    }
  };

  const handleThemeChange = (theme) => {
    document.documentElement.setAttribute('data-theme', theme);
    if (user) {
      updateSettings({ theme });
    }
  };

  const handleLanguageChange = (language) => {
    if (user) {
      updateSettings({ language });
    }
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

  const currentTheme = user?.theme || document.documentElement.getAttribute('data-theme') || 'dark';
  const currentLang = user?.language || 'java';

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', maxWidth: '720px', margin: '0 auto' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
        <SettingsIcon size={24} color="var(--accent)" />
        <h1 style={{ fontSize: '1.5rem', fontWeight: 800 }}>Settings & Preferences</h1>
      </div>

      {/* Account Info */}
      <div className="card">
        <h2 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '0.75rem' }}>Account & Profile</h2>
        {user ? (
          <div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0.75rem 0', borderBottom: '1px solid var(--border-color)' }}>
              <div>
                <div style={{ fontWeight: 600 }}>Username</div>
                <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>{user.username}</div>
              </div>
              <span className="chip" style={{ background: 'var(--accent-light)', color: 'var(--accent)' }}>Active Session</span>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0.75rem 0' }}>
              <div>
                <div style={{ fontWeight: 600 }}>PIN Protection</div>
                <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                  {user.has_pin ? '4-digit PIN is enabled' : 'No PIN configured'}
                </div>
              </div>
              <span className="chip" style={{ background: user.has_pin ? 'var(--success-bg)' : 'var(--bg-input)', color: user.has_pin ? 'var(--success)' : 'var(--text-muted)' }}>
                {user.has_pin ? 'Protected' : 'Open'}
              </span>
            </div>
          </div>
        ) : (
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.5rem 0' }}>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
              You are currently using guest mode. Sign in with a username to sync your progress.
            </p>
            <button onClick={onOpenLogin} className="btn-primary" style={{ fontSize: '0.825rem' }}>
              Sign In
            </button>
          </div>
        )}
      </div>

      {/* Study Preferences */}
      <div className="card">
        <h2 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '1.25rem' }}>Study Preferences</h2>

        {/* Daily Goal */}
        <div style={{ marginBottom: '1.5rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
            <label style={{ fontWeight: 600, fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <Target size={16} color="var(--accent)" />
              <span>Daily Target (Questions / Day)</span>
            </label>
            <span style={{ fontWeight: 700, fontSize: '1rem', color: 'var(--accent)' }}>
              {dailyGoal}
            </span>
          </div>
          <input
            type="range"
            min="1"
            max="10"
            value={dailyGoal}
            onChange={(e) => handleGoalChange(e.target.value)}
            style={{ width: '100%', cursor: 'pointer' }}
          />
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
            <span>1 problem</span>
            <span>5 problems</span>
            <span>10 problems</span>
          </div>
        </div>

        {/* Preferred Code Language */}
        <div style={{ marginBottom: '1.5rem' }}>
          <label style={{ display: 'block', fontWeight: 600, fontSize: '0.9rem', marginBottom: '0.6rem' }}>
            Default Code Language
          </label>
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <button
              onClick={() => handleLanguageChange('java')}
              className={currentLang === 'java' ? 'btn-primary' : 'btn-secondary'}
              style={{ flex: 1, padding: '0.6rem' }}
            >
              Java
            </button>
            <button
              onClick={() => handleLanguageChange('python')}
              className={currentLang === 'python' ? 'btn-primary' : 'btn-secondary'}
              style={{ flex: 1, padding: '0.6rem' }}
            >
              Python
            </button>
          </div>
        </div>

        {/* Theme */}
        <div>
          <label style={{ display: 'block', fontWeight: 600, fontSize: '0.9rem', marginBottom: '0.6rem' }}>
            Interface Theme
          </label>
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <button
              onClick={() => handleThemeChange('dark')}
              className={currentTheme === 'dark' ? 'btn-primary' : 'btn-secondary'}
              style={{ flex: 1, padding: '0.6rem' }}
            >
              <Moon size={16} />
              <span>Dark Theme (Default)</span>
            </button>
            <button
              onClick={() => handleThemeChange('light')}
              className={currentTheme === 'light' ? 'btn-primary' : 'btn-secondary'}
              style={{ flex: 1, padding: '0.6rem' }}
            >
              <Sun size={16} />
              <span>Light Theme</span>
            </button>
          </div>
        </div>
      </div>

      {/* Backup & Data Sync */}
      <div className="card">
        <h2 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '0.75rem' }}>Data Backup & Portability</h2>
        <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
          Export your entire roadmap progress, review history, notes, and activity as a JSON backup file.
        </p>

        <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
          <button onClick={exportData} className="btn-secondary" style={{ flex: '1 1 180px' }}>
            <Download size={16} />
            <span>Export Backup (JSON)</span>
          </button>

          <label className="btn-secondary" style={{ flex: '1 1 180px', cursor: 'pointer' }}>
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

      {/* Account Actions */}
      {user && (
        <div className="card" style={{ border: '1px solid rgba(239, 68, 68, 0.2)' }}>
          <h2 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '0.75rem', color: 'var(--danger)' }}>
            Danger Zone
          </h2>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
            <div>
              <div style={{ fontWeight: 600 }}>Log Out</div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Clear active session from this device</div>
            </div>
            <button onClick={logout} className="btn-secondary" style={{ fontSize: '0.85rem' }}>
              <LogOut size={16} />
              <span>Log Out</span>
            </button>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem', marginTop: '1.25rem', paddingTop: '1.25rem', borderTop: '1px solid var(--border-color)' }}>
            <div>
              <div style={{ fontWeight: 600, color: 'var(--danger)' }}>Delete My Data</div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Permanently delete account, progress, and reviews (FR-30)</div>
            </div>
            <button onClick={() => setShowDeleteConfirm(true)} className="btn-danger" style={{ fontSize: '0.85rem' }}>
              <Trash2 size={16} />
              <span>Delete My Data</span>
            </button>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="modal-overlay">
          <div className="modal-content" style={{ maxWidth: '420px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--danger)', marginBottom: '0.75rem' }}>
              <ShieldAlert size={22} />
              <h3 style={{ fontSize: '1.15rem', fontWeight: 700 }}>Confirm Deletion</h3>
            </div>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '1.25rem', lineHeight: 1.5 }}>
              Are you sure you want to permanently erase all progress for <strong>{user?.username}</strong>? This cannot be undone.
            </p>
            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem' }}>
              <button onClick={() => setShowDeleteConfirm(false)} className="btn-secondary">
                Cancel
              </button>
              <button 
                onClick={async () => {
                  setShowDeleteConfirm(false);
                  await deleteAccount();
                  showToast('Account data deleted successfully.');
                }} 
                className="btn-danger"
              >
                Yes, Delete Everything
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}


import React, { useState } from 'react';
import { useApp } from '../context/AppContext';
import { Lock, User, AlertCircle, X, ShieldAlert } from 'lucide-react';

export default function LoginModal({ isOpen, onClose }) {
  const { login } = useApp();
  const [username, setUsername] = useState('');
  const [pin, setPin] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    const cleanUser = username.trim().toLowerCase();
    if (!/^[a-z0-9_]{3,20}$/.test(cleanUser)) {
      setError('Username must be 3-20 characters: lowercase letters, numbers, and underscores.');
      return;
    }

    if (pin && !/^\d{4}$/.test(pin)) {
      setError('PIN must be exactly 4 digits, or left blank.');
      return;
    }

    setSubmitting(true);
    try {
      await login(cleanUser, pin);
      onClose();
    } catch (err) {
      setError(err.message || 'Login failed. Please check your credentials.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.25rem' }}>
          <div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 700 }}>DSA Tracker Login</h2>
            <p style={{ fontSize: '0.825rem', color: 'var(--text-secondary)' }}>
              Enter your username to access or create your study progress.
            </p>
          </div>
          <button onClick={onClose} className="icon-btn" style={{ border: 'none' }}>
            <X size={18} />
          </button>
        </div>

        {error && (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            padding: '0.75rem',
            background: 'var(--danger-bg)',
            border: '1px solid rgba(239, 68, 68, 0.3)',
            borderRadius: 'var(--radius-md)',
            color: 'var(--danger)',
            fontSize: '0.85rem',
            marginBottom: '1rem'
          }}>
            <AlertCircle size={16} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '0.35rem', color: 'var(--text-secondary)' }}>
              Username (required)
            </label>
            <div style={{ position: 'relative' }}>
              <input
                type="text"
                className="input"
                placeholder="e.g. codemaster_99"
                value={username}
                onChange={(e) => setUsername(e.target.value.toLowerCase())}
                autoFocus
                required
                style={{ paddingLeft: '2.4rem' }}
              />
              <User size={16} style={{ position: 'absolute', left: '0.85rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
            </div>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginTop: '0.25rem' }}>
              3 to 20 characters (a-z, 0-9, _)
            </span>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '0.35rem', color: 'var(--text-secondary)' }}>
              4-digit PIN (optional)
            </label>
            <div style={{ position: 'relative' }}>
              <input
                type="password"
                maxLength={4}
                className="input"
                placeholder="••••"
                value={pin}
                onChange={(e) => setPin(e.target.value.replace(/\D/g, ''))}
                style={{ paddingLeft: '2.4rem', letterSpacing: '0.25em' }}
              />
              <Lock size={16} style={{ position: 'absolute', left: '0.85rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
            </div>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginTop: '0.25rem' }}>
              Protects your profile from accidental edits by others.
            </span>
          </div>

          <div style={{
            display: 'flex',
            alignItems: 'flex-start',
            gap: '0.5rem',
            padding: '0.75rem',
            background: 'var(--bg-input)',
            border: '1px solid var(--border-color)',
            borderRadius: 'var(--radius-md)',
            fontSize: '0.775rem',
            color: 'var(--text-muted)',
            lineHeight: 1.4
          }}>
            <ShieldAlert size={16} style={{ flexShrink: 0, marginTop: '2px', color: 'var(--warning)' }} />
            <span>
              <strong>Note:</strong> This app does not use passwords or email authentication. Anyone who enters your username (and PIN, if configured) can view and modify this progress.
            </span>
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.6rem', marginTop: '0.5rem' }}>
            <button type="button" onClick={onClose} className="btn-secondary">
              Cancel
            </button>
            <button type="submit" disabled={submitting} className="btn-primary">
              {submitting ? 'Entering...' : 'Enter App'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}


import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useApp } from '../context/AppContext';
import { Play, Pause, RotateCcw, Clock } from 'lucide-react';

export default function SolveTimer({ seq, difficulty, isDone, onSlowDetected }) {
  const { statsMap, saveQuestionStats, user } = useApp();
  const qSeq = Number(seq);
  const currentStats = statsMap[qSeq] || { seconds: 0, attempts: 0, slow: false };

  const [seconds, setSeconds] = useState(currentStats.seconds || 0);
  const [isRunning, setIsRunning] = useState(false);
  const unsavedSecondsRef = useRef(0);
  const secondsRef = useRef(seconds);
  secondsRef.current = seconds;

  // Flush on isDone
  useEffect(() => {
    if (isDone) {
      flushSeconds(false);
    }
  }, [isDone]);

  // Sync initial seconds when question changes
  useEffect(() => {
    const s = statsMap[qSeq]?.seconds || 0;
    setSeconds(s);
    setIsRunning(false);
    unsavedSecondsRef.current = 0;
  }, [qSeq, statsMap]);

  // Flush unsaved seconds to state and Supabase/localStorage
  const flushSeconds = useCallback((newAttempt = false) => {
    if (unsavedSecondsRef.current > 0 || newAttempt) {
      const toAdd = unsavedSecondsRef.current;
      unsavedSecondsRef.current = 0;
      saveQuestionStats(qSeq, {
        addSeconds: toAdd,
        newAttempt
      });
    }
  }, [qSeq, saveQuestionStats]);

  // Handle Start
  const handleStart = () => {
    const todayStr = new Date().toISOString().split('T')[0];
    const userPrefix = user?.username ? user.username.toLowerCase() : 'guest';
    const attemptKey = `chainline_attempt_${userPrefix}_${qSeq}_${todayStr}`;

    let isNewAttempt = false;
    try {
      if (!localStorage.getItem(attemptKey)) {
        isNewAttempt = true;
        localStorage.setItem(attemptKey, '1');
      }
    } catch (_) {}

    setIsRunning(true);
    if (isNewAttempt) {
      flushSeconds(true);
    }
  };

  // Handle Pause
  const handlePause = () => {
    setIsRunning(false);
    flushSeconds(false);
  };

  // Handle Reset
  const handleReset = () => {
    setIsRunning(false);
    unsavedSecondsRef.current = 0;
    setSeconds(0);
    // Overwrite to 0 in storage
    saveQuestionStats(qSeq, {
      addSeconds: -secondsRef.current
    });
  };

  // Timer interval: tick every second, auto-save every 15 seconds
  useEffect(() => {
    if (!isRunning) return;

    const interval = setInterval(() => {
      setSeconds(prev => prev + 1);
      unsavedSecondsRef.current += 1;

      // Auto-save every 15 seconds
      if (unsavedSecondsRef.current >= 15) {
        flushSeconds(false);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [isRunning, flushSeconds]);

  // Auto-pause when tab is hidden (Section 6.1)
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.visibilityState === 'hidden' && isRunning) {
        setIsRunning(false);
        flushSeconds(false);
      }
    };
    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
  }, [isRunning, flushSeconds]);

  // Save on unmount / question switch
  useEffect(() => {
    return () => {
      flushSeconds(false);
    };
  }, [flushSeconds]);

  // Format time display as MM:SS (or HH:MM:SS)
  const formatTime = (totalSec) => {
    const h = Math.floor(totalSec / 3600);
    const m = Math.floor((totalSec % 3600) / 60);
    const s = totalSec % 60;
    const mm = String(m).padStart(2, '0');
    const ss = String(s).padStart(2, '0');
    if (h > 0) {
      return `${String(h).padStart(2, '0')}:${mm}:${ss}`;
    }
    return `${mm}:${ss}`;
  };

  const attemptsCount = currentStats.attempts || 0;

  return (
    <div 
      className="glass-card question-timer-card"
      style={{
        padding: '14px 18px',
        width: '100%',
        boxSizing: 'border-box',
        display: 'flex',
        flexDirection: 'column',
        gap: '10px'
      }}
    >
      {/* Desktop Layout: One row (Time, Start/Pause, Reset, Attempts) */}
      <div className="timer-row-desktop" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Clock size={18} color="var(--accent)" />
          <span style={{ fontSize: '1.4rem', fontWeight: 800, fontFamily: 'var(--font-mono)', letterSpacing: '0.02em', color: 'var(--text-color)', minWidth: '80px' }}>
            {formatTime(seconds)}
          </span>
          {isRunning && (
            <span style={{ width: 8, height: 8, borderRadius: '50%', background: '#10B981', display: 'inline-block', animation: 'pulse 1.5s infinite' }} />
          )}
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          {isRunning ? (
            <button
              type="button"
              onClick={handlePause}
              className="btn-secondary"
              style={{ minHeight: '40px', padding: '0 14px', fontSize: '0.85rem', display: 'inline-flex', alignItems: 'center', gap: '6px' }}
            >
              <Pause size={15} />
              <span>Pause</span>
            </button>
          ) : (
            <button
              type="button"
              onClick={handleStart}
              className="btn-primary"
              style={{ minHeight: '40px', padding: '0 16px', fontSize: '0.85rem', display: 'inline-flex', alignItems: 'center', gap: '6px' }}
            >
              <Play size={15} />
              <span>Start</span>
            </button>
          )}

          <button
            type="button"
            onClick={handleReset}
            className="btn-secondary"
            style={{ minHeight: '40px', padding: '0 12px', fontSize: '0.85rem' }}
            title="Reset timer"
            aria-label="Reset timer"
          >
            <RotateCcw size={15} />
          </button>
        </div>

        <div style={{ fontSize: '0.825rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)', fontWeight: 600 }}>
          Attempts: {attemptsCount}
        </div>
      </div>

      {/* Mobile Layout: 2 Lines (Line 1: Time & Attempts, Line 2: 3 buttons each 48px) */}
      <div className="timer-row-mobile" style={{ display: 'none', flexDirection: 'column', gap: '10px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Clock size={16} color="var(--accent)" />
            <span style={{ fontSize: '1.4rem', fontWeight: 800, fontFamily: 'var(--font-mono)', color: 'var(--text-color)' }}>
              {formatTime(seconds)}
            </span>
            {isRunning && (
              <span style={{ width: 8, height: 8, borderRadius: '50%', background: '#10B981', display: 'inline-block' }} />
            )}
          </div>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)', fontWeight: 600 }}>
            Attempts: {attemptsCount}
          </span>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1.5fr 1fr 1fr', gap: '8px', width: '100%' }}>
          {isRunning ? (
            <button
              type="button"
              onClick={handlePause}
              className="btn-secondary"
              style={{ minHeight: '48px', height: '48px', justifyContent: 'center', fontSize: '0.9rem' }}
            >
              <Pause size={16} />
              <span>Pause</span>
            </button>
          ) : (
            <button
              type="button"
              onClick={handleStart}
              className="btn-primary"
              style={{ minHeight: '48px', height: '48px', justifyContent: 'center', fontSize: '0.9rem' }}
            >
              <Play size={16} />
              <span>Start</span>
            </button>
          )}

          <button
            type="button"
            onClick={handlePause}
            disabled={!isRunning}
            className="btn-secondary"
            style={{ minHeight: '48px', height: '48px', justifyContent: 'center', fontSize: '0.9rem', opacity: isRunning ? 1 : 0.4 }}
          >
            <span>Pause</span>
          </button>

          <button
            type="button"
            onClick={handleReset}
            className="btn-secondary"
            style={{ minHeight: '48px', height: '48px', justifyContent: 'center', fontSize: '0.9rem' }}
          >
            <RotateCcw size={16} />
            <span>Reset</span>
          </button>
        </div>
      </div>
    </div>
  );
}
import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useApp } from '../context/AppContext';
import { Play, Pause, RotateCcw, Clock } from 'lucide-react';

export default function SolveTimer({ seq, difficulty, isDone }) {
  const { statsMap, saveQuestionStats, user } = useApp();
  const qSeq = Number(seq);

  // Read saved total from statsMap on mount
  const savedTotal = statsMap[qSeq]?.seconds || 0;
  const attemptsCount = statsMap[qSeq]?.attempts || 0;

  // 3-state state machine: 'idle' | 'running' | 'paused'
  const [timerState, setTimerState] = useState('idle');
  const [seconds, setSeconds] = useState(savedTotal);

  const unsavedSecondsRef = useRef(0);
  const secondsRef = useRef(seconds);
  secondsRef.current = seconds;

  const timerStateRef = useRef(timerState);
  timerStateRef.current = timerState;

  // Flush unsaved seconds to state and Supabase/localStorage
  const flushSeconds = useCallback(() => {
    if (unsavedSecondsRef.current > 0) {
      const toAdd = unsavedSecondsRef.current;
      unsavedSecondsRef.current = 0;
      saveQuestionStats(qSeq, { addSeconds: toAdd });
    }
  }, [qSeq, saveQuestionStats]);

  // Flush on isDone
  useEffect(() => {
    if (isDone) {
      if (timerStateRef.current === 'running') {
        setTimerState('paused');
      }
      flushSeconds();
    }
  }, [isDone, flushSeconds]);

  // Handle Start (First tap operates synchronously in the same event)
  const handleStart = () => {
    setTimerState('running');

    // Record attempt for today if not already recorded
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

    if (isNewAttempt) {
      saveQuestionStats(qSeq, { newAttempt: true });
    }
  };

  // Handle Pause
  const handlePause = () => {
    setTimerState('paused');
    flushSeconds();
  };

  // Handle Resume
  const handleResume = () => {
    setTimerState('running');
  };

  // Handle Reset (Always transitions back to idle with 0 seconds)
  const handleReset = () => {
    setTimerState('idle');
    const toSubtract = secondsRef.current;
    unsavedSecondsRef.current = 0;
    setSeconds(0);
    if (toSubtract > 0) {
      saveQuestionStats(qSeq, { addSeconds: -toSubtract });
    }
  };

  // Ticking loop: ticks every second when running, auto-saves every 15s
  useEffect(() => {
    if (timerState !== 'running') return;

    const interval = setInterval(() => {
      setSeconds(prev => prev + 1);
      unsavedSecondsRef.current += 1;

      // Auto-save every 15 seconds while running
      if (unsavedSecondsRef.current >= 15) {
        flushSeconds();
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [timerState, flushSeconds]);

  // Automatic pause when the browser tab is hidden (Section 6.1)
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.visibilityState === 'hidden' && timerStateRef.current === 'running') {
        setTimerState('paused');
        flushSeconds();
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
  }, [flushSeconds]);

  // Save on unmount / question switch
  useEffect(() => {
    return () => {
      if (unsavedSecondsRef.current > 0) {
        const toAdd = unsavedSecondsRef.current;
        unsavedSecondsRef.current = 0;
        saveQuestionStats(qSeq, { addSeconds: toAdd });
      }
    };
  }, [qSeq, saveQuestionStats]);

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

  return (
    <div 
      className="glass-card question-timer-card"
      style={{
        padding: '14px 18px',
        width: '100%',
        boxSizing: 'border-box',
        display: 'flex',
        flexDirection: 'column',
        gap: '10px',
        marginTop: 'auto'
      }}
    >
      {/* Desktop Layout: One row (Time, Start/Pause/Resume, Reset, Attempts) */}
      <div className="timer-row-desktop" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Clock size={18} color="var(--accent)" />
          <span className="timer-display-time" style={{ fontSize: '1.4rem', fontWeight: 800, fontFamily: 'var(--font-mono)', letterSpacing: '0.02em', color: 'var(--text-color)', minWidth: '80px' }}>
            {formatTime(seconds)}
          </span>
          {timerState === 'running' && (
            <span style={{ width: 8, height: 8, borderRadius: '50%', background: '#10B981', display: 'inline-block', animation: 'pulse 1.5s infinite' }} />
          )}
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          {timerState === 'running' ? (
            <button
              type="button"
              onClick={handlePause}
              className="btn-secondary timer-action-btn timer-btn-pause"
              style={{ minHeight: '40px', padding: '0 14px', fontSize: '0.85rem', display: 'inline-flex', alignItems: 'center', gap: '6px' }}
            >
              <Pause size={15} />
              <span>Pause</span>
            </button>
          ) : timerState === 'paused' ? (
            <button
              type="button"
              onClick={handleResume}
              className="btn-primary timer-action-btn timer-btn-resume"
              style={{ minHeight: '40px', padding: '0 16px', fontSize: '0.85rem', display: 'inline-flex', alignItems: 'center', gap: '6px' }}
            >
              <Play size={15} />
              <span>Resume</span>
            </button>
          ) : (
            <button
              type="button"
              onClick={handleStart}
              className="btn-primary timer-action-btn timer-btn-start"
              style={{ minHeight: '40px', padding: '0 16px', fontSize: '0.85rem', display: 'inline-flex', alignItems: 'center', gap: '6px' }}
            >
              <Play size={15} />
              <span>Start</span>
            </button>
          )}

          <button
            type="button"
            onClick={handleReset}
            className="btn-secondary timer-reset-btn"
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

      {/* Mobile Layout: 2 Lines (Line 1: Time & Attempts, Line 2: Exactly 2 buttons: Primary + Reset) */}
      <div className="timer-row-mobile" style={{ display: 'none', flexDirection: 'column', gap: '10px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Clock size={16} color="var(--accent)" />
            <span className="timer-display-time" style={{ fontSize: '1.4rem', fontWeight: 800, fontFamily: 'var(--font-mono)', color: 'var(--text-color)' }}>
              {formatTime(seconds)}
            </span>
            {timerState === 'running' && (
              <span style={{ width: 8, height: 8, borderRadius: '50%', background: '#10B981', display: 'inline-block' }} />
            )}
          </div>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)', fontWeight: 600 }}>
            Attempts: {attemptsCount}
          </span>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', width: '100%' }}>
          {timerState === 'running' ? (
            <button
              type="button"
              onClick={handlePause}
              className="btn-secondary timer-action-btn timer-btn-pause"
              style={{ minHeight: '48px', height: '48px', justifyContent: 'center', fontSize: '0.9rem', gap: '6px' }}
            >
              <Pause size={16} />
              <span>Pause</span>
            </button>
          ) : timerState === 'paused' ? (
            <button
              type="button"
              onClick={handleResume}
              className="btn-primary timer-action-btn timer-btn-resume"
              style={{ minHeight: '48px', height: '48px', justifyContent: 'center', fontSize: '0.9rem', gap: '6px' }}
            >
              <Play size={16} />
              <span>Resume</span>
            </button>
          ) : (
            <button
              type="button"
              onClick={handleStart}
              className="btn-primary timer-action-btn timer-btn-start"
              style={{ minHeight: '48px', height: '48px', justifyContent: 'center', fontSize: '0.9rem', gap: '6px' }}
            >
              <Play size={16} />
              <span>Start</span>
            </button>
          )}

          <button
            type="button"
            onClick={handleReset}
            className="btn-secondary timer-reset-btn"
            style={{ minHeight: '48px', height: '48px', justifyContent: 'center', fontSize: '0.9rem', gap: '6px' }}
          >
            <RotateCcw size={16} />
            <span>Reset</span>
          </button>
        </div>
      </div>
    </div>
  );
}

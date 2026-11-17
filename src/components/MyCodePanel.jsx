import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useApp } from '../context/AppContext';
import { Copy, Check, Eye, EyeOff, AlertCircle, Code2, BookOpen } from 'lucide-react';
import Prism from 'prismjs';
import 'prismjs/components/prism-java';
import 'prismjs/components/prism-python';

export default function MyCodePanel({ seq, richSolution }) {
  const { language: globalLanguage, solutionsMap, saveUserSolution, loadUserSolution, showToast } = useApp();
  const qSeq = Number(seq);

  const [panelLang, setPanelLang] = useState(globalLanguage || 'java');
  const [code, setCode] = useState('');
  const [saveStatus, setSaveStatus] = useState('saved'); // 'saved' | 'saving'
  const [copied, setCopied] = useState(false);
  const [showReference, setShowReference] = useState(false);
  const [refTab, setRefTab] = useState('brute'); // 'brute' | 'optimal' (Brute force first)
  const [charLimitExceeded, setCharLimitExceeded] = useState(false);

  const saveTimerRef = useRef(null);
  const textareaRef = useRef(null);

  // Sync / load code when question or panel language changes
  useEffect(() => {
    let active = true;
    const cachedCode = solutionsMap[qSeq]?.[panelLang];
    if (cachedCode !== undefined) {
      setCode(cachedCode);
      setCharLimitExceeded(cachedCode.length >= 20000);
      setSaveStatus('saved');
    } else {
      loadUserSolution(qSeq, panelLang).then(loaded => {
        if (active) {
          setCode(loaded || '');
          setCharLimitExceeded((loaded || '').length >= 20000);
          setSaveStatus('saved');
        }
      });
    }
    return () => { active = false; };
  }, [qSeq, panelLang, solutionsMap, loadUserSolution]);

  // Debounced auto-save (1.5 seconds after typing stops)
  const triggerAutoSave = useCallback((newCode, lang) => {
    if (saveTimerRef.current) {
      clearTimeout(saveTimerRef.current);
    }
    setSaveStatus('saving');
    saveTimerRef.current = setTimeout(async () => {
      try {
        await saveUserSolution(qSeq, lang, newCode);
        setSaveStatus('saved');
      } catch (err) {
        setSaveStatus('saved');
      }
    }, 1500);
  }, [qSeq, saveUserSolution]);

  // Clean up timer on unmount
  useEffect(() => {
    return () => {
      if (saveTimerRef.current) clearTimeout(saveTimerRef.current);
    };
  }, []);

  // Handle Code Change
  const handleChange = (e) => {
    const val = e.target.value;
    if (val.length > 20000) {
      setCharLimitExceeded(true);
      // Clamp to 20,000 characters
      const clamped = val.slice(0, 20000);
      setCode(clamped);
      triggerAutoSave(clamped, panelLang);
      return;
    }
    setCharLimitExceeded(false);
    setCode(val);
    triggerAutoSave(val, panelLang);
  };

  // Tab key handler: insert 4 spaces
  const handleKeyDown = (e) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const textarea = textareaRef.current;
      if (!textarea) return;

      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const spaces = '    ';

      const newCode = code.substring(0, start) + spaces + code.substring(end);
      if (newCode.length > 20000) {
        setCharLimitExceeded(true);
        return;
      }

      setCode(newCode);
      triggerAutoSave(newCode, panelLang);

      // Restore cursor position
      setTimeout(() => {
        textarea.selectionStart = textarea.selectionEnd = start + 4;
      }, 0);
    }
  };

  // Copy code to clipboard
  const handleCopy = async () => {
    if (!code) return;
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
      showToast('Code copied to clipboard', 'info');
    } catch (_) {}
  };

  // Reference solution data
  const refCode = refTab === 'brute' 
    ? richSolution?.brute?.code?.[panelLang] 
    : richSolution?.optimal?.code?.[panelLang];

  const refIdea = refTab === 'brute' 
    ? richSolution?.brute?.idea 
    : richSolution?.optimal?.idea;

  const refTime = refTab === 'brute' 
    ? richSolution?.brute?.time 
    : richSolution?.optimal?.time;

  const refSpace = refTab === 'brute' 
    ? richSolution?.brute?.space 
    : richSolution?.optimal?.space;

  // Prism highlight effect for reference code
  useEffect(() => {
    if (showReference && refCode) {
      setTimeout(() => Prism.highlightAll(), 0);
    }
  }, [showReference, refTab, panelLang, refCode]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', width: '100%' }}>
      {/* Top Header Card */}
      <div 
        className="glass-card" 
        style={{ 
          padding: '16px 20px', 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'space-between', 
          flexWrap: 'wrap', 
          gap: '12px' 
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Code2 size={20} color="var(--accent)" />
          <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--text-color)', margin: 0 }}>
            My Solution
          </h3>
          <span 
            style={{ 
              fontSize: '0.75rem', 
              fontFamily: 'var(--font-mono)', 
              color: saveStatus === 'saving' ? 'var(--revisit-color)' : 'var(--text-muted)',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '4px'
            }}
          >
            {saveStatus === 'saving' ? 'Saving...' : 'Saved'}
          </span>
        </div>

        {/* Controls: Language Switch, Copy, Show Reference Solution toggle */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
          
          {/* Language Switch: Java | Python */}
          <div 
            style={{ 
              display: 'inline-flex', 
              background: 'var(--glass-surface)', 
              border: '1px solid var(--glass-border)', 
              borderRadius: 'var(--radius-pill)', 
              padding: '2px', 
              gap: '2px' 
            }}
          >
            <button
              type="button"
              onClick={() => setPanelLang('java')}
              style={{
                padding: '4px 12px',
                borderRadius: 'var(--radius-pill)',
                fontSize: '0.75rem',
                fontWeight: 700,
                border: 'none',
                cursor: 'pointer',
                background: panelLang === 'java' ? 'var(--accent)' : 'transparent',
                color: panelLang === 'java' ? '#fff' : 'var(--text-muted)'
              }}
            >
              Java
            </button>
            <button
              type="button"
              onClick={() => setPanelLang('python')}
              style={{
                padding: '4px 12px',
                borderRadius: 'var(--radius-pill)',
                fontSize: '0.75rem',
                fontWeight: 700,
                border: 'none',
                cursor: 'pointer',
                background: panelLang === 'python' ? 'var(--accent)' : 'transparent',
                color: panelLang === 'python' ? '#fff' : 'var(--text-muted)'
              }}
            >
              Python
            </button>
          </div>

          {/* Copy Button */}
          <button
            type="button"
            onClick={handleCopy}
            className="btn-secondary"
            style={{ padding: '6px 12px', fontSize: '0.78rem', minHeight: '36px', display: 'inline-flex', alignItems: 'center', gap: '5px' }}
            title="Copy my code"
          >
            {copied ? <Check size={14} color="#10B981" /> : <Copy size={14} />}
            <span>{copied ? 'Copied' : 'Copy'}</span>
          </button>

          {/* Toggle Show Reference Solution */}
          <button
            type="button"
            onClick={() => setShowReference(!showReference)}
            className={`btn-secondary ${showReference ? 'active' : ''}`}
            style={{ 
              padding: '6px 12px', 
              fontSize: '0.78rem', 
              minHeight: '36px', 
              display: 'inline-flex', 
              alignItems: 'center', 
              gap: '6px',
              background: showReference ? 'var(--accent-soft)' : 'var(--glass-surface)',
              color: showReference ? 'var(--accent)' : 'var(--text-color)'
            }}
          >
            {showReference ? <EyeOff size={14} /> : <Eye size={14} />}
            <span>Reference</span>
          </button>
        </div>
      </div>

      {/* Limit Warning Banner */}
      {charLimitExceeded && (
        <div 
          style={{ 
            padding: '10px 14px', 
            borderRadius: 'var(--radius-inner)', 
            background: 'rgba(239, 68, 68, 0.12)', 
            border: '1px solid #ef4444', 
            color: '#ef4444',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            fontSize: '0.825rem'
          }}
        >
          <AlertCircle size={16} />
          <span>Your code is longer than 20,000 characters. Extra characters were trimmed.</span>
        </div>
      )}

      {/* Plain Monospace Textarea Editor */}
      <div className="glass-card" style={{ padding: '16px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
        <textarea
          ref={textareaRef}
          value={code}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          placeholder={`// Write your ${panelLang === 'java' ? 'Java' : 'Python'} solution here...\n// Press Tab to indent 4 spaces.\n// Auto-saves automatically.`}
          spellCheck={false}
          style={{
            width: '100%',
            minHeight: '300px',
            height: '380px',
            fontFamily: 'var(--font-mono)',
            fontSize: '14px',
            lineHeight: 1.6,
            background: 'transparent',
            color: 'var(--text-color)',
            border: 'none',
            outline: 'none',
            resize: 'vertical',
            boxSizing: 'border-box'
          }}
        />

        {/* Character count footer */}
        <div style={{ display: 'flex', justifyContent: 'flex-end', fontSize: '0.72rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
          {code.length.toLocaleString()} / 20,000 characters
        </div>
      </div>

      {/* Reference Solution Section (When toggled on) */}
      {showReference && (
        <div className="glass-card" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '14px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '10px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <BookOpen size={18} color="var(--accent)" />
              <h4 style={{ fontSize: '0.95rem', fontWeight: 700, margin: 0, color: 'var(--text-color)' }}>
                Reference Solution ({panelLang === 'java' ? 'Java' : 'Python'})
              </h4>
            </div>

            {/* Brute force | Optimal tab toggle (Brute force first per Part 1) */}
            <div 
              style={{ 
                display: 'inline-flex', 
                background: 'var(--glass-surface)', 
                border: '1px solid var(--glass-border)', 
                borderRadius: 'var(--radius-pill)', 
                padding: '2px', 
                gap: '2px' 
              }}
            >
              <button
                type="button"
                onClick={() => setRefTab('brute')}
                style={{
                  padding: '4px 12px',
                  borderRadius: 'var(--radius-pill)',
                  fontSize: '0.75rem',
                  fontWeight: 700,
                  border: 'none',
                  cursor: 'pointer',
                  background: refTab === 'brute' ? 'var(--accent)' : 'transparent',
                  color: refTab === 'brute' ? '#fff' : 'var(--text-muted)'
                }}
              >
                Brute force
              </button>
              <button
                type="button"
                onClick={() => setRefTab('optimal')}
                style={{
                  padding: '4px 12px',
                  borderRadius: 'var(--radius-pill)',
                  fontSize: '0.75rem',
                  fontWeight: 700,
                  border: 'none',
                  cursor: 'pointer',
                  background: refTab === 'optimal' ? 'var(--accent)' : 'transparent',
                  color: refTab === 'optimal' ? '#fff' : 'var(--text-muted)'
                }}
              >
                Optimal
              </button>
            </div>
          </div>

          {/* Reference Idea & Complexity */}
          {refIdea && (
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', margin: 0 }}>
              <strong style={{ color: 'var(--text-color)' }}>Key idea: </strong>{refIdea}
            </p>
          )}

          {(refTime || refSpace) && (
            <div style={{ display: 'flex', gap: '12px', fontSize: '0.78rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
              {refTime && <span>Time: {refTime}</span>}
              {refTime && refSpace && <span>·</span>}
              {refSpace && <span>Space: {refSpace}</span>}
            </div>
          )}

          {/* Reference Code Block */}
          {refCode ? (
            <div className="code-panel" style={{
              background: 'var(--code-bg)',
              borderRadius: 'var(--radius-inner)',
              overflow: 'hidden',
              border: '1px solid rgba(255, 255, 255, 0.12)',
              width: '100%',
              maxWidth: '100%'
            }}>
              <pre style={{
                margin: 0,
                padding: '16px',
                fontFamily: 'var(--font-code)',
                fontSize: '13px',
                lineHeight: '20px',
                overflowX: 'auto',
                whiteSpace: 'pre',
                wordBreak: 'normal',
                maxWidth: '100%',
                boxSizing: 'border-box'
              }}>
                <code className={`language-${panelLang}`}>
                  {refCode}
                </code>
              </pre>
            </div>
          ) : (
            <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', fontStyle: 'italic', padding: '12px 0' }}>
              Reference code not available for this problem.
            </div>
          )}
        </div>
      )}
    </div>
  );
}
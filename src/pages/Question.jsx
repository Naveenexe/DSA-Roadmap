import React, { useState, useEffect, useMemo } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import Prism from 'prismjs';
import 'prismjs/components/prism-java';
import 'prismjs/components/prism-python';
import { 
  ArrowLeft, 
  ArrowRight, 
  ExternalLink, 
  Copy, 
  Check, 
  Clock, 
  AlertTriangle, 
  Link2, 
  Lock, 
  Lightbulb, 
  BookOpen, 
  Code2, 
  Sparkles,
  FileText
} from 'lucide-react';

export default function Question() {
  const { seq: seqParam } = useParams();
  const navigate = useNavigate();
  const seq = parseInt(seqParam, 10);

  const { 
    questions, 
    chapters, 
    progressMap, 
    updateProgress, 
    user, 
    updateSettings, 
    showToast 
  } = useApp();

  // Active view in right panel: null (initial), 'hint-1', 'hint-2', 'hint-3', 'approach', 'code'
  const [activePanel, setActivePanel] = useState(null);

  // Approach / Code sub-tab: 'optimal' or 'brute'
  const [approachSubTab, setApproachSubTab] = useState('optimal');
  const [codeSubTab, setCodeSubTab] = useState('optimal');

  // Copy code feedback
  const [copied, setCopied] = useState(false);

  // Cached chapter solutions
  const [solutionsCache, setSolutionsCache] = useState({});
  const [loadingSolution, setLoadingSolution] = useState(false);

  // Unlocked hints level for current seq: 0 = none, 1 = hint 1, 2 = hints 1&2, 3 = hints 1,2&3
  const [unlockedHintLevel, setUnlockedHintLevel] = useState(() => {
    const saved = localStorage.getItem(`unlocked_hints_${seq}`);
    return saved ? parseInt(saved, 10) : 0;
  });

  // Sync unlocked hint level when seq changes
  useEffect(() => {
    const saved = localStorage.getItem(`unlocked_hints_${seq}`);
    const level = saved ? parseInt(saved, 10) : 0;
    setUnlockedHintLevel(level);
    setActivePanel(null); // Keep clean initial view with only buttons shown
  }, [seq]);

  // Notes state
  const currentProgress = progressMap[seq];
  const [notes, setNotes] = useState('');
  const [notesSaved, setNotesSaved] = useState(true);

  // Scheduling state for Revisit & Remind on Done
  const [remindOnDone, setRemindOnDone] = useState(true);
  const [revisitDate, setRevisitDate] = useState(() => {
    const tom = new Date();
    tom.setDate(tom.getDate() + 1);
    return tom.toISOString().split('T')[0];
  });

  // Current question object from static questions.json
  const question = useMemo(() => {
    return questions.find(q => q.seq === seq);
  }, [questions, seq]);

  // Current chapter
  const chapter = useMemo(() => {
    if (!question) return null;
    return chapters.find(c => c.id === question.chapter);
  }, [chapters, question]);

  // Leads to question (the question that builds on this seq)
  const leadsToQuestion = useMemo(() => {
    return questions.find(q => q.buildsOn === seq);
  }, [questions, seq]);

  // Builds on question
  const buildsOnQuestion = useMemo(() => {
    if (!question || !question.buildsOn) return null;
    return questions.find(q => q.seq === question.buildsOn);
  }, [questions, question]);

  // Sync notes when seq or progressMap changes
  useEffect(() => {
    setNotes(currentProgress?.notes || '');
    setNotesSaved(true);
  }, [seq, currentProgress?.notes]);

  // Fetch chapter solutions on demand
  useEffect(() => {
    if (!question?.chapter) return;
    const chId = question.chapter;

    if (!solutionsCache[chId]) {
      setLoadingSolution(true);
      fetch(`/data/solutions/${chId}.json`)
        .then(res => {
          if (!res.ok) throw new Error(`HTTP ${res.status}`);
          return res.json();
        })
        .then(data => {
          setSolutionsCache(prev => ({ ...prev, [chId]: data }));
        })
        .catch(err => {
          console.warn(`Could not load full solution for ${chId}:`, err);
        })
        .finally(() => {
          setLoadingSolution(false);
        });
    }
  }, [question?.chapter, solutionsCache]);

  // Current question's rich solution from chapter JSON
  const richSolution = useMemo(() => {
    if (!question?.chapter || !solutionsCache[question.chapter]) return null;
    const list = solutionsCache[question.chapter];
    return list.find(s => s.seq === seq);
  }, [question?.chapter, solutionsCache, seq]);

  // Language: java or python
  const language = user?.language || 'java';

  // Trigger Prism highlighting on content/tab change
  useEffect(() => {
    if (activePanel === 'code') {
      Prism.highlightAll();
    }
  }, [richSolution, codeSubTab, language, activePanel]);

  // Debounced auto-save notes
  useEffect(() => {
    if (notes === (currentProgress?.notes || '')) {
      setNotesSaved(true);
      return;
    }
    setNotesSaved(false);
    const timer = setTimeout(() => {
      updateProgress({
        questionSeq: seq,
        status: currentProgress?.status || 'todo',
        notes: notes.slice(0, 2000)
      });
      setNotesSaved(true);
    }, 800);
    return () => clearTimeout(timer);
  }, [notes, seq, currentProgress?.status, currentProgress?.notes, updateProgress]);

  if (!question) {
    return (
      <div className="panel" style={{ textAlign: 'center', padding: '3rem', margin: '2rem auto', maxWidth: '600px' }}>
        <h2>Question not found</h2>
        <p style={{ color: 'var(--text-muted)', marginTop: '0.5rem' }}>
          Sequence #{seq} does not exist in the 300 roadmap.
        </p>
        <Link to="/roadmap" className="btn-primary" style={{ marginTop: '1rem', display: 'inline-flex' }}>
          Back to Roadmap
        </Link>
      </div>
    );
  }

  // Active solution data for Approach & Code
  const approachData = approachSubTab === 'optimal' 
    ? (richSolution?.optimal || question.optimal)
    : (richSolution?.brute || question.brute);

  const codeData = codeSubTab === 'optimal'
    ? (richSolution?.optimal || question.optimal)
    : (richSolution?.brute || question.brute);

  const currentCode = codeData?.code?.[language] || '// Solution code loading...';

  // Hints array
  const hints = richSolution?.hints || [
    "Think about whether you can avoid redundant work by storing intermediate state.",
    "Identify the core pattern or data structure that yields optimal asymptotic time.",
    "Formulate the complete invariant and transition steps before writing code."
  ];

  // Hint unlock handlers (Never changes question status)
  const unlockHint = (hintNum) => {
    if (hintNum > unlockedHintLevel) {
      setUnlockedHintLevel(hintNum);
      localStorage.setItem(`unlocked_hints_${seq}`, String(hintNum));
    }
    setActivePanel(`hint-${hintNum}`);
  };

  const handleCopy = () => {
    if (!currentCode) return;
    navigator.clipboard.writeText(currentCode);
    setCopied(true);
    showToast('Code copied to clipboard', 'info');
    setTimeout(() => setCopied(false), 2000);
  };

  const handleStatusChange = (newStatus) => {
    updateProgress({
      questionSeq: seq,
      status: newStatus,
      dueDate: newStatus === 'revisit' ? revisitDate : null
    });
  };

  const handleMistakeToggle = () => {
    const isMistake = Boolean(currentProgress?.mistake);
    updateProgress({
      questionSeq: seq,
      status: currentProgress?.status || 'todo',
      mistake: !isMistake
    });
    showToast(!isMistake ? 'Flagged as mistake for review' : 'Mistake tag removed', 'info');
  };

  const handleQuickRevisit = (days) => {
    const d = new Date();
    d.setDate(d.getDate() + days);
    const dateStr = d.toISOString().split('T')[0];
    setRevisitDate(dateStr);
    updateProgress({
      questionSeq: seq,
      status: 'revisit',
      dueDate: dateStr
    });
    showToast(`Scheduled revisit for ${dateStr}`, 'info');
  };

  const currentStatus = currentProgress?.status || 'todo';
  const isMistake = Boolean(currentProgress?.mistake);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem', width: '100%', maxWidth: '1440px', margin: '0 auto' }}>
      {/* Top Nav Strip: Previous / Sequence indicator / Next */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0.2rem 0' }}>
        <button
          onClick={() => navigate(`/question/${Math.max(1, seq - 1)}`)}
          disabled={seq <= 1}
          className="btn-secondary"
          style={{ padding: '0.35rem 0.75rem', fontSize: '0.8rem' }}
        >
          <ArrowLeft size={13} />
          <span>Prev (#{Math.max(1, seq - 1)})</span>
        </button>

        <Link to={`/roadmap#${question.chapter}`} style={{ fontSize: '0.825rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
          <span>{chapter ? chapter.name : `Chapter ${question.chapter}`}</span>
          <span style={{ fontFamily: 'var(--font-mono)' }}>({seq}/300)</span>
        </Link>

        <button
          onClick={() => navigate(`/question/${Math.min(300, seq + 1)}`)}
          disabled={seq >= 300}
          className="btn-secondary"
          style={{ padding: '0.35rem 0.75rem', fontSize: '0.8rem' }}
        >
          <span>Next (#{Math.min(300, seq + 1)})</span>
          <ArrowRight size={13} />
        </button>
      </div>

      {/* Split Layout: Left Panel & Right Editor Panel */}
      <div className="question-split-container">
        
        {/* LEFT PANEL: Details, Context, Actions, Notes */}
        <div className="question-left-panel">
          {/* Main Info Box */}
          <div className="panel" style={{ padding: '1.25rem' }}>
            {/* Header info */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem', flexWrap: 'wrap' }}>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.85rem', color: 'var(--accent)', fontWeight: 700 }}>
                #{seq}
              </span>
              <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                · LC #{question.lc}
              </span>
              <span className={`chip-${question.difficulty.toLowerCase()}`}>
                {question.difficulty}
              </span>
              {chapter && (
                <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', background: 'var(--bg-input)', padding: '0.15rem 0.45rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border)' }}>
                  {chapter.name}
                </span>
              )}
            </div>

            {/* Title */}
            <h1 style={{ fontSize: '1.45rem', fontWeight: 700, letterSpacing: '-0.02em', marginBottom: '1rem', color: 'var(--text-main)' }}>
              {question.title}
            </h1>

            {/* Action Bar: LeetCode Button (Orange Outline) + Status Dropdown + Mistake Button */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', flexWrap: 'wrap', marginBottom: '1rem' }}>
              {/* LeetCode Button (Orange Outline) */}
              <a
                href={`https://leetcode.com/problems/${question.slug}/`}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-outline-orange"
              >
                <span>Solve on LeetCode</span>
                <ExternalLink size={13} />
              </a>

              {/* Status Dropdown */}
              <select
                value={currentStatus}
                onChange={(e) => handleStatusChange(e.target.value)}
                className="select"
                style={{
                  fontWeight: 600,
                  fontSize: '0.825rem',
                  padding: '0.4rem 0.65rem',
                  borderColor: currentStatus === 'done' ? 'var(--status-done)' : currentStatus === 'in_progress' ? 'var(--status-inprogress)' : currentStatus === 'revisit' ? 'var(--status-revisit)' : 'var(--border)'
                }}
              >
                <option value="todo">Todo</option>
                <option value="in_progress">In Progress</option>
                <option value="done">Solved (Done)</option>
                <option value="revisit">Revisit</option>
              </select>

              {/* Mistake Toggle */}
              <button
                onClick={handleMistakeToggle}
                className="btn-secondary"
                title={isMistake ? 'Flagged as a mistake' : 'Flag this question as a mistake'}
                style={{
                  padding: '0.4rem 0.65rem',
                  borderColor: isMistake ? 'var(--status-mistake)' : 'var(--border)',
                  background: isMistake ? 'var(--status-mistake-bg)' : 'transparent',
                  color: isMistake ? 'var(--status-mistake)' : 'var(--text-muted)'
                }}
              >
                <AlertTriangle size={14} color={isMistake ? 'var(--status-mistake)' : 'currentColor'} />
                <span style={{ fontSize: '0.8rem' }}>Mistake</span>
              </button>
            </div>

            {/* Revisit Scheduler Bar if status is Revisit */}
            {currentStatus === 'revisit' && (
              <div style={{
                marginBottom: '1rem',
                padding: '0.65rem 0.85rem',
                background: 'var(--status-revisit-bg)',
                border: '1px solid rgba(138, 156, 168, 0.3)',
                borderRadius: 'var(--radius-sm)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                flexWrap: 'wrap',
                gap: '0.5rem',
                fontSize: '0.8rem'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--status-revisit)', fontWeight: 600 }}>
                  <Clock size={14} />
                  <span>Due:</span>
                  <input
                    type="date"
                    value={revisitDate}
                    onChange={(e) => {
                      setRevisitDate(e.target.value);
                      updateProgress({ questionSeq: seq, status: 'revisit', dueDate: e.target.value });
                    }}
                    className="input"
                    style={{ padding: '0.2rem 0.4rem', fontSize: '0.78rem', height: '28px' }}
                  />
                </div>
                <div style={{ display: 'flex', gap: '0.3rem' }}>
                  <button onClick={() => handleQuickRevisit(1)} className="btn-secondary" style={{ fontSize: '0.75rem', padding: '0.2rem 0.45rem' }}>Tomorrow</button>
                  <button onClick={() => handleQuickRevisit(3)} className="btn-secondary" style={{ fontSize: '0.75rem', padding: '0.2rem 0.45rem' }}>+3 Days</button>
                  <button onClick={() => handleQuickRevisit(7)} className="btn-secondary" style={{ fontSize: '0.75rem', padding: '0.2rem 0.45rem' }}>+1 Week</button>
                </div>
              </div>
            )}

            {/* Remind on Done Checkbox */}
            {currentStatus === 'done' && (
              <div style={{ marginBottom: '1rem', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                <label style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', cursor: 'pointer' }}>
                  <input
                    type="checkbox"
                    checked={remindOnDone}
                    onChange={(e) => {
                      setRemindOnDone(e.target.checked);
                      updateProgress({ questionSeq: seq, status: 'done', remind: e.target.checked });
                    }}
                  />
                  <span>Remind me again (Spaced repetition: 1, 3, 7, 21 days)</span>
                </label>
              </div>
            )}

            {/* Chain Transitions (Builds on / Leads to) */}
            <div style={{
              padding: '0.75rem',
              background: 'var(--bg-input)',
              borderRadius: 'var(--radius-sm)',
              border: '1px solid var(--border)',
              fontSize: '0.825rem',
              display: 'flex',
              flexDirection: 'column',
              gap: '0.4rem'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.5rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                  <Link2 size={14} color="var(--accent)" />
                  <span style={{ fontWeight: 600 }}>Builds On:</span>
                  {buildsOnQuestion ? (
                    <Link to={`/question/${buildsOnQuestion.seq}`} style={{ color: 'var(--accent)', fontWeight: 600 }}>
                      #{buildsOnQuestion.seq} {buildsOnQuestion.title}
                    </Link>
                  ) : (
                    <span style={{ color: 'var(--text-muted)' }}>Chapter foundation</span>
                  )}
                </div>

                {leadsToQuestion && (
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                    <span style={{ color: 'var(--text-muted)' }}>Leads to:</span>
                    <Link to={`/question/${leadsToQuestion.seq}`} style={{ color: 'var(--accent)', fontWeight: 600 }}>
                      #{leadsToQuestion.seq} {leadsToQuestion.title} →
                    </Link>
                  </div>
                )}
              </div>

              <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', lineHeight: 1.4 }}>
                <strong style={{ color: 'var(--text-sub)' }}>Why it follows: </strong>
                {richSolution?.whyNext || `Directly reinforces algorithmic techniques from #${buildsOnQuestion ? buildsOnQuestion.seq : 'fundamental concepts'}.`}
              </p>
            </div>
          </div>

          {/* Personal Notes Panel */}
          <div className="panel" style={{ padding: '1rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.85rem', fontWeight: 600 }}>
                <FileText size={15} color="var(--accent)" />
                <span>Personal Notes</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                <span>{notesSaved ? 'Saved' : 'Saving...'}</span>
                <span>{notes.length}/2000</span>
              </div>
            </div>

            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value.slice(0, 2000))}
              placeholder="Record your edge cases, pitfalls, or takeaways here (auto-saved)..."
              rows={5}
              className="input"
              style={{ width: '100%', resize: 'vertical', lineHeight: 1.5, fontFamily: 'var(--font-sans)', fontSize: '0.825rem' }}
            />
          </div>
        </div>

        {/* RIGHT PANEL: Flow Buttons & Guidance / Code / Approach */}
        <div className="question-right-panel">
          
          {/* Button Row: [Hint 1] [Hint 2] [Hint 3] [Approach] [Code] */}
          <div className="flow-btn-group">
            {/* Hint 1 */}
            <button
              onClick={() => unlockHint(1)}
              className={`flow-btn ${activePanel === 'hint-1' ? 'active' : unlockedHintLevel >= 1 ? 'unlocked' : ''}`}
            >
              <Lightbulb size={13} />
              <span>Hint 1</span>
            </button>

            {/* Hint 2 (unlocked when level >= 1) */}
            <button
              onClick={() => unlockHint(2)}
              disabled={unlockedHintLevel < 1}
              className={`flow-btn ${activePanel === 'hint-2' ? 'active' : unlockedHintLevel >= 2 ? 'unlocked' : ''}`}
              title={unlockedHintLevel < 1 ? 'Open Hint 1 first' : 'View Hint 2'}
            >
              {unlockedHintLevel < 1 ? <Lock size={12} /> : <Lightbulb size={13} />}
              <span>Hint 2</span>
            </button>

            {/* Hint 3 (unlocked when level >= 2) */}
            <button
              onClick={() => unlockHint(3)}
              disabled={unlockedHintLevel < 2}
              className={`flow-btn ${activePanel === 'hint-3' ? 'active' : unlockedHintLevel >= 3 ? 'unlocked' : ''}`}
              title={unlockedHintLevel < 2 ? 'Open Hint 2 first' : 'View Hint 3'}
            >
              {unlockedHintLevel < 2 ? <Lock size={12} /> : <Lightbulb size={13} />}
              <span>Hint 3</span>
            </button>

            {/* Approach button */}
            <button
              onClick={() => setActivePanel('approach')}
              className={`flow-btn ${activePanel === 'approach' ? 'active' : ''}`}
            >
              <BookOpen size={13} />
              <span>Approach</span>
            </button>

            {/* Code button */}
            <button
              onClick={() => setActivePanel('code')}
              className={`flow-btn ${activePanel === 'code' ? 'active' : ''}`}
            >
              <Code2 size={13} />
              <span>Code</span>
            </button>
          </div>

          {/* Panel Body depending on active selection */}
          
          {/* 1. INITIAL STATE: Nothing revealed yet */}
          {activePanel === null && (
            <div style={{
              flex: 1,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              padding: '3rem 1.5rem',
              textAlign: 'center',
              gap: '1rem',
              color: 'var(--text-muted)'
            }}>
              <div style={{
                width: 48,
                height: 48,
                borderRadius: 'var(--radius-sm)',
                background: 'var(--bg-input)',
                border: '1px solid var(--border)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'var(--accent)'
              }}>
                <Sparkles size={24} />
              </div>
              <div style={{ maxWidth: '380px' }}>
                <h3 style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--text-main)', marginBottom: '0.35rem' }}>
                  Solution Guidance
                </h3>
                <p style={{ fontSize: '0.825rem', lineHeight: 1.5 }}>
                  Select an option above to view hints, algorithmic approach, or code. Hints unlock in sequence to prevent accidental spoilers.
                </p>
              </div>

              <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.5rem' }}>
                <button
                  onClick={() => unlockHint(1)}
                  className="btn-primary"
                  style={{ fontSize: '0.8rem', padding: '0.35rem 0.85rem' }}
                >
                  <Lightbulb size={13} />
                  <span>Reveal Hint 1</span>
                </button>
                <button
                  onClick={() => setActivePanel('code')}
                  className="btn-secondary"
                  style={{ fontSize: '0.8rem', padding: '0.35rem 0.85rem' }}
                >
                  <Code2 size={13} />
                  <span>Go to Code</span>
                </button>
              </div>
            </div>
          )}

          {/* 2. HINTS VIEW */}
          {(activePanel === 'hint-1' || activePanel === 'hint-2' || activePanel === 'hint-3') && (
            <div style={{ padding: '1.25rem', display: 'flex', flexDirection: 'column', gap: '1rem', overflowY: 'auto' }}>
              
              {/* Hint 1 Card */}
              <div style={{
                background: activePanel === 'hint-1' ? 'var(--bg-input)' : 'var(--bg-panel)',
                border: '1px solid',
                borderColor: activePanel === 'hint-1' ? 'var(--accent)' : 'var(--border)',
                borderRadius: 'var(--radius-md)',
                padding: '1rem'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--accent)', fontWeight: 600, fontSize: '0.85rem', marginBottom: '0.4rem' }}>
                  <Lightbulb size={14} />
                  <span>Hint 1: Conceptual Nudge</span>
                </div>
                <p style={{ fontSize: '0.875rem', lineHeight: 1.55, color: 'var(--text-main)' }}>
                  {hints[0]}
                </p>
              </div>

              {/* Hint 2 Card / Unlock Button */}
              {unlockedHintLevel >= 2 ? (
                <div style={{
                  background: activePanel === 'hint-2' ? 'var(--bg-input)' : 'var(--bg-panel)',
                  border: '1px solid',
                  borderColor: activePanel === 'hint-2' ? 'var(--accent)' : 'var(--border)',
                  borderRadius: 'var(--radius-md)',
                  padding: '1rem'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--accent)', fontWeight: 600, fontSize: '0.85rem', marginBottom: '0.4rem' }}>
                    <Lightbulb size={14} />
                    <span>Hint 2: Pattern & Data Structure</span>
                  </div>
                  <p style={{ fontSize: '0.875rem', lineHeight: 1.55, color: 'var(--text-main)' }}>
                    {hints[1]}
                  </p>
                </div>
              ) : (
                <div style={{
                  padding: '0.85rem',
                  border: '1px dashed var(--border)',
                  borderRadius: 'var(--radius-md)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  gap: '0.5rem'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                    <Lock size={13} />
                    <span>Hint 2 is currently locked</span>
                  </div>
                  <button
                    onClick={() => unlockHint(2)}
                    className="btn-secondary"
                    style={{ fontSize: '0.78rem', padding: '0.3rem 0.65rem' }}
                  >
                    Unlock Hint 2
                  </button>
                </div>
              )}

              {/* Hint 3 Card / Unlock Button */}
              {unlockedHintLevel >= 3 ? (
                <div style={{
                  background: activePanel === 'hint-3' ? 'var(--bg-input)' : 'var(--bg-panel)',
                  border: '1px solid',
                  borderColor: activePanel === 'hint-3' ? 'var(--accent)' : 'var(--border)',
                  borderRadius: 'var(--radius-md)',
                  padding: '1rem'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--accent)', fontWeight: 600, fontSize: '0.85rem', marginBottom: '0.4rem' }}>
                    <Lightbulb size={14} />
                    <span>Hint 3: Algorithmic Strategy</span>
                  </div>
                  <p style={{ fontSize: '0.875rem', lineHeight: 1.55, color: 'var(--text-main)' }}>
                    {hints[2]}
                  </p>
                </div>
              ) : unlockedHintLevel >= 2 ? (
                <div style={{
                  padding: '0.85rem',
                  border: '1px dashed var(--border)',
                  borderRadius: 'var(--radius-md)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  gap: '0.5rem'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                    <Lock size={13} />
                    <span>Hint 3 is currently locked</span>
                  </div>
                  <button
                    onClick={() => unlockHint(3)}
                    className="btn-secondary"
                    style={{ fontSize: '0.78rem', padding: '0.3rem 0.65rem' }}
                  >
                    Unlock Hint 3
                  </button>
                </div>
              ) : null}

              {/* Quick links to Approach or Code */}
              <div style={{ marginTop: '0.5rem', display: 'flex', gap: '0.5rem', justifyContent: 'flex-end' }}>
                <button
                  onClick={() => setActivePanel('approach')}
                  className="btn-secondary"
                  style={{ fontSize: '0.8rem', padding: '0.35rem 0.75rem' }}
                >
                  <span>View Approach</span>
                  <ArrowRight size={13} />
                </button>
              </div>
            </div>
          )}

          {/* 3. APPROACH VIEW */}
          {activePanel === 'approach' && (
            <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
              {/* Approach Sub-tabs */}
              <div style={{
                display: 'flex',
                borderBottom: '1px solid var(--border)',
                background: 'var(--bg-panel)',
                padding: '0 0.85rem'
              }}>
                <button
                  onClick={() => setApproachSubTab('optimal')}
                  style={{
                    padding: '0.65rem 1rem',
                    fontSize: '0.85rem',
                    fontWeight: 600,
                    border: 'none',
                    borderBottom: approachSubTab === 'optimal' ? '2px solid var(--accent)' : '2px solid transparent',
                    color: approachSubTab === 'optimal' ? 'var(--accent)' : 'var(--text-muted)',
                    background: 'transparent',
                    cursor: 'pointer'
                  }}
                >
                  Optimal Approach
                </button>
                <button
                  onClick={() => setApproachSubTab('brute')}
                  style={{
                    padding: '0.65rem 1rem',
                    fontSize: '0.85rem',
                    fontWeight: 600,
                    border: 'none',
                    borderBottom: approachSubTab === 'brute' ? '2px solid var(--medium)' : '2px solid transparent',
                    color: approachSubTab === 'brute' ? 'var(--medium)' : 'var(--text-muted)',
                    background: 'transparent',
                    cursor: 'pointer'
                  }}
                >
                  Brute Force
                </button>
              </div>

              {/* Approach Content */}
              <div style={{ padding: '1.25rem', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {/* Complexities */}
                <div style={{ display: 'flex', gap: '1.25rem', flexWrap: 'wrap' }}>
                  <div style={{ fontSize: '0.825rem' }}>
                    <span style={{ color: 'var(--text-muted)', marginRight: '0.4rem' }}>Time Complexity:</span>
                    <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 600, color: 'var(--accent)' }}>
                      {approachData?.time || 'O(n)'}
                    </span>
                  </div>
                  <div style={{ fontSize: '0.825rem' }}>
                    <span style={{ color: 'var(--text-muted)', marginRight: '0.4rem' }}>Space Complexity:</span>
                    <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 600, color: 'var(--status-revisit)' }}>
                      {approachData?.space || 'O(1)'}
                    </span>
                  </div>
                </div>

                {/* Why slow banner (if Brute Force) */}
                {approachSubTab === 'brute' && approachData?.whySlow && (
                  <div style={{
                    padding: '0.75rem',
                    background: 'var(--medium-bg)',
                    border: '1px solid rgba(255, 192, 30, 0.3)',
                    borderRadius: 'var(--radius-sm)',
                    fontSize: '0.825rem'
                  }}>
                    <strong style={{ color: 'var(--medium)' }}>Why this is too slow: </strong>
                    <span style={{ color: 'var(--text-main)' }}>{approachData.whySlow}</span>
                  </div>
                )}

                {/* Idea */}
                <div>
                  <h4 style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.35rem' }}>
                    Core Idea
                  </h4>
                  <p style={{ fontSize: '0.9rem', color: 'var(--text-main)', lineHeight: 1.55 }}>
                    {approachData?.idea}
                  </p>
                </div>

                {/* Numbered Steps */}
                {approachData?.steps && approachData.steps.length > 0 && (
                  <div>
                    <h4 style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.45rem' }}>
                      Algorithmic Steps
                    </h4>
                    <ol style={{ paddingLeft: '1.25rem', display: 'flex', flexDirection: 'column', gap: '0.35rem', fontSize: '0.875rem', color: 'var(--text-main)', lineHeight: 1.5 }}>
                      {approachData.steps.map((st, idx) => (
                        <li key={idx}>{st}</li>
                      ))}
                    </ol>
                  </div>
                )}

                {/* Direct link to Code */}
                <div style={{ marginTop: '0.5rem', display: 'flex', justifyContent: 'flex-end' }}>
                  <button
                    onClick={() => {
                      setCodeSubTab(approachSubTab);
                      setActivePanel('code');
                    }}
                    className="btn-primary"
                    style={{ fontSize: '0.8rem', padding: '0.35rem 0.85rem' }}
                  >
                    <span>View Solution Code</span>
                    <ArrowRight size={13} />
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* 4. CODE VIEW */}
          {activePanel === 'code' && (
            <div style={{ display: 'flex', flexDirection: 'column', height: '100%', minHeight: '480px' }}>
              {/* Header Bar: Brute/Optimal tabs + Java/Python switch + Copy button */}
              <div className="code-editor-header">
                {/* Approach tabs */}
                <div style={{ display: 'flex', gap: '0.35rem' }}>
                  <button
                    onClick={() => setCodeSubTab('optimal')}
                    style={{
                      padding: '0.25rem 0.6rem',
                      fontSize: '0.78rem',
                      fontWeight: 600,
                      borderRadius: 'var(--radius-sm)',
                      border: '1px solid',
                      borderColor: codeSubTab === 'optimal' ? 'var(--accent)' : 'transparent',
                      background: codeSubTab === 'optimal' ? 'var(--accent-light)' : 'transparent',
                      color: codeSubTab === 'optimal' ? 'var(--accent)' : 'var(--text-muted)',
                      cursor: 'pointer'
                    }}
                  >
                    Optimal
                  </button>
                  <button
                    onClick={() => setCodeSubTab('brute')}
                    style={{
                      padding: '0.25rem 0.6rem',
                      fontSize: '0.78rem',
                      fontWeight: 600,
                      borderRadius: 'var(--radius-sm)',
                      border: '1px solid',
                      borderColor: codeSubTab === 'brute' ? 'var(--medium)' : 'transparent',
                      background: codeSubTab === 'brute' ? 'var(--medium-bg)' : 'transparent',
                      color: codeSubTab === 'brute' ? 'var(--medium)' : 'var(--text-muted)',
                      cursor: 'pointer'
                    }}
                  >
                    Brute Force
                  </button>
                </div>

                {/* Right controls: Language Switch + Copy */}
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <div style={{ display: 'flex', gap: '0.2rem', background: '#181818', padding: '2px', borderRadius: 'var(--radius-sm)' }}>
                    <button
                      onClick={() => updateSettings({ language: 'java' })}
                      style={{
                        padding: '0.2rem 0.5rem',
                        fontSize: '0.75rem',
                        fontWeight: 600,
                        border: 'none',
                        borderRadius: 'var(--radius-sm)',
                        background: language === 'java' ? 'var(--accent)' : 'transparent',
                        color: language === 'java' ? '#1A1A1A' : 'var(--text-muted)',
                        cursor: 'pointer'
                      }}
                    >
                      Java
                    </button>
                    <button
                      onClick={() => updateSettings({ language: 'python' })}
                      style={{
                        padding: '0.2rem 0.5rem',
                        fontSize: '0.75rem',
                        fontWeight: 600,
                        border: 'none',
                        borderRadius: 'var(--radius-sm)',
                        background: language === 'python' ? 'var(--accent)' : 'transparent',
                        color: language === 'python' ? '#1A1A1A' : 'var(--text-muted)',
                        cursor: 'pointer'
                      }}
                    >
                      Python
                    </button>
                  </div>

                  <button
                    onClick={handleCopy}
                    className="btn-secondary"
                    style={{ padding: '0.25rem 0.6rem', fontSize: '0.75rem' }}
                    title="Copy code"
                  >
                    {copied ? <Check size={13} color="var(--status-done)" /> : <Copy size={13} />}
                    <span>{copied ? 'Copied' : 'Copy'}</span>
                  </button>
                </div>
              </div>

              {/* Code Container */}
              <div className="code-container">
                <pre className={`language-${language}`}>
                  <code className={`language-${language}`}>
                    {currentCode}
                  </code>
                </pre>
              </div>

              {/* Complexity footer */}
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                padding: '0.5rem 0.85rem',
                borderTop: '1px solid var(--border)',
                background: 'var(--bg-panel)',
                fontSize: '0.78rem',
                color: 'var(--text-muted)'
              }}>
                <div>
                  <span>Time: </span>
                  <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 600, color: 'var(--accent)' }}>
                    {codeData?.time || 'O(n)'}
                  </span>
                </div>
                <div>
                  <span>Space: </span>
                  <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 600, color: 'var(--status-revisit)' }}>
                    {codeData?.space || 'O(1)'}
                  </span>
                </div>
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  );
}

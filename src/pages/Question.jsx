import React, { useState, useEffect, useMemo, useRef } from 'react';
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
  FileText,
  Circle,
  CheckCircle2,
  RotateCcw,
  ChevronDown
} from 'lucide-react';

const STATUS_OPTIONS = [
  { value: 'todo', label: 'Todo', icon: Circle, color: 'var(--text-muted)' },
  { value: 'in_progress', label: 'In Progress', icon: Clock, color: '#F59E0B' },
  { value: 'done', label: 'Solved (Done)', icon: CheckCircle2, color: '#10B981' },
  { value: 'revisit', label: 'Revisit', icon: RotateCcw, color: 'var(--revisit-color)' }
];

export default function Question() {
  const { seq: seqParam } = useParams();
  const navigate = useNavigate();
  const seq = parseInt(seqParam, 10);

  const { 
    questions, 
    chapters, 
    loadingData,
    progressMap, 
    updateProgress, 
    user, 
    language,
    updateLanguage, 
    showToast 
  } = useApp();

  // Active view in right panel: null (initial), 'hint-1', 'hint-2', 'hint-3', 'approach', 'code'
  const [activePanel, setActivePanel] = useState(() => {
    try {
      const params = new URLSearchParams(window.location.search);
      return params.get('panel') || null;
    } catch (_) {
      return null;
    }
  });

  // Approach / Code sub-tab: 'optimal' or 'brute'
  const [approachSubTab, setApproachSubTab] = useState('optimal');
  const [codeSubTab, setCodeSubTab] = useState('optimal');

  // Copy code feedback
  const [copied, setCopied] = useState(false);

  // Cached chapter solutions
  const [solutionsCache, setSolutionsCache] = useState({});
  const [loadingSolution, setLoadingSolution] = useState(false);

  // Custom Glass Status Dropdown state
  const [statusDropdownOpen, setStatusDropdownOpen] = useState(false);
  const statusDropdownRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(event) {
      if (statusDropdownRef.current && !statusDropdownRef.current.contains(event.target)) {
        setStatusDropdownOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

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
    try {
      const params = new URLSearchParams(window.location.search);
      const urlPanel = params.get('panel');
      if (urlPanel) {
        setActivePanel(urlPanel);
        return;
      }
    } catch (_) {}
    setActivePanel(null); // Keep clean initial view with only buttons shown
  }, [seq]);

  // Current question object from static questions.json
  const question = useMemo(() => {
    return questions.find(q => q.seq === seq);
  }, [questions, seq]);

  // Current progress entry
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

  // Trigger Prism highlighting on content/tab change or language change
  useEffect(() => {
    if (activePanel === 'code') {
      setTimeout(() => Prism.highlightAll(), 0);
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

  if (loadingData || (questions.length === 0 && !question)) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', width: '100%', paddingTop: '0.25rem' }}>
        <div className="question-grid-container" style={{ display: 'grid', gridTemplateColumns: 'repeat(12, 1fr)', gap: '1.5rem' }}>
          <div className="question-col-5" style={{ gridColumn: 'span 5' }}>
            <div className="glass-card skeleton" style={{ height: '520px', borderRadius: 'var(--radius-card)' }} />
          </div>
          <div className="question-col-7" style={{ gridColumn: 'span 7' }}>
            <div className="glass-card skeleton" style={{ height: '520px', borderRadius: 'var(--radius-card)' }} />
          </div>
        </div>
      </div>
    );
  }

  if (!question) {
    return (
      <div className="glass-card" style={{ textAlign: 'center', padding: '3rem', margin: '3rem auto', maxWidth: '540px' }}>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '0.5rem' }}>Question not found</h2>
        <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem', fontSize: '0.9rem' }}>
          Sequence #{seq} does not exist in the 300 roadmap.
        </p>
        <Link to="/roadmap" className="btn-primary" style={{ display: 'inline-flex' }}>
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

  // Hint unlock handlers (Never changes question status per Section 5.5)
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
  const currentStatusObj = STATUS_OPTIONS.find(s => s.value === currentStatus) || STATUS_OPTIONS[0];
  const CurrentStatusIcon = currentStatusObj.icon;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', width: '100%', paddingTop: '0.25rem' }}>
      {/* 5 / 7 Column Split Layout (Section 5.5) */}
      <div className="question-grid-container" style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(12, 1fr)',
        gap: '1.5rem',
        alignItems: 'start'
      }}>
        
        {/* LEFT 5 COLUMNS: Question Details, Links, Actions, Notes */}
        <div className="question-col-5" style={{
          gridColumn: 'span 5',
          display: 'flex',
          flexDirection: 'column',
          gap: '1.25rem'
        }}>
          {/* Main Info Glass Card */}
          <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '1.15rem' }}>
            {/* Mono label (Seq, chapter, difficulty) */}
            <div style={{ 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'space-between',
              flexWrap: 'wrap',
              gap: '0.5rem'
            }}>
              <div style={{ 
                fontFamily: 'var(--font-mono)', 
                fontSize: '0.8rem', 
                fontWeight: 600, 
                color: 'var(--text-muted)',
                letterSpacing: '0.04em'
              }}>
                SEQ #{String(seq).padStart(3, '0')} · LC #{question.lc}
              </div>

              <span className={`diff-pill diff-pill-${question.difficulty.toLowerCase()}`}>
                {question.difficulty}
              </span>
            </div>

            {/* Title */}
            <div>
              <div style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.25rem' }}>
                {chapter ? chapter.name : `Chapter ${question.chapter}`}
              </div>
              <h1 style={{ 
                fontSize: '1.55rem', 
                fontWeight: 700, 
                lineHeight: 1.25, 
                letterSpacing: '-0.02em', 
                color: 'var(--text-color)' 
              }}>
                {question.title}
              </h1>
            </div>

            {/* Builds on and Leads to links */}
            <div style={{
              padding: '14px 16px',
              borderRadius: 'var(--radius-inner)',
              background: 'var(--glass-surface)',
              border: '1px solid var(--glass-border)',
              display: 'flex',
              flexDirection: 'column',
              gap: '0.65rem',
              fontSize: '0.825rem'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.5rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
                  <Link2 size={15} color="var(--accent)" />
                  <span style={{ fontWeight: 600, color: 'var(--text-color)' }}>Builds on:</span>
                  {buildsOnQuestion ? (
                    <Link 
                      to={`/question/${buildsOnQuestion.seq}`} 
                      style={{ color: 'var(--accent)', fontWeight: 700, textDecoration: 'underline' }}
                    >
                      #{buildsOnQuestion.seq} {buildsOnQuestion.title}
                    </Link>
                  ) : (
                    <span style={{ color: 'var(--text-muted)' }}>Chapter foundation</span>
                  )}
                </div>

                {leadsToQuestion && (
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                    <span style={{ color: 'var(--text-muted)' }}>Leads to:</span>
                    <Link 
                      to={`/question/${leadsToQuestion.seq}`} 
                      style={{ color: 'var(--accent)', fontWeight: 700, textDecoration: 'underline' }}
                    >
                      #{leadsToQuestion.seq} →
                    </Link>
                  </div>
                )}
              </div>

              <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', lineHeight: 1.45, margin: 0 }}>
                <strong style={{ color: 'var(--text-color)' }}>Why it follows: </strong>
                {richSolution?.whyNext || `Directly reinforces algorithmic techniques from #${buildsOnQuestion ? buildsOnQuestion.seq : 'core concepts'}.`}
              </p>
            </div>

            {/* Action Buttons: Open on LeetCode + Glass Status Selector + Mistake Toggle */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', flexWrap: 'wrap' }}>
                {/* Open on LeetCode */}
                <a
                  href={`https://leetcode.com/problems/${question.slug}/`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-secondary"
                  style={{ 
                    flex: '1 1 150px', 
                    padding: '0.5rem 0.85rem', 
                    fontSize: '0.825rem',
                    justifyContent: 'center'
                  }}
                >
                  <span>Open on LeetCode</span>
                  <ExternalLink size={14} />
                </a>

                {/* Custom Glass-Style Status Dropdown (SRS 2.0 Part A #6) */}
                <div style={{ position: 'relative', flex: '1 1 150px' }} ref={statusDropdownRef}>
                  <button
                    type="button"
                    onClick={() => setStatusDropdownOpen(!statusDropdownOpen)}
                    className="btn-secondary"
                    style={{
                      width: '100%',
                      padding: '0.5rem 0.85rem',
                      fontSize: '0.825rem',
                      fontWeight: 600,
                      justifyContent: 'space-between',
                      borderRadius: 'var(--radius-pill)',
                      borderColor: currentStatus === 'done' ? '#10B981' : currentStatus === 'revisit' ? 'var(--revisit-color)' : currentStatus === 'in_progress' ? '#F59E0B' : 'var(--glass-border)',
                      background: 'var(--glass-surface)',
                      color: 'var(--text-color)'
                    }}
                    aria-haspopup="listbox"
                    aria-expanded={statusDropdownOpen}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
                      <CurrentStatusIcon size={14} color={currentStatusObj.color} />
                      <span>{currentStatusObj.label}</span>
                    </div>
                    <ChevronDown size={14} style={{ opacity: 0.6, transform: statusDropdownOpen ? 'rotate(180deg)' : 'none', transition: 'transform 150ms ease' }} />
                  </button>

                  {statusDropdownOpen && (
                    <div
                      style={{
                        position: 'absolute',
                        top: 'calc(100% + 6px)',
                        left: 0,
                        right: 0,
                        zIndex: 100,
                        background: 'var(--glass-strong)',
                        backdropFilter: 'blur(24px)',
                        WebkitBackdropFilter: 'blur(24px)',
                        border: '1px solid var(--glass-border)',
                        borderRadius: 'var(--radius-inner)',
                        boxShadow: 'var(--card-shadow)',
                        padding: '6px',
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '3px'
                      }}
                      role="listbox"
                    >
                      {STATUS_OPTIONS.map((opt) => {
                        const Icon = opt.icon;
                        const isSelected = opt.value === currentStatus;
                        return (
                          <button
                            key={opt.value}
                            type="button"
                            onClick={() => {
                              handleStatusChange(opt.value);
                              setStatusDropdownOpen(false);
                            }}
                            style={{
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'space-between',
                              padding: '8px 12px',
                              borderRadius: 'var(--radius-sm)',
                              border: 'none',
                              background: isSelected ? 'var(--accent-soft)' : 'transparent',
                              color: isSelected ? 'var(--text-color)' : 'var(--text-muted)',
                              fontSize: '0.825rem',
                              fontWeight: 600,
                              cursor: 'pointer',
                              textAlign: 'left',
                              transition: 'background 120ms ease'
                            }}
                            onMouseEnter={(e) => { if (!isSelected) e.currentTarget.style.background = 'var(--glass-surface)'; }}
                            onMouseLeave={(e) => { if (!isSelected) e.currentTarget.style.background = 'transparent'; }}
                          >
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                              <Icon size={14} color={opt.color} />
                              <span>{opt.label}</span>
                            </div>
                            {isSelected && <Check size={14} color="var(--accent)" />}
                          </button>
                        );
                      })}
                    </div>
                  )}
                </div>

                {/* Mistake Toggle */}
                <button
                  type="button"
                  onClick={handleMistakeToggle}
                  className="btn-secondary"
                  style={{
                    padding: '0.5rem 0.85rem',
                    fontSize: '0.825rem',
                    borderColor: isMistake ? '#EF4444' : 'var(--glass-border)',
                    background: isMistake ? 'rgba(239, 68, 68, 0.15)' : 'var(--glass-surface)',
                    color: isMistake ? '#EF4444' : 'var(--text-muted)'
                  }}
                  title={isMistake ? 'Flagged as a mistake' : 'Flag this question as a mistake'}
                >
                  <AlertTriangle size={15} color={isMistake ? '#EF4444' : 'currentColor'} />
                  <span>Mistake</span>
                </button>
              </div>

              {/* Revisit Scheduler Options */}
              {currentStatus === 'revisit' && (
                <div style={{
                  padding: '10px 14px',
                  borderRadius: 'var(--radius-inner)',
                  background: 'var(--revisit-bg)',
                  border: '1px solid var(--revisit-color)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  flexWrap: 'wrap',
                  gap: '0.5rem',
                  fontSize: '0.8rem'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', color: 'var(--revisit-color)', fontWeight: 600 }}>
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
                      style={{ padding: '0.2rem 0.45rem', fontSize: '0.78rem', height: '30px' }}
                    />
                  </div>
                  <div style={{ display: 'flex', gap: '0.35rem' }}>
                    <button type="button" onClick={() => handleQuickRevisit(1)} className="btn-secondary" style={{ fontSize: '0.72rem', padding: '0.2rem 0.5rem' }}>+1d</button>
                    <button type="button" onClick={() => handleQuickRevisit(3)} className="btn-secondary" style={{ fontSize: '0.72rem', padding: '0.2rem 0.5rem' }}>+3d</button>
                    <button type="button" onClick={() => handleQuickRevisit(7)} className="btn-secondary" style={{ fontSize: '0.72rem', padding: '0.2rem 0.5rem' }}>+7d</button>
                  </div>
                </div>
              )}

              {/* Remind on Done Checkbox */}
              {currentStatus === 'done' && (
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', padding: '0 4px' }}>
                  <label style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
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
            </div>

            {/* Personal Notes (Section 5.5) */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', marginTop: '0.25rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-color)' }}>
                  <FileText size={15} color="var(--accent)" />
                  <span>Personal Notes</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  <span>{notesSaved ? 'Saved' : 'Saving...'}</span>
                  <span>·</span>
                  <span>{notes.length}/2000</span>
                </div>
              </div>

              <textarea
                value={notes}
                onChange={(e) => setNotes(e.target.value.slice(0, 2000))}
                placeholder="Record your edge cases, pitfalls, or takeaways here (auto-saved)..."
                rows={5}
                className="input"
                style={{ 
                  width: '100%', 
                  resize: 'vertical', 
                  lineHeight: 1.5, 
                  fontFamily: 'var(--font-sans)', 
                  fontSize: '0.85rem',
                  borderRadius: 'var(--radius-inner)'
                }}
              />
            </div>
          </div>
        </div>

        {/* RIGHT 7 COLUMNS: Button Row + Dynamic Panels (Approach/Code/Hints) */}
        <div className="question-col-7" style={{
          gridColumn: 'span 7',
          display: 'flex',
          flexDirection: 'column',
          gap: '1rem'
        }}>
          {/* Glass Card containing the 5 Button Row and Active Panel */}
          <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '1.25rem', minHeight: '520px' }}>
            
            {/* Glass Pill Button Row: [Hint 1] [Hint 2] [Hint 3] [Approach] [Code] + Language Switcher (SRS 2.0 Part A #1 & #3) */}
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              gap: '0.65rem',
              flexWrap: 'wrap',
              borderBottom: '1px solid var(--glass-border)',
              paddingBottom: '1rem'
            }}>
              {/* Five Buttons: Hint 1, Hint 2, Hint 3, Approach, Code */}
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
                {/* Hint 1 */}
                <button
                  type="button"
                  onClick={() => unlockHint(1)}
                  className={activePanel === 'hint-1' ? 'btn-primary' : 'btn-secondary'}
                  style={{
                    borderRadius: 'var(--radius-pill)',
                    padding: '0.45rem 0.9rem',
                    fontSize: '0.825rem'
                  }}
                >
                  <Lightbulb size={14} />
                  <span>Hint 1</span>
                </button>

                {/* Hint 2 (Locked until Hint 1 is opened) */}
                <button
                  type="button"
                  onClick={() => unlockHint(2)}
                  disabled={unlockedHintLevel < 1}
                  className={activePanel === 'hint-2' ? 'btn-primary' : 'btn-secondary'}
                  style={{
                    borderRadius: 'var(--radius-pill)',
                    padding: '0.45rem 0.9rem',
                    fontSize: '0.825rem',
                    opacity: unlockedHintLevel < 1 ? 0.45 : 1,
                    cursor: unlockedHintLevel < 1 ? 'not-allowed' : 'pointer'
                  }}
                  title={unlockedHintLevel < 1 ? 'Open Hint 1 first to unlock Hint 2' : 'View Hint 2'}
                >
                  {unlockedHintLevel < 1 ? <Lock size={13} /> : <Lightbulb size={14} />}
                  <span>Hint 2</span>
                </button>

                {/* Hint 3 (Locked until Hint 2 is opened) */}
                <button
                  type="button"
                  onClick={() => unlockHint(3)}
                  disabled={unlockedHintLevel < 2}
                  className={activePanel === 'hint-3' ? 'btn-primary' : 'btn-secondary'}
                  style={{
                    borderRadius: 'var(--radius-pill)',
                    padding: '0.45rem 0.9rem',
                    fontSize: '0.825rem',
                    opacity: unlockedHintLevel < 2 ? 0.45 : 1,
                    cursor: unlockedHintLevel < 2 ? 'not-allowed' : 'pointer'
                  }}
                  title={unlockedHintLevel < 2 ? 'Open Hint 2 first to unlock Hint 3' : 'View Hint 3'}
                >
                  {unlockedHintLevel < 2 ? <Lock size={13} /> : <Lightbulb size={14} />}
                  <span>Hint 3</span>
                </button>

                {/* Approach Button */}
                <button
                  type="button"
                  onClick={() => setActivePanel('approach')}
                  className={activePanel === 'approach' ? 'btn-primary' : 'btn-secondary'}
                  style={{
                    borderRadius: 'var(--radius-pill)',
                    padding: '0.45rem 0.9rem',
                    fontSize: '0.825rem'
                  }}
                >
                  <BookOpen size={14} />
                  <span>Approach</span>
                </button>

                {/* Code Button */}
                <button
                  type="button"
                  onClick={() => setActivePanel('code')}
                  className={activePanel === 'code' ? 'btn-primary' : 'btn-secondary'}
                  style={{
                    borderRadius: 'var(--radius-pill)',
                    padding: '0.45rem 0.9rem',
                    fontSize: '0.825rem'
                  }}
                >
                  <Code2 size={14} />
                  <span>Code</span>
                </button>
              </div>

              {/* Language Switcher (Java | Python) always accessible (SRS 2.0 Part A #1) */}
              <div style={{
                display: 'inline-flex',
                alignItems: 'center',
                background: 'var(--glass-surface)',
                border: '1px solid var(--glass-border)',
                padding: '2px',
                borderRadius: 'var(--radius-pill)'
              }}>
                <button
                  type="button"
                  onClick={() => updateLanguage('java')}
                  style={{
                    padding: '0.25rem 0.65rem',
                    fontSize: '0.75rem',
                    fontWeight: 700,
                    border: 'none',
                    borderRadius: 'var(--radius-pill)',
                    background: language === 'java' ? 'var(--accent)' : 'transparent',
                    color: language === 'java' ? 'var(--accent-text)' : 'var(--text-muted)',
                    cursor: 'pointer',
                    transition: 'all 150ms ease'
                  }}
                >
                  Java
                </button>
                <button
                  type="button"
                  onClick={() => updateLanguage('python')}
                  style={{
                    padding: '0.25rem 0.65rem',
                    fontSize: '0.75rem',
                    fontWeight: 700,
                    border: 'none',
                    borderRadius: 'var(--radius-pill)',
                    background: language === 'python' ? 'var(--accent)' : 'transparent',
                    color: language === 'python' ? 'var(--accent-text)' : 'var(--text-muted)',
                    cursor: 'pointer',
                    transition: 'all 150ms ease'
                  }}
                >
                  Python
                </button>
              </div>
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
                gap: '1.25rem',
                color: 'var(--text-muted)'
              }}>
                <div style={{
                  width: 54,
                  height: 54,
                  borderRadius: 'var(--radius-inner)',
                  background: 'var(--glass-surface)',
                  border: '1px solid var(--glass-border)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'var(--accent)'
                }}>
                  <Sparkles size={28} />
                </div>
                <div style={{ maxWidth: '420px' }}>
                  <h3 style={{ fontSize: '1.15rem', fontWeight: 700, color: 'var(--text-color)', marginBottom: '0.45rem' }}>
                    Solution Guidance
                  </h3>
                  <p style={{ fontSize: '0.875rem', lineHeight: 1.55 }}>
                    Select an option above to inspect progressive hints, the algorithmic approach, or the implementation code. Hints unlock in sequence.
                  </p>
                </div>

                <div style={{ display: 'flex', gap: '0.75rem', marginTop: '0.5rem', flexWrap: 'wrap' }}>
                  <button
                    type="button"
                    onClick={() => unlockHint(1)}
                    className="btn-primary"
                    style={{ fontSize: '0.825rem', padding: '0.45rem 1rem' }}
                  >
                    <Lightbulb size={14} />
                    <span>Reveal Hint 1</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => setActivePanel('code')}
                    className="btn-secondary"
                    style={{ fontSize: '0.825rem', padding: '0.45rem 1rem' }}
                  >
                    <Code2 size={14} />
                    <span>Go Straight to Code</span>
                  </button>
                </div>
              </div>
            )}

            {/* 2. HINTS VIEW */}
            {(activePanel === 'hint-1' || activePanel === 'hint-2' || activePanel === 'hint-3') && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', flex: 1 }}>
                {/* Hint 1 Card */}
                <div style={{
                  background: activePanel === 'hint-1' ? 'var(--accent-soft)' : 'var(--glass-surface)',
                  border: '1px solid',
                  borderColor: activePanel === 'hint-1' ? 'var(--accent)' : 'var(--glass-border)',
                  borderRadius: 'var(--radius-inner)',
                  padding: '1.1rem'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', color: 'var(--text-color)', fontWeight: 700, fontSize: '0.875rem', marginBottom: '0.45rem' }}>
                    <Lightbulb size={16} color="var(--accent)" />
                    <span>Hint 1: Conceptual Nudge</span>
                  </div>
                  <p style={{ fontSize: '0.9rem', lineHeight: 1.6, color: 'var(--text-color)' }}>
                    {hints[0]}
                  </p>
                </div>

                {/* Hint 2 Card / Unlock Button */}
                {unlockedHintLevel >= 2 ? (
                  <div style={{
                    background: activePanel === 'hint-2' ? 'var(--accent-soft)' : 'var(--glass-surface)',
                    border: '1px solid',
                    borderColor: activePanel === 'hint-2' ? 'var(--accent)' : 'var(--glass-border)',
                    borderRadius: 'var(--radius-inner)',
                    padding: '1.1rem'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', color: 'var(--text-color)', fontWeight: 700, fontSize: '0.875rem', marginBottom: '0.45rem' }}>
                      <Lightbulb size={16} color="var(--accent)" />
                      <span>Hint 2: Pattern & Data Structure</span>
                    </div>
                    <p style={{ fontSize: '0.9rem', lineHeight: 1.6, color: 'var(--text-color)' }}>
                      {hints[1]}
                    </p>
                  </div>
                ) : (
                  <div style={{
                    padding: '1rem',
                    border: '1px dashed var(--glass-border)',
                    borderRadius: 'var(--radius-inner)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    gap: '0.5rem'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                      <Lock size={15} />
                      <span>Hint 2 is locked</span>
                    </div>
                    <button
                      type="button"
                      onClick={() => unlockHint(2)}
                      className="btn-secondary"
                      style={{ fontSize: '0.8rem', padding: '0.35rem 0.75rem' }}
                    >
                      Unlock Hint 2
                    </button>
                  </div>
                )}

                {/* Hint 3 Card / Unlock Button */}
                {unlockedHintLevel >= 3 ? (
                  <div style={{
                    background: activePanel === 'hint-3' ? 'var(--accent-soft)' : 'var(--glass-surface)',
                    border: '1px solid',
                    borderColor: activePanel === 'hint-3' ? 'var(--accent)' : 'var(--glass-border)',
                    borderRadius: 'var(--radius-inner)',
                    padding: '1.1rem'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', color: 'var(--text-color)', fontWeight: 700, fontSize: '0.875rem', marginBottom: '0.45rem' }}>
                      <Lightbulb size={16} color="var(--accent)" />
                      <span>Hint 3: Algorithmic Strategy</span>
                    </div>
                    <p style={{ fontSize: '0.9rem', lineHeight: 1.6, color: 'var(--text-color)' }}>
                      {hints[2]}
                    </p>
                  </div>
                ) : unlockedHintLevel >= 2 ? (
                  <div style={{
                    padding: '1rem',
                    border: '1px dashed var(--glass-border)',
                    borderRadius: 'var(--radius-inner)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    gap: '0.5rem'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                      <Lock size={15} />
                      <span>Hint 3 is locked</span>
                    </div>
                    <button
                      type="button"
                      onClick={() => unlockHint(3)}
                      className="btn-secondary"
                      style={{ fontSize: '0.8rem', padding: '0.35rem 0.75rem' }}
                    >
                      Unlock Hint 3
                    </button>
                  </div>
                ) : null}

                {/* Quick link to Approach */}
                <div style={{ marginTop: 'auto', display: 'flex', justifyContent: 'flex-end', paddingTop: '1rem' }}>
                  <button
                    type="button"
                    onClick={() => setActivePanel('approach')}
                    className="btn-secondary"
                    style={{ fontSize: '0.825rem', padding: '0.45rem 0.9rem' }}
                  >
                    <span>View Algorithmic Approach</span>
                    <ArrowRight size={14} />
                  </button>
                </div>
              </div>
            )}

            {/* 3. APPROACH VIEW (Section 5.5: Brute force & Optimal tabs, idea, steps, complexity chips) */}
            {activePanel === 'approach' && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', flex: 1 }}>
                {/* Sub-tabs: Optimal vs Brute Force */}
                <div style={{ display: 'flex', gap: '0.5rem', borderBottom: '1px solid var(--glass-border)', paddingBottom: '0.65rem' }}>
                  <button
                    type="button"
                    onClick={() => setApproachSubTab('optimal')}
                    className={approachSubTab === 'optimal' ? 'btn-primary' : 'btn-secondary'}
                    style={{ padding: '0.4rem 0.85rem', fontSize: '0.825rem', borderRadius: 'var(--radius-pill)' }}
                  >
                    Optimal Approach
                  </button>
                  <button
                    type="button"
                    onClick={() => setApproachSubTab('brute')}
                    className={approachSubTab === 'brute' ? 'btn-primary' : 'btn-secondary'}
                    style={{ padding: '0.4rem 0.85rem', fontSize: '0.825rem', borderRadius: 'var(--radius-pill)' }}
                  >
                    Brute Force
                  </button>
                </div>

                {/* Complexity Chips */}
                <div style={{ display: 'flex', gap: '0.85rem', flexWrap: 'wrap' }}>
                  <div style={{
                    padding: '6px 14px',
                    borderRadius: 'var(--radius-pill)',
                    background: 'var(--glass-surface)',
                    border: '1px solid var(--glass-border)',
                    fontSize: '0.825rem',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.45rem'
                  }}>
                    <span style={{ color: 'var(--text-muted)' }}>Time:</span>
                    <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 700, color: 'var(--text-color)' }}>
                      {approachData?.time || 'O(n)'}
                    </span>
                  </div>

                  <div style={{
                    padding: '6px 14px',
                    borderRadius: 'var(--radius-pill)',
                    background: 'var(--glass-surface)',
                    border: '1px solid var(--glass-border)',
                    fontSize: '0.825rem',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.45rem'
                  }}>
                    <span style={{ color: 'var(--text-muted)' }}>Space:</span>
                    <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 700, color: 'var(--text-color)' }}>
                      {approachData?.space || 'O(1)'}
                    </span>
                  </div>
                </div>

                {/* Why slow banner (if Brute Force) */}
                {approachSubTab === 'brute' && approachData?.whySlow && (
                  <div style={{
                    padding: '12px 16px',
                    borderRadius: 'var(--radius-inner)',
                    background: 'rgba(245, 158, 11, 0.12)',
                    border: '1px solid rgba(245, 158, 11, 0.35)',
                    fontSize: '0.85rem',
                    color: 'var(--text-color)',
                    lineHeight: 1.5
                  }}>
                    <strong style={{ color: '#D97706' }}>Why this is too slow: </strong>
                    <span>{approachData.whySlow}</span>
                  </div>
                )}

                {/* Core Idea */}
                <div>
                  <h4 style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: '0.45rem' }}>
                    Core Idea
                  </h4>
                  <p style={{ fontSize: '0.925rem', color: 'var(--text-color)', lineHeight: 1.6 }}>
                    {approachData?.idea}
                  </p>
                </div>

                {/* Algorithmic Steps */}
                {approachData?.steps && approachData.steps.length > 0 && (
                  <div>
                    <h4 style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: '0.5rem' }}>
                      Algorithmic Steps
                    </h4>
                    <ol style={{ paddingLeft: '1.25rem', display: 'flex', flexDirection: 'column', gap: '0.45rem', fontSize: '0.9rem', color: 'var(--text-color)', lineHeight: 1.55 }}>
                      {approachData.steps.map((st, idx) => (
                        <li key={idx}>{st}</li>
                      ))}
                    </ol>
                  </div>
                )}

                {/* Action Link to Code */}
                <div style={{ marginTop: 'auto', display: 'flex', justifyContent: 'flex-end', paddingTop: '1rem' }}>
                  <button
                    type="button"
                    onClick={() => {
                      setCodeSubTab(approachSubTab);
                      setActivePanel('code');
                    }}
                    className="btn-primary"
                    style={{ fontSize: '0.825rem', padding: '0.45rem 1rem' }}
                  >
                    <span>View Solution Code</span>
                    <ArrowRight size={14} />
                  </button>
                </div>
              </div>
            )}

            {/* 4. CODE VIEW (Section 5.5: Brute force / Optimal tabs, Java/Python switch, Copy button, always dark #12152B editor) */}
            {activePanel === 'code' && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem', flex: 1 }}>
                {/* Header Controls: Sub-tabs + Language + Copy */}
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.75rem' }}>
                  {/* Approach Sub-tabs */}
                  <div style={{ display: 'flex', gap: '0.4rem' }}>
                    <button
                      type="button"
                      onClick={() => setCodeSubTab('optimal')}
                      className={codeSubTab === 'optimal' ? 'btn-primary' : 'btn-secondary'}
                      style={{ padding: '0.35rem 0.75rem', fontSize: '0.78rem', borderRadius: 'var(--radius-pill)' }}
                    >
                      Optimal
                    </button>
                    <button
                      type="button"
                      onClick={() => setCodeSubTab('brute')}
                      className={codeSubTab === 'brute' ? 'btn-primary' : 'btn-secondary'}
                      style={{ padding: '0.35rem 0.75rem', fontSize: '0.78rem', borderRadius: 'var(--radius-pill)' }}
                    >
                      Brute Force
                    </button>
                  </div>

                  {/* Language switch & Copy button */}
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <div style={{ 
                      display: 'flex', 
                      background: 'rgba(0, 0, 0, 0.45)', 
                      padding: '2px', 
                      borderRadius: 'var(--radius-pill)',
                      border: '1px solid var(--glass-border)'
                    }}>
                      <button
                        type="button"
                        onClick={() => updateLanguage('java')}
                        style={{
                          padding: '0.25rem 0.65rem',
                          fontSize: '0.75rem',
                          fontWeight: 700,
                          border: 'none',
                          borderRadius: 'var(--radius-pill)',
                          background: language === 'java' ? 'var(--accent)' : 'transparent',
                          color: language === 'java' ? 'var(--accent-text)' : 'var(--text-muted)',
                          cursor: 'pointer'
                        }}
                      >
                        Java
                      </button>
                      <button
                        type="button"
                        onClick={() => updateLanguage('python')}
                        style={{
                          padding: '0.25rem 0.65rem',
                          fontSize: '0.75rem',
                          fontWeight: 700,
                          border: 'none',
                          borderRadius: 'var(--radius-pill)',
                          background: language === 'python' ? 'var(--accent)' : 'transparent',
                          color: language === 'python' ? 'var(--accent-text)' : 'var(--text-muted)',
                          cursor: 'pointer'
                        }}
                      >
                        Python
                      </button>
                    </div>

                    <button
                      type="button"
                      onClick={handleCopy}
                      className="btn-secondary"
                      style={{ padding: '0.35rem 0.75rem', fontSize: '0.78rem' }}
                      title="Copy code to clipboard"
                    >
                      {copied ? <Check size={14} color="#10B981" /> : <Copy size={14} />}
                      <span>{copied ? 'Copied' : 'Copy'}</span>
                    </button>
                  </div>
                </div>

                {/* Code Container (Dark #12152B editor per Section 4.2) */}
                <div className="code-panel" style={{ flex: 1, minHeight: '380px' }}>
                  <pre className={`language-${language}`} style={{ margin: 0, padding: '18px', overflowX: 'auto' }}>
                    <code className={`language-${language}`}>
                      {currentCode}
                    </code>
                  </pre>
                </div>

                {/* Complexity Footer */}
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  padding: '8px 14px',
                  borderRadius: 'var(--radius-inner)',
                  background: 'var(--glass-surface)',
                  fontSize: '0.8rem',
                  color: 'var(--text-muted)'
                }}>
                  <div>
                    <span>Time Complexity: </span>
                    <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 700, color: 'var(--text-color)' }}>
                      {codeData?.time || 'O(n)'}
                    </span>
                  </div>
                  <div>
                    <span>Space Complexity: </span>
                    <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 700, color: 'var(--text-color)' }}>
                      {codeData?.space || 'O(1)'}
                    </span>
                  </div>
                </div>
              </div>
            )}

          </div>
        </div>
      </div>

      {/* Previous and Next Question Navigation Buttons at Bottom (Section 5.5) */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '1.25rem 0',
        marginTop: '0.5rem'
      }}>
        <button
          type="button"
          onClick={() => navigate(`/question/${Math.max(1, seq - 1)}`)}
          disabled={seq <= 1}
          className="btn-secondary"
          style={{ padding: '0.5rem 1rem', fontSize: '0.85rem' }}
        >
          <ArrowLeft size={15} />
          <span>Prev (#{Math.max(1, seq - 1)})</span>
        </button>

        <Link 
          to={`/roadmap#${question.chapter}`} 
          style={{ 
            fontSize: '0.85rem', 
            fontWeight: 600, 
            color: 'var(--text-muted)', 
            display: 'flex', 
            alignItems: 'center', 
            gap: '0.4rem' 
          }}
        >
          <span>{chapter ? chapter.name : `Chapter ${question.chapter}`}</span>
          <span style={{ fontFamily: 'var(--font-mono)' }}>({seq}/300)</span>
        </Link>

        <button
          type="button"
          onClick={() => navigate(`/question/${Math.min(300, seq + 1)}`)}
          disabled={seq >= 300}
          className="btn-secondary"
          style={{ padding: '0.5rem 1rem', fontSize: '0.85rem' }}
        >
          <span>Next (#{Math.min(300, seq + 1)})</span>
          <ArrowRight size={15} />
        </button>
      </div>
    </div>
  );
}

import React, { useState, useEffect, useMemo, useRef } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { 
  CheckCircle2, 
  Clock, 
  Circle, 
  AlertTriangle, 
  Link2, 
  ExternalLink, 
  Copy, 
  Check, 
  ChevronLeft, 
  ChevronRight, 
  Lightbulb, 
  Lock, 
  BookOpen, 
  Code2, 
  ArrowRight, 
  Sparkles,
  FileText,
  ChevronDown,
  ChevronUp
} from 'lucide-react';
import Prism from 'prismjs';
import 'prismjs/components/prism-java';
import 'prismjs/components/prism-python';

const STATUS_OPTIONS = [
  { value: 'todo', label: 'Todo', icon: Circle, color: 'var(--text-muted)' },
  { value: 'in_progress', label: 'In Progress', icon: Clock, color: '#F59E0B' },
  { value: 'done', label: 'Solved (Done)', icon: CheckCircle2, color: '#10B981' },
  { value: 'revisit', label: 'Revisit', icon: Clock, color: 'var(--revisit-color)' }
];

export default function Question() {
  const { seq: seqParam } = useParams();
  const seq = parseInt(seqParam, 10);
  const navigate = useNavigate();

  const { 
    questions, 
    chapters, 
    progressMap, 
    updateProgress, 
    showToast,
    language,
    updateLanguage,
    loadingData
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

  // Approach / Code sub-tab: 'brute' or 'optimal' (SRS 2.0 Part 1: Brute force first, default is brute)
  const [approachSubTab, setApproachSubTab] = useState('brute');
  const [codeSubTab, setCodeSubTab] = useState('brute');

  // Copy code feedback
  const [copied, setCopied] = useState(false);

  // Cached chapter solutions
  const [solutionsCache, setSolutionsCache] = useState({});
  const [loadingSolution, setLoadingSolution] = useState(false);

  // Custom Glass Status Dropdown state
  const [statusDropdownOpen, setStatusDropdownOpen] = useState(false);
  const statusDropdownRef = useRef(null);

  // Notes collapsible state (closed by default on mobile per Part 2 #6g)
  const [notesCollapsed, setNotesCollapsed] = useState(true);

  useEffect(() => {
    function handleClickOutside(event) {
      if (statusDropdownRef.current && !statusDropdownRef.current.contains(event.target)) {
        setStatusDropdownOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Current question data
  const question = useMemo(() => {
    return questions.find(q => q.seq === seq) || null;
  }, [questions, seq]);

  // Chapter data
  const chapter = useMemo(() => {
    if (!question) return null;
    return chapters.find(c => c.id === question.chapter) || null;
  }, [question, chapters]);

  // Builds on & Leads to questions
  const buildsOnQuestion = useMemo(() => {
    if (!question || !question.buildsOn) return null;
    return questions.find(q => q.seq === question.buildsOn) || null;
  }, [question, questions]);

  const leadsToQuestion = useMemo(() => {
    if (!question || !question.leadsTo || question.leadsTo.length === 0) return null;
    const nextSeq = question.leadsTo[0];
    return questions.find(q => q.seq === nextSeq) || null;
  }, [question, questions]);

  // Previous & Next questions in contiguous chain
  const prevQuestion = useMemo(() => {
    if (seq <= 1) return null;
    return questions.find(q => q.seq === seq - 1) || null;
  }, [seq, questions]);

  const nextQuestion = useMemo(() => {
    if (seq >= 300) return null;
    return questions.find(q => q.seq === seq + 1) || null;
  }, [seq, questions]);

  // Current user progress
  const currentProgress = progressMap[seq] || null;

  // Track unlocked hints in localStorage
  const unlockedStorageKey = `chainline_unlocked_hints_${seq}`;
  const [unlockedHintLevel, setUnlockedHintLevel] = useState(() => {
    try {
      const saved = localStorage.getItem(unlockedStorageKey);
      return saved ? parseInt(saved, 10) : 0;
    } catch (_) {
      return 0;
    }
  });

  const unlockHint = (hintNum) => {
    const newLvl = Math.max(unlockedHintLevel, hintNum);
    setUnlockedHintLevel(newLvl);
    try {
      localStorage.setItem(unlockedStorageKey, String(newLvl));
    } catch (_) {}
    setActivePanel(`hint-${hintNum}`);
  };

  // Local form states
  const [notes, setNotes] = useState(currentProgress?.notes || '');
  const [notesSaved, setNotesSaved] = useState(true);
  const [remindOnDone, setRemindOnDone] = useState(true);
  const [revisitDate, setRevisitDate] = useState(() => {
    const d = new Date();
    d.setDate(d.getDate() + 1);
    return d.toISOString().split('T')[0];
  });

  useEffect(() => {
    if (currentProgress) {
      setNotes(currentProgress.notes || '');
    } else {
      setNotes('');
    }
    // Reset view panel or sync with URL
    try {
      const params = new URLSearchParams(window.location.search);
      const urlPanel = params.get('panel');
      if (urlPanel && ['hint-1', 'hint-2', 'hint-3', 'approach', 'code'].includes(urlPanel)) {
        setActivePanel(urlPanel);
      } else {
        setActivePanel(null);
      }
    } catch (_) {
      setActivePanel(null);
    }
    // Default tabs to brute force per Part 1
    setApproachSubTab('brute');
    setCodeSubTab('brute');
    setStatusDropdownOpen(false);
  }, [seq]);

  // Fetch full solutions JSON for the chapter
  useEffect(() => {
    if (!question?.chapter) return;
    const chId = question.chapter;
    if (!solutionsCache[chId]) {
      setLoadingSolution(true);
      fetch(`/data/solutions/${chId}.json`)
        .then(res => res.json())
        .then(data => {
          setSolutionsCache(prev => ({ ...prev, [chId]: data }));
        })
        .catch(err => {
          console.error(`Failed to load solutions for ${chId}:`, err);
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
        <Link to="/roadmap" className="btn-primary" style={{ display: 'inline-flex', minHeight: '44px' }}>
          Back to Roadmap
        </Link>
      </div>
    );
  }

  // Active solution data for Approach & Code: Brute force first per Part 1
  const approachData = approachSubTab === 'brute'
    ? (richSolution?.brute || question.brute)
    : (richSolution?.optimal || question.optimal);

  const codeData = codeSubTab === 'brute'
    ? (richSolution?.brute || question.brute)
    : (richSolution?.optimal || question.optimal);

  const currentCode = codeData?.code?.[language] || '// Solution code loading...';

  // Hints array
  const hints = richSolution?.hints || [
    "Think about whether you can avoid redundant work by storing intermediate state.",
    "Identify the core pattern or data structure that yields optimal asymptotic time.",
    "Formulate the complete invariant and transition steps before writing code."
  ];

  const handleCopyCode = async () => {
    try {
      await navigator.clipboard.writeText(currentCode);
      setCopied(true);
      showToast('Solution code copied to clipboard', 'info');
      setTimeout(() => setCopied(false), 2000);
    } catch (_) {
      showToast('Failed to copy code to clipboard', 'error');
    }
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
    <div className="question-page-root" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', width: '100%', paddingTop: '0.25rem' }}>
      
      {/* 5 / 7 Column Split Layout on Desktop; Single Column in exact 8-step order on mobile */}
      <div className="question-grid-container" style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(12, 1fr)',
        gap: '1.5rem',
        alignItems: 'start'
      }}>
        
        {/* LEFT 5 COLUMNS: Details, Links, Actions, Notes, Navigation */}
        <div className="question-col-5" style={{
          gridColumn: 'span 5',
          display: 'flex',
          flexDirection: 'column',
          gap: '1.25rem'
        }}>
          
          {/* SECTION A: Chapter label & Title (Order 1 on mobile, 26px title, scroll-margin) */}
          <div className="glass-card question-header-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
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

            <div>
              <div className="question-chapter-label" style={{ fontSize: '0.825rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.25rem' }}>
                {chapter ? chapter.name : `Chapter ${question.chapter}`}
              </div>
              <h1 className="question-title-heading" style={{ 
                fontSize: '1.65rem', 
                fontWeight: 700, 
                lineHeight: 1.25, 
                letterSpacing: '-0.02em', 
                color: 'var(--text-color)' 
              }}>
                {question.title}
              </h1>
            </div>
          </div>

          {/* SECTION B: Builds on / Leads to card (Order 2 on mobile) */}
          <div className="glass-card question-builds-card" style={{
            padding: '16px 20px',
            display: 'flex',
            flexDirection: 'column',
            gap: '0.65rem',
            fontSize: '0.85rem'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.5rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
                <Link2 size={16} color="var(--accent)" />
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

            <p style={{ color: 'var(--text-muted)', fontSize: '0.825rem', lineHeight: 1.45, margin: 0 }}>
              <strong style={{ color: 'var(--text-color)' }}>Why it follows: </strong>
              {richSolution?.whyNext || `Directly reinforces algorithmic techniques from #${buildsOnQuestion ? buildsOnQuestion.seq : 'core concepts'}.`}
            </p>
          </div>

          {/* SECTION C: Open on LeetCode full-width + Status & Mistake row (Order 3 on mobile) */}
          <div className="glass-card question-actions-card" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
            {/* Full-width Open on LeetCode button */}
            <a
              href={`https://leetcode.com/problems/${question.slug}/`}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-secondary question-leetcode-btn"
              style={{ 
                width: '100%', 
                minHeight: '48px', 
                fontSize: '0.925rem',
                justifyContent: 'center',
                gap: '0.5rem'
              }}
            >
              <span>Open on LeetCode</span>
              <ExternalLink size={16} />
            </a>

            {/* Row with status dropdown and Mistake button side by side */}
            <div className="question-status-mistake-row" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
              {/* Glass Status Selector */}
              <div style={{ position: 'relative' }} ref={statusDropdownRef}>
                <button
                  type="button"
                  onClick={() => setStatusDropdownOpen(!statusDropdownOpen)}
                  className="btn-secondary"
                  style={{
                    width: '100%',
                    minHeight: '44px',
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
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', overflow: 'hidden' }}>
                    <CurrentStatusIcon size={15} color={currentStatusObj.color} style={{ flexShrink: 0 }} />
                    <span style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{currentStatusObj.label}</span>
                  </div>
                  <ChevronDown size={14} style={{ opacity: 0.6, flexShrink: 0, transform: statusDropdownOpen ? 'rotate(180deg)' : 'none', transition: 'transform 150ms ease' }} />
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
                            padding: '10px 12px',
                            minHeight: '44px',
                            borderRadius: 'var(--radius-sm)',
                            border: 'none',
                            background: isSelected ? 'var(--accent-soft)' : 'transparent',
                            color: isSelected ? 'var(--text-color)' : 'var(--text-muted)',
                            fontSize: '0.85rem',
                            fontWeight: 600,
                            cursor: 'pointer',
                            textAlign: 'left'
                          }}
                        >
                          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            <Icon size={15} color={opt.color} />
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
                  width: '100%',
                  minHeight: '44px',
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
                    className="glass-input"
                    style={{ padding: '0.2rem 0.45rem', fontSize: '16px', height: '36px', minHeight: '36px', width: 'auto' }}
                  />
                </div>
                <div style={{ display: 'flex', gap: '0.35rem' }}>
                  <button type="button" onClick={() => handleQuickRevisit(1)} className="btn-secondary" style={{ fontSize: '0.78rem', padding: '0.2rem 0.6rem', minHeight: '36px' }}>+1d</button>
                  <button type="button" onClick={() => handleQuickRevisit(3)} className="btn-secondary" style={{ fontSize: '0.78rem', padding: '0.2rem 0.6rem', minHeight: '36px' }}>+3d</button>
                  <button type="button" onClick={() => handleQuickRevisit(7)} className="btn-secondary" style={{ fontSize: '0.78rem', padding: '0.2rem 0.6rem', minHeight: '36px' }}>+7d</button>
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

          {/* SECTION G: Personal Notes in Collapsible Card (Order 6 on mobile, closed by default) */}
          <div className="glass-card question-notes-card" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
            <button
              type="button"
              onClick={() => setNotesCollapsed(!notesCollapsed)}
              className="question-notes-toggle-header"
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                width: '100%',
                background: 'none',
                border: 'none',
                padding: 0,
                cursor: 'pointer',
                textAlign: 'left'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.9rem', fontWeight: 700, color: 'var(--text-color)' }}>
                <FileText size={16} color="var(--accent)" />
                <span>Personal Notes</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  {notesSaved ? 'Saved' : 'Saving...'}
                </span>
                <span className="mobile-notes-chevron">
                  {notesCollapsed ? <ChevronDown size={16} /> : <ChevronUp size={16} />}
                </span>
              </div>
            </button>

            {/* Body of Notes - collapsible on mobile */}
            <div className={`question-notes-body ${notesCollapsed ? 'notes-collapsed-mobile' : ''}`}>
              <textarea
                value={notes}
                onChange={(e) => setNotes(e.target.value.slice(0, 2000))}
                placeholder="Record your edge cases, pitfalls, or takeaways here (auto-saved)..."
                rows={4}
                className="glass-input"
                style={{ 
                  width: '100%', 
                  resize: 'vertical', 
                  lineHeight: 1.5, 
                  fontFamily: 'var(--font-sans)', 
                  fontSize: '16px',
                  borderRadius: 'var(--radius-inner)'
                }}
              />
              <div style={{ textAlign: 'right', fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                {notes.length}/2000 characters
              </div>
            </div>
          </div>

          {/* SECTION H: Previous & Next Question Buttons (Order 7 on mobile, two equal buttons side by side) */}
          <div className="question-nav-footer" style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: '12px',
            width: '100%'
          }}>
            {prevQuestion ? (
              <button
                type="button"
                onClick={() => navigate(`/question/${prevQuestion.seq}`)}
                className="btn-secondary"
                style={{ width: '100%', minHeight: '48px', padding: '0.6rem 0.85rem', fontSize: '0.85rem', gap: '0.4rem', justifyContent: 'center' }}
                title={`Previous: #${prevQuestion.seq} ${prevQuestion.title}`}
              >
                <ChevronLeft size={16} />
                <span style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  #{prevQuestion.seq} Prev
                </span>
              </button>
            ) : (
              <div />
            )}

            {nextQuestion ? (
              <button
                type="button"
                onClick={() => navigate(`/question/${nextQuestion.seq}`)}
                className="btn-primary"
                style={{ width: '100%', minHeight: '48px', padding: '0.6rem 0.85rem', fontSize: '0.85rem', gap: '0.4rem', justifyContent: 'center' }}
                title={`Next: #${nextQuestion.seq} ${nextQuestion.title}`}
              >
                <span style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  Next #{nextQuestion.seq}
                </span>
                <ChevronRight size={16} />
              </button>
            ) : (
              <div />
            )}
          </div>

        </div>

        {/* RIGHT 7 COLUMNS: Button Row + Dynamic Panels (Approach/Code/Hints) */}
        <div className="question-col-7" style={{
          gridColumn: 'span 7',
          display: 'flex',
          flexDirection: 'column',
          gap: '1rem'
        }}>
          
          {/* SECTION D: Five Buttons Row (Order 4 on mobile: scrolls sideways with snapping, sticky under top bar) */}
          <div className="question-pill-nav-sticky">
            <div className="question-pill-nav-scroll">
              {/* Hint 1 */}
              <button
                type="button"
                onClick={() => unlockHint(1)}
                className={`pill-nav-btn ${activePanel === 'hint-1' ? 'btn-primary' : 'btn-secondary'}`}
              >
                <Lightbulb size={14} />
                <span>Hint 1</span>
              </button>

              {/* Hint 2 */}
              <button
                type="button"
                onClick={() => unlockHint(2)}
                disabled={unlockedHintLevel < 1}
                className={`pill-nav-btn ${activePanel === 'hint-2' ? 'btn-primary' : 'btn-secondary'}`}
                style={{
                  opacity: unlockedHintLevel < 1 ? 0.45 : 1,
                  cursor: unlockedHintLevel < 1 ? 'not-allowed' : 'pointer'
                }}
                title={unlockedHintLevel < 1 ? 'Open Hint 1 first' : 'View Hint 2'}
              >
                {unlockedHintLevel < 1 ? <Lock size={13} /> : <Lightbulb size={14} />}
                <span>Hint 2</span>
              </button>

              {/* Hint 3 */}
              <button
                type="button"
                onClick={() => unlockHint(3)}
                disabled={unlockedHintLevel < 2}
                className={`pill-nav-btn ${activePanel === 'hint-3' ? 'btn-primary' : 'btn-secondary'}`}
                style={{
                  opacity: unlockedHintLevel < 2 ? 0.45 : 1,
                  cursor: unlockedHintLevel < 2 ? 'not-allowed' : 'pointer'
                }}
                title={unlockedHintLevel < 2 ? 'Open Hint 2 first' : 'View Hint 3'}
              >
                {unlockedHintLevel < 2 ? <Lock size={13} /> : <Lightbulb size={14} />}
                <span>Hint 3</span>
              </button>

              {/* Approach Button */}
              <button
                type="button"
                onClick={() => setActivePanel('approach')}
                className={`pill-nav-btn ${activePanel === 'approach' ? 'btn-primary' : 'btn-secondary'}`}
              >
                <BookOpen size={14} />
                <span>Approach</span>
              </button>

              {/* Code Button */}
              <button
                type="button"
                onClick={() => setActivePanel('code')}
                className={`pill-nav-btn ${activePanel === 'code' ? 'btn-primary' : 'btn-secondary'}`}
              >
                <Code2 size={14} />
                <span>Code</span>
              </button>
            </div>
          </div>

          {/* SECTION E & F: Open Panel at Full Width (Order 5 on mobile) */}
          <div className="glass-card question-panel-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '1.25rem', minHeight: '480px' }}>
            
            {/* INITIAL STATE: Nothing revealed yet */}
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

                <div style={{ display: 'flex', gap: '0.75rem', marginTop: '0.5rem', flexWrap: 'wrap', justifyContent: 'center' }}>
                  <button
                    type="button"
                    onClick={() => unlockHint(1)}
                    className="btn-primary"
                    style={{ fontSize: '0.85rem', padding: '0.5rem 1.1rem', minHeight: '44px' }}
                  >
                    <Lightbulb size={14} />
                    <span>Reveal Hint 1</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => setActivePanel('code')}
                    className="btn-secondary"
                    style={{ fontSize: '0.85rem', padding: '0.5rem 1.1rem', minHeight: '44px' }}
                  >
                    <Code2 size={14} />
                    <span>Go Straight to Code</span>
                  </button>
                </div>
              </div>
            )}

            {/* HINTS VIEW */}
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
                  <p style={{ fontSize: '0.925rem', color: 'var(--text-color)', lineHeight: 1.55 }}>
                    {hints[0]}
                  </p>
                </div>

                {/* Hint 2 Card */}
                {unlockedHintLevel >= 2 && (
                  <div style={{
                    background: activePanel === 'hint-2' ? 'var(--accent-soft)' : 'var(--glass-surface)',
                    border: '1px solid',
                    borderColor: activePanel === 'hint-2' ? 'var(--accent)' : 'var(--glass-border)',
                    borderRadius: 'var(--radius-inner)',
                    padding: '1.1rem'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', color: 'var(--text-color)', fontWeight: 700, fontSize: '0.875rem', marginBottom: '0.45rem' }}>
                      <Lightbulb size={16} color="var(--accent)" />
                      <span>Hint 2: Pattern Identification</span>
                    </div>
                    <p style={{ fontSize: '0.925rem', color: 'var(--text-color)', lineHeight: 1.55 }}>
                      {hints[1]}
                    </p>
                  </div>
                )}

                {/* Hint 3 Card */}
                {unlockedHintLevel >= 3 && (
                  <div style={{
                    background: activePanel === 'hint-3' ? 'var(--accent-soft)' : 'var(--glass-surface)',
                    border: '1px solid',
                    borderColor: activePanel === 'hint-3' ? 'var(--accent)' : 'var(--glass-border)',
                    borderRadius: 'var(--radius-inner)',
                    padding: '1.1rem'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', color: 'var(--text-color)', fontWeight: 700, fontSize: '0.875rem', marginBottom: '0.45rem' }}>
                      <Lightbulb size={16} color="var(--accent)" />
                      <span>Hint 3: Invariant & State Formulation</span>
                    </div>
                    <p style={{ fontSize: '0.925rem', color: 'var(--text-color)', lineHeight: 1.55 }}>
                      {hints[2]}
                    </p>
                  </div>
                )}

                {/* Next Action in sequence */}
                <div style={{ marginTop: 'auto', display: 'flex', justifyContent: 'flex-end', paddingTop: '1rem', gap: '0.5rem' }}>
                  {activePanel === 'hint-1' && (
                    <button
                      type="button"
                      onClick={() => unlockHint(2)}
                      className="btn-primary"
                      style={{ fontSize: '0.85rem', padding: '0.5rem 1rem', minHeight: '44px' }}
                    >
                      <span>Unlock Hint 2</span>
                      <ArrowRight size={14} />
                    </button>
                  )}
                  {activePanel === 'hint-2' && (
                    <button
                      type="button"
                      onClick={() => unlockHint(3)}
                      className="btn-primary"
                      style={{ fontSize: '0.85rem', padding: '0.5rem 1rem', minHeight: '44px' }}
                    >
                      <span>Unlock Hint 3</span>
                      <ArrowRight size={14} />
                    </button>
                  )}
                  {activePanel === 'hint-3' && (
                    <button
                      type="button"
                      onClick={() => setActivePanel('approach')}
                      className="btn-primary"
                      style={{ fontSize: '0.85rem', padding: '0.5rem 1rem', minHeight: '44px' }}
                    >
                      <span>View Approach</span>
                      <ArrowRight size={14} />
                    </button>
                  )}
                </div>
              </div>
            )}

            {/* APPROACH VIEW (Brute force first, then Optimal - Part 1 & Part 2 #6e) */}
            {activePanel === 'approach' && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', flex: 1 }}>
                
                {/* Two-part control: Brute force | Optimal, each half 50% wide, Brute force first */}
                <div className="approach-subtabs-control" style={{
                  display: 'grid',
                  gridTemplateColumns: '1fr 1fr',
                  gap: '4px',
                  background: 'var(--progress-track)',
                  padding: '3px',
                  borderRadius: 'var(--radius-pill)',
                  width: '100%'
                }}>
                  <button
                    type="button"
                    onClick={() => setApproachSubTab('brute')}
                    className={`approach-subtab-btn ${approachSubTab === 'brute' ? 'active' : ''}`}
                    style={{
                      padding: '8px',
                      minHeight: '44px',
                      borderRadius: 'var(--radius-pill)',
                      border: 'none',
                      background: approachSubTab === 'brute' ? 'var(--accent)' : 'transparent',
                      color: approachSubTab === 'brute' ? 'var(--accent-text)' : 'var(--text-color)',
                      fontWeight: 700,
                      fontSize: '0.85rem',
                      cursor: 'pointer',
                      transition: 'all 150ms ease'
                    }}
                  >
                    Brute force
                  </button>
                  <button
                    type="button"
                    onClick={() => setApproachSubTab('optimal')}
                    className={`approach-subtab-btn ${approachSubTab === 'optimal' ? 'active' : ''}`}
                    style={{
                      padding: '8px',
                      minHeight: '44px',
                      borderRadius: 'var(--radius-pill)',
                      border: 'none',
                      background: approachSubTab === 'optimal' ? 'var(--accent)' : 'transparent',
                      color: approachSubTab === 'optimal' ? 'var(--accent-text)' : 'var(--text-color)',
                      fontWeight: 700,
                      fontSize: '0.85rem',
                      cursor: 'pointer',
                      transition: 'all 150ms ease'
                    }}
                  >
                    Optimal
                  </button>
                </div>

                {/* Complexity Chips (Wrap onto two lines if needed per Part 2 #6e) */}
                <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
                  <div style={{
                    padding: '8px 16px',
                    borderRadius: 'var(--radius-pill)',
                    background: 'var(--glass-surface)',
                    border: '1px solid var(--glass-border)',
                    fontSize: '0.85rem',
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
                    padding: '8px 16px',
                    borderRadius: 'var(--radius-pill)',
                    background: 'var(--glass-surface)',
                    border: '1px solid var(--glass-border)',
                    fontSize: '0.85rem',
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
                    fontSize: '0.875rem',
                    color: 'var(--text-color)',
                    lineHeight: 1.5
                  }}>
                    <strong style={{ color: '#D97706' }}>Why this is too slow: </strong>
                    <span>{approachData.whySlow}</span>
                  </div>
                )}

                {/* Core Idea */}
                <div>
                  <h4 style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: '0.45rem' }}>
                    Core Idea
                  </h4>
                  <p style={{ fontSize: '0.95rem', color: 'var(--text-color)', lineHeight: 1.6 }}>
                    {approachData?.idea}
                  </p>
                </div>

                {/* Algorithmic Steps */}
                {approachData?.steps && approachData.steps.length > 0 && (
                  <div>
                    <h4 style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: '0.5rem' }}>
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
                    style={{ fontSize: '0.85rem', padding: '0.5rem 1.1rem', minHeight: '44px' }}
                  >
                    <span>View Solution Code</span>
                    <ArrowRight size={14} />
                  </button>
                </div>
              </div>
            )}

            {/* CODE VIEW (Brute force first, then Optimal - Part 1 & Part 2 #6e, #6f) */}
            {activePanel === 'code' && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem', flex: 1, minWidth: 0, maxWidth: '100%' }}>
                
                {/* Control Row 1: Two-Part Control: Brute force | Optimal (50% each, Brute force first) */}
                <div className="code-subtabs-control" style={{
                  display: 'grid',
                  gridTemplateColumns: '1fr 1fr',
                  gap: '4px',
                  background: 'var(--progress-track)',
                  padding: '3px',
                  borderRadius: 'var(--radius-pill)',
                  width: '100%'
                }}>
                  <button
                    type="button"
                    onClick={() => setCodeSubTab('brute')}
                    className={`code-subtab-btn ${codeSubTab === 'brute' ? 'active' : ''}`}
                    style={{
                      padding: '8px',
                      minHeight: '44px',
                      borderRadius: 'var(--radius-pill)',
                      border: 'none',
                      background: codeSubTab === 'brute' ? 'var(--accent)' : 'transparent',
                      color: codeSubTab === 'brute' ? 'var(--accent-text)' : 'var(--text-color)',
                      fontWeight: 700,
                      fontSize: '0.85rem',
                      cursor: 'pointer',
                      transition: 'all 150ms ease'
                    }}
                  >
                    Brute force
                  </button>
                  <button
                    type="button"
                    onClick={() => setCodeSubTab('optimal')}
                    className={`code-subtab-btn ${codeSubTab === 'optimal' ? 'active' : ''}`}
                    style={{
                      padding: '8px',
                      minHeight: '44px',
                      borderRadius: 'var(--radius-pill)',
                      border: 'none',
                      background: codeSubTab === 'optimal' ? 'var(--accent)' : 'transparent',
                      color: codeSubTab === 'optimal' ? 'var(--accent-text)' : 'var(--text-color)',
                      fontWeight: 700,
                      fontSize: '0.85rem',
                      cursor: 'pointer',
                      transition: 'all 150ms ease'
                    }}
                  >
                    Optimal
                  </button>
                </div>

                {/* Control Row 2: Java | Python on left, Copy button on right (Part 2 #6e) */}
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '0.5rem', width: '100%' }}>
                  {/* Java | Python switch */}
                  <div style={{ 
                    display: 'flex', 
                    background: 'var(--glass-surface)', 
                    padding: '3px', 
                    borderRadius: 'var(--radius-pill)',
                    border: '1px solid var(--glass-border)'
                  }}>
                    <button
                      type="button"
                      onClick={() => updateLanguage('java')}
                      style={{
                        padding: '6px 14px',
                        minHeight: '38px',
                        fontSize: '0.8rem',
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
                        padding: '6px 14px',
                        minHeight: '38px',
                        fontSize: '0.8rem',
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

                  {/* Copy button */}
                  <button
                    type="button"
                    onClick={handleCopyCode}
                    className="btn-secondary"
                    style={{ 
                      padding: '6px 14px', 
                      fontSize: '0.8rem', 
                      gap: '0.35rem', 
                      borderRadius: 'var(--radius-pill)',
                      minHeight: '38px' 
                    }}
                    title="Copy code to clipboard"
                  >
                    {copied ? <Check size={14} color="#10B981" /> : <Copy size={14} />}
                    <span>{copied ? 'Copied' : 'Copy'}</span>
                  </button>
                </div>

                {/* Complexity Chips above code (wrap onto two lines if needed) */}
                <div style={{ display: 'flex', gap: '0.65rem', flexWrap: 'wrap' }}>
                  <span style={{
                    padding: '4px 10px',
                    borderRadius: 'var(--radius-pill)',
                    background: 'var(--glass-surface)',
                    border: '1px solid var(--glass-border)',
                    fontSize: '0.78rem',
                    fontFamily: 'var(--font-mono)'
                  }}>
                    Time: {codeData?.time || 'O(n)'}
                  </span>
                  <span style={{
                    padding: '4px 10px',
                    borderRadius: 'var(--radius-pill)',
                    background: 'var(--glass-surface)',
                    border: '1px solid var(--glass-border)',
                    fontSize: '0.78rem',
                    fontFamily: 'var(--font-mono)'
                  }}>
                    Space: {codeData?.space || 'O(1)'}
                  </span>
                </div>

                {/* Code Box: Font 13px, padding 16px, long lines scroll sideways inside box only, never wrap, never push page wider (Part 2 #6f) */}
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
                    <code className={`language-${language}`}>
                      {currentCode}
                    </code>
                  </pre>
                </div>

              </div>
            )}

          </div>

        </div>

      </div>

    </div>
  );
}

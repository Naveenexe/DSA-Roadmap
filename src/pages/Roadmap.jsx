import React, { useState, useMemo, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { 
  Search, 
  ExternalLink, 
  CheckCircle2, 
  Clock, 
  Circle, 
  AlertTriangle,
  Link2,
  X,
  Filter,
  Check,
  ChevronDown
} from 'lucide-react';

export default function Roadmap() {
  const { questions, chapters, progressMap, getNextUp } = useApp();
  const location = useLocation();

  const nextUp = getNextUp();

  // Active chapter state (defaults to ch-01 or from hash)
  const [activeChapterId, setActiveChapterId] = useState('ch-01');

  // Filters
  const [search, setSearch] = useState('');
  const [selectedDifficulty, setSelectedDifficulty] = useState('all'); // all, easy, medium, hard
  const [selectedStatus, setSelectedStatus] = useState('all'); // all, todo, in_progress, done, revisit
  const [filterMistakes, setFilterMistakes] = useState(false);

  // Mobile bottom sheet / sidebar toggle
  const [mobileSheetOpen, setMobileSheetOpen] = useState(false);

  // Sync hash to active chapter
  useEffect(() => {
    if (location.hash) {
      const targetId = location.hash.replace('#', '');
      const exists = chapters.find(c => c.id === targetId);
      if (exists) {
        setActiveChapterId(targetId);
      }
    }
  }, [location.hash, chapters]);

  // Active chapter object
  const activeChapter = useMemo(() => {
    return chapters.find(c => c.id === activeChapterId) || chapters[0] || {
      id: 'ch-01',
      order: 1,
      name: 'Arrays & Hashing',
      seqFrom: 1,
      seqTo: 21,
      whyNext: 'Foundation of counting, lookup and in-place transformations.'
    };
  }, [chapters, activeChapterId]);

  // Questions for active chapter
  const chapterQuestions = useMemo(() => {
    return questions.filter(q => q.chapter === activeChapter.id);
  }, [questions, activeChapter.id]);

  // Calculations for active chapter (Section 3 #12, #18)
  const chapterTotal = chapterQuestions.length || (activeChapter.seqTo - activeChapter.seqFrom + 1);
  const chapterDoneCount = useMemo(() => {
    return chapterQuestions.filter(q => progressMap[q.seq]?.status === 'done').length;
  }, [chapterQuestions, progressMap]);

  // Filtered questions
  const filteredQuestions = useMemo(() => {
    const qSearch = search.trim().toLowerCase();
    return chapterQuestions.filter(q => {
      // Search
      if (qSearch) {
        const matchesTitle = q.title.toLowerCase().includes(qSearch);
        const matchesLc = String(q.lc).includes(qSearch);
        const matchesSeq = String(q.seq) === qSearch;
        if (!matchesTitle && !matchesLc && !matchesSeq) return false;
      }

      // Difficulty
      if (selectedDifficulty !== 'all' && q.difficulty.toLowerCase() !== selectedDifficulty.toLowerCase()) {
        return false;
      }

      // Status
      const userStatus = progressMap[q.seq]?.status || 'todo';
      if (selectedStatus !== 'all' && userStatus !== selectedStatus) {
        return false;
      }

      // Mistake
      if (filterMistakes && !progressMap[q.seq]?.mistake) {
        return false;
      }

      return true;
    });
  }, [chapterQuestions, search, selectedDifficulty, selectedStatus, filterMistakes, progressMap]);

  // Filter chips counts (Section 5.4: Counts appear on each chip)
  const filterCounts = useMemo(() => {
    const counts = {
      all: chapterQuestions.length,
      easy: chapterQuestions.filter(q => q.difficulty === 'Easy').length,
      medium: chapterQuestions.filter(q => q.difficulty === 'Medium').length,
      hard: chapterQuestions.filter(q => q.difficulty === 'Hard').length,
      revisit: chapterQuestions.filter(q => progressMap[q.seq]?.status === 'revisit').length,
      mistakes: chapterQuestions.filter(q => progressMap[q.seq]?.mistake).length
    };
    return counts;
  }, [chapterQuestions, progressMap]);

  const clearFilters = () => {
    setSearch('');
    setSelectedDifficulty('all');
    setSelectedStatus('all');
    setFilterMistakes(false);
  };

  const hasActiveFilters = search || selectedDifficulty !== 'all' || selectedStatus !== 'all' || filterMistakes;

  // Status icon renderer per Section 4.6 & Section 3 #15
  const renderStatusIcon = (status, seq) => {
    const p = progressMap[seq];
    if (status === 'done') {
      return (
        <span 
          style={{ 
            width: 24, 
            height: 24, 
            borderRadius: '50%', 
            background: 'var(--accent-soft)', 
            color: 'var(--accent-soft-text)', 
            display: 'inline-flex', 
            alignItems: 'center', 
            justifyContent: 'center' 
          }} 
          title="Done (Solved)"
          aria-label="Solved"
        >
          <Check size={14} strokeWidth={3} />
        </span>
      );
    }
    if (status === 'in_progress') {
      return (
        <span 
          style={{ 
            width: 24, 
            height: 24, 
            borderRadius: '50%', 
            border: '2px solid var(--accent)', 
            display: 'inline-flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            position: 'relative',
            overflow: 'hidden'
          }} 
          title="In progress"
          aria-label="In progress"
        >
          {/* Half filled circle */}
          <div style={{ position: 'absolute', left: 0, top: 0, width: '50%', height: '100%', background: 'var(--accent)' }} />
        </span>
      );
    }
    if (status === 'revisit') {
      return (
        <span 
          style={{ 
            display: 'inline-flex', 
            alignItems: 'center', 
            color: 'var(--revisit-color)' 
          }} 
          title="Needs Revisit"
          aria-label="Revisit"
        >
          <Clock size={20} />
        </span>
      );
    }
    // Todo: Hollow circle
    return (
      <span 
        style={{ 
          width: 20, 
          height: 20, 
          borderRadius: '50%', 
          border: '2px solid var(--progress-track)', 
          display: 'inline-flex', 
          alignItems: 'center', 
          justifyContent: 'center' 
        }} 
        title="Todo"
        aria-label="Todo"
      />
    );
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '280px minmax(0, 1fr)', gap: '24px', alignItems: 'start' }} className="roadmap-layout-grid">
      
      {/* 1. LEFT SIDEBAR: Sticky 280px on desktop (Section 5.4 & Section 3 #10) */}
      <aside className="glass-card roadmap-sidebar" style={{
        position: 'sticky',
        top: '96px',
        maxHeight: 'calc(100vh - 120px)',
        overflowY: 'auto',
        padding: '16px 12px',
        display: 'flex',
        flexDirection: 'column',
        gap: '4px'
      }}>
        <div style={{ padding: '4px 10px 10px 10px', borderBottom: '1px solid var(--glass-border)', marginBottom: '6px' }}>
          <span style={{
            fontSize: '0.75rem',
            fontFamily: 'var(--font-mono)',
            fontWeight: 700,
            textTransform: 'uppercase',
            letterSpacing: '0.08em',
            color: 'var(--text-muted)'
          }}>
            18 Chapters
          </span>
        </div>

        {chapters.map(ch => {
          const chQs = questions.filter(q => q.chapter === ch.id);
          const totalInCh = chQs.length || (ch.seqTo - ch.seqFrom + 1);
          const doneInCh = chQs.filter(q => progressMap[q.seq]?.status === 'done').length;
          const ratio = totalInCh ? (doneInCh / totalInCh) : 0;
          const isActive = ch.id === activeChapter.id;

          return (
            <button
              key={ch.id}
              onClick={() => {
                setActiveChapterId(ch.id);
                setMobileSheetOpen(false);
              }}
              style={{
                width: '100%',
                display: 'flex',
                flexDirection: 'column',
                gap: '5px',
                padding: '10px 12px',
                borderRadius: 'var(--radius-inner)',
                background: isActive ? 'var(--accent-soft)' : 'transparent',
                color: isActive ? 'var(--accent-soft-text)' : 'var(--text-color)',
                textAlign: 'left',
                transition: 'all 150ms ease'
              }}
              onMouseEnter={(e) => {
                if (!isActive) e.currentTarget.style.background = 'var(--glass-surface)';
              }}
              onMouseLeave={(e) => {
                if (!isActive) e.currentTarget.style.background = 'transparent';
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.85rem' }}>
                <span style={{ fontWeight: isActive ? 700 : 600, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {ch.order}. {ch.name}
                </span>
                <span style={{
                  fontFamily: 'var(--font-mono)',
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  color: isActive ? 'var(--accent-soft-text)' : 'var(--text-muted)'
                }}>
                  {doneInCh}/{totalInCh}
                </span>
              </div>

              {/* Progress bar fill (Section 3 #10: bar fill matches counts) */}
              <div className="progress-bar-container" style={{ height: '5px', background: isActive ? 'rgba(0,0,0,0.1)' : 'var(--progress-track)' }}>
                <div 
                  className="progress-bar-fill" 
                  style={{ 
                    width: `${Math.round(ratio * 100)}%`,
                    background: isActive ? 'var(--accent)' : 'var(--progress-fill)'
                  }} 
                />
              </div>
            </button>
          );
        })}
      </aside>

      {/* 2. MAIN CONTENT AREA */}
      <main style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        
        {/* Header Glass Card (Section 5.4 & Section 3 #18) */}
        <div className="glass-card" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem', marginBottom: '16px' }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '4px', flexWrap: 'wrap' }}>
                <h1 style={{ fontSize: 'clamp(1.4rem, 3vw, 1.85rem)', fontWeight: 800, color: 'var(--text-color)', letterSpacing: '-0.02em' }}>
                  {activeChapter.order}. {activeChapter.name}
                </h1>
                {/* Badge "9 of 14" (Section 5.4) */}
                <span style={{
                  background: 'var(--accent-soft)',
                  color: 'var(--accent-soft-text)',
                  fontSize: '0.825rem',
                  fontWeight: 700,
                  padding: '3px 12px',
                  borderRadius: 'var(--radius-pill)',
                  fontFamily: 'var(--font-mono)'
                }}>
                  {chapterDoneCount} of {chapterTotal}
                </span>
              </div>

              {/* Mono Line: "14 QUESTIONS · 9 DONE" (Section 5.4, 4.4) */}
              <div style={{
                fontFamily: 'var(--font-mono)',
                fontSize: '0.75rem',
                fontWeight: 700,
                color: 'var(--text-muted)',
                letterSpacing: '0.08em',
                textTransform: 'uppercase'
              }}>
                {chapterTotal} QUESTIONS · {chapterDoneCount} DONE
              </div>

              <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginTop: '6px' }}>
                {activeChapter.whyNext}
              </p>
            </div>

            {/* Search Box (Section 5.4) */}
            <div style={{ position: 'relative', width: '100%', maxWidth: '280px' }}>
              <Search size={16} style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search question or LC#..."
                className="glass-input"
                style={{ paddingLeft: '40px', paddingRight: '32px', height: '42px', fontSize: '0.88rem' }}
              />
              {search && (
                <button
                  onClick={() => setSearch('')}
                  style={{ position: 'absolute', right: '10px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }}
                >
                  <X size={14} />
                </button>
              )}
            </div>
          </div>

          {/* Filter Chips with real counts (Section 5.4) */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            flexWrap: 'wrap',
            paddingTop: '12px',
            borderTop: '1px solid var(--glass-border)'
          }}>
            <button
              onClick={() => { setSelectedDifficulty('all'); setSelectedStatus('all'); setFilterMistakes(false); }}
              className="nav-pill"
              style={{
                background: (!hasActiveFilters || (selectedDifficulty === 'all' && selectedStatus === 'all' && !filterMistakes)) ? 'var(--accent)' : 'var(--glass-surface)',
                color: (!hasActiveFilters || (selectedDifficulty === 'all' && selectedStatus === 'all' && !filterMistakes)) ? 'var(--accent-text)' : 'var(--text-color)',
                fontSize: '0.8rem',
                padding: '5px 14px'
              }}
            >
              All ({filterCounts.all})
            </button>

            <button
              onClick={() => setSelectedDifficulty(selectedDifficulty === 'easy' ? 'all' : 'easy')}
              className="nav-pill"
              style={{
                background: selectedDifficulty === 'easy' ? 'var(--easy-pill-bg)' : 'var(--glass-surface)',
                color: selectedDifficulty === 'easy' ? 'var(--easy-pill-text)' : 'var(--text-color)',
                fontSize: '0.8rem',
                padding: '5px 14px'
              }}
            >
              Easy ({filterCounts.easy})
            </button>

            <button
              onClick={() => setSelectedDifficulty(selectedDifficulty === 'medium' ? 'all' : 'medium')}
              className="nav-pill"
              style={{
                background: selectedDifficulty === 'medium' ? 'var(--medium-pill-bg)' : 'var(--glass-surface)',
                color: selectedDifficulty === 'medium' ? 'var(--medium-pill-text)' : 'var(--text-color)',
                fontSize: '0.8rem',
                padding: '5px 14px'
              }}
            >
              Medium ({filterCounts.medium})
            </button>

            <button
              onClick={() => setSelectedDifficulty(selectedDifficulty === 'hard' ? 'all' : 'hard')}
              className="nav-pill"
              style={{
                background: selectedDifficulty === 'hard' ? 'var(--hard-pill-bg)' : 'var(--glass-surface)',
                color: selectedDifficulty === 'hard' ? 'var(--hard-pill-text)' : 'var(--text-color)',
                fontSize: '0.8rem',
                padding: '5px 14px'
              }}
            >
              Hard ({filterCounts.hard})
            </button>

            <button
              onClick={() => setSelectedStatus(selectedStatus === 'revisit' ? 'all' : 'revisit')}
              className="nav-pill"
              style={{
                background: selectedStatus === 'revisit' ? 'var(--revisit-bg)' : 'var(--glass-surface)',
                color: selectedStatus === 'revisit' ? 'var(--revisit-color)' : 'var(--text-color)',
                fontSize: '0.8rem',
                padding: '5px 14px'
              }}
            >
              Revisit ({filterCounts.revisit})
            </button>

            <button
              onClick={() => setFilterMistakes(!filterMistakes)}
              className="nav-pill"
              style={{
                background: filterMistakes ? 'rgba(239, 68, 68, 0.15)' : 'var(--glass-surface)',
                color: filterMistakes ? '#EF4444' : 'var(--text-color)',
                fontSize: '0.8rem',
                padding: '5px 14px'
              }}
            >
              Mistakes ({filterCounts.mistakes})
            </button>
          </div>

          {/* Status Legend (Section 5.4 & Section 3 #15) */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '16px',
            flexWrap: 'wrap',
            marginTop: '12px',
            fontSize: '0.78rem',
            color: 'var(--text-muted)'
          }}>
            <span style={{ fontWeight: 600 }}>Status:</span>
            <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
              <span style={{ width: 14, height: 14, borderRadius: '50%', border: '2px solid var(--progress-track)' }} />
              <span>Todo</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
              <span style={{ width: 14, height: 14, borderRadius: '50%', border: '2px solid var(--accent)', position: 'relative', overflow: 'hidden' }}>
                <span style={{ position: 'absolute', left: 0, top: 0, width: '50%', height: '100%', background: 'var(--accent)' }} />
              </span>
              <span>In progress</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
              <span style={{ width: 16, height: 16, borderRadius: '50%', background: 'var(--accent-soft)', color: 'var(--accent-soft-text)', display: 'inline-flex', alignItems: 'center', justifyContent: 'center' }}>
                <Check size={10} strokeWidth={3} />
              </span>
              <span>Done</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
              <Clock size={15} color="var(--revisit-color)" />
              <span>Revisit with due date</span>
            </div>
          </div>
        </div>

        {/* 3. QUESTION LIST (Section 4.6 & Section 3 #13, #14) */}
        <div>
          {filteredQuestions.length === 0 ? (
            <div className="glass-card empty-state-box">
              <Filter size={36} color="var(--text-muted)" />
              <div>
                <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-color)' }}>
                  Nothing matches these filters
                </h3>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                  Try relaxing your search terms or active difficulty chips.
                </p>
              </div>
              <button onClick={clearFilters} className="btn-secondary">
                Clear filters
              </button>
            </div>
          ) : (
            filteredQuestions.map((q) => {
              const p = progressMap[q.seq];
              const status = p?.status || 'todo';
              const isNextUp = nextUp && nextUp.seq === q.seq;
              const buildsOnQuestion = q.buildsOn ? questions.find(item => item.seq === q.buildsOn) : null;
              const reviewItem = p?.status === 'revisit' 
                ? (p.dueDate || (useApp().reviews?.find(r => r.question_seq === q.seq)?.due_date)) 
                : null;

              return (
                <div
                  key={q.seq}
                  className={`question-row ${isNextUp ? 'highlight-next-up' : ''}`}
                >
                  {/* Column 1: Status Icon (fixed 32px width) */}
                  <div style={{ width: 32, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                    {renderStatusIcon(status, q.seq)}
                  </div>

                  {/* Column 2: Seq Number (fixed 44px width) */}
                  <div style={{ width: 44, flexShrink: 0, fontFamily: 'var(--font-mono)', fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600 }}>
                    #{q.seq}
                  </div>

                  {/* Column 3: Title (one line, ellipsis; full on hover/tap per Section 3 #14) */}
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <Link
                      to={`/question/${q.seq}`}
                      className="question-row-title"
                      title={`#${q.seq} ${q.title} (LC #${q.lc})`}
                      style={{ display: 'inline-block', maxWidth: '100%' }}
                    >
                      {q.title}
                    </Link>
                  </div>

                  {/* Revisit Due Date Chip if status is revisit (Section 4.6 & FR-36) */}
                  {status === 'revisit' && (
                    <div className="due-chip" style={{ flexShrink: 0 }}>
                      <Clock size={11} />
                      <span>{reviewItem ? `Due ${reviewItem}` : 'Revisit'}</span>
                    </div>
                  )}

                  {/* Column 4: Difficulty Pill (fixed width 84px per Section 4.6) */}
                  <span className={`diff-pill diff-pill-${q.difficulty.toLowerCase()}`}>
                    {q.difficulty}
                  </span>

                  {/* Column 5: Builds On (Fixed 180px width, ALWAYS shows Seq number per Section 3 #11) */}
                  <div style={{ width: 180, flexShrink: 0, fontSize: '0.8rem', color: 'var(--text-muted)' }} className="roadmap-col-builds-on">
                    {buildsOnQuestion ? (
                      <Link 
                        to={`/question/${buildsOnQuestion.seq}`}
                        style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', color: 'var(--accent)', fontWeight: 600 }}
                        title={`Builds on #${buildsOnQuestion.seq} ${buildsOnQuestion.title}`}
                      >
                        <Link2 size={12} />
                        <span>Builds on #{buildsOnQuestion.seq}</span>
                      </Link>
                    ) : (
                      <span style={{ fontStyle: 'italic', opacity: 0.7 }}>Foundation</span>
                    )}
                  </div>

                  {/* Column 6: LeetCode Icon Button (40px circle per Section 4.6) */}
                  <a
                    href={`https://leetcode.com/problems/${q.slug}/`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="icon-circle-btn"
                    style={{ flexShrink: 0 }}
                    title={`Open ${q.title} on LeetCode`}
                  >
                    <ExternalLink size={15} />
                  </a>
                </div>
              );
            })
          )}
        </div>
      </main>

    </div>
  );
}

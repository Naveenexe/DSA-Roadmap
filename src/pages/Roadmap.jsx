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
  ChevronDown,
  Info,
  Layers
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

  // Mobile bottom sheet toggle for 18 chapters
  const [chapterSheetOpen, setChapterSheetOpen] = useState(false);

  // Mobile info legend toggle
  const [showLegend, setShowLegend] = useState(false);

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

  // Calculations for active chapter
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

  // Filter chips counts
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

  // Status icon renderer
  const renderStatusIcon = (status) => {
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
    <div className="roadmap-layout-container" style={{ display: 'grid', gridTemplateColumns: '280px minmax(0, 1fr)', gap: '24px', alignItems: 'start' }}>
      
      {/* MOBILE-ONLY TOP CHAPTER BUTTON (Opens Bottom Sheet per Part 2 #5) */}
      <div className="mobile-chapter-selector-wrap">
        <button
          type="button"
          onClick={() => setChapterSheetOpen(true)}
          className="btn-secondary mobile-chapter-select-btn"
          aria-label="Select chapter"
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', overflow: 'hidden' }}>
            <Layers size={18} color="var(--accent)" style={{ flexShrink: 0 }} />
            <span style={{ fontWeight: 700, fontSize: '0.95rem', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
              {activeChapter.order}. {activeChapter.name}
            </span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexShrink: 0 }}>
            <span className="mobile-chapter-count-badge">
              {chapterDoneCount} of {chapterTotal}
            </span>
            <ChevronDown size={16} />
          </div>
        </button>
      </div>

      {/* 1. LEFT SIDEBAR: Sticky 280px on desktop (hidden on phones) */}
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
                setChapterSheetOpen(false);
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
                transition: 'all 150ms ease',
                minHeight: '44px'
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

              {/* Progress bar fill */}
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
      <main style={{ display: 'flex', flexDirection: 'column', gap: '16px', minWidth: 0 }}>
        
        {/* Header Glass Card */}
        <div className="glass-card roadmap-header-card" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem', marginBottom: '16px' }}>
            <div style={{ flex: 1, minWidth: '220px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '4px', flexWrap: 'wrap' }}>
                <h1 style={{ fontSize: 'clamp(1.3rem, 3vw, 1.85rem)', fontWeight: 800, color: 'var(--text-color)', letterSpacing: '-0.02em' }}>
                  {activeChapter.order}. {activeChapter.name}
                </h1>
                {/* Badge "9 of 14" */}
                <span className="desktop-chapter-badge" style={{
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

              {/* Mono Line: "14 QUESTIONS · 9 DONE" */}
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

            {/* Search Box (Full width on phones per Part 2 #5) */}
            <div className="roadmap-search-box-wrap" style={{ position: 'relative', width: '100%', maxWidth: '320px' }}>
              <Search size={16} style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search question or LC#..."
                className="glass-input roadmap-search-input"
                style={{ paddingLeft: '40px', paddingRight: '32px', height: '44px', minHeight: '44px', fontSize: '16px' }}
              />
              {search && (
                <button
                  type="button"
                  onClick={() => setSearch('')}
                  style={{ position: 'absolute', right: '10px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)', minHeight: '36px', minWidth: '36px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
                  aria-label="Clear search"
                >
                  <X size={15} />
                </button>
              )}
            </div>
          </div>

          {/* Filter Chips in one row that scrolls sideways with snapping on phones (Part 2 #5) */}
          <div className="roadmap-filter-chips-row">
            <button
              type="button"
              onClick={() => { setSelectedDifficulty('all'); setSelectedStatus('all'); setFilterMistakes(false); }}
              className="nav-pill filter-chip"
              style={{
                background: (!hasActiveFilters || (selectedDifficulty === 'all' && selectedStatus === 'all' && !filterMistakes)) ? 'var(--accent)' : 'var(--glass-surface)',
                color: (!hasActiveFilters || (selectedDifficulty === 'all' && selectedStatus === 'all' && !filterMistakes)) ? 'var(--accent-text)' : 'var(--text-color)',
                fontSize: '0.825rem',
                padding: '8px 14px',
                minHeight: '44px'
              }}
            >
              All ({filterCounts.all})
            </button>

            <button
              type="button"
              onClick={() => setSelectedDifficulty(selectedDifficulty === 'easy' ? 'all' : 'easy')}
              className="nav-pill filter-chip"
              style={{
                background: selectedDifficulty === 'easy' ? 'var(--easy-pill-bg)' : 'var(--glass-surface)',
                color: selectedDifficulty === 'easy' ? 'var(--easy-pill-text)' : 'var(--text-color)',
                fontSize: '0.825rem',
                padding: '8px 14px',
                minHeight: '44px'
              }}
            >
              Easy ({filterCounts.easy})
            </button>

            <button
              type="button"
              onClick={() => setSelectedDifficulty(selectedDifficulty === 'medium' ? 'all' : 'medium')}
              className="nav-pill filter-chip"
              style={{
                background: selectedDifficulty === 'medium' ? 'var(--medium-pill-bg)' : 'var(--glass-surface)',
                color: selectedDifficulty === 'medium' ? 'var(--medium-pill-text)' : 'var(--text-color)',
                fontSize: '0.825rem',
                padding: '8px 14px',
                minHeight: '44px'
              }}
            >
              Medium ({filterCounts.medium})
            </button>

            <button
              type="button"
              onClick={() => setSelectedDifficulty(selectedDifficulty === 'hard' ? 'all' : 'hard')}
              className="nav-pill filter-chip"
              style={{
                background: selectedDifficulty === 'hard' ? 'var(--hard-pill-bg)' : 'var(--glass-surface)',
                color: selectedDifficulty === 'hard' ? 'var(--hard-pill-text)' : 'var(--text-color)',
                fontSize: '0.825rem',
                padding: '8px 14px',
                minHeight: '44px'
              }}
            >
              Hard ({filterCounts.hard})
            </button>

            <button
              type="button"
              onClick={() => setSelectedStatus(selectedStatus === 'revisit' ? 'all' : 'revisit')}
              className="nav-pill filter-chip"
              style={{
                background: selectedStatus === 'revisit' ? 'var(--revisit-bg)' : 'var(--glass-surface)',
                color: selectedStatus === 'revisit' ? 'var(--revisit-color)' : 'var(--text-color)',
                fontSize: '0.825rem',
                padding: '8px 14px',
                minHeight: '44px'
              }}
            >
              Revisit ({filterCounts.revisit})
            </button>

            <button
              type="button"
              onClick={() => setFilterMistakes(!filterMistakes)}
              className="nav-pill filter-chip"
              style={{
                background: filterMistakes ? 'rgba(239, 68, 68, 0.15)' : 'var(--glass-surface)',
                color: filterMistakes ? '#EF4444' : 'var(--text-color)',
                fontSize: '0.825rem',
                padding: '8px 14px',
                minHeight: '44px'
              }}
            >
              Mistakes ({filterCounts.mistakes})
            </button>

            {/* Mobile Info Button: Legend collapses behind small info icon (Part 2 #5) */}
            <button
              type="button"
              onClick={() => setShowLegend(!showLegend)}
              className="icon-circle-btn mobile-legend-toggle-btn"
              title="Show Status Legend"
              aria-label="Toggle status legend"
              style={{ minWidth: '44px', minHeight: '44px' }}
            >
              <Info size={16} />
            </button>
          </div>

          {/* Status Legend (Collapses behind small info icon on mobile, visible on desktop) */}
          <div className={`roadmap-status-legend ${showLegend ? 'legend-visible-mobile' : ''}`}>
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

        {/* 3. QUESTION LIST (Cards on mobile at least 72px high, rows on desktop) */}
        <div className="roadmap-question-list">
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
              <button onClick={clearFilters} className="btn-secondary" style={{ minHeight: '44px' }}>
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
                  className={`question-item-card ${isNextUp ? 'highlight-next-up' : ''}`}
                >
                  {/* DESKTOP ROW VIEW (>= 768px) */}
                  <div className="question-row-desktop">
                    <div style={{ width: 32, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                      {renderStatusIcon(status)}
                    </div>

                    <div style={{ width: 44, flexShrink: 0, fontFamily: 'var(--font-mono)', fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600 }}>
                      #{q.seq}
                    </div>

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

                    {status === 'revisit' && (
                      <div className="due-chip" style={{ flexShrink: 0 }}>
                        <Clock size={11} />
                        <span>{reviewItem ? `Due ${reviewItem}` : 'Revisit'}</span>
                      </div>
                    )}

                    <span className={`diff-pill diff-pill-${q.difficulty.toLowerCase()}`}>
                      {q.difficulty}
                    </span>

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

                    <a
                      href={`https://leetcode.com/problems/${q.slug}/`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="icon-circle-btn"
                      style={{ flexShrink: 0, minWidth: '40px', minHeight: '40px' }}
                      title={`Open ${q.title} on LeetCode`}
                    >
                      <ExternalLink size={15} />
                    </a>
                  </div>

                  {/* MOBILE CARD VIEW (< 768px, at least 72px high per Part 2 #5) */}
                  <div className="question-card-mobile">
                    {/* First line: status icon, number, title (wraps at most two lines) */}
                    <div className="question-card-mobile-line1">
                      <div style={{ flexShrink: 0, display: 'inline-flex', alignItems: 'center' }}>
                        {renderStatusIcon(status)}
                      </div>
                      <span className="question-mobile-seq">#{q.seq}</span>
                      <Link to={`/question/${q.seq}`} className="question-mobile-title">
                        {q.title}
                      </Link>
                    </div>

                    {/* Second line: difficulty pill, "builds on #n", 44px LeetCode arrow button at right end */}
                    <div className="question-card-mobile-line2">
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap', flex: 1, minWidth: 0 }}>
                        <span className={`diff-pill diff-pill-${q.difficulty.toLowerCase()}`}>
                          {q.difficulty}
                        </span>

                        {buildsOnQuestion ? (
                          <Link 
                            to={`/question/${buildsOnQuestion.seq}`}
                            className="question-mobile-buildson"
                          >
                            <Link2 size={12} />
                            <span>builds on #{buildsOnQuestion.seq}</span>
                          </Link>
                        ) : (
                          <span className="question-mobile-foundation">Foundation</span>
                        )}

                        {status === 'revisit' && (
                          <span className="due-chip">
                            <Clock size={11} />
                            <span>{reviewItem ? `Due ${reviewItem}` : 'Revisit'}</span>
                          </span>
                        )}
                      </div>

                      <a
                        href={`https://leetcode.com/problems/${q.slug}/`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="mobile-lc-arrow-btn"
                        title={`Open ${q.title} on LeetCode`}
                        aria-label={`Open ${q.title} on LeetCode`}
                      >
                        <ExternalLink size={16} />
                      </a>
                    </div>
                  </div>

                </div>
              );
            })
          )}
        </div>
      </main>

      {/* MOBILE BOTTOM SHEET FOR 18 CHAPTERS (Part 2 #5) */}
      {chapterSheetOpen && (
        <div className="bottom-sheet-overlay" onClick={() => setChapterSheetOpen(false)}>
          <div className="bottom-sheet-content glass-card" onClick={(e) => e.stopPropagation()}>
            <div className="bottom-sheet-handle" />
            <div className="bottom-sheet-header">
              <h3 style={{ fontSize: '1.1rem', fontWeight: 800, color: 'var(--text-color)' }}>
                Select Chapter (18 Total)
              </h3>
              <button
                type="button"
                onClick={() => setChapterSheetOpen(false)}
                className="icon-circle-btn"
                style={{ width: 36, height: 36, minWidth: 36, minHeight: 36 }}
                aria-label="Close"
              >
                <X size={16} />
              </button>
            </div>

            <div className="bottom-sheet-scrollable-list">
              {chapters.map(ch => {
                const chQs = questions.filter(q => q.chapter === ch.id);
                const totalInCh = chQs.length || (ch.seqTo - ch.seqFrom + 1);
                const doneInCh = chQs.filter(q => progressMap[q.seq]?.status === 'done').length;
                const ratio = totalInCh ? (doneInCh / totalInCh) : 0;
                const isActive = ch.id === activeChapter.id;

                return (
                  <button
                    key={ch.id}
                    type="button"
                    onClick={() => {
                      setActiveChapterId(ch.id);
                      setChapterSheetOpen(false);
                    }}
                    className={`bottom-sheet-chapter-item ${isActive ? 'active' : ''}`}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '4px' }}>
                      <span style={{ fontWeight: isActive ? 700 : 600, fontSize: '0.925rem', color: isActive ? 'var(--accent)' : 'var(--text-color)' }}>
                        {ch.order}. {ch.name}
                      </span>
                      <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-muted)' }}>
                        {doneInCh}/{totalInCh}
                      </span>
                    </div>
                    <div className="progress-bar-container" style={{ height: '6px' }}>
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
            </div>
          </div>
        </div>
      )}

    </div>
  );
}

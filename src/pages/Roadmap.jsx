import React, { useState, useMemo, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { 
  ChevronDown, 
  ChevronRight, 
  ExternalLink, 
  Search, 
  CheckCircle2, 
  Clock, 
  Circle,
  AlertTriangle,
  Link2,
  X,
  BookOpen
} from 'lucide-react';

export default function Roadmap() {
  const { questions, chapters, progressMap } = useApp();
  const location = useLocation();

  // Filters
  const [search, setSearch] = useState('');
  const [selectedChapter, setSelectedChapter] = useState('all');
  const [selectedDifficulty, setSelectedDifficulty] = useState('all');
  const [selectedStatus, setSelectedStatus] = useState('all');
  const [filterMistakes, setFilterMistakes] = useState(false);

  // Collapsed chapters map when in "all" view
  const [collapsedChapters, setCollapsedChapters] = useState({});

  // Scroll to chapter anchor if in hash
  useEffect(() => {
    if (location.hash) {
      const id = location.hash.replace('#', '');
      setSelectedChapter(id);
      const el = document.getElementById(id);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth' });
      }
    }
  }, [location.hash]);

  const toggleChapterCollapse = (chId) => {
    setCollapsedChapters(prev => ({
      ...prev,
      [chId]: !prev[chId]
    }));
  };

  // Questions grouped by chapter
  const questionsByChapter = useMemo(() => {
    const map = {};
    chapters.forEach(ch => {
      map[ch.id] = [];
    });
    questions.forEach(q => {
      if (map[q.chapter]) {
        map[q.chapter].push(q);
      }
    });
    return map;
  }, [chapters, questions]);

  // Overall stats
  const totalSolved = useMemo(() => {
    return Object.values(progressMap).filter(p => p.status === 'done').length;
  }, [progressMap]);

  // Status icon renderer
  const renderStatusIcon = (status, isMistake) => {
    if (isMistake) {
      return (
        <span title="Flagged as mistake" style={{ display: 'inline-flex', alignItems: 'center' }}>
          <AlertTriangle size={15} color="var(--status-mistake)" />
        </span>
      );
    }
    if (status === 'done') {
      return (
        <span title="Solved" style={{ display: 'inline-flex', alignItems: 'center' }}>
          <CheckCircle2 size={16} color="var(--status-done)" />
        </span>
      );
    }
    if (status === 'in_progress') {
      return (
        <span title="In Progress" style={{ display: 'inline-flex', alignItems: 'center' }}>
          <Circle size={15} color="var(--status-inprogress)" fill="var(--status-inprogress)" fillOpacity={0.6} />
        </span>
      );
    }
    if (status === 'revisit') {
      return (
        <span title="Needs Revisit" style={{ display: 'inline-flex', alignItems: 'center' }}>
          <Clock size={15} color="var(--status-revisit)" />
        </span>
      );
    }
    return (
      <span title="Todo" style={{ display: 'inline-flex', alignItems: 'center', opacity: 0.35 }}>
        <Circle size={14} color="var(--text-muted)" />
      </span>
    );
  };

  // Filter questions function
  const filterQuestionList = (list) => {
    const qSearch = search.trim().toLowerCase();
    return list.filter(q => {
      if (qSearch) {
        const matchesTitle = q.title.toLowerCase().includes(qSearch);
        const matchesLc = String(q.lc).includes(qSearch);
        const matchesSeq = String(q.seq) === qSearch;
        if (!matchesTitle && !matchesLc && !matchesSeq) return false;
      }
      if (selectedDifficulty !== 'all' && q.difficulty.toLowerCase() !== selectedDifficulty.toLowerCase()) {
        return false;
      }
      const p = progressMap[q.seq];
      const userStatus = p?.status || 'todo';
      if (selectedStatus !== 'all' && userStatus !== selectedStatus) {
        return false;
      }
      if (filterMistakes && !p?.mistake) {
        return false;
      }
      return true;
    });
  };

  // Visible chapters
  const visibleChapters = useMemo(() => {
    if (selectedChapter === 'all') return chapters;
    return chapters.filter(c => c.id === selectedChapter);
  }, [chapters, selectedChapter]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', width: '100%', maxWidth: '1400px', margin: '0 auto' }}>
      {/* Header bar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem' }}>
        <div>
          <h1 style={{ fontSize: '1.4rem', fontWeight: 700, letterSpacing: '-0.02em', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span>Problem List</span>
            <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)' }}>
              ({totalSolved}/300 Solved)
            </span>
          </h1>
          <p style={{ fontSize: '0.825rem', color: 'var(--text-muted)' }}>
            Curated 300-question algorithmic journey partitioned across 18 sequential chapters.
          </p>
        </div>

        {/* Global Progress Bar */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', minWidth: '220px' }}>
          <div style={{ flex: 1, height: 6, background: 'var(--border)', borderRadius: 3, overflow: 'hidden' }}>
            <div 
              style={{ 
                width: `${Math.round((totalSolved / 300) * 100)}%`, 
                height: '100%', 
                background: 'var(--accent)',
                transition: 'width 0.3s ease'
              }} 
            />
          </div>
          <span style={{ fontSize: '0.8rem', fontFamily: 'var(--font-mono)', fontWeight: 600, color: 'var(--accent)' }}>
            {Math.round((totalSolved / 300) * 100)}%
          </span>
        </div>
      </div>

      {/* Filter Row */}
      <div className="panel" style={{ padding: '0.75rem 1rem', display: 'flex', flexWrap: 'wrap', gap: '0.75rem', alignItems: 'center', justifyContent: 'space-between' }}>
        {/* Search */}
        <div style={{ position: 'relative', flex: '1 1 240px', maxWidth: '360px' }}>
          <Search size={15} style={{ position: 'absolute', left: '0.65rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
          <input
            type="text"
            placeholder="Search questions by title, LC# or seq..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input"
            style={{ width: '100%', paddingLeft: '2rem', height: '34px' }}
          />
          {search && (
            <button 
              onClick={() => setSearch('')}
              style={{ position: 'absolute', right: '0.5rem', top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}
            >
              <X size={14} />
            </button>
          )}
        </div>

        {/* Difficulty Filters */}
        <div style={{ display: 'flex', gap: '0.35rem', alignItems: 'center' }}>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginRight: '0.2rem' }}>Difficulty:</span>
          {['all', 'easy', 'medium', 'hard'].map(d => (
            <button
              key={d}
              onClick={() => setSelectedDifficulty(d)}
              style={{
                padding: '0.25rem 0.6rem',
                fontSize: '0.78rem',
                fontWeight: 600,
                borderRadius: 'var(--radius-sm)',
                border: '1px solid',
                borderColor: selectedDifficulty === d ? (d === 'easy' ? 'var(--easy)' : d === 'medium' ? 'var(--medium)' : d === 'hard' ? 'var(--hard)' : 'var(--accent)') : 'var(--border)',
                background: selectedDifficulty === d ? (d === 'easy' ? 'var(--easy-bg)' : d === 'medium' ? 'var(--medium-bg)' : d === 'hard' ? 'var(--hard-bg)' : 'var(--accent-light)') : 'transparent',
                color: selectedDifficulty === d ? (d === 'easy' ? 'var(--easy)' : d === 'medium' ? 'var(--medium)' : d === 'hard' ? 'var(--hard)' : 'var(--accent)') : 'var(--text-muted)',
                cursor: 'pointer'
              }}
            >
              {d.charAt(0).toUpperCase() + d.slice(1)}
            </button>
          ))}
        </div>

        {/* Status Filters */}
        <div style={{ display: 'flex', gap: '0.35rem', alignItems: 'center' }}>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginRight: '0.2rem' }}>Status:</span>
          {[
            { id: 'all', label: 'All' },
            { id: 'todo', label: 'Todo' },
            { id: 'in_progress', label: 'In Progress' },
            { id: 'done', label: 'Solved' },
            { id: 'revisit', label: 'Revisit' }
          ].map(s => (
            <button
              key={s.id}
              onClick={() => setSelectedStatus(s.id)}
              style={{
                padding: '0.25rem 0.6rem',
                fontSize: '0.78rem',
                fontWeight: 600,
                borderRadius: 'var(--radius-sm)',
                border: '1px solid',
                borderColor: selectedStatus === s.id ? 'var(--accent)' : 'var(--border)',
                background: selectedStatus === s.id ? 'var(--accent-light)' : 'transparent',
                color: selectedStatus === s.id ? 'var(--accent)' : 'var(--text-muted)',
                cursor: 'pointer'
              }}
            >
              {s.label}
            </button>
          ))}

          {/* Mistakes flag */}
          <button
            onClick={() => setFilterMistakes(!filterMistakes)}
            style={{
              padding: '0.25rem 0.6rem',
              fontSize: '0.78rem',
              fontWeight: 600,
              borderRadius: 'var(--radius-sm)',
              border: '1px solid',
              borderColor: filterMistakes ? 'var(--status-mistake)' : 'var(--border)',
              background: filterMistakes ? 'var(--status-mistake-bg)' : 'transparent',
              color: filterMistakes ? 'var(--status-mistake)' : 'var(--text-muted)',
              cursor: 'pointer',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.3rem'
            }}
          >
            <AlertTriangle size={13} />
            <span>Mistakes</span>
          </button>
        </div>
      </div>

      {/* Main Roadmap Grid: Left Chapter Sidebar + Right Problem List Table */}
      <div style={{ display: 'grid', gridTemplateColumns: '260px 1fr', gap: '1rem', alignItems: 'start' }}>
        {/* Left Chapters Sidebar */}
        <div className="panel" style={{ padding: '0.5rem', maxHeight: 'calc(100vh - 180px)', overflowY: 'auto' }}>
          <div style={{ padding: '0.5rem 0.65rem', borderBottom: '1px solid var(--border)', marginBottom: '0.35rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
              Chapters
            </span>
            <button
              onClick={() => setSelectedChapter('all')}
              style={{
                background: 'none',
                border: 'none',
                fontSize: '0.75rem',
                color: selectedChapter === 'all' ? 'var(--accent)' : 'var(--text-muted)',
                cursor: 'pointer',
                fontWeight: 600
              }}
            >
              View All
            </button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.15rem' }}>
            {chapters.map(ch => {
              const chQuestions = questionsByChapter[ch.id] || [];
              const chSolved = chQuestions.filter(q => progressMap[q.seq]?.status === 'done').length;
              const isSelected = selectedChapter === ch.id;

              return (
                <button
                  key={ch.id}
                  onClick={() => setSelectedChapter(ch.id)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '0.45rem 0.65rem',
                    borderRadius: 'var(--radius-sm)',
                    border: '1px solid',
                    borderColor: isSelected ? 'var(--accent)' : 'transparent',
                    background: isSelected ? 'var(--accent-light)' : 'transparent',
                    color: isSelected ? 'var(--accent)' : 'var(--text-main)',
                    textAlign: 'left',
                    fontSize: '0.8rem',
                    cursor: 'pointer',
                    transition: 'background 0.15s ease'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', overflow: 'hidden' }}>
                    <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', color: 'var(--text-muted)', minWidth: '18px' }}>
                      {ch.order}.
                    </span>
                    <span style={{ fontWeight: isSelected ? 600 : 400, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      {ch.name}
                    </span>
                  </div>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.72rem', color: isSelected ? 'var(--accent)' : 'var(--text-muted)', marginLeft: '0.5rem' }}>
                    {chSolved}/{chQuestions.length}
                  </span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Right Problem Table Area */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          {visibleChapters.map(ch => {
            const rawList = questionsByChapter[ch.id] || [];
            const filteredList = filterQuestionList(rawList);
            const chSolved = rawList.filter(q => progressMap[q.seq]?.status === 'done').length;
            const isCollapsed = selectedChapter === 'all' && collapsedChapters[ch.id];

            if (selectedChapter === 'all' && filteredList.length === 0 && (search || selectedDifficulty !== 'all' || selectedStatus !== 'all' || filterMistakes)) {
              return null;
            }

            return (
              <div key={ch.id} id={ch.id} className="lc-table-container">
                {/* Chapter Group Header */}
                <div 
                  onClick={() => selectedChapter === 'all' && toggleChapterCollapse(ch.id)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '0.75rem 1rem',
                    background: 'var(--bg-panel)',
                    borderBottom: isCollapsed ? 'none' : '1px solid var(--border)',
                    cursor: selectedChapter === 'all' ? 'pointer' : 'default',
                    userSelect: 'none'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                    {selectedChapter === 'all' && (
                      <span style={{ color: 'var(--text-muted)' }}>
                        {isCollapsed ? <ChevronRight size={16} /> : <ChevronDown size={16} />}
                      </span>
                    )}
                    <div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <span style={{ fontWeight: 700, fontSize: '0.95rem' }}>
                          Chapter {ch.order}: {ch.name}
                        </span>
                        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                          (Seq #{ch.seqFrom} - #{ch.seqTo})
                        </span>
                      </div>
                      <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '0.15rem' }}>
                        {ch.whyNext}
                      </p>
                    </div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    <span style={{ fontSize: '0.78rem', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>
                      {chSolved}/{rawList.length} Solved
                    </span>
                    <div style={{ width: 60, height: 5, background: 'var(--border)', borderRadius: 2.5, overflow: 'hidden' }}>
                      <div 
                        style={{ 
                          width: `${Math.round((chSolved / (rawList.length || 1)) * 100)}%`, 
                          height: '100%', 
                          background: 'var(--accent)' 
                        }} 
                      />
                    </div>
                  </div>
                </div>

                {/* Table Body (Collapsible) */}
                {!isCollapsed && (
                  <table className="lc-table">
                    <thead>
                      <tr>
                        <th style={{ width: 44, textAlign: 'center' }}>Status</th>
                        <th style={{ width: 56 }}>#</th>
                        <th>Title</th>
                        <th style={{ width: 90 }}>Difficulty</th>
                        <th style={{ width: 140 }}>Builds On</th>
                        <th style={{ width: 60, textAlign: 'center' }}>LeetCode</th>
                      </tr>
                    </thead>
                    <tbody>
                      {filteredList.length === 0 ? (
                        <tr>
                          <td colSpan={6} style={{ textAlign: 'center', padding: '1.5rem', color: 'var(--text-muted)' }}>
                            No questions match the current filter criteria in this chapter.
                          </td>
                        </tr>
                      ) : (
                        filteredList.map((q, idx) => {
                          const p = progressMap[q.seq];
                          const status = p?.status || 'todo';
                          const isMistake = Boolean(p?.mistake);
                          const buildsOnQ = q.buildsOn ? questions.find(item => item.seq === q.buildsOn) : null;
                          const isEven = idx % 2 === 1;

                          return (
                            <tr key={q.seq} className={isEven ? 'row-even' : ''}>
                              {/* Status Column */}
                              <td style={{ textAlign: 'center' }}>
                                {renderStatusIcon(status, isMistake)}
                              </td>

                              {/* Seq # */}
                              <td style={{ fontFamily: 'var(--font-mono)', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                                {q.seq}
                              </td>

                              {/* Title link */}
                              <td>
                                <Link 
                                  to={`/question/${q.seq}`}
                                  style={{ fontWeight: 500, color: 'var(--text-main)', transition: 'color 0.15s ease' }}
                                  onMouseEnter={(e) => e.target.style.color = 'var(--accent)'}
                                  onMouseLeave={(e) => e.target.style.color = 'var(--text-main)'}
                                >
                                  {q.title}
                                </Link>
                              </td>

                              {/* Difficulty */}
                              <td>
                                <span className={`badge-${q.difficulty.toLowerCase()}`}>
                                  {q.difficulty}
                                </span>
                              </td>

                              {/* Builds On */}
                              <td style={{ fontSize: '0.78rem' }}>
                                {buildsOnQ ? (
                                  <Link 
                                    to={`/question/${buildsOnQ.seq}`} 
                                    style={{ color: 'var(--accent)', display: 'inline-flex', alignItems: 'center', gap: '0.25rem' }}
                                    title={`Builds on #${buildsOnQ.seq}: ${buildsOnQ.title}`}
                                  >
                                    <Link2 size={12} />
                                    <span>#{buildsOnQ.seq}</span>
                                    <span style={{ color: 'var(--text-muted)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', maxWidth: '85px' }}>
                                      {buildsOnQ.title}
                                    </span>
                                  </Link>
                                ) : (
                                  <span style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>
                                    Foundation
                                  </span>
                                )}
                              </td>

                              {/* External LeetCode Link */}
                              <td style={{ textAlign: 'center' }}>
                                <a
                                  href={`https://leetcode.com/problems/${q.slug}/`}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  title={`Open ${q.title} on LeetCode`}
                                  style={{ color: 'var(--text-muted)', display: 'inline-flex', alignItems: 'center', transition: 'color 0.15s ease' }}
                                  onMouseEnter={(e) => e.currentTarget.style.color = 'var(--accent)'}
                                  onMouseLeave={(e) => e.currentTarget.style.color = 'var(--text-muted)'}
                                >
                                  <ExternalLink size={14} />
                                </a>
                              </td>
                            </tr>
                          );
                        })
                      )}
                    </tbody>
                  </table>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

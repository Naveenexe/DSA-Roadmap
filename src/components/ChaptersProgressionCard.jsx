import React, { useState, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { useApp } from '../context/AppContext';

export default function ChaptersProgressionCard() {
  const { chapters, questions, progressMap, getNextUp } = useApp();
  const nextUp = getNextUp();

  // Part 1 / Part 2 switch state, default to the part holding Next up
  const [activePart, setActivePart] = useState(() => {
    if (nextUp?.chapter) {
      // Find chapter order
      const ch = chapters.find(c => c.id === nextUp.chapter);
      if (ch && ch.order > 18) return 'part2';
    }
    return 'part1';
  });

  const part1Chapters = useMemo(() => chapters.filter(c => c.order <= 18), [chapters]);
  const part2Chapters = useMemo(() => chapters.filter(c => c.order > 18), [chapters]);

  const displayedChapters = activePart === 'part1' ? part1Chapters : part2Chapters;

  return (
    <div className="glass-card home-chapters-card" style={{ padding: '24px', width: '100%', boxSizing: 'border-box' }}>
      {/* Header with Title and Part 1 / Part 2 switch */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px', marginBottom: '16px' }}>
        <div>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-color)', margin: 0 }}>
            Chapters Progression
          </h3>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', margin: '2px 0 0 0' }}>
            {chapters.length} chapters · {questions.length} questions
          </p>
        </div>

        {/* Two-part tab switch */}
        <div 
          style={{ 
            display: 'inline-flex', 
            background: 'var(--glass-surface)', 
            border: '1px solid var(--glass-border)', 
            borderRadius: 'var(--radius-pill)', 
            padding: '3px',
            gap: '3px'
          }}
        >
          <button
            type="button"
            onClick={() => setActivePart('part1')}
            style={{
              padding: '6px 14px',
              borderRadius: 'var(--radius-pill)',
              fontSize: '0.78rem',
              fontWeight: 700,
              border: 'none',
              cursor: 'pointer',
              transition: 'all 150ms ease',
              background: activePart === 'part1' ? 'var(--accent)' : 'transparent',
              color: activePart === 'part1' ? '#fff' : 'var(--text-muted)'
            }}
          >
            Part 1 (1–18)
          </button>

          <button
            type="button"
            onClick={() => setActivePart('part2')}
            style={{
              padding: '6px 14px',
              borderRadius: 'var(--radius-pill)',
              fontSize: '0.78rem',
              fontWeight: 700,
              border: 'none',
              cursor: 'pointer',
              transition: 'all 150ms ease',
              background: activePart === 'part2' ? 'var(--accent)' : 'transparent',
              color: activePart === 'part2' ? '#fff' : 'var(--text-muted)'
            }}
          >
            Part 2 (19–32)
          </button>
        </div>
      </div>

      {/* Chapter rows: 2 columns on desktop/tablet, 1 column on phone */}
      <div className="chapters-two-columns" style={{ display: 'grid', gridTemplateColumns: 'repeat(2, minmax(0, 1fr))', gap: '10px 16px' }}>
        {displayedChapters.map(ch => {
          const chQuestions = questions.filter(q => q.chapter === ch.id);
          const totalInCh = chQuestions.length || (ch.seqTo - ch.seqFrom + 1);
          const solvedInCh = chQuestions.filter(q => progressMap[q.seq]?.status === 'done').length;
          const chRatio = totalInCh ? (solvedInCh / totalInCh) : 0;

          return (
            <Link
              key={ch.id}
              to={`/roadmap#${ch.id}`}
              className="chapter-prog-row"
              style={{
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                gap: '4px',
                padding: '8px 12px',
                borderRadius: 'var(--radius-inner)',
                background: 'var(--glass-surface)',
                border: '1px solid var(--glass-border)',
                textDecoration: 'none',
                transition: 'all 150ms ease'
              }}
              onMouseEnter={(e) => e.currentTarget.style.background = 'var(--glass-strong)'}
              onMouseLeave={(e) => e.currentTarget.style.background = 'var(--glass-surface)'}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.825rem' }}>
                <span style={{ fontWeight: 600, color: 'var(--text-color)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {ch.order}. {ch.name}
                </span>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  {solvedInCh}/{totalInCh}
                </span>
              </div>

              <div className="progress-bar-container" style={{ height: '6px' }}>
                <div 
                  className="progress-bar-fill" 
                  style={{ width: `${Math.round(chRatio * 100)}%` }} 
                />
              </div>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
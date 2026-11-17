import React, { useMemo } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { AlertCircle, ArrowRight, BarChart2, CheckCircle2 } from 'lucide-react';

export default function NeedsAttentionCard() {
  const { questions, chapters, progressMap, statsMap, getNextUp } = useApp();
  const navigate = useNavigate();
  const nextUp = getNextUp();

  // Compute weak chapters per Section 6.4
  const weakChapters = useMemo(() => {
    if (!chapters || chapters.length === 0 || !questions || questions.length === 0) {
      return [];
    }

    const scored = [];
    chapters.forEach(ch => {
      const chQuestions = questions.filter(q => q.chapter === ch.id);
      const solvedList = chQuestions.filter(q => progressMap[q.seq]?.status === 'done');
      const solvedCount = solvedList.length;

      // Only evaluate if at least 3 solved in chapter
      if (solvedCount >= 3) {
        let mistakeCount = 0;
        let forgotCount = 0;
        let slowCount = 0;

        chQuestions.forEach(q => {
          const prog = progressMap[q.seq];
          const st = statsMap[q.seq];
          if (prog?.mistake) mistakeCount++;
          if (st?.forgotCount) forgotCount += st.forgotCount;
          if (st?.slow) slowCount++;
        });

        const score = ((2 * mistakeCount) + (2 * forgotCount) + (1 * slowCount)) / solvedCount;
        if (score > 0) {
          scored.push({
            id: ch.id,
            order: ch.order,
            name: ch.name,
            score,
            mistakeCount,
            forgotCount,
            slowCount,
            solvedCount
          });
        }
      }
    });

    // Top 3 chapters with score > 0
    scored.sort((a, b) => b.score - a.score);
    return scored.slice(0, 3);
  }, [chapters, questions, progressMap, statsMap]);

  return (
    <div 
      className="glass-card home-needs-attention-card" 
      style={{ 
        padding: '24px', 
        display: 'flex', 
        flexDirection: 'column', 
        gap: '16px',
        width: '100%',
        boxSizing: 'border-box'
      }}
    >
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '8px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <AlertCircle size={18} color="var(--accent)" />
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-color)', margin: 0 }}>
            Needs Attention
          </h3>
        </div>
        <Link 
          to="/stats" 
          style={{ 
            fontSize: '0.8rem', 
            fontWeight: 600, 
            color: 'var(--accent)', 
            display: 'flex', 
            alignItems: 'center', 
            gap: '4px',
            textDecoration: 'none'
          }}
        >
          <span>All stats</span>
          <ArrowRight size={13} />
        </Link>
      </div>

      {/* Content */}
      {weakChapters.length > 0 ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {weakChapters.map(ch => (
            <div 
              key={ch.id}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                flexWrap: 'wrap',
                gap: '8px',
                padding: '12px 14px',
                borderRadius: 'var(--radius-inner)',
                background: 'var(--glass-surface)',
                border: '1px solid var(--glass-border)'
              }}
            >
              <div style={{ minWidth: 0, flex: '1 1 200px' }}>
                <div style={{ fontWeight: 700, fontSize: '0.9rem', color: 'var(--text-color)', marginBottom: '4px' }}>
                  {ch.order}. {ch.name}
                </div>
                {/* Reason chips */}
                <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                  {ch.mistakeCount > 0 && (
                    <span style={{ fontSize: '0.72rem', padding: '2px 8px', borderRadius: 'var(--radius-pill)', background: 'rgba(239, 68, 68, 0.12)', color: '#ef4444', fontWeight: 600 }}>
                      {ch.mistakeCount} {ch.mistakeCount === 1 ? 'mistake' : 'mistakes'}
                    </span>
                  )}
                  {ch.forgotCount > 0 && (
                    <span style={{ fontSize: '0.72rem', padding: '2px 8px', borderRadius: 'var(--radius-pill)', background: 'rgba(245, 158, 11, 0.12)', color: 'var(--revisit-color)', fontWeight: 600 }}>
                      {ch.forgotCount} forgot
                    </span>
                  )}
                  {ch.slowCount > 0 && (
                    <span style={{ fontSize: '0.72rem', padding: '2px 8px', borderRadius: 'var(--radius-pill)', background: 'rgba(59, 130, 246, 0.12)', color: '#3b82f6', fontWeight: 600 }}>
                      {ch.slowCount} slow
                    </span>
                  )}
                </div>
              </div>

              <Link 
                to={`/roadmap#${ch.id}`}
                className="btn-secondary"
                style={{ padding: '6px 12px', fontSize: '0.8rem', minHeight: '36px', whiteSpace: 'nowrap' }}
              >
                Open chapter
              </Link>
            </div>
          ))}
        </div>
      ) : (
        <div style={{ textAlign: 'center', padding: '16px 8px', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '10px' }}>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', margin: 0, maxWidth: '280px', lineHeight: 1.5 }}>
            Solve a few questions and your weak spots will show here.
          </p>
          {nextUp && (
            <button 
              onClick={() => navigate(`/question/${nextUp.seq}`)} 
              className="btn-secondary"
              style={{ fontSize: '0.825rem', padding: '6px 14px', minHeight: '38px' }}
            >
              Start Next Up
            </button>
          )}
        </div>
      )}
    </div>
  );
}
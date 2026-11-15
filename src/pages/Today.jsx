import React, { useMemo } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { 
  CheckCircle2, 
  RotateCcw, 
  AlertTriangle, 
  ArrowRight, 
  Calendar as CalendarIcon,
  ExternalLink,
  Target,
  Sparkles,
  Trash2
} from 'lucide-react';

export default function Today() {
  const { 
    dueReviews, 
    reviews,
    submitReview, 
    questions, 
    chapters, 
    progressMap, 
    todaySolvedCount, 
    user, 
    getNextUp 
  } = useApp();
  const navigate = useNavigate();

  const nextUp = getNextUp();
  const dailyGoal = user?.daily_goal || 2;
  const todayStr = new Date().toISOString().split('T')[0];

  // Due & Overdue counts (Section 5.6)
  const overdueCount = useMemo(() => {
    return dueReviews.filter(r => r.due_date < todayStr).length;
  }, [dueReviews, todayStr]);

  const dueTodayCount = dueReviews.length - overdueCount;

  // Next 7 days calendar data with review dots (Section 5.6)
  const next7Days = useMemo(() => {
    const days = [];
    const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    for (let i = 0; i < 7; i++) {
      const d = new Date();
      d.setDate(d.getDate() + i);
      const iso = d.toISOString().split('T')[0];
      const count = reviews.filter(r => r.due_date === iso).length;
      days.push({
        date: d,
        iso,
        dayName: i === 0 ? 'Today' : weekdays[d.getDay()],
        dayNum: d.getDate(),
        reviewCount: count
      });
    }
    return days;
  }, [reviews]);

  // Daily goal ring calculation (Desktop: 72px radius)
  const goalPercent = Math.min(100, Math.round((todaySolvedCount / dailyGoal) * 100));
  const desktopRingRadius = 36;
  const desktopCircumference = 2 * Math.PI * desktopRingRadius;
  const desktopOffset = desktopCircumference - (Math.min(todaySolvedCount, dailyGoal) / dailyGoal) * desktopCircumference;

  // Mobile small goal ring (24px radius)
  const mobileRingRadius = 20;
  const mobileCircumference = 2 * Math.PI * mobileRingRadius;
  const mobileOffset = mobileCircumference - (Math.min(todaySolvedCount, dailyGoal) / dailyGoal) * mobileCircumference;

  return (
    <div className="today-page-root" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', width: '100%' }}>
      
      {/* Page Heading with Counts (Part 2 #7) */}
      <div style={{
        display: 'flex',
        alignItems: 'baseline',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '0.75rem'
      }}>
        <div>
          <h1 style={{ 
            fontSize: '1.85rem', 
            fontWeight: 800, 
            letterSpacing: '-0.03em', 
            color: 'var(--text-color)',
            lineHeight: 1.2
          }}>
            Today’s Reviews
          </h1>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
            Spaced repetition recall: 1 → 3 → 7 → 21 days
          </p>
        </div>

        {/* Count Badges */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
          <div style={{
            padding: '6px 14px',
            borderRadius: 'var(--radius-pill)',
            background: 'var(--glass-surface)',
            border: '1px solid var(--glass-border)',
            fontSize: '0.85rem',
            fontWeight: 700,
            color: 'var(--text-color)'
          }}>
            <span>{dueReviews.length} due</span>
          </div>

          {overdueCount > 0 && (
            <div style={{
              padding: '6px 14px',
              borderRadius: 'var(--radius-pill)',
              background: 'var(--revisit-bg)',
              border: '1px solid var(--revisit-color)',
              fontSize: '0.85rem',
              fontWeight: 700,
              color: 'var(--revisit-color)'
            }}>
              <span>{overdueCount} overdue</span>
            </div>
          )}
        </div>
      </div>

      {/* MOBILE ONLY: Daily Goal Ring + Next 7 Days Strip (Part 2 #7) */}
      <div className="today-mobile-top-section">
        {/* Small Goal Ring under heading */}
        <div className="glass-card today-mobile-goal-card" style={{ padding: '12px 16px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{ position: 'relative', width: 48, height: 48, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <svg width="48" height="48">
                <circle cx="24" cy="24" r={mobileRingRadius} stroke="var(--progress-track)" strokeWidth="4" fill="none" />
                <circle 
                  className="progress-ring-circle" 
                  cx="24" cy="24" r={mobileRingRadius} 
                  stroke="var(--accent)" strokeWidth="4" 
                  strokeDasharray={mobileCircumference} 
                  strokeDashoffset={mobileOffset} 
                  strokeLinecap="round" fill="none" 
                />
              </svg>
              <span style={{ position: 'absolute', fontSize: '0.75rem', fontWeight: 800, fontFamily: 'var(--font-mono)' }}>
                {todaySolvedCount}/{dailyGoal}
              </span>
            </div>
            <div>
              <div style={{ fontSize: '0.875rem', fontWeight: 700, color: 'var(--text-color)' }}>
                Today's Daily Goal
              </div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                {todaySolvedCount >= dailyGoal ? "Goal completed!" : `${dailyGoal - todaySolvedCount} questions remaining`}
              </div>
            </div>
          </div>
          <Target size={18} color="var(--accent)" />
        </div>

        {/* Next 7 Days horizontal strip of day chips at top (Part 2 #7) */}
        <div className="today-mobile-calendar-strip">
          {next7Days.map((d, idx) => (
            <div 
              key={idx} 
              className={`today-mobile-day-chip ${idx === 0 ? 'active' : ''}`}
            >
              <span className="day-chip-name">{d.dayName}</span>
              <span className="day-chip-num">{d.dayNum}</span>
              {d.reviewCount > 0 ? (
                <span className="day-chip-dot" title={`${d.reviewCount} due`} />
              ) : (
                <span className="day-chip-empty" />
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Main Grid: Reviews List (Left on desktop) + Sidebar (Right on desktop) */}
      <div className="today-grid-container" style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(12, 1fr)',
        gap: '1.5rem',
        alignItems: 'start'
      }}>
        {/* LEFT (8 cols): Due & Overdue Review Cards */}
        <div className="today-col-left" style={{
          gridColumn: 'span 8',
          display: 'flex',
          flexDirection: 'column',
          gap: '1rem'
        }}>
          {dueReviews.length === 0 ? (
            /* Empty State: "All caught up" */
            <div className="glass-card" style={{
              padding: '3.5rem 2rem',
              textAlign: 'center',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '1rem'
            }}>
              <div style={{
                width: 64,
                height: 64,
                borderRadius: '50%',
                background: 'rgba(16, 185, 129, 0.15)',
                border: '1px solid rgba(16, 185, 129, 0.35)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#10B981'
              }}>
                <CheckCircle2 size={34} />
              </div>

              <div>
                <h3 style={{ fontSize: '1.35rem', fontWeight: 700, color: 'var(--text-color)', marginBottom: '0.35rem' }}>
                  All caught up
                </h3>
                <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', maxWidth: '400px', lineHeight: 1.55 }}>
                  You have completed all scheduled spaced-repetition reviews for today. Continue progressing along the roadmap to schedule new reviews.
                </p>
              </div>

              {nextUp && (
                <button
                  type="button"
                  onClick={() => navigate(`/question/${nextUp.seq}`)}
                  className="btn-primary"
                  style={{ marginTop: '0.5rem', padding: '0.65rem 1.35rem', fontSize: '0.9rem', minHeight: '44px' }}
                >
                  <span>Open Next Up (#{nextUp.seq})</span>
                  <ArrowRight size={15} />
                </button>
              )}
            </div>
          ) : (
            /* List of Review Cards: Stacked one per row, Recalled & Forgot side by side at full width, 48px high (Part 2 #7) */
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              {dueReviews.map((rev) => {
                const q = questions.find(item => item.seq === rev.question_seq);
                if (!q) return null;

                const isOverdue = rev.due_date < todayStr;
                const mistake = progressMap[q.seq]?.mistake;
                const ch = chapters.find(c => c.id === q.chapter);

                return (
                  <div
                    key={rev.question_seq}
                    className="glass-card today-review-card"
                    style={{
                      padding: '20px',
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '1rem',
                      borderColor: isOverdue ? 'var(--revisit-color)' : 'var(--glass-border)'
                    }}
                  >
                    {/* Header info row */}
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.5rem' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
                        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 700 }}>
                          #{q.seq}
                        </span>

                        {ch && (
                          <span style={{
                            fontSize: '0.75rem',
                            fontWeight: 600,
                            padding: '3px 8px',
                            borderRadius: 'var(--radius-pill)',
                            background: 'var(--glass-surface)',
                            border: '1px solid var(--glass-border)',
                            color: 'var(--text-color)'
                          }}>
                            {ch.name}
                          </span>
                        )}

                        <span className={`diff-pill diff-pill-${q.difficulty.toLowerCase()}`}>
                          {q.difficulty}
                        </span>

                        {mistake && (
                          <span style={{
                            display: 'inline-flex',
                            alignItems: 'center',
                            gap: '3px',
                            padding: '3px 8px',
                            borderRadius: 'var(--radius-pill)',
                            background: 'rgba(239, 68, 68, 0.15)',
                            border: '1px solid rgba(239, 68, 68, 0.35)',
                            color: '#EF4444',
                            fontSize: '0.72rem',
                            fontWeight: 700
                          }}>
                            <AlertTriangle size={11} />
                            <span>Mistake</span>
                          </span>
                        )}
                      </div>

                      {/* Due date badge in revisit colour */}
                      <span className="due-chip">
                        {isOverdue ? `Overdue (${rev.due_date})` : `Due Today (${rev.due_date})`}
                      </span>
                    </div>

                    {/* Problem Title Link */}
                    <div>
                      <Link
                        to={`/question/${q.seq}`}
                        style={{
                          fontSize: '1.15rem',
                          fontWeight: 700,
                          color: 'var(--text-color)',
                          letterSpacing: '-0.01em',
                          display: 'inline-block'
                        }}
                      >
                        {q.title}
                      </Link>
                      <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px', lineHeight: 1.45 }}>
                        Step {rev.step + 1} of 4 · Spaced interval: {['1 day', '3 days', '7 days', '21 days'][rev.step] || '21 days'}
                      </p>
                    </div>

                    {/* Recalled and Forgot buttons sit side by side at full width, 48 px high (Part 2 #7) */}
                    <div className="today-review-actions" style={{
                      display: 'grid',
                      gridTemplateColumns: '1fr 1fr',
                      gap: '10px',
                      width: '100%',
                      marginTop: '0.25rem'
                    }}>
                      <button
                        type="button"
                        onClick={() => submitReview({ questionSeq: rev.question_seq, action: 'recalled' })}
                        className="btn-primary"
                        style={{
                          width: '100%',
                          minHeight: '48px',
                          fontSize: '0.9rem',
                          background: '#10B981',
                          borderColor: '#10B981',
                          justifyContent: 'center',
                          gap: '0.45rem'
                        }}
                        title="Remembered the solution approach without checking hints"
                      >
                        <CheckCircle2 size={16} />
                        <span>Recalled</span>
                      </button>

                      <button
                        type="button"
                        onClick={() => submitReview({ questionSeq: rev.question_seq, action: 'forgot' })}
                        className="btn-secondary"
                        style={{
                          width: '100%',
                          minHeight: '48px',
                          fontSize: '0.9rem',
                          borderColor: '#EF4444',
                          color: '#EF4444',
                          justifyContent: 'center',
                          gap: '0.45rem'
                        }}
                        title="Needed hints; reset interval to 1 day and mark mistake"
                      >
                        <RotateCcw size={16} />
                        <span>Forgot</span>
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* RIGHT SIDEBAR (4 cols on desktop): Daily Goal Ring Card + Calendar Card (Desktop only) */}
        <aside className="today-col-right" style={{
          gridColumn: 'span 4',
          display: 'flex',
          flexDirection: 'column',
          gap: '1.25rem'
        }}>
          {/* Daily Goal Card */}
          <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center' }}>
            <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-color)', marginBottom: '16px' }}>
              Daily Progress Target
            </h3>

            <div className="progress-ring-wrap" style={{ width: 96, height: 96 }}>
              <svg width="96" height="96">
                <circle cx="48" cy="48" r={desktopRingRadius} stroke="var(--progress-track)" strokeWidth="8" fill="none" />
                <circle
                  className="progress-ring-circle"
                  cx="48" cy="48" r={desktopRingRadius}
                  stroke="var(--accent)"
                  strokeWidth="8"
                  strokeDasharray={desktopCircumference}
                  strokeDashoffset={desktopOffset}
                  strokeLinecap="round"
                  fill="none"
                />
              </svg>

              <div style={{ position: 'absolute', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <span style={{ fontSize: '1.4rem', fontWeight: 800, lineHeight: 1, fontFamily: 'var(--font-sans)', fontVariantNumeric: 'tabular-nums' }}>
                  {todaySolvedCount}
                </span>
                <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: 600 }}>
                  of {dailyGoal}
                </span>
              </div>
            </div>

            <div style={{ marginTop: '16px', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              {todaySolvedCount >= dailyGoal ? (
                <span style={{ color: '#10B981', fontWeight: 600 }}>✓ Daily goal accomplished!</span>
              ) : (
                <span>{dailyGoal - todaySolvedCount} more questions to hit daily target</span>
              )}
            </div>
          </div>

          {/* Next 7 Days Calendar Card */}
          <div className="glass-card" style={{ padding: '24px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
              <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-color)' }}>
                Next 7 Days Schedule
              </h3>
              <CalendarIcon size={16} color="var(--text-muted)" />
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {next7Days.map((d, idx) => (
                <div
                  key={idx}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '8px 12px',
                    borderRadius: 'var(--radius-inner)',
                    background: idx === 0 ? 'var(--accent-soft)' : 'var(--glass-surface)',
                    border: '1px solid',
                    borderColor: idx === 0 ? 'var(--accent)' : 'var(--glass-border)',
                    fontSize: '0.85rem'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span style={{ fontWeight: idx === 0 ? 700 : 500, color: idx === 0 ? 'var(--accent-soft-text)' : 'var(--text-color)' }}>
                      {d.dayName}
                    </span>
                    <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                      {d.date.toLocaleString('default', { month: 'short' })} {d.dayNum}
                    </span>
                  </div>

                  {d.reviewCount > 0 ? (
                    <span style={{
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: '4px',
                      fontFamily: 'var(--font-mono)',
                      fontSize: '0.75rem',
                      fontWeight: 700,
                      color: 'var(--revisit-color)'
                    }}>
                      <span style={{ width: 7, height: 7, borderRadius: '50%', background: 'var(--revisit-color)' }} />
                      <span>{d.reviewCount} due</span>
                    </span>
                  ) : (
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>—</span>
                  )}
                </div>
              ))}
            </div>
          </div>
        </aside>
      </div>

    </div>
  );
}

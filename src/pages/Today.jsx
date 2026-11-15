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

  // Daily goal ring calculation
  const goalPercent = Math.min(100, Math.round((todaySolvedCount / dailyGoal) * 100));
  const ringRadius = 36;
  const ringCircumference = 2 * Math.PI * ringRadius;
  const ringOffset = ringCircumference - (Math.min(todaySolvedCount, dailyGoal) / dailyGoal) * ringCircumference;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', width: '100%' }}>
      {/* Page Heading with Counts (Section 5.6) */}
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
            fontSize: '0.825rem',
            fontWeight: 600,
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
              fontSize: '0.825rem',
              fontWeight: 700,
              color: 'var(--revisit-color)'
            }}>
              <span>{overdueCount} overdue</span>
            </div>
          )}
        </div>
      </div>

      {/* Main Grid: Reviews List (Left) + Sidebar (Right) */}
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
            /* Empty State: "All caught up" with button to open Next up (Section 5.6) */
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
                  onClick={() => navigate(`/question/${nextUp.seq}`)}
                  className="btn-primary"
                  style={{ marginTop: '0.5rem', padding: '0.55rem 1.25rem', fontSize: '0.875rem' }}
                >
                  <span>Open Next Up (#{nextUp.seq})</span>
                  <ArrowRight size={15} />
                </button>
              )}
            </div>
          ) : (
            /* List of Review Cards (Section 5.6: title, chapter chip, difficulty, mistake tag, due date in revisit colour, Recalled & Forgot buttons) */
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
                    className="glass-card"
                    style={{
                      padding: '18px 22px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      flexWrap: 'wrap',
                      gap: '1rem',
                      borderColor: isOverdue ? 'var(--revisit-color)' : 'var(--glass-border)'
                    }}
                  >
                    {/* Left: Info */}
                    <div style={{ flex: '1 1 280px', display: 'flex', flexDirection: 'column', gap: '0.45rem' }}>
                      {/* Meta chips: Seq, Chapter, Difficulty, Mistake */}
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
                        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600 }}>
                          #{q.seq}
                        </span>

                        {ch && (
                          <span style={{
                            fontSize: '0.75rem',
                            fontWeight: 600,
                            padding: '2px 8px',
                            borderRadius: 'var(--radius-pill)',
                            background: 'var(--glass-surface)',
                            border: '1px solid var(--glass-border)',
                            color: 'var(--text-muted)'
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
                            fontSize: '0.72rem',
                            fontWeight: 700,
                            padding: '2px 8px',
                            borderRadius: 'var(--radius-pill)',
                            background: 'rgba(239, 68, 68, 0.15)',
                            color: '#EF4444',
                            border: '1px solid rgba(239, 68, 68, 0.3)'
                          }}>
                            <AlertTriangle size={12} />
                            <span>Mistake</span>
                          </span>
                        )}
                      </div>

                      {/* Question Title */}
                      <Link 
                        to={`/question/${q.seq}`} 
                        style={{ 
                          fontSize: '1.05rem', 
                          fontWeight: 700, 
                          color: 'var(--text-color)', 
                          letterSpacing: '-0.01em',
                          textDecoration: 'none'
                        }}
                      >
                        {q.title}
                      </Link>

                      {/* Due date info (overdue in revisit colour) */}
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                        <span style={{
                          color: isOverdue ? 'var(--revisit-color)' : 'var(--text-muted)',
                          fontWeight: isOverdue ? 700 : 500
                        }}>
                          {isOverdue ? `Overdue (${rev.due_date})` : `Due today`}
                        </span>
                        <span>·</span>
                        <span>Step {rev.step + 1} of 4</span>
                      </div>
                    </div>

                    {/* Right: Actions (Recalled & Forgot) */}
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
                      {/* Recalled Button (Success) */}
                      <button
                        onClick={() => submitReview({ questionSeq: q.seq, action: 'recalled' })}
                        className="btn-primary"
                        style={{
                          padding: '0.45rem 1rem',
                          fontSize: '0.825rem',
                          borderRadius: 'var(--radius-pill)'
                        }}
                        title="Remembered the optimal approach without checking hints"
                      >
                        <CheckCircle2 size={14} />
                        <span>Recalled</span>
                      </button>

                      {/* Forgot Button */}
                      <button
                        onClick={() => submitReview({ questionSeq: q.seq, action: 'forgot' })}
                        className="btn-secondary"
                        style={{
                          padding: '0.45rem 0.9rem',
                          fontSize: '0.825rem',
                          borderRadius: 'var(--radius-pill)',
                          color: 'var(--revisit-color)',
                          borderColor: 'var(--revisit-color)'
                        }}
                        title="Forgot pattern; resets review to step 1 (due tomorrow)"
                      >
                        <RotateCcw size={14} />
                        <span>Forgot</span>
                      </button>

                      {/* Dismiss from Queue */}
                      <button
                        onClick={() => submitReview({ questionSeq: q.seq, action: 'delete' })}
                        className="icon-circle-btn"
                        style={{ width: 34, height: 34 }}
                        title="Remove from review queue"
                      >
                        <Trash2 size={14} />
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* RIGHT (4 cols): Side Widgets (Desktop) or Bottom (Mobile) */}
        <div className="today-col-right" style={{
          gridColumn: 'span 4',
          display: 'flex',
          flexDirection: 'column',
          gap: '1.25rem'
        }}>
          {/* Widget 1: Next 7 Days Small Calendar with Dots (Section 5.6) */}
          <div className="glass-card" style={{ padding: '20px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
              <CalendarIcon size={16} color="var(--accent)" />
              <h3 style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-color)' }}>
                Next 7 Days
              </h3>
            </div>

            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(7, 1fr)',
              gap: '6px',
              textAlign: 'center'
            }}>
              {next7Days.map((d, idx) => (
                <div 
                  key={d.iso}
                  style={{
                    padding: '8px 2px',
                    borderRadius: 'var(--radius-inner)',
                    background: idx === 0 ? 'var(--accent-soft)' : 'var(--glass-surface)',
                    border: '1px solid',
                    borderColor: idx === 0 ? 'var(--accent)' : 'var(--glass-border)',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    gap: '4px'
                  }}
                >
                  <span style={{ fontSize: '0.68rem', fontWeight: 600, color: 'var(--text-muted)' }}>
                    {d.dayName}
                  </span>
                  <span style={{
                    fontSize: '0.95rem',
                    fontWeight: 700,
                    fontFamily: 'var(--font-mono)',
                    color: idx === 0 ? 'var(--accent-soft-text)' : 'var(--text-color)'
                  }}>
                    {d.dayNum}
                  </span>
                  
                  {/* Review Dot indicator */}
                  <div style={{ height: 6, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    {d.reviewCount > 0 ? (
                      <span 
                        style={{
                          width: 6,
                          height: 6,
                          borderRadius: '50%',
                          background: idx === 0 ? 'var(--accent)' : 'var(--revisit-color)'
                        }}
                        title={`${d.reviewCount} review${d.reviewCount > 1 ? 's' : ''} scheduled`}
                      />
                    ) : null}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Widget 2: Daily Goal Ring (Section 5.6) */}
          <div className="glass-card" style={{ padding: '20px', display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
            <div style={{ position: 'relative', width: 84, height: 84, flexShrink: 0 }}>
              <svg width="84" height="84" viewBox="0 0 84 84">
                {/* Background Track */}
                <circle
                  cx="42"
                  cy="42"
                  r={ringRadius}
                  stroke="var(--progress-track)"
                  strokeWidth="8"
                  fill="none"
                />
                {/* Progress Arc */}
                <circle
                  cx="42"
                  cy="42"
                  r={ringRadius}
                  stroke="var(--accent)"
                  strokeWidth="8"
                  strokeDasharray={ringCircumference}
                  strokeDashoffset={ringOffset}
                  strokeLinecap="round"
                  fill="none"
                  transform="rotate(-90 42 42)"
                />
              </svg>
              <div style={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontFamily: 'var(--font-mono)',
                fontSize: '0.85rem',
                fontWeight: 700,
                color: 'var(--text-color)'
              }}>
                {goalPercent}%
              </div>
            </div>

            <div>
              <div style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                Daily Goal
              </div>
              <div style={{ fontSize: '1.15rem', fontWeight: 800, color: 'var(--text-color)', marginTop: '2px' }}>
                {todaySolvedCount} of {dailyGoal} solved
              </div>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                {todaySolvedCount >= dailyGoal ? 'Goal achieved today!' : `${dailyGoal - todaySolvedCount} more to hit your goal.`}
              </p>
            </div>
          </div>

          {/* Widget 3: Next Up Shortcut Card (Section 5.6) */}
          {nextUp && (
            <div className="glass-card" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span style={{
                  fontSize: '0.75rem',
                  fontWeight: 700,
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em',
                  color: 'var(--accent)'
                }}>
                  Next Up Shortcut
                </span>
                <span className={`diff-pill diff-pill-${nextUp.difficulty.toLowerCase()}`}>
                  {nextUp.difficulty}
                </span>
              </div>

              <div>
                <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                  Seq #{nextUp.seq} · LC #{nextUp.lc}
                </div>
                <h4 style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--text-color)', marginTop: '3px', lineHeight: 1.3 }}>
                  {nextUp.title}
                </h4>
              </div>

              <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.35rem' }}>
                <button
                  onClick={() => navigate(`/question/${nextUp.seq}`)}
                  className="btn-primary"
                  style={{ flex: 1, padding: '0.45rem 0.85rem', fontSize: '0.825rem' }}
                >
                  <span>Solve</span>
                  <ArrowRight size={14} />
                </button>
                <a
                  href={`https://leetcode.com/problems/${nextUp.slug}/`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-secondary"
                  style={{ padding: '0.45rem 0.75rem', fontSize: '0.825rem' }}
                  title="Open on LeetCode"
                >
                  <ExternalLink size={14} />
                </a>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

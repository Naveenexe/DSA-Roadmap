import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { 
  CheckCircle2, 
  RotateCcw, 
  AlertTriangle, 
  Trash2, 
  ArrowRight, 
  Target,
  ExternalLink
} from 'lucide-react';

export default function Today() {
  const { 
    dueReviews, 
    upcomingReviews, 
    submitReview, 
    questions, 
    progressMap, 
    todaySolvedCount, 
    user, 
    getNextUp 
  } = useApp();
  const navigate = useNavigate();

  const nextUp = getNextUp();
  const dailyGoal = user?.daily_goal || 2;
  const goalPercent = Math.min(100, Math.round((todaySolvedCount / dailyGoal) * 100));

  const todayStr = new Date().toISOString().split('T')[0];
  const intervals = [1, 3, 7, 21];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', width: '100%', maxWidth: '1440px', margin: '0 auto' }}>
      {/* Top Banner: Today's Target */}
      <div className="panel" style={{
        padding: '1rem 1.25rem'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem', marginBottom: '0.75rem' }}>
          <div>
            <h1 style={{ fontSize: '1.25rem', fontWeight: 700, letterSpacing: '-0.01em' }}>Today's Focus</h1>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              Spaced repetition reviews (1 → 3 → 7 → 21 days) to keep algorithmic patterns fresh.
            </p>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', background: 'var(--bg-input)', padding: '0.4rem 0.85rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border)' }}>
            <Target size={16} color="var(--accent)" />
            <div>
              <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Daily Goal</div>
              <div style={{ fontSize: '0.95rem', fontWeight: 700 }}>
                {todaySolvedCount} / {dailyGoal} solved
              </div>
            </div>
          </div>
        </div>

        <div style={{ height: 4, background: 'var(--border)', borderRadius: 2, overflow: 'hidden' }}>
          <div style={{ width: `${goalPercent}%`, height: '100%', background: 'var(--accent)' }} />
        </div>
      </div>

      {/* Next Up Card */}
      {nextUp && (
        <div className="panel" style={{ padding: '0.85rem 1.25rem', borderLeft: '3px solid var(--accent)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem' }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.2rem' }}>
                <span style={{ background: 'var(--accent-light)', color: 'var(--accent)', fontSize: '0.75rem', fontWeight: 700, padding: '0.15rem 0.5rem', borderRadius: 'var(--radius-sm)' }}>
                  Next Up
                </span>
                <span className={`chip-${nextUp.difficulty.toLowerCase()}`}>{nextUp.difficulty}</span>
                <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>Seq #{nextUp.seq} · LC #{nextUp.lc}</span>
              </div>
              <h3 style={{ fontSize: '1.05rem', fontWeight: 700 }}>
                <Link to={`/question/${nextUp.seq}`} style={{ color: 'inherit' }}>
                  {nextUp.title}
                </Link>
              </h3>
            </div>

            <button onClick={() => navigate(`/question/${nextUp.seq}`)} className="btn-primary" style={{ fontSize: '0.8rem', padding: '0.35rem 0.85rem' }}>
              <span>Solve Problem</span>
              <ArrowRight size={13} />
            </button>
          </div>
        </div>
      )}

      {/* Due & Overdue Reviews Section */}
      <div className="panel" style={{ padding: '1rem 1.25rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.85rem' }}>
          <div>
            <h2 style={{ fontSize: '1.05rem', fontWeight: 700 }}>
              Due for Review ({dueReviews.length})
            </h2>
            <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
              Recall the optimal technique without looking at solution hints. Spaced steps: 1 → 3 → 7 → 21 days.
            </p>
          </div>
        </div>

        {dueReviews.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '1.5rem', color: 'var(--text-muted)' }}>
            <CheckCircle2 size={32} color="var(--status-done)" style={{ margin: '0 auto 0.4rem auto' }} />
            <p style={{ fontWeight: 600, color: 'var(--text-main)', fontSize: '0.9rem' }}>All reviews caught up for today!</p>
            <p style={{ fontSize: '0.78rem' }}>Continue along the roadmap to schedule new reviews.</p>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {dueReviews.map((rev) => {
              const q = questions.find(item => item.seq === rev.question_seq);
              if (!q) return null;

              const isOverdue = rev.due_date < todayStr;
              const mistake = progressMap[q.seq]?.mistake;
              const intervalDays = intervals[Math.min(rev.step, intervals.length - 1)];

              return (
                <div
                  key={rev.question_seq}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '0.75rem 1rem',
                    background: 'var(--bg-input)',
                    border: '1px solid var(--border)',
                    borderRadius: 'var(--radius-sm)',
                    flexWrap: 'wrap',
                    gap: '0.75rem'
                  }}
                >
                  <div style={{ flex: '1 1 240px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.2rem', flexWrap: 'wrap' }}>
                      <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                        #{q.seq}
                      </span>
                      <Link to={`/question/${q.seq}`} style={{ fontWeight: 600, fontSize: '0.9rem', color: 'inherit' }}>
                        {q.title}
                      </Link>
                      <span className={`chip-${q.difficulty.toLowerCase()}`}>
                        {q.difficulty}
                      </span>
                      {mistake && (
                        <span style={{ background: 'var(--hard-bg)', color: 'var(--hard)', fontSize: '0.7rem', fontWeight: 600, padding: '0.1rem 0.4rem', borderRadius: 'var(--radius-sm)', border: '1px solid rgba(239, 71, 67, 0.25)' }}>
                          Mistake
                        </span>
                      )}
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                      <span>LC #{q.lc}</span>
                      <span>·</span>
                      <span style={{ color: isOverdue ? 'var(--hard)' : 'var(--text-muted)', fontWeight: isOverdue ? 600 : 400 }}>
                        {isOverdue ? `Overdue (${rev.due_date})` : `Due today`}
                      </span>
                      <span>·</span>
                      <span>Interval Step {rev.step + 1}/4 (+{intervalDays}d)</span>
                    </div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                    <button
                      onClick={() => submitReview({ questionSeq: q.seq, action: 'recalled' })}
                      className="btn-primary"
                      style={{ fontSize: '0.78rem', padding: '0.3rem 0.7rem', background: 'var(--status-done)', borderColor: 'var(--status-done)' }}
                      title="Remembered the approach without hints"
                    >
                      <CheckCircle2 size={13} />
                      <span>Recalled</span>
                    </button>

                    <button
                      onClick={() => submitReview({ questionSeq: q.seq, action: 'forgot' })}
                      className="btn-secondary"
                      style={{ fontSize: '0.78rem', padding: '0.3rem 0.7rem', color: 'var(--hard)', borderColor: 'rgba(239, 71, 67, 0.3)' }}
                      title="Needed hint or forgot approach; resets review to tomorrow"
                    >
                      <RotateCcw size={13} />
                      <span>Forgot</span>
                    </button>

                    <button
                      onClick={() => submitReview({ questionSeq: q.seq, action: 'delete' })}
                      className="icon-btn"
                      style={{ width: 28, height: 28 }}
                      title="Remove from review queue"
                    >
                      <Trash2 size={13} />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Upcoming Reviews (Next 7 Days) */}
      <div className="panel" style={{ padding: '1rem 1.25rem' }}>
        <h2 style={{ fontSize: '0.95rem', fontWeight: 700, marginBottom: '0.65rem' }}>
          Upcoming Reviews (Next 7 Days)
        </h2>
        {upcomingReviews.length === 0 ? (
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            No reviews scheduled in the next 7 days.
          </p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
            {upcomingReviews.map(rev => {
              const q = questions.find(item => item.seq === rev.question_seq);
              if (!q) return null;
              return (
                <div
                  key={rev.question_seq}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '0.5rem 0.75rem',
                    background: 'var(--bg-input)',
                    borderRadius: 'var(--radius-sm)',
                    border: '1px solid var(--border)',
                    fontSize: '0.8rem'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                    <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.72rem', color: 'var(--text-muted)' }}>#{q.seq}</span>
                    <Link to={`/question/${q.seq}`} style={{ fontWeight: 600, color: 'inherit' }}>{q.title}</Link>
                    <span className={`chip-${q.difficulty.toLowerCase()}`}>{q.difficulty}</span>
                  </div>
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                    Due {rev.due_date}
                  </span>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

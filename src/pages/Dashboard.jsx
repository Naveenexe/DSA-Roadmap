import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { 
  CheckCircle2, 
  Flame, 
  Target, 
  RotateCcw, 
  ArrowRight, 
  ExternalLink,
  BookOpen,
  Sparkles
} from 'lucide-react';

export default function Dashboard({ onOpenLogin }) {
  const { 
    user, 
    questions, 
    chapters, 
    progressMap, 
    streak, 
    todaySolvedCount, 
    getNextUp, 
    dueReviews,
    activity
  } = useApp();
  const navigate = useNavigate();

  const nextUp = getNextUp();

  // Stats calculation
  const totalQuestions = questions.length || 300;
  const doneCount = Object.values(progressMap).filter(p => p.status === 'done').length;
  const inProgressCount = Object.values(progressMap).filter(p => p.status === 'in_progress').length;
  const revisitCount = Object.values(progressMap).filter(p => p.status === 'revisit').length;
  const percentComplete = Math.round((doneCount / totalQuestions) * 100);

  // Difficulty stats
  const diffStats = {
    Easy: { done: 0, total: 0 },
    Medium: { done: 0, total: 0 },
    Hard: { done: 0, total: 0 }
  };

  questions.forEach(q => {
    if (diffStats[q.difficulty]) {
      diffStats[q.difficulty].total++;
      if (progressMap[q.seq]?.status === 'done') {
        diffStats[q.difficulty].done++;
      }
    }
  });

  // 12-week activity grid data (84 days)
  const activityMap = {};
  activity.forEach(a => {
    activityMap[a.day] = a.solved_count;
  });

  const activityDays = [];
  const today = new Date();
  for (let i = 83; i >= 0; i--) {
    const d = new Date();
    d.setDate(today.getDate() - i);
    const dateStr = d.toISOString().split('T')[0];
    activityDays.push({
      date: dateStr,
      count: activityMap[dateStr] || 0
    });
  }

  const dailyGoal = user?.daily_goal || 2;
  const goalPercent = Math.min(100, Math.round((todaySolvedCount / dailyGoal) * 100));

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', width: '100%', maxWidth: '1440px', margin: '0 auto' }}>
      {/* Top Banner / Welcome */}
      <div className="panel" style={{
        display: 'flex',
        flexWrap: 'wrap',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: '0.75rem',
        padding: '1rem 1.25rem'
      }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.2rem' }}>
            <h1 style={{ fontSize: '1.25rem', fontWeight: 700, letterSpacing: '-0.01em' }}>
              {user ? `Welcome back, ${user.username}` : 'DSA Roadmap Tracker'}
            </h1>
          </div>
          <p style={{ fontSize: '0.825rem', color: 'var(--text-muted)' }}>
            Curated sequence of 300 problems across 18 chapters with spaced repetition.
          </p>
        </div>

        {!user && (
          <button onClick={onOpenLogin} className="btn-primary" style={{ padding: '0.4rem 0.85rem', fontSize: '0.825rem' }}>
            Sign In to Sync
          </button>
        )}
      </div>

      {/* Next Up Card */}
      {nextUp ? (
        <div className="panel" style={{
          padding: '1rem 1.25rem',
          borderLeft: '3px solid var(--accent)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem', flexWrap: 'wrap', gap: '0.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <span style={{ background: 'var(--accent-light)', color: 'var(--accent)', fontSize: '0.75rem', fontWeight: 700, padding: '0.15rem 0.5rem', borderRadius: 'var(--radius-sm)' }}>
                Next Up in Chain
              </span>
              <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                Seq #{nextUp.seq} · LC #{nextUp.lc}
              </span>
            </div>
            <span className={`chip-${nextUp.difficulty.toLowerCase()}`}>
              {nextUp.difficulty}
            </span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '1rem', flexWrap: 'wrap' }}>
            <div>
              <h2 style={{ fontSize: '1.15rem', fontWeight: 700, marginBottom: '0.25rem' }}>
                <Link to={`/question/${nextUp.seq}`} style={{ color: 'inherit' }}>
                  {nextUp.title}
                </Link>
              </h2>
              <p style={{ fontSize: '0.825rem', color: 'var(--text-muted)' }}>
                <strong style={{ color: 'var(--text-sub)' }}>Key insight:</strong> {nextUp.optimal.idea}
              </p>
            </div>

            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <a
                href={`https://leetcode.com/problems/${nextUp.slug}/`}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-outline-orange"
                style={{ fontSize: '0.8rem', padding: '0.35rem 0.75rem' }}
              >
                <span>LeetCode</span>
                <ExternalLink size={13} />
              </a>
              <button 
                onClick={() => navigate(`/question/${nextUp.seq}`)} 
                className="btn-primary"
                style={{ fontSize: '0.8rem', padding: '0.35rem 0.85rem' }}
              >
                <span>Solve Now</span>
                <ArrowRight size={13} />
              </button>
            </div>
          </div>
        </div>
      ) : (
        <div className="panel" style={{ textAlign: 'center', padding: '1.5rem' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--status-done)' }}>
            All 300 Roadmap Questions Completed!
          </h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.825rem', marginTop: '0.35rem' }}>
            Maintain your spaced repetition reviews to preserve algorithmic recall.
          </p>
        </div>
      )}

      {/* Quick Metrics Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '0.75rem'
      }}>
        {/* Daily Goal Card */}
        <div className="panel" style={{ padding: '0.85rem 1rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)' }}>Today's Goal</span>
            <Target size={15} color="var(--accent)" />
          </div>
          <div style={{ fontSize: '1.4rem', fontWeight: 700, marginBottom: '0.35rem' }}>
            {todaySolvedCount} <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 400 }}>/ {dailyGoal} solved</span>
          </div>
          <div style={{ height: 4, background: 'var(--border)', borderRadius: 2, overflow: 'hidden' }}>
            <div style={{ width: `${goalPercent}%`, height: '100%', background: 'var(--accent)' }} />
          </div>
        </div>

        {/* Streak Card */}
        <div className="panel" style={{ padding: '0.85rem 1rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)' }}>Daily Streak</span>
            <Flame size={15} color="var(--accent)" />
          </div>
          <div style={{ fontSize: '1.4rem', fontWeight: 700, color: 'var(--accent)', marginBottom: '0.35rem' }}>
            {streak} <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 400 }}>days</span>
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            {todaySolvedCount > 0 ? "Goal met for today!" : "Solve 1 problem today to keep streak active"}
          </p>
        </div>

        {/* Due Reviews Card */}
        <div className="panel" style={{ padding: '0.85rem 1rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)' }}>Due Reviews</span>
            <RotateCcw size={15} color="var(--status-revisit)" />
          </div>
          <div style={{ fontSize: '1.4rem', fontWeight: 700, color: dueReviews.length > 0 ? 'var(--hard)' : 'var(--text-main)', marginBottom: '0.35rem' }}>
            {dueReviews.length} <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 400 }}>pending</span>
          </div>
          <Link to="/today" style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--accent)', display: 'inline-flex', alignItems: 'center', gap: '0.2rem' }}>
            Open Review Queue <ArrowRight size={11} />
          </Link>
        </div>

        {/* Total Progress */}
        <div className="panel" style={{ padding: '0.85rem 1rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)' }}>Overall Solved</span>
            <CheckCircle2 size={15} color="var(--status-done)" />
          </div>
          <div style={{ fontSize: '1.4rem', fontWeight: 700, color: 'var(--status-done)', marginBottom: '0.35rem' }}>
            {doneCount} <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 400 }}>/ {totalQuestions} ({percentComplete}%)</span>
          </div>
          <div style={{ height: 4, background: 'var(--border)', borderRadius: 2, overflow: 'hidden' }}>
            <div style={{ width: `${percentComplete}%`, height: '100%', background: 'var(--status-done)' }} />
          </div>
        </div>
      </div>

      {/* Difficulty Breakdown & Activity Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: '0.75rem'
      }}>
        {/* Difficulty Breakdown Panel */}
        <div className="panel" style={{ padding: '1rem' }}>
          <h3 style={{ fontSize: '0.9rem', fontWeight: 700, marginBottom: '0.75rem' }}>
            Difficulty Breakdown
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
            {['Easy', 'Medium', 'Hard'].map(diff => {
              const stat = diffStats[diff];
              const pct = stat.total ? Math.round((stat.done / stat.total) * 100) : 0;
              const colorVar = diff === 'Easy' ? 'var(--easy)' : diff === 'Medium' ? 'var(--medium)' : 'var(--hard)';
              return (
                <div key={diff}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', marginBottom: '0.25rem' }}>
                    <span style={{ fontWeight: 600, color: colorVar }}>{diff}</span>
                    <span style={{ color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>{stat.done} / {stat.total} ({pct}%)</span>
                  </div>
                  <div style={{ height: 4, background: 'var(--border)', borderRadius: 2, overflow: 'hidden' }}>
                    <div style={{
                      height: '100%',
                      width: `${pct}%`,
                      backgroundColor: colorVar
                    }} />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* 12-Week Activity Heatmap Panel */}
        <div className="panel" style={{ padding: '1rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.65rem' }}>
            <h3 style={{ fontSize: '0.9rem', fontWeight: 700 }}>Activity Heatmap</h3>
            <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Past 12 weeks</span>
          </div>
          <div style={{ display: 'grid', gridAutoFlow: 'column', gridTemplateRows: 'repeat(7, 11px)', gap: '3px', overflowX: 'auto', paddingBottom: '0.25rem' }}>
            {activityDays.map((day, idx) => {
              const count = day.count;
              let bg = 'var(--border)';
              if (count >= 4) bg = 'var(--accent)';
              else if (count === 3) bg = 'rgba(255, 161, 22, 0.75)';
              else if (count === 2) bg = 'rgba(255, 161, 22, 0.5)';
              else if (count === 1) bg = 'rgba(255, 161, 22, 0.25)';

              return (
                <div
                  key={idx}
                  title={`${day.date}: ${count} solved`}
                  style={{ width: 11, height: 11, borderRadius: 2, backgroundColor: bg }}
                />
              );
            })}
          </div>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: '0.35rem', marginTop: '0.5rem', fontSize: '0.7rem', color: 'var(--text-muted)' }}>
            <span>Less</span>
            <div style={{ width: 10, height: 10, borderRadius: 2, background: 'var(--border)' }} />
            <div style={{ width: 10, height: 10, borderRadius: 2, background: 'rgba(255, 161, 22, 0.25)' }} />
            <div style={{ width: 10, height: 10, borderRadius: 2, background: 'rgba(255, 161, 22, 0.5)' }} />
            <div style={{ width: 10, height: 10, borderRadius: 2, background: 'rgba(255, 161, 22, 0.75)' }} />
            <div style={{ width: 10, height: 10, borderRadius: 2, background: 'var(--accent)' }} />
            <span>More</span>
          </div>
        </div>
      </div>

      {/* 18 Chapters Quick Grid */}
      <div className="panel" style={{ padding: '1rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.85rem' }}>
          <div>
            <h3 style={{ fontSize: '0.95rem', fontWeight: 700 }}>18 Roadmap Chapters</h3>
            <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Sequential algorithmic progression</p>
          </div>
          <Link to="/roadmap" className="btn-secondary" style={{ fontSize: '0.78rem', padding: '0.3rem 0.65rem' }}>
            <span>Open Problem List</span>
            <ArrowRight size={12} />
          </Link>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
          gap: '0.65rem'
        }}>
          {chapters.map(ch => {
            const chQuestions = questions.filter(q => q.chapter === ch.id);
            const chDone = chQuestions.filter(q => progressMap[q.seq]?.status === 'done').length;
            const chPct = chQuestions.length ? Math.round((chDone / chQuestions.length) * 100) : 0;

            return (
              <Link
                to={`/roadmap#${ch.id}`}
                key={ch.id}
                style={{
                  display: 'block',
                  padding: '0.75rem',
                  background: 'var(--bg-input)',
                  border: '1px solid var(--border)',
                  borderRadius: 'var(--radius-sm)',
                  color: 'inherit',
                  textDecoration: 'none'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.25rem' }}>
                  <span style={{ fontWeight: 600, fontSize: '0.85rem' }}>{ch.order}. {ch.name}</span>
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>{ch.seqFrom} - {ch.seqTo}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.72rem', color: 'var(--text-muted)', marginBottom: '0.25rem' }}>
                  <span>{chDone} / {chQuestions.length} solved</span>
                  <span style={{ fontFamily: 'var(--font-mono)' }}>{chPct}%</span>
                </div>
                <div style={{ height: 3, background: 'var(--border)', borderRadius: 1.5, overflow: 'hidden' }}>
                  <div style={{ width: `${chPct}%`, height: '100%', background: 'var(--accent)' }} />
                </div>
              </Link>
            );
          })}
        </div>
      </div>
    </div>
  );
}

import React, { useMemo } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { 
  Target, 
  ClipboardCheck, 
  Flame, 
  ArrowRight, 
  ExternalLink,
  ChevronRight,
  BookOpen
} from 'lucide-react';

export default function Dashboard({ onOpenAuth }) {
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

  // Time-based greeting (Section 5.3)
  const greeting = useMemo(() => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 18) return 'Good afternoon';
    return 'Good evening';
  }, []);

  const displayName = user?.display_name || user?.username || 'learner';

  // Real Counts & Stats
  const totalQuestions = 300;
  const doneCount = useMemo(() => {
    return Object.values(progressMap).filter(p => p.status === 'done').length;
  }, [progressMap]);

  const diffCounts = useMemo(() => {
    const counts = {
      Easy: { done: 0, total: 0 },
      Medium: { done: 0, total: 0 },
      Hard: { done: 0, total: 0 }
    };
    questions.forEach(q => {
      if (counts[q.difficulty]) {
        counts[q.difficulty].total++;
        if (progressMap[q.seq]?.status === 'done') {
          counts[q.difficulty].done++;
        }
      }
    });
    return counts;
  }, [questions, progressMap]);

  // Builds on question for nextUp
  const nextUpBuildsOn = useMemo(() => {
    if (!nextUp || !nextUp.buildsOn) return null;
    return questions.find(q => q.seq === nextUp.buildsOn);
  }, [nextUp, questions]);

  // Desktop Progress Ring parameters (190px)
  const desktopRingSize = 190;
  const desktopStroke = 14;
  const desktopRadius = (desktopRingSize - desktopStroke) / 2;
  const desktopCircumference = 2 * Math.PI * desktopRadius;
  const progressRatio = Math.min(1, Math.max(0, doneCount / totalQuestions));
  const desktopDashoffset = desktopCircumference - (progressRatio * desktopCircumference);

  // Mobile Progress Ring parameters (160px per Part 2 #4)
  const mobileRingSize = 160;
  const mobileStroke = 12;
  const mobileRadius = (mobileRingSize - mobileStroke) / 2;
  const mobileCircumference = 2 * Math.PI * mobileRadius;
  const mobileDashoffset = mobileCircumference - (progressRatio * mobileCircumference);

  // 12 by 7 Activity Matrix (84 cells: 12 weeks = 84 days)
  const activityMatrix = useMemo(() => {
    const actMap = {};
    activity.forEach(a => {
      actMap[a.day] = a.solved_count;
    });

    const days = [];
    const today = new Date();
    // 83 days ago up to today = 84 days
    for (let i = 83; i >= 0; i--) {
      const d = new Date();
      d.setDate(today.getDate() - i);
      const dateStr = d.toISOString().split('T')[0];
      const count = actMap[dateStr] || 0;
      let level = 0;
      if (count >= 5) level = 4;
      else if (count >= 3) level = 3;
      else if (count === 2) level = 2;
      else if (count === 1) level = 1;

      days.push({
        date: dateStr,
        dayOfWeek: d.getDay(),
        count,
        level
      });
    }
    return days;
  }, [activity]);

  // Month labels for activity grid
  const monthLabels = useMemo(() => {
    const labels = [];
    const today = new Date();
    let lastMonth = '';
    for (let w = 0; w < 12; w++) {
      const d = new Date();
      d.setDate(today.getDate() - (11 - w) * 7);
      const mName = d.toLocaleString('default', { month: 'short' });
      if (mName !== lastMonth) {
        labels.push({ weekIndex: w, name: mName });
        lastMonth = mName;
      }
    }
    return labels;
  }, []);

  const dailyGoal = user?.daily_goal || 2;

  return (
    <div className="home-dashboard-root" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      
      {/* 1. GREETING (Order 1 on mobile, 28px on mobile) */}
      <div className="home-greeting-section" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 className="home-greeting-title">
            {greeting}, <span style={{ fontStyle: 'italic', fontWeight: 800 }}>{displayName}</span>
          </h1>
          <p style={{ fontSize: '0.95rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
            Chainline DSA roadmap · Solve 300 curated questions in order.
          </p>
        </div>

        {!user && (
          <button onClick={onOpenAuth} className="btn-primary desktop-only-btn">
            Sign In / Create Account
          </button>
        )}
      </div>

      {/* TOP GRID: Next Up + Overall Ring */}
      <div className="home-top-grid" style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1.8fr) minmax(0, 1fr)', gap: '24px' }}>
        
        {/* Next Up Card (Order 2 on mobile) */}
        {nextUp ? (
          <div className="glass-card home-next-up-card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between', gap: '1rem' }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.65rem' }}>
                <span style={{
                  fontFamily: 'var(--font-mono)',
                  fontSize: '0.75rem',
                  fontWeight: 700,
                  textTransform: 'uppercase',
                  letterSpacing: '0.08em',
                  color: 'var(--accent)',
                  background: 'var(--accent-soft)',
                  padding: '4px 12px',
                  borderRadius: 'var(--radius-pill)'
                }}>
                  Next Up
                </span>
                <span className={`diff-pill diff-pill-${nextUp.difficulty.toLowerCase()}`}>
                  {nextUp.difficulty}
                </span>
              </div>

              <h2 className="home-next-up-title" style={{ fontSize: 'clamp(1.25rem, 2.5vw, 1.6rem)', fontWeight: 700, letterSpacing: '-0.02em', marginBottom: '0.5rem', color: 'var(--text-color)' }}>
                #{nextUp.seq} {nextUp.title}
              </h2>

              {/* Builds on chip */}
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap', fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '0.75rem' }}>
                <span style={{ fontWeight: 600 }}>Builds on:</span>
                {nextUpBuildsOn ? (
                  <span style={{
                    padding: '3px 10px',
                    borderRadius: 'var(--radius-pill)',
                    background: 'var(--glass-surface)',
                    border: '1px solid var(--glass-border)',
                    fontFamily: 'var(--font-mono)',
                    fontSize: '0.8rem',
                    color: 'var(--text-color)'
                  }}>
                    #{nextUpBuildsOn.seq} {nextUpBuildsOn.title}
                  </span>
                ) : (
                  <span style={{ fontStyle: 'italic' }}>Chapter foundation</span>
                )}
                <span>·</span>
                <span>LC #{nextUp.lc}</span>
              </div>

              <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', lineHeight: 1.5, display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                {nextUp.optimal?.idea || nextUp.brute?.idea || 'Focus on the core pattern to optimize asymptotic time and space.'}
              </p>
            </div>

            {/* Buttons: Stacked full width on phones (Start on top, Open on LeetCode below) */}
            <div className="home-next-up-actions" style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap', marginTop: '0.5rem' }}>
              <button 
                onClick={() => navigate(`/question/${nextUp.seq}`)} 
                className="btn-primary home-btn-start"
              >
                <span>Start Problem</span>
                <ArrowRight size={16} />
              </button>

              <a
                href={`https://leetcode.com/problems/${nextUp.slug}/`}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-secondary home-btn-lc"
              >
                <span>Open on LeetCode</span>
                <ExternalLink size={14} />
              </a>
            </div>
          </div>
        ) : (
          <div className="glass-card empty-state-box home-next-up-card">
            <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-color)' }}>
              All 300 Questions Complete!
            </h3>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', maxWidth: '340px' }}>
              You have reached the end of the chain. Keep reviewing due items to lock in long-term mastery.
            </p>
            <Link to="/today" className="btn-primary" style={{ width: '100%', minHeight: '44px' }}>
              Review Due Questions
            </Link>
          </div>
        )}

        {/* Progress Ring Card (Order 3 on mobile: 160px ring centered) */}
        <div className="glass-card home-progress-ring-card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center', padding: '24px' }}>
          {/* Desktop Ring (190px) */}
          <div className="progress-ring-wrap desktop-ring" style={{ width: desktopRingSize, height: desktopRingSize }}>
            <svg width={desktopRingSize} height={desktopRingSize}>
              <circle
                cx={desktopRingSize / 2}
                cy={desktopRingSize / 2}
                r={desktopRadius}
                stroke="var(--progress-track)"
                strokeWidth={desktopStroke}
                fill="none"
              />
              <circle
                className="progress-ring-circle"
                cx={desktopRingSize / 2}
                cy={desktopRingSize / 2}
                r={desktopRadius}
                stroke="var(--accent)"
                strokeWidth={desktopStroke}
                strokeDasharray={desktopCircumference}
                strokeDashoffset={desktopDashoffset}
                strokeLinecap="round"
                fill="none"
              />
            </svg>

            <div style={{ position: 'absolute', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
              <span style={{ fontSize: '2.5rem', fontWeight: 800, lineHeight: 1, letterSpacing: '-0.03em', fontFamily: 'var(--font-sans)', fontVariantNumeric: 'tabular-nums' }}>
                {doneCount}
              </span>
              <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600, marginTop: '2px' }}>
                of 300 done
              </span>
            </div>
          </div>

          {/* Mobile Ring (160px centered per Part 2 #4) */}
          <div className="progress-ring-wrap mobile-ring" style={{ width: mobileRingSize, height: mobileRingSize, margin: '0 auto' }}>
            <svg width={mobileRingSize} height={mobileRingSize}>
              <circle
                cx={mobileRingSize / 2}
                cy={mobileRingSize / 2}
                r={mobileRadius}
                stroke="var(--progress-track)"
                strokeWidth={mobileStroke}
                fill="none"
              />
              <circle
                className="progress-ring-circle"
                cx={mobileRingSize / 2}
                cy={mobileRingSize / 2}
                r={mobileRadius}
                stroke="var(--accent)"
                strokeWidth={mobileStroke}
                strokeDasharray={mobileCircumference}
                strokeDashoffset={mobileDashoffset}
                strokeLinecap="round"
                fill="none"
              />
            </svg>

            <div style={{ position: 'absolute', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
              <span style={{ fontSize: '2.1rem', fontWeight: 800, lineHeight: 1, letterSpacing: '-0.03em', fontFamily: 'var(--font-sans)', fontVariantNumeric: 'tabular-nums' }}>
                {doneCount}
              </span>
              <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600, marginTop: '2px' }}>
                of 300 done
              </span>
            </div>
          </div>

          {/* Difficulty Breakdown (Below the ring) */}
          <div style={{ display: 'flex', gap: '0.65rem', justifyContent: 'center', marginTop: '16px', width: '100%' }}>
            <div style={{ textAlign: 'center', flex: 1 }}>
              <div style={{ fontSize: '0.72rem', fontWeight: 700, color: 'var(--easy-pill-text)' }}>Easy</div>
              <div style={{ fontSize: '0.9rem', fontWeight: 700, fontFamily: 'var(--font-mono)' }}>
                {diffCounts.Easy.done}/{diffCounts.Easy.total}
              </div>
            </div>
            <div style={{ textAlign: 'center', flex: 1, borderLeft: '1px solid var(--glass-border)', borderRight: '1px solid var(--glass-border)' }}>
              <div style={{ fontSize: '0.72rem', fontWeight: 700, color: 'var(--medium-pill-text)' }}>Med</div>
              <div style={{ fontSize: '0.9rem', fontWeight: 700, fontFamily: 'var(--font-mono)' }}>
                {diffCounts.Medium.done}/{diffCounts.Medium.total}
              </div>
            </div>
            <div style={{ textAlign: 'center', flex: 1 }}>
              <div style={{ fontSize: '0.72rem', fontWeight: 700, color: 'var(--hard-pill-text)' }}>Hard</div>
              <div style={{ fontSize: '0.9rem', fontWeight: 700, fontFamily: 'var(--font-mono)' }}>
                {diffCounts.Hard.done}/{diffCounts.Hard.total}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 3 STAT CARDS (Order 4 on mobile: 3 cards in one row, each about a third width, number on top and label under it) */}
      <div className="home-stats-row" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px' }}>
        
        {/* Stat 1: Today's Goal */}
        <div className="glass-card home-stat-card" style={{ padding: '20px' }}>
          <div className="home-stat-header" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
            <span className="home-stat-label" style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)' }}>Today's Goal</span>
            <Target size={20} color="var(--accent)" className="home-stat-icon" />
          </div>
          <div className="home-stat-number" style={{ fontSize: '2rem', fontWeight: 800, fontFamily: 'var(--font-sans)', fontVariantNumeric: 'tabular-nums', color: 'var(--text-color)' }}>
            {todaySolvedCount} <span style={{ fontSize: '1rem', fontWeight: 500, color: 'var(--text-muted)' }}>/ {dailyGoal}</span>
          </div>
          <span className="home-stat-mobile-label">Today's Goal</span>
          <div className="progress-bar-container home-stat-bar" style={{ marginTop: '10px' }}>
            <div 
              className="progress-bar-fill" 
              style={{ width: `${Math.min(100, Math.round((todaySolvedCount / dailyGoal) * 100))}%` }} 
            />
          </div>
        </div>

        {/* Stat 2: Due Reviews */}
        <Link to="/today" className="glass-card glass-card-interactive home-stat-card" style={{ padding: '20px', display: 'block' }}>
          <div className="home-stat-header" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
            <span className="home-stat-label" style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)' }}>Due Reviews</span>
            <ClipboardCheck size={20} color="var(--revisit-color)" className="home-stat-icon" />
          </div>
          <div className="home-stat-number" style={{ fontSize: '2rem', fontWeight: 800, fontFamily: 'var(--font-sans)', fontVariantNumeric: 'tabular-nums', color: dueReviews.length > 0 ? 'var(--revisit-color)' : 'var(--text-color)' }}>
            {dueReviews.length} <span style={{ fontSize: '1rem', fontWeight: 500, color: 'var(--text-muted)' }}>pending</span>
          </div>
          <span className="home-stat-mobile-label">Due Reviews</span>
          <div className="home-stat-link" style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '8px', display: 'flex', alignItems: 'center', gap: '4px' }}>
            <span>Open Queue</span>
            <ArrowRight size={12} />
          </div>
        </Link>

        {/* Stat 3: Daily Streak */}
        <div className="glass-card home-stat-card" style={{ padding: '20px' }}>
          <div className="home-stat-header" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
            <span className="home-stat-label" style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)' }}>Daily Streak</span>
            <Flame size={20} color="var(--revisit-color)" className="home-stat-icon" />
          </div>
          <div className="home-stat-number" style={{ fontSize: '2rem', fontWeight: 800, fontFamily: 'var(--font-sans)', fontVariantNumeric: 'tabular-nums', color: 'var(--revisit-color)' }}>
            {streak} <span style={{ fontSize: '1rem', fontWeight: 500, color: 'var(--text-muted)' }}>{streak === 1 ? 'day' : 'days'}</span>
          </div>
          <span className="home-stat-mobile-label">Daily Streak</span>
          <div className="home-stat-subtitle" style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '8px' }}>
            {todaySolvedCount > 0 ? "Solved today!" : "Maintain streak"}
          </div>
        </div>
      </div>

      {/* BOTTOM GRID: Chapter Progression + Activity Grid */}
      <div className="home-bottom-grid" style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1.4fr) minmax(0, 1fr)', gap: '24px' }}>
        
        {/* Chapter Progress Card (Order 5 on mobile: 1 column of 18 rows, each 48px) */}
        <div className="glass-card home-chapters-card" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
            <div>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-color)' }}>
                18 Chapters Progression
              </h3>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                Calculated directly from questions data
              </p>
            </div>
            <Link to="/roadmap" className="btn-secondary" style={{ padding: '6px 14px', fontSize: '0.8rem', minHeight: '44px' }}>
              Full Roadmap
            </Link>
          </div>

          <div className="chapters-two-columns" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px 20px' }}>
            {chapters.map(ch => {
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

        {/* Activity Card: 12 cols by 7 rows = 84 cells (Order 6 on mobile) */}
        <div className="glass-card home-activity-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-color)' }}>
                Activity (Past 12 Weeks)
              </h3>
              <span style={{ fontSize: '0.78rem', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>
                84 days
              </span>
            </div>

            {/* Month labels header */}
            <div className="activity-month-labels" style={{ display: 'flex', justifyContent: 'space-between', paddingLeft: '28px', fontSize: '0.72rem', color: 'var(--text-muted)', marginBottom: '6px' }}>
              {monthLabels.map((m, idx) => (
                <span key={idx}>{m.name}</span>
              ))}
            </div>

            {/* Grid Container with Weekday Labels */}
            <div className="activity-grid-wrapper" style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
              {/* Weekday indicators */}
              <div className="activity-weekday-labels" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between', fontSize: '0.68rem', color: 'var(--text-muted)', height: '115px', padding: '2px 0' }}>
                <span>Sun</span>
                <span>Tue</span>
                <span>Thu</span>
                <span>Sat</span>
              </div>

              {/* 84 cells grid */}
              <div className="activity-matrix">
                {activityMatrix.map((item, idx) => {
                  const levelVar = `var(--activity-${item.level})`;
                  return (
                    <div
                      key={idx}
                      className="activity-cell"
                      style={{ background: levelVar }}
                      title={`${item.date}: ${item.count} question${item.count === 1 ? '' : 's'} solved`}
                    />
                  );
                })}
              </div>
            </div>
          </div>

          {/* Legend: Less to More with 5-level scale */}
          <div className="activity-legend" style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: '6px', fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '16px' }}>
            <span>Less</span>
            {[0, 1, 2, 3, 4].map(lvl => (
              <div 
                key={lvl} 
                style={{ 
                  width: 12, 
                  height: 12, 
                  borderRadius: 3, 
                  background: `var(--activity-${lvl})`,
                  border: '1px solid var(--glass-border)'
                }} 
              />
            ))}
            <span>More</span>
          </div>
        </div>

      </div>

    </div>
  );
}

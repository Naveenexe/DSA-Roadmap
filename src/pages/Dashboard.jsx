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
import ActivityCard from '../components/ActivityCard';
import NeedsAttentionCard from '../components/NeedsAttentionCard';
import ChaptersProgressionCard from '../components/ChaptersProgressionCard';
import InterviewHomeCard from '../components/InterviewHomeCard';

export default function Dashboard({ onOpenAuth }) {
  const { 
    user, 
    questions, 
    chapters, 
    progressMap, 
    streak, 
    todaySolvedCount, 
    getNextUp, 
    dueReviews 
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

  // Dynamic count from questions data (never hardcoded 300)
  const totalQuestions = questions.length || 500;
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
  const progressRatio = totalQuestions > 0 ? Math.min(1, Math.max(0, doneCount / totalQuestions)) : 0;
  const desktopDashoffset = desktopCircumference - (progressRatio * desktopCircumference);

  // Mobile Progress Ring parameters (160px)
  const mobileRingSize = 160;
  const mobileStroke = 12;
  const mobileRadius = (mobileRingSize - mobileStroke) / 2;
  const mobileCircumference = 2 * Math.PI * mobileRadius;
  const mobileDashoffset = mobileCircumference - (progressRatio * mobileCircumference);

  const dailyGoal = user?.daily_goal || 2;

  return (
    <div className="home-dashboard-root" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      
      {/* 1. GREETING (Order 1 on mobile) */}
      <div className="home-greeting-section" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 className="home-greeting-title">
            {greeting}, <span style={{ fontStyle: 'italic', fontWeight: 800 }}>{displayName}</span>
          </h1>
          <p style={{ fontSize: '0.95rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
            Chainline DSA roadmap · Solve {totalQuestions} curated questions in order.
          </p>
        </div>

        {!user && (
          <button onClick={onOpenAuth} className="btn-primary desktop-only-btn">
            Sign In / Create Account
          </button>
        )}
      </div>

      {/* TOP GRID: Next Up + Overall Ring + Interview Plan / Company Prep */}
      <div className="home-top-grid">
        
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

            {/* Buttons: Stacked full width on phones */}
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
              All {totalQuestions} Questions Complete!
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
                of {totalQuestions} done
              </span>
            </div>
          </div>

          {/* Mobile Ring (160px centered) */}
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
                of {totalQuestions} done
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

        {/* Desktop-only Interview / Company Prep Card in Top Row (Right of ring) */}
        <div className="home-top-interview-card-wrap">
          <InterviewHomeCard />
        </div>
      </div>

      {/* 3 STAT CARDS (Order 4 on mobile) */}
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
        <Link to="/today" className="glass-card glass-card-interactive home-stat-card" style={{ padding: '20px', display: 'block', textDecoration: 'none' }}>
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

      {/* Mobile/Tablet Interview Plan / Company Prep Card (Order 5 on phone) */}
      <div className="home-mid-interview-card-wrap">
        <InterviewHomeCard />
      </div>

      {/* LOWER HOME (Desktop: 7fr / 5fr, ending on same baseline. Phone: Order 6, 7, 8) */}
      <div className="home-bottom-grid">
        
        {/* Left: Chapters Card with Part 1 & Part 2 tabs (Order 6 on phone) */}
        <div className="home-bottom-left-column">
          <ChaptersProgressionCard />
        </div>

        {/* Right: Stacked Activity Card & Needs Attention Card (Order 7 & 8 on phone) */}
        <div className="home-bottom-right-column">
          <ActivityCard />
          <NeedsAttentionCard />
        </div>

      </div>

    </div>
  );
}
import React, { useMemo } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { Calendar, Briefcase, ArrowRight, CheckCircle2, ChevronRight, Sparkles } from 'lucide-react';

export default function InterviewHomeCard() {
  const { interviewPlan, questions, progressMap, companies, clearInterviewPlan } = useApp();
  const navigate = useNavigate();

  // Plan data calculations
  const planInfo = useMemo(() => {
    if (!interviewPlan?.date) return null;

    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const targetDate = new Date(interviewPlan.date + 'T00:00:00');
    targetDate.setHours(0, 0, 0, 0);

    const diffTime = targetDate.getTime() - today.getTime();
    const daysLeft = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1; // counting today

    const isPast = daysLeft <= 0;

    // Question pool
    let pool = questions.filter(q => progressMap[q.seq]?.status !== 'done');
    let scopeQuestions = questions;

    if (interviewPlan.company) {
      scopeQuestions = questions.filter(q => q.companies && q.companies.includes(interviewPlan.company));
      pool = pool.filter(q => q.companies && q.companies.includes(interviewPlan.company));
    }

    const totalScope = scopeQuestions.length;
    const doneScope = scopeQuestions.filter(q => progressMap[q.seq]?.status === 'done').length;
    const readinessRatio = totalScope > 0 ? (doneScope / totalScope) : 0;

    // Daily target: pool size / daysLeft, rounded up, clamped 1..10
    const rawTarget = daysLeft > 0 ? Math.ceil(pool.length / Math.max(1, daysLeft)) : 0;
    const dailyTarget = Math.min(10, Math.max(1, rawTarget));
    const isOverloaded = rawTarget > 10;

    const todayTargetList = pool.slice(0, Math.min(5, dailyTarget));

    return {
      daysLeft,
      isPast,
      isComplete: pool.length === 0,
      totalScope,
      doneScope,
      readinessRatio,
      dailyTarget,
      isOverloaded,
      todayTargetList,
      company: interviewPlan.company
    };
  }, [interviewPlan, questions, progressMap]);

  // Mini progress ring parameters
  const ringSize = 72;
  const stroke = 6;
  const radius = (ringSize - stroke) / 2;
  const circumference = 2 * Math.PI * radius;

  // Render Interview Plan card if date is set
  if (planInfo) {
    const dashoffset = circumference - (planInfo.readinessRatio * circumference);

    return (
      <div 
        className="glass-card home-interview-plan-card" 
        style={{ 
          padding: '24px', 
          display: 'flex', 
          flexDirection: 'column', 
          gap: '14px', 
          width: '100%', 
          boxSizing: 'border-box' 
        }}
      >
        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '8px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Calendar size={18} color="var(--accent)" />
            <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--text-color)', margin: 0 }}>
              Interview Plan
            </h3>
          </div>
          {planInfo.company && (
            <span style={{
              fontSize: '0.75rem',
              fontWeight: 700,
              padding: '2px 8px',
              borderRadius: 'var(--radius-pill)',
              background: 'var(--accent-soft)',
              color: 'var(--accent)'
            }}>
              {companies.find(c => c.slug === planInfo.company)?.name || planInfo.company}
            </span>
          )}
        </div>

        {planInfo.isPast ? (
          <div style={{ textAlign: 'center', padding: '12px 0' }}>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginBottom: '12px' }}>
              Your interview date has passed.
            </p>
            <button 
              onClick={clearInterviewPlan}
              className="btn-secondary"
              style={{ fontSize: '0.8rem', padding: '6px 14px', minHeight: '38px' }}
            >
              Clear plan
            </button>
          </div>
        ) : planInfo.isComplete ? (
          <div style={{ textAlign: 'center', padding: '12px 0' }}>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-color)', fontWeight: 600, marginBottom: '12px' }}>
              🎉 You have covered everything in your plan!
            </p>
            <button 
              onClick={clearInterviewPlan}
              className="btn-secondary"
              style={{ fontSize: '0.8rem', padding: '6px 14px', minHeight: '38px' }}
            >
              Clear plan
            </button>
          </div>
        ) : (
          <>
            {/* Top row: Days left and mini readiness ring */}
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '16px' }}>
              <div>
                <div style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--text-color)', fontFamily: 'var(--font-sans)', lineHeight: 1 }}>
                  {planInfo.daysLeft} <span style={{ fontSize: '0.95rem', fontWeight: 500, color: 'var(--text-muted)' }}>{planInfo.daysLeft === 1 ? 'day left' : 'days left'}</span>
                </div>
                <div style={{ fontSize: '0.825rem', color: 'var(--accent)', fontWeight: 600, marginTop: '4px' }}>
                  Target: {planInfo.dailyTarget} / day
                </div>
              </div>

              {/* Readiness mini ring */}
              <div style={{ position: 'relative', width: ringSize, height: ringSize, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <svg width={ringSize} height={ringSize}>
                  <circle
                    cx={ringSize / 2}
                    cy={ringSize / 2}
                    r={radius}
                    stroke="var(--progress-track)"
                    strokeWidth={stroke}
                    fill="none"
                  />
                  <circle
                    cx={ringSize / 2}
                    cy={ringSize / 2}
                    r={radius}
                    stroke="var(--accent)"
                    strokeWidth={stroke}
                    strokeDasharray={circumference}
                    strokeDashoffset={dashoffset}
                    strokeLinecap="round"
                    fill="none"
                    style={{ transform: 'rotate(-90deg)', transformOrigin: '50% 50%' }}
                  />
                </svg>
                <div style={{ position: 'absolute', fontSize: '0.8rem', fontWeight: 800, fontFamily: 'var(--font-mono)' }}>
                  {Math.round(planInfo.readinessRatio * 100)}%
                </div>
              </div>
            </div>

            {planInfo.isOverloaded && (
              <p style={{ fontSize: '0.78rem', color: 'var(--revisit-color)', margin: 0 }}>
                There are not enough days to cover everything. Showing 10 a day.
              </p>
            )}

            {/* Target Questions for today */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginTop: '4px' }}>
              <div style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Today's Target ({planInfo.todayTargetList.length})
              </div>
              {planInfo.todayTargetList.map(q => (
                <div 
                  key={q.seq} 
                  style={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'space-between',
                    gap: '8px',
                    padding: '8px 12px',
                    borderRadius: 'var(--radius-inner)',
                    background: 'var(--glass-surface)',
                    border: '1px solid var(--glass-border)',
                    fontSize: '0.825rem'
                  }}
                >
                  <div style={{ minWidth: 0, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', fontWeight: 600 }}>
                    #{q.seq} {q.title}
                  </div>
                  <button 
                    onClick={() => navigate(`/question/${q.seq}`)} 
                    className="btn-primary" 
                    style={{ padding: '4px 10px', fontSize: '0.75rem', minHeight: '32px' }}
                  >
                    Start
                  </button>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    );
  }

  // Fallback: Company Prep Card (Section 5 & 8.3)
  return (
    <div 
      className="glass-card home-interview-plan-card" 
      style={{ 
        padding: '24px', 
        display: 'flex', 
        flexDirection: 'column', 
        justifyContent: 'space-between', 
        gap: '14px', 
        width: '100%', 
        boxSizing: 'border-box' 
      }}
    >
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
          <Briefcase size={18} color="var(--accent)" />
          <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--text-color)', margin: 0 }}>
            Company Preparation
          </h3>
        </div>
        <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', lineHeight: 1.4, margin: '0 0 12px 0' }}>
          Targeted problem sets for 30 top tech companies (Google, Meta, Amazon, Microsoft, and more).
        </p>

        {/* Mini quick badges */}
        <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap', marginBottom: '8px' }}>
          {['Google', 'Amazon', 'Meta', 'Microsoft', 'Apple'].map(name => (
            <span 
              key={name} 
              style={{ 
                fontSize: '0.75rem', 
                padding: '3px 9px', 
                borderRadius: 'var(--radius-pill)', 
                background: 'var(--glass-surface)', 
                border: '1px solid var(--glass-border)',
                color: 'var(--text-color)',
                fontWeight: 600
              }}
            >
              {name}
            </span>
          ))}
        </div>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        <Link 
          to="/companies" 
          className="btn-primary" 
          style={{ width: '100%', minHeight: '40px', justifyContent: 'center', fontSize: '0.85rem', textDecoration: 'none' }}
        >
          <span>Explore Companies</span>
          <ArrowRight size={14} />
        </Link>
        <Link 
          to="/settings" 
          style={{ 
            fontSize: '0.78rem', 
            color: 'var(--accent)', 
            textAlign: 'center', 
            fontWeight: 600, 
            textDecoration: 'none',
            padding: '4px' 
          }}
        >
          Set an interview date →
        </Link>
      </div>
    </div>
  );
}
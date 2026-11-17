import React, { useMemo } from 'react';
import { Link } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { 
  BarChart2, 
  Clock, 
  Flame, 
  Target, 
  ArrowLeft, 
  AlertCircle,
  Calendar,
  Layers,
  ChevronRight
} from 'lucide-react';

export default function Stats() {
  const { questions, chapters, progressMap, statsMap, activity, streak } = useApp();

  // 1. Average time per difficulty (Easy, Medium, Hard)
  const avgTimePerDiff = useMemo(() => {
    const data = {
      Easy: { totalSeconds: 0, count: 0 },
      Medium: { totalSeconds: 0, count: 0 },
      Hard: { totalSeconds: 0, count: 0 }
    };

    questions.forEach(q => {
      const s = statsMap[q.seq];
      if (s && s.seconds > 0 && data[q.difficulty]) {
        data[q.difficulty].totalSeconds += s.seconds;
        data[q.difficulty].count++;
      }
    });

    const result = {};
    let maxAvg = 1;
    ['Easy', 'Medium', 'Hard'].forEach(diff => {
      const avg = data[diff].count > 0 ? Math.round(data[diff].totalSeconds / data[diff].count) : 0;
      if (avg > maxAvg) maxAvg = avg;
      result[diff] = {
        avgSeconds: avg,
        count: data[diff].count,
        formatted: avg > 0 ? `${Math.floor(avg / 60)}m ${avg % 60}s` : '—'
      };
    });

    return { result, maxAvg, hasData: Object.values(data).some(d => d.count > 0) };
  }, [questions, statsMap]);

  // 2. Questions solved per week for the last 12 weeks
  const weeklySolved = useMemo(() => {
    const actMap = {};
    if (Array.isArray(activity)) {
      activity.forEach(a => {
        if (a.day) actMap[a.day] = a.solved_count || 0;
      });
    }

    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const mDay = (today.getDay() + 6) % 7; // Monday = 0
    const currWeekMon = new Date(today);
    currWeekMon.setDate(today.getDate() - mDay);

    const weeks = [];
    let maxWeekCount = 1;
    let total12Weeks = 0;

    for (let w = 11; w >= 0; w--) {
      const weekMon = new Date(currWeekMon);
      weekMon.setDate(currWeekMon.getDate() - w * 7);

      let weekSum = 0;
      for (let d = 0; d < 7; d++) {
        const cellD = new Date(weekMon);
        cellD.setDate(weekMon.getDate() + d);
        const dStr = cellD.toISOString().split('T')[0];
        if (dStr <= today.toISOString().split('T')[0]) {
          weekSum += actMap[dStr] || 0;
        }
      }

      total12Weeks += weekSum;
      if (weekSum > maxWeekCount) maxWeekCount = weekSum;

      const label = `${weekMon.getDate()} ${weekMon.toLocaleString('default', { month: 'short' })}`;
      weeks.push({ weekMon, label, count: weekSum });
    }

    return { weeks, maxWeekCount, total12Weeks, hasData: total12Weeks > 0 };
  }, [activity]);

  // 3. Chapters ranked by score (Weak topics)
  const rankedChapters = useMemo(() => {
    if (!chapters || chapters.length === 0) return [];
    const scored = [];

    chapters.forEach(ch => {
      const chQuestions = questions.filter(q => q.chapter === ch.id);
      const solvedList = chQuestions.filter(q => progressMap[q.seq]?.status === 'done');
      const solvedCount = solvedList.length;

      if (solvedCount >= 3) {
        let mistakeCount = 0;
        let forgotCount = 0;
        let slowCount = 0;

        chQuestions.forEach(q => {
          if (progressMap[q.seq]?.mistake) mistakeCount++;
          if (statsMap[q.seq]?.forgotCount) forgotCount += statsMap[q.seq].forgotCount;
          if (statsMap[q.seq]?.slow) slowCount++;
        });

        const score = ((2 * mistakeCount) + (2 * forgotCount) + (1 * slowCount)) / solvedCount;
        scored.push({
          id: ch.id,
          order: ch.order,
          name: ch.name,
          score: Number(score.toFixed(2)),
          mistakeCount,
          forgotCount,
          slowCount,
          solvedCount
        });
      }
    });

    scored.sort((a, b) => b.score - a.score);
    return scored;
  }, [chapters, questions, progressMap, statsMap]);

  // 4. Total time spent & total attempts
  const { totalTimeFormatted, totalAttempts, totalTimedQuestions } = useMemo(() => {
    let secs = 0;
    let attempts = 0;
    let timed = 0;

    Object.values(statsMap).forEach(s => {
      if (s) {
        secs += s.seconds || 0;
        attempts += s.attempts || 0;
        if (s.seconds > 0) timed++;
      }
    });

    const hours = Math.floor(secs / 3600);
    const mins = Math.floor((secs % 3600) / 60);
    const formatted = hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;

    return {
      totalTimeFormatted: formatted,
      totalAttempts: attempts,
      totalTimedQuestions: timed
    };
  }, [statsMap]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', width: '100%', maxWidth: '100%' }}>
      {/* Top back link */}
      <div>
        <Link 
          to="/" 
          style={{ 
            display: 'inline-flex', 
            alignItems: 'center', 
            gap: '6px', 
            color: 'var(--accent)', 
            fontWeight: 600, 
            fontSize: '0.85rem', 
            textDecoration: 'none' 
          }}
        >
          <ArrowLeft size={16} />
          <span>Home</span>
        </Link>
      </div>

      {/* Header */}
      <div className="glass-card" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '6px' }}>
          <BarChart2 size={24} color="var(--accent)" />
          <h1 style={{ fontSize: 'clamp(1.5rem, 3.5vw, 2rem)', fontWeight: 800, color: 'var(--text-color)', margin: 0 }}>
            Performance & Insights
          </h1>
        </div>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', margin: 0 }}>
          Detailed analytics on solve speed, practice consistency, and chapter accuracy.
        </p>
      </div>

      {/* Top Summary Row (2 columns: Total Time Spent & Streak/Consistency) */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
        {/* Total Time Card */}
        <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)' }}>Total Practice Time</span>
            <Clock size={20} color="var(--accent)" />
          </div>
          <div style={{ fontSize: '2.5rem', fontWeight: 800, fontFamily: 'var(--font-sans)', color: 'var(--text-color)', lineHeight: 1 }}>
            {totalTimeFormatted}
          </div>
          <div style={{ fontSize: '0.825rem', color: 'var(--text-muted)' }}>
            Across {totalTimedQuestions} timed problems ({totalAttempts} solve attempts)
          </div>
        </div>

        {/* Consistency Card */}
        <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)' }}>Streak & Regularity</span>
            <Flame size={20} color="var(--revisit-color)" />
          </div>
          <div style={{ fontSize: '2.5rem', fontWeight: 800, fontFamily: 'var(--font-sans)', color: 'var(--revisit-color)', lineHeight: 1 }}>
            {streak} <span style={{ fontSize: '1.25rem', fontWeight: 600, color: 'var(--text-muted)' }}>{streak === 1 ? 'day' : 'days'}</span>
          </div>
          <div style={{ fontSize: '0.825rem', color: 'var(--text-muted)' }}>
            {weeklySolved.total12Weeks} questions solved in the last 12 weeks
          </div>
        </div>
      </div>

      {/* Two-column layout for Difficulty Times & Weekly Bar Chart */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px' }}>
        
        {/* Average Time per Difficulty */}
        <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-color)', margin: '0 0 4px 0' }}>
              Average Time per Difficulty
            </h3>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', margin: 0 }}>
              Calculated from solve timer sessions
            </p>
          </div>

          {avgTimePerDiff.hasData ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', marginTop: '8px' }}>
              {['Easy', 'Medium', 'Hard'].map(diff => {
                const item = avgTimePerDiff.result[diff];
                const ratio = avgTimePerDiff.maxAvg > 0 ? (item.avgSeconds / avgTimePerDiff.maxAvg) : 0;
                const pillClass = `diff-pill diff-pill-${diff.toLowerCase()}`;

                return (
                  <div key={diff} style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.85rem' }}>
                      <span className={pillClass}>{diff}</span>
                      <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 700, color: 'var(--text-color)' }}>
                        {item.formatted} {item.count > 0 && <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 500 }}>({item.count} solved)</span>}
                      </span>
                    </div>
                    <div className="progress-bar-container" style={{ height: '8px' }}>
                      <div 
                        className="progress-bar-fill" 
                        style={{ 
                          width: `${Math.round(ratio * 100)}%`,
                          background: diff === 'Easy' ? 'var(--easy-pill-text)' : diff === 'Medium' ? 'var(--medium-pill-text)' : 'var(--hard-pill-text)'
                        }} 
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div style={{ padding: '24px 0', textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
              Start the solve timer on any question to track your speed.
            </div>
          )}
        </div>

        {/* 12-Week Solved Bars */}
        <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-color)', margin: '0 0 4px 0' }}>
              Questions Solved per Week
            </h3>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', margin: 0 }}>
              Last 12 weeks of activity
            </p>
          </div>

          {weeklySolved.hasData ? (
            <div style={{ display: 'flex', alignItems: 'flex-end', gap: '8px', height: '160px', paddingTop: '20px', width: '100%' }}>
              {weeklySolved.weeks.map((wk, idx) => {
                const barHeight = weeklySolved.maxWeekCount > 0 
                  ? Math.max(6, Math.round((wk.count / weeklySolved.maxWeekCount) * 120))
                  : 6;

                return (
                  <div 
                    key={idx} 
                    style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '6px' }}
                    title={`${wk.label}: ${wk.count} solved`}
                  >
                    <span style={{ fontSize: '0.7rem', fontFamily: 'var(--font-mono)', fontWeight: 700, color: wk.count > 0 ? 'var(--accent)' : 'transparent' }}>
                      {wk.count}
                    </span>
                    <div 
                      style={{ 
                        width: '100%', 
                        maxWidth: '22px', 
                        height: `${barHeight}px`, 
                        borderRadius: '4px', 
                        background: wk.count > 0 ? 'var(--accent)' : 'var(--glass-surface)',
                        border: '1px solid var(--glass-border)'
                      }} 
                    />
                    <span style={{ fontSize: '0.65rem', color: 'var(--text-muted)', transform: 'rotate(-45deg)', transformOrigin: 'top left', whiteSpace: 'nowrap', marginTop: '6px', height: '24px' }}>
                      {idx % 2 === 0 ? wk.label : ''}
                    </span>
                  </div>
                );
              })}
            </div>
          ) : (
            <div style={{ padding: '24px 0', textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
              Solve a question to start your 12-week activity chart.
            </div>
          )}
        </div>

      </div>

      {/* Chapters Ranked by Score (Accuracy / Weak Topics) */}
      <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <div>
          <h3 style={{ fontSize: '1.15rem', fontWeight: 700, color: 'var(--text-color)', margin: '0 0 4px 0' }}>
            Chapters Accuracy Ranking
          </h3>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', margin: 0 }}>
            Ranked by weak-spots formula: (2 × mistakes + 2 × forgot + 1 × slow) / solved questions (minimum 3 solved per chapter)
          </p>
        </div>

        {rankedChapters.length > 0 ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {rankedChapters.map((ch, idx) => (
              <div 
                key={ch.id}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '12px 16px',
                  borderRadius: 'var(--radius-inner)',
                  background: 'var(--glass-surface)',
                  border: '1px solid var(--glass-border)',
                  flexWrap: 'wrap',
                  gap: '12px'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px', minWidth: '220px' }}>
                  <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 800, fontSize: '0.9rem', color: idx < 3 && ch.score > 0 ? 'var(--accent)' : 'var(--text-muted)', width: '24px' }}>
                    #{idx + 1}
                  </span>
                  <div>
                    <div style={{ fontWeight: 700, fontSize: '0.9rem', color: 'var(--text-color)' }}>
                      {ch.order}. {ch.name}
                    </div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                      {ch.solvedCount} questions solved
                    </div>
                  </div>
                </div>

                {/* Score and chips */}
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
                  <div style={{ display: 'flex', gap: '6px' }}>
                    {ch.mistakeCount > 0 && (
                      <span style={{ fontSize: '0.72rem', padding: '2px 8px', borderRadius: 'var(--radius-pill)', background: 'rgba(239, 68, 68, 0.12)', color: '#ef4444', fontWeight: 600 }}>
                        {ch.mistakeCount} mistakes
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

                  <div style={{ textAlign: 'right', minWidth: '70px' }}>
                    <div style={{ fontSize: '1rem', fontWeight: 800, fontFamily: 'var(--font-mono)', color: ch.score > 0 ? (ch.score > 1 ? '#ef4444' : 'var(--accent)') : 'var(--text-muted)' }}>
                      {ch.score}
                    </div>
                    <div style={{ fontSize: '0.68rem', color: 'var(--text-muted)' }}>score</div>
                  </div>

                  <Link 
                    to={`/roadmap#${ch.id}`}
                    className="btn-secondary"
                    style={{ padding: '6px 12px', fontSize: '0.8rem', minHeight: '36px' }}
                  >
                    Open
                  </Link>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div style={{ padding: '24px 0', textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
            Solve at least 3 questions in a chapter to generate accuracy rankings.
          </div>
        )}
      </div>

    </div>
  );
}
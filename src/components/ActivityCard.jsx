import React, { useMemo, useState } from 'react';
import { useApp } from '../context/AppContext';

export default function ActivityCard() {
  const { activity } = useApp();
  const [activeTooltip, setActiveTooltip] = useState(null);

  // Compute the 84-day window (12 weeks × 7 days, Monday start)
  // Last column (col 11) is the current week, col 0 is 11 weeks ago
  const { grid, monthLabels, stats, solvedIn12Weeks } = useMemo(() => {
    const actMap = {};
    if (Array.isArray(activity)) {
      activity.forEach(a => {
        if (a.day) actMap[a.day] = a.solved_count || 0;
      });
    }

    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const todayStr = today.toISOString().split('T')[0];

    // Day of week with Monday = 0, ..., Sunday = 6
    const mDay = (today.getDay() + 6) % 7;

    // Current week's Monday
    const currWeekMon = new Date(today);
    currWeekMon.setDate(today.getDate() - mDay);

    // Monday of 11 weeks earlier (start of grid)
    const startDate = new Date(currWeekMon);
    startDate.setDate(currWeekMon.getDate() - 11 * 7);

    let totalSolved = 0;
    let activeDaysCount = 0;
    let maxSolvedInDay = 0;
    let bestDayDateStr = '';
    const dayRecords = [];

    // Columns: 0 to 11 (weeks); Rows: 0 to 6 (Mon to Sun)
    const columns = [];
    for (let c = 0; c < 12; c++) {
      const colDays = [];
      for (let r = 0; r < 7; r++) {
        const d = new Date(startDate);
        d.setDate(startDate.getDate() + c * 7 + r);
        const dStr = d.toISOString().split('T')[0];
        const isToday = dStr === todayStr;
        const isFuture = dStr > todayStr;
        const count = isFuture ? 0 : (actMap[dStr] || 0);

        if (!isFuture) {
          totalSolved += count;
          if (count > 0) {
            activeDaysCount++;
            if (count > maxSolvedInDay) {
              maxSolvedInDay = count;
              bestDayDateStr = dStr;
            }
          }
          dayRecords.push({ date: dStr, count });
        }

        let level = 0;
        if (!isFuture) {
          if (count >= 5) level = 4;
          else if (count >= 3) level = 3;
          else if (count === 2) level = 2;
          else if (count === 1) level = 1;
        }

        colDays.push({
          date: dStr,
          dayOfWeek: r,
          weekIndex: c,
          count,
          level,
          isToday,
          isFuture
        });
      }
      columns.push(colDays);
    }

    // Calculate longest streak in 84-day window
    let longestStreak = 0;
    let currentRun = 0;
    dayRecords.forEach(rec => {
      if (rec.count > 0) {
        currentRun++;
        if (currentRun > longestStreak) longestStreak = currentRun;
      } else {
        currentRun = 0;
      }
    });

    // Month labels: sit above the first column of each month by grid column
    // Skip if closer than 3 columns to previous
    const mLabels = [];
    let lastLabelCol = -4;
    for (let c = 0; c < 12; c++) {
      const colMon = new Date(startDate);
      colMon.setDate(startDate.getDate() + c * 7);
      const prevMon = new Date(colMon);
      prevMon.setDate(colMon.getDate() - 7);

      const curMonthName = colMon.toLocaleString('default', { month: 'short' });
      const prevMonthName = prevMon.toLocaleString('default', { month: 'short' });

      if (c === 0 || curMonthName !== prevMonthName) {
        if (c - lastLabelCol >= 3) {
          mLabels.push({ weekIndex: c, name: curMonthName });
          lastLabelCol = c;
        }
      }
    }

    // Format best day string
    let bestDayFormatted = '—';
    if (maxSolvedInDay > 0 && bestDayDateStr) {
      const bDate = new Date(bestDayDateStr + 'T00:00:00');
      const dayNum = bDate.getDate();
      const mStr = bDate.toLocaleString('default', { month: 'short' });
      bestDayFormatted = `${maxSolvedInDay} (${dayNum} ${mStr})`;
    }

    return {
      grid: columns,
      monthLabels: mLabels,
      stats: {
        activeDays: activeDaysCount,
        longestStreak,
        bestDay: bestDayFormatted
      },
      solvedIn12Weeks: totalSolved
    };
  }, [activity]);

  // Format tooltip content
  const formatTooltip = (item) => {
    if (!item || item.isFuture) return null;
    const d = new Date(item.date + 'T00:00:00');
    const weekday = d.toLocaleDateString('default', { weekday: 'short' });
    const day = d.getDate();
    const month = d.toLocaleDateString('default', { month: 'short' });
    const countText = `${item.count} solved`;
    return `${weekday} ${day} ${month} · ${countText}`;
  };

  return (
    <div 
      className="glass-card home-activity-card" 
      style={{ 
        padding: '24px', 
        display: 'flex', 
        flexDirection: 'column', 
        gap: '16px',
        width: '100%',
        boxSizing: 'border-box'
      }}
    >
      {/* Header: Activity & N solved in 12 weeks */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '8px' }}>
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-color)', margin: 0 }}>
          Activity
        </h3>
        <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--accent)', fontFamily: 'var(--font-mono)' }}>
          {solvedIn12Weeks} solved in 12 weeks
        </span>
      </div>

      {solvedIn12Weeks === 0 && (
        <p style={{ fontSize: '0.825rem', color: 'var(--text-muted)', margin: '-6px 0 0 0' }}>
          Solve a question to light up your first square.
        </p>
      )}

      {/* Grid Container */}
      <div style={{ width: '100%', minWidth: 0 }}>
        {/* Month labels placed by CSS grid column (no pixel offsets) */}
        <div 
          style={{ 
            display: 'grid', 
            gridTemplateColumns: '24px repeat(12, minmax(0, 1fr))', 
            gap: '4px', 
            width: '100%', 
            marginBottom: '4px',
            alignItems: 'end'
          }}
        >
          <div style={{ gridColumn: 1 }} />
          {monthLabels.map(m => (
            <div 
              key={m.weekIndex} 
              style={{ 
                gridColumn: m.weekIndex + 2, 
                fontSize: '0.72rem', 
                fontWeight: 600, 
                color: 'var(--text-muted)',
                lineHeight: 1
              }}
            >
              {m.name}
            </div>
          ))}
        </div>

        {/* 84-cell Matrix with Mon, Wed, Fri weekday labels */}
        <div 
          style={{ 
            display: 'grid', 
            gridTemplateColumns: '24px repeat(12, minmax(0, 1fr))', 
            gridTemplateRows: 'repeat(7, auto)', 
            gap: '4px', 
            width: '100%',
            alignItems: 'center'
          }}
        >
          {/* Weekday labels in column 1, aligned to rows 1, 3, 5 (Mon = 1, Wed = 3, Fri = 5) */}
          <div style={{ gridColumn: 1, gridRow: 1, fontSize: '0.7rem', color: 'var(--text-muted)', fontWeight: 600 }}>Mon</div>
          <div style={{ gridColumn: 1, gridRow: 3, fontSize: '0.7rem', color: 'var(--text-muted)', fontWeight: 600 }}>Wed</div>
          <div style={{ gridColumn: 1, gridRow: 5, fontSize: '0.7rem', color: 'var(--text-muted)', fontWeight: 600 }}>Fri</div>

          {/* 12 columns x 7 rows cells */}
          {grid.map((col, colIdx) => 
            col.map((cell, rowIdx) => {
              const tooltipText = formatTooltip(cell);
              return (
                <div
                  key={`${colIdx}-${rowIdx}`}
                  style={{
                    gridColumn: colIdx + 2,
                    gridRow: rowIdx + 1,
                    width: '100%',
                    aspectRatio: '1 / 1',
                    maxWidth: '36px',
                    borderRadius: '6px',
                    boxSizing: 'border-box',
                    background: cell.isFuture ? 'transparent' : `var(--activity-${cell.level})`,
                    border: cell.isFuture 
                      ? '1px dashed var(--glass-border)' 
                      : (cell.isToday ? '2px solid var(--accent)' : '1px solid var(--glass-border)'),
                    cursor: cell.isFuture ? 'default' : 'pointer',
                    position: 'relative'
                  }}
                  role={cell.isFuture ? 'presentation' : 'button'}
                  aria-label={tooltipText || 'Future date'}
                  tabIndex={cell.isFuture ? -1 : 0}
                  onMouseEnter={() => !cell.isFuture && setActiveTooltip(cell)}
                  onMouseLeave={() => setActiveTooltip(null)}
                  onClick={() => !cell.isFuture && setActiveTooltip(cell)}
                />
              );
            })
          )}
        </div>
      </div>

      {/* Active tooltip line / description */}
      <div style={{ minHeight: '20px', fontSize: '0.78rem', color: activeTooltip ? 'var(--text-color)' : 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
        {activeTooltip ? formatTooltip(activeTooltip) : 'Hover or tap a square for details'}
      </div>

      {/* Below the grid: mini stats row + legend */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px', borderTop: '1px solid var(--glass-border)', paddingTop: '12px' }}>
        {/* 3 mini stats */}
        <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
          <div>
            <div style={{ fontSize: '0.68rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Active days
            </div>
            <div style={{ fontSize: '0.9rem', fontWeight: 700, fontFamily: 'var(--font-mono)', color: 'var(--text-color)' }}>
              {stats.activeDays} <span style={{ fontSize: '0.75rem', fontWeight: 500, color: 'var(--text-muted)' }}>/ 84</span>
            </div>
          </div>

          <div>
            <div style={{ fontSize: '0.68rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Longest streak
            </div>
            <div style={{ fontSize: '0.9rem', fontWeight: 700, fontFamily: 'var(--font-mono)', color: 'var(--text-color)' }}>
              {stats.longestStreak} <span style={{ fontSize: '0.75rem', fontWeight: 500, color: 'var(--text-muted)' }}>{stats.longestStreak === 1 ? 'day' : 'days'}</span>
            </div>
          </div>

          <div>
            <div style={{ fontSize: '0.68rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Best day
            </div>
            <div style={{ fontSize: '0.9rem', fontWeight: 700, fontFamily: 'var(--font-mono)', color: 'var(--text-color)' }}>
              {stats.bestDay}
            </div>
          </div>
        </div>

        {/* Legend: Less to More */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '5px', fontSize: '0.72rem', color: 'var(--text-muted)' }}>
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
  );
}
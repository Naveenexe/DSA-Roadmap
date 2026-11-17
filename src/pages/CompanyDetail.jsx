import React, { useState, useMemo } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { 
  ArrowLeft, 
  ArrowRight, 
  ExternalLink, 
  Check, 
  Clock, 
  Link2, 
  Filter, 
  Sparkles,
  Briefcase
} from 'lucide-react';
import CompanyLogo from '../components/CompanyLogo';

export default function CompanyDetail() {
  const { slug } = useParams();
  const navigate = useNavigate();
  const { companies, questions, chapters, progressMap } = useApp();

  const [filterDifficulty, setFilterDifficulty] = useState('all'); // all, easy, medium, hard
  const [filterNotDoneOnly, setFilterNotDoneOnly] = useState(false);

  // Identify current company
  const company = useMemo(() => {
    return companies?.find(c => c.slug === slug) || { slug, name: slug, domain: '' };
  }, [companies, slug]);

  // Questions tagged for this company
  const companyQuestions = useMemo(() => {
    return questions.filter(q => q.companies && q.companies.includes(slug));
  }, [questions, slug]);

  // Done count & readiness
  const totalCount = companyQuestions.length;
  const doneCount = useMemo(() => {
    return companyQuestions.filter(q => progressMap[q.seq]?.status === 'done').length;
  }, [companyQuestions, progressMap]);

  const readinessRatio = totalCount > 0 ? (doneCount / totalCount) : 0;

  // Difficulty counts
  const diffCounts = useMemo(() => {
    const counts = {
      Easy: { done: 0, total: 0 },
      Medium: { done: 0, total: 0 },
      Hard: { done: 0, total: 0 }
    };
    companyQuestions.forEach(q => {
      if (counts[q.difficulty]) {
        counts[q.difficulty].total++;
        if (progressMap[q.seq]?.status === 'done') {
          counts[q.difficulty].done++;
        }
      }
    });
    return counts;
  }, [companyQuestions, progressMap]);

  // Start next: lowest-Seq unfinished question of this company
  const startNextQuestion = useMemo(() => {
    const unfinished = companyQuestions.filter(q => progressMap[q.seq]?.status !== 'done');
    if (unfinished.length === 0) return null;
    return unfinished.sort((a, b) => a.seq - b.seq)[0];
  }, [companyQuestions, progressMap]);

  // Next company recommendation (for when all are done)
  const nextCompany = useMemo(() => {
    if (!companies || companies.length === 0) return null;
    const curIdx = companies.findIndex(c => c.slug === slug);
    const nextIdx = (curIdx + 1) % companies.length;
    return companies[nextIdx];
  }, [companies, slug]);

  // Filtered list
  const filteredQuestions = useMemo(() => {
    return companyQuestions.filter(q => {
      if (filterDifficulty !== 'all' && q.difficulty.toLowerCase() !== filterDifficulty.toLowerCase()) {
        return false;
      }
      if (filterNotDoneOnly && progressMap[q.seq]?.status === 'done') {
        return false;
      }
      return true;
    });
  }, [companyQuestions, filterDifficulty, filterNotDoneOnly, progressMap]);

  // Group filtered questions by chapter
  const groupedByChapter = useMemo(() => {
    const map = new Map();
    filteredQuestions.forEach(q => {
      const ch = chapters.find(c => c.id === q.chapter) || { id: q.chapter, order: 0, name: q.chapter };
      if (!map.has(ch.id)) {
        map.set(ch.id, { chapter: ch, list: [] });
      }
      map.get(ch.id).list.push(q);
    });
    return Array.from(map.values()).sort((a, b) => a.chapter.order - b.chapter.order);
  }, [filteredQuestions, chapters]);

  // Ring calculations
  const ringSize = 110;
  const stroke = 9;
  const radius = (ringSize - stroke) / 2;
  const circumference = 2 * Math.PI * radius;
  const dashoffset = circumference - (readinessRatio * circumference);

  const renderStatusIcon = (status) => {
    if (status === 'done') {
      return (
        <span style={{ width: 22, height: 22, borderRadius: '50%', background: 'var(--accent-soft)', color: 'var(--accent-soft-text)', display: 'inline-flex', alignItems: 'center', justifyContent: 'center' }}>
          <Check size={13} strokeWidth={3} />
        </span>
      );
    }
    if (status === 'in_progress') {
      return (
        <span style={{ width: 22, height: 22, borderRadius: '50%', border: '2px solid var(--accent)', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', position: 'relative', overflow: 'hidden' }}>
          <div style={{ position: 'absolute', left: 0, top: 0, width: '50%', height: '100%', background: 'var(--accent)' }} />
        </span>
      );
    }
    if (status === 'revisit') {
      return <Clock size={18} color="var(--revisit-color)" />;
    }
    return <span style={{ width: 18, height: 18, borderRadius: '50%', border: '2px solid var(--progress-track)', display: 'inline-flex' }} />;
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', width: '100%', maxWidth: '100%' }}>
      {/* Navigation link */}
      <div>
        <Link 
          to="/companies" 
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
          <span>All Companies</span>
        </Link>
      </div>

      {/* Header Glass Card */}
      <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '20px' }}>
          
          {/* Logo & Name */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <CompanyLogo slug={company.slug} name={company.name} domain={company.domain} size={56} showTooltip={false} />
            <div>
              <h1 style={{ fontSize: 'clamp(1.4rem, 3.5vw, 2rem)', fontWeight: 800, color: 'var(--text-color)', margin: 0, letterSpacing: '-0.02em' }}>
                {company.name}
              </h1>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px', fontFamily: 'var(--font-mono)' }}>
                {totalCount} tagged questions · {doneCount} solved
              </div>
            </div>
          </div>

          {/* Readiness Ring & Difficulty Breakdown */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '20px', flexWrap: 'wrap' }}>
            {/* Readiness Ring */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
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
                <div style={{ position: 'absolute', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                  <span style={{ fontSize: '1.25rem', fontWeight: 800, fontFamily: 'var(--font-sans)', lineHeight: 1 }}>
                    {Math.round(readinessRatio * 100)}%
                  </span>
                  <span style={{ fontSize: '0.68rem', color: 'var(--text-muted)', fontWeight: 600 }}>
                    readiness
                  </span>
                </div>
              </div>

              {/* Difficulty breakdown */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', fontSize: '0.8rem' }}>
                <div style={{ display: 'flex', gap: '6px', alignItems: 'center' }}>
                  <span style={{ color: 'var(--easy-pill-text)', fontWeight: 700, minWidth: '40px' }}>Easy</span>
                  <span style={{ fontFamily: 'var(--font-mono)' }}>{diffCounts.Easy.done}/{diffCounts.Easy.total}</span>
                </div>
                <div style={{ display: 'flex', gap: '6px', alignItems: 'center' }}>
                  <span style={{ color: 'var(--medium-pill-text)', fontWeight: 700, minWidth: '40px' }}>Med</span>
                  <span style={{ fontFamily: 'var(--font-mono)' }}>{diffCounts.Medium.done}/{diffCounts.Medium.total}</span>
                </div>
                <div style={{ display: 'flex', gap: '6px', alignItems: 'center' }}>
                  <span style={{ color: 'var(--hard-pill-text)', fontWeight: 700, minWidth: '40px' }}>Hard</span>
                  <span style={{ fontFamily: 'var(--font-mono)' }}>{diffCounts.Hard.done}/{diffCounts.Hard.total}</span>
                </div>
              </div>
            </div>

            {/* Start Next Button */}
            {startNextQuestion ? (
              <button
                onClick={() => navigate(`/question/${startNextQuestion.seq}`)}
                className="btn-primary"
                style={{ padding: '10px 20px', minHeight: '44px', fontSize: '0.9rem' }}
              >
                <span>Start Next (#{startNextQuestion.seq})</span>
                <ArrowRight size={16} />
              </button>
            ) : (
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--accent)', fontWeight: 700, fontSize: '0.9rem' }}>
                <Sparkles size={18} />
                <span>All {totalCount} Done!</span>
              </div>
            )}

          </div>

        </div>

        {/* Filter Chips: All, Easy, Medium, Hard, Not done */}
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', borderTop: '1px solid var(--glass-border)', paddingTop: '16px' }}>
          {['all', 'easy', 'medium', 'hard'].map(diff => (
            <button
              key={diff}
              type="button"
              onClick={() => setFilterDifficulty(diff)}
              className="nav-pill filter-chip"
              style={{
                background: filterDifficulty === diff ? 'var(--accent)' : 'var(--glass-surface)',
                color: filterDifficulty === diff ? 'var(--accent-text)' : 'var(--text-color)',
                fontSize: '0.8rem',
                padding: '6px 14px',
                minHeight: '38px',
                textTransform: 'capitalize'
              }}
            >
              {diff === 'all' ? 'All' : diff}
            </button>
          ))}

          <button
            type="button"
            onClick={() => setFilterNotDoneOnly(!filterNotDoneOnly)}
            className="nav-pill filter-chip"
            style={{
              background: filterNotDoneOnly ? 'var(--accent-soft)' : 'var(--glass-surface)',
              color: filterNotDoneOnly ? 'var(--accent)' : 'var(--text-color)',
              fontSize: '0.8rem',
              padding: '6px 14px',
              minHeight: '38px'
            }}
          >
            Not Done ({totalCount - doneCount})
          </button>
        </div>
      </div>

      {/* Empty State: All Completed */}
      {doneCount === totalCount && totalCount > 0 && (
        <div className="glass-card" style={{ padding: '24px', textAlign: 'center', background: 'var(--accent-soft)' }}>
          <h3 style={{ fontSize: '1.15rem', fontWeight: 800, color: 'var(--accent)', margin: '0 0 6px 0' }}>
            🎉 You have solved all questions tagged for {company.name}!
          </h3>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-color)', margin: '0 0 14px 0' }}>
            Keep reviewing due items, or explore the next company.
          </p>
          {nextCompany && (
            <Link to={`/companies/${nextCompany.slug}`} className="btn-primary" style={{ display: 'inline-flex', padding: '8px 16px', minHeight: '40px', textDecoration: 'none' }}>
              <span>Next Company: {nextCompany.name}</span>
              <ArrowRight size={15} />
            </Link>
          )}
        </div>
      )}

      {/* Grouped Question Rows under small chapter headings */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {groupedByChapter.map(group => (
          <div key={group.chapter.id} style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {/* Small chapter heading */}
            <div style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', padding: '0 4px' }}>
              Chapter {group.chapter.order}: {group.chapter.name}
            </div>

            {/* Questions list */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {group.list.map(q => {
                const p = progressMap[q.seq];
                const status = p?.status || 'todo';
                const buildsOnQ = q.buildsOn ? questions.find(item => item.seq === q.buildsOn) : null;

                return (
                  <div
                    key={q.seq}
                    className="glass-card question-item-card"
                    style={{ padding: '12px 16px' }}
                  >
                    {/* Desktop row view */}
                    <div className="question-row-desktop">
                      <div style={{ width: 28, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        {renderStatusIcon(status)}
                      </div>
                      <div style={{ width: 44, fontFamily: 'var(--font-mono)', fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600 }}>
                        #{q.seq}
                      </div>
                      <div style={{ flex: 1, minWidth: 0 }}>
                        <Link to={`/question/${q.seq}`} className="question-row-title" style={{ display: 'inline-block', maxWidth: '100%' }}>
                          {q.title}
                        </Link>
                      </div>
                      <span className={`diff-pill diff-pill-${q.difficulty.toLowerCase()}`}>
                        {q.difficulty}
                      </span>
                      <div style={{ width: 170, fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                        {buildsOnQ ? (
                          <Link to={`/question/${buildsOnQ.seq}`} style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', color: 'var(--accent)', fontWeight: 600 }}>
                            <Link2 size={12} />
                            <span>Builds on #{buildsOnQ.seq}</span>
                          </Link>
                        ) : (
                          <span style={{ fontStyle: 'italic', opacity: 0.7 }}>Foundation</span>
                        )}
                      </div>
                      <a
                        href={`https://leetcode.com/problems/${q.slug}/`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="icon-circle-btn"
                        style={{ minWidth: '38px', minHeight: '38px' }}
                        title={`Open on LeetCode`}
                      >
                        <ExternalLink size={14} />
                      </a>
                    </div>

                    {/* Mobile card view */}
                    <div className="question-card-mobile">
                      <div className="question-card-mobile-line1">
                        <div style={{ flexShrink: 0, display: 'inline-flex', alignItems: 'center' }}>
                          {renderStatusIcon(status)}
                        </div>
                        <span className="question-mobile-seq">#{q.seq}</span>
                        <Link to={`/question/${q.seq}`} className="question-mobile-title">
                          {q.title}
                        </Link>
                      </div>
                      <div className="question-card-mobile-line2">
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap', flex: '1 1 auto', minWidth: 0 }}>
                          <span className={`diff-pill diff-pill-${q.difficulty.toLowerCase()}`}>
                            {q.difficulty}
                          </span>
                          {buildsOnQ ? (
                            <Link to={`/question/${buildsOnQ.seq}`} className="question-mobile-buildson">
                              <Link2 size={12} />
                              <span>builds on #{buildsOnQ.seq}</span>
                            </Link>
                          ) : (
                            <span className="question-mobile-foundation">Foundation</span>
                          )}
                        </div>
                        <a
                          href={`https://leetcode.com/problems/${q.slug}/`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="mobile-lc-arrow-btn"
                        >
                          <ExternalLink size={15} />
                        </a>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      {/* Legal & Attribution Disclaimer Footer */}
      <footer style={{ textAlign: 'center', fontSize: '0.75rem', color: 'var(--text-muted)', padding: '16px 0 32px 0', borderTop: '1px solid var(--glass-border)' }}>
        Company names and logos belong to their owners. Chainline is not affiliated with them. Tags reported by candidates.
      </footer>
    </div>
  );
}
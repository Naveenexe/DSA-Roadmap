import React, { useState, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { Search, X, Briefcase, ArrowRight } from 'lucide-react';
import CompanyLogo from '../components/CompanyLogo';

export default function Companies() {
  const { companies, questions, progressMap } = useApp();
  const [search, setSearch] = useState('');

  // Calculate tagged question counts and progress for each company
  const companyList = useMemo(() => {
    if (!companies || companies.length === 0) return [];

    const list = companies.map(comp => {
      const tagged = questions.filter(q => q.companies && q.companies.includes(comp.slug));
      const done = tagged.filter(q => progressMap[q.seq]?.status === 'done').length;
      return {
        ...comp,
        totalQuestions: tagged.length,
        doneQuestions: done,
        progressRatio: tagged.length > 0 ? (done / tagged.length) : 0
      };
    });

    // Hide companies with 0 questions, sort most questions first
    return list.filter(c => c.totalQuestions > 0).sort((a, b) => b.totalQuestions - a.totalQuestions);
  }, [companies, questions, progressMap]);

  // Filter by search query
  const filteredList = useMemo(() => {
    const q = search.trim().toLowerCase();
    if (!q) return companyList;
    return companyList.filter(c => c.name.toLowerCase().includes(q) || c.slug.toLowerCase().includes(q));
  }, [companyList, search]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', width: '100%', maxWidth: '100%' }}>
      {/* Header Card */}
      <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
              <Briefcase size={20} color="var(--accent)" />
              <h1 style={{ fontSize: 'clamp(1.4rem, 3vw, 1.85rem)', fontWeight: 800, color: 'var(--text-color)', margin: 0 }}>
                Company Problem Sets
              </h1>
            </div>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', margin: 0 }}>
              Curated LeetCode problems reported for 30 top tech companies.
            </p>
          </div>

          <Link to="/roadmap" className="btn-secondary" style={{ fontSize: '0.85rem', padding: '8px 16px', minHeight: '44px' }}>
            Back to Roadmap
          </Link>
        </div>

        {/* Search Box */}
        <div style={{ position: 'relative', width: '100%', maxWidth: '360px' }}>
          <Search size={16} style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search company (e.g. Google, Amazon)..."
            className="glass-input"
            style={{ paddingLeft: '40px', paddingRight: '32px', height: '44px', minHeight: '44px', fontSize: '16px', width: '100%' }}
          />
          {search && (
            <button
              type="button"
              onClick={() => setSearch('')}
              style={{ position: 'absolute', right: '10px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)', border: 'none', background: 'transparent', cursor: 'pointer', padding: '4px' }}
              aria-label="Clear search"
            >
              <X size={15} />
            </button>
          )}
        </div>
      </div>

      {/* Grid of Company Cards (3 cols desktop, 2 cols tablet/mobile) */}
      {filteredList.length === 0 ? (
        <div className="glass-card empty-state-box" style={{ padding: '40px 20px', textAlign: 'center' }}>
          <Briefcase size={36} color="var(--text-muted)" style={{ margin: '0 auto 12px auto' }} />
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-color)', margin: '0 0 6px 0' }}>
            No companies found
          </h3>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', margin: '0 0 16px 0' }}>
            No companies match "{search}".
          </p>
          <button onClick={() => setSearch('')} className="btn-secondary" style={{ minHeight: '44px' }}>
            Clear search
          </button>
        </div>
      ) : (
        <div 
          className="companies-grid" 
          style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', 
            gap: '16px',
            width: '100%'
          }}
        >
          {filteredList.map(comp => (
            <Link
              key={comp.slug}
              to={`/companies/${comp.slug}`}
              className="glass-card glass-card-interactive company-prep-card"
              style={{
                padding: '20px',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                gap: '14px',
                textDecoration: 'none',
                minWidth: '150px'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                <CompanyLogo slug={comp.slug} name={comp.name} domain={comp.domain} size={48} showTooltip={false} />
                <div style={{ minWidth: 0, flex: 1 }}>
                  <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--text-color)', margin: 0, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {comp.name}
                  </h3>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '2px', fontFamily: 'var(--font-mono)' }}>
                    {comp.totalQuestions} questions
                  </div>
                </div>
              </div>

              {/* Progress bar with done/N */}
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '6px' }}>
                  <span>Solved</span>
                  <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 600 }}>
                    {comp.doneQuestions} / {comp.totalQuestions}
                  </span>
                </div>
                <div className="progress-bar-container" style={{ height: '7px' }}>
                  <div
                    className="progress-bar-fill"
                    style={{ width: `${Math.round(comp.progressRatio * 100)}%` }}
                  />
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}

      {/* Legal & Attribution Disclaimer Footer */}
      <footer style={{ textAlign: 'center', fontSize: '0.75rem', color: 'var(--text-muted)', padding: '16px 0 32px 0', borderTop: '1px solid var(--glass-border)' }}>
        Company names and logos belong to their owners. Chainline is not affiliated with them. Tags reported by candidates.
      </footer>
    </div>
  );
}
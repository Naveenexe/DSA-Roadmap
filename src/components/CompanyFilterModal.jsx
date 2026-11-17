import React, { useState, useMemo, useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import { useApp } from '../context/AppContext';
import { Search, X, Briefcase } from 'lucide-react';
import CompanyLogo from './CompanyLogo';

export default function CompanyFilterModal({ 
  isOpen, 
  onClose, 
  onSelectCompany, 
  chapterQuestions = [], 
  anchorRef 
}) {
  const { companies } = useApp();
  const [search, setSearch] = useState('');
  const [coords, setCoords] = useState({ top: 0, left: 0, width: 280 });
  const isMobile = typeof window !== 'undefined' && window.innerWidth < 768;

  // Position portal dropdown relative to anchorRef on desktop
  useEffect(() => {
    if (!isOpen || isMobile || !anchorRef?.current) return;
    const rect = anchorRef.current.getBoundingClientRect();
    const dropdownWidth = 280;
    let left = rect.left;
    if (left + dropdownWidth > window.innerWidth - 16) {
      left = window.innerWidth - dropdownWidth - 16;
    }
    setCoords({
      top: rect.bottom + 8,
      left: Math.max(16, left),
      width: dropdownWidth
    });
  }, [isOpen, isMobile, anchorRef]);

  // Compute question count per company within active chapter
  const companyCounts = useMemo(() => {
    const counts = {};
    chapterQuestions.forEach(q => {
      if (Array.isArray(q.companies)) {
        q.companies.forEach(slug => {
          counts[slug] = (counts[slug] || 0) + 1;
        });
      }
    });
    return counts;
  }, [chapterQuestions]);

  // Filter companies that have at least 1 question in this chapter (or all 30 if none)
  const availableCompanies = useMemo(() => {
    if (!companies || companies.length === 0) return [];
    const q = search.trim().toLowerCase();
    return companies
      .filter(c => {
        if (q && !c.name.toLowerCase().includes(q) && !c.slug.toLowerCase().includes(q)) {
          return false;
        }
        return true;
      })
      .map(c => ({
        ...c,
        count: companyCounts[c.slug] || 0
      }))
      .sort((a, b) => (b.count - a.count) || a.name.localeCompare(b.name));
  }, [companies, companyCounts, search]);

  if (!isOpen) return null;

  // Mobile Bottom Sheet
  if (isMobile) {
    return createPortal(
      <div className="bottom-sheet-overlay" onClick={onClose} style={{ zIndex: 60 }}>
        <div 
          className="bottom-sheet-content glass-card" 
          onClick={(e) => e.stopPropagation()}
          style={{ maxHeight: '75vh', display: 'flex', flexDirection: 'column', gap: '12px' }}
        >
          <div className="bottom-sheet-handle" />
          <div className="bottom-sheet-header">
            <h3 style={{ fontSize: '1.1rem', fontWeight: 800, color: 'var(--text-color)', margin: 0 }}>
              Filter by Company
            </h3>
            <button
              type="button"
              onClick={onClose}
              className="icon-circle-btn"
              style={{ width: 36, height: 36, minWidth: 36, minHeight: 36 }}
              aria-label="Close"
            >
              <X size={16} />
            </button>
          </div>

          {/* Search box */}
          <div style={{ position: 'relative', width: '100%' }}>
            <Search size={15} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search company..."
              className="glass-input"
              style={{ paddingLeft: '36px', height: '40px', minHeight: '40px', fontSize: '15px', width: '100%' }}
              autoFocus
            />
          </div>

          {/* Scrollable list */}
          <div style={{ overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '4px', paddingBottom: '16px' }}>
            {availableCompanies.map(comp => (
              <button
                key={comp.slug}
                type="button"
                onClick={() => {
                  onSelectCompany(comp.slug);
                  onClose();
                }}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '10px 12px',
                  borderRadius: 'var(--radius-inner)',
                  background: 'transparent',
                  border: 'none',
                  cursor: 'pointer',
                  minHeight: '44px',
                  textAlign: 'left',
                  transition: 'background 120ms ease'
                }}
                onMouseEnter={(e) => e.currentTarget.style.background = 'var(--glass-surface)'}
                onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <CompanyLogo slug={comp.slug} name={comp.name} domain={comp.domain} size={28} showTooltip={false} />
                  <span style={{ fontWeight: 600, fontSize: '0.9rem', color: 'var(--text-color)' }}>
                    {comp.name}
                  </span>
                </div>
                {comp.count > 0 && (
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', color: 'var(--accent)', fontWeight: 700 }}>
                    {comp.count}
                  </span>
                )}
              </button>
            ))}
          </div>
        </div>
      </div>,
      document.body
    );
  }

  // Desktop Portal Dropdown
  return createPortal(
    <>
      {/* Invisible backdrop to dismiss on click outside */}
      <div 
        style={{ position: 'fixed', inset: 0, zIndex: 40 }} 
        onClick={onClose} 
      />
      <div
        className="glass-card"
        style={{
          position: 'fixed',
          top: `${coords.top}px`,
          left: `${coords.left}px`,
          width: `${coords.width}px`,
          maxHeight: '340px',
          zIndex: 41,
          padding: '12px',
          display: 'flex',
          flexDirection: 'column',
          gap: '8px',
          boxShadow: '0 12px 32px rgba(0,0,0,0.3)',
          boxSizing: 'border-box'
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <div style={{ position: 'relative', width: '100%' }}>
          <Search size={14} style={{ position: 'absolute', left: '10px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Filter companies..."
            className="glass-input"
            style={{ paddingLeft: '32px', height: '34px', minHeight: '34px', fontSize: '0.8rem', width: '100%' }}
            autoFocus
          />
        </div>

        <div style={{ overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '2px', maxHeight: '240px' }}>
          {availableCompanies.map(comp => (
            <button
              key={comp.slug}
              type="button"
              onClick={() => {
                onSelectCompany(comp.slug);
                onClose();
              }}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '6px 8px',
                borderRadius: 'var(--radius-inner)',
                background: 'transparent',
                border: 'none',
                cursor: 'pointer',
                textAlign: 'left',
                minHeight: '36px',
                transition: 'background 120ms ease'
              }}
              onMouseEnter={(e) => e.currentTarget.style.background = 'var(--glass-surface)'}
              onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <CompanyLogo slug={comp.slug} name={comp.name} domain={comp.domain} size={22} showTooltip={false} />
                <span style={{ fontWeight: 600, fontSize: '0.825rem', color: 'var(--text-color)' }}>
                  {comp.name}
                </span>
              </div>
              {comp.count > 0 && (
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.72rem', color: 'var(--accent)', fontWeight: 700 }}>
                  {comp.count}
                </span>
              )}
            </button>
          ))}
        </div>
      </div>
    </>,
    document.body
  );
}
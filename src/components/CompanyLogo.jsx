import React, { useState } from 'react';
import { useApp } from '../context/AppContext';

export default function CompanyLogo({ 
  slug, 
  name: propName, 
  domain: propDomain, 
  size = 24, 
  showTooltip = true,
  style = {} 
}) {
  const { companies } = useApp();
  const [failed, setFailed] = useState(false);

  // Look up company info if only slug is provided
  const companyInfo = companies?.find(c => c.slug === slug);
  const displayName = propName || companyInfo?.name || slug;
  const domain = propDomain || companyInfo?.domain;

  const logoToken = import.meta.env.VITE_LOGO_TOKEN;
  // If logoToken is provided and domain exists, construct logo URL
  // Otherwise, or if loading fails, gracefully fallback to letter chip
  const logoUrl = (logoToken && domain && !failed) 
    ? `https://img.logo.dev/${domain}?token=${logoToken}` 
    : null;

  const firstLetter = (displayName ? displayName.charAt(0) : '?').toUpperCase();
  const tooltipText = showTooltip 
    ? `${displayName} · Reported by candidates. May be out of date.` 
    : undefined;

  return (
    <div
      title={tooltipText}
      style={{
        width: `${size}px`,
        height: `${size}px`,
        minWidth: `${size}px`,
        minHeight: `${size}px`,
        maxWidth: `${size}px`,
        maxHeight: `${size}px`,
        borderRadius: '50%',
        background: 'var(--glass-surface)',
        border: '1px solid var(--glass-border)',
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        overflow: 'hidden',
        boxSizing: 'border-box',
        verticalAlign: 'middle',
        flexShrink: 0,
        ...style
      }}
    >
      {logoUrl ? (
        <img
          src={logoUrl}
          alt={displayName}
          loading="lazy"
          onError={() => setFailed(true)}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            borderRadius: '50%'
          }}
        />
      ) : (
        <span
          style={{
            fontSize: `${Math.max(10, Math.round(size * 0.44))}px`,
            fontWeight: 800,
            fontFamily: 'var(--font-sans)',
            color: 'var(--accent)',
            lineHeight: 1,
            userSelect: 'none'
          }}
        >
          {firstLetter}
        </span>
      )}
    </div>
  );
}
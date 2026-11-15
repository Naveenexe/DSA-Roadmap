import React from 'react';

export default function ChainlineLogo({ size = 26, showText = true, className = '' }) {
  return (
    <div className={`chainline-brand ${className}`} style={{ display: 'inline-flex', alignItems: 'center', gap: '0.6rem' }}>
      <svg 
        width={size} 
        height={size} 
        viewBox="0 0 32 32" 
        fill="none" 
        xmlns="http://www.w3.org/2000/svg"
        style={{ flexShrink: 0 }}
      >
        {/* Background rounded squircle */}
        <rect width="32" height="32" rx="9" fill="var(--accent)" />
        {/* Outer interlocking rounded link */}
        <path 
          d="M20 8H14.5C10.9 8 8 10.9 8 14.5C8 18.1 10.9 21 14.5 21H20" 
          stroke="var(--accent-text)" 
          strokeWidth="2.75" 
          strokeLinecap="round" 
        />
        {/* Inner interlocked link forming letter C */}
        <path 
          d="M22 11H16.5C14.0 11 12 13.0 12 15.5C12 18.0 14.0 20 16.5 20H22" 
          stroke="var(--accent-soft-text)" 
          strokeWidth="2.5" 
          strokeLinecap="round" 
        />
      </svg>
      {showText && (
        <span style={{ 
          fontFamily: 'var(--font-sans)', 
          fontWeight: 700, 
          fontSize: '1.15rem', 
          letterSpacing: '-0.025em', 
          color: 'var(--text-color)' 
        }}>
          Chainline
        </span>
      )}
    </div>
  );
}

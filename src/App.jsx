import React, { useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useApp } from './context/AppContext';
import Navbar from './components/Navbar';
import MobileNav from './components/MobileNav';
import AuthView from './components/AuthView';
import Dashboard from './pages/Dashboard';
import Roadmap from './pages/Roadmap';
import Question from './pages/Question';
import Today from './pages/Today';
import Settings from './pages/Settings';
import { AlertCircle, CheckCircle, Info } from 'lucide-react';

export default function App() {
  const [authModalOpen, setAuthModalOpen] = useState(false);
  const [authTab, setAuthTab] = useState('signin');
  const { toast } = useApp();

  const handleOpenAuth = (tab = 'signin') => {
    setAuthTab(tab);
    setAuthModalOpen(true);
  };

  return (
    <div className="app-root">
      {/* Background Ambient Blurred Orbs (Section 3 #17 & Section 4.1) */}
      <div className="orb-background" aria-hidden="true">
        <div className="orb orb-1" />
        <div className="orb orb-2" />
        <div className="orb orb-3" />
      </div>

      {/* Top Floating Glass Navigation Pill (64px, Section 4.6 & 5.2) */}
      <Navbar onOpenAuth={() => handleOpenAuth('signin')} />

      {/* Main Content Area (Max width 1280px, Section 5.1) */}
      <main className="main-container">
        <Routes>
          <Route path="/" element={<Dashboard onOpenAuth={handleOpenAuth} />} />
          <Route path="/roadmap" element={<Roadmap />} />
          <Route path="/question/:seq" element={<Question />} />
          <Route path="/today" element={<Today />} />
          <Route path="/settings" element={<Settings onOpenAuth={handleOpenAuth} />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>

      {/* Mobile Bottom Navigation Bar (Visible on every page except Sign in) */}
      {!authModalOpen && <MobileNav />}

      {/* Sign In & Create Account Modal (Section 5.2 & FR-1, FR-1a) */}
      <AuthView 
        isOpen={authModalOpen} 
        initialTab={authTab}
        onClose={() => setAuthModalOpen(false)} 
      />

      {/* Floating Glass Toast Alert */}
      {toast && (
        <div className="toast-container">
          {toast.type === 'error' ? (
            <AlertCircle size={18} color="#EF4444" />
          ) : toast.type === 'success' ? (
            <CheckCircle size={18} color="#10B981" />
          ) : (
            <Info size={18} color="var(--accent-text)" />
          )}
          <span>{toast.message}</span>
        </div>
      )}
    </div>
  );
}

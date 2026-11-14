import React, { useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useApp } from './context/AppContext';
import Navbar from './components/Navbar';
import MobileNav from './components/MobileNav';
import LoginModal from './components/LoginModal';
import Dashboard from './pages/Dashboard';
import Roadmap from './pages/Roadmap';
import Question from './pages/Question';
import Today from './pages/Today';
import Settings from './pages/Settings';
import { AlertCircle, CheckCircle, Info } from 'lucide-react';

export default function App() {
  const [loginModalOpen, setLoginModalOpen] = useState(false);
  const { toast } = useApp();

  return (
    <div className="app-layout">
      <Navbar onOpenLogin={() => setLoginModalOpen(true)} />
      
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard onOpenLogin={() => setLoginModalOpen(true)} />} />
          <Route path="/roadmap" element={<Roadmap />} />
          <Route path="/question/:seq" element={<Question />} />
          <Route path="/today" element={<Today />} />
          <Route path="/settings" element={<Settings onOpenLogin={() => setLoginModalOpen(true)} />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>

      <MobileNav />

      <LoginModal 
        isOpen={loginModalOpen} 
        onClose={() => setLoginModalOpen(false)} 
      />

      {/* Floating Toast Alert */}
      {toast && (
        <div className="toast-banner">
          {toast.type === 'error' ? (
            <AlertCircle size={18} color="var(--danger)" />
          ) : toast.type === 'success' ? (
            <CheckCircle size={18} color="var(--success)" />
          ) : (
            <Info size={18} color="var(--accent)" />
          )}
          <span style={{ fontSize: '0.85rem', fontWeight: 500 }}>{toast.message}</span>
        </div>
      )}
    </div>
  );
}


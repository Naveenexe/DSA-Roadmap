import React, { createContext, useContext, useState, useEffect, useMemo, useCallback } from 'react';
import { api } from '../services/api';

const AppContext = createContext(null);

export function AppProvider({ children }) {
  const [questions, setQuestions] = useState([]);
  const [chapters, setChapters] = useState([]);
  const [loadingData, setLoadingData] = useState(true);

  // User session
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('dsa_session_user');
    return saved ? JSON.parse(saved) : null;
  });
  const [pinHash, setPinHash] = useState(() => {
    return localStorage.getItem('dsa_session_pin_hash') || null;
  });

  // State
  const [progressMap, setProgressMap] = useState({});
  const [reviews, setReviews] = useState([]);
  const [activity, setActivity] = useState([]);
  const [toast, setToast] = useState(null);

  // Load static questions and chapters
  useEffect(() => {
    async function loadStaticData() {
      try {
        const [chRes, qRes] = await Promise.all([
          fetch('/data/chapters.json'),
          fetch('/data/questions.json')
        ]);
        const chData = await chRes.json();
        const qData = await qRes.json();
        setChapters(chData);
        setQuestions(qData);
      } catch (err) {
        console.error('Failed to load static question data:', err);
      } finally {
        setLoadingData(false);
      }
    }
    loadStaticData();
  }, []);

  // Sync state when user is logged in
  const syncUserState = useCallback(async (username, hash) => {
    if (!username) return;
    try {
      const state = await api.getState(username, hash);
      if (state.user) {
        setUser(state.user);
        localStorage.setItem('dsa_session_user', JSON.stringify(state.user));
        // Apply theme
        if (state.user.theme) {
          document.documentElement.setAttribute('data-theme', state.user.theme);
        }
      }
      
      const pMap = {};
      if (Array.isArray(state.progress)) {
        state.progress.forEach(item => {
          pMap[item.question_seq] = item;
        });
      }
      setProgressMap(pMap);
      setReviews(state.reviews || []);
      setActivity(state.activity || []);
    } catch (err) {
      console.error('Error fetching user state:', err);
    }
  }, []);

  useEffect(() => {
    if (user && user.username) {
      syncUserState(user.username, pinHash);
    }
  }, [user?.username, pinHash, syncUserState]);

  // Handle Login
  const login = async (username, pin) => {
    const res = await api.login(username, pin);
    setUser(res.user);
    setPinHash(res.pinHash);
    localStorage.setItem('dsa_session_user', JSON.stringify(res.user));
    if (res.pinHash) {
      localStorage.setItem('dsa_session_pin_hash', res.pinHash);
    } else {
      localStorage.removeItem('dsa_session_pin_hash');
    }
    if (res.user.theme) {
      document.documentElement.setAttribute('data-theme', res.user.theme);
    }

    const pMap = {};
    if (res.state && Array.isArray(res.state.progress)) {
      res.state.progress.forEach(p => { pMap[p.question_seq] = p; });
    }
    setProgressMap(pMap);
    setReviews(res.state?.reviews || []);
    setActivity(res.state?.activity || []);
    return res.user;
  };

  // Handle Logout
  const logout = () => {
    setUser(null);
    setPinHash(null);
    setProgressMap({});
    setReviews([]);
    setActivity([]);
    localStorage.removeItem('dsa_session_user');
    localStorage.removeItem('dsa_session_pin_hash');
  };

  // Delete User Account
  const deleteAccount = async () => {
    if (!user) return;
    await api.deleteUser(user.username, pinHash);
    logout();
  };

  // Optimistic Progress Update
  const updateProgress = async ({ questionSeq, status, mistake, notes, remind = true, dueDate = null }) => {
    if (!user) return;

    // Previous state snapshot for rollback
    const prevProgress = { ...progressMap };
    const prevReviews = [...reviews];
    const prevActivity = [...activity];

    // Optimistically update local state
    const todayStr = new Date().toISOString().split('T')[0];
    const nowIso = new Date().toISOString();
    const existing = progressMap[questionSeq];
    const wasAlreadyDone = existing && existing.status === 'done';

    const updatedItem = {
      question_seq: questionSeq,
      status: status,
      mistake: mistake !== undefined ? mistake : (existing?.mistake || false),
      notes: notes !== undefined ? notes : (existing?.notes || ''),
      solved_at: status === 'done' ? (existing?.solved_at || nowIso) : existing?.solved_at,
      updated_at: nowIso
    };

    setProgressMap(prev => ({
      ...prev,
      [questionSeq]: updatedItem
    }));

    if (status === 'done' && !wasAlreadyDone) {
      setActivity(prev => {
        const copy = [...prev];
        const idx = copy.findIndex(a => a.day === todayStr);
        if (idx >= 0) {
          copy[idx] = { ...copy[idx], solved_count: copy[idx].solved_count + 1 };
        } else {
          copy.push({ day: todayStr, solved_count: 1 });
        }
        return copy;
      });

      if (remind) {
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        const tomStr = tomorrow.toISOString().split('T')[0];
        setReviews(prev => {
          const filtered = prev.filter(r => r.question_seq !== questionSeq);
          filtered.push({ question_seq: questionSeq, due_date: tomStr, step: 0, source: 'auto' });
          return filtered;
        });
      }
    } else if (status === 'revisit') {
      const tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);
      const revDate = dueDate || tomorrow.toISOString().split('T')[0];
      setReviews(prev => {
        const filtered = prev.filter(r => r.question_seq !== questionSeq);
        filtered.push({ question_seq: questionSeq, due_date: revDate, step: 0, source: 'manual' });
        return filtered;
      });
    }

    try {
      const newState = await api.saveProgress(user.username, pinHash, {
        questionSeq,
        status,
        mistake: updatedItem.mistake,
        notes: updatedItem.notes,
        remind,
        dueDate
      });

      if (newState) {
        const pMap = {};
        newState.progress.forEach(p => { pMap[p.question_seq] = p; });
        setProgressMap(pMap);
        setReviews(newState.reviews || []);
        setActivity(newState.activity || []);
      }
    } catch (err) {
      console.error('Failed to save progress, rolling back:', err);
      // Rollback
      setProgressMap(prevProgress);
      setReviews(prevReviews);
      setActivity(prevActivity);
      showToast('Failed to save progress. Changes rolled back.', 'error');
    }
  };

  // Submit Review Action (Recalled, Forgot, Delete, Reschedule)
  const submitReview = async ({ questionSeq, action, dueDate = null }) => {
    if (!user) return;

    const prevProgress = { ...progressMap };
    const prevReviews = [...reviews];

    // Optimistic calculation
    const today = new Date();
    const todayStr = today.toISOString().split('T')[0];

    if (action === 'delete') {
      setReviews(prev => prev.filter(r => r.question_seq !== questionSeq));
    } else if (action === 'recalled') {
      setReviews(prev => {
        const rev = prev.find(r => r.question_seq === questionSeq);
        if (!rev) return prev;
        if (rev.step >= 3) {
          return prev.filter(r => r.question_seq !== questionSeq);
        }
        const nextStep = rev.step + 1;
        const intervals = [1, 3, 7, 21];
        const days = intervals[nextStep] || 21;
        const nextDate = new Date();
        nextDate.setDate(nextDate.getDate() + days);
        return prev.map(r => r.question_seq === questionSeq ? {
          ...r,
          step: nextStep,
          due_date: nextDate.toISOString().split('T')[0]
        } : r);
      });
    } else if (action === 'forgot') {
      const tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);
      const tomStr = tomorrow.toISOString().split('T')[0];

      setReviews(prev => {
        const exists = prev.some(r => r.question_seq === questionSeq);
        if (exists) {
          return prev.map(r => r.question_seq === questionSeq ? {
            ...r,
            step: 0,
            due_date: tomStr
          } : r);
        } else {
          return [...prev, { question_seq: questionSeq, due_date: tomStr, step: 0, source: 'auto' }];
        }
      });

      // Mark mistake in progressMap
      setProgressMap(prev => {
        const curr = prev[questionSeq] || { question_seq: questionSeq, status: 'todo', notes: '' };
        return {
          ...prev,
          [questionSeq]: { ...curr, mistake: true }
        };
      });
    }

    try {
      const newState = await api.saveReview(user.username, pinHash, { questionSeq, action, dueDate });
      if (newState) {
        const pMap = {};
        newState.progress.forEach(p => { pMap[p.question_seq] = p; });
        setProgressMap(pMap);
        setReviews(newState.reviews || []);
      }
    } catch (err) {
      console.error('Failed to save review:', err);
      setProgressMap(prevProgress);
      setReviews(prevReviews);
      showToast('Failed to save review action. Rolled back.', 'error');
    }
  };

  // Update Settings
  const updateSettings = async ({ dailyGoal, language, theme }) => {
    if (!user) return;
    try {
      const updated = await api.saveSettings(user.username, pinHash, { dailyGoal, language, theme });
      const newUser = { ...user, ...updated };
      setUser(newUser);
      localStorage.setItem('dsa_session_user', JSON.stringify(newUser));
      if (theme) {
        document.documentElement.setAttribute('data-theme', theme);
      }
      showToast('Settings saved successfully!');
    } catch (err) {
      showToast('Failed to save settings: ' + err.message, 'error');
    }
  };

  const showToast = (message, type = 'info') => {
    setToast({ message, type });
    setTimeout(() => {
      setToast(null);
    }, 3500);
  };

  // Calculate Streak (SRS 7.3)
  const streak = useMemo(() => {
    if (!activity || activity.length === 0) return 0;
    const actMap = {};
    activity.forEach(a => {
      if (a.solved_count >= 1) actMap[a.day] = true;
    });

    const today = new Date();
    const todayStr = today.toISOString().split('T')[0];

    // Check if solved today or yesterday
    let checkDate = new Date();
    if (!actMap[todayStr]) {
      // Check yesterday
      checkDate.setDate(checkDate.getDate() - 1);
      const yestStr = checkDate.toISOString().split('T')[0];
      if (!actMap[yestStr]) return 0;
    }

    let count = 0;
    while (true) {
      const dStr = checkDate.toISOString().split('T')[0];
      if (actMap[dStr]) {
        count++;
        checkDate.setDate(checkDate.getDate() - 1);
      } else {
        break;
      }
    }
    return count;
  }, [activity]);

  // Today Solved Count
  const todaySolvedCount = useMemo(() => {
    const todayStr = new Date().toISOString().split('T')[0];
    const rec = activity.find(a => a.day === todayStr);
    return rec ? rec.solved_count : 0;
  }, [activity]);

  // Calculate Next Up (SRS 7.4)
  const getNextUp = useCallback((chapterFilter = null) => {
    if (!questions || questions.length === 0) return null;
    const todayStr = new Date().toISOString().split('T')[0];

    // Map future manual reviews
    const futureManualReviews = new Set();
    reviews.forEach(r => {
      if (r.source === 'manual' && r.due_date > todayStr) {
        futureManualReviews.add(r.question_seq);
      }
    });

    const isAvailable = (q) => {
      const p = progressMap[q.seq];
      const status = p ? p.status : 'todo';
      const isUnfinished = status === 'todo' || status === 'in_progress';
      const hasFutureManual = futureManualReviews.has(q.seq);
      return isUnfinished && !hasFutureManual;
    };

    if (chapterFilter) {
      const inChapter = questions.filter(q => q.chapter === chapterFilter && isAvailable(q));
      if (inChapter.length > 0) return inChapter[0];
    }

    const nextOverall = questions.find(isAvailable);
    return nextOverall || null;
  }, [questions, progressMap, reviews]);

  // Due Reviews (due_date <= today), mistake reviews first
  const dueReviews = useMemo(() => {
    const todayStr = new Date().toISOString().split('T')[0];
    const due = reviews.filter(r => r.due_date <= todayStr);
    return due.sort((a, b) => {
      const aMistake = progressMap[a.question_seq]?.mistake ? 1 : 0;
      const bMistake = progressMap[b.question_seq]?.mistake ? 1 : 0;
      if (bMistake !== aMistake) return bMistake - aMistake; // mistake first
      return a.question_seq - b.question_seq;
    });
  }, [reviews, progressMap]);

  // Upcoming Reviews (next 7 days)
  const upcomingReviews = useMemo(() => {
    const today = new Date();
    const todayStr = today.toISOString().split('T')[0];
    const nextWeek = new Date();
    nextWeek.setDate(nextWeek.getDate() + 7);
    const nextWeekStr = nextWeek.toISOString().split('T')[0];

    return reviews
      .filter(r => r.due_date > todayStr && r.due_date <= nextWeekStr)
      .sort((a, b) => a.due_date.localeCompare(b.due_date));
  }, [reviews]);

  // Export / Import
  const exportData = () => {
    const data = {
      version: "1.0",
      exported_at: new Date().toISOString(),
      user: {
        username: user?.username,
        daily_goal: user?.daily_goal,
        language: user?.language,
        theme: user?.theme
      },
      progress: Object.values(progressMap),
      reviews: reviews,
      activity: activity
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `dsa-tracker-${user?.username || 'export'}-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const importData = async (jsonString) => {
    try {
      const parsed = JSON.parse(jsonString);
      if (!parsed.progress || !Array.isArray(parsed.progress)) {
        throw new Error('Invalid backup file format');
      }

      // Merge into local state
      const newPMap = { ...progressMap };
      parsed.progress.forEach(p => {
        if (p.question_seq >= 1 && p.question_seq <= 300) {
          newPMap[p.question_seq] = p;
        }
      });
      setProgressMap(newPMap);
      if (Array.isArray(parsed.reviews)) setReviews(parsed.reviews);
      if (Array.isArray(parsed.activity)) setActivity(parsed.activity);

      if (user) {
        // save to storage
        const local = {
          user: user,
          progress: Object.values(newPMap),
          reviews: parsed.reviews || reviews,
          activity: parsed.activity || activity
        };
        localStorage.setItem(`dsa_tracker_${user.username.toLowerCase()}`, JSON.stringify(local));
      }
      showToast('Progress imported successfully!');
    } catch (err) {
      showToast('Failed to import backup: ' + err.message, 'error');
    }
  };

  const value = {
    loadingData,
    questions,
    chapters,
    user,
    pinHash,
    isLoggedIn: !!user,
    login,
    logout,
    deleteAccount,
    progressMap,
    reviews,
    activity,
    updateProgress,
    submitReview,
    updateSettings,
    streak,
    todaySolvedCount,
    getNextUp,
    dueReviews,
    upcomingReviews,
    exportData,
    importData,
    toast,
    showToast
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useApp() {
  const context = useContext(AppContext);
  if (!context) throw new Error('useApp must be used within an AppProvider');
  return context;
}


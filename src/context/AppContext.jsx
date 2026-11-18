import React, { createContext, useContext, useState, useEffect, useMemo, useCallback } from 'react';
import { api, getNextReviewDate, getFriendlyErrorMessage } from '../services/api';
import { FEATURES } from '../config/features';

const AppContext = createContext(null);

export function AppProvider({ children }) {
  const [questions, setQuestions] = useState([]);
  const [chapters, setChapters] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [loadingData, setLoadingData] = useState(true);

  // User session
  const [user, setUser] = useState(() => {
    try {
      const saved = localStorage.getItem('chainline_session_user');
      return saved ? JSON.parse(saved) : null;
    } catch (_) {
      return null;
    }
  });

  const [pinHash, setPinHash] = useState(() => {
    return localStorage.getItem('chainline_session_pin_hash') || null;
  });

  // Theme state: 'light', 'evening', 'dark' (URL param > user profile > localStorage > 'light')
  const [theme, setTheme] = useState(() => {
    try {
      const params = new URLSearchParams(window.location.search);
      const urlTheme = params.get('theme');
      if (urlTheme && ['light', 'evening', 'dark'].includes(urlTheme)) return urlTheme;
    } catch (_) { }
    if (user?.theme) return user.theme;
    const saved = localStorage.getItem('chainline_theme');
    return saved || 'light';
  });

  // Language state: 'java' or 'python' (URL param > user profile > localStorage > 'java')
  const [language, setLanguage] = useState(() => {
    try {
      const params = new URLSearchParams(window.location.search);
      const urlLang = params.get('lang');
      if (urlLang && ['java', 'python'].includes(urlLang)) return urlLang;
    } catch (_) { }
    if (user?.language) return user.language;
    return localStorage.getItem('chainline_language') || 'java';
  });

  // Apply theme to root DOM element
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('chainline_theme', theme);
  }, [theme]);

  // Keep language in localStorage
  useEffect(() => {
    localStorage.setItem('chainline_language', language);
  }, [language]);

  // State maps
  const [progressMap, setProgressMap] = useState({});
  const [reviews, setReviews] = useState([]);
  const [activity, setActivity] = useState([]);
  const [toast, setToast] = useState(null);

  // SRS 3.0: Stats and Interview Plan
  const [statsMap, setStatsMap] = useState(() => {
    try {
      const saved = localStorage.getItem('chainline_guest_stats');
      return saved ? JSON.parse(saved) : {};
    } catch (_) {
      return {};
    }
  });

  const [interviewPlan, setInterviewPlan] = useState(() => {
    try {
      const saved = localStorage.getItem('chainline_guest_interview');
      return saved ? JSON.parse(saved) : { date: null, company: null };
    } catch (_) {
      return { date: null, company: null };
    }
  });

  // Load static questions, chapters and companies
  useEffect(() => {
    async function loadStaticData() {
      try {
        const [chRes, qRes, compRes] = await Promise.all([
          fetch('/data/chapters.json'),
          fetch('/data/questions.json'),
          fetch('/data/companies.json').catch(() => null)
        ]);
        const chData = await chRes.json();
        const qData = await qRes.json();
        let compData = { companies: [] };
        if (compRes && compRes.ok) {
          try {
            compData = await compRes.json();
          } catch (_) { }
        }

        let finalChapters = chData;
        let finalQuestions = qData;
        if (!FEATURES.part2Questions) {
          finalChapters = chData.filter(c => c.order <= 18);
          finalQuestions = qData.filter(q => q.seq <= 300);
        }

        setChapters(finalChapters);
        setQuestions(finalQuestions);
        setCompanies(compData?.companies || []);
      } catch (err) {
        console.error('Failed to load static question/chapter/company data:', err);
      } finally {
        setLoadingData(false);
      }
    }
    loadStaticData();
  }, []);

  // Sync state directly from Supabase
  const syncUserState = useCallback(async (username, hash) => {
    if (!username) return;
    try {
      const [state, extras] = await Promise.all([
        api.getState(username, hash),
        api.getExtras(username, hash).catch(err => {
          console.warn('Failed to load extras:', err.message);
          return null;
        })
      ]);

      const pMap = {};
      if (Array.isArray(state?.progress)) {
        state.progress.forEach(p => { pMap[p.question_seq] = p; });
      }
      setProgressMap(pMap);
      setReviews(state?.reviews || []);
      setActivity(state?.activity || []);

      if (extras) {
        if (extras.interview_date !== undefined || extras.interview_company !== undefined) {
          setInterviewPlan({
            date: extras.interview_date || null,
            company: extras.interview_company || null
          });
        }
        if (Array.isArray(extras.stats)) {
          const sMap = {};
          extras.stats.forEach(s => {
            sMap[s.question_seq] = {
              seconds: s.seconds || 0,
              attempts: s.attempts || 0,
              forgotCount: s.forgot_count || 0,
              slow: Boolean(s.slow),
              lastAt: s.last_at || null
            };
          });
          setStatsMap(sMap);
        }
      }
    } catch (err) {
      console.warn('Failed to sync user state from Supabase:', err.message);
    }
  }, []);

  useEffect(() => {
    if (user && user.username) {
      syncUserState(user.username, pinHash);
    }
  }, [user?.username, pinHash, syncUserState]);

  // Handle Login (Section 5.2 & FR-1)
  const login = async (username, pin) => {
    try {
      const res = await api.login(username, pin);
      setUser(res.user);
      setPinHash(res.pinHash);
      localStorage.setItem('chainline_session_user', JSON.stringify(res.user));
      if (res.pinHash) {
        localStorage.setItem('chainline_session_pin_hash', res.pinHash);
      } else {
        localStorage.removeItem('chainline_session_pin_hash');
      }

      if (res.user.theme) {
        setTheme(res.user.theme);
      }
      if (res.user.language) {
        setLanguage(res.user.language);
        localStorage.setItem('chainline_language', res.user.language);
      }

      const pMap = {};
      if (res.state && Array.isArray(res.state.progress)) {
        res.state.progress.forEach(p => { pMap[p.question_seq] = p; });
      }
      setProgressMap(pMap);
      setReviews(res.state?.reviews || []);
      setActivity(res.state?.activity || []);
      syncUserState(res.user.username, res.pinHash);
      return res.user;
    } catch (err) {
      throw err;
    }
  };

  // Handle Register (Section 5.2 & FR-1a)
  const register = async ({ username, displayName, pin, dailyGoal, language, theme: chosenTheme }) => {
    try {
      const selectedTheme = chosenTheme || theme || 'light';
      const res = await api.register(username, displayName, pin, dailyGoal, language, selectedTheme);
      setUser(res.user);
      setPinHash(res.pinHash);
      localStorage.setItem('chainline_session_user', JSON.stringify(res.user));
      if (res.pinHash) {
        localStorage.setItem('chainline_session_pin_hash', res.pinHash);
      } else {
        localStorage.removeItem('chainline_session_pin_hash');
      }

      setTheme(selectedTheme);
      setLanguage(language || 'java');
      localStorage.setItem('chainline_language', language || 'java');
      setProgressMap({});
      setReviews([]);
      setActivity([]);
      setStatsMap({});
      setInterviewPlan({ date: null, company: null });
      return res.user;
    } catch (err) {
      throw err;
    }
  };

  // Handle Logout
  const logout = () => {
    setUser(null);
    setPinHash(null);
    setProgressMap({});
    setReviews([]);
    setActivity([]);
    setStatsMap({});
    setInterviewPlan({ date: null, company: null });
    localStorage.removeItem('chainline_session_user');
    localStorage.removeItem('chainline_session_pin_hash');
  };

  // Delete User Account (Section 7.2 & Acceptance #14)
  const deleteAccount = async () => {
    if (!user) return;
    try {
      await api.deleteUser({ username: user.username, pinHash });
      logout();
      showToast('Account and all progress successfully deleted.', 'info');
    } catch (err) {
      showToast('Failed to delete account: ' + err.message, 'error');
    }
  };

  // Update Progress (FR-35, Section 7.2)
  const updateProgress = async ({ questionSeq, status, mistake, notes, remind = true, dueDate = null }) => {
    const prevProgress = { ...progressMap };
    const prevReviews = [...reviews];
    const prevActivity = [...activity];

    const todayStr = new Date().toISOString().split('T')[0];
    const existing = progressMap[questionSeq];
    const wasAlreadyDone = existing && existing.status === 'done';

    const updatedItem = {
      question_seq: questionSeq,
      status: status,
      mistake: mistake !== undefined ? mistake : (existing?.mistake || false),
      notes: notes !== undefined ? notes : (existing?.notes || ''),
      solved_at: status === 'done' ? (existing?.solved_at || new Date().toISOString()) : existing?.solved_at,
      updated_at: new Date().toISOString()
    };

    setProgressMap(prev => ({
      ...prev,
      [questionSeq]: updatedItem
    }));

    if (!user) return;

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
        const tomStr = getNextReviewDate(0);
        setReviews(prev => {
          const filtered = prev.filter(r => r.question_seq !== questionSeq);
          filtered.push({ question_seq: questionSeq, due_date: tomStr, step: 0, source: 'auto' });
          return filtered;
        });
        api.saveReview({
          username: user.username,
          pinHash,
          seq: questionSeq,
          due: tomStr,
          step: 0,
          source: 'auto'
        });
      }
    } else if (status === 'revisit') {
      const revDate = dueDate || getNextReviewDate(0);
      setReviews(prev => {
        const filtered = prev.filter(r => r.question_seq !== questionSeq);
        filtered.push({ question_seq: questionSeq, due_date: revDate, step: 0, source: 'manual' });
        return filtered;
      });
      api.saveReview({
        username: user.username,
        pinHash,
        seq: questionSeq,
        due: revDate,
        step: 0,
        source: 'manual'
      });
    }

    try {
      await api.saveProgress({
        username: user.username,
        pinHash,
        seq: questionSeq,
        status,
        mistake: updatedItem.mistake,
        notes: updatedItem.notes,
        day: todayStr
      });
    } catch (err) {
      console.error('Failed to save progress, rolling back:', err);
      setProgressMap(prevProgress);
      setReviews(prevReviews);
      setActivity(prevActivity);
      showToast('Failed to save progress. Changes rolled back.', 'error');
    }
  };

  // Submit Review Action (Section 5.6: Recalled or Forgot)
  const submitReview = async ({ questionSeq, action, dueDate = null }) => {
    if (!user) return;

    const prevProgress = { ...progressMap };
    const prevReviews = [...reviews];

    if (action === 'delete') {
      setReviews(prev => prev.filter(r => r.question_seq !== questionSeq));
      try {
        await api.deleteReview({ username: user.username, pinHash, seq: questionSeq });
      } catch (err) {
        console.error('Failed to delete review:', err);
      }
      return;
    }

    if (action === 'recalled') {
      const rev = reviews.find(r => r.question_seq === questionSeq);
      if (!rev) return;

      if (rev.step >= 3) {
        // Step 4 finished (completed 21-day review)
        setReviews(prev => prev.filter(r => r.question_seq !== questionSeq));
        try {
          await api.deleteReview({ username: user.username, pinHash, seq: questionSeq });
          showToast(`Problem #${questionSeq} master review completed!`, 'info');
        } catch (err) {
          console.error(err);
        }
        return;
      }

      const nextStep = rev.step + 1;
      const nextDue = getNextReviewDate(nextStep);
      setReviews(prev => prev.map(r => r.question_seq === questionSeq ? {
        ...r,
        step: nextStep,
        due_date: nextDue
      } : r));

      try {
        await api.saveReview({
          username: user.username,
          pinHash,
          seq: questionSeq,
          due: nextDue,
          step: nextStep,
          source: rev.source || 'auto'
        });
        showToast(`Next review scheduled for ${nextDue}`, 'info');
      } catch (err) {
        console.error(err);
      }
    } else if (action === 'forgot') {
      const tomStr = getNextReviewDate(0);
      setReviews(prev => {
        const filtered = prev.filter(r => r.question_seq !== questionSeq);
        filtered.push({ question_seq: questionSeq, due_date: tomStr, step: 0, source: 'auto' });
        return filtered;
      });

      // Mark mistake
      setProgressMap(prev => {
        const curr = prev[questionSeq] || { question_seq: questionSeq, status: 'todo', notes: '' };
        return {
          ...prev,
          [questionSeq]: { ...curr, mistake: true }
        };
      });

      try {
        await Promise.all([
          api.saveReview({
            username: user.username,
            pinHash,
            seq: questionSeq,
            due: tomStr,
            step: 0,
            source: 'auto'
          }),
          api.saveProgress({
            username: user.username,
            pinHash,
            seq: questionSeq,
            status: progressMap[questionSeq]?.status || 'todo',
            mistake: true,
            notes: progressMap[questionSeq]?.notes || '',
            day: new Date().toISOString().split('T')[0]
          })
        ]);
        // SRS 3.0 Section 9.3: save_stats is called in addition with p_forgot set to true
        saveQuestionStats(questionSeq, { forgot: true });
        showToast(`Reset to Step 1: due tomorrow. Flagged as mistake.`, 'info');
      } catch (err) {
        console.error(err);
      }
    }
  };

  // Update preferred code language ('java' | 'python') across the entire app
  const updateLanguage = useCallback(async (newLang) => {
    if (newLang !== 'java' && newLang !== 'python') return;
    setLanguage(newLang);
    localStorage.setItem('chainline_language', newLang);

    if (user) {
      const updatedUser = { ...user, language: newLang };
      setUser(updatedUser);
      localStorage.setItem('chainline_session_user', JSON.stringify(updatedUser));
      try {
        await api.saveSettings({
          username: user.username,
          pinHash,
          displayName: user.display_name,
          dailyGoal: user.daily_goal,
          language: newLang,
          theme: user.theme || theme
        });
      } catch (err) {
        console.error('Failed to sync language to server:', err);
      }
    }
  }, [user, pinHash, theme]);

  // Update Settings (FR-26, Section 5.7)
  const updateSettings = async ({ displayName, dailyGoal, language: newLang, theme: newTheme }) => {
    if (newTheme) {
      setTheme(newTheme);
      localStorage.setItem('chainline_theme', newTheme);
    }
    if (newLang) {
      setLanguage(newLang);
      localStorage.setItem('chainline_language', newLang);
    }

    if (!user) {
      return;
    }

    const updatedUser = {
      ...user,
      display_name: displayName !== undefined ? displayName : user.display_name,
      daily_goal: dailyGoal !== undefined ? dailyGoal : user.daily_goal,
      language: newLang !== undefined ? newLang : (user.language || language),
      theme: newTheme !== undefined ? newTheme : (user.theme || theme)
    };

    setUser(updatedUser);
    localStorage.setItem('chainline_session_user', JSON.stringify(updatedUser));

    try {
      await api.saveSettings({
        username: user.username,
        pinHash,
        displayName: updatedUser.display_name,
        dailyGoal: updatedUser.daily_goal,
        language: updatedUser.language,
        theme: updatedUser.theme
      });
      showToast('Settings saved successfully!');
    } catch (err) {
      showToast('Failed to save settings to server: ' + err.message, 'error');
    }
  };

  const showToast = (message, type = 'info') => {
    setToast({ message, type });
    setTimeout(() => {
      setToast(null);
    }, 3200);
  };

  // Calculate Streak
  const streak = useMemo(() => {
    if (!activity || activity.length === 0) return 0;
    const actMap = {};
    activity.forEach(a => {
      if (a.solved_count >= 1) actMap[a.day] = true;
    });

    const todayStr = new Date().toISOString().split('T')[0];
    let checkDate = new Date();
    if (!actMap[todayStr]) {
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

  // Today solved count
  const todaySolvedCount = useMemo(() => {
    const todayStr = new Date().toISOString().split('T')[0];
    const rec = activity.find(a => a.day === todayStr);
    return rec ? rec.solved_count : 0;
  }, [activity]);

  // Due and upcoming reviews
  const todayStr = new Date().toISOString().split('T')[0];

  const dueReviews = useMemo(() => {
    return reviews.filter(r => r.due_date <= todayStr);
  }, [reviews, todayStr]);

  const upcomingReviews = useMemo(() => {
    const nextWeek = new Date();
    nextWeek.setDate(nextWeek.getDate() + 7);
    const nextWeekStr = nextWeek.toISOString().split('T')[0];
    return reviews.filter(r => r.due_date > todayStr && r.due_date <= nextWeekStr);
  }, [reviews, todayStr]);

  // Next Up algorithm
  const getNextUp = useCallback(() => {
    if (!questions || questions.length === 0) return null;
    for (let i = 0; i < questions.length; i++) {
      const q = questions[i];
      const p = progressMap[q.seq];
      if (!p || p.status === 'todo' || p.status === 'in_progress') {
        return q;
      }
    }
    return null;
  }, [questions, progressMap]);

  // SRS 3.0: Save question stats
  const saveQuestionStats = useCallback(async (seq, { addSeconds = 0, newAttempt = false, forgot = false, slow = false } = {}) => {
    const qSeq = Number(seq);
    setStatsMap(prev => {
      const existing = prev[qSeq] || { seconds: 0, attempts: 0, forgotCount: 0, slow: false };
      const updated = {
        seconds: (existing.seconds || 0) + (Number(addSeconds) || 0),
        attempts: (existing.attempts || 0) + (newAttempt ? 1 : 0),
        forgotCount: (existing.forgotCount || 0) + (forgot ? 1 : 0),
        slow: existing.slow || Boolean(slow),
        lastAt: new Date().toISOString()
      };
      const nextMap = { ...prev, [qSeq]: updated };
      if (!user) {
        try {
          localStorage.setItem('chainline_guest_stats', JSON.stringify(nextMap));
        } catch (_) { }
      }
      return nextMap;
    });

    if (user && user.username) {
      try {
        await api.saveStats({
          username: user.username,
          pinHash,
          seq: qSeq,
          addSeconds,
          newAttempt,
          forgot,
          slow
        });
      } catch (err) {
        console.warn('Failed to sync stats to server:', err.message);
      }
    }
  }, [user, pinHash]);

  // SRS 3.0: Interview date & company plan
  const updateInterviewPlan = useCallback(async (date, company) => {
    const plan = { date: date || null, company: company ? company.trim() : null };
    setInterviewPlan(plan);
    if (!user) {
      try {
        localStorage.setItem('chainline_guest_interview', JSON.stringify(plan));
      } catch (_) { }
    } else {
      try {
        await api.saveInterview({
          username: user.username,
          pinHash,
          date: plan.date,
          company: plan.company
        });
      } catch (err) {
        console.warn('Failed to save interview plan to server:', err.message);
      }
    }
  }, [user, pinHash]);

  const clearInterviewPlan = useCallback(async () => {
    await updateInterviewPlan(null, null);
  }, [updateInterviewPlan]);

  // Export & Import progress
  const exportData = () => {
    const data = {
      version: 3,
      user: {
        username: user?.username,
        display_name: user?.display_name,
        daily_goal: user?.daily_goal,
        language: user?.language,
        theme: user?.theme
      },
      progress: Object.values(progressMap),
      reviews,
      activity,
      stats: Object.entries(statsMap).map(([seq, s]) => ({ question_seq: Number(seq), ...s })),
      interview: interviewPlan,
      exported_at: new Date().toISOString()
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `chainline-${user?.username || 'progress'}-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
    showToast('Progress exported to JSON file', 'info');
  };

  const importData = (jsonStr) => {
    try {
      const parsed = JSON.parse(jsonStr);
      if (parsed.progress && Array.isArray(parsed.progress)) {
        const pMap = {};
        parsed.progress.forEach(p => { pMap[p.question_seq] = p; });
        setProgressMap(pMap);
      }
      if (parsed.reviews && Array.isArray(parsed.reviews)) {
        setReviews(parsed.reviews);
      }
      if (parsed.activity && Array.isArray(parsed.activity)) {
        setActivity(parsed.activity);
      }
      if (parsed.stats && Array.isArray(parsed.stats)) {
        const sMap = {};
        parsed.stats.forEach(s => {
          sMap[s.question_seq] = {
            seconds: s.seconds || 0,
            attempts: s.attempts || 0,
            forgotCount: s.forgotCount || s.forgot_count || 0,
            slow: Boolean(s.slow),
            lastAt: s.lastAt || s.last_at || null
          };
        });
        setStatsMap(sMap);
      }
      if (parsed.interview && typeof parsed.interview === 'object') {
        setInterviewPlan({
          date: parsed.interview.date || null,
          company: parsed.interview.company || null
        });
      }
      showToast('Progress imported successfully', 'info');
    } catch (e) {
      showToast('Failed to import JSON: invalid format', 'error');
    }
  };

  const value = {
    questions,
    chapters,
    companies,
    loadingData,
    user,
    pinHash,
    theme,
    setTheme,
    language,
    setLanguage: updateLanguage,
    updateLanguage,
    progressMap,
    reviews,
    activity,
    streak,
    todaySolvedCount,
    dueReviews,
    upcomingReviews,
    statsMap,
    interviewPlan,
    saveQuestionStats,
    updateInterviewPlan,
    clearInterviewPlan,
    toast,
    showToast,
    login,
    register,
    logout,
    deleteAccount,
    updateProgress,
    submitReview,
    updateSettings,
    getNextUp,
    exportData,
    importData
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
}

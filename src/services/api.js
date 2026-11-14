// API service for DSA Roadmap Tracker
// Supports Supabase RPC calls with automatic fallback to localStorage

const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || '';
const SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || '';

// Compute SHA-256 of username + pin
export async function computePinHash(username, pin) {
  if (!pin) return null;
  const msg = `${username.toLowerCase()}:${pin}`;
  const msgUint8 = new TextEncoder().encode(msg);
  const hashBuffer = await crypto.subtle.digest('SHA-256', msgUint8);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

// Local storage fallback helpers
const LOCAL_STORAGE_KEY_PREFIX = 'dsa_tracker_';

function getLocalKey(username) {
  return `${LOCAL_STORAGE_KEY_PREFIX}${username.toLowerCase()}`;
}

function getLocalData(username) {
  const raw = localStorage.getItem(getLocalKey(username));
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch (e) {
    return null;
  }
}

function saveLocalData(username, data) {
  localStorage.setItem(getLocalKey(username), JSON.stringify(data));
}

// Call Supabase RPC endpoint
async function callRpc(functionName, params) {
  if (!SUPABASE_URL || !SUPABASE_ANON_KEY) {
    throw new Error('Supabase not configured');
  }

  const response = await fetch(`${SUPABASE_URL}/rest/v1/rpc/${functionName}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'apikey': SUPABASE_ANON_KEY,
      'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
      'Prefer': 'return=representation'
    },
    body: JSON.stringify(params)
  });

  if (!response.ok) {
    const errorBody = await response.text();
    let msg = `RPC Error (${response.status})`;
    try {
      const errJson = JSON.parse(errorBody);
      msg = errJson.message || msg;
    } catch (_) {}
    throw new Error(msg);
  }

  return await response.json();
}

// Spaced repetition interval helper
// Intervals: 1, 3, 7, 21 days
export function getNextReviewDate(currentStep, fromDate = new Date()) {
  const intervals = [1, 3, 7, 21];
  const days = intervals[Math.min(currentStep, intervals.length - 1)];
  const next = new Date(fromDate);
  next.setDate(next.getDate() + days);
  return next.toISOString().split('T')[0];
}

export const api = {
  // Login or create user
  async login(username, pin) {
    const cleanUser = username.trim().toLowerCase();
    if (!/^[a-z0-9_]{3,20}$/.test(cleanUser)) {
      throw new Error('Username must be 3-20 characters (a-z, 0-9, and underscore).');
    }

    const pinHash = pin ? await computePinHash(cleanUser, pin) : null;

    if (SUPABASE_URL && SUPABASE_ANON_KEY) {
      try {
        const user = await callRpc('login_user', {
          p_username: cleanUser,
          p_pin_hash: pinHash
        });
        const state = await callRpc('get_state', {
          p_username: cleanUser,
          p_pin_hash: pinHash
        });
        return { user, state, pinHash };
      } catch (err) {
        console.warn('Supabase login failed, trying local storage:', err.message);
        // If it was an invalid PIN error from database, bubble it up!
        if (err.message.includes('Invalid PIN')) throw err;
      }
    }

    // Offline / LocalStorage mode
    let localData = getLocalData(cleanUser);
    if (!localData) {
      localData = {
        user: {
          id: crypto.randomUUID ? crypto.randomUUID() : 'local-' + Date.now(),
          username: cleanUser,
          pin_hash: pinHash,
          has_pin: !!pinHash,
          daily_goal: 2,
          language: 'java',
          theme: 'dark'
        },
        progress: [],
        reviews: [],
        activity: []
      };
      saveLocalData(cleanUser, localData);
    } else {
      if (localData.user.pin_hash && localData.user.pin_hash !== pinHash) {
        throw new Error('Invalid PIN for this username.');
      }
      if (!localData.user.pin_hash && pinHash) {
        localData.user.pin_hash = pinHash;
        localData.user.has_pin = true;
        saveLocalData(cleanUser, localData);
      }
    }

    return {
      user: localData.user,
      state: {
        user: localData.user,
        progress: localData.progress,
        reviews: localData.reviews,
        activity: localData.activity
      },
      pinHash
    };
  },

  // Get full state
  async getState(username, pinHash) {
    const cleanUser = username.trim().toLowerCase();
    if (SUPABASE_URL && SUPABASE_ANON_KEY) {
      try {
        return await callRpc('get_state', {
          p_username: cleanUser,
          p_pin_hash: pinHash
        });
      } catch (e) {
        console.warn('Supabase getState failed:', e.message);
      }
    }

    const localData = getLocalData(cleanUser);
    if (!localData) throw new Error('User not found');
    return {
      user: localData.user,
      progress: localData.progress || [],
      reviews: localData.reviews || [],
      activity: localData.activity || []
    };
  },

  // Save question progress
  async saveProgress(username, pinHash, { questionSeq, status, mistake, notes, remind = true, dueDate = null }) {
    const cleanUser = username.trim().toLowerCase();
    if (SUPABASE_URL && SUPABASE_ANON_KEY) {
      try {
        return await callRpc('save_progress', {
          p_username: cleanUser,
          p_pin_hash: pinHash,
          p_question_seq: questionSeq,
          p_status: status,
          p_mistake: !!mistake,
          p_notes: notes || '',
          p_remind: remind,
          p_due_date: dueDate
        });
      } catch (e) {
        console.warn('Supabase saveProgress failed, applying locally:', e.message);
      }
    }

    // Local Storage Fallback
    const local = getLocalData(cleanUser) || {
      user: { username: cleanUser, daily_goal: 2, language: 'java', theme: 'dark' },
      progress: [],
      reviews: [],
      activity: []
    };

    const todayStr = new Date().toISOString().split('T')[0];
    const nowIso = new Date().toISOString();

    let progItem = local.progress.find(p => p.question_seq === questionSeq);
    const wasAlreadyDone = progItem && progItem.status === 'done';

    if (!progItem) {
      progItem = {
        question_seq: questionSeq,
        status: status,
        mistake: !!mistake,
        notes: notes || '',
        solved_at: status === 'done' ? nowIso : null,
        updated_at: nowIso
      };
      local.progress.push(progItem);
    } else {
      progItem.status = status;
      progItem.mistake = !!mistake;
      progItem.notes = notes !== undefined ? notes : progItem.notes;
      if (status === 'done' && !progItem.solved_at) {
        progItem.solved_at = nowIso;
      }
      progItem.updated_at = nowIso;
    }

    // Activity record on Done
    if (status === 'done' && !wasAlreadyDone) {
      let act = local.activity.find(a => a.day === todayStr);
      if (!act) {
        local.activity.push({ day: todayStr, solved_count: 1 });
      } else {
        act.solved_count += 1;
      }

      // Spaced repetition review scheduling
      if (remind) {
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        const tomStr = tomorrow.toISOString().split('T')[0];
        
        let rev = local.reviews.find(r => r.question_seq === questionSeq);
        if (!rev) {
          local.reviews.push({
            question_seq: questionSeq,
            due_date: tomStr,
            step: 0,
            source: 'auto'
          });
        } else {
          rev.due_date = tomStr;
          rev.step = 0;
          rev.source = 'auto';
        }
      }
    } else if (status === 'revisit') {
      const tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);
      const revDate = dueDate || tomorrow.toISOString().split('T')[0];

      let rev = local.reviews.find(r => r.question_seq === questionSeq);
      if (!rev) {
        local.reviews.push({
          question_seq: questionSeq,
          due_date: revDate,
          step: 0,
          source: 'manual'
        });
      } else {
        rev.due_date = revDate;
        rev.step = 0;
        rev.source = 'manual';
      }
    }

    saveLocalData(cleanUser, local);
    return {
      user: local.user,
      progress: local.progress,
      reviews: local.reviews,
      activity: local.activity
    };
  },

  // Save review response: recalled, forgot, delete, or reschedule
  async saveReview(username, pinHash, { questionSeq, action, dueDate = null }) {
    const cleanUser = username.trim().toLowerCase();
    if (SUPABASE_URL && SUPABASE_ANON_KEY) {
      try {
        return await callRpc('save_review', {
          p_username: cleanUser,
          p_pin_hash: pinHash,
          p_question_seq: questionSeq,
          p_action: action,
          p_due_date: dueDate
        });
      } catch (e) {
        console.warn('Supabase saveReview failed:', e.message);
      }
    }

    // Local Storage logic for Review
    const local = getLocalData(cleanUser);
    if (!local) throw new Error('User not found');

    const revIdx = local.reviews.findIndex(r => r.question_seq === questionSeq);
    const today = new Date();
    const todayStr = today.toISOString().split('T')[0];

    if (action === 'delete') {
      if (revIdx >= 0) local.reviews.splice(revIdx, 1);
    } else if (action === 'recalled') {
      if (revIdx >= 0) {
        const rev = local.reviews[revIdx];
        if (rev.step >= 3) {
          local.reviews.splice(revIdx, 1);
        } else {
          const nextStep = rev.step + 1;
          const intervals = [1, 3, 7, 21];
          const nextDays = intervals[nextStep] || 21;
          const nextDate = new Date();
          nextDate.setDate(nextDate.getDate() + nextDays);

          rev.step = nextStep;
          rev.due_date = nextDate.toISOString().split('T')[0];
        }
      }
    } else if (action === 'forgot') {
      const tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);
      const tomStr = tomorrow.toISOString().split('T')[0];

      if (revIdx >= 0) {
        local.reviews[revIdx].step = 0;
        local.reviews[revIdx].due_date = tomStr;
      } else {
        local.reviews.push({
          question_seq: questionSeq,
          due_date: tomStr,
          step: 0,
          source: 'auto'
        });
      }

      // Mark mistake tag
      let pItem = local.progress.find(p => p.question_seq === questionSeq);
      if (pItem) pItem.mistake = true;
    } else if (action === 'reschedule') {
      const revDate = dueDate || todayStr;
      if (revIdx >= 0) {
        local.reviews[revIdx].due_date = revDate;
        local.reviews[revIdx].step = 0;
        local.reviews[revIdx].source = 'manual';
      } else {
        local.reviews.push({
          question_seq: questionSeq,
          due_date: revDate,
          step: 0,
          source: 'manual'
        });
      }
    }

    saveLocalData(cleanUser, local);
    return {
      user: local.user,
      progress: local.progress,
      reviews: local.reviews,
      activity: local.activity
    };
  },

  // Save Settings
  async saveSettings(username, pinHash, { dailyGoal, language, theme }) {
    const cleanUser = username.trim().toLowerCase();
    if (SUPABASE_URL && SUPABASE_ANON_KEY) {
      try {
        return await callRpc('save_settings', {
          p_username: cleanUser,
          p_pin_hash: pinHash,
          p_daily_goal: dailyGoal,
          p_language: language,
          p_theme: theme
        });
      } catch (e) {
        console.warn('Supabase saveSettings failed:', e.message);
      }
    }

    const local = getLocalData(cleanUser);
    if (!local) throw new Error('User not found');

    if (dailyGoal) local.user.daily_goal = Math.max(1, Math.min(10, dailyGoal));
    if (language) local.user.language = language;
    if (theme) local.user.theme = theme;

    saveLocalData(cleanUser, local);
    return local.user;
  },

  // Delete User
  async deleteUser(username, pinHash) {
    const cleanUser = username.trim().toLowerCase();
    if (SUPABASE_URL && SUPABASE_ANON_KEY) {
      try {
        await callRpc('delete_user', {
          p_username: cleanUser,
          p_pin_hash: pinHash
        });
      } catch (e) {
        console.warn('Supabase deleteUser failed:', e.message);
      }
    }
    localStorage.removeItem(getLocalKey(cleanUser));
    return true;
  }
};


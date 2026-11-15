// Chainline: DSA Roadmap Tracker 2.0 API service
// Implements Supabase RPC client per Section 7 with full local-first offline fallback

const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || '';
const SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || '';

// Compute SHA-256 per Section 7.3:
// "SHA-256, in the browser, of the text username, a colon, the PIN, a colon, and the word chainline."
export async function computePinHash(username, pin) {
  if (!pin) return null;
  const msg = `${username.toLowerCase()}:${pin}:chainline`;
  const msgUint8 = new TextEncoder().encode(msg);
  const hashBuffer = await crypto.subtle.digest('SHA-256', msgUint8);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

// Error code humanizer per Section 7.3
export function getFriendlyErrorMessage(errCodeOrMsg) {
  if (!errCodeOrMsg) return 'An unexpected error occurred.';
  const str = String(errCodeOrMsg);
  if (str.includes('NO_SUCH_USER')) {
    return 'No account with that username. Create one?';
  }
  if (str.includes('PIN_REQUIRED')) {
    return 'PIN_REQUIRED';
  }
  if (str.includes('WRONG_PIN')) {
    return 'That PIN is not right.';
  }
  if (str.includes('USERNAME_TAKEN')) {
    return 'That username is taken.';
  }
  if (str.includes('BAD_USERNAME')) {
    return 'Use 3 to 20 letters, numbers or underscores.';
  }
  return str;
}

// Local storage offline registry
const LOCAL_REGISTRY_KEY = 'chainline_user_registry';
const LOCAL_DATA_PREFIX = 'chainline_data_';

function getLocalRegistry() {
  try {
    const raw = localStorage.getItem(LOCAL_REGISTRY_KEY);
    return raw ? JSON.parse(raw) : {};
  } catch (e) {
    return {};
  }
}

function saveLocalRegistry(registry) {
  localStorage.setItem(LOCAL_REGISTRY_KEY, JSON.stringify(registry));
}

function getUserLocalData(username) {
  try {
    const raw = localStorage.getItem(`${LOCAL_DATA_PREFIX}${username.toLowerCase()}`);
    return raw ? JSON.parse(raw) : { progress: [], reviews: [], activity: [] };
  } catch (e) {
    return { progress: [], reviews: [], activity: [] };
  }
}

function saveUserLocalData(username, data) {
  localStorage.setItem(`${LOCAL_DATA_PREFIX}${username.toLowerCase()}`, JSON.stringify(data));
}

// Call Supabase RPC function
async function callRpc(functionName, params) {
  if (!SUPABASE_URL || !SUPABASE_ANON_KEY) {
    throw new Error('SUPABASE_NOT_CONFIGURED');
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
    let code = `RPC Error (${response.status})`;
    try {
      const errJson = JSON.parse(errorBody);
      code = errJson.message || errJson.details || errJson.hint || code;
    } catch (_) {}
    throw new Error(code);
  }

  return await response.json();
}

// Spaced repetition interval helper: 1, 3, 7, 21 days
export function getNextReviewDate(currentStep, fromDate = new Date()) {
  const intervals = [1, 3, 7, 21];
  const days = intervals[Math.min(currentStep, intervals.length - 1)];
  const next = new Date(fromDate);
  next.setDate(next.getDate() + days);
  return next.toISOString().split('T')[0];
}

export const api = {
  // Sign in (Section 5.2 & FR-1)
  // NEVER creates an account!
  async login(username, pin) {
    const cleanUser = username.trim().toLowerCase();
    if (!/^[a-z0-9_]{3,20}$/.test(cleanUser)) {
      throw new Error('BAD_USERNAME');
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
        if (err.message.includes('NO_SUCH_USER') || err.message.includes('PIN_REQUIRED') || err.message.includes('WRONG_PIN')) {
          throw err;
        }
        console.warn('Supabase offline or failed, trying local storage:', err.message);
      }
    }

    // Local storage fallback
    const registry = getLocalRegistry();
    const existing = registry[cleanUser];
    if (!existing) {
      throw new Error('NO_SUCH_USER');
    }

    if (existing.has_pin) {
      if (!pinHash) {
        throw new Error('PIN_REQUIRED');
      }
      if (existing.pin_hash !== pinHash) {
        throw new Error('WRONG_PIN');
      }
    }

    const state = getUserLocalData(cleanUser);
    const userSafe = { ...existing };
    delete userSafe.pin_hash;
    return { user: userSafe, state, pinHash };
  },

  // Create account (Section 5.2 & FR-1a)
  async register(username, displayName, pin, dailyGoal = 2, language = 'java', theme = 'light') {
    const cleanUser = username.trim().toLowerCase();
    if (!/^[a-z0-9_]{3,20}$/.test(cleanUser)) {
      throw new Error('BAD_USERNAME');
    }

    const pinHash = pin ? await computePinHash(cleanUser, pin) : null;

    if (SUPABASE_URL && SUPABASE_ANON_KEY) {
      try {
        const user = await callRpc('register_user', {
          p_username: cleanUser,
          p_display_name: displayName ? displayName.trim() : null,
          p_pin_hash: pinHash,
          p_daily_goal: dailyGoal,
          p_language: language,
          p_theme: theme
        });
        const state = { progress: [], reviews: [], activity: [] };
        return { user, state, pinHash };
      } catch (err) {
        if (err.message.includes('USERNAME_TAKEN') || err.message.includes('BAD_USERNAME')) {
          throw err;
        }
        console.warn('Supabase offline or failed, falling back to local storage:', err.message);
      }
    }

    // Local storage fallback
    const registry = getLocalRegistry();
    if (registry[cleanUser]) {
      throw new Error('USERNAME_TAKEN');
    }

    const newUser = {
      username: cleanUser,
      display_name: displayName ? displayName.trim() : null,
      daily_goal: dailyGoal,
      language: language,
      theme: theme,
      has_pin: Boolean(pinHash),
      pin_hash: pinHash,
      created_at: new Date().toISOString()
    };

    registry[cleanUser] = newUser;
    saveLocalRegistry(registry);
    saveUserLocalData(cleanUser, { progress: [], reviews: [], activity: [] });

    const userSafe = { ...newUser };
    delete userSafe.pin_hash;
    return { user: userSafe, state: { progress: [], reviews: [], activity: [] }, pinHash };
  },

  // Save question progress (FR-35, Section 7.2)
  async saveProgress({ username, pinHash, seq, status, mistake, notes, day }) {
    const cleanUser = username.toLowerCase();
    const todayStr = day || new Date().toISOString().split('T')[0];

    if (SUPABASE_URL && SUPABASE_ANON_KEY) {
      try {
        return await callRpc('save_progress', {
          p_username: cleanUser,
          p_pin_hash: pinHash,
          p_seq: seq,
          p_status: status,
          p_mistake: Boolean(mistake),
          p_notes: notes || '',
          p_day: todayStr
        });
      } catch (err) {
        console.warn('Supabase save_progress failed, saving locally:', err.message);
      }
    }

    // Local fallback
    const data = getUserLocalData(cleanUser);
    const existingIdx = data.progress.findIndex(p => p.question_seq === seq);
    const wasAlreadyDone = existingIdx >= 0 && data.progress[existingIdx].status === 'done';

    const updatedItem = {
      question_seq: seq,
      status: status,
      mistake: Boolean(mistake),
      notes: notes || '',
      solved_at: status === 'done' ? new Date().toISOString() : null,
      updated_at: new Date().toISOString()
    };

    if (existingIdx >= 0) {
      data.progress[existingIdx] = updatedItem;
    } else {
      data.progress.push(updatedItem);
    }

    // Update activity if transitioned to done for the first time
    if (status === 'done' && !wasAlreadyDone) {
      const actIdx = data.activity.findIndex(a => a.day === todayStr);
      if (actIdx >= 0) {
        data.activity[actIdx].solved_count += 1;
      } else {
        data.activity.push({ day: todayStr, solved_count: 1 });
      }
    }

    saveUserLocalData(cleanUser, data);
    return { ok: true };
  },

  // Save review schedule item (Section 7.2)
  async saveReview({ username, pinHash, seq, due, step, source = 'auto' }) {
    const cleanUser = username.toLowerCase();

    if (SUPABASE_URL && SUPABASE_ANON_KEY) {
      try {
        return await callRpc('save_review', {
          p_username: cleanUser,
          p_pin_hash: pinHash,
          p_seq: seq,
          p_due: due,
          p_step: step,
          p_source: source
        });
      } catch (err) {
        console.warn('Supabase save_review failed, saving locally:', err.message);
      }
    }

    // Local fallback
    const data = getUserLocalData(cleanUser);
    const idx = data.reviews.findIndex(r => r.question_seq === seq);
    const item = { question_seq: seq, due_date: due, step: step, source: source };
    if (idx >= 0) {
      data.reviews[idx] = item;
    } else {
      data.reviews.push(item);
    }
    saveUserLocalData(cleanUser, data);
    return { ok: true };
  },

  // Delete review item (Section 7.2)
  async deleteReview({ username, pinHash, seq }) {
    const cleanUser = username.toLowerCase();

    if (SUPABASE_URL && SUPABASE_ANON_KEY) {
      try {
        return await callRpc('delete_review', {
          p_username: cleanUser,
          p_pin_hash: pinHash,
          p_seq: seq
        });
      } catch (err) {
        console.warn('Supabase delete_review failed, deleting locally:', err.message);
      }
    }

    // Local fallback
    const data = getUserLocalData(cleanUser);
    data.reviews = data.reviews.filter(r => r.question_seq !== seq);
    saveUserLocalData(cleanUser, data);
    return { ok: true };
  },

  // Save settings (display_name, daily_goal, language, theme)
  async saveSettings({ username, pinHash, displayName, dailyGoal, language, theme }) {
    const cleanUser = username.toLowerCase();

    if (SUPABASE_URL && SUPABASE_ANON_KEY) {
      try {
        return await callRpc('save_settings', {
          p_username: cleanUser,
          p_pin_hash: pinHash,
          p_display_name: displayName,
          p_daily_goal: dailyGoal,
          p_language: language,
          p_theme: theme
        });
      } catch (err) {
        console.warn('Supabase save_settings failed, saving locally:', err.message);
      }
    }

    // Local fallback
    const registry = getLocalRegistry();
    if (registry[cleanUser]) {
      registry[cleanUser].display_name = displayName;
      registry[cleanUser].daily_goal = dailyGoal;
      registry[cleanUser].language = language;
      registry[cleanUser].theme = theme;
      saveLocalRegistry(registry);
    }
    return { ok: true };
  },

  // Delete user and all rows (Section 7.2)
  async deleteUser({ username, pinHash }) {
    const cleanUser = username.toLowerCase();

    if (SUPABASE_URL && SUPABASE_ANON_KEY) {
      try {
        await callRpc('delete_user', {
          p_username: cleanUser,
          p_pin_hash: pinHash
        });
      } catch (err) {
        console.warn('Supabase delete_user failed:', err.message);
      }
    }

    // Local fallback
    const registry = getLocalRegistry();
    delete registry[cleanUser];
    saveLocalRegistry(registry);
    localStorage.removeItem(`${LOCAL_DATA_PREFIX}${cleanUser}`);
    return { ok: true };
  }
};

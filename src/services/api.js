// Chainline: DSA Roadmap Tracker 2.0 API service
// Implements Supabase RPC client per Section 7 (Database and Data Flow)
// Direct Supabase RPC only - all local/mock user storage removed per Part B Step 5

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

// Call Supabase RPC function directly
async function callRpc(functionName, params) {
  if (!SUPABASE_URL || !SUPABASE_ANON_KEY) {
    throw new Error('SUPABASE_NOT_CONFIGURED: Please ensure VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY are set.');
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

    const user = await callRpc('login_user', {
      p_username: cleanUser,
      p_pin_hash: pinHash
    });
    const state = await callRpc('get_state', {
      p_username: cleanUser,
      p_pin_hash: pinHash
    });
    return { user, state, pinHash };
  },

  // Fetch state for active session from Supabase
  async getState(username, pinHash) {
    const cleanUser = username.trim().toLowerCase();
    return await callRpc('get_state', {
      p_username: cleanUser,
      p_pin_hash: pinHash || null
    });
  },

  // Create account (Section 5.2 & FR-1a)
  async register(username, displayName, pin, dailyGoal = 2, language = 'java', theme = 'light') {
    const cleanUser = username.trim().toLowerCase();
    if (!/^[a-z0-9_]{3,20}$/.test(cleanUser)) {
      throw new Error('BAD_USERNAME');
    }

    const pinHash = pin ? await computePinHash(cleanUser, pin) : null;

    const user = await callRpc('register_user', {
      p_username: cleanUser,
      p_display_name: displayName ? displayName.trim() : null,
      p_pin_hash: pinHash,
      p_daily_goal: dailyGoal ? Number(dailyGoal) : 2,
      p_language: language,
      p_theme: theme
    });
    const state = { progress: [], reviews: [], activity: [] };
    return { user, state, pinHash };
  },

  // Save question progress (FR-35, Section 7.2)
  async saveProgress({ username, pinHash, seq, status, mistake, notes, day }) {
    const cleanUser = username.toLowerCase();
    const todayStr = day || new Date().toISOString().split('T')[0];

    return await callRpc('save_progress', {
      p_username: cleanUser,
      p_pin_hash: pinHash || null,
      p_seq: Number(seq),
      p_status: status,
      p_mistake: Boolean(mistake),
      p_notes: notes || '',
      p_day: todayStr
    });
  },

  // Save review schedule item (Section 7.2)
  async saveReview({ username, pinHash, seq, due, step, source = 'auto' }) {
    const cleanUser = username.toLowerCase();

    return await callRpc('save_review', {
      p_username: cleanUser,
      p_pin_hash: pinHash || null,
      p_seq: Number(seq),
      p_due: due,
      p_step: Number(step),
      p_source: source
    });
  },

  // Delete review item (Section 7.2)
  async deleteReview({ username, pinHash, seq }) {
    const cleanUser = username.toLowerCase();

    return await callRpc('delete_review', {
      p_username: cleanUser,
      p_pin_hash: pinHash || null,
      p_seq: Number(seq)
    });
  },

  // Save settings (display_name, daily_goal, language, theme)
  async saveSettings({ username, pinHash, displayName, dailyGoal, language, theme }) {
    const cleanUser = username.toLowerCase();

    return await callRpc('save_settings', {
      p_username: cleanUser,
      p_pin_hash: pinHash || null,
      p_display_name: displayName,
      p_daily_goal: dailyGoal ? Number(dailyGoal) : 2,
      p_language: language,
      p_theme: theme
    });
  },

  // Delete user and all rows (Section 7.2)
  async deleteUser({ username, pinHash }) {
    const cleanUser = username.toLowerCase();

    return await callRpc('delete_user', {
      p_username: cleanUser,
      p_pin_hash: pinHash || null
    });
  }
};

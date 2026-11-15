# Software Requirements Specification 2.0

**Chainline: DSA Roadmap Tracker** (design, accounts, database and Vercel deployment update)

Version 2.0 · 15 November 2026 · Supersedes the design, login, theme and hosting parts of SRS 1.0

## 1. How to Read This Document

SRS 1.0 (including Appendix A, the 300-question catalogue, and Appendix B, the content-generation prompt) stays valid for everything that this document does not change. Where the two documents disagree, **SRS 2.0 wins**. The visual reference is the frosted-glass light design the owner approved (Home and Roadmap screens, generated in Gemini). That image is a style reference only. Section 3 lists its mistakes, and none of them may be copied into the product.

### 1.1 What changes from SRS 1.0

| Area | SRS 1.0 | SRS 2.0 |
| --- | --- | --- |
| Visual design | LeetCode-orange style, Samsung font | Frosted-glass design: soft colour orbs, rounded glass cards, indigo accent |
| Themes | Dark (default) and light | Three modes: **Light (Daylight)**, **Evening (Dusk)**, **Dark (Midnight)** |
| Login | One screen; a new username created an account automatically | Separate **Sign in** and **Create account** screens (typing a wrong username no longer creates an account by accident) |
| Hosting | Netlify | **Vercel** |
| Database | Described only | Full schema, functions and setup steps (section 7) |
| Name and logo | Placeholder | Name Chainline, original logo mark (not LeetCode’s) |
| Empty areas | Not addressed | No unused or cut-off area on any screen (rule 4.1) |
| Responsive layout | Basic | Defined breakpoints and layouts per page (section 5) |

## 2. Product Name and Brand

- Name: **Chainline**. Tagline: Solve 300, in order.
- Logo: an original mark of two interlocking rounded links that together form a letter C, plus the wordmark Chainline in bold. Do not use or imitate the LeetCode bracket logo.
- Favicon: the link mark alone on the accent colour.

## 3. Corrections to the Reference Image

The reference image looks good overall, but it contains the mistakes below. The product must follow the **Fix** column, not the image.

| # | Where | Problem in the image | Fix in the product |
| --- | --- | --- | --- |
| 1 | Logo | The logo looks like the LeetCode bracket mark | Use the original Chainline mark (section 2) |
| 2 | Nav bar | The streak icon looks like a candle, not a flame | Flame icon with the number and the word days |
| 3 | Nav bar | No account control, so no way to log out or switch user | Avatar button with a menu: username, theme, settings, log out |
| 4 | Home, ring | Two rings with a thick, uneven arc that does not equal 84 of 300 (28 percent) | One ring, round caps, constant thickness, arc length exactly done divided by 300, starting at 12 o’clock |
| 5 | Home, stat cards | The icons float above the cards and collide with the Next up card | Icons sit inside the card, with a fixed gap between rows |
| 6 | Home, stat cards | Icons are inconsistent in style and meaning | One icon set (Lucide): target, clipboard-check, flame |
| 7 | Home, chapters | Only 14 chapters appear, with names that do not match the real 18 (for example Math, Design, Backtracking) | Show all 18 chapters with the exact names in section 4.3 |
| 8 | Home, chapters | Progress bars look like toggle switches and carry no numbers | Real progress bars with a done/total label (for example 9/14) and a fill that matches the data |
| 9 | Home, activity grid | 7 by 6 cells (42) under a 12-week title, no labels, random colours | 12 columns (weeks) by 7 rows (days) = 84 cells, weekday and month labels, a 5-level colour scale, a legend |
| 10 | Roadmap, sidebar | Bar fill is random and does not match the counts (Two Pointers is 9 of 14 but its bar is almost empty) | Fill = done divided by total, with a number label |
| 11 | Roadmap, list | “#24 builds on #1” uses the LeetCode number; the others use the Seq number | Always use the **Seq** number for builds on. Show the LeetCode number separately as a small LC label |
| 12 | Roadmap, list | The mock data is impossible: 9 of 14 done, yet only 3 are done and one is in progress among the first 8 | All counts are computed from real statuses, never typed in |
| 13 | Roadmap, list | Only 8 of the 14 questions are shown | Show all 14 questions of the chapter |
| 14 | Roadmap, list | Row #28 wraps to two lines and the row is taller; the builds on column drifts | Fixed row height, single-line title with ellipsis (full title on hover or tap), fixed column widths |
| 15 | Roadmap, list | Status icons are unclear (todo is a filled grey dot, revisit has no date) | Todo is a hollow circle, In progress a half-filled circle, Done a check circle, Revisit a clock with a due-date chip, plus a legend |
| 16 | Roadmap, list | A stray sparkle shape appears at the bottom right corner | Nothing decorative outside the design system |
| 17 | Roadmap, background | A pink orb sits behind the list and lowers text contrast | Orbs are kept to the screen edges and never behind text rows; text contrast stays at 4.5 to 1 or better |
| 18 | Roadmap, header | Muted text (14 QUESTIONS · 9 DONE) and the search placeholder are too faint | Use the muted token from section 4.2 (at least 4.5 to 1) |
| 19 | Both | Only a light theme is shown | Three modes (section 4.2) |

## 4. Design System

### 4.1 Principles

1. **Frosted glass over soft colour.** A calm gradient background with three blurred colour orbs; every card is translucent glass with a thin light border.
2. **Rounded and friendly.** Large radii, pill buttons, no sharp corners.
3. **No empty areas.** Every region of every screen holds content or a designed empty state (illustration, one sentence, one action). Nothing is cut off, nothing is a placeholder box, and no text is lorem ipsum.
4. **Numbers are always real.** Every count, bar and ring is computed from the user’s data.
5. **Same layout in all three modes.** Only the colours change.

### 4.2 Colour tokens (three modes)

Implement as CSS variables on the root element, switched by a data-theme attribute with the values light, evening and dark.

| Token | Light (Daylight) | Evening (Dusk) | Dark (Midnight) |
| --- | --- | --- | --- |
| Background gradient | #BFE3FF to #EAF3FF, diagonal | #1C1743 to #4A2F6B, with a faint #E8795F glow along the bottom | #090C18 to #0F1428 |
| Orb 1 | #7DB7FF at 35% | #FF8A6B at 35% | #4F46E5 at 28% |
| Orb 2 | #7EE8D1 at 30% | #8B6CFF at 30% | #14B8A6 at 18% |
| Orb 3 | #FFB3C7 at 25% | #FFB86B at 28% | #7C3AED at 20% |
| Glass surface | rgba(255,255,255,0.62) | rgba(255,255,255,0.10) | rgba(255,255,255,0.06) |
| Glass strong (hover, selected) | rgba(255,255,255,0.85) | rgba(255,255,255,0.16) | rgba(255,255,255,0.10) |
| Glass border | rgba(255,255,255,0.85) | rgba(255,255,255,0.18) | rgba(255,255,255,0.10) |
| Card shadow | 0 12px 32px rgba(60,70,160,0.14) | 0 16px 40px rgba(10,5,30,0.45) | 0 16px 40px rgba(0,0,0,0.5) |
| Text | #1E1B4B | #FFF3E8 | #E8EAF6 |
| Muted text | #4B5575 | #D2C4E0 | #9AA3C0 |
| Accent (primary button, active nav pill) | #1E1B4B with white text | #FFC38A with #2A1B3D text | #A5A6FF with #0A0D1A text |
| Accent soft (badges, selected row, done icon) | #C7CAF8 with #3730A3 text | rgba(255,184,107,0.22) with #FFD9B0 text | rgba(139,140,248,0.22) with #C9CAFF text |
| Progress fill | #4338CA to #6366F1 | #FFB86B to #FF7E8B | #8B8CF8 to #60A5FA |
| Progress track | rgba(30,27,75,0.12) | rgba(255,255,255,0.14) | rgba(255,255,255,0.10) |
| Easy pill | #BDF0D4 with #14532D text | rgba(110,231,183,0.22) with #A7F3D0 text | same as Evening |
| Medium pill | #FDE8A8 with #78350F text | rgba(253,224,71,0.20) with #FDE68A text | same as Evening |
| Hard pill | #FBC1C1 with #7F1D1D text | rgba(252,165,165,0.22) with #FECACA text | same as Evening |
| Revisit (clock, due chip) | #D97706 | #FFB86B | #FBBF24 |
| Focus ring (2 px, 2 px offset) | #4F46E5 | #FFC38A | #A5A6FF |
| Activity levels 0 to 4 | #E3E7FB, #C7CBF5, #9FA6EE, #6F77E0, #3F3FC0 | rgba(255,255,255,0.10), #5A3F7E, #8E5C93, #D4806F, #FFB86B | #1B2140, #2B3380, #4551B8, #6B76E8, #A5A6FF |

The code panel uses the same dark editor colours in all three modes so code is always easy to read: background #12152B, text #E6E8FF, keywords #9FA8FF, strings #A5F3D0, numbers #FFD479, comments #7A84AD, functions #7DD3FC.

Activity levels: 0 = no questions, 1 = one, 2 = two, 3 = three or four, 4 = five or more.

**Mode behaviour.** The mode is chosen on the login screen, in the account menu and in Settings, saved per user, and applied with a 300 ms cross-fade. Default for a new user: Light. Optional P2: an Auto setting (Light by day, Evening from 6 pm to 9 pm, Dark after 9 pm).

### 4.3 Chapter names and totals (use exactly these everywhere)

| # | Display name | Questions | # | Display name | Questions |
| --- | --- | --- | --- | --- | --- |
| 1 | Arrays & Hashing | 21 | 10 | Heap | 14 |
| 2 | Two Pointers | 14 | 11 | Greedy | 17 |
| 3 | Sliding Window | 14 | 12 | Intervals | 8 |
| 4 | Binary Search | 18 | 13 | Graphs: BFS & DFS | 22 |
| 5 | Stack | 15 | 14 | Graphs: Advanced | 17 |
| 6 | Linked List | 17 | 15 | DP: 1D | 19 |
| 7 | Backtracking | 21 | 16 | DP: 2D & Strings | 24 |
| 8 | Binary Trees | 27 | 17 | Tries & Design | 9 |
| 9 | Binary Search Trees | 9 | 18 | Bits & Math | 14 |

The totals add up to 300. They are calculated from questions.json, not typed in.

### 4.4 Typography

| Use | Font | Size and weight |
| --- | --- | --- |
| Page title and greeting | Plus Jakarta Sans (closest match to the reference; fallback Manrope, then system sans-serif) | 40/44 bold on desktop, 28/32 on mobile. The user’s name is italic. |
| Section and card title | Plus Jakarta Sans | 20/24 semibold |
| Body | Plus Jakarta Sans | 16/24 regular |
| Big numbers (ring, stats) | Plus Jakarta Sans, tabular numerals | 44 bold in the ring, 32 bold in stat cards |
| Labels and captions | Geist Mono (fallback JetBrains Mono, then monospace) | 12 uppercase, letter spacing 0.08em |
| Code | JetBrains Mono | 14/22 |

Load fonts with swap display and a fallback stack so text never disappears.

### 4.5 Shape, spacing, effects

- Card radius 28 px (20 px for inner blocks), buttons and chips fully rounded, inputs 16 px.
- Spacing grid of 4 px. Gap between sections 24 px. Card padding 24 px (16 px on mobile).
- Glass: background blur 24 px (18 px on mobile), 1 px border, shadow from the token table. If backdrop blur is not supported, use the glass colour at 92% opacity.
- Hover: cards lift by 2 px and move to the Glass strong colour. Press: scale 0.98. Transitions 150 to 250 ms ease-out. If the user prefers reduced motion, turn off lifts and cross-fades.
- Icons: Lucide, 20 px, 1.75 px stroke.

### 4.6 Components

- **Top bar:** a floating glass pill, 64 px high, 16 px from the top. Contents: logo and name, Home, Roadmap, Today, Settings (the active link is the Accent pill), streak chip (flame icon and the number of days), avatar menu. Sticks to the top while scrolling.
- **Buttons:** primary = Accent fill; secondary = glass pill with border; icon button = 40 px circle. Minimum touch target 44 px.
- **Progress bar:** 10 px high, rounded, fill from the token, with a done/total label at the right.
- **Progress ring:** 200 px on desktop and 160 px on mobile; 14 px stroke; one ring; the arc is exactly done divided by total; the number in the centre.
- **Status icons:** Todo is a hollow circle; In progress a half-filled circle; Done a circle in Accent soft with a check; Revisit a clock in the revisit colour. Every icon also has an accessible name.
- **Difficulty pills:** Easy, Medium, Hard in the token colours, fixed width 84 px.
- **Question row:** fixed height 64 px. Columns: status icon, Seq number, title (one line, ellipsis), difficulty pill, builds on #n (Seq number), LeetCode icon button. A Revisit row also shows a due-date chip.
- **Activity grid:** 12 columns by 7 rows, weekday labels (Mon, Wed, Fri), month labels above, a legend (Less to More), a tooltip with the date and the count.
- **Inputs:** glass fields with a visible label above and a clear error line below.
- **Empty states:** a small illustration, one sentence, one action button.
- **Loading:** skeleton shapes with the same size as the final content, so the layout does not jump.
- **Toast:** bottom centre on desktop, above the bottom bar on mobile.

## 5. Page Specifications

### 5.1 Breakpoints

| Name | Width | Layout |
| --- | --- | --- |
| Desktop | 1200 px and wider | Content max width 1280 px, 12-column grid, sticky sidebars |
| Tablet | 768 to 1199 px | Sidebars become horizontal chip scrollers or drawers, two-column grids |
| Mobile | below 768 px | One column, bottom navigation bar (Home, Roadmap, Today, Settings), cards stacked |

Test at 360, 390, 768, 1024, 1440 and 1920 px. There is no horizontal page scroll at any width. At 1920 px the content stays centred and the orbs fill the sides.

### 5.2 Sign in and Create account

**Layout (desktop):** two halves over the orb background. Left half: logo, a large heading “Solve 300, *in order.*”, one line of text (“A chain of 300 LeetCode questions, each building on the last.”), and three floating glass preview cards that show the real product (a progress ring, a streak chip, a row of the roadmap list). Right half: one glass card, 440 px wide, with a segmented switch **Sign in | Create account**. A theme switcher (three small swatches) sits in the top right corner. On mobile the hero shrinks to a logo and one line, and the card takes the full width.

**Sign in:** username field; PIN field (four boxes) shown only after the server says a PIN is needed; button Sign in. Errors: “No account with that username. Create one?” (with a link to the other tab), “That PIN is not right.”

**Create account:** username (3 to 20 characters: a to z, 0 to 9, underscore; checked for availability while typing), display name (optional), PIN (optional, four boxes, with the note “A PIN keeps others from opening your page. You cannot recover it, so remember it.”), daily goal (chips 1 to 5, default 2), preferred language (Java or Python), mode (three swatch cards: Light, Evening, Dark; choosing one changes the page immediately). Button Create account. Error: “That username is taken.”

**Both tabs:** a short honest note under the card: “There is no email or password. Anyone who knows your username (and PIN, if you set one) can open your page.”

### 5.3 Home

| Region | Content |
| --- | --- |
| Greeting | “Good morning”, “Good afternoon” or “Good evening” plus the user’s name in italics, chosen by local time |
| Next up card (8 of 12 columns) | Label Next up, the Seq number and title, chips for difficulty and Builds on #n with its title, and the buttons **Start** (primary) and **Open on LeetCode** (secondary) |
| Overall ring (4 of 12 columns) | Ring with done / 300, plus a small Easy, Medium and Hard breakdown below it |
| Three stat cards (equal width) | Today (solved today / daily goal), Due reviews (count, opens the Today page), Streak (days) |
| Chapter progress card (7 of 12 columns) | All 18 chapters in two columns of nine: name, done/total, progress bar. Each row opens that chapter. |
| Activity card (5 of 12 columns) | The 12 by 7 activity grid with labels and legend |

Mobile order: greeting, Next up, ring, three stat cards in a row (scrollable if needed), chapter progress (one column), activity grid. Tablet: Next up and ring side by side, stats in a row, chapters and activity stacked.

### 5.4 Roadmap

- **Left sidebar (280 px, sticky):** all 18 chapters, each with name, done/total and a progress bar; the active chapter uses Accent soft. Tablet: a horizontal chip scroller. Mobile: a button showing the chapter name that opens a bottom sheet.
- **Header:** chapter name, a badge “9 of 14” (calculated), the mono line “14 QUESTIONS · 9 DONE”, search box (title or LC number).
- **Filter chips:** All, Easy, Medium, Hard, Revisit, Mistakes (scrollable on small screens). Counts appear on each chip.
- **Status legend:** a small row explaining the four status icons.
- **List:** all questions of the chapter in seq order as question rows (section 4.6). The row for the next-up question is highlighted with Accent soft. Mobile: each row becomes a two-line card: first line status icon, Seq number and title (up to two lines); second line difficulty pill, builds on #n and the LeetCode icon.
- **Empty state** (a filter with no results): illustration, “Nothing matches these filters”, button Clear filters.

### 5.5 Question page

Split layout on desktop (left 5 columns, right 7 columns); stacked on tablet and mobile. Left glass card: mono label (Seq, chapter, difficulty), title, Builds on and Leads to links, **Open on LeetCode** button, status selector, mistake toggle, notes. Right side: a row of five glass pill buttons **Hint 1, Hint 2, Hint 3, Approach, Code** (Hint 2 and 3 are locked until the one before is opened), and the panel for the chosen button below. Approach shows two tabs (Brute force, Optimal) with idea, steps and complexity chips. Code shows the same two tabs with a Java / Python switch and a Copy button. The code panel is always dark (section 4.2). Previous and Next question buttons at the bottom. Opening a panel never changes the status.

### 5.6 Today

Heading with the counts (due, overdue). A list of review cards: title, chapter chip, difficulty, mistake tag, due date (overdue in the revisit colour), and the buttons **Recalled** and **Forgot**. At the side (desktop) or below (mobile): the next seven days as a small calendar with dots, the daily goal ring, and the Next up shortcut. Empty state when nothing is due: “All caught up” with a button to open Next up.

### 5.7 Settings

Glass cards: Profile (display name), Daily goal (stepper 1 to 10), Language (Java or Python), **Mode** (three swatch cards, Light, Evening, Dark, each a small preview of the real colours), Export and Import progress, Log out, and Delete my data (outlined in the danger colour, with a typed confirmation).

## 6. Functional Requirement Changes

| ID | Change | Priority |
| --- | --- | --- |
| FR-1 (replaced) | Sign in screen: username, and PIN if the account has one. It never creates an account. | P0 |
| FR-1a (new) | Create account screen as in 5.2, with live username check and a clear error when the name is taken. | P0 |
| FR-26 (replaced) | Three modes (Light, Evening, Dark), saved per user, switchable from the login screen, the account menu and Settings. | P0 |
| FR-31 (new) | Avatar menu in the top bar: username, mode switcher, Settings, Log out. | P0 |
| FR-32 (new) | Every screen follows rule 4.1 (no empty or cut-off areas) and shows designed empty and loading states. | P0 |
| FR-33 (new) | Layouts follow section 5 at all breakpoints with no horizontal page scroll. | P0 |
| FR-34 (new) | Respect the reduced-motion setting. | P1 |
| FR-35 (new) | All counts, bars, rings and chapter totals are calculated from data (rule 4.4). | P0 |
| FR-36 (new) | A Revisit question shows its due date wherever its status is shown. | P1 |

## 7. Database (Supabase)

This replaces sections 6.2 and 6.3 of SRS 1.0 and is the full setup. The browser never reads or writes the tables. It only calls the functions below with the Supabase anon key. Run 7.1 first, then 7.2, in the Supabase SQL Editor.

### 7.1 Tables

```sql
create table app_users (
  id uuid primary key default gen_random_uuid(),
  username text unique not null check (username ~ '^[a-z0-9_]{3,20}$'),
  display_name text,
  pin_hash text,
  daily_goal int not null default 2 check (daily_goal between 1 and 10),
  language text not null default 'java' check (language in ('java','python')),
  theme text not null default 'light' check (theme in ('light','evening','dark')),
  created_at timestamptz not null default now()
);

create table progress (
  user_id uuid references app_users(id) on delete cascade,
  question_seq int not null check (question_seq between 1 and 300),
  status text not null default 'todo' check (status in ('todo','in_progress','done','revisit')),
  mistake boolean not null default false,
  notes text not null default '',
  solved_at timestamptz,
  updated_at timestamptz not null default now(),
  primary key (user_id, question_seq)
);

create table reviews (
  user_id uuid references app_users(id) on delete cascade,
  question_seq int not null check (question_seq between 1 and 300),
  due_date date not null,
  step int not null default 0,
  source text not null default 'auto' check (source in ('auto','manual')),
  primary key (user_id, question_seq)
);

create table activity (
  user_id uuid references app_users(id) on delete cascade,
  day date not null,
  solved_count int not null default 0,
  primary key (user_id, day)
);

alter table app_users enable row level security;
alter table progress enable row level security;
alter table reviews enable row level security;
alter table activity enable row level security;
revoke all on app_users, progress, reviews, activity from anon, authenticated;
```

With row-level security on and no policies, direct table access is denied for everyone except the functions below (they run with the owner’s rights).

### 7.2 Functions

```sql
create or replace function _auth(p_username text, p_pin_hash text)
returns uuid language plpgsql security definer set search_path = public as $$
declare v_id uuid; v_pin text;
begin
  select id, pin_hash into v_id, v_pin from app_users where username = lower(p_username);
  if v_id is null then raise exception 'NO_SUCH_USER'; end if;
  if v_pin is not null and p_pin_hash is null then raise exception 'PIN_REQUIRED'; end if;
  if v_pin is not null and v_pin <> p_pin_hash then raise exception 'WRONG_PIN'; end if;
  return v_id;
end $$;

create or replace function register_user(p_username text, p_display_name text, p_pin_hash text,
  p_daily_goal int, p_language text, p_theme text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v app_users;
begin
  if lower(p_username) !~ '^[a-z0-9_]{3,20}$' then raise exception 'BAD_USERNAME'; end if;
  insert into app_users(username, display_name, pin_hash, daily_goal, language, theme)
  values (lower(p_username), nullif(trim(p_display_name), ''), p_pin_hash,
    coalesce(p_daily_goal, 2), coalesce(p_language, 'java'), coalesce(p_theme, 'light'))
  returning * into v;
  return (to_jsonb(v) - 'pin_hash' - 'id') || jsonb_build_object('has_pin', v.pin_hash is not null);
exception when unique_violation then
  raise exception 'USERNAME_TAKEN';
end $$;

create or replace function login_user(p_username text, p_pin_hash text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v_id uuid; v app_users;
begin
  v_id := _auth(p_username, p_pin_hash);
  select * into v from app_users where id = v_id;
  return (to_jsonb(v) - 'pin_hash' - 'id') || jsonb_build_object('has_pin', v.pin_hash is not null);
end $$;

create or replace function get_state(p_username text, p_pin_hash text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v_id uuid;
begin
  v_id := _auth(p_username, p_pin_hash);
  return jsonb_build_object(
    'progress', coalesce((select jsonb_agg(to_jsonb(p) - 'user_id') from progress p where p.user_id = v_id), '[]'::jsonb),
    'reviews',  coalesce((select jsonb_agg(to_jsonb(r) - 'user_id') from reviews r where r.user_id = v_id), '[]'::jsonb),
    'activity', coalesce((select jsonb_agg(to_jsonb(a) - 'user_id') from activity a
                          where a.user_id = v_id and a.day >= current_date - 100), '[]'::jsonb));
end $$;

create or replace function save_progress(p_username text, p_pin_hash text, p_seq int,
  p_status text, p_mistake boolean, p_notes text, p_day date)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v_id uuid; v_old timestamptz;
begin
  v_id := _auth(p_username, p_pin_hash);
  select solved_at into v_old from progress where user_id = v_id and question_seq = p_seq;
  insert into progress(user_id, question_seq, status, mistake, notes, solved_at, updated_at)
  values (v_id, p_seq, p_status, coalesce(p_mistake, false), coalesce(p_notes, ''),
    case when p_status = 'done' then now() end, now())
  on conflict (user_id, question_seq) do update
    set status = excluded.status, mistake = excluded.mistake, notes = excluded.notes,
        solved_at = coalesce(progress.solved_at, excluded.solved_at), updated_at = now();
  if p_status = 'done' and v_old is null then
    insert into activity(user_id, day, solved_count) values (v_id, p_day, 1)
    on conflict (user_id, day) do update set solved_count = activity.solved_count + 1;
  end if;
  return jsonb_build_object('ok', true);
end $$;

create or replace function save_review(p_username text, p_pin_hash text, p_seq int,
  p_due date, p_step int, p_source text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v_id uuid;
begin
  v_id := _auth(p_username, p_pin_hash);
  insert into reviews(user_id, question_seq, due_date, step, source)
  values (v_id, p_seq, p_due, coalesce(p_step, 0), coalesce(p_source, 'auto'))
  on conflict (user_id, question_seq) do update
    set due_date = excluded.due_date, step = excluded.step, source = excluded.source;
  return jsonb_build_object('ok', true);
end $$;

create or replace function delete_review(p_username text, p_pin_hash text, p_seq int)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v_id uuid;
begin
  v_id := _auth(p_username, p_pin_hash);
  delete from reviews where user_id = v_id and question_seq = p_seq;
  return jsonb_build_object('ok', true);
end $$;

create or replace function save_settings(p_username text, p_pin_hash text, p_display_name text,
  p_daily_goal int, p_language text, p_theme text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v_id uuid;
begin
  v_id := _auth(p_username, p_pin_hash);
  update app_users set display_name = nullif(trim(p_display_name), ''),
    daily_goal = p_daily_goal, language = p_language, theme = p_theme where id = v_id;
  return jsonb_build_object('ok', true);
end $$;

create or replace function delete_user(p_username text, p_pin_hash text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v_id uuid;
begin
  v_id := _auth(p_username, p_pin_hash);
  delete from app_users where id = v_id;
  return jsonb_build_object('ok', true);
end $$;

revoke execute on function _auth(text, text) from public, anon, authenticated;
grant execute on function
  register_user(text, text, text, int, text, text),
  login_user(text, text),
  get_state(text, text),
  save_progress(text, text, int, text, boolean, text, date),
  save_review(text, text, int, date, int, text),
  delete_review(text, text, int),
  save_settings(text, text, text, int, text, text),
  delete_user(text, text)
to anon;
```

### 7.3 Rules for the front end

- Call the functions with the Supabase client’s rpc method and the anon key only. Never put the service\_role key in the front end.
- PIN hash: SHA-256, in the browser, of the text username, a colon, the PIN, a colon, and the word chainline. With no PIN, send null.
- The function error messages are codes. Show these texts: NO\_SUCH\_USER = “No account with that username. Create one?”; PIN\_REQUIRED = show the PIN boxes; WRONG\_PIN = “That PIN is not right.”; USERNAME\_TAKEN = “That username is taken.”; BAD\_USERNAME = “Use 3 to 20 letters, numbers or underscores.”
- Send the user’s local date as p\_day in save\_progress, so streaks follow the user’s own calendar day.
- A four-digit PIN can still be guessed by repeated calls, because this version has no attempt limit. This is accepted for version 2.0 and is stated on the login screen. An attempt lockout can be added later.

### 7.4 Supabase setup steps

1. Go to supabase.com, sign in, and create a new project named chainline. Choose the region closest to you and save the database password somewhere safe.
2. Open SQL Editor, create a new query, paste section 7.1 and run it. Create another query with section 7.2 and run it.
3. Open Table Editor and confirm that the four tables exist with row-level security enabled.
4. Open Project Settings, then API. Copy the Project URL and the anon public key.
5. In the project folder, create a file named .env.local with these two lines and your own values: VITE\_SUPABASE\_URL=your project URL and VITE\_SUPABASE\_ANON\_KEY=your anon key. Do not commit this file.
6. Run the app locally, create an account, mark a question Done, and check that a row appears in progress in the Table Editor.
7. Free Supabase projects can be paused after a period of inactivity. If the app stops responding, open the Supabase dashboard and restore the project. Check Supabase’s current free-plan rules. The Export button in Settings is the backup.

## 8. Deployment on Vercel

This replaces section 9 of SRS 1.0 (Netlify).

1. Remove netlify.toml from the project. Add a file named vercel.json in the project root so that every path opens the single-page app:

```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
```

2. Push the project to a GitHub repository.
3. On vercel.com, sign in with GitHub, choose Add New, then Project, and import the repository.
4. Framework preset: Vite. Build command: npm run build. Output directory: dist.
5. Under Environment Variables add VITE\_SUPABASE\_URL and VITE\_SUPABASE\_ANON\_KEY with the values from step 4 of 7.4, for Production, Preview and Development.
6. Click Deploy. Open the Vercel address, create an account, and run the acceptance checks in section 9.
7. Every push to the main branch redeploys the site. After you change an environment variable, redeploy for it to take effect.
8. Optional: add a custom domain under the project’s Domains settings.
9. When everything works on Vercel, delete the old Netlify site.

The Vercel Hobby plan is meant for personal, non-commercial use. Check Vercel’s current terms before sharing the site widely or charging for it.

## 9. Acceptance Criteria (in addition to SRS 1.0, section 12)

1. Signing in with an unknown username shows the error and does not create an account.
2. Creating an account with a taken username shows “That username is taken.” A free username creates the account and signs in.
3. For an account with a PIN, Sign in asks for the PIN; a wrong PIN shows the PIN error.
4. Light, Evening and Dark each apply to every screen, survive a refresh, and are saved per user (the same mode appears on another device).
5. The Home ring arc equals done divided by 300 when tested with 0, 84 and 300 done questions.
6. The Home chapter card and the Roadmap sidebar show the 18 names and totals of section 4.3, and the totals add up to 300.
7. The activity grid has exactly 84 cells (12 by 7), with weekday and month labels and a legend.
8. Roadmap shows every question of the chapter; the badge and bars match the real statuses; builds on always shows Seq numbers.
9. No question row changes height; long titles end in an ellipsis and show in full on hover or tap.
10. From 360 px to 1920 px there is no horizontal page scroll, and mobile has the bottom navigation.
11. Text contrast is at least 4.5 to 1 in all three modes (check with a contrast tool).
12. A direct request to the tables with the anon key is denied; the function calls work.
13. The Vercel site loads, and refreshing on the Roadmap address still opens the Roadmap.
14. Delete my data removes the account and all its rows.
15. With reduced motion turned on in the device settings, lifts and cross-fades are off.
16. None of the problems listed in section 3 appears anywhere in the product.

## Appendix: Prompt for Antigravity (SRS 2.0)

Paste this together with this document.

```text
Update the Chainline app to match SRS 2.0 exactly. SRS 1.0 still applies wherever SRS 2.0 is silent.

1. Replace the whole UI with the frosted-glass design in sections 4 and 5. Implement the three modes (light, evening, dark) as CSS variables, using the exact tokens in 4.2. Do not copy any mistake listed in section 3.
2. Build the Sign in and Create account screens from 5.2. Sign in must never create an account.
3. Build Home, Roadmap, Question, Today and Settings from section 5, responsive at the breakpoints in 5.1. Every count, bar, ring and chapter total must be calculated from the data. Chapter names and totals must match section 4.3.
4. No empty or cut-off areas anywhere. Add loading skeletons and designed empty states.
5. Database: run the SQL in section 7. The browser calls only the Supabase functions through rpc, never the tables. Hash the PIN in the browser as described in 7.3 and show the messages listed there.
6. Deployment: delete netlify.toml, add vercel.json from section 8, and read VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY from the environment.
7. When finished, run the acceptance checks in section 9 and list any that fail.

Do not change the question data or the solution files.
```

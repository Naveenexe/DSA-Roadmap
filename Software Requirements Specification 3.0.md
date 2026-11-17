# Software Requirements Specification 3.0

**Chainline Version 3**: 500 questions, company logos, preparation tools and the activity card fix

Version 3.0 · 17 November 2026 · Adds to SRS 1.0 and SRS 2.0 without changing what already works

## 1. How to Read This Document and Protect Version 2

SRS 1.0 and SRS 2.0 stay valid. Version 3 only **adds** or **fixes** what is listed here. Where this document is silent, nothing changes. Where it disagrees with an older document, SRS 3.0 wins.

### 1.1 Rules that keep the existing app working

1. Questions 1 to 300 keep their Seq number, LeetCode number, link name, chapter, solutions and hints exactly as they are. They are never renumbered or reordered.
2. New questions are Seq 301 to 500, in new chapters 19 to 32.
3. No existing table, column, function or function signature is renamed, removed or changed. The only existing objects touched are the two question-number range checks in 9.1. Everything else is added with default values.
4. The database migration in section 9 can be run more than once and loses no data.
5. Every new feature sits behind a switch in one config file (11.2), so any feature can be turned off without deleting code.
6. No count is typed into the code. Totals (500, chapter sizes, company counts) always come from the data files.
7. After every stage, the 16 acceptance checks of SRS 2.0 section 9 and the checks of SRS 1.0 section 12 must still pass.
8. Work happens on a git branch named v3. Before starting, tag the deployed version v2.0. Vercel builds a preview address for the branch; merge into main only after section 12 passes.

### 1.2 What changes

| Area | Change | Section |
| --- | --- | --- |
| Home, Activity card | Fixed layout that fills the card, with real content in the free space | 2 |
| Questions | 200 new questions (Seq 301 to 500) in 14 new chapters | 3 |
| Company logos and filter | New | 4 |
| Company prep mode | New pages | 5 |
| Solve timer, attempts and weak topics | New | 6 |
| My solution | New panel on the question page | 7 |
| Interview date plan | New | 8 |
| Database | Additive migration | 9 |

### 1.3 Not in version 3.0

Mock interview mode, C++ solutions, installable app and push reminders, predict-the-complexity quizzes, badges and weekly summaries, and PDF or flashcard export are left for a later version.

## 2. Activity Card Fix (Home)

### 2.1 What is wrong today

Observed on desktop and on phone: the squares are small and fixed in size, so the grid covers only about 40 percent of the card width on desktop and about 55 percent on phone, and the rest of the card is empty. The month labels sit at fixed pixel positions and drift away from their weeks (the Nov label ends up beyond the grid). The weekday labels read Sun, Tue, Thu, Sat. The header shows 84 days, which tells the user nothing. On desktop the card is stretched to the height of the chapters card, which leaves its lower half blank.

### 2.2 Required design

- **Grid fills the card width.** One label column plus 12 equal columns. Cells are square (aspect ratio 1:1), gap 4 px (3 px on phone), radius 6 px, no larger than 36 px. Expected size: about 30 px on desktop and about 24 px on a 390 px phone.
- **84 cells.** 12 columns (weeks) by 7 rows (days). Weeks start on Monday. The last column is the current week; the first is 11 weeks earlier.
- **Weekday labels** Mon, Wed and Fri, aligned to rows 1, 3 and 5.
- **Month labels** sit above the first column of each month. They are placed by grid column, never by pixel. A label is skipped if it would be closer than 3 columns to the previous one.
- **Today** has a 2 px accent ring. **Days after today** are drawn as a dashed outline with no fill and no tooltip.
- **Header:** the title Activity on the left and, on the right, a calculated line such as 23 solved in 12 weeks.
- **Below the grid:** a legend (Less to More) on the right, and a row of three mini stats: Active days (out of 84), Longest streak, Best day (count and date). All three are calculated from the data.
- **Tooltip** on hover (desktop) or tap (phone), for example Tue 11 Nov · 2 solved.
- **Card height equals content height.** The card is never stretched to match its neighbour.
- **New user:** the empty grid still shows, with the line “Solve a question to light up your first square.”
- Colours come from the activity level tokens in SRS 2.0 section 4.2. Every cell has an accessible label with its date and count.

### 2.3 Home layout change

- **Desktop and tablet in landscape:** the lower part of Home has two columns. Left, 7 of 12 columns: the chapters card. Right, 5 of 12 columns: two cards stacked, first the Activity card (2.2), then the **Needs attention** card (6.4). Both columns end on the same line. The Needs attention card grows to fill any leftover height, and its content stays vertically centred when it is short.
- **Phone:** one column in this order: greeting, Next up, ring, stat cards, interview plan card (if shown), chapters card, Activity card, Needs attention card.

### 2.4 Chapters card with 32 chapters

A two-part switch Part 1 (chapters 1 to 18) | Part 2 (chapters 19 to 32) sits in the card header. It opens on the part that holds the Next up question. Each part shows its chapters in two columns (one column on phone), each with name, done/total and a bar. The overall ring on Home shows done out of the total of all questions (500).

## 3. New Questions (Part 2)

### 3.1 Rules

- 200 new questions, Seq 301 to 500, listed in Appendix A in the same columns as SRS 1.0 Appendix A. Builds on may point to any earlier Seq (1 to 499).
- No premium-only questions, and no question that is already among the first 300.
- Each question has the same solution entry as before: brute force and optimal, in Java and Python, with the **Brute force tab first**, plus three progressive hints.
- The Next up rule is unchanged. After question 300 it continues at 301.

### 3.2 New chapters

| # | Chapter | Seq range | Questions |
| --- | --- | --- | --- |
| 19 | Arrays & Hashing II | 301 to 314 | 14 |
| 20 | Strings | 315 to 328 | 14 |
| 21 | Two Pointers & Sliding Window II | 329 to 342 | 14 |
| 22 | Binary Search II | 343 to 354 | 12 |
| 23 | Stack & Queue II | 355 to 368 | 14 |
| 24 | Linked List & Design II | 369 to 380 | 12 |
| 25 | Backtracking II | 381 to 394 | 14 |
| 26 | Trees & BST II | 395 to 412 | 18 |
| 27 | Heap, Greedy & Intervals II | 413 to 428 | 16 |
| 28 | Matrix, Math & Bits II | 429 to 442 | 14 |
| 29 | Graphs II (BFS & DFS) | 443 to 458 | 16 |
| 30 | Graphs III (Topo, Union-Find, Shortest Paths) | 459 to 472 | 14 |
| 31 | DP II (1D & Knapsack) | 473 to 486 | 14 |
| 32 | DP III (2D, Strings & Intervals) | 487 to 500 | 14 |

The counts add up to 200. The rule in SRS 1.0 section 7.5 now reads: chapters 1 to 18 cover Seq 1 to 300 and chapters 19 to 32 cover Seq 301 to 500, each range contiguous, with no gaps or overlaps.

### 3.3 Where they appear

The Roadmap sidebar shows two group headings, Part 1 (chapters 1 to 18) and Part 2 (chapters 19 to 32). Each new chapter has an intro card and a short pattern cheat sheet like the existing ones. Existing users keep all their progress; their ring changes from, for example, 84/300 to 84/500 because the total is calculated.

### 3.4 Content generation

The solutions are written in 8 batches of 25 questions: batch 13 is Seq 301 to 325, batch 14 is 326 to 350, and so on up to batch 20 (Seq 476 to 500). They go into public/data/solutions/ch-19.json to ch-32.json. The quality checklist of SRS 1.0 section 10.4 applies, and every entry includes hints (an array of three strings: a small nudge, the pattern or data structure, and almost the full idea with no code).

## 4. Company Logos and Company Filter

### 4.1 Data files

- **public/data/companies.json:** an updated date, and for each company a slug, a display name and a website domain. The first list holds 30 companies: Google (google.com), Amazon (amazon.com), Microsoft (microsoft.com), Meta (meta.com), Apple (apple.com), Netflix (netflix.com), Uber (uber.com), Airbnb (airbnb.com), Adobe (adobe.com), Bloomberg (bloomberg.com), Oracle (oracle.com), Salesforce (salesforce.com), LinkedIn (linkedin.com), Goldman Sachs (goldmansachs.com), Atlassian (atlassian.com), Nvidia (nvidia.com), Tesla (tesla.com), TikTok (tiktok.com), Walmart (walmart.com), PayPal (paypal.com), Cisco (cisco.com), Intuit (intuit.com), Stripe (stripe.com), Databricks (databricks.com), Flipkart (flipkart.com), Zoho (zoho.com), Infosys (infosys.com), TCS (tcs.com), Paytm (paytm.com), Swiggy (swiggy.com).
- **questions.json:** each question may have an optional companies list of 0 to 5 slugs. Existing fields are unchanged.

### 4.2 Data policy

Company tags are not copied from LeetCode (company tags are a Premium feature there, and scraping would break its terms). The tags are community-reported and must be treated as unverified:

1. Tag a question only where the link between the company and the question is widely reported. If unsure, leave it untagged.
2. Write companies-review.md listing every tag, so the owner can check and correct the JSON by hand.
3. Show the tooltip “Reported by candidates. May be out of date.” wherever tags appear, and a footer line: “Company names and logos belong to their owners. Chainline is not affiliated with them.”
4. A question without tags shows no company row at all (no empty row).

### 4.3 Logos

- Logos are loaded from a logo service by domain. They are not stored in the repository. The address and a key are set with an environment variable named VITE\_LOGO\_TOKEN, and the service is chosen by the owner after checking its current free-tier and attribution rules. The old free Clearbit logo address no longer works and must not be used.
- If the key is missing or a logo fails to load, show a round letter chip with the company’s first letter. Logos load lazily, have a fixed size, and never delay the page.

### 4.4 Where companies appear

- **Question page:** an Asked at row under the Builds on card with round glass logos, 36 px (28 px on phone), wrapping onto more lines if needed. Hover or tap shows the name.
- **Roadmap rows:** up to 3 logos of 24 px and a +n chip. On phone the logos sit on a third line of the card (22 px), only when tags exist.
- **Company filter:** a Company chip next to the difficulty chips. It opens a searchable list (a portal dropdown on desktop, a bottom sheet on phone) with logo, name and question count. The choice shows as a removable chip and combines with the other filters inside the current chapter.
- No layout shift: logo slots have fixed sizes before the image loads.

## 5. Company Prep Mode

- **Where to find it:** a By company button in the Roadmap header and a Company prep card on Home (it shares the card slot with the interview plan, 8.3). The four-item navigation does not change.
- **/companies:** a grid of company cards (3 columns on desktop, 2 on tablet and on phone). Each card: logo (48 px), name, N questions, and a progress bar with done/N. Search box on top. Sorted by number of questions, most first. Companies with no tagged questions are hidden.
- **/companies/:slug:** a header with the logo, the name, a ring showing readiness (done divided by tagged, calculated), counts by difficulty, and a **Start next** button (the lowest-Seq unfinished question of that company). Below, filter chips (All, Easy, Medium, Hard, Not done) and the question rows in Seq order under small chapter headings, using the same row component as the Roadmap.
- Readiness is only done divided by tagged questions. The page never claims anything about real interview results.
- Empty states: no search result (Clear search), all questions done (a congratulation line and a link to the next company).

## 6. Solve Timer, Attempts and Weak Topics

### 6.1 Timer

A full-width Timer row on the question page, under the status row: the time as 00:00, buttons Start and Pause, and Reset. It adds up the time across visits. It pauses by itself when the browser tab is hidden. It saves every 15 seconds, on Pause, on leaving the page and when the question is marked Done.

### 6.2 Attempts

An attempt is a day on which the user started the timer for that question. The count is stored and shown as Attempts: 2 beside the timer.

### 6.3 Slow rule

When a question is marked Done and its total time is above 20 minutes (Easy), 40 minutes (Medium) or 60 minutes (Hard), a toast asks “That took a while. Add it to Revisit?” with Yes and No. Yes creates a manual review for tomorrow. Nothing is added without the user’s choice. The slow mark is stored.

### 6.4 Needs attention (weak topics)

For every chapter with at least 3 solved questions, score = (2 × mistake-tagged + 2 × Forgot answers + 1 × slow) divided by the number solved. The card lists the top 3 chapters with a score above 0: chapter name, chips such as 3 mistakes · 2 forgot · 1 slow, and an Open chapter button. For a new user the card shows “Solve a few questions and your weak spots will show here.” with a button to Next up. The header has an All stats link.

### 6.5 Stats page

Route /stats, reached from the Needs attention card and the avatar menu. Cards: average time per difficulty (three bars), questions solved per week for the last 12 weeks (bars), chapters ranked by score, total time spent, longest streak. Every number is calculated; each card has an empty state.

## 7. My Solution

- A sixth button, **My code**, joins the question page button group. On phone the grid becomes Hint 1, Hint 2, Hint 3 on the first row, then Approach, Code and My code on the second row. On desktop all six sit in the existing button row.
- The panel holds a code editor (a plain text area in a monospace font, Tab inserts four spaces) with the same Java | Python switch used everywhere. The user’s code is kept separately for each language.
- It saves by itself 1.5 seconds after typing stops and shows Saving and then Saved. The limit is 20,000 characters, with a clear message when it is reached. There is a Copy button.
- A switch Show reference solution opens the Brute force | Optimal tabs below the editor (side by side from 1200 px, stacked below that).
- A small dot on the My code button shows that saved code exists.
- The code is stored as plain text and is never run, judged or displayed as HTML.

## 8. Interview Date Plan

### 8.1 Setting it

Settings gets an Interview plan card: a date field (today or later), an optional company list (from companies.json), Save and Clear. If the user has no plan, nothing changes anywhere else.

### 8.2 Algorithm

1. Pool = every question that is not Done. If a company is chosen, only the questions tagged with that company. Otherwise all questions, in Seq order.
2. Days left = the number of days from today to the interview date, counting today, at least 1.
3. Daily target = the pool size divided by days left, rounded up, kept between 1 and 10.
4. Today’s list = the first daily-target questions of the pool in Seq order. Due reviews are shown separately and do not count towards it.
5. Everything is recalculated every day. Solved questions leave the pool.
6. If the real need is more than 10 a day, show the line “There are not enough days to cover everything. Showing 10 a day.”
7. When the pool is empty, show “You have covered everything in your plan.” After the interview date has passed, show “Your interview date has passed.” with a Clear plan button.

### 8.3 Where it shows

- **Home:** an Interview plan card with days left, a ring (done divided by total in the plan scope, calculated), and today’s target list of up to 5 rows with Start buttons. Without a plan, the same card slot shows a Company prep card (5) with a Set an interview date link, so the slot is never empty.
- **Today page:** a Plan for today section above the due reviews.

## 9. Database Migration (additive)

Save as supabase/migration-v3.sql and run it once in the Supabase SQL Editor before the new front end is deployed. It does not delete or change any existing data and can be run again safely.

### 9.1 Tables, columns and range checks

The old tables only accept question numbers up to 300. Without the first four lines, marking question 301 or later as done would fail.

```sql
alter table progress drop constraint if exists progress_question_seq_check;
alter table progress add constraint progress_question_seq_check check (question_seq between 1 and 1000);
alter table reviews drop constraint if exists reviews_question_seq_check;
alter table reviews add constraint reviews_question_seq_check check (question_seq between 1 and 1000);

alter table app_users add column if not exists interview_date date;
alter table app_users add column if not exists interview_company text;

create table if not exists question_stats (
  user_id uuid references app_users(id) on delete cascade,
  question_seq int not null check (question_seq between 1 and 1000),
  seconds int not null default 0 check (seconds >= 0),
  attempts int not null default 0,
  forgot_count int not null default 0,
  slow boolean not null default false,
  last_at timestamptz not null default now(),
  primary key (user_id, question_seq)
);

create table if not exists user_solutions (
  user_id uuid references app_users(id) on delete cascade,
  question_seq int not null check (question_seq between 1 and 1000),
  language text not null check (language in ('java','python')),
  code text not null default '' check (length(code) <= 20000),
  updated_at timestamptz not null default now(),
  primary key (user_id, question_seq, language)
);

alter table question_stats enable row level security;
alter table user_solutions enable row level security;
revoke all on question_stats, user_solutions from anon, authenticated;
```

If the first line reports that it cannot find the constraint, list the real names with: select conname from pg\_constraint where conrelid = 'progress'::regclass; and use the name it shows. The delete-my-data function from SRS 2.0 already removes the new tables’ rows too, because they are linked with on delete cascade.

### 9.2 New functions

The existing functions (get\_state, save\_progress, save\_review and the others) are not touched. The new functions reuse the existing \_auth helper.

```sql
create or replace function get_extras(p_username text, p_pin_hash text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v_id uuid; v app_users;
begin
  v_id := _auth(p_username, p_pin_hash);
  select * into v from app_users where id = v_id;
  return jsonb_build_object(
    'interview_date', v.interview_date,
    'interview_company', v.interview_company,
    'stats', coalesce((select jsonb_agg(to_jsonb(s) - 'user_id') from question_stats s where s.user_id = v_id), '[]'::jsonb),
    'solutions', coalesce((select jsonb_agg(distinct u.question_seq) from user_solutions u
                           where u.user_id = v_id and length(u.code) > 0), '[]'::jsonb));
end $$;

create or replace function save_stats(p_username text, p_pin_hash text, p_seq int,
  p_add_seconds int, p_new_attempt boolean, p_forgot boolean, p_slow boolean)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v_id uuid;
begin
  v_id := _auth(p_username, p_pin_hash);
  insert into question_stats(user_id, question_seq, seconds, attempts, forgot_count, slow, last_at)
  values (v_id, p_seq, greatest(coalesce(p_add_seconds, 0), 0),
    case when p_new_attempt then 1 else 0 end,
    case when p_forgot then 1 else 0 end,
    coalesce(p_slow, false), now())
  on conflict (user_id, question_seq) do update set
    seconds = question_stats.seconds + greatest(coalesce(p_add_seconds, 0), 0),
    attempts = question_stats.attempts + case when p_new_attempt then 1 else 0 end,
    forgot_count = question_stats.forgot_count + case when p_forgot then 1 else 0 end,
    slow = question_stats.slow or coalesce(p_slow, false),
    last_at = now();
  return jsonb_build_object('ok', true);
end $$;

create or replace function save_user_solution(p_username text, p_pin_hash text, p_seq int,
  p_language text, p_code text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v_id uuid;
begin
  v_id := _auth(p_username, p_pin_hash);
  if p_language not in ('java','python') then raise exception 'BAD_LANGUAGE'; end if;
  if length(coalesce(p_code, '')) > 20000 then raise exception 'CODE_TOO_LONG'; end if;
  insert into user_solutions(user_id, question_seq, language, code, updated_at)
  values (v_id, p_seq, p_language, coalesce(p_code, ''), now())
  on conflict (user_id, question_seq, language) do update set code = excluded.code, updated_at = now();
  return jsonb_build_object('ok', true);
end $$;

create or replace function get_user_solutions(p_username text, p_pin_hash text, p_seq int)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v_id uuid;
begin
  v_id := _auth(p_username, p_pin_hash);
  return coalesce((select jsonb_agg(jsonb_build_object('language', language, 'code', code, 'updated_at', updated_at))
                   from user_solutions where user_id = v_id and question_seq = p_seq), '[]'::jsonb);
end $$;

create or replace function save_interview(p_username text, p_pin_hash text, p_date date, p_company text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v_id uuid;
begin
  v_id := _auth(p_username, p_pin_hash);
  update app_users set interview_date = p_date, interview_company = nullif(trim(p_company), '') where id = v_id;
  return jsonb_build_object('ok', true);
end $$;

grant execute on function
  get_extras(text, text),
  save_stats(text, text, int, int, boolean, boolean, boolean),
  save_user_solution(text, text, int, text, text),
  get_user_solutions(text, text, int),
  save_interview(text, text, date, text)
to anon;
```

### 9.3 Front-end rules

- Existing calls stay as they are. The new data is loaded with get\_extras after sign in, and My code is loaded one question at a time with get\_user\_solutions.
- When the user taps Forgot on a review, the existing review call runs as before, and save\_stats is called in addition with p\_forgot set to true.
- Export in Settings includes the new data (stats, saved code, interview settings). Import accepts a version 2 file that has none of it.
- Error codes to show: BAD\_LANGUAGE (“Choose Java or Python.”) and CODE\_TOO\_LONG (“Your code is longer than 20,000 characters.”).

## 10. Pages and Responsive Rules for New and Changed Screens

All of this follows the design system, the three modes, the z-index scale, the portal rule for dropdowns and sheets, and the no-empty-area rule of SRS 2.0. Targets are at least 44 px, and no page scrolls sideways at any width.

| Element | Desktop (1200 px and up) | Tablet (768 to 1199 px) | Phone (below 768 px) |
| --- | --- | --- | --- |
| Activity card | 12-week grid fills the card, cells about 30 px, stats row of 3 | Same, cells about 28 px | Same, cells about 24 px, stats row stays 3 across with smaller text |
| Needs attention card | Below Activity in the right column, fills leftover height | Below Activity | Last card of Home, full width |
| Interview plan card | Right of the ring row on Home | Full width under the stat cards | Full width under the stat cards, target rows stacked |
| Part 1 / Part 2 switch | In the chapters card header | Same | Full-width two-part control at the top of the card |
| /companies grid | 3 columns | 2 columns | 2 columns, cards at least 150 px wide |
| Company page header | Logo and name on the left, ring on the right | Same | Logo and name, ring below, Start next full width |
| Asked at row | Under the Builds on card | Same | Same, logos 28 px, wraps |
| Company filter | Portal dropdown | Portal dropdown | Bottom sheet with search |
| Timer row | One row: time, Start, Pause, Reset, Attempts | Same | Time and Attempts on the first line, three buttons on the second, each 48 px high |
| Question page buttons | Six pills in one row | Six pills in one row | Grid 3 + 3 (Hints, then Approach, Code, My code) |
| My code panel | Editor, reference solution beside it | Editor, reference below | Editor full width, 14 lines tall, reference below |
| /stats | Two-column cards | Two-column cards | One column |

The Roadmap sidebar lists Part 1 and Part 2 under two group headings on desktop; on phone the chapter bottom sheet shows the same two groups. Navigation stays Home, Roadmap, Today, Settings.

## 11. Rollout and Safeguards

### 11.1 Order of work

1. Tag the deployed code v2.0. Create the branch v3.
2. Ask the owner to export their own progress from Settings (a safety copy).
3. Run the migration in section 9 in the Supabase SQL Editor, then confirm a v2 sign in still works.
4. Add the data files: questions 301 to 500, chapters 19 to 32, companies, solutions in 8 batches.
5. Build the changes in this order: activity card and Home layout, Roadmap Part 1 and Part 2, company logos and filter, company pages, timer and stats, My code, interview plan.
6. After each step, deploy the branch as a Vercel preview and run the regression checks.
7. Merge into main only when section 12 passes.

### 11.2 Feature switches

One file, src/config/features.ts, holds true or false for each of: part2Questions, companies, companyPrep, timerStats, mySolution, interviewPlan, activityV2. Each flag removes its feature from the screens when set to false and leaves everything else unchanged.

### 11.3 Rollback

Set a flag to false, or promote the previous deployment from the Vercel dashboard. The database changes are additive, so no database rollback is needed.

## 12. Acceptance Criteria

1. Every check of SRS 2.0 section 9 and SRS 1.0 section 12 still passes.
2. A user with progress from version 2 signs in and finds the same done questions, reviews, notes and streak. The ring now shows done out of 500.
3. The entries for questions 1 to 300 (data and solutions) are identical before and after, compared by file hash.
4. Marking Seq 301 and Seq 500 as Done saves and survives a refresh.
5. The Roadmap shows 32 chapters under Part 1 and Part 2; the chapter sizes match section 3.2 and add up to 500.
6. In questions.json all 500 LeetCode numbers and link names are unique, every builds on is smaller than its Seq, and chapters 19 to 32 are contiguous.
7. Every new question has Brute force and Optimal in Java and Python and three hints, with Brute force first.
8. The Activity card grid fills the card width at 360, 390, 768, 1024, 1440 and 1920 px, has exactly 84 cells, has correct Mon, Wed, Fri and month labels, a ringed today, dashed future days, the stats row and the tooltip, and has no empty area.
9. On Home the left and right columns end on the same line, and no block is blank.
10. The Asked at row appears only for tagged questions; a failed logo shows a letter chip; nothing shifts while logos load.
11. The Company filter and the company pages show only tagged questions; readiness is done divided by tagged; Start next opens the right question.
12. The timer starts, pauses, pauses when the tab is hidden, keeps its total after a refresh, and shows the slow toast at the right limits.
13. Needs attention shows the top 3 chapters with the right reasons from test data, and the empty state for a new user.
14. The Stats page numbers match the data.
15. My code saves, keeps Java and Python apart, copies, stops at 20,000 characters with a message, survives a refresh and never runs.
16. Interview plan: 100 unsolved questions and 10 days left gives a target of 10; the target changes the next day; a company choice limits the pool; Clear works; a past date shows its message.
17. Every new or changed screen passes at 360, 390 and 430 px and at 1440 px in all three modes, with no sideways scroll, 44 px targets and nothing hidden by the bars.
18. Setting any feature flag to false removes that feature and nothing else breaks.
19. Export contains the new data, and a version 2 export file still imports.
20. Text contrast is at least 4.5 to 1 in all three modes.

## Appendix A: New Question Catalogue (Seq 301 to 500)

Columns are the same as in SRS 1.0 Appendix A. LeetCode link: https://leetcode.com/problems/ followed by the link name and a slash. The numbers and link names were written from memory and have not been checked on leetcode.com; the build must write any mismatch to data-warnings.md and keep going. Builds on uses Seq numbers.

### Chapter 19: Arrays & Hashing II (Seq 301 to 314)

| Seq | LC | Title | Slug | Diff | Builds on | Brute force | Optimal | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 301 | 219 | Contains Duplicate II | contains-duplicate-ii | E | #1 | Compare every pair within distance k | Sliding window set, or a map of last index | O(nk) → O(n) |
| 302 | 349 | Intersection of Two Arrays | intersection-of-two-arrays | E | #301 | Compare every pair | Two sets | O(mn) → O(m+n) |
| 303 | 350 | Intersection of Two Arrays II | intersection-of-two-arrays-ii | E | #302 | Compare and remove matches | Count map, or sort with two pointers | O(mn) → O(m+n) |
| 304 | 1207 | Unique Number of Occurrences | unique-number-of-occurrences | E | #303 | Count each value by scanning | Count map plus a set of the counts | O(n²) → O(n) |
| 305 | 448 | Find All Numbers Disappeared in an Array | find-all-numbers-disappeared-in-an-array | E | #13 | Set of seen numbers | Mark seen by negating a\[abs(x)−1\] | O(n) space → O(1) space |
| 306 | 645 | Set Mismatch | set-mismatch | E | #305 | Count map | Negation marking, or sum formulas | O(n) space → O(1) space |
| 307 | 485 | Max Consecutive Ones | max-consecutive-ones | E | #306 | Check every start | One pass with a running count | O(n²) → O(n) |
| 308 | 665 | Non-decreasing Array | non-decreasing-array | M | #307 | Try changing each element | One pass, fix at the first drop | O(n²) → O(n) |
| 309 | 581 | Shortest Unsorted Continuous Subarray | shortest-unsorted-continuous-subarray | M | #308 | Sort a copy and compare | Scan with running max and min for the two ends | O(n log n) → O(n) |
| 310 | 1480 | Running Sum of 1d Array | running-sum-of-1d-array | E | #9 | Re-sum for each index | Prefix sum | O(n²) → O(n) |
| 311 | 303 | Range Sum Query - Immutable | range-sum-query-immutable | E | #310 | Sum the range on every query | Prefix sums, answer each query in O(1) | O(n) per query → O(1) |
| 312 | 304 | Range Sum Query 2D - Immutable | range-sum-query-2d-immutable | M | #311 | Sum the rectangle on every query | 2D prefix sums | O(mn) per query → O(1) |
| 313 | 724 | Find Pivot Index | find-pivot-index | E | #310 | Sum both sides for each index | Total sum and a running left sum | O(n²) → O(n) |
| 314 | 523 | Continuous Subarray Sum | continuous-subarray-sum | M | #11 | Check every subarray | Prefix remainder map with first index | O(n²) → O(n) |

### Chapter 20: Strings (Seq 315 to 328)

| Seq | LC | Title | Slug | Diff | Builds on | Brute force | Optimal | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 315 | 387 | First Unique Character in a String | first-unique-character-in-a-string | E | #3 | For each letter scan the whole string | Count letters, then find the first with count 1 | O(n²) → O(n) |
| 316 | 383 | Ransom Note | ransom-note | E | #315 | Remove matching letters one by one | Count letters in a 26-slot array | O(mn) → O(m+n) |
| 317 | 205 | Isomorphic Strings | isomorphic-strings | E | #316 | Try all letter mappings | Two maps in one pass | exponential → O(n) |
| 318 | 290 | Word Pattern | word-pattern | E | #317 | Try all mappings | Two maps in one pass | exponential → O(n) |
| 319 | 409 | Longest Palindrome | longest-palindrome | E | #316 | Try every arrangement | Count letters; use pairs, add 1 for an odd count | exponential → O(n) |
| 320 | 58 | Length of Last Word | length-of-last-word | E | #319 | Split into words | Scan from the end | O(n) space → O(1) space |
| 321 | 13 | Roman to Integer | roman-to-integer | E | #320 | Long if-chains for symbol pairs | Value map; subtract when a smaller value comes before a larger one | O(n) both, simpler |
| 322 | 12 | Integer to Roman | integer-to-roman | M | #321 | If-chains for each digit | Greedy over a value table (1000, 900, down to 1) | O(1) bounded |
| 323 | 67 | Add Binary | add-binary | E | #322 | Convert to integers (overflows) | Add from the end with a carry | overflow risk → O(max(m,n)) |
| 324 | 415 | Add Strings | add-strings | E | #323 | Convert to integers (overflows) | Add digit by digit with a carry | overflow risk → O(max(m,n)) |
| 325 | 43 | Multiply Strings | multiply-strings | M | #324 | Repeated addition | School multiplication into a result array | huge → O(mn) |
| 326 | 151 | Reverse Words in a String | reverse-words-in-a-string | M | #320 | Split, reverse, join | Reverse everything, then each word, in a char array | O(n) space → O(1) extra |
| 327 | 6 | Zigzag Conversion | zigzag-conversion | M | #326 | Build the full grid | One list per row, bounce the row index | O(n·rows) → O(n) |
| 328 | 28 | Find the Index of the First Occurrence in a String | find-the-index-of-the-first-occurrence-in-a-string | E | #327 | Compare at every start | KMP prefix table | O(nm) → O(n+m) |

### Chapter 21: Two Pointers & Sliding Window II (Seq 329 to 342)

| Seq | LC | Title | Slug | Diff | Builds on | Brute force | Optimal | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 329 | 344 | Reverse String | reverse-string | E | #22 | Copy into a new reversed array | Swap with two pointers | O(n) space → O(1) space |
| 330 | 345 | Reverse Vowels of a String | reverse-vowels-of-a-string | E | #329 | Collect vowels, then refill in reverse | Two pointers that skip consonants | O(n) space → O(1) extra |
| 331 | 27 | Remove Element | remove-element | E | #30 | Copy to a new list | Slow and fast pointers in place | O(n) space → O(1) space |
| 332 | 88 | Merge Sorted Array | merge-sorted-array | E | #84 | Copy and sort everything | Two pointers filling from the back | O((m+n) log(m+n)) → O(m+n) |
| 333 | 392 | Is Subsequence | is-subsequence | E | #331 | Generate all subsequences | Two pointers | exponential → O(n) |
| 334 | 1679 | Max Number of K-Sum Pairs | max-number-of-k-sum-pairs | M | #24 | Check every pair | Sort and two pointers, or a count map | O(n²) → O(n log n) |
| 335 | 881 | Boats to Save People | boats-to-save-people | M | #334 | Try all pairings | Sort, pair the heaviest with the lightest | exponential → O(n log n) |
| 336 | 633 | Sum of Square Numbers | sum-of-square-numbers | M | #24 | Try every a and b | Two pointers from 0 and the square root of c | O(c) → O(√c) |
| 337 | 1456 | Maximum Number of Vowels in a Substring of Given Length | maximum-number-of-vowels-in-a-substring-of-given-length | M | #37 | Count vowels in every window | Fixed window slide | O(nk) → O(n) |
| 338 | 1423 | Maximum Points You Can Obtain from Cards | maximum-points-you-can-obtain-from-cards | M | #337 | Recursion over left or right picks | Slide a window of k cards from both ends | O(2ᵏ) → O(k) |
| 339 | 1493 | Longest Subarray of 1's After Deleting One Element | longest-subarray-of-1s-after-deleting-one-element | M | #45 | Try deleting each element | Window with at most one zero | O(n²) → O(n) |
| 340 | 1695 | Maximum Erasure Value | maximum-erasure-value | M | #38 | Check every subarray for repeats | Window with a set and a running sum | O(n²) → O(n) |
| 341 | 1658 | Minimum Operations to Reduce X to Zero | minimum-operations-to-reduce-x-to-zero | M | #42 | Recursion taking from either end | Longest middle window with sum = total − x | O(2ⁿ) → O(n) |
| 342 | 1838 | Frequency of the Most Frequent Element | frequency-of-the-most-frequent-element | M | #341 | Try every target value | Sort, window whose cost is at most k | O(n²) → O(n log n) |

### Chapter 22: Binary Search II (Seq 343 to 354)

| Seq | LC | Title | Slug | Diff | Builds on | Brute force | Optimal | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 343 | 744 | Find Smallest Letter Greater Than Target | find-smallest-letter-greater-than-target | E | #51 | Linear scan | Upper-bound binary search | O(n) → O(log n) |
| 344 | 441 | Arranging Coins | arranging-coins | E | #54 | Subtract row by row | Binary search on rows, or the quadratic formula | O(√n) → O(log n) |
| 345 | 1539 | Kth Missing Positive Number | kth-missing-positive-number | E | #343 | Walk the numbers and count the missing ones | Binary search on the missing count at each index | O(n+k) → O(log n) |
| 346 | 852 | Peak Index in a Mountain Array | peak-index-in-a-mountain-array | M | #59 | Linear scan | Binary search on the slope | O(n) → O(log n) |
| 347 | 658 | Find K Closest Elements | find-k-closest-elements | M | #346 | Sort by distance | Binary search the left edge of the window | O(n log n) → O(log n + k) |
| 348 | 1283 | Find the Smallest Divisor Given a Threshold | find-the-smallest-divisor-given-a-threshold | M | #63 | Try every divisor | Binary search on the divisor | O(n·max) → O(n log max) |
| 349 | 1760 | Minimum Limit of Balls in a Bag | minimum-limit-of-balls-in-a-bag | M | #348 | Try every limit | Binary search on the limit with a count check | O(n·max) → O(n log max) |
| 350 | 2300 | Successful Pairs of Spells and Potions | successful-pairs-of-spells-and-potions | M | #343 | Check every spell and potion | Sort potions, binary search per spell | O(nm) → O((n+m) log m) |
| 351 | 2187 | Minimum Time to Complete Trips | minimum-time-to-complete-trips | M | #349 | Simulate time step by step | Binary search on time | O(T·n) → O(n log T) |
| 352 | 2226 | Maximum Candies Allocated to K Children | maximum-candies-allocated-to-k-children | M | #351 | Try every pile size | Binary search on the pile size | O(n·max) → O(n log max) |
| 353 | 981 | Time Based Key-Value Store | time-based-key-value-store | M | #350 | Scan the list of timestamps | Binary search over each key's timestamps | O(n) → O(log n) |
| 354 | 719 | Find K-th Smallest Pair Distance | find-k-th-smallest-pair-distance | H | #66 | List all pair distances and sort | Binary search on the distance with a two-pointer count | O(n² log n) → O(n log W) |

### Chapter 23: Stack & Queue II (Seq 355 to 368)

| Seq | LC | Title | Slug | Diff | Builds on | Brute force | Optimal | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 355 | 232 | Implement Queue using Stacks | implement-queue-using-stacks | E | #69 | Move everything on every operation | Two stacks; move only when the out-stack is empty | O(n) per op → O(1) amortised |
| 356 | 225 | Implement Stack using Queues | implement-stack-using-queues | E | #355 | Two queues, moving all items on each push | One queue: rotate it after each push | O(n) per push, less memory |
| 357 | 933 | Number of Recent Calls | number-of-recent-calls | E | #356 | Keep all calls and scan them | Queue; drop old calls from the front | O(n) → O(1) amortised |
| 358 | 1047 | Remove All Adjacent Duplicates In String | remove-all-adjacent-duplicates-in-string | E | #68 | Repeatedly scan and delete pairs | Stack | O(n²) → O(n) |
| 359 | 921 | Minimum Add to Make Parentheses Valid | minimum-add-to-make-parentheses-valid | M | #358 | Stack of brackets | Two counters (open and needed) | O(n) space → O(1) space |
| 360 | 1249 | Minimum Remove to Make Valid Parentheses | minimum-remove-to-make-valid-parentheses | M | #359 | Try removing every subset | Stack of indices; remove the unmatched | exponential → O(n) |
| 361 | 32 | Longest Valid Parentheses | longest-valid-parentheses | H | #360 | Check every substring | Stack of indices, or two-pass counters | O(n³) → O(n) |
| 362 | 224 | Basic Calculator | basic-calculator | H | #71 | Recursive parsing with string copies | Stack of signs and running results | O(n²) → O(n) |
| 363 | 946 | Validate Stack Sequences | validate-stack-sequences | M | #68 | Try all pop orders | Simulate with a stack | exponential → O(n) |
| 364 | 636 | Exclusive Time of Functions | exclusive-time-of-functions | M | #363 | Track every time unit | Stack of running calls and the previous timestamp | O(T) → O(n) |
| 365 | 1475 | Final Prices With a Special Discount in a Shop | final-prices-with-a-special-discount-in-a-shop | E | #72 | Scan right for each price | Monotonic stack | O(n²) → O(n) |
| 366 | 456 | 132 Pattern | 132-pattern | M | #74 | Check every triple | Monotonic stack from the right | O(n³) → O(n) |
| 367 | 907 | Sum of Subarray Minimums | sum-of-subarray-minimums | M | #76 | Minimum of every subarray | Previous and next smaller with a monotonic stack | O(n²) → O(n) |
| 368 | 1438 | Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit | longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit | M | #48 | Check every subarray | Window with two monotonic deques | O(n²) → O(n) |

### Chapter 24: Linked List & Design II (Seq 369 to 380)

| Seq | LC | Title | Slug | Diff | Builds on | Brute force | Optimal | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 369 | 203 | Remove Linked List Elements | remove-linked-list-elements | E | #90 | Copy kept values to a new list | Dummy head; skip matching nodes | O(n) space → O(1) space |
| 370 | 237 | Delete Node in a Linked List | delete-node-in-a-linked-list | M | #369 | Needs the head (it is not given) | Copy the next node's value and skip it | not possible → O(1) |
| 371 | 24 | Swap Nodes in Pairs | swap-nodes-in-pairs | M | #83 | Swap the values through an array | Rewire pointers pair by pair | O(n) space → O(1) space |
| 372 | 61 | Rotate List | rotate-list | M | #89 | Rotate by one, k times | Make a ring, cut at length − k | O(nk) → O(n) |
| 373 | 328 | Odd Even Linked List | odd-even-linked-list | M | #371 | Copy to arrays and rebuild | Two chains joined at the end | O(n) space → O(1) space |
| 374 | 86 | Partition List | partition-list | M | #373 | Partition in an array and rebuild | Two chains (small and large), then join | O(n) space → O(1) space |
| 375 | 92 | Reverse Linked List II | reverse-linked-list-ii | M | #83 | Array, reverse the section | Reverse the section in place | O(n) space → O(1) space |
| 376 | 1721 | Swapping Nodes in a Linked List | swapping-nodes-in-a-linked-list | M | #89 | Array indexes | Two pointers (the fast one leads by k) | two passes → one pass |
| 377 | 707 | Design Linked List | design-linked-list | M | #376 | Array copy on every operation | Singly linked list with a dummy head and a size | O(n) shifts → O(1) at the head |
| 378 | 706 | Design HashMap | design-hashmap | E | #377 | One huge array for all possible keys | Buckets with chaining | huge memory → O(1) average |
| 379 | 380 | Insert Delete GetRandom O(1) | insert-delete-getrandom-o1 | M | #378 | Scan a list on delete | Array plus map; swap with the last on delete | O(n) → O(1) |
| 380 | 1472 | Design Browser History | design-browser-history | M | #379 | List with full copies | Array and a current pointer; truncate on visit | O(n) per step → O(1) |

### Chapter 25: Backtracking II (Seq 381 to 394)

| Seq | LC | Title | Slug | Diff | Builds on | Brute force | Optimal | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 381 | 401 | Binary Watch | binary-watch | E | #102 | Try every time and count bits | Loop hours and minutes counting set bits, or backtrack over LEDs | O(720) both |
| 382 | 1079 | Letter Tile Possibilities | letter-tile-possibilities | M | #109 | Generate all sequences, dedupe with a set | Backtrack with letter counts | O(n!·n) → pruned |
| 383 | 526 | Beautiful Arrangement | beautiful-arrangement | M | #108 | All permutations, then check | Check each position as you place | O(n!·n) → pruned |
| 384 | 491 | Non-decreasing Subsequences | non-decreasing-subsequences | M | #103 | All subsets, filter and dedupe | Backtrack with a set per level | O(2ⁿ·n) → pruned |
| 385 | 967 | Numbers With Same Consecutive Differences | numbers-with-same-consecutive-differences | M | #111 | Check every n-digit number | Build digit by digit with plus or minus k | O(10ⁿ) → O(2ⁿ·10) |
| 386 | 1415 | The k-th Lexicographical String of All Happy Strings of a Given Length | the-k-th-lexicographical-string-of-all-happy-strings-of-a-given-length | M | #385 | Generate all and sort | Backtrack in order; stop at the k-th | all strings → stops early |
| 387 | 1239 | Maximum Length of a Concatenated String with Unique Characters | maximum-length-of-a-concatenated-string-with-unique-characters | M | #102 | All subsets, check each | Backtrack with a bitmask of used letters | O(2ⁿ·L) → pruned |
| 388 | 357 | Count Numbers with Unique Digits | count-numbers-with-unique-digits | M | #108 | Check every number | Count by digit length (combinatorics) | O(10ⁿ) → O(n) |
| 389 | 1219 | Path with Maximum Gold | path-with-maximum-gold | M | #115 | All paths without pruning | DFS from each gold cell with marking | exponential → pruned |
| 390 | 980 | Unique Paths III | unique-paths-iii | H | #389 | Try all walks | DFS counting visited free cells | exponential → pruned |
| 391 | 306 | Additive Number | additive-number | M | #390 | Try all splits blindly | Fix the first two numbers, then check the rest | O(n³) → O(n²·n) |
| 392 | 842 | Split Array into Fibonacci Sequence | split-array-into-fibonacci-sequence | M | #391 | All splits | Backtrack with 32-bit and leading-zero checks | exponential → pruned |
| 393 | 140 | Word Break II | word-break-ii | H | #246 | Try all splits | Backtrack with memo and a word set | O(2ⁿ) → memoised |
| 394 | 282 | Expression Add Operators | expression-add-operators | H | #393 | Try all operator strings, then evaluate | Backtrack tracking the value and the last operand | O(4ⁿ·n) → pruned |

# Software Requirements Specification

**DSA Roadmap Tracker**: a 300-question LeetCode study path

Version 1.0 · 14 November 2026 · Prepared for implementation in Antigravity

## 1. Introduction

### 1.1 Purpose

This document specifies a web app that guides one learner (and any number of other learners, each with a separate page) through **300 LeetCode questions in a fixed chain**. Each question builds on the one before it, so the learner never faces a random jump in difficulty or topic. Each question has a **brute force** and an **optimal** approach with code in **Java and Python**, a direct **LeetCode** button, and progress tracking with scheduling.

### 1.2 Scope

**In scope:** simple username login (optional PIN), roadmap of 18 chapters, question pages, status tracking, revisit scheduling with spaced repetition, Today page, progress dashboard, notes, filters, dark and light themes, deployment on Netlify with an online Supabase database.

**Out of scope (version 1):** algorithm visualizers, email or password authentication, social features, comments, payments, automatic syncing with a LeetCode account, a code editor or judge.

### 1.3 Definitions

| Term | Meaning |
| --- | --- |
| Seq | The question's position (1 to 300) in the chain. This is the primary key everywhere. |
| LC | The LeetCode problem number. |
| Slug | The last part of the LeetCode URL, e.g. two-sum. |
| Chain | The ordered list of 300 questions; each lists the earlier question it builds on. |
| Chapter | A group of related questions (18 in total). |
| Approach | Either Brute force or Optimal, each with idea, steps, code and complexity. |
| Review | A scheduled reminder to attempt a question again on a due date. |

## 2. Product Overview

### 2.1 Goals

1. Remove the decision of what to solve next: the chain decides.
2. Make revision automatic through scheduling and spaced repetition.
3. Let the learner compare a slow and a fast solution for every question, in their preferred language.
4. Keep it simple: no sign-up friction, fast pages, works on a phone.

### 2.2 Users

Students preparing for coding interviews. Each person types a username and gets their own progress. No admin role is needed.

### 2.3 Assumptions and constraints

- The 300 questions and all solution content ship with the site as static JSON files. Only user progress lives in the database.
- No premium-only LeetCode questions are used.
- Login has no real authentication. Anyone who knows a username (and its PIN, if set) can open that progress. This is accepted for version 1 and must be stated on the login page.
- Netlify hosts the site; Supabase (hosted Postgres) is the database.

## 3. Architecture and Tech Stack

| Layer | Choice |
| --- | --- |
| Front end | React with Vite, plain CSS using CSS variables for themes, React Router |
| Code display | Prism or Shiki for Java and Python highlighting |
| Static content | JSON files in /public/data, loaded per chapter on demand |
| Database | Supabase Postgres, accessed only through database functions (see 6.3) |
| Hosting | Netlify (static site, SPA redirect rule) |
| Client storage | localStorage for the session (username, PIN hash), language and theme |

## 4. Functional Requirements

Priority: P0 = must have, P1 = should have, P2 = nice to have.

| ID | Requirement | Priority |
| --- | --- | --- |
| FR-1 | Login page with one username field (3 to 20 characters: a to z, 0 to 9, underscore) and an optional 4-digit PIN. A new username creates the account; an existing one loads it; if a PIN was set it must match. | P0 |
| FR-2 | No email, password or OAuth. The session is remembered in localStorage until the user logs out. | P0 |
| FR-3 | Each user sees and changes only their own progress. | P0 |
| FR-4 | Roadmap page shows the 18 chapters as collapsible sections, each with a progress bar (done / total). Questions appear in seq order. | P0 |
| FR-5 | Each question row shows seq, title, difficulty chip, status chip, a Builds on link and a LeetCode icon button. | P0 |
| FR-6 | Each chapter has an intro card: why it follows the previous chapter and a 3 to 5 line pattern cheat sheet. | P1 |
| FR-7 | Filters by chapter, difficulty, status, needs revisit and mistake-tagged; search by title or LC number. | P1 |
| FR-8 | A Next up button (header and dashboard) opens the next question per rule 7.4. | P0 |
| FR-9 | Question page header: seq, LC number, title, difficulty, chapter, status selector, mistake toggle. | P0 |
| FR-10 | A LeetCode button opens https://leetcode.com/problems/{slug}/ in a new tab. | P0 |
| FR-11 | Question page shows Builds on and Leads to links and a one-sentence reason why this question comes here. | P0 |
| FR-12 | Two tabs, Brute force and Optimal. Each shows: the idea in plain words, numbered steps, code, time and space complexity. | P0 |
| FR-13 | A Java / Python switch applies to every question at once and is remembered per user. | P0 |
| FR-14 | Code blocks have syntax highlighting and a Copy button. | P1 |
| FR-15 | Personal notes per question with autosave (up to 2000 characters). | P1 |
| FR-16 | Previous and Next question buttons follow seq order. | P0 |
| FR-17 | Statuses: Todo, In progress, Done, Revisit. | P0 |
| FR-18 | Marking Done records solved\_at, adds to today's count, and offers a Remind me again checkbox (default on). | P0 |
| FR-19 | Revisit later opens a date picker (default tomorrow; quick picks: tomorrow, 3 days, 1 week). | P0 |
| FR-20 | Today page lists due and overdue reviews, today's solved count against the daily goal, and the Next up question. Each review has Recalled and Forgot buttons. | P0 |
| FR-21 | Spaced repetition follows rule 7.2. | P0 |
| FR-22 | Mistake tag: a toggle marking that the first attempt went wrong; such reviews are listed first. | P1 |
| FR-23 | Dashboard: overall progress ring, per-chapter bars, difficulty breakdown. | P1 |
| FR-24 | Streak counter and daily goal (1 to 10, default 2). | P1 |
| FR-25 | Activity grid for the last 12 weeks. | P2 |
| FR-26 | Dark theme (default) and light theme, remembered. | P0 |
| FR-27 | Responsive layout; bottom navigation on mobile. | P0 |
| FR-28 | Export and import of progress as a JSON file. | P2 |
| FR-29 | Loading and error states; updates appear instantly and roll back with a retry message if saving fails. | P0 |
| FR-30 | Log out, and Delete my data (removes the account and all rows). | P1 |

## 5. Screens

1. **Login:** app name, username field, optional PIN field, Enter button, a short note that there is no real authentication.
2. **Home (dashboard):** greeting, Next up card, today's goal progress, streak, due reviews count, overall ring, chapter bars.
3. **Roadmap:** filter bar, chapter sections, question rows.
4. **Question:** header, builds-on strip, LeetCode button, Brute force / Optimal tabs, language switch, notes box, status and schedule controls, previous and next buttons.
5. **Today:** due and overdue reviews, upcoming reviews (next 7 days), Next up.
6. **Settings:** daily goal, theme, export, import, log out, delete data.

Navigation: Home, Roadmap, Today, Settings in a top bar on desktop and a bottom bar on mobile. A Next up button stays visible in the header.

## 6. Data Model

### 6.1 Static content files

| File | Contents |
| --- | --- |
| /public/data/chapters.json | id, order, name, summary, whyNext, patterns (list of strings), seqFrom, seqTo |
| /public/data/questions.json | seq, lc, title, slug, difficulty, chapter, buildsOn, brute {idea, time}, optimal {idea, time}. Generated from Appendix A. |
| /public/data/solutions/ch-01.json to ch-18.json | Loaded when a chapter is opened. Per question: seq, whyNext, and for both brute and optimal: idea, steps (list), time, space, code {java, python}. |

Chapter order is data-driven (the order field), so it can be rearranged without changing code, and a user may open any chapter at any time.

### 6.2 Database tables (Supabase / Postgres)

```sql
create table app_users (
  id uuid primary key default gen_random_uuid(),
  username text unique not null check (username ~ '^[a-z0-9_]{3,20}$'),
  pin_hash text,
  daily_goal int not null default 2 check (daily_goal between 1 and 10),
  language text not null default 'java' check (language in ('java','python')),
  theme text not null default 'dark' check (theme in ('dark','light')),
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
```

A question with no row in progress is treated as todo.

### 6.3 Access without authentication

The browser must never read or write the tables directly. All access goes through Postgres functions called with the Supabase anon key: login\_user(username, pin\_hash), get\_state(username, pin\_hash), save\_progress(...), save\_review(...), save\_settings(...), delete\_user(...). Each function verifies the username and PIN hash, then touches only that user's rows. Row-level security is enabled on every table with no policy for the anon role, so direct table access is denied. The PIN hash is SHA-256 of username plus PIN, computed in the browser. This keeps casual visitors out but is not strong security; the login page says so.

## 7. Business Rules

### 7.1 Status rules

- Any status can change to any other.
- Done sets solved\_at the first time only and adds 1 to today's activity count (not again if the same question is re-marked on the same day).
- Revisit requires a due date and creates a manual review.
- Moving a question out of Done does not delete its review; the user can remove a review from the Today page.

### 7.2 Spaced repetition

Intervals in days: 1, 3, 7, 21.

- Done with Remind me again checked creates a review with step 0 and due date today + 1.
- Recalled on a review at step s: if s is the last step (3) the review is deleted; otherwise step becomes s + 1 and the due date moves forward by the interval for the new step (3, 7, then 21 days).
- Forgot: step returns to 0, due date is tomorrow, and the mistake tag is set.
- A manual review (Revisit) uses the chosen date, then follows the same Recalled and Forgot rules, starting at step 0.
- Overdue reviews stay on the Today page until answered. Dates use the user's local calendar day.

### 7.3 Streak and daily goal

A day counts toward the streak when solved\_count is at least 1. The streak is the number of consecutive days up to today (or yesterday, if today has no solve yet) with a count of at least 1. The daily goal only drives the progress display and does not affect the streak.

### 7.4 Next up

Next up is the lowest seq whose status is todo or in progress and which has no future-dated manual review. If the user has chosen a chapter filter, it searches within that chapter first. If everything is done, show a completion message.

### 7.5 Chain integrity

For every question, buildsOn is smaller than seq. Chapters cover contiguous seq ranges with no gaps or overlaps. Every LC number and every slug appears once.

## 8. Non-Functional Requirements

| Area | Requirement |
| --- | --- |
| Performance | First page interactive within 2 seconds on a typical mobile connection; questions.json under 120 KB compressed; solution files loaded per chapter. |
| Reliability | Optimistic updates with rollback; no data loss when a request fails. |
| Usability | Every page reachable in at most 2 clicks from Home; keyboard accessible; visible focus states; colour contrast at least 4.5 to 1 in both themes. |
| Compatibility | Latest two versions of Chrome, Edge, Safari and Firefox; phones from 360 px width. |
| Security | Database functions only (see 6.3); anon key in environment variables; no secrets in the repository; notes are plain text and are escaped when displayed. |
| Maintainability | Content separate from code; adding or editing a question needs only JSON changes. |

## 9. Deployment

1. Create a Supabase project and run the SQL in 6.2 together with the functions in 6.3. Enable row-level security on all four tables.
2. Put the site in a Git repository and connect it to Netlify.
3. Build command: npm run build. Publish directory: dist.
4. Environment variables: VITE\_SUPABASE\_URL and VITE\_SUPABASE\_ANON\_KEY.
5. Add a netlify.toml rule so that every path returns index.html (single-page app): from /\* to /index.html with status 200.
6. Deploy. Test with two different usernames to confirm progress is separate.

## 10. Content Specification

### 10.1 Each solution entry has

Idea in 1 to 3 plain sentences; numbered steps; code in Java and Python; time and space complexity; for brute force, one sentence on why it is too slow.

### 10.2 Reference entry: Two Sum (Seq 2, LC 1)

**Brute force:** check every pair. Time O(n²), space O(1).

```java
class Solution {
    public int[] twoSum(int[] nums, int target) {
        for (int i = 0; i < nums.length; i++) {
            for (int j = i + 1; j < nums.length; j++) {
                if (nums[i] + nums[j] == target) return new int[]{i, j};
            }
        }
        return new int[]{};
    }
}
```

```python
class Solution:
    def twoSum(self, nums, target):
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []
```

**Optimal:** store each value's index in a HashMap and look up the complement. Time O(n), space O(n).

```java
class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> seen = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int need = target - nums[i];
            if (seen.containsKey(need)) return new int[]{seen.get(need), i};
            seen.put(nums[i], i);
        }
        return new int[]{};
    }
}
```

```python
class Solution:
    def twoSum(self, nums, target):
        seen = {}
        for i, x in enumerate(nums):
            need = target - x
            if need in seen:
                return [seen[need], i]
            seen[x] = i
        return []
```

### 10.3 Authoring plan

The catalogue in Appendix A gives the one-line idea and complexity for every question. The full programs (brute and optimal, Java and Python, 1,200 programs in total) are written as separate JSON files in 12 batches of 25 questions: batch 1 is seq 1 to 25, batch 2 is 26 to 50, and so on up to batch 12 (276 to 300). They are merged into the chapter files in 6.1.

### 10.4 Quality checklist for every solution

1. Passes the sample cases on LeetCode and uses the same method signature.
2. Java uses class Solution with the LeetCode signature; Python uses class Solution.
3. Brute force and optimal differ in a way the learner can see (complexity or memory).
4. Complexity statements are correct for the code shown.
5. No premium-only questions.
6. Before generating questions.json, verify each LC number and slug against leetcode.com.

## 11. Chapter Map

| Chapter | Name | Seq | Why it comes here |
| --- | --- | --- | --- |
| 1 | Arrays and Hashing | 1 to 21 | Foundation: counting, prefix sums and in-place tricks used everywhere later. |
| 2 | Two Pointers | 22 to 35 | Uses array order; Two Sum becomes Two Sum II, then 3Sum and 4Sum. |
| 3 | Sliding Window | 36 to 49 | Two pointers moving together over subarrays and substrings. |
| 4 | Binary Search | 50 to 67 | Sorted order again, then searching on the answer itself. |
| 5 | Stack and Monotonic Stack | 68 to 82 | Next greater and span ideas that later reappear in trees and DP. |
| 6 | Linked List | 83 to 99 | Pointer skills, reusing slow and fast pointers. |
| 7 | Recursion and Backtracking | 100 to 120 | Builds the recursion habit needed for trees and DP; ends with Target Sum, the bridge into DP. |
| 8 | Binary Trees | 121 to 147 | Recursion on a structure; ends with House Robber III as a DP preview. |
| 9 | Binary Search Trees | 148 to 156 | Trees plus ordering. |
| 10 | Heap and Priority Queue | 157 to 170 | Kth element and streaming problems; follows sorting and BST order ideas. |
| 11 | Greedy | 171 to 187 | Local choices; uses sorting and heaps. |
| 12 | Intervals | 188 to 195 | Sorting plus greedy sweeps. |
| 13 | Graphs: BFS and DFS | 196 to 217 | Trees generalised: grids, shortest paths in unweighted graphs. |
| 14 | Graphs: Topological Sort, Union-Find, Shortest Paths | 218 to 234 | Advanced graph tools on top of BFS and DFS. |
| 15 | Dynamic Programming (1D) | 235 to 253 | Recursion with repeated work, fixed by memoisation. |
| 16 | Dynamic Programming (2D and Strings) | 254 to 277 | Grids, two-string problems, intervals and stock states. |
| 17 | Tries and Design | 278 to 286 | Prefix trees and cache design, building on trees, hashing and linked lists. |
| 18 | Bit Manipulation and Math | 287 to 300 | Compact tricks to finish the path. |

## 12. Acceptance Criteria

1. A new username with no PIN opens an empty account; logging in again with the same name returns the same progress.
2. A username with a PIN rejects a wrong PIN.
3. Two usernames never see each other's progress.
4. The roadmap shows exactly 300 questions in 18 chapters in seq order with correct counts per chapter.
5. The LeetCode button for every question opens the correct problem page.
6. The language switch changes code on every question and survives a refresh.
7. Marking a question Done updates the chapter bar, the dashboard and today's count immediately, and the change is still there after a refresh.
8. A Revisit question with a future date does not appear on Today until its due date.
9. Recalled moves a review through 1, 3, 7 and 21 days and deletes it after the last step; Forgot sets it to tomorrow and tags it as a mistake.
10. Next up returns the lowest-seq unfinished question and ignores questions scheduled for the future.
11. Dark mode is the default, light mode works, and the choice persists.
12. The site works at 360 px width.
13. Deleting data removes every row for that user.

## Appendix A: Question Catalogue (300 Questions)

Columns: Seq, LC number, Title, Slug, Difficulty (E, M, H), Builds on (seq of an earlier question), Brute force idea, Optimal idea, Time (brute → optimal). LeetCode link: https://leetcode.com/problems/ followed by the slug and a slash. Verify numbers and slugs when generating questions.json.

### Chapter 1: Arrays and Hashing (Seq 1 to 21)

| Seq | LC | Title | Slug | Diff | Builds on | Brute force | Optimal | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 217 | Contains Duplicate | contains-duplicate | E | none | Compare every pair | Add to a HashSet, stop on a repeat | O(n²) → O(n) |
| 2 | 1 | Two Sum | two-sum | E | #1 | Check every pair | HashMap of value to index, look up the complement | O(n²) → O(n) |
| 3 | 242 | Valid Anagram | valid-anagram | E | #2 | Sort both strings and compare | Count letters in a 26-slot array | O(n log n) → O(n) |
| 4 | 49 | Group Anagrams | group-anagrams | M | #3 | Compare each word with every group | Map keyed by sorted word or letter counts | O(n²k) → O(nk) |
| 5 | 347 | Top K Frequent Elements | top-k-frequent-elements | M | #4 | Count, then sort by frequency | Bucket sort by frequency | O(n log n) → O(n) |
| 6 | 169 | Majority Element | majority-element | E | #5 | HashMap counts or sort | Boyer–Moore voting | O(n) space → O(1) space |
| 7 | 229 | Majority Element II | majority-element-ii | M | #6 | HashMap counts | Boyer–Moore with two candidates | O(n) space → O(1) space |
| 8 | 238 | Product of Array Except Self | product-of-array-except-self | M | #7 | For each index multiply all others | Prefix and suffix products | O(n²) → O(n) |
| 9 | 560 | Subarray Sum Equals K | subarray-sum-equals-k | M | #8 | Sum every subarray | Prefix sums with a HashMap of counts | O(n²) → O(n) |
| 10 | 525 | Contiguous Array | contiguous-array | M | #9 | Check every subarray | Treat 0 as −1, map first index of each prefix | O(n²) → O(n) |
| 11 | 974 | Subarray Sums Divisible by K | subarray-sums-divisible-by-k | M | #9 | Sum every subarray | Count prefix remainders | O(n²) → O(n) |
| 12 | 128 | Longest Consecutive Sequence | longest-consecutive-sequence | M | #1 | Sort and scan | Set; start counting only at sequence starts | O(n log n) → O(n) |
| 13 | 442 | Find All Duplicates in an Array | find-all-duplicates-in-an-array | M | #1 | HashSet of seen values | Mark visited by negating a\[abs(x)−1\] | O(n) space → O(1) space |
| 14 | 287 | Find the Duplicate Number | find-the-duplicate-number | M | #13 | Sort or HashSet | Floyd cycle detection on indices | O(n log n) → O(n) |
| 15 | 41 | First Missing Positive | first-missing-positive | H | #13 | Put all in a set, test 1, 2, 3 and so on | Cyclic placement: put x at index x−1 | O(n) space → O(1) space |
| 16 | 36 | Valid Sudoku | valid-sudoku | M | #1 | Three separate passes (rows, columns, boxes) | One pass with row, column and box sets | O(n²) → O(n²) |
| 17 | 73 | Set Matrix Zeroes | set-matrix-zeroes | M | #16 | Copy the matrix and mark zeros | Use first row and column as markers | O(mn) space → O(1) space |
| 18 | 118 | Pascal's Triangle | pascals-triangle | E | #17 | Compute each value with the combination formula | Build each row from the previous row | O(n³) → O(n²) |
| 19 | 54 | Spiral Matrix | spiral-matrix | M | #18 | Visited matrix | Shrink four boundaries | O(mn) space → O(1) space |
| 20 | 48 | Rotate Image | rotate-image | M | #19 | Copy into a new matrix | Transpose, then reverse each row | O(n²) space → O(1) space |
| 21 | 189 | Rotate Array | rotate-array | M | #20 | Shift by one, k times | Reverse the whole array, then the two parts | O(nk) → O(n) |

### Chapter 2: Two Pointers (Seq 22 to 35)

| Seq | LC | Title | Slug | Diff | Builds on | Brute force | Optimal | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 22 | 125 | Valid Palindrome | valid-palindrome | E | #21 | Build a cleaned reverse and compare | Two pointers moving inward | O(n) space → O(1) space |
| 23 | 680 | Valid Palindrome II | valid-palindrome-ii | E | #22 | Try deleting each character | Two pointers; on a mismatch skip either side | O(n²) → O(n) |
| 24 | 167 | Two Sum II - Input Array Is Sorted | two-sum-ii-input-array-is-sorted | M | #2 | Check every pair | Two pointers from both ends | O(n²) → O(n) |
| 25 | 15 | 3Sum | 3sum | M | #24 | Three nested loops plus a set | Sort, fix one, two pointers | O(n³) → O(n²) |
| 26 | 16 | 3Sum Closest | 3sum-closest | M | #25 | Three nested loops | Sort, fix one, two pointers tracking the closest | O(n³) → O(n²) |
| 27 | 18 | 4Sum | 4sum | M | #25 | Four nested loops | Sort, fix two, two pointers | O(n⁴) → O(n³) |
| 28 | 11 | Container With Most Water | container-with-most-water | M | #24 | Try every pair | Move the pointer at the shorter line | O(n²) → O(n) |
| 29 | 42 | Trapping Rain Water | trapping-rain-water | H | #28 | For each bar scan for left and right max | Two pointers with running maximums | O(n²) → O(n) |
| 30 | 26 | Remove Duplicates from Sorted Array | remove-duplicates-from-sorted-array | E | #24 | Copy into a set or list | Slow and fast pointers in place | O(n) space → O(1) space |
| 31 | 283 | Move Zeroes | move-zeroes | E | #30 | Copy non-zeros to a new array | Slow and fast pointer swap | O(n) space → O(1) space |
| 32 | 75 | Sort Colors | sort-colors | M | #31 | Sort the array | Dutch national flag with three pointers | O(n log n) → O(n) |
| 33 | 844 | Backspace String Compare | backspace-string-compare | E | #22 | Build both strings with a stack | Two pointers from the end | O(n) space → O(1) space |
| 34 | 977 | Squares of a Sorted Array | squares-of-a-sorted-array | E | #24 | Square, then sort | Two pointers filling from the back | O(n log n) → O(n) |
| 35 | 31 | Next Permutation | next-permutation | M | #32 | Generate permutations in order | Find the pivot, swap with the next larger, reverse the tail | O(n!·n) → O(n) |

### Chapter 3: Sliding Window (Seq 36 to 49)

| Seq | LC | Title | Slug | Diff | Builds on | Brute force | Optimal | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 36 | 121 | Best Time to Buy and Sell Stock | best-time-to-buy-and-sell-stock | E | #28 | Try every buy and sell pair | Track the minimum price so far | O(n²) → O(n) |
| 37 | 643 | Maximum Average Subarray I | maximum-average-subarray-i | E | #36 | Re-sum every window | Slide a fixed window: add one, drop one | O(nk) → O(n) |
| 38 | 3 | Longest Substring Without Repeating Characters | longest-substring-without-repeating-characters | M | #37 | Check every substring for repeats | Window with a map of last seen index | O(n³) → O(n) |
| 39 | 424 | Longest Repeating Character Replacement | longest-repeating-character-replacement | M | #38 | Count each substring's most common letter | Window valid while length − maxFreq ≤ k | O(n²) → O(n) |
| 40 | 567 | Permutation in String | permutation-in-string | M | #37 | Generate all permutations of s1 | Fixed window with letter counts | O(n!) → O(n) |
| 41 | 438 | Find All Anagrams in a String | find-all-anagrams-in-a-string | M | #40 | Sort every window | Sliding count comparison | O(nk log k) → O(n) |
| 42 | 209 | Minimum Size Subarray Sum | minimum-size-subarray-sum | M | #37 | Sum every subarray | Grow right, shrink left while sum ≥ target | O(n²) → O(n) |
| 43 | 713 | Subarray Product Less Than K | subarray-product-less-than-k | M | #42 | Multiply every subarray | Window; add (right − left + 1) each step | O(n²) → O(n) |
| 44 | 904 | Fruit Into Baskets | fruit-into-baskets | M | #39 | Check every subarray for at most 2 types | Window with a count map | O(n²) → O(n) |
| 45 | 1004 | Max Consecutive Ones III | max-consecutive-ones-iii | M | #44 | Count zeros in every subarray | Window allowing at most k zeros | O(n²) → O(n) |
| 46 | 930 | Binary Subarrays With Sum | binary-subarrays-with-sum | M | #9 | Sum every subarray | Prefix-sum map, or atMost(goal) − atMost(goal−1) | O(n²) → O(n) |
| 47 | 76 | Minimum Window Substring | minimum-window-substring | H | #41 | Check every substring | Expand to cover, shrink to minimise | O(n²) → O(n) |
| 48 | 239 | Sliding Window Maximum | sliding-window-maximum | H | #37 | Scan each window for its max | Monotonic deque | O(nk) → O(n) |
| 49 | 992 | Subarrays with K Different Integers | subarrays-with-k-different-integers | H | #46 | Check every subarray | atMost(K) − atMost(K−1) | O(n²) → O(n) |

### Chapter 4: Binary Search (Seq 50 to 67)

| Seq | LC | Title | Slug | Diff | Builds on | Brute force | Optimal | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 50 | 704 | Binary Search | binary-search | E | #49 | Linear scan | Halve the range each step | O(n) → O(log n) |
| 51 | 35 | Search Insert Position | search-insert-position | E | #50 | Linear scan | Lower-bound binary search | O(n) → O(log n) |
| 52 | 278 | First Bad Version | first-bad-version | E | #51 | Test versions one by one | Binary search on the boundary | O(n) → O(log n) |
| 53 | 367 | Valid Perfect Square | valid-perfect-square | E | #52 | Try i·i for each i | Binary search the root | O(√n) → O(log n) |
| 54 | 69 | Sqrt(x) | sqrtx | E | #53 | Try i·i ≤ x upward | Binary search the answer | O(√x) → O(log x) |
| 55 | 34 | Find First and Last Position of Element in Sorted Array | find-first-and-last-position-of-element-in-sorted-array | M | #51 | Linear scan | Two binary searches (first and last) | O(n) → O(log n) |
| 56 | 33 | Search in Rotated Sorted Array | search-in-rotated-sorted-array | M | #50 | Linear scan | Decide which half is sorted each step | O(n) → O(log n) |
| 57 | 81 | Search in Rotated Sorted Array II | search-in-rotated-sorted-array-ii | M | #56 | Linear scan | Same, shrink both ends on duplicates | O(n) → O(log n) average |
| 58 | 153 | Find Minimum in Rotated Sorted Array | find-minimum-in-rotated-sorted-array | M | #56 | Linear scan | Compare mid with the right end | O(n) → O(log n) |
| 59 | 162 | Find Peak Element | find-peak-element | M | #58 | Linear scan | Move toward the larger neighbour | O(n) → O(log n) |
| 60 | 540 | Single Element in a Sorted Array | single-element-in-a-sorted-array | M | #59 | XOR everything | Binary search on pair parity | O(n) → O(log n) |
| 61 | 74 | Search a 2D Matrix | search-a-2d-matrix | M | #50 | Scan every cell | Treat as one sorted array | O(mn) → O(log mn) |
| 62 | 240 | Search a 2D Matrix II | search-a-2d-matrix-ii | M | #61 | Scan every cell | Staircase walk from top-right | O(mn) → O(m+n) |
| 63 | 875 | Koko Eating Bananas | koko-eating-bananas | M | #54 | Try every speed from 1 to max | Binary search on speed | O(n·max) → O(n log max) |
| 64 | 1011 | Capacity To Ship Packages Within D Days | capacity-to-ship-packages-within-d-days | M | #63 | Try every capacity | Binary search on capacity with a greedy check | O(n·sum) → O(n log sum) |
| 65 | 1482 | Minimum Number of Days to Make m Bouquets | minimum-number-of-days-to-make-m-bouquets | M | #64 | Try every day | Binary search on days with a count check | O(n·max) → O(n log max) |
| 66 | 410 | Split Array Largest Sum | split-array-largest-sum | H | #64 | Try every split with recursion | Binary search on the largest sum | exponential → O(n log sum) |
| 67 | 4 | Median of Two Sorted Arrays | median-of-two-sorted-arrays | H | #66 | Merge and pick the middle | Binary search the partition on the shorter array | O(m+n) → O(log min(m,n)) |

### Chapter 5: Stack and Monotonic Stack (Seq 68 to 82)

| Seq | LC | Title | Slug | Diff | Builds on | Brute force | Optimal | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 68 | 20 | Valid Parentheses | valid-parentheses | E | #33 | Repeatedly delete matching pairs | Stack of open brackets | O(n²) → O(n) |
| 69 | 155 | Min Stack | min-stack | M | #68 | Scan the stack for the minimum | Store (value, current min) pairs | O(n) getMin → O(1) |
| 70 | 150 | Evaluate Reverse Polish Notation | evaluate-reverse-polish-notation | M | #68 | Repeatedly find an operator and collapse | Operand stack | O(n²) → O(n) |
| 71 | 227 | Basic Calculator II | basic-calculator-ii | M | #70 | Two passes: multiply and divide first, then add and subtract | One pass with a stack | O(n) → O(n) |
| 72 | 496 | Next Greater Element I | next-greater-element-i | E | #68 | Scan right for each element | Monotonic stack plus a map | O(nm) → O(n+m) |
| 73 | 503 | Next Greater Element II | next-greater-element-ii | M | #72 | Circular scan for each element | Monotonic stack over 2n indices | O(n²) → O(n) |
| 74 | 739 | Daily Temperatures | daily-temperatures | M | #72 | Scan ahead for each day | Monotonic decreasing stack | O(n²) → O(n) |
| 75 | 901 | Online Stock Span | online-stock-span | M | #74 | Walk back for each price | Stack of (price, span) | O(n²) → O(n) |
| 76 | 84 | Largest Rectangle in Histogram | largest-rectangle-in-histogram | H | #74 | Expand around every bar | Monotonic increasing stack | O(n²) → O(n) |
| 77 | 85 | Maximal Rectangle | maximal-rectangle | H | #76 | Check every rectangle | Histogram per row | O(m²n²) → O(mn) |
| 78 | 402 | Remove K Digits | remove-k-digits | M | #74 | Try all removals | Greedy monotonic stack | exponential → O(n) |
| 79 | 853 | Car Fleet | car-fleet | M | #74 | Simulate time steps | Sort by position, stack of arrival times | O(n·T) → O(n log n) |
| 80 | 394 | Decode String | decode-string | M | #70 | Expand the innermost brackets repeatedly | Two stacks (counts and strings) | O(n²) → O(n·len) |
| 81 | 735 | Asteroid Collision | asteroid-collision | M | #80 | Simulate repeated passes | Stack of survivors | O(n²) → O(n) |
| 82 | 71 | Simplify Path | simplify-path | M | #81 | Manual string surgery | Split by slash and use a stack | O(n²) → O(n) |

### Chapter 6: Linked List (Seq 83 to 99)

| Seq | LC | Title | Slug | Diff | Builds on | Brute force | Optimal | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 83 | 206 | Reverse Linked List | reverse-linked-list | E | #82 | Copy to an array and rebuild | Flip pointers with prev and curr | O(n) space → O(1) space |
| 84 | 21 | Merge Two Sorted Lists | merge-two-sorted-lists | E | #83 | Dump into an array and sort | Two pointers with a dummy head | O(n log n) → O(n) |
| 85 | 876 | Middle of the Linked List | middle-of-the-linked-list | E | #83 | Count nodes, then walk n/2 | Slow and fast pointers | two passes → one pass |
| 86 | 141 | Linked List Cycle | linked-list-cycle | E | #85 | HashSet of visited nodes | Floyd slow and fast | O(n) space → O(1) space |
| 87 | 142 | Linked List Cycle II | linked-list-cycle-ii | M | #86 | HashSet of visited nodes | Floyd, then restart one pointer at the head | O(n) space → O(1) space |
| 88 | 160 | Intersection of Two Linked Lists | intersection-of-two-linked-lists | E | #86 | HashSet of nodes from list A | Two pointers that switch heads | O(n) space → O(1) space |
| 89 | 19 | Remove Nth Node From End of List | remove-nth-node-from-end-of-list | M | #85 | Count the length, then remove | Fast pointer n steps ahead, one pass | two passes → one pass |
| 90 | 83 | Remove Duplicates from Sorted List | remove-duplicates-from-sorted-list | E | #84 | HashSet of seen values | Skip equal next nodes | O(n) space → O(1) space |
| 91 | 82 | Remove Duplicates from Sorted List II | remove-duplicates-from-sorted-list-ii | M | #90 | Count map, then rebuild | Dummy head, skip whole duplicate runs | O(n) space → O(1) space |
| 92 | 234 | Palindrome Linked List | palindrome-linked-list | E | #85 | Copy to an array, compare the ends | Reverse the second half in place | O(n) space → O(1) space |
| 93 | 2 | Add Two Numbers | add-two-numbers | M | #84 | Convert to integers (overflows) | Digit by digit with a carry | overflow risk → O(max(m,n)) |
| 94 | 143 | Reorder List | reorder-list | M | #92 | Array with two indices | Find the middle, reverse, merge | O(n) space → O(1) space |
| 95 | 148 | Sort List | sort-list | M | #84 | Copy to an array and sort | Merge sort on the list | O(n) space → O(log n) space |
| 96 | 138 | Copy List with Random Pointer | copy-list-with-random-pointer | M | #83 | HashMap from old node to new node | Interleave copies, then split | O(n) space → O(1) space |
| 97 | 25 | Reverse Nodes in k-Group | reverse-nodes-in-k-group | H | #83 | Array, reverse chunks | Reverse each group in place | O(n) space → O(1) space |
| 98 | 23 | Merge k Sorted Lists | merge-k-sorted-lists | H | #84 | Collect all values and sort | Min-heap or divide and conquer | O(N log N) → O(N log k) |
| 99 | 146 | LRU Cache | lru-cache | M | #96 | Scan a list on every access | HashMap plus doubly linked list | O(n) → O(1) |

### Chapter 7: Recursion and Backtracking (Seq 100 to 120)

| Seq | LC | Title | Slug | Diff | Builds on | Brute force | Optimal | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100 | 509 | Fibonacci Number | fibonacci-number | E | #99 | Plain recursion | Memoisation or two variables | O(2ⁿ) → O(n) |
| 101 | 50 | Pow(x, n) | powx-n | M | #100 | Multiply n times | Fast exponentiation (square and halve) | O(n) → O(log n) |
| 102 | 78 | Subsets | subsets | M | #101 | Enumerate all bitmasks | Backtracking: take or leave each item | O(n·2ⁿ) → O(n·2ⁿ) |
| 103 | 90 | Subsets II | subsets-ii | M | #102 | Generate all, dedupe with a set | Sort; skip equal values at the same level | O(n·2ⁿ), less memory |
| 104 | 39 | Combination Sum | combination-sum | M | #102 | Try all subsets, filter by sum | Backtrack with start index and remaining sum | exponential → pruned |
| 105 | 40 | Combination Sum II | combination-sum-ii | M | #103 | All subsets, filter and dedupe | Sort; use each once; skip duplicates | exponential → pruned |
| 106 | 216 | Combination Sum III | combination-sum-iii | M | #104 | All subsets of 1 to 9 | Backtrack with k and n limits | O(2⁹) → pruned |
| 107 | 77 | Combinations | combinations | M | #102 | All subsets, keep size k | Backtrack with start index; stop at size k | O(2ⁿ) → O(C(n,k)·k) |
| 108 | 46 | Permutations | permutations | M | #107 | All nⁿ sequences, keep valid | used array or in-place swap | O(nⁿ) → O(n·n!) |
| 109 | 47 | Permutations II | permutations-ii | M | #108 | Use a set to remove duplicates | Sort; skip an equal value if the previous is unused | O(n·n!), less memory |
| 110 | 784 | Letter Case Permutation | letter-case-permutation | M | #102 | Iterative expansion | Backtrack: lower or upper at each letter | O(n·2ˡ) both |
| 111 | 17 | Letter Combinations of a Phone Number | letter-combinations-of-a-phone-number | M | #107 | Nested loops (depth fixed) | Backtrack by digit index | O(4ⁿ·n) both |
| 112 | 22 | Generate Parentheses | generate-parentheses | M | #111 | All 2²ⁿ strings, keep valid | Backtrack with open and close counts | O(2²ⁿ·n) → Catalan number |
| 113 | 131 | Palindrome Partitioning | palindrome-partitioning | M | #102 | All partitions, then check | Backtrack; cut only at palindromes | O(n·2ⁿ), pruned |
| 114 | 93 | Restore IP Addresses | restore-ip-addresses | M | #113 | Three nested cut loops | Backtrack segments of 1 to 3 digits | bounded by 3⁴ |
| 115 | 79 | Word Search | word-search | M | #114 | Try all paths without pruning | DFS with visited marking and early stop | O(mn·4ˡ) → pruned |
| 116 | 51 | N-Queens | n-queens | H | #108 | Try every placement of n queens | Row by row with column and diagonal sets | O(n²ⁿ) → O(n!) |
| 117 | 52 | N-Queens II | n-queens-ii | H | #116 | Same, building boards | Same, only count solutions | O(n!) both |
| 118 | 37 | Sudoku Solver | sudoku-solver | H | #116 | Try all digits everywhere | Backtrack with row, column and box masks | 9⁸¹ → pruned |
| 119 | 494 | Target Sum | target-sum | M | #102 | Recursion: choose plus or minus | Memoisation, or subset-sum DP on (sum+target)/2 | O(2ⁿ) → O(n·sum) |
| 120 | 698 | Partition to K Equal Sum Subsets | partition-to-k-equal-sum-subsets | M | #119 | Try all assignments to k buckets | Backtrack with sorted input, or bitmask memo | O(kⁿ) → O(n·2ⁿ) |

### Chapter 8: Binary Trees (Seq 121 to 147)

| Seq | LC | Title | Slug | Diff | Builds on | Brute force | Optimal | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 121 | 104 | Maximum Depth of Binary Tree | maximum-depth-of-binary-tree | E | #120 | BFS counting levels | Recursion: 1 + max(left, right) | O(n) both |
| 122 | 111 | Minimum Depth of Binary Tree | minimum-depth-of-binary-tree | E | #121 | Full recursion | BFS, stop at the first leaf | O(n), earlier exit |
| 123 | 226 | Invert Binary Tree | invert-binary-tree | E | #121 | BFS swapping children | Recursive swap | O(n) both |
| 124 | 100 | Same Tree | same-tree | E | #123 | Serialise both and compare | Recurse on both trees together | O(n) both |
| 125 | 101 | Symmetric Tree | symmetric-tree | E | #124 | Invert one copy and compare | Mirror recursion (left.left with right.right) | O(n) both |
| 126 | 110 | Balanced Binary Tree | balanced-binary-tree | E | #121 | Compute height at every node | Bottom-up, return −1 if unbalanced | O(n²) → O(n) |
| 127 | 543 | Diameter of Binary Tree | diameter-of-binary-tree | E | #126 | Heights of both sides at every node | One DFS with a global best | O(n²) → O(n) |
| 128 | 572 | Subtree of Another Tree | subtree-of-another-tree | E | #124 | isSame check at every node | Serialise both and string match | O(mn) → O(m+n) |
| 129 | 112 | Path Sum | path-sum | E | #121 | List all root-to-leaf paths, then sum | DFS subtracting from the target | O(n) both |
| 130 | 113 | Path Sum II | path-sum-ii | M | #129 | Collect every path, then filter | Backtracking with a path list | O(n²) worst case both |
| 131 | 257 | Binary Tree Paths | binary-tree-paths | E | #129 | Build every path string separately | DFS with the path built on the way | O(n·h) both |
| 132 | 437 | Path Sum III | path-sum-iii | M | #130 | Start a DFS from every node | Prefix-sum HashMap along the path | O(n²) → O(n) |
| 133 | 1448 | Count Good Nodes in Binary Tree | count-good-nodes-in-binary-tree | M | #129 | Check each node against its whole path | Pass the max so far downward | O(n·h) → O(n) |
| 134 | 124 | Binary Tree Maximum Path Sum | binary-tree-maximum-path-sum | H | #127 | Every node as the top, recompute gains | One DFS returning the best downward gain | O(n²) → O(n) |
| 135 | 102 | Binary Tree Level Order Traversal | binary-tree-level-order-traversal | M | #121 | DFS with a depth map | BFS by queue size | O(n) both |
| 136 | 199 | Binary Tree Right Side View | binary-tree-right-side-view | M | #135 | Level order, keep the last of each level | BFS, or DFS visiting right first | O(n) both |
| 137 | 103 | Binary Tree Zigzag Level Order Traversal | binary-tree-zigzag-level-order-traversal | M | #135 | Level order, reverse alternate levels | Deque with a flipping direction | O(n) both |
| 138 | 94 | Binary Tree Inorder Traversal | binary-tree-inorder-traversal | E | #121 | Recursion | Iterative stack, or Morris traversal | O(h) space → O(1) space |
| 139 | 144 | Binary Tree Preorder Traversal | binary-tree-preorder-traversal | E | #138 | Recursion | Iterative stack | O(n) both |
| 140 | 105 | Construct Binary Tree from Preorder and Inorder Traversal | construct-binary-tree-from-preorder-and-inorder-traversal | M | #139 | Linear search for the root in inorder each time | HashMap from value to inorder index | O(n²) → O(n) |
| 141 | 236 | Lowest Common Ancestor of a Binary Tree | lowest-common-ancestor-of-a-binary-tree | M | #129 | Store both root paths and compare | Single DFS returning found nodes | O(n) both, less memory |
| 142 | 114 | Flatten Binary Tree to Linked List | flatten-binary-tree-to-linked-list | M | #139 | Preorder list, then rebuild | Rewire using the rightmost node of the left subtree | O(n) space → O(1) space |
| 143 | 297 | Serialize and Deserialize Binary Tree | serialize-and-deserialize-binary-tree | H | #140 | Level order with null markers | Preorder with null markers | O(n) both |
| 144 | 863 | All Nodes Distance K in Binary Tree | all-nodes-distance-k-in-binary-tree | M | #141 | Search from every node | Parent map plus BFS from the target | O(n²) → O(n) |
| 145 | 662 | Maximum Width of Binary Tree | maximum-width-of-binary-tree | M | #135 | Level order including null nodes | Index nodes like a heap; width = last − first + 1 | O(2ʰ) → O(n) |
| 146 | 222 | Count Complete Tree Nodes | count-complete-tree-nodes | E | #121 | Visit all nodes | Compare left and right heights | O(n) → O(log² n) |
| 147 | 337 | House Robber III | house-robber-iii | M | #132 | Recursion with repeated subproblems | Return a (rob, skip) pair per node | exponential → O(n) |

### Chapter 9: Binary Search Trees (Seq 148 to 156)

| Seq | LC | Title | Slug | Diff | Builds on | Brute force | Optimal | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 148 | 700 | Search in a Binary Search Tree | search-in-a-binary-search-tree | E | #147 | Search the whole tree | Go left or right using the order | O(n) → O(h) |
| 149 | 98 | Validate Binary Search Tree | validate-binary-search-tree | M | #148 | Compare each node with its whole subtree | Pass (low, high) bounds, or check inorder order | O(n²) → O(n) |
| 150 | 701 | Insert into a Binary Search Tree | insert-into-a-binary-search-tree | M | #148 | Rebuild from the sorted values | Walk down and attach a new leaf | O(n) → O(h) |
| 151 | 450 | Delete Node in a BST | delete-node-in-a-bst | M | #150 | Rebuild without the key | Replace with the successor or predecessor | O(n) → O(h) |
| 152 | 230 | Kth Smallest Element in a BST | kth-smallest-element-in-a-bst | M | #138 | Inorder into a list, take index k−1 | Inorder with early stop | O(n) space → O(h) space |
| 153 | 235 | Lowest Common Ancestor of a Binary Search Tree | lowest-common-ancestor-of-a-binary-search-tree | M | #141 | Generic LCA | Walk using the BST order | O(n) → O(h) |
| 154 | 108 | Convert Sorted Array to Binary Search Tree | convert-sorted-array-to-binary-search-tree | E | #150 | Insert one by one (skewed tree) | Pick the middle as root recursively | O(n²) → O(n) |
| 155 | 173 | Binary Search Tree Iterator | binary-search-tree-iterator | M | #152 | Flatten the whole tree up front | Controlled inorder stack | O(n) space → O(h) space |
| 156 | 99 | Recover Binary Search Tree | recover-binary-search-tree | M | #149 | Inorder list, sort, rewrite | Find the two out-of-order nodes in one inorder pass | O(n log n) → O(n) |

### Chapter 10: Heap and Priority Queue (Seq 157 to 170)

| Seq | LC | Title | Slug | Diff | Builds on | Brute force | Optimal | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 157 | 703 | Kth Largest Element in a Stream | kth-largest-element-in-a-stream | E | #152 | Sort after every add | Min-heap of size k | O(n log n) → O(log k) per add |
| 158 | 215 | Kth Largest Element in an Array | kth-largest-element-in-an-array | M | #157 | Sort | Heap of size k, or quickselect | O(n log n) → O(n log k) |
| 159 | 1046 | Last Stone Weight | last-stone-weight | E | #157 | Re-sort every round | Max-heap | O(n² log n) → O(n log n) |
| 160 | 973 | K Closest Points to Origin | k-closest-points-to-origin | M | #158 | Sort all distances | Max-heap of size k, or quickselect | O(n log n) → O(n log k) |
| 161 | 692 | Top K Frequent Words | top-k-frequent-words | M | #5 | Count, then full sort | Heap with a frequency and alphabet comparator | O(n log n) → O(n log k) |
| 162 | 451 | Sort Characters By Frequency | sort-characters-by-frequency | M | #161 | Sort characters, then regroup | Count with buckets or a heap | O(n log n) → O(n) |
| 163 | 621 | Task Scheduler | task-scheduler | M | #159 | Simulate slot by slot | Greedy formula, or max-heap | O(n·idle) → O(n) |
| 164 | 767 | Reorganize String | reorganize-string | M | #163 | Try all permutations | Max-heap, alternate the top two | O(n!) → O(n log k) |
| 165 | 1054 | Distant Barcodes | distant-barcodes | M | #164 | Try all permutations | Heap, or fill even then odd slots by frequency | O(n!) → O(n log n) |
| 166 | 295 | Find Median from Data Stream | find-median-from-data-stream | H | #158 | Keep a sorted list by insertion | Two heaps (max-heap low half, min-heap high half) | O(n) per add → O(log n) |
| 167 | 378 | Kth Smallest Element in a Sorted Matrix | kth-smallest-element-in-a-sorted-matrix | M | #158 | Flatten and sort | Min-heap by rows, or binary search on value | O(n² log n) → O(k log n) |
| 168 | 373 | Find K Pairs with Smallest Sums | find-k-pairs-with-smallest-sums | M | #167 | All pairs, then sort | Min-heap expanding neighbours | O(mn log mn) → O(k log k) |
| 169 | 355 | Design Twitter | design-twitter | M | #98 | Collect all tweets and sort | Merge feeds with a heap of latest tweets | O(T log T) → O(F + 10 log F) |
| 170 | 502 | IPO | ipo | H | #166 | Rescan projects every round | Sort by capital plus a max-heap of profits | O(kn) → O(n log n) |

### Chapter 11: Greedy (Seq 171 to 187)

| Seq | LC | Title | Slug | Diff | Builds on | Brute force | Optimal | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 171 | 455 | Assign Cookies | assign-cookies | E | #170 | Try all pairings | Sort both, match greedily | O(n!) → O(n log n) |
| 172 | 860 | Lemonade Change | lemonade-change | E | #171 | Track every change combination | Greedy: give a 10 plus a 5 first | exponential → O(n) |
| 173 | 561 | Array Partition | array-partition | E | #171 | Try all pairings | Sort, sum every other element | O(n!) → O(n log n) |
| 174 | 976 | Largest Perimeter Triangle | largest-perimeter-triangle | E | #173 | Check all triples | Sort descending, first valid triple | O(n³) → O(n log n) |
| 175 | 122 | Best Time to Buy and Sell Stock II | best-time-to-buy-and-sell-stock-ii | M | #36 | Recursion over buy and sell | Add every upward step | O(2ⁿ) → O(n) |
| 176 | 53 | Maximum Subarray | maximum-subarray | M | #175 | Sum every subarray | Kadane's algorithm | O(n²) → O(n) |
| 177 | 918 | Maximum Sum Circular Subarray | maximum-sum-circular-subarray | M | #176 | Try every circular start | max(Kadane, total − minimum Kadane) | O(n²) → O(n) |
| 178 | 55 | Jump Game | jump-game | M | #176 | Recursion over all jumps | Track the farthest reachable index | O(2ⁿ) → O(n) |
| 179 | 45 | Jump Game II | jump-game-ii | M | #178 | DP over all jumps | Greedy window (BFS levels) | O(n²) → O(n) |
| 180 | 134 | Gas Station | gas-station | M | #179 | Try each start | One pass with total and tank | O(n²) → O(n) |
| 181 | 135 | Candy | candy | H | #180 | Repeatedly fix violations | Left pass, then right pass | O(n²) → O(n) |
| 182 | 763 | Partition Labels | partition-labels | M | #181 | Try every cut | Last-occurrence map, extend the end | O(n²) → O(n) |
| 183 | 316 | Remove Duplicate Letters | remove-duplicate-letters | M | #182 | Try all subsequences | Greedy stack with last index | exponential → O(n) |
| 184 | 330 | Patching Array | patching-array | H | #183 | Try all patch sets | Greedy: extend the reachable range | exponential → O(n + log target) |
| 185 | 1029 | Two City Scheduling | two-city-scheduling | M | #181 | Try all assignments | Sort by cost difference | O(2ⁿ) → O(n log n) |
| 186 | 406 | Queue Reconstruction by Height | queue-reconstruction-by-height | M | #185 | Try all orderings | Sort height descending, insert at index k | O(n!) → O(n²) |
| 187 | 678 | Valid Parenthesis String | valid-parenthesis-string | M | #68 | Recursion over the star choices | Track low and high open counts | O(3ⁿ) → O(n) |

### Chapter 12: Intervals (Seq 188 to 195)

| Seq | LC | Title | Slug | Diff | Builds on | Brute force | Optimal | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 188 | 56 | Merge Intervals | merge-intervals | M | #187 | Merge pairs repeatedly | Sort by start, then sweep | O(n²) → O(n log n) |
| 189 | 57 | Insert Interval | insert-interval | M | #188 | Append, then re-merge everything | Three phases: before, overlap, after | O(n log n) → O(n) |
| 190 | 435 | Non-overlapping Intervals | non-overlapping-intervals | M | #188 | Recursion over keep or drop | Sort by end, keep greedily | O(2ⁿ) → O(n log n) |
| 191 | 452 | Minimum Number of Arrows to Burst Balloons | minimum-number-of-arrows-to-burst-balloons | M | #190 | Try arrow positions | Sort by end, shoot at the end | exponential → O(n log n) |
| 192 | 986 | Interval List Intersections | interval-list-intersections | M | #188 | Compare all pairs | Two pointers on the sorted lists | O(mn) → O(m+n) |
| 193 | 1288 | Remove Covered Intervals | remove-covered-intervals | M | #188 | Compare all pairs | Sort by start ascending and end descending; track the max end | O(n²) → O(n log n) |
| 194 | 729 | My Calendar I | my-calendar-i | M | #188 | List and check all bookings | TreeMap floor and ceiling check | O(n) → O(log n) per booking |
| 195 | 1094 | Car Pooling | car-pooling | M | #194 | Simulate every kilometre | Difference array or sweep line | O(n·L) → O(n log n) |

### Chapter 13: Graphs, BFS and DFS (Seq 196 to 217)

| Seq | LC | Title | Slug | Diff | Builds on | Brute force | Optimal | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 196 | 733 | Flood Fill | flood-fill | E | #115 | Repeated passes until nothing changes | DFS or BFS from the start cell | O((mn)²) → O(mn) |
| 197 | 200 | Number of Islands | number-of-islands | M | #196 | Repeated scans to merge land | DFS or BFS flooding each unseen land cell | O((mn)²) → O(mn) |
| 198 | 695 | Max Area of Island | max-area-of-island | M | #197 | Re-scan for each island | DFS returning the area | O((mn)²) → O(mn) |
| 199 | 463 | Island Perimeter | island-perimeter | E | #197 | Count neighbours using a copied grid | Count 4 minus shared edges | O(mn) both |
| 200 | 130 | Surrounded Regions | surrounded-regions | M | #197 | Flood each region, test if it touches the border | Flood from the border, flip the rest | O((mn)²) → O(mn) |
| 201 | 417 | Pacific Atlantic Water Flow | pacific-atlantic-water-flow | M | #200 | DFS from every cell to both oceans | Reverse flow from each ocean's border | O((mn)²) → O(mn) |
| 202 | 1020 | Number of Enclaves | number-of-enclaves | M | #200 | Test each region for a border touch | Flood border land, count the rest | O((mn)²) → O(mn) |
| 203 | 994 | Rotting Oranges | rotting-oranges | M | #197 | Re-scan the grid every minute | Multi-source BFS | O((mn)²) → O(mn) |
| 204 | 542 | 01 Matrix | 01-matrix | M | #203 | BFS from every cell | Multi-source BFS from all zeros | O((mn)²) → O(mn) |
| 205 | 1091 | Shortest Path in Binary Matrix | shortest-path-in-binary-matrix | M | #204 | DFS over all paths | BFS with 8 directions | exponential → O(n²) |
| 206 | 127 | Word Ladder | word-ladder | H | #205 | DFS over all transformation paths | BFS with wildcard buckets | exponential → O(N·L²) |
| 207 | 133 | Clone Graph | clone-graph | M | #197 | Naive copy (loops forever on cycles) | DFS or BFS with an old-to-new map | not workable → O(V+E) |
| 208 | 785 | Is Graph Bipartite? | is-graph-bipartite | M | #207 | Try all two-colourings | BFS or DFS two-colouring | O(2ⁿ) → O(V+E) |
| 209 | 886 | Possible Bipartition | possible-bipartition | M | #208 | Try all splits | Build the graph, then two-colour | O(2ⁿ) → O(V+E) |
| 210 | 841 | Keys and Rooms | keys-and-rooms | M | #207 | Repeated scans for new keys | DFS or BFS from room 0 | O(n²) → O(V+E) |
| 211 | 547 | Number of Provinces | number-of-provinces | M | #197 | Merge by repeated scanning | DFS, BFS or Union-Find | O(n³) → O(n²) |
| 212 | 1971 | Find if Path Exists in Graph | find-if-path-exists-in-graph | E | #210 | DFS over all paths | BFS or DFS with visited, or Union-Find | exponential → O(V+E) |
| 213 | 797 | All Paths From Source to Target | all-paths-from-source-to-target | M | #212 | Generate all paths, then filter | DFS backtracking on a DAG | O(2ⁿ·n) both |
| 214 | 934 | Shortest Bridge | shortest-bridge | M | #204 | BFS from each land cell | DFS the first island, then multi-source BFS | O((mn)²) → O(mn) |
| 215 | 399 | Evaluate Division | evaluate-division | M | #207 | Try all equation chains | Weighted graph DFS or BFS, or Union-Find | exponential → O(Q·(V+E)) |
| 216 | 752 | Open the Lock | open-the-lock | M | #206 | DFS over all combinations | BFS over the 10⁴ states, skip dead ends | exponential → O(10⁴) |
| 217 | 310 | Minimum Height Trees | minimum-height-trees | M | #212 | BFS from every node | Peel leaves layer by layer | O(n²) → O(n) |

### Chapter 14: Graphs, Topological Sort, Union-Find and Shortest Paths (Seq 218 to 234)

| Seq | LC | Title | Slug | Diff | Builds on | Brute force | Optimal | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 218 | 207 | Course Schedule | course-schedule | M | #217 | DFS from each node to find cycles | Kahn's topological sort | O(V·(V+E)) → O(V+E) |
| 219 | 210 | Course Schedule II | course-schedule-ii | M | #218 | Repeated scans for zero in-degree | Kahn's order | O(V²) → O(V+E) |
| 220 | 802 | Find Eventual Safe States | find-eventual-safe-states | M | #218 | DFS from each node | Reverse graph topological sort, or colour DFS | O(V·(V+E)) → O(V+E) |
| 221 | 329 | Longest Increasing Path in a Matrix | longest-increasing-path-in-a-matrix | H | #220 | DFS from each cell | DFS with memo, or topological sort | exponential → O(mn) |
| 222 | 684 | Redundant Connection | redundant-connection | M | #211 | DFS cycle check for each edge | Union-Find: the edge joining one set | O(n²) → O(n·α(n)) |
| 223 | 721 | Accounts Merge | accounts-merge | M | #222 | Merge lists repeatedly | Union-Find on emails | O(n²) → O(N·α(N)) |
| 224 | 990 | Satisfiability of Equality Equations | satisfiability-of-equality-equations | M | #222 | Try all letter assignments | Union the equalities, then check the inequalities | O(26ⁿ) → O(n) |
| 225 | 1319 | Number of Operations to Make Network Connected | number-of-operations-to-make-network-connected | M | #222 | Try all cable moves | Count components minus 1 (needs n−1 cables) | exponential → O(n + c) |
| 226 | 947 | Most Stones Removed with Same Row or Column | most-stones-removed-with-same-row-or-column | M | #225 | Simulate removal orders | Union rows and columns; answer = n − components | exponential → O(n·α(n)) |
| 227 | 743 | Network Delay Time | network-delay-time | M | #217 | Repeated relaxation (Bellman-Ford) | Dijkstra with a min-heap | O(VE) → O(E log V) |
| 228 | 787 | Cheapest Flights Within K Stops | cheapest-flights-within-k-stops | M | #227 | DFS over all routes | Bellman-Ford with k+1 rounds | exponential → O(k·E) |
| 229 | 1631 | Path With Minimum Effort | path-with-minimum-effort | M | #227 | DFS over all paths | Dijkstra on the max edge, or binary search plus BFS | exponential → O(mn log mn) |
| 230 | 778 | Swim in Rising Water | swim-in-rising-water | H | #229 | DFS over all paths | Dijkstra, or binary search plus BFS | exponential → O(n² log n) |
| 231 | 1514 | Path with Maximum Probability | path-with-maximum-probability | M | #227 | DFS over all paths | Dijkstra with a max-heap on the product | exponential → O(E log V) |
| 232 | 1584 | Min Cost to Connect All Points | min-cost-to-connect-all-points | M | #222 | Try all edge subsets | Kruskal (Union-Find) or Prim | exponential → O(n² log n) |
| 233 | 332 | Reconstruct Itinerary | reconstruct-itinerary | H | #213 | Try all orderings | Hierholzer's algorithm with sorted edges | O(E!) → O(E log E) |
| 234 | 1334 | Find the City With the Smallest Number of Neighbors at a Threshold Distance | find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance | M | #227 | Dijkstra from every city | Floyd–Warshall | O(V·E log V) vs O(V³) |

### Chapter 15: Dynamic Programming, 1D (Seq 235 to 253)

| Seq | LC | Title | Slug | Diff | Builds on | Brute force | Optimal | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 235 | 70 | Climbing Stairs | climbing-stairs | E | #100 | Plain recursion | DP with two variables | O(2ⁿ) → O(n) |
| 236 | 746 | Min Cost Climbing Stairs | min-cost-climbing-stairs | E | #235 | Recursion | DP: minimum of the previous two | O(2ⁿ) → O(n) |
| 237 | 1137 | N-th Tribonacci Number | n-th-tribonacci-number | E | #235 | Recursion | Three rolling variables | O(3ⁿ) → O(n) |
| 238 | 198 | House Robber | house-robber | M | #236 | Recursion: take or skip | dp\[i\] = max(dp\[i−1\], dp\[i−2\] + a\[i\]) | O(2ⁿ) → O(n) |
| 239 | 213 | House Robber II | house-robber-ii | M | #238 | Recursion on a circle | Run House Robber twice (skip first, skip last) | O(2ⁿ) → O(n) |
| 240 | 740 | Delete and Earn | delete-and-earn | M | #238 | Recursion | Bucket by value, then House Robber | O(2ⁿ) → O(n + max) |
| 241 | 91 | Decode Ways | decode-ways | M | #235 | Recursion over 1 or 2 digit cuts | DP on prefixes | O(2ⁿ) → O(n) |
| 242 | 322 | Coin Change | coin-change | M | #235 | Recursion over all coins | DP over amounts | exponential → O(S·c) |
| 243 | 518 | Coin Change II | coin-change-ii | M | #242 | Recursion counting ways | DP with coins in the outer loop | exponential → O(S·c) |
| 244 | 377 | Combination Sum IV | combination-sum-iv | M | #243 | Recursion | DP with amounts in the outer loop | exponential → O(T·n) |
| 245 | 279 | Perfect Squares | perfect-squares | M | #242 | Recursion over squares | DP like coin change | exponential → O(n√n) |
| 246 | 139 | Word Break | word-break | M | #245 | Recursion over prefixes | DP over the end index | O(2ⁿ) → O(n²) |
| 247 | 300 | Longest Increasing Subsequence | longest-increasing-subsequence | M | #246 | Try all subsequences | O(n²) DP, or tails array with binary search | O(2ⁿ) → O(n log n) |
| 248 | 673 | Number of Longest Increasing Subsequence | number-of-longest-increasing-subsequence | M | #247 | Enumerate all subsequences | DP with length and count arrays | O(2ⁿ) → O(n²) |
| 249 | 354 | Russian Doll Envelopes | russian-doll-envelopes | H | #247 | Recursion over nesting | Sort (width ascending, height descending), then LIS | O(2ⁿ) → O(n log n) |
| 250 | 152 | Maximum Product Subarray | maximum-product-subarray | M | #176 | Multiply every subarray | Track the running max and min | O(n²) → O(n) |
| 251 | 416 | Partition Equal Subset Sum | partition-equal-subset-sum | M | #119 | Try all subsets | 0/1 knapsack DP, or a bitset | O(2ⁿ) → O(n·sum) |
| 252 | 1049 | Last Stone Weight II | last-stone-weight-ii | M | #251 | Try all sign choices | Subset sum closest to half | O(2ⁿ) → O(n·sum) |
| 253 | 343 | Integer Break | integer-break | M | #245 | Recursion over splits | DP, or the greedy rule of using 3s | exponential → O(n²) |

### Chapter 16: Dynamic Programming, 2D and Strings (Seq 254 to 277)

| Seq | LC | Title | Slug | Diff | Builds on | Brute force | Optimal | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 254 | 62 | Unique Paths | unique-paths | M | #253 | Recursion | 2D DP, 1D rolling array, or combinatorics | exponential → O(mn) |
| 255 | 63 | Unique Paths II | unique-paths-ii | M | #254 | Recursion with obstacles | DP with zero at obstacles | exponential → O(mn) |
| 256 | 64 | Minimum Path Sum | minimum-path-sum | M | #254 | Recursion | DP: min(top, left) + cell | exponential → O(mn) |
| 257 | 120 | Triangle | triangle | M | #256 | Recursion | Bottom-up DP in O(n) space | O(2ⁿ) → O(n²) |
| 258 | 931 | Minimum Falling Path Sum | minimum-falling-path-sum | M | #257 | Recursion | DP row by row | O(3ⁿ) → O(n²) |
| 259 | 221 | Maximal Square | maximal-square | M | #256 | Check every square | dp = 1 + min(top, left, diagonal) | O(mn·min(m,n)²) → O(mn) |
| 260 | 174 | Dungeon Game | dungeon-game | H | #256 | Recursion | DP from the bottom-right | exponential → O(mn) |
| 261 | 1143 | Longest Common Subsequence | longest-common-subsequence | M | #247 | Recursion on both strings | 2D DP | exponential → O(mn) |
| 262 | 1035 | Uncrossed Lines | uncrossed-lines | M | #261 | Recursion | Same as LCS on the arrays | exponential → O(mn) |
| 263 | 583 | Delete Operation for Two Strings | delete-operation-for-two-strings | M | #261 | Recursion | m + n − 2·LCS | exponential → O(mn) |
| 264 | 72 | Edit Distance | edit-distance | M | #261 | Recursion with 3 choices | 2D DP (insert, delete, replace) | exponential → O(mn) |
| 265 | 115 | Distinct Subsequences | distinct-subsequences | H | #264 | Recursion | 2D DP on prefixes | exponential → O(mn) |
| 266 | 97 | Interleaving String | interleaving-string | M | #264 | Recursion | 2D DP on (i, j) | exponential → O(mn) |
| 267 | 5 | Longest Palindromic Substring | longest-palindromic-substring | M | #23 | Check every substring | Expand around centres, or DP | O(n³) → O(n²) |
| 268 | 647 | Palindromic Substrings | palindromic-substrings | M | #267 | Check every substring | Expand around centres | O(n³) → O(n²) |
| 269 | 516 | Longest Palindromic Subsequence | longest-palindromic-subsequence | M | #261 | Try all subsequences | LCS of the string and its reverse, or interval DP | O(2ⁿ) → O(n²) |
| 270 | 132 | Palindrome Partitioning II | palindrome-partitioning-ii | H | #113 | Backtrack over all cuts | Palindrome table plus cut DP | O(2ⁿ) → O(n²) |
| 271 | 10 | Regular Expression Matching | regular-expression-matching | H | #264 | Recursion | 2D DP on (i, j) | exponential → O(mn) |
| 272 | 44 | Wildcard Matching | wildcard-matching | H | #271 | Recursion | 2D DP, or greedy two pointers | exponential → O(mn) |
| 273 | 312 | Burst Balloons | burst-balloons | H | #269 | Try all burst orders | Interval DP (choose the last balloon to burst) | O(n!) → O(n³) |
| 274 | 309 | Best Time to Buy and Sell Stock with Cooldown | best-time-to-buy-and-sell-stock-with-cooldown | M | #175 | Recursion on states | State machine DP | O(2ⁿ) → O(n) |
| 275 | 714 | Best Time to Buy and Sell Stock with Transaction Fee | best-time-to-buy-and-sell-stock-with-transaction-fee | M | #274 | Recursion | Two-state DP (hold and free) | O(2ⁿ) → O(n) |
| 276 | 123 | Best Time to Buy and Sell Stock III | best-time-to-buy-and-sell-stock-iii | H | #275 | Try every two-transaction split | Four-state DP | O(n²) → O(n) |
| 277 | 188 | Best Time to Buy and Sell Stock IV | best-time-to-buy-and-sell-stock-iv | H | #276 | Recursion over k transactions | DP with states per transaction | exponential → O(nk) |

### Chapter 17: Tries and Design (Seq 278 to 286)

| Seq | LC | Title | Slug | Diff | Builds on | Brute force | Optimal | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 278 | 14 | Longest Common Prefix | longest-common-prefix | E | #277 | Compare character by character across all words | Vertical scan, or a trie | O(S) both |
| 279 | 208 | Implement Trie (Prefix Tree) | implement-trie-prefix-tree | M | #278 | List of words, scanned every time | Node with a children map and an end flag | O(n·L) → O(L) |
| 280 | 211 | Design Add and Search Words Data Structure | design-add-and-search-words-data-structure | M | #279 | Scan all words with wildcard matching | Trie plus DFS at each dot | O(n·L) → O(L·26^dots) worst case |
| 281 | 648 | Replace Words | replace-words | M | #279 | Check every root for each word | Trie of the roots | O(R·W) → O(total chars) |
| 282 | 1268 | Search Suggestions System | search-suggestions-system | M | #279 | Filter all products for each prefix | Sort plus binary search, or a trie | O(n·L) → O(L log n) |
| 283 | 677 | Map Sum Pairs | map-sum-pairs | M | #279 | Scan all keys for the prefix | Trie storing prefix sums | O(n) → O(L) |
| 284 | 212 | Word Search II | word-search-ii | H | #115 | Run Word Search once per word | Trie plus one DFS over the grid | O(W·mn·4ˡ) → O(mn·4ˡ) |
| 285 | 421 | Maximum XOR of Two Numbers in an Array | maximum-xor-of-two-numbers-in-an-array | M | #279 | Check every pair | Binary trie, pick the opposite bit | O(n²) → O(32n) |
| 286 | 460 | LFU Cache | lfu-cache | H | #99 | Scan for the least frequent key | HashMaps plus frequency lists | O(n) → O(1) |

### Chapter 18: Bit Manipulation and Math (Seq 287 to 300)

| Seq | LC | Title | Slug | Diff | Builds on | Brute force | Optimal | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 287 | 136 | Single Number | single-number | E | #286 | HashMap counts | XOR everything | O(n) space → O(1) space |
| 288 | 137 | Single Number II | single-number-ii | M | #287 | HashMap counts | Count each bit modulo 3 | O(n) space → O(1) space |
| 289 | 260 | Single Number III | single-number-iii | M | #288 | HashMap counts | XOR, then split by a set bit | O(n) space → O(1) space |
| 290 | 191 | Number of 1 Bits | number-of-1-bits | E | #287 | Check all 32 bits | n & (n−1) clears the lowest set bit | O(32) → O(number of set bits) |
| 291 | 338 | Counting Bits | counting-bits | E | #290 | Count bits for each number | dp\[i\] = dp\[i >> 1\] + (i & 1) | O(n log n) → O(n) |
| 292 | 231 | Power of Two | power-of-two | E | #290 | Divide by 2 repeatedly | n > 0 and (n & (n−1)) == 0 | O(log n) → O(1) |
| 293 | 268 | Missing Number | missing-number | E | #287 | Sort and scan, or a set | XOR, or the sum formula | O(n log n) → O(n) |
| 294 | 190 | Reverse Bits | reverse-bits | E | #290 | Build a string, reverse it, parse it | Shift the bits one by one | O(32) both |
| 295 | 371 | Sum of Two Integers | sum-of-two-integers | M | #294 | Loop incrementing (no plus allowed) | XOR for the sum, AND shifted left for the carry | O(n) → O(1) |
| 296 | 7 | Reverse Integer | reverse-integer | M | #295 | Convert to a string and reverse | Pop and push digits with an overflow check | O(d) both |
| 297 | 9 | Palindrome Number | palindrome-number | E | #296 | Convert to a string | Reverse half of the number | O(d) space → O(1) space |
| 298 | 202 | Happy Number | happy-number | E | #297 | HashSet to detect a loop | Floyd cycle detection | O(n) space → O(1) space |
| 299 | 204 | Count Primes | count-primes | M | #298 | Trial division for each number | Sieve of Eratosthenes | O(n√n) → O(n log log n) |
| 300 | 172 | Factorial Trailing Zeroes | factorial-trailing-zeroes | M | #299 | Compute n! and count the zeros | Sum n/5 + n/25 + n/125 and so on | huge → O(log n) |

## Appendix B: Prompt for Antigravity

Paste the prompt below into Antigravity together with this document. It builds the app first, then writes all solution content in 12 batches, checking each batch before the next one starts. It can be resumed: if it stops, reply with the batch number to continue from.

```text
You are given a Software Requirements Specification (SRS) for a DSA Roadmap Tracker. Follow it exactly.

STEP 1. Build the app
Build the React + Vite app described in sections 1 to 9 and 11 to 12 of the SRS: username login with optional PIN, roadmap, question page, status, revisit scheduling with spaced repetition (1, 3, 7, 21 days), Today page, dashboard, notes, filters, dark (default) and light theme. Include the Supabase SQL and database functions from section 6, and a netlify.toml with the single-page-app redirect. Do not build visualizers.

STEP 2. Generate the question data
Parse Appendix A. Create public/data/chapters.json and public/data/questions.json (one entry per row, all 300). Do not change any LC number or slug silently. If a number or slug looks wrong, keep it and list it in a file named data-warnings.md.

STEP 3. Generate the solutions in 12 batches of 25 questions
Batch 1 is seq 1 to 25, batch 2 is 26 to 50, and so on up to batch 12 (seq 276 to 300). For every question write public/data/solutions/ch-XX.json entries in the schema of section 6.1 and the style of the Two Sum reference in section 10.2:
- brute: idea (1 to 3 plain sentences), steps (numbered), why it is slow, time, space, code.java, code.python
- optimal: idea, steps, time, space, code.java, code.python
- whyNext: one sentence on why this question follows the one it builds on
Rules: Java and Python use class Solution with the exact LeetCode signature; brute and optimal must really differ; complexity must match the code; use the brute and optimal ideas given in Appendix A as the starting point; no premium-only problems.

STEP 4. Check each batch before starting the next
Compile every Java solution and run every Python solution on at least one sample input. Write the results to batch-report.md (batch number, passed, failed, fixes made). Fix failures before moving on.

STEP 5. Final validation
Write and run a script that confirms: 300 entries, every field present, buildsOn is smaller than seq, chapter ranges are contiguous, no duplicate LC numbers or slugs. Print a short summary.

If you run out of budget, stop at the end of a finished batch and tell me the last completed batch number so I can say: Continue from batch N.
```

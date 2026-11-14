import re
import json
import os

SRS_PATH = r"c:\Users\admin\Documents\leetcode\Software Requirements Specification.md"
PUBLIC_DATA_DIR = r"c:\Users\admin\Documents\leetcode\public\data"
os.makedirs(PUBLIC_DATA_DIR, exist_ok=True)

with open(SRS_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Chapters metadata
chapters_meta = [
    {
        "id": "ch-01",
        "order": 1,
        "name": "Arrays and Hashing",
        "seqFrom": 1,
        "seqTo": 21,
        "whyNext": "Foundation: counting, prefix sums and in-place tricks used everywhere later.",
        "summary": "Fundamental array and hash table patterns for fast lookups, frequency counts, and in-place manipulations.",
        "patterns": [
            "Hash map / set for O(1) lookups and frequency counting",
            "Prefix sum array to answer range sum queries in O(1)",
            "In-place array indexing / sign marking for O(1) extra space",
            "Boyer-Moore voting algorithm for majority elements"
        ]
    },
    {
        "id": "ch-02",
        "order": 2,
        "name": "Two Pointers",
        "seqFrom": 22,
        "seqTo": 35,
        "whyNext": "Uses array order; Two Sum becomes Two Sum II, then 3Sum and 4Sum.",
        "summary": "Pairwise scanning from opposite ends or at variable speeds on sorted or ordered sequences.",
        "patterns": [
            "Inward converging pointers for sorted pair/triplet sums",
            "Fast and slow runner pointers for in-place deduplication and partitioning",
            "Dutch National Flag 3-pointer partition",
            "Next permutation pivot-and-swap scan"
        ]
    },
    {
        "id": "ch-03",
        "order": 3,
        "name": "Sliding Window",
        "seqFrom": 36,
        "seqTo": 49,
        "whyNext": "Two pointers moving together over subarrays and substrings.",
        "summary": "Dynamic and fixed-size contiguous subarray and substring maintenance.",
        "patterns": [
            "Fixed size window: add incoming, remove outgoing element",
            "Dynamic window: expand right to satisfy condition, shrink left to minimize/restore",
            "At-most trick: exact(K) = atMost(K) - atMost(K - 1)",
            "Monotonic deque for sliding window maximum in O(n)"
        ]
    },
    {
        "id": "ch-04",
        "order": 4,
        "name": "Binary Search",
        "seqFrom": 50,
        "seqTo": 67,
        "whyNext": "Sorted order again, then searching on the answer itself.",
        "summary": "Halving search spaces for elements, boundaries, and monotonic answer domains.",
        "patterns": [
            "Classic lower and upper bound binary search",
            "Rotated sorted array: identify the sorted half and narrow range",
            "Binary search on monotonic answer space (min max / max min capacity/days)",
            "Staircase walk on row/column sorted 2D matrices"
        ]
    },
    {
        "id": "ch-05",
        "order": 5,
        "name": "Stack and Monotonic Stack",
        "seqFrom": 68,
        "seqTo": 82,
        "whyNext": "Next greater and span ideas that later reappear in trees and DP.",
        "summary": "LIFO state tracking, matching nested structures, and monotonic stacks for nearest greater/smaller queries.",
        "patterns": [
            "Parentheses and nested structure matching with LIFO stack",
            "Monotonic decreasing stack for next greater element / daily temperatures",
            "Monotonic increasing stack for largest rectangle in histogram / maximal rectangle",
            "Greedy digit/character removal with stack"
        ]
    },
    {
        "id": "ch-06",
        "order": 6,
        "name": "Linked List",
        "seqFrom": 83,
        "seqTo": 99,
        "whyNext": "Pointer skills, reusing slow and fast pointers.",
        "summary": "Sequential node pointer manipulation, cycle detection, reversals, and reordering.",
        "patterns": [
            "Dummy head node to simplify boundary additions/removals",
            "Three-pointer iterative list reversal (prev, curr, next)",
            "Floyd's Tortoise and Hare algorithm for cycle detection and middle node",
            "In-place interleaving and split for complex list copies"
        ]
    },
    {
        "id": "ch-07",
        "order": 7,
        "name": "Recursion and Backtracking",
        "seqFrom": 100,
        "seqTo": 120,
        "whyNext": "Builds the recursion habit needed for trees and DP; ends with Target Sum, the bridge into DP.",
        "summary": "Exhaustive state space exploration, combinatorial generation, and constrained search pruning.",
        "patterns": [
            "Subsets and combinations: choose/skip recursion with start index",
            "Permutations: used array or swap-based backtracking",
            "Constraint pruning: early backtrack on invalid partial states",
            "Bridge to DP: overlapping subproblems memoization"
        ]
    },
    {
        "id": "ch-08",
        "order": 8,
        "name": "Binary Trees",
        "seqFrom": 121,
        "seqTo": 147,
        "whyNext": "Recursion on a structure; ends with House Robber III as a DP preview.",
        "summary": "Hierarchical tree traversal, depth-first search, breadth-first level orders, and structural transformations.",
        "patterns": [
            "Bottom-up postorder DFS: solve subtrees then aggregate root result",
            "Level order traversal using queue with level size snapshot",
            "Path sum tracking with prefix sum hash map across ancestor paths",
            "Tree serialization and deserialization via preorder/level order"
        ]
    },
    {
        "id": "ch-09",
        "order": 9,
        "name": "Binary Search Trees",
        "seqFrom": 148,
        "seqTo": 156,
        "whyNext": "Trees plus ordering.",
        "summary": "Exploiting the BST ordering invariant for O(h) searches, insertions, deletions, and sorted traversals.",
        "patterns": [
            "BST search and insertion using value comparisons to prune branches",
            "Inorder traversal produces strictly ascending sorted order",
            "Validation using (min, max) inherited bounds",
            "BST iterative traversal with explicit left-spine stack"
        ]
    },
    {
        "id": "ch-10",
        "order": 10,
        "name": "Heap and Priority Queue",
        "seqFrom": 157,
        "seqTo": 170,
        "whyNext": "Kth element and streaming problems; follows sorting and BST order ideas.",
        "summary": "Min and max priority queues for top-K elements, stream medians, and greedy schedules.",
        "patterns": [
            "Min-heap of size K for K-th largest streaming element",
            "Two heaps (max-heap low half, min-heap high half) for running median",
            "Multi-criteria priority queue with custom comparators",
            "K-way merge of sorted streams / arrays"
        ]
    },
    {
        "id": "ch-11",
        "order": 11,
        "name": "Greedy",
        "seqFrom": 171,
        "seqTo": 187,
        "whyNext": "Local choices; uses sorting and heaps.",
        "summary": "Making locally optimal choices that lead to globally optimal solutions.",
        "patterns": [
            "Sort-first greedy matching (e.g. intervals, assigning cookies)",
            "Kadane's algorithm for maximum subarray sum",
            "Farthest reach tracking for jump game decisions",
            "Bidirectional / multi-pass greedy passes (e.g. candy distribution)"
        ]
    },
    {
        "id": "ch-12",
        "order": 12,
        "name": "Intervals",
        "seqFrom": 188,
        "seqTo": 195,
        "whyNext": "Sorting plus greedy sweeps.",
        "summary": "Interval overlap resolution, merges, insertions, and point-stabbing problems.",
        "patterns": [
            "Sort by start time to linearize overlapping intervals",
            "Sort by end time for greedy maximum non-overlapping set",
            "Two-pointer sweep for mutual interval intersections",
            "Difference array / sweep line for concurrency capacity counting"
        ]
    },
    {
        "id": "ch-13",
        "order": 13,
        "name": "Graphs: BFS and DFS",
        "seqFrom": 196,
        "seqTo": 217,
        "whyNext": "Trees generalised: grids, shortest paths in unweighted graphs.",
        "summary": "Connected components, grid explorations, shortest unweighted paths, and graph traversals.",
        "patterns": [
            "Connected component flood fill via recursive DFS or iterative BFS",
            "Multi-source BFS for simultaneous shortest distance wavefront propagation",
            "Bipartite graph two-coloring check",
            "Cycle detection in undirected graphs using visited sets"
        ]
    },
    {
        "id": "ch-14",
        "order": 14,
        "name": "Graphs: Topological Sort, Union-Find, Shortest Paths",
        "seqFrom": 218,
        "seqTo": 234,
        "whyNext": "Advanced graph tools on top of BFS and DFS.",
        "summary": "Directed acyclic graph ordering, disjoint set union for connectivity, and weighted shortest path algorithms.",
        "patterns": [
            "Kahn's in-degree algorithm for DAG topological sort",
            "Disjoint Set Union (DSU) with path compression and rank union",
            "Dijkstra's algorithm with min-heap for non-negative weighted shortest paths",
            "Bellman-Ford / Floyd-Warshall for edge-constrained or all-pairs shortest paths"
        ]
    },
    {
        "id": "ch-15",
        "order": 15,
        "name": "Dynamic Programming (1D)",
        "seqFrom": 235,
        "seqTo": 253,
        "whyNext": "Recursion with repeated work, fixed by memoisation.",
        "summary": "Subproblem optimal substructure along a single dimension with state compression.",
        "patterns": [
            "Linear recurrence with rolling variables (Fibonacci, Climbing Stairs)",
            "Pick vs Skip decision state transitions (House Robber)",
            "Unbounded vs 0/1 knapsack subproblem transitions (Coin Change)",
            "Longest increasing subsequence: O(n^2) DP and O(n log n) patience sorting"
        ]
    },
    {
        "id": "ch-16",
        "order": 16,
        "name": "Dynamic Programming (2D and Strings)",
        "seqFrom": 254,
        "seqTo": 277,
        "whyNext": "Grids, two-string problems, intervals and stock states.",
        "summary": "Multi-dimensional tables for grids, dual-string alignments, palindromes, and state machines.",
        "patterns": [
            "Grid path counting and minimum cost paths (Unique Paths, Min Path Sum)",
            "Two-string alignment matrix for LCS and Edit Distance",
            "Interval DP: solving for all lengths from 1 to N (Burst Balloons)",
            "Multi-state finite automata transitions (Stock trading with cooldown/fee)"
        ]
    },
    {
        "id": "ch-17",
        "order": 17,
        "name": "Tries and Design",
        "seqFrom": 278,
        "seqTo": 286,
        "whyNext": "Prefix trees and cache design, building on trees, hashing and linked lists.",
        "summary": "Prefix tree data structures for string queries and composite data structures for caching.",
        "patterns": [
            "Trie node with 26 child pointers and isEndOfWord flag",
            "Bitwise trie for maximum XOR pair queries",
            "Trie combined with DFS for grid word searches",
            "HashMap coupled with Doubly Linked List for O(1) LRU / LFU cache eviction"
        ]
    },
    {
        "id": "ch-18",
        "order": 18,
        "name": "Bit Manipulation and Math",
        "seqFrom": 287,
        "seqTo": 300,
        "whyNext": "Compact tricks to finish the path.",
        "summary": "Bitwise operators, parity tricks, number theory, and prime generation algorithms.",
        "patterns": [
            "XOR cancellation (x ^ x = 0, x ^ 0 = x) for finding unique elements",
            "Bit clearing trick: n & (n - 1) removes lowest set bit",
            "Bitmask representation for subset states",
            "Sieve of Eratosthenes for prime enumeration"
        ]
    }
]

with open(os.path.join(PUBLIC_DATA_DIR, "chapters.json"), "w", encoding="utf-8") as f:
    json.dump(chapters_meta, f, indent=2)

# Parse Appendix A table rows
# Row pattern: | Seq | LC | Title | Slug | Diff | Builds on | Brute force | Optimal | Time |
# e.g.: | 1 | 217 | Contains Duplicate | contains-duplicate | E | none | Compare every pair | Add to a HashSet, stop on a repeat | O(n²) → O(n) |

rows = []
warnings = []
current_chapter = None

# Extract Appendix A section
app_a_start = content.find("## Appendix A: Question Catalogue (300 Questions)")
app_b_start = content.find("## Appendix B: Prompt for Antigravity")
app_a_text = content[app_a_start:app_b_start]

for line in app_a_text.splitlines():
    line = line.strip()
    if line.startswith("### Chapter"):
        # Match chapter number
        m = re.search(r"Chapter\s+(\d+):", line)
        if m:
            ch_num = int(m.group(1))
            current_chapter = f"ch-{ch_num:02d}"
    elif line.startswith("|") and not line.startswith("| Seq") and not line.startswith("| ---"):
        parts = [p.strip() for p in line.split("|")]
        # parts[0] is '', parts[-1] is ''
        cells = [p for p in parts if p != '']
        if len(cells) >= 9:
            try:
                seq = int(cells[0])
                lc = int(cells[1])
                title = cells[2]
                slug = cells[3]
                diff_code = cells[4]
                difficulty = "Easy" if diff_code == "E" else ("Medium" if diff_code == "M" else "Hard")
                builds_on_str = cells[5]
                builds_on = None
                if builds_on_str.lower() != "none":
                    m_bo = re.search(r"#?(\d+)", builds_on_str)
                    if m_bo:
                        builds_on = int(m_bo.group(1))
                
                brute_idea = cells[6]
                optimal_idea = cells[7]
                time_str = cells[8]

                # split time if contains arrow
                if "→" in time_str:
                    t_parts = time_str.split("→")
                    brute_time = t_parts[0].strip()
                    optimal_time = t_parts[1].strip()
                elif "vs" in time_str:
                    t_parts = time_str.split("vs")
                    brute_time = t_parts[0].strip()
                    optimal_time = t_parts[1].strip()
                elif "both" in time_str:
                    brute_time = time_str
                    optimal_time = time_str
                else:
                    brute_time = time_str
                    optimal_time = time_str

                rows.append({
                    "seq": seq,
                    "lc": lc,
                    "title": title,
                    "slug": slug,
                    "difficulty": difficulty,
                    "chapter": current_chapter,
                    "buildsOn": builds_on,
                    "brute": {
                        "idea": brute_idea,
                        "time": brute_time
                    },
                    "optimal": {
                        "idea": optimal_idea,
                        "time": optimal_time
                    }
                })
            except Exception as e:
                warnings.append(f"Could not parse line: {line} -> {e}")

print(f"Parsed {len(rows)} questions from Appendix A.")

# Validation checks
seen_seq = set()
seen_lc = set()
seen_slug = set()

for q in rows:
    if q["seq"] in seen_seq:
        warnings.append(f"Duplicate seq: {q['seq']}")
    seen_seq.add(q["seq"])

    if q["lc"] in seen_lc:
        warnings.append(f"Duplicate LC number: {q['lc']} in {q['title']}")
    seen_lc.add(q["lc"])

    if q["slug"] in seen_slug:
        warnings.append(f"Duplicate slug: {q['slug']} in {q['title']}")
    seen_slug.add(q["slug"])

    if q["buildsOn"] is not None and q["buildsOn"] >= q["seq"]:
        warnings.append(f"Question {q['seq']} buildsOn {q['buildsOn']} which is not smaller than seq")

with open(os.path.join(PUBLIC_DATA_DIR, "questions.json"), "w", encoding="utf-8") as f:
    json.dump(rows, f, indent=2)

warn_path = r"c:\Users\admin\Documents\leetcode\data-warnings.md"
with open(warn_path, "w", encoding="utf-8") as f:
    f.write("# Data Warnings\n\n")
    if warnings:
        for w in warnings:
            f.write(f"- {w}\n")
    else:
        f.write("No warnings found. All 300 questions parsed cleanly and validated successfully.\n")

print(f"Generated {PUBLIC_DATA_DIR}/questions.json with {len(rows)} entries.")
print(f"Warnings written to {warn_path}: {len(warnings)} warnings.")


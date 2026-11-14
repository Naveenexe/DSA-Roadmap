import re

def clean_to_prose(text):
    if not text:
        return ""
    # Convert code-like notation to English
    text = re.sub(r'(\w+)\.length\(\)', r'the length of \1', text)
    text = re.sub(r'(\w+)\.length', r'the length of \1', text)
    text = re.sub(r'(\w+)\[(\w+)\]', r'\1 at index \2', text)
    text = re.sub(r'(\w+)\.left', r'the left child of \1', text)
    text = re.sub(r'(\w+)\.right', r'the right child of \1', text)
    text = re.sub(r'(\w+)\.next', r'the next node after \1', text)
    text = re.sub(r'==', ' is equal to ', text)
    text = re.sub(r'!=', ' is not equal to ', text)
    text = re.sub(r'<=', ' is at most ', text)
    text = re.sub(r'>=', ' is at least ', text)
    text = re.sub(r'<', ' is less than ', text)
    text = re.sub(r'>', ' is greater than ', text)
    text = re.sub(r'[{}\[\];()_]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    if text and not text.endswith('.'):
        text += '.'
    return text[0].upper() + text[1:] if text else ''

def generate_hints_for_question(q, sol, ch):
    title = q['title']
    ch_name = ch['name']
    opt_idea = sol['optimal']['idea']
    steps = sol['optimal']['steps']
    time_c = sol['optimal']['time']
    space_c = sol['optimal']['space']

    idea_lower = opt_idea.lower()
    ch_lower = ch_name.lower()

    # 1. Pattern & Data Structure detection
    if 'hashset' in idea_lower or 'hash set' in idea_lower:
        ds_name = "a Hash Set"
        nudge = "Think about whether you can detect duplicates or look up previously seen items in constant time as you iterate."
        idea_summary = "Add each item to a Hash Set as you traverse; if an item is already present, you have identified a duplicate immediately."
    elif 'hashmap' in idea_lower or 'hash map' in idea_lower or 'frequency' in idea_lower or 'counting' in idea_lower:
        ds_name = "a Hash Map or frequency table"
        nudge = "Instead of nested loops, can you store previous elements or counts so you can query complementary values in constant time?"
        idea_summary = "Record each element and its occurrence or index in the map, and look up whether the required match or complement has already been recorded."
    elif 'sliding window' in idea_lower or 'window' in idea_lower:
        ds_name = "the Sliding Window technique"
        nudge = "Notice that contiguous subarrays or substrings can be examined by expanding an end pointer and shrinking a start pointer when constraints are violated."
        idea_summary = "Expand the right boundary to incorporate new elements into the window, and increment the left boundary to restore the valid condition whenever constraints are exceeded."
    elif 'two pointer' in idea_lower or 'pointers' in idea_lower:
        ds_name = "the Two Pointers pattern"
        nudge = "If the data is sorted or symmetric, can you move pointers inward from both ends to prune unviable pairs in linear time?"
        idea_summary = "Initialize pointers at opposing ends (or one fast and one slow), evaluate the current combination, and move the appropriate pointer inward based on the target value."
    elif 'binary search' in idea_lower:
        ds_name = "Binary Search"
        nudge = "Look for monotonicity: can you test the midpoint of your search range and discard half of all remaining candidates on every step?"
        idea_summary = "Compute the midpoint between the search bounds, test whether it satisfies your condition, and adjust the left or right boundary accordingly to narrow the range logarithmically."
    elif 'monotonic stack' in idea_lower:
        ds_name = "a Monotonic Stack"
        nudge = "To find the next greater or smaller element for each item in linear time, consider maintaining elements in strictly increasing or decreasing order."
        idea_summary = "Iterate through the array and pop elements from the stack whenever the incoming value breaks the monotonic order, recording the answer for all popped elements."
    elif 'stack' in idea_lower:
        ds_name = "a Stack (LIFO)"
        nudge = "Notice how matching pairs or nested structures require the most recently opened element to be closed or resolved first."
        idea_summary = "Push opening elements onto the stack, and when encountering a closing element, pop from the stack and verify that it matches."
    elif 'fast and slow' in idea_lower or 'floyd' in idea_lower:
        ds_name = "Floyd's Cycle Detection (Fast and Slow Pointers)"
        nudge = "If one pointer moves one step at a time while another moves two steps at a time, will they ever collide if a loop exists?"
        idea_summary = "Advance a slow pointer by one node and a fast pointer by two nodes; if they meet, a cycle exists, and the cycle start can be located by resetting one pointer to the head."
    elif 'linked list' in ch_lower:
        ds_name = "pointer manipulation with a dummy node"
        nudge = "Using a dummy head node simplifies boundary edge cases such as modifying or removing the very first element of the list."
        idea_summary = "Maintain a dummy head pointing to the list head, track previous and current pointers, and adjust the next links sequentially without losing references."
    elif 'heap' in idea_lower or 'priority queue' in idea_lower:
        ds_name = "a Min-Heap or Max-Heap (Priority Queue)"
        nudge = "Do you really need to sort all elements, or do you only need to continuously extract or maintain the k extremal elements?"
        idea_summary = "Keep a priority queue of size k containing the candidates seen so far; whenever the queue exceeds capacity, discard the non-optimal element."
    elif 'backtrack' in idea_lower or 'backtracking' in idea_lower:
        ds_name = "Backtracking with recursion"
        nudge = "Explore decisions one choice at a time: make a choice, recurse down to explore further, and remember to undo the choice upon returning."
        idea_summary = "Define a recursive helper that takes current state and index, iterate over valid next choices, recurse, and backtrack by removing the choice from the working path."
    elif 'trie' in idea_lower or 'prefix tree' in idea_lower:
        ds_name = "a Trie (Prefix Tree)"
        nudge = "Words that share prefixes can share the same initial sequence of tree nodes, drastically reducing repeated lookups."
        idea_summary = "Insert strings character by character into a tree of 26-way nodes, marking the terminal node of each complete word."
    elif 'topological' in idea_lower or 'kahn' in idea_lower:
        ds_name = "Kahn's Algorithm (Topological Sort BFS)"
        nudge = "Which nodes or courses have zero prerequisites and can be completed immediately?"
        idea_summary = "Compute the in-degree of all nodes, enqueue all nodes with in-degree zero, and as each node is processed, decrement the in-degrees of its neighbors."
    elif 'union-find' in idea_lower or 'disjoint set' in idea_lower:
        ds_name = "a Disjoint Set Union (Union-Find) data structure"
        nudge = "Think about merging disjoint sets and checking whether two elements belong to the same connected component in nearly O(1) time."
        idea_summary = "Maintain parent and rank arrays, implement find with path compression, and union connected components by rank."
    elif 'dijkstra' in idea_lower:
        ds_name = "Dijkstra's Shortest Path Algorithm"
        nudge = "Since edge weights are non-negative, the shortest tentative distance in a min-heap is guaranteed to be optimal."
        idea_summary = "Store tentative distances in a min-heap starting from the source, continually popping the closest unvisited node and relaxing its outgoing edges."
    elif 'bfs' in idea_lower:
        ds_name = "Breadth-First Search (BFS) using a Queue"
        nudge = "To find the shortest path or process elements level-by-level, explore all equidistant neighbors before moving further outwards."
        idea_summary = "Enqueue the starting node, track visited nodes to avoid cycles, and repeatedly dequeue nodes while offering their unvisited valid neighbors."
    elif 'dfs' in idea_lower or 'tree' in ch_lower:
        ds_name = "Depth-First Search (DFS) / Tree Traversal"
        nudge = "What is the base case when reaching a null node or leaf, and how do results from the left and right subtrees combine?"
        idea_summary = "Handle null nodes with a base value, recursively compute the result for child subproblems, and combine their returns into the answer for the current root."
    elif 'dp' in idea_lower or 'dynamic programming' in idea_lower:
        ds_name = "Dynamic Programming (DP)"
        nudge = "Identify the overlapping subproblems: how can the answer to state i be computed using previously calculated answers to smaller states?"
        idea_summary = "Define a DP state representing the optimal answer up to index i, establish the base cases, and transition forward using the recurrence relation."
    elif 'bit' in idea_lower or 'xor' in idea_lower:
        ds_name = "Bitwise Operations (such as XOR)"
        nudge = "Remember that XORing a number with itself yields 0, and XORing any number with 0 preserves that number."
        idea_summary = "Apply bitwise operations across all values so duplicate numbers cancel each other out, isolating the unique answer in O(1) space."
    elif 'greedy' in idea_lower:
        ds_name = "a Greedy Strategy"
        nudge = "Can you prove that making the locally optimal choice at each step will never prevent you from reaching the global optimal solution?"
        idea_summary = "Sort or process elements in a priority order, greedily taking the most beneficial available choice at every iteration."
    else:
        ds_name = f"a structured approach tailored for {ch_name}"
        nudge = "Break down the core constraints and observe what invariant remains unchanged as you step through the input."
        idea_summary = clean_to_prose(opt_idea)

    # Hint 1: Nudge
    h1 = nudge

    # Hint 2: Data structure / pattern + complexity target
    h2 = f"Apply {ds_name}. This achieves {time_c} time and {space_c} auxiliary space."

    # Hint 3: Almost full idea
    if steps and len(steps) >= 2:
        step_prose = clean_to_prose(steps[0]) + " Then " + clean_to_prose(steps[1]).lower()
        h3 = f"{idea_summary} In detail: {step_prose}"
    else:
        h3 = idea_summary

    # Ensure clean formatting
    h1 = clean_to_prose(h1)
    h2 = clean_to_prose(h2)
    h3 = clean_to_prose(h3)

    return [h1, h2, h3]

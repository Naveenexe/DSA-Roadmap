# Batch 10: Questions 226 to 250

def get_batch():
    return [
    {
        "seq": 226,
        "whyNext": "DSU row/col grouping: connect stone's row r with col ~c (bitwise negation); answer is stones.length - number_of_components.",
        "brute": {
            "idea": "Build adjacency graph between stones sharing row or col; run DFS to count connected components.",
            "steps": [
                "Build graph connecting stones sharing x or y.",
                "Count connected components with DFS.",
                "Return n - components."
            ],
            "time": "O(n^2)",
            "space": "O(n^2)",
            "whySlow": "Checks all pairs of stones to create edges.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int removeStones(int[][] stones) {\n        int n = stones.length;\n        List<Integer>[] adj = new List[n];\n        for (int i = 0; i < n; i++) adj[i] = new ArrayList<>();\n        for (int i = 0; i < n; i++) {\n            for (int j = i + 1; j < n; j++) {\n                if (stones[i][0] == stones[j][0] || stones[i][1] == stones[j][1]) {\n                    adj[i].add(j);\n                    adj[j].add(i);\n                }\n            }\n        }\n        boolean[] visited = new boolean[n];\n        int components = 0;\n        for (int i = 0; i < n; i++) {\n            if (!visited[i]) {\n                components++;\n                dfs(adj, i, visited);\n            }\n        }\n        return n - components;\n    }\n    private void dfs(List<Integer>[] adj, int u, boolean[] visited) {\n        visited[u] = true;\n        for (int v : adj[u]) {\n            if (!visited[v]) dfs(adj, v, visited);\n        }\n    }\n}",
                "python": "from collections import defaultdict\n\nclass Solution:\n    def removeStones(self, stones: list[list[int]]) -> int:\n        n = len(stones)\n        adj = defaultdict(list)\n        for i in range(n):\n            for j in range(i + 1, n):\n                if stones[i][0] == stones[j][0] or stones[i][1] == stones[j][1]:\n                    adj[i].append(j)\n                    adj[j].append(i)\n        visited = set()\n        comp = 0\n        def dfs(u):\n            visited.add(u)\n            for v in adj[u]:\n                if v not in visited: dfs(v)\n        for i in range(n):\n            if i not in visited:\n                comp += 1\n                dfs(i)\n        return n - comp"
            }
        },
        "optimal": {
            "idea": "DSU indexing: union stone x with ~y (bitwise NOT). Number of removable stones is n - unique_roots.",
            "steps": [
                "Map<Integer, Integer> parent.",
                "For stone [x, y]: union(x, ~y).",
                "Count unique roots find(x) for all stone coordinates x.",
                "Return stones.length - uniqueRoots."
            ],
            "time": "O(n * alpha(n))",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    private Map<Integer, Integer> parent = new HashMap<>();\n    private int count = 0;\n    public int removeStones(int[][] stones) {\n        for (int[] s : stones) {\n            union(s[0], ~s[1]);\n        }\n        return stones.length - count;\n    }\n    private int find(int x) {\n        if (!parent.containsKey(x)) {\n            parent.put(x, x);\n            count++;\n        }\n        if (x != parent.get(x)) {\n            parent.put(x, find(parent.get(x)));\n        }\n        return parent.get(x);\n    }\n    private void union(int x, int y) {\n        int rx = find(x), ry = find(y);\n        if (rx != ry) {\n            parent.put(rx, ry);\n            count--;\n        }\n    }\n}",
                "python": "class Solution:\n    def removeStones(self, stones: list[list[int]]) -> int:\n        parent = {}\n        count = 0\n        def find(x):\n            nonlocal count\n            if x not in parent:\n                parent[x] = x\n                count += 1\n            if x != parent[x]:\n                parent[x] = find(parent[x])\n            return parent[x]\n        def union(x, y):\n            nonlocal count\n            rx, ry = find(x), find(y)\n            if rx != ry:\n                parent[rx] = ry\n                count -= 1\n        for x, y in stones:\n            union(x, ~y)\n        return len(stones) - count"
            }
        }
    },
    {
        "seq": 227,
        "whyNext": "Canonical Dijkstra algorithm: single-source shortest path on directed weighted graph with non-negative edge weights.",
        "brute": {
            "idea": "Bellman-Ford algorithm relaxing all edges n - 1 times.",
            "steps": [
                "Initialize dist[1..n] with infinity, dist[k] = 0.",
                "Repeat n - 1 times: for each edge (u, v, w), dist[v] = min(dist[v], dist[u] + w).",
                "Return max(dist) or -1."
            ],
            "time": "O(V * E)",
            "space": "O(V)",
            "whySlow": "Bellman-Ford relaxes all edges V times instead of Dijkstra's greedy priority queue.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int networkDelayTime(int[][] times, int n, int k) {\n        int[] dist = new int[n + 1];\n        Arrays.fill(dist, 1000000);\n        dist[k] = 0;\n        for (int i = 1; i < n; i++) {\n            for (int[] e : times) {\n                int u = e[0], v = e[1], w = e[2];\n                if (dist[u] + w < dist[v]) {\n                    dist[v] = dist[u] + w;\n                }\n            }\n        }\n        int max = 0;\n        for (int i = 1; i <= n; i++) max = Math.max(max, dist[i]);\n        return max >= 1000000 ? -1 : max;\n    }\n}",
                "python": "class Solution:\n    def networkDelayTime(self, times: list[list[int]], n: int, k: int) -> int:\n        dist = [float('inf')] * (n + 1)\n        dist[k] = 0\n        for _ in range(n - 1):\n            for u, v, w in times:\n                if dist[u] + w < dist[v]:\n                    dist[v] = dist[u] + w\n        ans = max(dist[1:])\n        return ans if ans < float('inf') else -1"
            }
        },
        "optimal": {
            "idea": "Dijkstra's Algorithm with Min-Heap: PriorityQueue stores (dist, node); poll minimum distance node, relax edges, update dist array.",
            "steps": [
                "Build adjacency list: adj[u] -> (v, w).",
                "Arrays.fill(dist, INF), dist[k] = 0.",
                "PriorityQueue<int[]> pq stores (dist, u).",
                "While !pq.isEmpty(): pop (d, u); if d > dist[u] continue.",
                "For (v, w) in adj[u]: if d + w < dist[v] { dist[v] = d + w; pq.offer(dist[v], v); }",
                "Return max(dist[1..n]) or -1."
            ],
            "time": "O(E log V)",
            "space": "O(V + E)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int networkDelayTime(int[][] times, int n, int k) {\n        List<int[]>[] adj = new List[n + 1];\n        for (int i = 1; i <= n; i++) adj[i] = new ArrayList<>();\n        for (int[] t : times) {\n            adj[t[0]].add(new int[]{t[1], t[2]});\n        }\n        int[] dist = new int[n + 1];\n        Arrays.fill(dist, Integer.MAX_VALUE);\n        dist[k] = 0;\n        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[0]));\n        pq.offer(new int[]{0, k});\n        while (!pq.isEmpty()) {\n            int[] cur = pq.poll();\n            int d = cur[0], u = cur[1];\n            if (d > dist[u]) continue;\n            for (int[] edge : adj[u]) {\n                int v = edge[0], w = edge[1];\n                if (d + w < dist[v]) {\n                    dist[v] = d + w;\n                    pq.offer(new int[]{dist[v], v});\n                }\n            }\n        }\n        int max = 0;\n        for (int i = 1; i <= n; i++) {\n            if (dist[i] == Integer.MAX_VALUE) return -1;\n            max = Math.max(max, dist[i]);\n        }\n        return max;\n    }\n}",
                "python": "import heapq\nfrom collections import defaultdict\n\nclass Solution:\n    def networkDelayTime(self, times: list[list[int]], n: int, k: int) -> int:\n        adj = defaultdict(list)\n        for u, v, w in times:\n            adj[u].append((v, w))\n        dist = [float('inf')] * (n + 1)\n        dist[k] = 0\n        pq = [(0, k)]\n        while pq:\n            d, u = heapq.heappop(pq)\n            if d > dist[u]:\n                continue\n            for v, w in adj[u]:\n                if d + w < dist[v]:\n                    dist[v] = d + w\n                    heapq.heappush(pq, (dist[v], v))\n        ans = max(dist[1:])\n        return ans if ans < float('inf') else -1"
            }
        }
    },
    {
        "seq": 228,
        "whyNext": "Constrained shortest path: Bellman-Ford relaxed exactly k + 1 times (each iteration corresponds to 1 edge/flight).",
        "brute": {
            "idea": "DFS with pruning exploring all paths from src to dst with length <= k + 1.",
            "steps": [
                "DFS(node, stops, cost).",
                "Prune if stops > k + 1 or cost >= minCost.",
                "Update minCost at dst."
            ],
            "time": "O(V^(k+1))",
            "space": "O(V)",
            "whySlow": "Exponential recursive paths without dynamic programming.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int findCheapestPrice(int n, int[][] flights, int src, int dst, int k) {\n        int[] dist = new int[n];\n        Arrays.fill(dist, 100000000);\n        dist[src] = 0;\n        for (int i = 0; i <= k; i++) {\n            int[] temp = Arrays.copyOf(dist, n);\n            for (int[] f : flights) {\n                int u = f[0], v = f[1], w = f[2];\n                if (dist[u] + w < temp[v]) {\n                    temp[v] = dist[u] + w;\n                }\n            }\n            dist = temp;\n        }\n        return dist[dst] >= 100000000 ? -1 : dist[dst];\n    }\n}",
                "python": "class Solution:\n    def findCheapestPrice(self, n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:\n        dist = [float('inf')] * n\n        dist[src] = 0\n        for _ in range(k + 1):\n            temp = list(dist)\n            for u, v, w in flights:\n                if dist[u] + w < temp[v]:\n                    temp[v] = dist[u] + w\n            dist = temp\n        return dist[dst] if dist[dst] < float('inf') else -1"
            }
        },
        "optimal": {
            "idea": "Bellman-Ford with copy: run k + 1 relaxation rounds using a snapshot copy of distances to prevent chaining multiple flights in one round.",
            "steps": [
                "int[] dist filled with INF, dist[src] = 0.",
                "For round from 0 to k:",
                "int[] temp = Arrays.copyOf(dist, n).",
                "For flight [u, v, price]: if dist[u] != INF && dist[u] + price < temp[v] temp[v] = dist[u] + price.",
                "dist = temp.",
                "Return dist[dst] != INF ? dist[dst] : -1."
            ],
            "time": "O(k * E)",
            "space": "O(V)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int findCheapestPrice(int n, int[][] flights, int src, int dst, int k) {\n        int[] dist = new int[n];\n        Arrays.fill(dist, Integer.MAX_VALUE);\n        dist[src] = 0;\n        for (int i = 0; i <= k; i++) {\n            int[] temp = Arrays.copyOf(dist, n);\n            for (int[] f : flights) {\n                int u = f[0], v = f[1], price = f[2];\n                if (dist[u] != Integer.MAX_VALUE && dist[u] + price < temp[v]) {\n                    temp[v] = dist[u] + price;\n                }\n            }\n            dist = temp;\n        }\n        return dist[dst] == Integer.MAX_VALUE ? -1 : dist[dst];\n    }\n}",
                "python": "class Solution:\n    def findCheapestPrice(self, n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:\n        dist = [float('inf')] * n\n        dist[src] = 0\n        for _ in range(k + 1):\n            temp = list(dist)\n            for u, v, price in flights:\n                if dist[u] != float('inf') and dist[u] + price < temp[v]:\n                    temp[v] = dist[u] + price\n            dist = temp\n        return dist[dst] if dist[dst] != float('inf') else -1"
            }
        }
    },
    {
        "seq": 229,
        "whyNext": "Modified Dijkstra: edge weight is abs(heights[r][c] - heights[nr][nc]); path effort is max effort along path; minimize total path effort.",
        "brute": {
            "idea": "Binary search on effort [0, 10^6] with BFS/DFS checking if path exists with max diff <= mid.",
            "steps": [
                "Binary search mid in [0, 10^6].",
                "Check connectivity from (0,0) to (m-1, n-1) with edge weights <= mid."
            ],
            "time": "O(m * n * log(max_height))",
            "space": "O(m * n)",
            "whySlow": "Repeated BFS invocations across binary search iterations.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int minimumEffortPath(int[][] heights) {\n        int m = heights.length, n = heights[0].length;\n        int low = 0, high = 1000000;\n        while (low < high) {\n            int mid = low + (high - low) / 2;\n            if (canReach(heights, mid, m, n)) {\n                high = mid;\n            } else {\n                low = mid + 1;\n            }\n        }\n        return low;\n    }\n    private boolean canReach(int[][] h, int maxEffort, int m, int n) {\n        boolean[][] visited = new boolean[m][n];\n        Queue<int[]> q = new LinkedList<>();\n        q.offer(new int[]{0, 0});\n        visited[0][0] = true;\n        int[][] dirs = {{1,0}, {-1,0}, {0,1}, {0,-1}};\n        while (!q.isEmpty()) {\n            int[] cur = q.poll();\n            if (cur[0] == m - 1 && cur[1] == n - 1) return true;\n            for (int[] d : dirs) {\n                int nr = cur[0] + d[0], nc = cur[1] + d[1];\n                if (nr >= 0 && nr < m && nc >= 0 && nc < n && !visited[nr][nc]) {\n                    if (Math.abs(h[nr][nc] - h[cur[0]][cur[1]]) <= maxEffort) {\n                        visited[nr][nc] = true;\n                        q.offer(new int[]{nr, nc});\n                    }\n                }\n            }\n        }\n        return false;\n    }\n}",
                "python": "from collections import deque\n\nclass Solution:\n    def minimumEffortPath(self, heights: list[list[int]]) -> int:\n        m, n = len(heights), len(heights[0])\n        def check(mid):\n            visited = [[False] * n for _ in range(m)]\n            q = deque([(0, 0)])\n            visited[0][0] = True\n            while q:\n                r, c = q.popleft()\n                if r == m - 1 and c == n - 1: return True\n                for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):\n                    nr, nc = r + dr, c + dc\n                    if 0 <= nr < m and 0 <= nc < n and not visited[nr][nc]:\n                        if abs(heights[nr][nc] - heights[r][c]) <= mid:\n                            visited[nr][nc] = True\n                            q.append((nr, nc))\n            return False\n        low, high = 0, 1000000\n        while low < high:\n            mid = (low + high) // 2\n            if check(mid): high = mid\n            else: low = mid + 1\n        return low"
            }
        },
        "optimal": {
            "idea": "Dijkstra with effort: dist[r][c] is min effort to reach (r, c). Next effort = max(curEffort, abs(diff)).",
            "steps": [
                "int[][] dist filled with INF, dist[0][0] = 0.",
                "PriorityQueue<int[]> stores (effort, r, c).",
                "Poll (effort, r, c): if r == m - 1 && c == n - 1 return effort.",
                "For 4 neighbors: newEffort = max(effort, abs(heights[nr][nc] - heights[r][c])).",
                "If newEffort < dist[nr][nc]: dist[nr][nc] = newEffort, pq.offer(newEffort, nr, nc)."
            ],
            "time": "O(m * n * log(m * n))",
            "space": "O(m * n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int minimumEffortPath(int[][] heights) {\n        int m = heights.length, n = heights[0].length;\n        int[][] dist = new int[m][n];\n        for (int[] row : dist) Arrays.fill(row, Integer.MAX_VALUE);\n        dist[0][0] = 0;\n        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[0]));\n        pq.offer(new int[]{0, 0, 0});\n        int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};\n        while (!pq.isEmpty()) {\n            int[] cur = pq.poll();\n            int effort = cur[0], r = cur[1], c = cur[2];\n            if (r == m - 1 && c == n - 1) return effort;\n            if (effort > dist[r][c]) continue;\n            for (int[] d : dirs) {\n                int nr = r + d[0], nc = c + d[1];\n                if (nr >= 0 && nr < m && nc >= 0 && nc < n) {\n                    int nextEffort = Math.max(effort, Math.abs(heights[nr][nc] - heights[r][c]));\n                    if (nextEffort < dist[nr][nc]) {\n                        dist[nr][nc] = nextEffort;\n                        pq.offer(new int[]{nextEffort, nr, nc});\n                    }\n                }\n            }\n        }\n        return 0;\n    }\n}",
                "python": "import heapq\n\nclass Solution:\n    def minimumEffortPath(self, heights: list[list[int]]) -> int:\n        m, n = len(heights), len(heights[0])\n        dist = [[float('inf')] * n for _ in range(m)]\n        dist[0][0] = 0\n        pq = [(0, 0, 0)]\n        while pq:\n            effort, r, c = heapq.heappop(pq)\n            if r == m - 1 and c == n - 1:\n                return effort\n            if effort > dist[r][c]:\n                continue\n            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n                nr, nc = r + dr, c + dc\n                if 0 <= nr < m and 0 <= nc < n:\n                    nxt_eff = max(effort, abs(heights[nr][nc] - heights[r][c]))\n                    if nxt_eff < dist[nr][nc]:\n                        dist[nr][nc] = nxt_eff\n                        heapq.heappush(pq, (nxt_eff, nr, nc))\n        return 0"
            }
        }
    },
    {
        "seq": 230,
        "whyNext": "Builds on Path With Minimum Effort: path weight is max(grid[r][c]) along the path; Dijkstra with PriorityQueue finds min time.",
        "brute": {
            "idea": "Binary search on time t in [0, n*n - 1]; check if path exists from (0,0) to (n-1, n-1) with grid[r][c] <= t.",
            "steps": [
                "Binary search on time t.",
                "Run BFS on cells with grid[r][c] <= t."
            ],
            "time": "O(n^2 log(n^2))",
            "space": "O(n^2)",
            "whySlow": "Multiple BFS passes over binary search range.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int swimInWater(int[][] grid) {\n        int n = grid.length;\n        int low = Math.max(grid[0][0], grid[n - 1][n - 1]), high = n * n - 1;\n        while (low < high) {\n            int mid = low + (high - low) / 2;\n            if (canReach(grid, mid, n)) {\n                high = mid;\n            } else {\n                low = mid + 1;\n            }\n        }\n        return low;\n    }\n    private boolean canReach(int[][] g, int t, int n) {\n        boolean[][] visited = new boolean[n][n];\n        Queue<int[]> q = new LinkedList<>();\n        q.offer(new int[]{0, 0});\n        visited[0][0] = true;\n        int[][] dirs = {{1,0}, {-1,0}, {0,1}, {0,-1}};\n        while (!q.isEmpty()) {\n            int[] cur = q.poll();\n            if (cur[0] == n - 1 && cur[1] == n - 1) return true;\n            for (int[] d : dirs) {\n                int nr = cur[0] + d[0], nc = cur[1] + d[1];\n                if (nr >= 0 && nr < n && nc >= 0 && nc < n && !visited[nr][nc] && g[nr][nc] <= t) {\n                    visited[nr][nc] = true;\n                    q.offer(new int[]{nr, nc});\n                }\n            }\n        }\n        return false;\n    }\n}",
                "python": "from collections import deque\n\nclass Solution:\n    def swimInWater(self, grid: list[list[int]]) -> int:\n        n = len(grid)\n        def check(t):\n            visited = [[False] * n for _ in range(n)]\n            q = deque([(0, 0)])\n            visited[0][0] = True\n            while q:\n                r, c = q.popleft()\n                if r == n - 1 and c == n - 1: return True\n                for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):\n                    nr, nc = r + dr, c + dc\n                    if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and grid[nr][nc] <= t:\n                        visited[nr][nc] = True\n                        q.append((nr, nc))\n            return False\n        low = max(grid[0][0], grid[n-1][n-1])\n        high = n * n - 1\n        while low < high:\n            mid = (low + high) // 2\n            if check(mid): high = mid\n            else: low = mid + 1\n        return low"
            }
        },
        "optimal": {
            "idea": "Dijkstra: min-heap storing (max_elevation, r, c); always advance to lowest elevation neighbor; return when reaching (n-1, n-1).",
            "steps": [
                "boolean[][] visited = new boolean[n][n].",
                "PriorityQueue<int[]> stores (time, r, c).",
                "Offer (grid[0][0], 0, 0); visited[0][0] = true.",
                "Poll (t, r, c): if r == n - 1 && c == n - 1 return t.",
                "For 4 neighbors: if unvisited, mark visited, push (max(t, grid[nr][nc]), nr, nc)."
            ],
            "time": "O(n^2 log n)",
            "space": "O(n^2)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int swimInWater(int[][] grid) {\n        int n = grid.length;\n        boolean[][] visited = new boolean[n][n];\n        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[0]));\n        pq.offer(new int[]{grid[0][0], 0, 0});\n        visited[0][0] = true;\n        int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};\n        while (!pq.isEmpty()) {\n            int[] cur = pq.poll();\n            int t = cur[0], r = cur[1], c = cur[2];\n            if (r == n - 1 && c == n - 1) return t;\n            for (int[] d : dirs) {\n                int nr = r + d[0], nc = c + d[1];\n                if (nr >= 0 && nr < n && nc >= 0 && nc < n && !visited[nr][nc]) {\n                    visited[nr][nc] = true;\n                    pq.offer(new int[]{Math.max(t, grid[nr][nc]), nr, nc});\n                }\n            }\n        }\n        return 0;\n    }\n}",
                "python": "import heapq\n\nclass Solution:\n    def swimInWater(self, grid: list[list[int]]) -> int:\n        n = len(grid)\n        visited = [[False] * n for _ in range(n)]\n        pq = [(grid[0][0], 0, 0)]\n        visited[0][0] = True\n        while pq:\n            t, r, c = heapq.heappop(pq)\n            if r == n - 1 and c == n - 1:\n                return t\n            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n                nr, nc = r + dr, c + dc\n                if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc]:\n                    visited[nr][nc] = True\n                    heapq.heappush(pq, (max(t, grid[nr][nc]), nr, nc))\n        return 0"
            }
        }
    },
    {
        "seq": 231,
        "whyNext": "Max-probability Dijkstra: edge weights multiply (prob in [0, 1]); max-heap finds highest probability path to end.",
        "brute": {
            "idea": "Bellman-Ford variant relaxing edge probabilities n - 1 times.",
            "steps": [
                "prob[start] = 1.0.",
                "Repeat n - 1 times: for each edge (u, v, p), prob[v] = max(prob[v], prob[u] * p)."
            ],
            "time": "O(V * E)",
            "space": "O(V)",
            "whySlow": "Relaxes all edges V times.",
            "code": {
                "java": "class Solution {\n    public double maxProbability(int n, int[][] edges, double[] succProb, int start_node, int end_node) {\n        double[] prob = new double[n];\n        prob[start_node] = 1.0;\n        for (int i = 0; i < n - 1; i++) {\n            boolean updated = false;\n            for (int j = 0; j < edges.length; j++) {\n                int u = edges[j][0], v = edges[j][1];\n                double p = succProb[j];\n                if (prob[u] * p > prob[v]) {\n                    prob[v] = prob[u] * p;\n                    updated = true;\n                }\n                if (prob[v] * p > prob[u]) {\n                    prob[u] = prob[v] * p;\n                    updated = true;\n                }\n            }\n            if (!updated) break;\n        }\n        return prob[end_node];\n    }\n}",
                "python": "class Solution:\n    def maxProbability(self, n: int, edges: list[list[int]], succProb: list[float], start_node: int, end_node: int) -> float:\n        prob = [0.0] * n\n        prob[start_node] = 1.0\n        for _ in range(n - 1):\n            updated = False\n            for (u, v), p in zip(edges, succProb):\n                if prob[u] * p > prob[v]:\n                    prob[v] = prob[u] * p\n                    updated = True\n                if prob[v] * p > prob[u]:\n                    prob[u] = prob[v] * p\n                    updated = True\n            if not updated: break\n        return prob[end_node]"
            }
        },
        "optimal": {
            "idea": "Dijkstra with Max-Heap: double[] prob = new double[n]; max-heap polls highest probability node first.",
            "steps": [
                "Build adjacency list: adj[u] -> (v, p).",
                "double[] prob = new double[n]; prob[start] = 1.0.",
                "PriorityQueue<Pair> max-heap comparing prob descending.",
                "Poll (p, u): if u == end_node return p.",
                "For (v, edgeP) in adj[u]: if p * edgeP > prob[v]: prob[v] = p * edgeP, push to heap."
            ],
            "time": "O(E log V)",
            "space": "O(V + E)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public double maxProbability(int n, int[][] edges, double[] succProb, int start, int end) {\n        List<double[]>[] adj = new List[n];\n        for (int i = 0; i < n; i++) adj[i] = new ArrayList<>();\n        for (int i = 0; i < edges.length; i++) {\n            int u = edges[i][0], v = edges[i][1];\n            double p = succProb[i];\n            adj[u].add(new double[]{v, p});\n            adj[v].add(new double[]{u, p});\n        }\n        double[] probs = new double[n];\n        probs[start] = 1.0;\n        PriorityQueue<double[]> pq = new PriorityQueue<>((a, b) -> Double.compare(b[0], a[0]));\n        pq.offer(new double[]{1.0, start});\n        while (!pq.isEmpty()) {\n            double[] cur = pq.poll();\n            double p = cur[0];\n            int u = (int) cur[1];\n            if (u == end) return p;\n            if (p < probs[u]) continue;\n            for (double[] edge : adj[u]) {\n                int v = (int) edge[0];\n                double weight = edge[1];\n                if (p * weight > probs[v]) {\n                    probs[v] = p * weight;\n                    pq.offer(new double[]{probs[v], v});\n                }\n            }\n        }\n        return 0.0;\n    }\n}",
                "python": "import heapq\nfrom collections import defaultdict\n\nclass Solution:\n    def maxProbability(self, n: int, edges: list[list[int]], succProb: list[float], start_node: int, end_node: int) -> float:\n        adj = defaultdict(list)\n        for (u, v), p in zip(edges, succProb):\n            adj[u].append((v, p))\n            adj[v].append((u, p))\n        probs = [0.0] * n\n        probs[start_node] = 1.0\n        pq = [(-1.0, start_node)]\n        while pq:\n            neg_p, u = heapq.heappop(pq)\n            p = -neg_p\n            if u == end_node:\n                return p\n            if p < probs[u]:\n                continue\n            for v, weight in adj[u]:\n                if p * weight > probs[v]:\n                    probs[v] = p * weight\n                    heapq.heappush(pq, (-probs[v], v))\n        return 0.0"
            }
        }
    },
    {
        "seq": 232,
        "whyNext": "Minimum Spanning Tree (MST): Prim's algorithm with min-heap connects all points with minimum total Manhattan distance.",
        "brute": {
            "idea": "Kruskal's algorithm: generate all n*(n-1)/2 edges, sort by Manhattan distance, and union with DSU.",
            "steps": [
                "Generate all edges.",
                "Sort edges.",
                "Kruskal's with DSU."
            ],
            "time": "O(n^2 log(n^2))",
            "space": "O(n^2)",
            "whySlow": "Stores and sorts all O(n^2) edges in memory.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int minCostConnectPoints(int[][] points) {\n        int n = points.length;\n        List<int[]> edges = new ArrayList<>();\n        for (int i = 0; i < n; i++) {\n            for (int j = i + 1; j < n; j++) {\n                int d = Math.abs(points[i][0] - points[j][0]) + Math.abs(points[i][1] - points[j][1]);\n                edges.add(new int[]{d, i, j});\n            }\n        }\n        edges.sort(Comparator.comparingInt(a -> a[0]));\n        int[] parent = new int[n];\n        for (int i = 0; i < n; i++) parent[i] = i;\n        int cost = 0, count = 0;\n        for (int[] e : edges) {\n            int ru = find(parent, e[1]), rv = find(parent, e[2]);\n            if (ru != rv) {\n                parent[ru] = rv;\n                cost += e[0];\n                if (++count == n - 1) break;\n            }\n        }\n        return cost;\n    }\n    private int find(int[] p, int i) {\n        if (p[i] == i) return i;\n        return p[i] = find(p, p[i]);\n    }\n}",
                "python": "class Solution:\n    def minCostConnectPoints(self, points: list[list[int]]) -> int:\n        n = len(points)\n        edges = []\n        for i in range(n):\n            for j in range(i + 1, n):\n                d = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])\n                edges.append((d, i, j))\n        edges.sort()\n        parent = list(range(n))\n        def find(i):\n            if parent[i] == i: return i\n            parent[i] = find(parent[i])\n            return parent[i]\n        cost = 0\n        count = 0\n        for d, u, v in edges:\n            ru, rv = find(u), find(v)\n            if ru != rv:\n                parent[ru] = rv\n                cost += d\n                count += 1\n                if count == n - 1: break\n        return cost"
            }
        },
        "optimal": {
            "idea": "Prim's Algorithm: maintain minCost array to MST; in each of the n steps, pick nearest unvisited point, add to MST, and update neighbors in O(n^2) and O(n) space.",
            "steps": [
                "int[] minDist filled with INF, minDist[0] = 0; boolean[] inMST.",
                "For i = 0..n-1: find unvisited u with minimum minDist[u].",
                "inMST[u] = true; totalCost += minDist[u].",
                "Update minDist[v] for all unvisited v with dist(u, v).",
                "Return totalCost."
            ],
            "time": "O(n^2)",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int minCostConnectPoints(int[][] points) {\n        int n = points.length;\n        int[] minDist = new int[n];\n        Arrays.fill(minDist, Integer.MAX_VALUE);\n        minDist[0] = 0;\n        boolean[] inMST = new boolean[n];\n        int totalCost = 0;\n        for (int step = 0; step < n; step++) {\n            int u = -1;\n            for (int i = 0; i < n; i++) {\n                if (!inMST[i] && (u == -1 || minDist[i] < minDist[u])) {\n                    u = i;\n                }\n            }\n            inMST[u] = true;\n            totalCost += minDist[u];\n            for (int v = 0; v < n; v++) {\n                if (!inMST[v]) {\n                    int d = Math.abs(points[u][0] - points[v][0]) + Math.abs(points[u][1] - points[v][1]);\n                    if (d < minDist[v]) {\n                        minDist[v] = d;\n                    }\n                }\n            }\n        }\n        return totalCost;\n    }\n}",
                "python": "class Solution:\n    def minCostConnectPoints(self, points: list[list[int]]) -> int:\n        n = len(points)\n        min_dist = [float('inf')] * n\n        min_dist[0] = 0\n        in_mst = [False] * n\n        total_cost = 0\n        for _ in range(n):\n            u = -1\n            for i in range(n):\n                if not in_mst[i] and (u == -1 or min_dist[i] < min_dist[u]):\n                    u = i\n            in_mst[u] = True\n            total_cost += min_dist[u]\n            x1, y1 = points[u]\n            for v in range(n):\n                if not in_mst[v]:\n                    x2, y2 = points[v]\n                    d = abs(x1 - x2) + abs(y1 - y2)\n                    if d < min_dist[v]:\n                        min_dist[v] = d\n        return total_cost"
            }
        }
    },
    {
        "seq": 233,
        "whyNext": "Hierholzer's algorithm for Eulerian path: sort outgoing destinations lexicographically with PriorityQueue; post-order DFS build.",
        "brute": {
            "idea": "Backtracking trying destinations in alphabetical order until a path uses all tickets.",
            "steps": [
                "Backtrack DFS.",
                "Mark ticket used, backtrack if path cannot finish all tickets."
            ],
            "time": "O(V!)",
            "space": "O(V + E)",
            "whySlow": "Backtracking explores dead-end paths repeatedly instead of Hierholzer's post-order stitch.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<String> findItinerary(List<List<String>> tickets) {\n        Map<String, PriorityQueue<String>> targets = new HashMap<>();\n        for (List<String> ticket : tickets) {\n            targets.computeIfAbsent(ticket.get(0), k -> new PriorityQueue<>()).add(ticket.get(1));\n        }\n        LinkedList<String> route = new LinkedList<>();\n        visit(\"JFK\", targets, route);\n        return route;\n    }\n    private void visit(String airport, Map<String, PriorityQueue<String>> targets, LinkedList<String> route) {\n        while (targets.containsKey(airport) && !targets.get(airport).isEmpty()) {\n            visit(targets.get(airport).poll(), targets, route);\n        }\n        route.addFirst(airport);\n    }\n}",
                "python": "from collections import defaultdict\nimport heapq\n\nclass Solution:\n    def findItinerary(self, tickets: list[list[str]]) -> list[str]:\n        targets = defaultdict(list)\n        for src, dst in tickets:\n            heapq.heappush(targets[src], dst)\n        route = []\n        def visit(airport):\n            while targets[airport]:\n                visit(heapq.heappop(targets[airport]))\n            route.append(airport)\n        visit(\"JFK\")\n        return route[::-1]"
            }
        },
        "optimal": {
            "idea": "Hierholzer's Algorithm: Map<String, PriorityQueue<String>>; post-order DFS adds airport when all outgoing edges consumed, then reverse route.",
            "steps": [
                "Map each airport to PriorityQueue of destination airports.",
                "dfs(airport): while targets.get(airport) not empty, pop smallest destination and recurse.",
                "route.addFirst(airport).",
                "Start at 'JFK'; return route."
            ],
            "time": "O(E log E)",
            "space": "O(V + E)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    private Map<String, PriorityQueue<String>> graph = new HashMap<>();\n    private LinkedList<String> route = new LinkedList<>();\n    public List<String> findItinerary(List<List<String>> tickets) {\n        for (List<String> t : tickets) {\n            graph.computeIfAbsent(t.get(0), k -> new PriorityQueue<>()).offer(t.get(1));\n        }\n        dfs(\"JFK\");\n        return route;\n    }\n    private void dfs(String airport) {\n        PriorityQueue<String> dests = graph.get(airport);\n        while (dests != null && !dests.isEmpty()) {\n            dfs(dests.poll());\n        }\n        route.addFirst(airport);\n    }\n}",
                "python": "import heapq\nfrom collections import defaultdict\n\nclass Solution:\n    def findItinerary(self, tickets: list[list[str]]) -> list[str]:\n        graph = defaultdict(list)\n        for u, v in tickets:\n            heapq.heappush(graph[u], v)\n        route = []\n        def dfs(airport: str):\n            while graph[airport]:\n                dfs(heapq.heappop(graph[airport]))\n            route.append(airport)\n        dfs(\"JFK\")\n        return route[::-1]"
            }
        }
    },
    {
        "seq": 234,
        "whyNext": "All-pairs shortest path: Floyd-Warshall computes shortest distances between all city pairs; pick city with minimum reachable cities (tie-break higher index).",
        "brute": {
            "idea": "Run Dijkstra from each city 0..n-1 independently to count reachable cities within distanceThreshold.",
            "steps": [
                "Run Dijkstra from city 0 to n - 1.",
                "Count reachable cities.",
                "Track city with min count."
            ],
            "time": "O(n * E log n)",
            "space": "O(n + E)",
            "whySlow": "Running n separate Dijkstra priority queue passes.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int findTheCity(int n, int[][] edges, int distanceThreshold) {\n        int[][] dist = new int[n][n];\n        for (int[] row : dist) Arrays.fill(row, 10000000);\n        for (int i = 0; i < n; i++) dist[i][i] = 0;\n        for (int[] e : edges) {\n            dist[e[0]][e[1]] = e[2];\n            dist[e[1]][e[0]] = e[2];\n        }\n        for (int k = 0; k < n; k++) {\n            for (int i = 0; i < n; i++) {\n                for (int j = 0; j < n; j++) {\n                    dist[i][j] = Math.min(dist[i][j], dist[i][k] + dist[k][j]);\n                }\n            }\n        }\n        int bestCity = -1, minReachable = Integer.MAX_VALUE;\n        for (int i = 0; i < n; i++) {\n            int reachable = 0;\n            for (int j = 0; j < n; j++) {\n                if (i != j && dist[i][j] <= distanceThreshold) reachable++;\n            }\n            if (reachable <= minReachable) {\n                minReachable = reachable;\n                bestCity = i;\n            }\n        }\n        return bestCity;\n    }\n}",
                "python": "class Solution:\n    def findTheCity(self, n: int, edges: list[list[int]], distanceThreshold: int) -> int:\n        dist = [[float('inf')] * n for _ in range(n)]\n        for i in range(n): dist[i][i] = 0\n        for u, v, w in edges:\n            dist[u][v] = dist[v][u] = w\n        for k in range(n):\n            for i in range(n):\n                for j in range(n):\n                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])\n        best_city, min_cnt = -1, float('inf')\n        for i in range(n):\n            cnt = sum(1 for j in range(n) if i != j and dist[i][j] <= distanceThreshold)\n            if cnt <= min_cnt:\n                min_cnt = cnt\n                best_city = i\n        return best_city"
            }
        },
        "optimal": {
            "idea": "Floyd-Warshall Algorithm: dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]). Count cities with dist <= threshold; pick smallest count with largest index.",
            "steps": [
                "Initialize n x n matrix with INF, dist[i][i] = 0.",
                "Fill edge weights dist[u][v] = dist[v][u] = w.",
                "Triple loop k, i, j: dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]).",
                "For i = 0..n-1: count reachable; if count <= minCount { minCount = count; bestCity = i; }",
                "Return bestCity."
            ],
            "time": "O(n^3)",
            "space": "O(n^2)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int findTheCity(int n, int[][] edges, int distanceThreshold) {\n        int[][] dist = new int[n][n];\n        for (int[] row : dist) Arrays.fill(row, 10000000);\n        for (int i = 0; i < n; i++) dist[i][i] = 0;\n        for (int[] e : edges) {\n            dist[e[0]][e[1]] = e[2];\n            dist[e[1]][e[0]] = e[2];\n        }\n        for (int k = 0; k < n; k++) {\n            for (int i = 0; i < n; i++) {\n                for (int j = 0; j < n; j++) {\n                    dist[i][j] = Math.min(dist[i][j], dist[i][k] + dist[k][j]);\n                }\n            }\n        }\n        int minCount = Integer.MAX_VALUE;\n        int bestCity = -1;\n        for (int i = 0; i < n; i++) {\n            int reachable = 0;\n            for (int j = 0; j < n; j++) {\n                if (i != j && dist[i][j] <= distanceThreshold) {\n                    reachable++;\n                }\n            }\n            if (reachable <= minCount) {\n                minCount = reachable;\n                bestCity = i;\n            }\n        }\n        return bestCity;\n    }\n}",
                "python": "class Solution:\n    def findTheCity(self, n: int, edges: list[list[int]], distanceThreshold: int) -> int:\n        dist = [[float('inf')] * n for _ in range(n)]\n        for i in range(n):\n            dist[i][i] = 0\n        for u, v, w in edges:\n            dist[u][v] = dist[v][u] = w\n        for k in range(n):\n            for i in range(n):\n                for j in range(n):\n                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])\n        best_city = -1\n        min_reachable = float('inf')\n        for i in range(n):\n            cnt = sum(1 for j in range(n) if i != j and dist[i][j] <= distanceThreshold)\n            if cnt <= min_reachable:\n                min_reachable = cnt\n                best_city = i\n        return best_city"
            }
        }
    },
    {
        "seq": 235,
        "whyNext": "Entry to Chapter 14 (1D Dynamic Programming): dp[i] = dp[i-1] + dp[i-2]; state compression achieves O(1) space.",
        "brute": {
            "idea": "Naive recursion: climb(n) = climb(n-1) + climb(n-2).",
            "steps": [
                "Base cases: if n <= 2 return n.",
                "Return climb(n-1) + climb(n-2)."
            ],
            "time": "O(2^n)",
            "space": "O(n)",
            "whySlow": "Exponential redundant subproblem re-computation.",
            "code": {
                "java": "class Solution {\n    public int climbStairs(int n) {\n        if (n <= 2) return n;\n        return climbStairs(n - 1) + climbStairs(n - 2);\n    }\n}",
                "python": "class Solution:\n    def climbStairs(self, n: int) -> int:\n        if n <= 2: return n\n        return self.climbStairs(n - 1) + self.climbStairs(n - 2)"
            }
        },
        "optimal": {
            "idea": "State compression DP: maintain two variables prev1 = 1, prev2 = 2. Update cur = prev1 + prev2.",
            "steps": [
                "If n <= 2 return n.",
                "a = 1, b = 2.",
                "For i = 3..n: c = a + b, a = b, b = c.",
                "Return b."
            ],
            "time": "O(n)",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public int climbStairs(int n) {\n        if (n <= 2) return n;\n        int a = 1, b = 2;\n        for (int i = 3; i <= n; i++) {\n            int c = a + b;\n            a = b;\n            b = c;\n        }\n        return b;\n    }\n}",
                "python": "class Solution:\n    def climbStairs(self, n: int) -> int:\n        if n <= 2:\n            return n\n        a, b = 1, 2\n        for _ in range(3, n + 1):\n            a, b = b, a + b\n        return b"
            }
        }
    },
    {
        "seq": 236,
        "whyNext": "Builds on Climbing Stairs: dp[i] = cost[i] + min(dp[i-1], dp[i-2]); minimize cost to reach the top.",
        "brute": {
            "idea": "Recursive search checking both 1-step and 2-step transitions.",
            "steps": [
                "minCost(step): cost[step] + min(minCost(step+1), minCost(step+2))."
            ],
            "time": "O(2^n)",
            "space": "O(n)",
            "whySlow": "Recomputes subtree costs exponentially.",
            "code": {
                "java": "class Solution {\n    public int minCostClimbingStairs(int[] cost) {\n        return Math.min(dfs(cost, 0), dfs(cost, 1));\n    }\n    private int dfs(int[] cost, int idx) {\n        if (idx >= cost.length) return 0;\n        return cost[idx] + Math.min(dfs(cost, idx + 1), dfs(cost, idx + 2));\n    }\n}",
                "python": "class Solution:\n    def minCostClimbingStairs(self, cost: list[int]) -> int:\n        def dfs(i):\n            if i >= len(cost): return 0\n            return cost[i] + min(dfs(i + 1), dfs(i + 2))\n        return min(dfs(0), dfs(1))"
            }
        },
        "optimal": {
            "idea": "O(1) space DP: prev1 = 0, prev2 = 0; cur = min(prev1 + cost[i-1], prev2 + cost[i-2]).",
            "steps": [
                "prev1 = 0, prev2 = 0.",
                "For i from 2 to cost.length:",
                "cur = Math.min(prev1 + cost[i - 1], prev2 + cost[i - 2]).",
                "prev2 = prev1; prev1 = cur.",
                "Return prev1."
            ],
            "time": "O(n)",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public int minCostClimbingStairs(int[] cost) {\n        int a = 0, b = 0;\n        for (int i = 2; i <= cost.length; i++) {\n            int c = Math.min(a + cost[i - 2], b + cost[i - 1]);\n            a = b;\n            b = c;\n        }\n        return b;\n    }\n}",
                "python": "class Solution:\n    def minCostClimbingStairs(self, cost: list[int]) -> int:\n        a = b = 0\n        for i in range(2, len(cost) + 1):\n            c = min(a + cost[i - 2], b + cost[i - 1])\n            a, b = b, c\n        return b"
            }
        }
    },
    {
        "seq": 237,
        "whyNext": "3-term recurrence: T_n = T_{n-1} + T_{n-2} + T_{n-3}; 3 state variables maintain O(1) space.",
        "brute": {
            "idea": "Naive 3-way recursion T(n) = T(n-1) + T(n-2) + T(n-3).",
            "steps": [
                "Base cases T(0)=0, T(1)=1, T(2)=1.",
                "Return sum of previous 3 values."
            ],
            "time": "O(3^n)",
            "space": "O(n)",
            "whySlow": "Exponential 3^n branching.",
            "code": {
                "java": "class Solution {\n    public int tribonacci(int n) {\n        if (n == 0) return 0;\n        if (n <= 2) return 1;\n        return tribonacci(n - 1) + tribonacci(n - 2) + tribonacci(n - 3);\n    }\n}",
                "python": "class Solution:\n    def tribonacci(self, n: int) -> int:\n        if n == 0: return 0\n        if n <= 2: return 1\n        return self.tribonacci(n - 1) + self.tribonacci(n - 2) + self.tribonacci(n - 3)"
            }
        },
        "optimal": {
            "idea": "Rolling variables a = 0, b = 1, c = 1: update d = a + b + c, a = b, b = c, c = d in O(n) time and O(1) space.",
            "steps": [
                "If n == 0 return 0; if n <= 2 return 1.",
                "a = 0, b = 1, c = 1.",
                "For i from 3 to n: d = a + b + c, a = b, b = c, c = d.",
                "Return c."
            ],
            "time": "O(n)",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public int tribonacci(int n) {\n        if (n == 0) return 0;\n        if (n <= 2) return 1;\n        int a = 0, b = 1, c = 1;\n        for (int i = 3; i <= n; i++) {\n            int d = a + b + c;\n            a = b;\n            b = c;\n            c = d;\n        }\n        return c;\n    }\n}",
                "python": "class Solution:\n    def tribonacci(self, n: int) -> int:\n        if n == 0:\n            return 0\n        if n <= 2:\n            return 1\n        a, b, c = 0, 1, 1\n        for _ in range(3, n + 1):\n            a, b, c = b, c, a + b + c\n        return c"
            }
        }
    },
    {
        "seq": 238,
        "whyNext": "Non-adjacent selection DP: rob[i] = max(rob[i-1], rob[i-2] + nums[i]); 2 state variables achieve O(1) space.",
        "brute": {
            "idea": "Recursion: at each house, either rob (skip next) or skip (rob next).",
            "steps": [
                "dfs(idx): max(nums[idx] + dfs(idx+2), dfs(idx+1))."
            ],
            "time": "O(2^n)",
            "space": "O(n)",
            "whySlow": "Exponential recursion.",
            "code": {
                "java": "class Solution {\n    public int rob(int[] nums) {\n        return dfs(nums, 0);\n    }\n    private int dfs(int[] nums, int i) {\n        if (i >= nums.length) return 0;\n        return Math.max(nums[i] + dfs(nums, i + 2), dfs(nums, i + 1));\n    }\n}",
                "python": "class Solution:\n    def rob(self, nums: list[int]) -> int:\n        def dfs(i):\n            if i >= len(nums): return 0\n            return max(nums[i] + dfs(i + 2), dfs(i + 1))\n        return dfs(0)"
            }
        },
        "optimal": {
            "idea": "O(1) space DP: prev1 = max profit up to i-1, prev2 = max profit up to i-2. cur = max(prev1, prev2 + x).",
            "steps": [
                "prev1 = 0, prev2 = 0.",
                "For x in nums: cur = Math.max(prev1, prev2 + x); prev2 = prev1; prev1 = cur.",
                "Return prev1."
            ],
            "time": "O(n)",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public int rob(int[] nums) {\n        int prev1 = 0, prev2 = 0;\n        for (int x : nums) {\n            int cur = Math.max(prev1, prev2 + x);\n            prev2 = prev1;\n            prev1 = cur;\n        }\n        return prev1;\n    }\n}",
                "python": "class Solution:\n    def rob(self, nums: list[int]) -> int:\n        prev1 = prev2 = 0\n        for x in nums:\n            prev1, prev2 = max(prev1, prev2 + x), prev1\n        return prev1"
            }
        }
    },
    {
        "seq": 239,
        "whyNext": "Circular array constraint: first and last houses are adjacent; answer is max(rob(0..n-2), rob(1..n-1)).",
        "brute": {
            "idea": "Try both possibilities: rob house 0 (cannot rob house n-1), or skip house 0 (can rob house n-1).",
            "steps": [
                "Call linear rob on nums[0..n-2].",
                "Call linear rob on nums[1..n-1].",
                "Take maximum."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "whySlow": "Allocates sliced sub-arrays instead of pointer bounds.",
            "code": {
                "java": "class Solution {\n    public int rob(int[] nums) {\n        if (nums.length == 1) return nums[0];\n        return Math.max(robRange(nums, 0, nums.length - 2), robRange(nums, 1, nums.length - 1));\n    }\n    private int robRange(int[] nums, int l, int r) {\n        int prev1 = 0, prev2 = 0;\n        for (int i = l; i <= r; i++) {\n            int cur = Math.max(prev1, prev2 + nums[i]);\n            prev2 = prev1;\n            prev1 = cur;\n        }\n        return prev1;\n    }\n}",
                "python": "class Solution:\n    def rob(self, nums: list[int]) -> int:\n        if len(nums) == 1: return nums[0]\n        def rob_simple(arr):\n            p1 = p2 = 0\n            for x in arr:\n                p1, p2 = max(p1, p2 + x), p1\n            return p1\n        return max(rob_simple(nums[:-1]), rob_simple(nums[1:]))"
            }
        },
        "optimal": {
            "idea": "Break circular dependency into 2 linear subproblems: robRange(0, n-2) and robRange(1, n-1) with O(1) space.",
            "steps": [
                "If nums.length == 1 return nums[0].",
                "Define helper robRange(nums, start, end) using 2 rolling variables.",
                "Return Math.max(robRange(nums, 0, n - 2), robRange(nums, 1, n - 1))."
            ],
            "time": "O(n)",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public int rob(int[] nums) {\n        if (nums.length == 1) return nums[0];\n        return Math.max(robLinear(nums, 0, nums.length - 2), robLinear(nums, 1, nums.length - 1));\n    }\n    private int robLinear(int[] nums, int start, int end) {\n        int prev1 = 0, prev2 = 0;\n        for (int i = start; i <= end; i++) {\n            int cur = Math.max(prev1, prev2 + nums[i]);\n            prev2 = prev1;\n            prev1 = cur;\n        }\n        return prev1;\n    }\n}",
                "python": "class Solution:\n    def rob(self, nums: list[int]) -> int:\n        if len(nums) == 1:\n            return nums[0]\n        def rob_linear(start: int, end: int) -> int:\n            p1 = p2 = 0\n            for i in range(start, end + 1):\n                p1, p2 = max(p1, p2 + nums[i]), p1\n            return p1\n        return max(rob_linear(0, len(nums) - 2), rob_linear(1, len(nums) - 1))"
            }
        }
    },
    {
        "seq": 240,
        "whyNext": "Reduction to House Robber: taking x deletes x-1 and x+1; points array points[v] = v * count[v] reduces directly to House Robber.",
        "brute": {
            "idea": "Recursively decide whether to pick each unique number; if picked, delete num-1 and num+1.",
            "steps": [
                "Sort unique numbers.",
                "Recursive branching with used sets."
            ],
            "time": "O(2^u)",
            "space": "O(u)",
            "whySlow": "Exponential branching.",
            "code": {
                "java": "class Solution {\n    public int deleteAndEarn(int[] nums) {\n        int max = 0;\n        for (int x : nums) max = Math.max(max, x);\n        int[] points = new int[max + 1];\n        for (int x : nums) points[x] += x;\n        int p1 = 0, p2 = 0;\n        for (int p : points) {\n            int cur = Math.max(p1, p2 + p);\n            p2 = p1;\n            p1 = cur;\n        }\n        return p1;\n    }\n}",
                "python": "class Solution:\n    def deleteAndEarn(self, nums: list[int]) -> int:\n        max_val = max(nums)\n        points = [0] * (max_val + 1)\n        for x in nums: points[x] += x\n        p1 = p2 = 0\n        for p in points:\n            p1, p2 = max(p1, p2 + p), p1\n        return p1"
            }
        },
        "optimal": {
            "idea": "Map to House Robber: points[v] = v * count[v] for v in 1..max_val. Apply linear House Robber DP on points array.",
            "steps": [
                "Find maxVal in nums.",
                "int[] points = new int[maxVal + 1]; accumulate points[x] += x.",
                "Apply House Robber with 2 variables on points array.",
                "Return result."
            ],
            "time": "O(n + maxVal)",
            "space": "O(maxVal)",
            "code": {
                "java": "class Solution {\n    public int deleteAndEarn(int[] nums) {\n        int max = 0;\n        for (int x : nums) max = Math.max(max, x);\n        int[] points = new int[max + 1];\n        for (int x : nums) points[x] += x;\n        int prev1 = 0, prev2 = 0;\n        for (int p : points) {\n            int cur = Math.max(prev1, prev2 + p);\n            prev2 = prev1;\n            prev1 = cur;\n        }\n        return prev1;\n    }\n}",
                "python": "class Solution:\n    def deleteAndEarn(self, nums: list[int]) -> int:\n        max_val = max(nums)\n        points = [0] * (max_val + 1)\n        for x in nums:\n            points[x] += x\n        p1 = p2 = 0\n        for p in points:\n            p1, p2 = max(p1, p2 + p), p1\n        return p1"
            }
        }
    },
    {
        "seq": 241,
        "whyNext": "Variable-step DP: single-digit decode (if s[i] != '0') + two-digit decode (if 10 <= s[i-1..i] <= 26).",
        "brute": {
            "idea": "Recursive branching: try 1-digit decode if valid, try 2-digit decode if valid.",
            "steps": [
                "dfs(index): if index == n return 1.",
                "Try 1 digit and 2 digits."
            ],
            "time": "O(2^n)",
            "space": "O(n)",
            "whySlow": "Exponential recursion.",
            "code": {
                "java": "class Solution {\n    public int numDecodings(String s) {\n        return dfs(s, 0);\n    }\n    private int dfs(String s, int idx) {\n        if (idx == s.length()) return 1;\n        if (s.charAt(idx) == '0') return 0;\n        int ways = dfs(s, idx + 1);\n        if (idx + 1 < s.length()) {\n            int val = Integer.parseInt(s.substring(idx, idx + 2));\n            if (val <= 26) ways += dfs(s, idx + 2);\n        }\n        return ways;\n    }\n}",
                "python": "class Solution:\n    def numDecodings(self, s: str) -> int:\n        def dfs(i):\n            if i == len(s): return 1\n            if s[i] == '0': return 0\n            ways = dfs(i + 1)\n            if i + 1 < len(s) and 10 <= int(s[i:i+2]) <= 26:\n                ways += dfs(i + 2)\n            return ways\n        return dfs(0)"
            }
        },
        "optimal": {
            "idea": "O(1) space DP: prev1 = ways to decode up to i-1, prev2 = ways to decode up to i-2. Check 1-digit and 2-digit validity.",
            "steps": [
                "If s[0] == '0' return 0.",
                "prev2 = 1, prev1 = 1.",
                "For i = 1..n-1: cur = 0.",
                "If s[i] != '0' cur += prev1.",
                "int twoDigit = Integer.parseInt(s.substring(i - 1, i + 1)); if 10 <= twoDigit <= 26 cur += prev2.",
                "prev2 = prev1; prev1 = cur.",
                "Return prev1."
            ],
            "time": "O(n)",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public int numDecodings(String s) {\n        if (s == null || s.length() == 0 || s.charAt(0) == '0') return 0;\n        int n = s.length();\n        int prev2 = 1, prev1 = 1;\n        for (int i = 1; i < n; i++) {\n            int cur = 0;\n            if (s.charAt(i) != '0') {\n                cur += prev1;\n            }\n            int twoDigit = (s.charAt(i - 1) - '0') * 10 + (s.charAt(i) - '0');\n            if (twoDigit >= 10 && twoDigit <= 26) {\n                cur += prev2;\n            }\n            prev2 = prev1;\n            prev1 = cur;\n        }\n        return prev1;\n    }\n}",
                "python": "class Solution:\n    def numDecodings(self, s: str) -> int:\n        if not s or s[0] == '0':\n            return 0\n        prev2, prev1 = 1, 1\n        for i in range(1, len(s)):\n            cur = 0\n            if s[i] != '0':\n                cur += prev1\n            two_digit = int(s[i-1:i+1])\n            if 10 <= two_digit <= 26:\n                cur += prev2\n            prev2, prev1 = prev1, cur\n        return prev1"
            }
        }
    },
    {
        "seq": 242,
        "whyNext": "Unbounded knapsack minimization: dp[a] = min(dp[a], 1 + dp[a - coin]) for each coin in coins.",
        "brute": {
            "idea": "Recursively try subtracting every coin from remaining amount, tracking minimum depth.",
            "steps": [
                "dfs(rem): 1 + min(dfs(rem - coin))."
            ],
            "time": "O(S^n)",
            "space": "O(amount)",
            "whySlow": "Exponential recursion.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int coinChange(int[] coins, int amount) {\n        int[] dp = new int[amount + 1];\n        Arrays.fill(dp, amount + 1);\n        dp[0] = 0;\n        for (int i = 1; i <= amount; i++) {\n            for (int c : coins) {\n                if (i >= c) dp[i] = Math.min(dp[i], dp[i - c] + 1);\n            }\n        }\n        return dp[amount] > amount ? -1 : dp[amount];\n    }\n}",
                "python": "class Solution:\n    def coinChange(self, coins: list[int], amount: int) -> int:\n        dp = [amount + 1] * (amount + 1)\n        dp[0] = 0\n        for i in range(1, amount + 1):\n            for c in coins:\n                if i >= c:\n                    dp[i] = min(dp[i], dp[i - c] + 1)\n        return dp[amount] if dp[amount] <= amount else -1"
            }
        },
        "optimal": {
            "idea": "Bottom-up 1D DP: dp[a] = min coins to make amount a. Initialize with amount + 1; dp[0] = 0.",
            "steps": [
                "int[] dp = new int[amount + 1]; Arrays.fill(dp, amount + 1); dp[0] = 0.",
                "For i = 1..amount: for coin in coins: if i >= coin dp[i] = min(dp[i], dp[i - coin] + 1).",
                "Return dp[amount] > amount ? -1 : dp[amount]."
            ],
            "time": "O(amount * n)",
            "space": "O(amount)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int coinChange(int[] coins, int amount) {\n        int[] dp = new int[amount + 1];\n        Arrays.fill(dp, amount + 1);\n        dp[0] = 0;\n        for (int i = 1; i <= amount; i++) {\n            for (int coin : coins) {\n                if (i >= coin) {\n                    dp[i] = Math.min(dp[i], dp[i - coin] + 1);\n                }\n            }\n        }\n        return dp[amount] > amount ? -1 : dp[amount];\n    }\n}",
                "python": "class Solution:\n    def coinChange(self, coins: list[int], amount: int) -> int:\n        dp = [amount + 1] * (amount + 1)\n        dp[0] = 0\n        for i in range(1, amount + 1):\n            for coin in coins:\n                if i >= coin:\n                    dp[i] = min(dp[i], dp[i - coin] + 1)\n        return dp[amount] if dp[amount] <= amount else -1"
            }
        }
    },
    {
        "seq": 243,
        "whyNext": "Unbounded knapsack combinations: loop over coins in outer loop to prevent counting permutations.",
        "brute": {
            "idea": "Recursive backtracking: explore combinations of coins summing to amount.",
            "steps": [
                "dfs(coinIdx, rem): try taking coin or skipping to next coin."
            ],
            "time": "O(2^(amount / minCoin))",
            "space": "O(amount)",
            "whySlow": "Exponential recursion.",
            "code": {
                "java": "class Solution {\n    public int change(int amount, int[] coins) {\n        int[] dp = new int[amount + 1];\n        dp[0] = 1;\n        for (int c : coins) {\n            for (int i = c; i <= amount; i++) {\n                dp[i] += dp[i - c];\n            }\n        }\n        return dp[amount];\n    }\n}",
                "python": "class Solution:\n    def change(self, amount: int, coins: list[int]) -> int:\n        dp = [0] * (amount + 1)\n        dp[0] = 1\n        for c in coins:\n            for i in range(c, amount + 1):\n                dp[i] += dp[i - c]\n        return dp[amount]"
            }
        },
        "optimal": {
            "idea": "1D DP with coins in outer loop: dp[i] += dp[i - coin] ensures each coin is processed in order, generating combinations only.",
            "steps": [
                "int[] dp = new int[amount + 1]; dp[0] = 1.",
                "For coin in coins: for i from coin to amount: dp[i] += dp[i - coin].",
                "Return dp[amount]."
            ],
            "time": "O(amount * n)",
            "space": "O(amount)",
            "code": {
                "java": "class Solution {\n    public int change(int amount, int[] coins) {\n        int[] dp = new int[amount + 1];\n        dp[0] = 1;\n        for (int coin : coins) {\n            for (int i = coin; i <= amount; i++) {\n                dp[i] += dp[i - coin];\n            }\n        }\n        return dp[amount];\n    }\n}",
                "python": "class Solution:\n    def change(self, amount: int, coins: list[int]) -> int:\n        dp = [0] * (amount + 1)\n        dp[0] = 1\n        for coin in coins:\n            for i in range(coin, amount + 1):\n                dp[i] += dp[i - coin]\n        return dp[amount]"
            }
        }
    },
    {
        "seq": 244,
        "whyNext": "Unbounded knapsack permutations: target in outer loop and numbers in inner loop counts ordered arrangements (1+2 != 2+1).",
        "brute": {
            "idea": "Backtracking / recursion: at current target sum, try adding each num in nums.",
            "steps": [
                "dfs(rem): sum of dfs(rem - num) for num in nums."
            ],
            "time": "O(N^target)",
            "space": "O(target)",
            "whySlow": "Exponential recursion.",
            "code": {
                "java": "class Solution {\n    public int combinationSum4(int[] nums, int target) {\n        int[] dp = new int[target + 1];\n        dp[0] = 1;\n        for (int i = 1; i <= target; i++) {\n            for (int num : nums) {\n                if (i >= num) dp[i] += dp[i - num];\n            }\n        }\n        return dp[target];\n    }\n}",
                "python": "class Solution:\n    def combinationSum4(self, nums: list[int], target: int) -> int:\n        dp = [0] * (target + 1)\n        dp[0] = 1\n        for i in range(1, target + 1):\n            for num in nums:\n                if i >= num: dp[i] += dp[i - num]\n        return dp[target]"
            }
        },
        "optimal": {
            "idea": "Target outer loop: dp[i] = sum of dp[i - num] for all num <= i. Counts distinct permutation orders.",
            "steps": [
                "int[] dp = new int[target + 1]; dp[0] = 1.",
                "For i = 1..target: for num in nums: if (i >= num) dp[i] += dp[i - num].",
                "Return dp[target]."
            ],
            "time": "O(target * n)",
            "space": "O(target)",
            "code": {
                "java": "class Solution {\n    public int combinationSum4(int[] nums, int target) {\n        int[] dp = new int[target + 1];\n        dp[0] = 1;\n        for (int i = 1; i <= target; i++) {\n            for (int num : nums) {\n                if (i >= num) {\n                    dp[i] += dp[i - num];\n                }\n            }\n        }\n        return dp[target];\n    }\n}",
                "python": "class Solution:\n    def combinationSum4(self, nums: list[int], target: int) -> int:\n        dp = [0] * (target + 1)\n        dp[0] = 1\n        for i in range(1, target + 1):\n            for num in nums:\n                if i >= num:\n                    dp[i] += dp[i - num]\n        return dp[target]"
            }
        }
    },
    {
        "seq": 245,
        "whyNext": "Unbounded knapsack on square numbers: dp[i] = 1 + min(dp[i - j*j]) for j*j <= i.",
        "brute": {
            "idea": "Recursively try subtracting every perfect square j*j <= n, keeping minimum depth.",
            "steps": [
                "dfs(rem): 1 + min(dfs(rem - j*j))."
            ],
            "time": "O(sqrt(n)^n)",
            "space": "O(n)",
            "whySlow": "Exponential recursion.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int numSquares(int n) {\n        int[] dp = new int[n + 1];\n        Arrays.fill(dp, n);\n        dp[0] = 0;\n        for (int i = 1; i <= n; i++) {\n            for (int j = 1; j * j <= i; j++) {\n                dp[i] = Math.min(dp[i], dp[i - j * j] + 1);\n            }\n        }\n        return dp[n];\n    }\n}",
                "python": "class Solution:\n    def numSquares(self, n: int) -> int:\n        dp = [n] * (n + 1)\n        dp[0] = 0\n        for i in range(1, n + 1):\n            j = 1\n            while j * j <= i:\n                dp[i] = min(dp[i], dp[i - j * j] + 1)\n                j += 1\n        return dp[n]"
            }
        },
        "optimal": {
            "idea": "Bottom-up 1D DP: dp[i] = min(dp[i], dp[i - j*j] + 1) for j*j <= i.",
            "steps": [
                "int[] dp = new int[n + 1]; Arrays.fill(dp, Integer.MAX_VALUE); dp[0] = 0.",
                "For i = 1..n: for j = 1; j*j <= i; j++: dp[i] = Math.min(dp[i], dp[i - j*j] + 1).",
                "Return dp[n]."
            ],
            "time": "O(n * sqrt(n))",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int numSquares(int n) {\n        int[] dp = new int[n + 1];\n        Arrays.fill(dp, Integer.MAX_VALUE);\n        dp[0] = 0;\n        for (int i = 1; i <= n; i++) {\n            for (int j = 1; j * j <= i; j++) {\n                dp[i] = Math.min(dp[i], dp[i - j * j] + 1);\n            }\n        }\n        return dp[n];\n    }\n}",
                "python": "class Solution:\n    def numSquares(self, n: int) -> int:\n        dp = [float('inf')] * (n + 1)\n        dp[0] = 0\n        for i in range(1, n + 1):\n            j = 1\n            while j * j <= i:\n                dp[i] = min(dp[i], dp[i - j * j] + 1)\n                j += 1\n        return dp[n]"
            }
        }
    },
    {
        "seq": 246,
        "whyNext": "Boolean prefix DP: dp[i] = true if any j < i has dp[j] == true and s[j..i] in wordDict.",
        "brute": {
            "idea": "Recursively check if any word in wordDict matches the prefix; recurse on suffix.",
            "steps": [
                "dfs(start): try all words matching prefix s[start..start+len].",
                "Recurse on remaining substring."
            ],
            "time": "O(2^n)",
            "space": "O(n)",
            "whySlow": "Exponential recursion.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public boolean wordBreak(String s, List<String> wordDict) {\n        Set<String> set = new HashSet<>(wordDict);\n        boolean[] dp = new boolean[s.length() + 1];\n        dp[0] = true;\n        for (int i = 1; i <= s.length(); i++) {\n            for (int j = 0; j < i; j++) {\n                if (dp[j] && set.contains(s.substring(j, i))) {\n                    dp[i] = true;\n                    break;\n                }\n            }\n        }\n        return dp[s.length()];\n    }\n}",
                "python": "class Solution:\n    def wordBreak(self, s: str, wordDict: list[str]) -> bool:\n        words = set(wordDict)\n        dp = [False] * (len(s) + 1)\n        dp[0] = True\n        for i in range(1, len(s) + 1):\n            for j in range(i):\n                if dp[j] and s[j:i] in words:\n                    dp[i] = True\n                    break\n        return dp[len(s)]"
            }
        },
        "optimal": {
            "idea": "Boolean 1D DP: dp[i] is true if prefix of length i can be segmented into dictionary words; check j < i with dp[j] == true.",
            "steps": [
                "Set<String> set = new HashSet<>(wordDict);",
                "boolean[] dp = new boolean[n + 1]; dp[0] = true.",
                "For i = 1..n: for j = 0..i-1: if dp[j] && set.contains(s.substring(j, i)) { dp[i] = true; break; }",
                "Return dp[n]."
            ],
            "time": "O(n^2)",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public boolean wordBreak(String s, List<String> wordDict) {\n        Set<String> set = new HashSet<>(wordDict);\n        int n = s.length();\n        boolean[] dp = new boolean[n + 1];\n        dp[0] = true;\n        for (int i = 1; i <= n; i++) {\n            for (int j = 0; j < i; j++) {\n                if (dp[j] && set.contains(s.substring(j, i))) {\n                    dp[i] = true;\n                    break;\n                }\n            }\n        }\n        return dp[n];\n    }\n}",
                "python": "class Solution:\n    def wordBreak(self, s: str, wordDict: list[str]) -> bool:\n        words = set(wordDict)\n        n = len(s)\n        dp = [False] * (n + 1)\n        dp[0] = True\n        for i in range(1, n + 1):\n            for j in range(i):\n                if dp[j] and s[j:i] in words:\n                    dp[i] = True\n                    break\n        return dp[n]"
            }
        }
    },
    {
        "seq": 247,
        "whyNext": "Patience Sorting / Binary Search: maintain tails array where tails[len] is smallest tail of LIS of length len; binary search updates in O(n log n).",
        "brute": {
            "idea": "O(n^2) DP: dp[i] = 1 + max(dp[j]) for all j < i where nums[j] < nums[i].",
            "steps": [
                "Initialize dp array of 1s.",
                "Nested loop for each i and j < i.",
                "Return max(dp)."
            ],
            "time": "O(n^2)",
            "space": "O(n)",
            "whySlow": "Linear scan for previous smaller elements.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int lengthOfLIS(int[] nums) {\n        int n = nums.length;\n        int[] dp = new int[n];\n        Arrays.fill(dp, 1);\n        int max = 1;\n        for (int i = 1; i < n; i++) {\n            for (int j = 0; j < i; j++) {\n                if (nums[j] < nums[i]) {\n                    dp[i] = Math.max(dp[i], dp[j] + 1);\n                }\n            }\n            max = Math.max(max, dp[i]);\n        }\n        return max;\n    }\n}",
                "python": "class Solution:\n    def lengthOfLIS(self, nums: list[int]) -> int:\n        dp = [1] * len(nums)\n        for i in range(len(nums)):\n            for j in range(i):\n                if nums[j] < nums[i]:\n                    dp[i] = max(dp[i], dp[j] + 1)\n        return max(dp)"
            }
        },
        "optimal": {
            "idea": "Patience sorting with binary search: maintain tails array; for each x, binary search first tail >= x. If not found, append; else replace.",
            "steps": [
                "int[] tails = new int[nums.length]; int size = 0.",
                "For x in nums: binary search index i in tails[0..size-1].",
                "If i < 0 i = -(i + 1); tails[i] = x.",
                "If i == size size++.",
                "Return size."
            ],
            "time": "O(n log n)",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int lengthOfLIS(int[] nums) {\n        int[] tails = new int[nums.length];\n        int size = 0;\n        for (int x : nums) {\n            int l = 0, r = size;\n            while (l < r) {\n                int m = l + (r - l) / 2;\n                if (tails[m] < x) l = m + 1;\n                else r = m;\n            }\n            tails[l] = x;\n            if (l == size) size++;\n        }\n        return size;\n    }\n}",
                "python": "import bisect\n\nclass Solution:\n    def lengthOfLIS(self, nums: list[int]) -> int:\n        tails = []\n        for x in nums:\n            idx = bisect.bisect_left(tails, x)\n            if idx == len(tails):\n                tails.append(x)\n            else:\n                tails[idx] = x\n        return len(tails)"
            }
        }
    },
    {
        "seq": 248,
        "whyNext": "Builds on LIS: simultaneously track length len[i] and count count[i] of LIS ending at index i.",
        "brute": {
            "idea": "Generate all subsequences, filter those that are strictly increasing and of maximum length, and count them.",
            "steps": [
                "Generate all 2^n subsequences.",
                "Track maximum length and count."
            ],
            "time": "O(2^n * n)",
            "space": "O(n)",
            "whySlow": "Exponential enumeration.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int findNumberOfLIS(int[] nums) {\n        int n = nums.length;\n        int[] len = new int[n];\n        int[] count = new int[n];\n        Arrays.fill(len, 1);\n        Arrays.fill(count, 1);\n        int maxLen = 1;\n        for (int i = 0; i < n; i++) {\n            for (int j = 0; j < i; j++) {\n                if (nums[j] < nums[i]) {\n                    if (len[j] + 1 > len[i]) {\n                        len[i] = len[j] + 1;\n                        count[i] = count[j];\n                    } else if (len[j] + 1 == len[i]) {\n                        count[i] += count[j];\n                    }\n                }\n            }\n            maxLen = Math.max(maxLen, len[i]);\n        }\n        int total = 0;\n        for (int i = 0; i < n; i++) {\n            if (len[i] == maxLen) total += count[i];\n        }\n        return total;\n    }\n}",
                "python": "class Solution:\n    def findNumberOfLIS(self, nums: list[int]) -> int:\n        n = len(nums)\n        length = [1] * n\n        count = [1] * n\n        for i in range(n):\n            for j in range(i):\n                if nums[j] < nums[i]:\n                    if length[j] + 1 > length[i]:\n                        length[i] = length[j] + 1\n                        count[i] = count[j]\n                    elif length[j] + 1 == length[i]:\n                        count[i] += count[j]\n        max_l = max(length)\n        return sum(c for l, c in zip(length, count) if l == max_l)"
            }
        },
        "optimal": {
            "idea": "Two 1D DP arrays: len[i] and count[i]. If len[j] + 1 > len[i]: len[i] = len[j] + 1, count[i] = count[j]; else if equal: count[i] += count[j].",
            "steps": [
                "int[] len = new int[n], count = new int[n]; Arrays.fill to 1.",
                "For i = 0..n-1: for j = 0..i-1: if nums[j] < nums[i]:",
                "If len[j] + 1 > len[i] { len[i] = len[j] + 1; count[i] = count[j]; }",
                "Else if len[j] + 1 == len[i] count[i] += count[j].",
                "maxLen = max(len); return sum of count[i] for all i where len[i] == maxLen."
            ],
            "time": "O(n^2)",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int findNumberOfLIS(int[] nums) {\n        int n = nums.length;\n        int[] len = new int[n];\n        int[] count = new int[n];\n        Arrays.fill(len, 1);\n        Arrays.fill(count, 1);\n        int maxLen = 1;\n        for (int i = 0; i < n; i++) {\n            for (int j = 0; j < i; j++) {\n                if (nums[j] < nums[i]) {\n                    if (len[j] + 1 > len[i]) {\n                        len[i] = len[j] + 1;\n                        count[i] = count[j];\n                    } else if (len[j] + 1 == len[i]) {\n                        count[i] += count[j];\n                    }\n                }\n            }\n            maxLen = Math.max(maxLen, len[i]);\n        }\n        int total = 0;\n        for (int i = 0; i < n; i++) {\n            if (len[i] == maxLen) total += count[i];\n        }\n        return total;\n    }\n}",
                "python": "class Solution:\n    def findNumberOfLIS(self, nums: list[int]) -> int:\n        n = len(nums)\n        length = [1] * n\n        count = [1] * n\n        for i in range(n):\n            for j in range(i):\n                if nums[j] < nums[i]:\n                    if length[j] + 1 > length[i]:\n                        length[i] = length[j] + 1\n                        count[i] = count[j]\n                    elif length[j] + 1 == length[i]:\n                        count[i] += count[j]\n        max_len = max(length)\n        return sum(c for l, c in zip(length, count) if l == max_len)"
            }
        }
    },
    {
        "seq": 249,
        "whyNext": "2D LIS reduction: sort width ascending, height descending; LIS on heights automatically guarantees valid Russian doll nesting.",
        "brute": {
            "idea": "Sort envelopes; run O(n^2) LIS checking w[j] < w[i] && h[j] < h[i].",
            "steps": [
                "Sort envelopes by width.",
                "Compute dp[i] = 1 + max(dp[j]) where both dimensions are strictly smaller."
            ],
            "time": "O(n^2)",
            "space": "O(n)",
            "whySlow": "Quadratic dynamic programming gets TLE for n = 100,000.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int maxEnvelopes(int[][] envelopes) {\n        Arrays.sort(envelopes, (a, b) -> a[0] != b[0] ? a[0] - b[0] : b[1] - a[1]);\n        int[] dp = new int[envelopes.length];\n        int size = 0;\n        for (int[] env : envelopes) {\n            int h = env[1];\n            int l = 0, r = size;\n            while (l < r) {\n                int m = l + (r - l) / 2;\n                if (dp[m] < h) l = m + 1;\n                else r = m;\n            }\n            dp[l] = h;\n            if (l == size) size++;\n        }\n        return size;\n    }\n}",
                "python": "import bisect\n\nclass Solution:\n    def maxEnvelopes(self, envelopes: list[list[int]]) -> int:\n        envelopes.sort(key=lambda x: (x[0], -x[1]))\n        tails = []\n        for _, h in envelopes:\n            idx = bisect.bisect_left(tails, h)\n            if idx == len(tails):\n                tails.append(h)\n            else:\n                tails[idx] = h\n        return len(tails)"
            }
        },
        "optimal": {
            "idea": "Sort by width ascending, height descending (w asc, h desc). Height descending prevents picking envelopes with identical width; run O(n log n) LIS on heights.",
            "steps": [
                "Arrays.sort(envelopes, (a, b) -> a[0] != b[0] ? a[0] - b[0] : b[1] - a[1]).",
                "int[] dp = new int[n]; size = 0.",
                "For [w, h] in envelopes: binary search position of h in dp[0..size-1].",
                "dp[idx] = h; if idx == size size++.",
                "Return size."
            ],
            "time": "O(n log n)",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int maxEnvelopes(int[][] envelopes) {\n        Arrays.sort(envelopes, (a, b) -> a[0] != b[0] ? a[0] - b[0] : b[1] - a[1]);\n        int[] dp = new int[envelopes.length];\n        int size = 0;\n        for (int[] env : envelopes) {\n            int h = env[1];\n            int l = 0, r = size;\n            while (l < r) {\n                int m = l + (r - l) / 2;\n                if (dp[m] < h) l = m + 1;\n                else r = m;\n            }\n            dp[l] = h;\n            if (l == size) size++;\n        }\n        return size;\n    }\n}",
                "python": "import bisect\n\nclass Solution:\n    def maxEnvelopes(self, envelopes: list[list[int]]) -> int:\n        envelopes.sort(key=lambda x: (x[0], -x[1]))\n        tails = []\n        for _, h in envelopes:\n            idx = bisect.bisect_left(tails, h)\n            if idx == len(tails):\n                tails.append(h)\n            else:\n                tails[idx] = h\n        return len(tails)"
            }
        }
    },
    {
        "seq": 250,
        "whyNext": "Double state tracking: multiplying by a negative flips min and max; track curMax and curMin at each step in O(1) space.",
        "brute": {
            "idea": "Test all O(n^2) subarrays by fixing start index and computing product to end.",
            "steps": [
                "Nested loops computing subarray products.",
                "Track maximum product."
            ],
            "time": "O(n^2)",
            "space": "O(1)",
            "whySlow": "Examines all quadratic subarray products.",
            "code": {
                "java": "class Solution {\n    public int maxProduct(int[] nums) {\n        int max = nums[0];\n        for (int i = 0; i < nums.length; i++) {\n            int prod = 1;\n            for (int j = i; j < nums.length; j++) {\n                prod *= nums[j];\n                max = Math.max(max, prod);\n            }\n        }\n        return max;\n    }\n}",
                "python": "class Solution:\n    def maxProduct(self, nums: list[int]) -> int:\n        ans = nums[0]\n        for i in range(len(nums)):\n            prod = 1\n            for j in range(i, len(nums)):\n                prod *= nums[j]\n                ans = max(ans, prod)\n        return ans"
            }
        },
        "optimal": {
            "idea": "Kadane with min and max: if num < 0, swap curMax and curMin. curMax = max(num, curMax * num), curMin = min(num, curMin * num).",
            "steps": [
                "curMax = nums[0], curMin = nums[0], ans = nums[0].",
                "For i = 1..n-1: num = nums[i].",
                "If num < 0 swap(curMax, curMin).",
                "curMax = max(num, curMax * num); curMin = min(num, curMin * num).",
                "ans = max(ans, curMax).",
                "Return ans."
            ],
            "time": "O(n)",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public int maxProduct(int[] nums) {\n        int curMax = nums[0], curMin = nums[0], ans = nums[0];\n        for (int i = 1; i < nums.length; i++) {\n            int num = nums[i];\n            if (num < 0) {\n                int temp = curMax;\n                curMax = curMin;\n                curMin = temp;\n            }\n            curMax = Math.max(num, curMax * num);\n            curMin = Math.min(num, curMin * num);\n            ans = Math.max(ans, curMax);\n        }\n        return ans;\n    }\n}",
                "python": "class Solution:\n    def maxProduct(self, nums: list[int]) -> int:\n        cur_max = cur_min = ans = nums[0]\n        for num in nums[1:]:\n            if num < 0:\n                cur_max, cur_min = cur_min, cur_max\n            cur_max = max(num, cur_max * num)\n            cur_min = min(num, cur_min * num)\n            ans = max(ans, cur_max)\n        return ans"
            }
        }
    }
]

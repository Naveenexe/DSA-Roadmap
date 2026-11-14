# scripts/gen_batch_10.py
import json

batch_10 = [
    # 226: Most Stones Removed with Same Row or Column
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
                "java": """import java.util.*;
class Solution {
    public int removeStones(int[][] stones) {
        int n = stones.length;
        List<Integer>[] adj = new List[n];
        for (int i = 0; i < n; i++) adj[i] = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (stones[i][0] == stones[j][0] || stones[i][1] == stones[j][1]) {
                    adj[i].add(j);
                    adj[j].add(i);
                }
            }
        }
        boolean[] visited = new boolean[n];
        int components = 0;
        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                components++;
                dfs(adj, i, visited);
            }
        }
        return n - components;
    }
    private void dfs(List<Integer>[] adj, int u, boolean[] visited) {
        visited[u] = true;
        for (int v : adj[u]) {
            if (!visited[v]) dfs(adj, v, visited);
        }
    }
}""",
                "python": """from collections import defaultdict

class Solution:
    def removeStones(self, stones: list[list[int]]) -> int:
        n = len(stones)
        adj = defaultdict(list)
        for i in range(n):
            for j in range(i + 1, n):
                if stones[i][0] == stones[j][0] or stones[i][1] == stones[j][1]:
                    adj[i].append(j)
                    adj[j].append(i)
        visited = set()
        comp = 0
        def dfs(u):
            visited.add(u)
            for v in adj[u]:
                if v not in visited: dfs(v)
        for i in range(n):
            if i not in visited:
                comp += 1
                dfs(i)
        return n - comp"""
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
                "java": """import java.util.*;
class Solution {
    private Map<Integer, Integer> parent = new HashMap<>();
    private int count = 0;
    public int removeStones(int[][] stones) {
        for (int[] s : stones) {
            union(s[0], ~s[1]);
        }
        return stones.length - count;
    }
    private int find(int x) {
        if (!parent.containsKey(x)) {
            parent.put(x, x);
            count++;
        }
        if (x != parent.get(x)) {
            parent.put(x, find(parent.get(x)));
        }
        return parent.get(x);
    }
    private void union(int x, int y) {
        int rx = find(x), ry = find(y);
        if (rx != ry) {
            parent.put(rx, ry);
            count--;
        }
    }
}""",
                "python": """class Solution:
    def removeStones(self, stones: list[list[int]]) -> int:
        parent = {}
        count = 0
        def find(x):
            nonlocal count
            if x not in parent:
                parent[x] = x
                count += 1
            if x != parent[x]:
                parent[x] = find(parent[x])
            return parent[x]
        def union(x, y):
            nonlocal count
            rx, ry = find(x), find(y)
            if rx != ry:
                parent[rx] = ry
                count -= 1
        for x, y in stones:
            union(x, ~y)
        return len(stones) - count"""
            }
        }
    },
    # 227: Network Delay Time
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
                "java": """import java.util.*;
class Solution {
    public int networkDelayTime(int[][] times, int n, int k) {
        int[] dist = new int[n + 1];
        Arrays.fill(dist, 1000000);
        dist[k] = 0;
        for (int i = 1; i < n; i++) {
            for (int[] e : times) {
                int u = e[0], v = e[1], w = e[2];
                if (dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                }
            }
        }
        int max = 0;
        for (int i = 1; i <= n; i++) max = Math.max(max, dist[i]);
        return max >= 1000000 ? -1 : max;
    }
}""",
                "python": """class Solution:
    def networkDelayTime(self, times: list[list[int]], n: int, k: int) -> int:
        dist = [float('inf')] * (n + 1)
        dist[k] = 0
        for _ in range(n - 1):
            for u, v, w in times:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
        ans = max(dist[1:])
        return ans if ans < float('inf') else -1"""
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
                "java": """import java.util.*;
class Solution {
    public int networkDelayTime(int[][] times, int n, int k) {
        List<int[]>[] adj = new List[n + 1];
        for (int i = 1; i <= n; i++) adj[i] = new ArrayList<>();
        for (int[] t : times) {
            adj[t[0]].add(new int[]{t[1], t[2]});
        }
        int[] dist = new int[n + 1];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[k] = 0;
        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[0]));
        pq.offer(new int[]{0, k});
        while (!pq.isEmpty()) {
            int[] cur = pq.poll();
            int d = cur[0], u = cur[1];
            if (d > dist[u]) continue;
            for (int[] edge : adj[u]) {
                int v = edge[0], w = edge[1];
                if (d + w < dist[v]) {
                    dist[v] = d + w;
                    pq.offer(new int[]{dist[v], v});
                }
            }
        }
        int max = 0;
        for (int i = 1; i <= n; i++) {
            if (dist[i] == Integer.MAX_VALUE) return -1;
            max = Math.max(max, dist[i]);
        }
        return max;
    }
}""",
                "python": """import heapq
from collections import defaultdict

class Solution:
    def networkDelayTime(self, times: list[list[int]], n: int, k: int) -> int:
        adj = defaultdict(list)
        for u, v, w in times:
            adj[u].append((v, w))
        dist = [float('inf')] * (n + 1)
        dist[k] = 0
        pq = [(0, k)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v, w in adj[u]:
                if d + w < dist[v]:
                    dist[v] = d + w
                    heapq.heappush(pq, (dist[v], v))
        ans = max(dist[1:])
        return ans if ans < float('inf') else -1"""
            }
        }
    },
    # 228: Cheapest Flights Within K Stops
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
                "java": """import java.util.*;
class Solution {
    public int findCheapestPrice(int n, int[][] flights, int src, int dst, int k) {
        int[] dist = new int[n];
        Arrays.fill(dist, 100000000);
        dist[src] = 0;
        for (int i = 0; i <= k; i++) {
            int[] temp = Arrays.copyOf(dist, n);
            for (int[] f : flights) {
                int u = f[0], v = f[1], w = f[2];
                if (dist[u] + w < temp[v]) {
                    temp[v] = dist[u] + w;
                }
            }
            dist = temp;
        }
        return dist[dst] >= 100000000 ? -1 : dist[dst];
    }
}""",
                "python": """class Solution:
    def findCheapestPrice(self, n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
        dist = [float('inf')] * n
        dist[src] = 0
        for _ in range(k + 1):
            temp = list(dist)
            for u, v, w in flights:
                if dist[u] + w < temp[v]:
                    temp[v] = dist[u] + w
            dist = temp
        return dist[dst] if dist[dst] < float('inf') else -1"""
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
                "java": """import java.util.*;
class Solution {
    public int findCheapestPrice(int n, int[][] flights, int src, int dst, int k) {
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[src] = 0;
        for (int i = 0; i <= k; i++) {
            int[] temp = Arrays.copyOf(dist, n);
            for (int[] f : flights) {
                int u = f[0], v = f[1], price = f[2];
                if (dist[u] != Integer.MAX_VALUE && dist[u] + price < temp[v]) {
                    temp[v] = dist[u] + price;
                }
            }
            dist = temp;
        }
        return dist[dst] == Integer.MAX_VALUE ? -1 : dist[dst];
    }
}""",
                "python": """class Solution:
    def findCheapestPrice(self, n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
        dist = [float('inf')] * n
        dist[src] = 0
        for _ in range(k + 1):
            temp = list(dist)
            for u, v, price in flights:
                if dist[u] != float('inf') and dist[u] + price < temp[v]:
                    temp[v] = dist[u] + price
            dist = temp
        return dist[dst] if dist[dst] != float('inf') else -1"""
            }
        }
    },
    # 229: Path With Minimum Effort
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
                "java": """import java.util.*;
class Solution {
    public int minimumEffortPath(int[][] heights) {
        int m = heights.length, n = heights[0].length;
        int low = 0, high = 1000000;
        while (low < high) {
            int mid = low + (high - low) / 2;
            if (canReach(heights, mid, m, n)) {
                high = mid;
            } else {
                low = mid + 1;
            }
        }
        return low;
    }
    private boolean canReach(int[][] h, int maxEffort, int m, int n) {
        boolean[][] visited = new boolean[m][n];
        Queue<int[]> q = new LinkedList<>();
        q.offer(new int[]{0, 0});
        visited[0][0] = true;
        int[][] dirs = {{1,0}, {-1,0}, {0,1}, {0,-1}};
        while (!q.isEmpty()) {
            int[] cur = q.poll();
            if (cur[0] == m - 1 && cur[1] == n - 1) return true;
            for (int[] d : dirs) {
                int nr = cur[0] + d[0], nc = cur[1] + d[1];
                if (nr >= 0 && nr < m && nc >= 0 && nc < n && !visited[nr][nc]) {
                    if (Math.abs(h[nr][nc] - h[cur[0]][cur[1]]) <= maxEffort) {
                        visited[nr][nc] = true;
                        q.offer(new int[]{nr, nc});
                    }
                }
            }
        }
        return false;
    }
}""",
                "python": """from collections import deque

class Solution:
    def minimumEffortPath(self, heights: list[list[int]]) -> int:
        m, n = len(heights), len(heights[0])
        def check(mid):
            visited = [[False] * n for _ in range(m)]
            q = deque([(0, 0)])
            visited[0][0] = True
            while q:
                r, c = q.popleft()
                if r == m - 1 and c == n - 1: return True
                for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and not visited[nr][nc]:
                        if abs(heights[nr][nc] - heights[r][c]) <= mid:
                            visited[nr][nc] = True
                            q.append((nr, nc))
            return False
        low, high = 0, 1000000
        while low < high:
            mid = (low + high) // 2
            if check(mid): high = mid
            else: low = mid + 1
        return low"""
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
                "java": """import java.util.*;
class Solution {
    public int minimumEffortPath(int[][] heights) {
        int m = heights.length, n = heights[0].length;
        int[][] dist = new int[m][n];
        for (int[] row : dist) Arrays.fill(row, Integer.MAX_VALUE);
        dist[0][0] = 0;
        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[0]));
        pq.offer(new int[]{0, 0, 0});
        int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        while (!pq.isEmpty()) {
            int[] cur = pq.poll();
            int effort = cur[0], r = cur[1], c = cur[2];
            if (r == m - 1 && c == n - 1) return effort;
            if (effort > dist[r][c]) continue;
            for (int[] d : dirs) {
                int nr = r + d[0], nc = c + d[1];
                if (nr >= 0 && nr < m && nc >= 0 && nc < n) {
                    int nextEffort = Math.max(effort, Math.abs(heights[nr][nc] - heights[r][c]));
                    if (nextEffort < dist[nr][nc]) {
                        dist[nr][nc] = nextEffort;
                        pq.offer(new int[]{nextEffort, nr, nc});
                    }
                }
            }
        }
        return 0;
    }
}""",
                "python": """import heapq

class Solution:
    def minimumEffortPath(self, heights: list[list[int]]) -> int:
        m, n = len(heights), len(heights[0])
        dist = [[float('inf')] * n for _ in range(m)]
        dist[0][0] = 0
        pq = [(0, 0, 0)]
        while pq:
            effort, r, c = heapq.heappop(pq)
            if r == m - 1 and c == n - 1:
                return effort
            if effort > dist[r][c]:
                continue
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n:
                    nxt_eff = max(effort, abs(heights[nr][nc] - heights[r][c]))
                    if nxt_eff < dist[nr][nc]:
                        dist[nr][nc] = nxt_eff
                        heapq.heappush(pq, (nxt_eff, nr, nc))
        return 0"""
            }
        }
    },
    # 230: Swim in Rising Water
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
                "java": """import java.util.*;
class Solution {
    public int swimInWater(int[][] grid) {
        int n = grid.length;
        int low = Math.max(grid[0][0], grid[n - 1][n - 1]), high = n * n - 1;
        while (low < high) {
            int mid = low + (high - low) / 2;
            if (canReach(grid, mid, n)) {
                high = mid;
            } else {
                low = mid + 1;
            }
        }
        return low;
    }
    private boolean canReach(int[][] g, int t, int n) {
        boolean[][] visited = new boolean[n][n];
        Queue<int[]> q = new LinkedList<>();
        q.offer(new int[]{0, 0});
        visited[0][0] = true;
        int[][] dirs = {{1,0}, {-1,0}, {0,1}, {0,-1}};
        while (!q.isEmpty()) {
            int[] cur = q.poll();
            if (cur[0] == n - 1 && cur[1] == n - 1) return true;
            for (int[] d : dirs) {
                int nr = cur[0] + d[0], nc = cur[1] + d[1];
                if (nr >= 0 && nr < n && nc >= 0 && nc < n && !visited[nr][nc] && g[nr][nc] <= t) {
                    visited[nr][nc] = true;
                    q.offer(new int[]{nr, nc});
                }
            }
        }
        return false;
    }
}""",
                "python": """from collections import deque

class Solution:
    def swimInWater(self, grid: list[list[int]]) -> int:
        n = len(grid)
        def check(t):
            visited = [[False] * n for _ in range(n)]
            q = deque([(0, 0)])
            visited[0][0] = True
            while q:
                r, c = q.popleft()
                if r == n - 1 and c == n - 1: return True
                for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and grid[nr][nc] <= t:
                        visited[nr][nc] = True
                        q.append((nr, nc))
            return False
        low = max(grid[0][0], grid[n-1][n-1])
        high = n * n - 1
        while low < high:
            mid = (low + high) // 2
            if check(mid): high = mid
            else: low = mid + 1
        return low"""
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
                "java": """import java.util.*;
class Solution {
    public int swimInWater(int[][] grid) {
        int n = grid.length;
        boolean[][] visited = new boolean[n][n];
        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[0]));
        pq.offer(new int[]{grid[0][0], 0, 0});
        visited[0][0] = true;
        int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        while (!pq.isEmpty()) {
            int[] cur = pq.poll();
            int t = cur[0], r = cur[1], c = cur[2];
            if (r == n - 1 && c == n - 1) return t;
            for (int[] d : dirs) {
                int nr = r + d[0], nc = c + d[1];
                if (nr >= 0 && nr < n && nc >= 0 && nc < n && !visited[nr][nc]) {
                    visited[nr][nc] = true;
                    pq.offer(new int[]{Math.max(t, grid[nr][nc]), nr, nc});
                }
            }
        }
        return 0;
    }
}""",
                "python": """import heapq

class Solution:
    def swimInWater(self, grid: list[list[int]]) -> int:
        n = len(grid)
        visited = [[False] * n for _ in range(n)]
        pq = [(grid[0][0], 0, 0)]
        visited[0][0] = True
        while pq:
            t, r, c = heapq.heappop(pq)
            if r == n - 1 and c == n - 1:
                return t
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc]:
                    visited[nr][nc] = True
                    heapq.heappush(pq, (max(t, grid[nr][nc]), nr, nc))
        return 0"""
            }
        }
    },
    # 231: Path with Maximum Probability
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
                "java": """class Solution {
    public double maxProbability(int n, int[][] edges, double[] succProb, int start_node, int end_node) {
        double[] prob = new double[n];
        prob[start_node] = 1.0;
        for (int i = 0; i < n - 1; i++) {
            boolean updated = false;
            for (int j = 0; j < edges.length; j++) {
                int u = edges[j][0], v = edges[j][1];
                double p = succProb[j];
                if (prob[u] * p > prob[v]) {
                    prob[v] = prob[u] * p;
                    updated = true;
                }
                if (prob[v] * p > prob[u]) {
                    prob[u] = prob[v] * p;
                    updated = true;
                }
            }
            if (!updated) break;
        }
        return prob[end_node];
    }
}""",
                "python": """class Solution:
    def maxProbability(self, n: int, edges: list[list[int]], succProb: list[float], start_node: int, end_node: int) -> float:
        prob = [0.0] * n
        prob[start_node] = 1.0
        for _ in range(n - 1):
            updated = False
            for (u, v), p in zip(edges, succProb):
                if prob[u] * p > prob[v]:
                    prob[v] = prob[u] * p
                    updated = True
                if prob[v] * p > prob[u]:
                    prob[u] = prob[v] * p
                    updated = True
            if not updated: break
        return prob[end_node]"""
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
                "java": """import java.util.*;
class Solution {
    public double maxProbability(int n, int[][] edges, double[] succProb, int start, int end) {
        List<double[]>[] adj = new List[n];
        for (int i = 0; i < n; i++) adj[i] = new ArrayList<>();
        for (int i = 0; i < edges.length; i++) {
            int u = edges[i][0], v = edges[i][1];
            double p = succProb[i];
            adj[u].add(new double[]{v, p});
            adj[v].add(new double[]{u, p});
        }
        double[] probs = new double[n];
        probs[start] = 1.0;
        PriorityQueue<double[]> pq = new PriorityQueue<>((a, b) -> Double.compare(b[0], a[0]));
        pq.offer(new double[]{1.0, start});
        while (!pq.isEmpty()) {
            double[] cur = pq.poll();
            double p = cur[0];
            int u = (int) cur[1];
            if (u == end) return p;
            if (p < probs[u]) continue;
            for (double[] edge : adj[u]) {
                int v = (int) edge[0];
                double weight = edge[1];
                if (p * weight > probs[v]) {
                    probs[v] = p * weight;
                    pq.offer(new double[]{probs[v], v});
                }
            }
        }
        return 0.0;
    }
}""",
                "python": """import heapq
from collections import defaultdict

class Solution:
    def maxProbability(self, n: int, edges: list[list[int]], succProb: list[float], start_node: int, end_node: int) -> float:
        adj = defaultdict(list)
        for (u, v), p in zip(edges, succProb):
            adj[u].append((v, p))
            adj[v].append((u, p))
        probs = [0.0] * n
        probs[start_node] = 1.0
        pq = [(-1.0, start_node)]
        while pq:
            neg_p, u = heapq.heappop(pq)
            p = -neg_p
            if u == end_node:
                return p
            if p < probs[u]:
                continue
            for v, weight in adj[u]:
                if p * weight > probs[v]:
                    probs[v] = p * weight
                    heapq.heappush(pq, (-probs[v], v))
        return 0.0"""
            }
        }
    },
    # 232: Min Cost to Connect All Points
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
                "java": """import java.util.*;
class Solution {
    public int minCostConnectPoints(int[][] points) {
        int n = points.length;
        List<int[]> edges = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                int d = Math.abs(points[i][0] - points[j][0]) + Math.abs(points[i][1] - points[j][1]);
                edges.add(new int[]{d, i, j});
            }
        }
        edges.sort(Comparator.comparingInt(a -> a[0]));
        int[] parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
        int cost = 0, count = 0;
        for (int[] e : edges) {
            int ru = find(parent, e[1]), rv = find(parent, e[2]);
            if (ru != rv) {
                parent[ru] = rv;
                cost += e[0];
                if (++count == n - 1) break;
            }
        }
        return cost;
    }
    private int find(int[] p, int i) {
        if (p[i] == i) return i;
        return p[i] = find(p, p[i]);
    }
}""",
                "python": """class Solution:
    def minCostConnectPoints(self, points: list[list[int]]) -> int:
        n = len(points)
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                d = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
                edges.append((d, i, j))
        edges.sort()
        parent = list(range(n))
        def find(i):
            if parent[i] == i: return i
            parent[i] = find(parent[i])
            return parent[i]
        cost = 0
        count = 0
        for d, u, v in edges:
            ru, rv = find(u), find(v)
            if ru != rv:
                parent[ru] = rv
                cost += d
                count += 1
                if count == n - 1: break
        return cost"""
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
                "java": """import java.util.*;
class Solution {
    public int minCostConnectPoints(int[][] points) {
        int n = points.length;
        int[] minDist = new int[n];
        Arrays.fill(minDist, Integer.MAX_VALUE);
        minDist[0] = 0;
        boolean[] inMST = new boolean[n];
        int totalCost = 0;
        for (int step = 0; step < n; step++) {
            int u = -1;
            for (int i = 0; i < n; i++) {
                if (!inMST[i] && (u == -1 || minDist[i] < minDist[u])) {
                    u = i;
                }
            }
            inMST[u] = true;
            totalCost += minDist[u];
            for (int v = 0; v < n; v++) {
                if (!inMST[v]) {
                    int d = Math.abs(points[u][0] - points[v][0]) + Math.abs(points[u][1] - points[v][1]);
                    if (d < minDist[v]) {
                        minDist[v] = d;
                    }
                }
            }
        }
        return totalCost;
    }
}""",
                "python": """class Solution:
    def minCostConnectPoints(self, points: list[list[int]]) -> int:
        n = len(points)
        min_dist = [float('inf')] * n
        min_dist[0] = 0
        in_mst = [False] * n
        total_cost = 0
        for _ in range(n):
            u = -1
            for i in range(n):
                if not in_mst[i] and (u == -1 or min_dist[i] < min_dist[u]):
                    u = i
            in_mst[u] = True
            total_cost += min_dist[u]
            x1, y1 = points[u]
            for v in range(n):
                if not in_mst[v]:
                    x2, y2 = points[v]
                    d = abs(x1 - x2) + abs(y1 - y2)
                    if d < min_dist[v]:
                        min_dist[v] = d
        return total_cost"""
            }
        }
    },
    # 233: Reconstruct Itinerary
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
                "java": """import java.util.*;
class Solution {
    public List<String> findItinerary(List<List<String>> tickets) {
        Map<String, PriorityQueue<String>> targets = new HashMap<>();
        for (List<String> ticket : tickets) {
            targets.computeIfAbsent(ticket.get(0), k -> new PriorityQueue<>()).add(ticket.get(1));
        }
        LinkedList<String> route = new LinkedList<>();
        visit("JFK", targets, route);
        return route;
    }
    private void visit(String airport, Map<String, PriorityQueue<String>> targets, LinkedList<String> route) {
        while (targets.containsKey(airport) && !targets.get(airport).isEmpty()) {
            visit(targets.get(airport).poll(), targets, route);
        }
        route.addFirst(airport);
    }
}""",
                "python": """from collections import defaultdict
import heapq

class Solution:
    def findItinerary(self, tickets: list[list[str]]) -> list[str]:
        targets = defaultdict(list)
        for src, dst in tickets:
            heapq.heappush(targets[src], dst)
        route = []
        def visit(airport):
            while targets[airport]:
                visit(heapq.heappop(targets[airport]))
            route.append(airport)
        visit("JFK")
        return route[::-1]"""
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
                "java": """import java.util.*;
class Solution {
    private Map<String, PriorityQueue<String>> graph = new HashMap<>();
    private LinkedList<String> route = new LinkedList<>();
    public List<String> findItinerary(List<List<String>> tickets) {
        for (List<String> t : tickets) {
            graph.computeIfAbsent(t.get(0), k -> new PriorityQueue<>()).offer(t.get(1));
        }
        dfs("JFK");
        return route;
    }
    private void dfs(String airport) {
        PriorityQueue<String> dests = graph.get(airport);
        while (dests != null && !dests.isEmpty()) {
            dfs(dests.poll());
        }
        route.addFirst(airport);
    }
}""",
                "python": """import heapq
from collections import defaultdict

class Solution:
    def findItinerary(self, tickets: list[list[str]]) -> list[str]:
        graph = defaultdict(list)
        for u, v in tickets:
            heapq.heappush(graph[u], v)
        route = []
        def dfs(airport: str):
            while graph[airport]:
                dfs(heapq.heappop(graph[airport]))
            route.append(airport)
        dfs("JFK")
        return route[::-1]"""
            }
        }
    },
    # 234: Find the City With the Smallest Number of Neighbors at a Threshold Distance
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
                "java": """import java.util.*;
class Solution {
    public int findTheCity(int n, int[][] edges, int distanceThreshold) {
        int[][] dist = new int[n][n];
        for (int[] row : dist) Arrays.fill(row, 10000000);
        for (int i = 0; i < n; i++) dist[i][i] = 0;
        for (int[] e : edges) {
            dist[e[0]][e[1]] = e[2];
            dist[e[1]][e[0]] = e[2];
        }
        for (int k = 0; k < n; k++) {
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    dist[i][j] = Math.min(dist[i][j], dist[i][k] + dist[k][j]);
                }
            }
        }
        int bestCity = -1, minReachable = Integer.MAX_VALUE;
        for (int i = 0; i < n; i++) {
            int reachable = 0;
            for (int j = 0; j < n; j++) {
                if (i != j && dist[i][j] <= distanceThreshold) reachable++;
            }
            if (reachable <= minReachable) {
                minReachable = reachable;
                bestCity = i;
            }
        }
        return bestCity;
    }
}""",
                "python": """class Solution:
    def findTheCity(self, n: int, edges: list[list[int]], distanceThreshold: int) -> int:
        dist = [[float('inf')] * n for _ in range(n)]
        for i in range(n): dist[i][i] = 0
        for u, v, w in edges:
            dist[u][v] = dist[v][u] = w
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
        best_city, min_cnt = -1, float('inf')
        for i in range(n):
            cnt = sum(1 for j in range(n) if i != j and dist[i][j] <= distanceThreshold)
            if cnt <= min_cnt:
                min_cnt = cnt
                best_city = i
        return best_city"""
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
                "java": """import java.util.*;
class Solution {
    public int findTheCity(int n, int[][] edges, int distanceThreshold) {
        int[][] dist = new int[n][n];
        for (int[] row : dist) Arrays.fill(row, 10000000);
        for (int i = 0; i < n; i++) dist[i][i] = 0;
        for (int[] e : edges) {
            dist[e[0]][e[1]] = e[2];
            dist[e[1]][e[0]] = e[2];
        }
        for (int k = 0; k < n; k++) {
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    dist[i][j] = Math.min(dist[i][j], dist[i][k] + dist[k][j]);
                }
            }
        }
        int minCount = Integer.MAX_VALUE;
        int bestCity = -1;
        for (int i = 0; i < n; i++) {
            int reachable = 0;
            for (int j = 0; j < n; j++) {
                if (i != j && dist[i][j] <= distanceThreshold) {
                    reachable++;
                }
            }
            if (reachable <= minCount) {
                minCount = reachable;
                bestCity = i;
            }
        }
        return bestCity;
    }
}""",
                "python": """class Solution:
    def findTheCity(self, n: int, edges: list[list[int]], distanceThreshold: int) -> int:
        dist = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
        for u, v, w in edges:
            dist[u][v] = dist[v][u] = w
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
        best_city = -1
        min_reachable = float('inf')
        for i in range(n):
            cnt = sum(1 for j in range(n) if i != j and dist[i][j] <= distanceThreshold)
            if cnt <= min_reachable:
                min_reachable = cnt
                best_city = i
        return best_city"""
            }
        }
    },
    # 235: Climbing Stairs
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
                "java": """class Solution {
    public int climbStairs(int n) {
        if (n <= 2) return n;
        return climbStairs(n - 1) + climbStairs(n - 2);
    }
}""",
                "python": """class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2: return n
        return self.climbStairs(n - 1) + self.climbStairs(n - 2)"""
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
                "java": """class Solution {
    public int climbStairs(int n) {
        if (n <= 2) return n;
        int a = 1, b = 2;
        for (int i = 3; i <= n; i++) {
            int c = a + b;
            a = b;
            b = c;
        }
        return b;
    }
}""",
                "python": """class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n
        a, b = 1, 2
        for _ in range(3, n + 1):
            a, b = b, a + b
        return b"""
            }
        }
    },
    # 236: Min Cost Climbing Stairs
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
                "java": """class Solution {
    public int minCostClimbingStairs(int[] cost) {
        return Math.min(dfs(cost, 0), dfs(cost, 1));
    }
    private int dfs(int[] cost, int idx) {
        if (idx >= cost.length) return 0;
        return cost[idx] + Math.min(dfs(cost, idx + 1), dfs(cost, idx + 2));
    }
}""",
                "python": """class Solution:
    def minCostClimbingStairs(self, cost: list[int]) -> int:
        def dfs(i):
            if i >= len(cost): return 0
            return cost[i] + min(dfs(i + 1), dfs(i + 2))
        return min(dfs(0), dfs(1))"""
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
                "java": """class Solution {
    public int minCostClimbingStairs(int[] cost) {
        int a = 0, b = 0;
        for (int i = 2; i <= cost.length; i++) {
            int c = Math.min(a + cost[i - 2], b + cost[i - 1]);
            a = b;
            b = c;
        }
        return b;
    }
}""",
                "python": """class Solution:
    def minCostClimbingStairs(self, cost: list[int]) -> int:
        a = b = 0
        for i in range(2, len(cost) + 1):
            c = min(a + cost[i - 2], b + cost[i - 1])
            a, b = b, c
        return b"""
            }
        }
    },
    # 237: N-th Tribonacci Number
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
                "java": """class Solution {
    public int tribonacci(int n) {
        if (n == 0) return 0;
        if (n <= 2) return 1;
        return tribonacci(n - 1) + tribonacci(n - 2) + tribonacci(n - 3);
    }
}""",
                "python": """class Solution:
    def tribonacci(self, n: int) -> int:
        if n == 0: return 0
        if n <= 2: return 1
        return self.tribonacci(n - 1) + self.tribonacci(n - 2) + self.tribonacci(n - 3)"""
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
                "java": """class Solution {
    public int tribonacci(int n) {
        if (n == 0) return 0;
        if (n <= 2) return 1;
        int a = 0, b = 1, c = 1;
        for (int i = 3; i <= n; i++) {
            int d = a + b + c;
            a = b;
            b = c;
            c = d;
        }
        return c;
    }
}""",
                "python": """class Solution:
    def tribonacci(self, n: int) -> int:
        if n == 0:
            return 0
        if n <= 2:
            return 1
        a, b, c = 0, 1, 1
        for _ in range(3, n + 1):
            a, b, c = b, c, a + b + c
        return c"""
            }
        }
    },
    # 238: House Robber
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
                "java": """class Solution {
    public int rob(int[] nums) {
        return dfs(nums, 0);
    }
    private int dfs(int[] nums, int i) {
        if (i >= nums.length) return 0;
        return Math.max(nums[i] + dfs(nums, i + 2), dfs(nums, i + 1));
    }
}""",
                "python": """class Solution:
    def rob(self, nums: list[int]) -> int:
        def dfs(i):
            if i >= len(nums): return 0
            return max(nums[i] + dfs(i + 2), dfs(i + 1))
        return dfs(0)"""
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
                "java": """class Solution {
    public int rob(int[] nums) {
        int prev1 = 0, prev2 = 0;
        for (int x : nums) {
            int cur = Math.max(prev1, prev2 + x);
            prev2 = prev1;
            prev1 = cur;
        }
        return prev1;
    }
}""",
                "python": """class Solution:
    def rob(self, nums: list[int]) -> int:
        prev1 = prev2 = 0
        for x in nums:
            prev1, prev2 = max(prev1, prev2 + x), prev1
        return prev1"""
            }
        }
    },
    # 239: House Robber II
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
                "java": """class Solution {
    public int rob(int[] nums) {
        if (nums.length == 1) return nums[0];
        return Math.max(robRange(nums, 0, nums.length - 2), robRange(nums, 1, nums.length - 1));
    }
    private int robRange(int[] nums, int l, int r) {
        int prev1 = 0, prev2 = 0;
        for (int i = l; i <= r; i++) {
            int cur = Math.max(prev1, prev2 + nums[i]);
            prev2 = prev1;
            prev1 = cur;
        }
        return prev1;
    }
}""",
                "python": """class Solution:
    def rob(self, nums: list[int]) -> int:
        if len(nums) == 1: return nums[0]
        def rob_simple(arr):
            p1 = p2 = 0
            for x in arr:
                p1, p2 = max(p1, p2 + x), p1
            return p1
        return max(rob_simple(nums[:-1]), rob_simple(nums[1:]))"""
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
                "java": """class Solution {
    public int rob(int[] nums) {
        if (nums.length == 1) return nums[0];
        return Math.max(robLinear(nums, 0, nums.length - 2), robLinear(nums, 1, nums.length - 1));
    }
    private int robLinear(int[] nums, int start, int end) {
        int prev1 = 0, prev2 = 0;
        for (int i = start; i <= end; i++) {
            int cur = Math.max(prev1, prev2 + nums[i]);
            prev2 = prev1;
            prev1 = cur;
        }
        return prev1;
    }
}""",
                "python": """class Solution:
    def rob(self, nums: list[int]) -> int:
        if len(nums) == 1:
            return nums[0]
        def rob_linear(start: int, end: int) -> int:
            p1 = p2 = 0
            for i in range(start, end + 1):
                p1, p2 = max(p1, p2 + nums[i]), p1
            return p1
        return max(rob_linear(0, len(nums) - 2), rob_linear(1, len(nums) - 1))"""
            }
        }
    },
    # 240: Delete and Earn
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
                "java": """class Solution {
    public int deleteAndEarn(int[] nums) {
        int max = 0;
        for (int x : nums) max = Math.max(max, x);
        int[] points = new int[max + 1];
        for (int x : nums) points[x] += x;
        int p1 = 0, p2 = 0;
        for (int p : points) {
            int cur = Math.max(p1, p2 + p);
            p2 = p1;
            p1 = cur;
        }
        return p1;
    }
}""",
                "python": """class Solution:
    def deleteAndEarn(self, nums: list[int]) -> int:
        max_val = max(nums)
        points = [0] * (max_val + 1)
        for x in nums: points[x] += x
        p1 = p2 = 0
        for p in points:
            p1, p2 = max(p1, p2 + p), p1
        return p1"""
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
                "java": """class Solution {
    public int deleteAndEarn(int[] nums) {
        int max = 0;
        for (int x : nums) max = Math.max(max, x);
        int[] points = new int[max + 1];
        for (int x : nums) points[x] += x;
        int prev1 = 0, prev2 = 0;
        for (int p : points) {
            int cur = Math.max(prev1, prev2 + p);
            prev2 = prev1;
            prev1 = cur;
        }
        return prev1;
    }
}""",
                "python": """class Solution:
    def deleteAndEarn(self, nums: list[int]) -> int:
        max_val = max(nums)
        points = [0] * (max_val + 1)
        for x in nums:
            points[x] += x
        p1 = p2 = 0
        for p in points:
            p1, p2 = max(p1, p2 + p), p1
        return p1"""
            }
        }
    },
    # 241: Decode Ways
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
                "java": """class Solution {
    public int numDecodings(String s) {
        return dfs(s, 0);
    }
    private int dfs(String s, int idx) {
        if (idx == s.length()) return 1;
        if (s.charAt(idx) == '0') return 0;
        int ways = dfs(s, idx + 1);
        if (idx + 1 < s.length()) {
            int val = Integer.parseInt(s.substring(idx, idx + 2));
            if (val <= 26) ways += dfs(s, idx + 2);
        }
        return ways;
    }
}""",
                "python": """class Solution:
    def numDecodings(self, s: str) -> int:
        def dfs(i):
            if i == len(s): return 1
            if s[i] == '0': return 0
            ways = dfs(i + 1)
            if i + 1 < len(s) and 10 <= int(s[i:i+2]) <= 26:
                ways += dfs(i + 2)
            return ways
        return dfs(0)"""
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
                "java": """class Solution {
    public int numDecodings(String s) {
        if (s == null || s.length() == 0 || s.charAt(0) == '0') return 0;
        int n = s.length();
        int prev2 = 1, prev1 = 1;
        for (int i = 1; i < n; i++) {
            int cur = 0;
            if (s.charAt(i) != '0') {
                cur += prev1;
            }
            int twoDigit = (s.charAt(i - 1) - '0') * 10 + (s.charAt(i) - '0');
            if (twoDigit >= 10 && twoDigit <= 26) {
                cur += prev2;
            }
            prev2 = prev1;
            prev1 = cur;
        }
        return prev1;
    }
}""",
                "python": """class Solution:
    def numDecodings(self, s: str) -> int:
        if not s or s[0] == '0':
            return 0
        prev2, prev1 = 1, 1
        for i in range(1, len(s)):
            cur = 0
            if s[i] != '0':
                cur += prev1
            two_digit = int(s[i-1:i+1])
            if 10 <= two_digit <= 26:
                cur += prev2
            prev2, prev1 = prev1, cur
        return prev1"""
            }
        }
    },
    # 242: Coin Change
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
                "java": """import java.util.*;
class Solution {
    public int coinChange(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, amount + 1);
        dp[0] = 0;
        for (int i = 1; i <= amount; i++) {
            for (int c : coins) {
                if (i >= c) dp[i] = Math.min(dp[i], dp[i - c] + 1);
            }
        }
        return dp[amount] > amount ? -1 : dp[amount];
    }
}""",
                "python": """class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        dp = [amount + 1] * (amount + 1)
        dp[0] = 0
        for i in range(1, amount + 1):
            for c in coins:
                if i >= c:
                    dp[i] = min(dp[i], dp[i - c] + 1)
        return dp[amount] if dp[amount] <= amount else -1"""
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
                "java": """import java.util.*;
class Solution {
    public int coinChange(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, amount + 1);
        dp[0] = 0;
        for (int i = 1; i <= amount; i++) {
            for (int coin : coins) {
                if (i >= coin) {
                    dp[i] = Math.min(dp[i], dp[i - coin] + 1);
                }
            }
        }
        return dp[amount] > amount ? -1 : dp[amount];
    }
}""",
                "python": """class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        dp = [amount + 1] * (amount + 1)
        dp[0] = 0
        for i in range(1, amount + 1):
            for coin in coins:
                if i >= coin:
                    dp[i] = min(dp[i], dp[i - coin] + 1)
        return dp[amount] if dp[amount] <= amount else -1"""
            }
        }
    },
    # 243: Coin Change II
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
                "java": """class Solution {
    public int change(int amount, int[] coins) {
        int[] dp = new int[amount + 1];
        dp[0] = 1;
        for (int c : coins) {
            for (int i = c; i <= amount; i++) {
                dp[i] += dp[i - c];
            }
        }
        return dp[amount];
    }
}""",
                "python": """class Solution:
    def change(self, amount: int, coins: list[int]) -> int:
        dp = [0] * (amount + 1)
        dp[0] = 1
        for c in coins:
            for i in range(c, amount + 1):
                dp[i] += dp[i - c]
        return dp[amount]"""
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
                "java": """class Solution {
    public int change(int amount, int[] coins) {
        int[] dp = new int[amount + 1];
        dp[0] = 1;
        for (int coin : coins) {
            for (int i = coin; i <= amount; i++) {
                dp[i] += dp[i - coin];
            }
        }
        return dp[amount];
    }
}""",
                "python": """class Solution:
    def change(self, amount: int, coins: list[int]) -> int:
        dp = [0] * (amount + 1)
        dp[0] = 1
        for coin in coins:
            for i in range(coin, amount + 1):
                dp[i] += dp[i - coin]
        return dp[amount]"""
            }
        }
    },
    # 244: Combination Sum IV
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
                "java": """class Solution {
    public int combinationSum4(int[] nums, int target) {
        int[] dp = new int[target + 1];
        dp[0] = 1;
        for (int i = 1; i <= target; i++) {
            for (int num : nums) {
                if (i >= num) dp[i] += dp[i - num];
            }
        }
        return dp[target];
    }
}""",
                "python": """class Solution:
    def combinationSum4(self, nums: list[int], target: int) -> int:
        dp = [0] * (target + 1)
        dp[0] = 1
        for i in range(1, target + 1):
            for num in nums:
                if i >= num: dp[i] += dp[i - num]
        return dp[target]"""
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
                "java": """class Solution {
    public int combinationSum4(int[] nums, int target) {
        int[] dp = new int[target + 1];
        dp[0] = 1;
        for (int i = 1; i <= target; i++) {
            for (int num : nums) {
                if (i >= num) {
                    dp[i] += dp[i - num];
                }
            }
        }
        return dp[target];
    }
}""",
                "python": """class Solution:
    def combinationSum4(self, nums: list[int], target: int) -> int:
        dp = [0] * (target + 1)
        dp[0] = 1
        for i in range(1, target + 1):
            for num in nums:
                if i >= num:
                    dp[i] += dp[i - num]
        return dp[target]"""
            }
        }
    },
    # 245: Perfect Squares
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
                "java": """import java.util.*;
class Solution {
    public int numSquares(int n) {
        int[] dp = new int[n + 1];
        Arrays.fill(dp, n);
        dp[0] = 0;
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j * j <= i; j++) {
                dp[i] = Math.min(dp[i], dp[i - j * j] + 1);
            }
        }
        return dp[n];
    }
}""",
                "python": """class Solution:
    def numSquares(self, n: int) -> int:
        dp = [n] * (n + 1)
        dp[0] = 0
        for i in range(1, n + 1):
            j = 1
            while j * j <= i:
                dp[i] = min(dp[i], dp[i - j * j] + 1)
                j += 1
        return dp[n]"""
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
                "java": """import java.util.*;
class Solution {
    public int numSquares(int n) {
        int[] dp = new int[n + 1];
        Arrays.fill(dp, Integer.MAX_VALUE);
        dp[0] = 0;
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j * j <= i; j++) {
                dp[i] = Math.min(dp[i], dp[i - j * j] + 1);
            }
        }
        return dp[n];
    }
}""",
                "python": """class Solution:
    def numSquares(self, n: int) -> int:
        dp = [float('inf')] * (n + 1)
        dp[0] = 0
        for i in range(1, n + 1):
            j = 1
            while j * j <= i:
                dp[i] = min(dp[i], dp[i - j * j] + 1)
                j += 1
        return dp[n]"""
            }
        }
    },
    # 246: Word Break
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
                "java": """import java.util.*;
class Solution {
    public boolean wordBreak(String s, List<String> wordDict) {
        Set<String> set = new HashSet<>(wordDict);
        boolean[] dp = new boolean[s.length() + 1];
        dp[0] = true;
        for (int i = 1; i <= s.length(); i++) {
            for (int j = 0; j < i; j++) {
                if (dp[j] && set.contains(s.substring(j, i))) {
                    dp[i] = true;
                    break;
                }
            }
        }
        return dp[s.length()];
    }
}""",
                "python": """class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        words = set(wordDict)
        dp = [False] * (len(s) + 1)
        dp[0] = True
        for i in range(1, len(s) + 1):
            for j in range(i):
                if dp[j] and s[j:i] in words:
                    dp[i] = True
                    break
        return dp[len(s)]"""
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
                "java": """import java.util.*;
class Solution {
    public boolean wordBreak(String s, List<String> wordDict) {
        Set<String> set = new HashSet<>(wordDict);
        int n = s.length();
        boolean[] dp = new boolean[n + 1];
        dp[0] = true;
        for (int i = 1; i <= n; i++) {
            for (int j = 0; j < i; j++) {
                if (dp[j] && set.contains(s.substring(j, i))) {
                    dp[i] = true;
                    break;
                }
            }
        }
        return dp[n];
    }
}""",
                "python": """class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        words = set(wordDict)
        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True
        for i in range(1, n + 1):
            for j in range(i):
                if dp[j] and s[j:i] in words:
                    dp[i] = True
                    break
        return dp[n]"""
            }
        }
    },
    # 247: Longest Increasing Subsequence
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
                "java": """import java.util.*;
class Solution {
    public int lengthOfLIS(int[] nums) {
        int n = nums.length;
        int[] dp = new int[n];
        Arrays.fill(dp, 1);
        int max = 1;
        for (int i = 1; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (nums[j] < nums[i]) {
                    dp[i] = Math.max(dp[i], dp[j] + 1);
                }
            }
            max = Math.max(max, dp[i]);
        }
        return max;
    }
}""",
                "python": """class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        dp = [1] * len(nums)
        for i in range(len(nums)):
            for j in range(i):
                if nums[j] < nums[i]:
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)"""
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
                "java": """import java.util.*;
class Solution {
    public int lengthOfLIS(int[] nums) {
        int[] tails = new int[nums.length];
        int size = 0;
        for (int x : nums) {
            int l = 0, r = size;
            while (l < r) {
                int m = l + (r - l) / 2;
                if (tails[m] < x) l = m + 1;
                else r = m;
            }
            tails[l] = x;
            if (l == size) size++;
        }
        return size;
    }
}""",
                "python": """import bisect

class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        tails = []
        for x in nums:
            idx = bisect.bisect_left(tails, x)
            if idx == len(tails):
                tails.append(x)
            else:
                tails[idx] = x
        return len(tails)"""
            }
        }
    },
    # 248: Number of Longest Increasing Subsequence
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
                "java": """import java.util.*;
class Solution {
    public int findNumberOfLIS(int[] nums) {
        int n = nums.length;
        int[] len = new int[n];
        int[] count = new int[n];
        Arrays.fill(len, 1);
        Arrays.fill(count, 1);
        int maxLen = 1;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (nums[j] < nums[i]) {
                    if (len[j] + 1 > len[i]) {
                        len[i] = len[j] + 1;
                        count[i] = count[j];
                    } else if (len[j] + 1 == len[i]) {
                        count[i] += count[j];
                    }
                }
            }
            maxLen = Math.max(maxLen, len[i]);
        }
        int total = 0;
        for (int i = 0; i < n; i++) {
            if (len[i] == maxLen) total += count[i];
        }
        return total;
    }
}""",
                "python": """class Solution:
    def findNumberOfLIS(self, nums: list[int]) -> int:
        n = len(nums)
        length = [1] * n
        count = [1] * n
        for i in range(n):
            for j in range(i):
                if nums[j] < nums[i]:
                    if length[j] + 1 > length[i]:
                        length[i] = length[j] + 1
                        count[i] = count[j]
                    elif length[j] + 1 == length[i]:
                        count[i] += count[j]
        max_l = max(length)
        return sum(c for l, c in zip(length, count) if l == max_l)"""
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
                "java": """import java.util.*;
class Solution {
    public int findNumberOfLIS(int[] nums) {
        int n = nums.length;
        int[] len = new int[n];
        int[] count = new int[n];
        Arrays.fill(len, 1);
        Arrays.fill(count, 1);
        int maxLen = 1;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (nums[j] < nums[i]) {
                    if (len[j] + 1 > len[i]) {
                        len[i] = len[j] + 1;
                        count[i] = count[j];
                    } else if (len[j] + 1 == len[i]) {
                        count[i] += count[j];
                    }
                }
            }
            maxLen = Math.max(maxLen, len[i]);
        }
        int total = 0;
        for (int i = 0; i < n; i++) {
            if (len[i] == maxLen) total += count[i];
        }
        return total;
    }
}""",
                "python": """class Solution:
    def findNumberOfLIS(self, nums: list[int]) -> int:
        n = len(nums)
        length = [1] * n
        count = [1] * n
        for i in range(n):
            for j in range(i):
                if nums[j] < nums[i]:
                    if length[j] + 1 > length[i]:
                        length[i] = length[j] + 1
                        count[i] = count[j]
                    elif length[j] + 1 == length[i]:
                        count[i] += count[j]
        max_len = max(length)
        return sum(c for l, c in zip(length, count) if l == max_len)"""
            }
        }
    },
    # 249: Russian Doll Envelopes
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
                "java": """import java.util.*;
class Solution {
    public int maxEnvelopes(int[][] envelopes) {
        Arrays.sort(envelopes, (a, b) -> a[0] != b[0] ? a[0] - b[0] : b[1] - a[1]);
        int[] dp = new int[envelopes.length];
        int size = 0;
        for (int[] env : envelopes) {
            int h = env[1];
            int l = 0, r = size;
            while (l < r) {
                int m = l + (r - l) / 2;
                if (dp[m] < h) l = m + 1;
                else r = m;
            }
            dp[l] = h;
            if (l == size) size++;
        }
        return size;
    }
}""",
                "python": """import bisect

class Solution:
    def maxEnvelopes(self, envelopes: list[list[int]]) -> int:
        envelopes.sort(key=lambda x: (x[0], -x[1]))
        tails = []
        for _, h in envelopes:
            idx = bisect.bisect_left(tails, h)
            if idx == len(tails):
                tails.append(h)
            else:
                tails[idx] = h
        return len(tails)"""
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
                "java": """import java.util.*;
class Solution {
    public int maxEnvelopes(int[][] envelopes) {
        Arrays.sort(envelopes, (a, b) -> a[0] != b[0] ? a[0] - b[0] : b[1] - a[1]);
        int[] dp = new int[envelopes.length];
        int size = 0;
        for (int[] env : envelopes) {
            int h = env[1];
            int l = 0, r = size;
            while (l < r) {
                int m = l + (r - l) / 2;
                if (dp[m] < h) l = m + 1;
                else r = m;
            }
            dp[l] = h;
            if (l == size) size++;
        }
        return size;
    }
}""",
                "python": """import bisect

class Solution:
    def maxEnvelopes(self, envelopes: list[list[int]]) -> int:
        envelopes.sort(key=lambda x: (x[0], -x[1]))
        tails = []
        for _, h in envelopes:
            idx = bisect.bisect_left(tails, h)
            if idx == len(tails):
                tails.append(h)
            else:
                tails[idx] = h
        return len(tails)"""
            }
        }
    },
    # 250: Maximum Product Subarray
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
                "java": """class Solution {
    public int maxProduct(int[] nums) {
        int max = nums[0];
        for (int i = 0; i < nums.length; i++) {
            int prod = 1;
            for (int j = i; j < nums.length; j++) {
                prod *= nums[j];
                max = Math.max(max, prod);
            }
        }
        return max;
    }
}""",
                "python": """class Solution:
    def maxProduct(self, nums: list[int]) -> int:
        ans = nums[0]
        for i in range(len(nums)):
            prod = 1
            for j in range(i, len(nums)):
                prod *= nums[j]
                ans = max(ans, prod)
        return ans"""
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
                "java": """class Solution {
    public int maxProduct(int[] nums) {
        int curMax = nums[0], curMin = nums[0], ans = nums[0];
        for (int i = 1; i < nums.length; i++) {
            int num = nums[i];
            if (num < 0) {
                int temp = curMax;
                curMax = curMin;
                curMin = temp;
            }
            curMax = Math.max(num, curMax * num);
            curMin = Math.min(num, curMin * num);
            ans = Math.max(ans, curMax);
        }
        return ans;
    }
}""",
                "python": """class Solution:
    def maxProduct(self, nums: list[int]) -> int:
        cur_max = cur_min = ans = nums[0]
        for num in nums[1:]:
            if num < 0:
                cur_max, cur_min = cur_min, cur_max
            cur_max = max(num, cur_max * num)
            cur_min = min(num, cur_min * num)
            ans = max(ans, cur_max)
        return ans"""
            }
        }
    }
]

with open('scripts/batches/batch_10.py', 'w', encoding='utf-8') as f:
    f.write("# Batch 10: Questions 226 to 250\n\n")
    f.write("def get_batch():\n")
    f.write("    return " + json.dumps(batch_10, indent=4) + "\n")

print("Wrote scripts/batches/batch_10.py with", len(batch_10), "questions.")


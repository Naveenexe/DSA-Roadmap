# scripts/gen_batch_09.py
import json

batch_9 = [
    # 201: Pacific Atlantic Water Flow
    {
        "seq": 201,
        "whyNext": "Multi-source reverse flood fill: flow uphill from ocean borders; intersection of reachable cells can reach both oceans.",
        "brute": {
            "idea": "From every cell (r, c), run DFS to check if water can flow down to both Pacific and Atlantic boundaries.",
            "steps": [
                "For each cell in grid, run DFS downhill.",
                "If both oceans reached, add to result list."
            ],
            "time": "O(m^2 * n^2)",
            "space": "O(m * n)",
            "whySlow": "Launches DFS from all m * n cells independently.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> pacificAtlantic(int[][] heights) {
        List<List<Integer>> res = new ArrayList<>();
        int m = heights.length, n = heights[0].length;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                boolean[] ocean = new boolean[2];
                dfs(heights, i, j, new boolean[m][n], ocean);
                if (ocean[0] && ocean[1]) res.add(Arrays.asList(i, j));
            }
        }
        return res;
    }
    private void dfs(int[][] h, int r, int c, boolean[][] visited, boolean[] ocean) {
        visited[r][c] = true;
        if (r == 0 || c == 0) ocean[0] = true;
        if (r == h.length - 1 || c == h[0].length - 1) ocean[1] = true;
        int[][] dirs = {{1,0}, {-1,0}, {0,1}, {0,-1}};
        for (int[] d : dirs) {
            int nr = r + d[0], nc = c + d[1];
            if (nr >= 0 && nr < h.length && nc >= 0 && nc < h[0].length && !visited[nr][nc] && h[nr][nc] <= h[r][c]) {
                dfs(h, nr, nc, visited, ocean);
            }
        }
    }
}""",
                "python": """class Solution:
    def pacificAtlantic(self, heights: list[list[int]]) -> list[list[int]]:
        m, n = len(heights), len(heights[0])
        res = []
        for i in range(m):
            for j in range(n):
                ocean = [False, False]
                visited = [[False]*n for _ in range(m)]
                def dfs(r, c):
                    visited[r][c] = True
                    if r == 0 or c == 0: ocean[0] = True
                    if r == m - 1 or c == n - 1: ocean[1] = True
                    for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < m and 0 <= nc < n and not visited[nr][nc] and heights[nr][nc] <= heights[r][c]:
                            dfs(nr, nc)
                dfs(i, j)
                if ocean[0] and ocean[1]: res.append([i, j])
        return res"""
            }
        },
        "optimal": {
            "idea": "Reverse flow from borders: flow uphill (heights[next] >= heights[cur]) from Pacific borders and Atlantic borders into two boolean grids.",
            "steps": [
                "boolean[][] pacific, atlantic.",
                "DFS uphill from row 0 and col 0 for Pacific.",
                "DFS uphill from row m - 1 and col n - 1 for Atlantic.",
                "Intersection of pacific[i][j] && atlantic[i][j] gives answer."
            ],
            "time": "O(m * n)",
            "space": "O(m * n)",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> pacificAtlantic(int[][] heights) {
        List<List<Integer>> res = new ArrayList<>();
        int m = heights.length, n = heights[0].length;
        boolean[][] pac = new boolean[m][n];
        boolean[][] atl = new boolean[m][n];
        for (int i = 0; i < m; i++) {
            dfs(heights, i, 0, pac, heights[i][0]);
            dfs(heights, i, n - 1, atl, heights[i][n - 1]);
        }
        for (int j = 0; j < n; j++) {
            dfs(heights, 0, j, pac, heights[0][j]);
            dfs(heights, m - 1, j, atl, heights[m - 1][j]);
        }
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (pac[i][j] && atl[i][j]) {
                    res.add(Arrays.asList(i, j));
                }
            }
        }
        return res;
    }
    private void dfs(int[][] h, int r, int c, boolean[][] visited, int prevH) {
        if (r < 0 || r >= h.length || c < 0 || c >= h[0].length || visited[r][c] || h[r][c] < prevH) return;
        visited[r][c] = true;
        dfs(h, r + 1, c, visited, h[r][c]);
        dfs(h, r - 1, c, visited, h[r][c]);
        dfs(h, r, c + 1, visited, h[r][c]);
        dfs(h, r, c - 1, visited, h[r][c]);
    }
}""",
                "python": """class Solution:
    def pacificAtlantic(self, heights: list[list[int]]) -> list[list[int]]:
        m, n = len(heights), len(heights[0])
        pac = [[False] * n for _ in range(m)]
        atl = [[False] * n for _ in range(m)]
        def dfs(r, c, visited, prev_h):
            if not (0 <= r < m and 0 <= c < n) or visited[r][c] or heights[r][c] < prev_h:
                return
            visited[r][c] = True
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                dfs(r + dr, c + dc, visited, heights[r][c])
        for i in range(m):
            dfs(i, 0, pac, heights[i][0])
            dfs(i, n - 1, atl, heights[i][n - 1])
        for j in range(n):
            dfs(0, j, pac, heights[0][j])
            dfs(m - 1, j, atl, heights[m - 1][j])
        res = []
        for i in range(m):
            for j in range(n):
                if pac[i][j] and atl[i][j]:
                    res.append([i, j])
        return res"""
            }
        }
    },
    # 202: Number of Enclaves
    {
        "seq": 202,
        "whyNext": "Builds on Surrounded Regions: sink boundary-connected 1s using DFS/BFS; remaining 1s are trapped enclaves; sum them.",
        "brute": {
            "idea": "For each 1 cell, run DFS to detect if it can touch the boundary; if not, add cluster size to enclave count.",
            "steps": [
                "Find connected components of 1s.",
                "If component never reaches edge of grid, count its cells."
            ],
            "time": "O(m * n)",
            "space": "O(m * n)",
            "whySlow": "Tracking component boundaries requires separate tracking structures.",
            "code": {
                "java": """class Solution {
    public int numEnclaves(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        for (int i = 0; i < m; i++) {
            sink(grid, i, 0);
            sink(grid, i, n - 1);
        }
        for (int j = 0; j < n; j++) {
            sink(grid, 0, j);
            sink(grid, m - 1, j);
        }
        int count = 0;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 1) count++;
            }
        }
        return count;
    }
    private void sink(int[][] g, int r, int c) {
        if (r < 0 || r >= g.length || c < 0 || c >= g[0].length || g[r][c] != 1) return;
        g[r][c] = 0;
        sink(g, r + 1, c);
        sink(g, r - 1, c);
        sink(g, r, c + 1);
        sink(g, r, c - 1);
    }
}""",
                "python": """class Solution:
    def numEnclaves(self, grid: list[list[int]]) -> int:
        m, n = len(grid), len(grid[0])
        def sink(r, c):
            if not (0 <= r < m and 0 <= c < n) or grid[r][c] != 1: return
            grid[r][c] = 0
            sink(r + 1, c)
            sink(r - 1, c)
            sink(r, c + 1)
            sink(r, c - 1)
        for i in range(m):
            sink(i, 0)
            sink(i, n - 1)
        for j in range(n):
            sink(0, j)
            sink(m - 1, j)
        return sum(grid[i][j] for i in range(m) for j in range(n))"""
            }
        },
        "optimal": {
            "idea": "In-place border flood-fill: sink all 1s on borders (mutating to 0); count remaining 1s in interior.",
            "steps": [
                "Run sink DFS from all border cells where grid[r][c] == 1.",
                "Count all remaining cells with grid[r][c] == 1.",
                "Return count."
            ],
            "time": "O(m * n)",
            "space": "O(m * n)",
            "code": {
                "java": """class Solution {
    public int numEnclaves(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        for (int i = 0; i < m; i++) {
            if (grid[i][0] == 1) dfs(grid, i, 0, m, n);
            if (grid[i][n - 1] == 1) dfs(grid, i, n - 1, m, n);
        }
        for (int j = 0; j < n; j++) {
            if (grid[0][j] == 1) dfs(grid, 0, j, m, n);
            if (grid[m - 1][j] == 1) dfs(grid, m - 1, j, m, n);
        }
        int count = 0;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 1) count++;
            }
        }
        return count;
    }
    private void dfs(int[][] g, int r, int c, int m, int n) {
        if (r < 0 || r >= m || c < 0 || c >= n || g[r][c] != 1) return;
        g[r][c] = 0;
        dfs(g, r + 1, c, m, n);
        dfs(g, r - 1, c, m, n);
        dfs(g, r, c + 1, m, n);
        dfs(g, r, c - 1, m, n);
    }
}""",
                "python": """class Solution:
    def numEnclaves(self, grid: list[list[int]]) -> int:
        m, n = len(grid), len(grid[0])
        def dfs(r: int, c: int):
            if not (0 <= r < m and 0 <= c < n) or grid[r][c] != 1:
                return
            grid[r][c] = 0
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)
        for i in range(m):
            if grid[i][0] == 1: dfs(i, 0)
            if grid[i][n - 1] == 1: dfs(i, n - 1)
        for j in range(n):
            if grid[0][j] == 1: dfs(0, j)
            if grid[m - 1][j] == 1: dfs(m - 1, j)
        return sum(row.count(1) for row in grid)"""
            }
        }
    },
    # 203: Rotting Oranges
    {
        "seq": 203,
        "whyNext": "Multi-source BFS: enqueue all initially rotten oranges (2); expand level-by-level (minutes); return elapsed minutes or -1.",
        "brute": {
            "idea": "Simulate minute by minute: at each minute find all fresh oranges adjacent to rotten ones, mark them rotten.",
            "steps": [
                "While fresh oranges exist and at least one orange rots this round:",
                "Scan whole grid to find oranges to rot.",
                "Increment minute counter."
            ],
            "time": "O((m * n)^2)",
            "space": "O(m * n)",
            "whySlow": "Scans whole grid repeatedly for every minute instead of using a queue.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public int orangesRotting(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        Queue<int[]> q = new LinkedList<>();
        int fresh = 0;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 2) q.offer(new int[]{i, j});
                else if (grid[i][j] == 1) fresh++;
            }
        }
        if (fresh == 0) return 0;
        int minutes = 0;
        int[][] dirs = {{1,0}, {-1,0}, {0,1}, {0,-1}};
        while (!q.isEmpty()) {
            int size = q.size();
            boolean rotted = false;
            for (int i = 0; i < size; i++) {
                int[] cur = q.poll();
                for (int[] d : dirs) {
                    int r = cur[0] + d[0], c = cur[1] + d[1];
                    if (r >= 0 && r < m && c >= 0 && c < n && grid[r][c] == 1) {
                        grid[r][c] = 2;
                        fresh--;
                        rotted = true;
                        q.offer(new int[]{r, c});
                    }
                }
            }
            if (rotted) minutes++;
        }
        return fresh == 0 ? minutes : -1;
    }
}""",
                "python": """from collections import deque

class Solution:
    def orangesRotting(self, grid: list[list[int]]) -> int:
        m, n = len(grid), len(grid[0])
        q = deque()
        fresh = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 2: q.append((i, j))
                elif grid[i][j] == 1: fresh += 1
        if fresh == 0: return 0
        minutes = 0
        while q:
            rotted = False
            for _ in range(len(q)):
                r, c = q.popleft()
                for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                        grid[nr][nc] = 2
                        fresh -= 1
                        rotted = True
                        q.append((nr, nc))
            if rotted: minutes += 1
        return minutes if fresh == 0 else -1"""
            }
        },
        "optimal": {
            "idea": "Multi-source BFS: enqueue all rotten cells initially; each level represents 1 minute; decrement fresh counter.",
            "steps": [
                "Count fresh oranges; enqueue all cells with value 2.",
                "If fresh == 0 return 0.",
                "Run BFS by level; for each popped cell, rot 4 adjacent fresh oranges, decrement fresh, enqueue.",
                "Return fresh == 0 ? minutes : -1."
            ],
            "time": "O(m * n)",
            "space": "O(m * n)",
            "code": {
                "java": """import java.util.*;
class Solution {
    public int orangesRotting(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        Queue<int[]> q = new LinkedList<>();
        int fresh = 0;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 2) q.offer(new int[]{i, j});
                else if (grid[i][j] == 1) fresh++;
            }
        }
        if (fresh == 0) return 0;
        int minutes = 0;
        int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        while (!q.isEmpty() && fresh > 0) {
            minutes++;
            int size = q.size();
            for (int i = 0; i < size; i++) {
                int[] cur = q.poll();
                for (int[] d : dirs) {
                    int r = cur[0] + d[0], c = cur[1] + d[1];
                    if (r >= 0 && r < m && c >= 0 && c < n && grid[r][c] == 1) {
                        grid[r][c] = 2;
                        fresh--;
                        q.offer(new int[]{r, c});
                    }
                }
            }
        }
        return fresh == 0 ? minutes : -1;
    }
}""",
                "python": """from collections import deque

class Solution:
    def orangesRotting(self, grid: list[list[int]]) -> int:
        m, n = len(grid), len(grid[0])
        q = deque()
        fresh = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 2:
                    q.append((i, j))
                elif grid[i][j] == 1:
                    fresh += 1
        if fresh == 0:
            return 0
        minutes = 0
        while q and fresh > 0:
            minutes += 1
            for _ in range(len(q)):
                r, c = q.popleft()
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                        grid[nr][nc] = 2
                        fresh -= 1
                        q.append((nr, nc))
        return minutes if fresh == 0 else -1"""
            }
        }
    },
    # 204: 01 Matrix
    {
        "seq": 204,
        "whyNext": "Multi-source BFS / 2-pass DP: distance from each cell to nearest 0; enqueue all 0 cells with distance 0.",
        "brute": {
            "idea": "For every 1 cell, run BFS to find the shortest path to nearest 0.",
            "steps": [
                "For each 1 cell, launch BFS.",
                "Return distance when encountering first 0."
            ],
            "time": "O((m * n)^2)",
            "space": "O(m * n)",
            "whySlow": "Launches m * n individual BFS searches.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public int[][] updateMatrix(int[][] mat) {
        int m = mat.length, n = mat[0].length;
        int[][] res = new int[m][n];
        for (int[] row : res) Arrays.fill(row, -1);
        Queue<int[]> q = new LinkedList<>();
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (mat[i][j] == 0) {
                    res[i][j] = 0;
                    q.offer(new int[]{i, j});
                }
            }
        }
        int[][] dirs = {{1,0}, {-1,0}, {0,1}, {0,-1}};
        while (!q.isEmpty()) {
            int[] cur = q.poll();
            for (int[] d : dirs) {
                int r = cur[0] + d[0], c = cur[1] + d[1];
                if (r >= 0 && r < m && c >= 0 && c < n && res[r][c] == -1) {
                    res[r][c] = res[cur[0]][cur[1]] + 1;
                    q.offer(new int[]{r, c});
                }
            }
        }
        return res;
    }
}""",
                "python": """from collections import deque

class Solution:
    def updateMatrix(self, mat: list[list[int]]) -> list[list[int]]:
        m, n = len(mat), len(mat[0])
        dist = [[-1] * n for _ in range(m)]
        q = deque()
        for i in range(m):
            for j in range(n):
                if mat[i][j] == 0:
                    dist[i][j] = 0
                    q.append((i, j))
        while q:
            r, c = q.popleft()
            for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    q.append((nr, nc))
        return dist"""
            }
        },
        "optimal": {
            "idea": "Two-pass DP without queue: top-left to bottom-right minimizes from top and left; bottom-right to top-left minimizes from bottom and right.",
            "steps": [
                "Initialize dist matrix with INF (e.g. m + n), dist[i][j] = 0 if mat[i][j] == 0.",
                "Pass 1: for i 0..m-1, j 0..n-1: dist[i][j] = min(dist[i][j], min(dist[i-1][j], dist[i][j-1]) + 1).",
                "Pass 2: for i m-1..0, j n-1..0: dist[i][j] = min(dist[i][j], min(dist[i+1][j], dist[i][j+1]) + 1).",
                "Return dist."
            ],
            "time": "O(m * n)",
            "space": "O(1) auxiliary",
            "code": {
                "java": """class Solution {
    public int[][] updateMatrix(int[][] mat) {
        int m = mat.length, n = mat[0].length;
        int INF = m + n;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (mat[i][j] != 0) {
                    int top = (i > 0) ? mat[i - 1][j] : INF;
                    int left = (j > 0) ? mat[i][j - 1] : INF;
                    mat[i][j] = Math.min(top, left) + 1;
                }
            }
        }
        for (int i = m - 1; i >= 0; i--) {
            for (int j = n - 1; j >= 0; j--) {
                if (mat[i][j] != 0) {
                    int bottom = (i < m - 1) ? mat[i + 1][j] : INF;
                    int right = (j < n - 1) ? mat[i][j + 1] : INF;
                    mat[i][j] = Math.min(mat[i][j], Math.min(bottom, right) + 1);
                }
            }
        }
        return mat;
    }
}""",
                "python": """class Solution:
    def updateMatrix(self, mat: list[list[int]]) -> list[list[int]]:
        m, n = len(mat), len(mat[0])
        INF = m + n
        for i in range(m):
            for j in range(n):
                if mat[i][j] != 0:
                    top = mat[i - 1][j] if i > 0 else INF
                    left = mat[i][j - 1] if j > 0 else INF
                    mat[i][j] = min(top, left) + 1
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                if mat[i][j] != 0:
                    bottom = mat[i + 1][j] if i < m - 1 else INF
                    right = mat[i][j + 1] if j < n - 1 else INF
                    mat[i][j] = min(mat[i][j], min(bottom, right) + 1)
        return mat"""
            }
        }
    },
    # 205: Shortest Path in Binary Matrix
    {
        "seq": 205,
        "whyNext": "8-directional BFS: shortest path on unweighted grid from (0,0) to (n-1, n-1) with level distance.",
        "brute": {
            "idea": "DFS searching all paths from (0,0) to (n-1, n-1) tracking minimum steps.",
            "steps": [
                "DFS exploring 8 directions.",
                "Keep visited set; backtrack upon returning.",
                "Track minimum path."
            ],
            "time": "O(8^(n^2))",
            "space": "O(n^2)",
            "whySlow": "DFS explores all exponential paths instead of BFS finding shortest path in level 1.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public int shortestPathBinaryMatrix(int[][] grid) {
        int n = grid.length;
        if (grid[0][0] != 0 || grid[n - 1][n - 1] != 0) return -1;
        Queue<int[]> q = new LinkedList<>();
        q.offer(new int[]{0, 0, 1});
        grid[0][0] = 1;
        int[][] dirs = {
            {-1,-1},{-1,0},{-1,1},{0,-1},{0,1},{1,-1},{1,0},{1,1}
        };
        while (!q.isEmpty()) {
            int[] cur = q.poll();
            int r = cur[0], c = cur[1], d = cur[2];
            if (r == n - 1 && c == n - 1) return d;
            for (int[] dir : dirs) {
                int nr = r + dir[0], nc = c + dir[1];
                if (nr >= 0 && nr < n && nc >= 0 && nc < n && grid[nr][nc] == 0) {
                    grid[nr][nc] = 1;
                    q.offer(new int[]{nr, nc, d + 1});
                }
            }
        }
        return -1;
    }
}""",
                "python": """from collections import deque

class Solution:
    def shortestPathBinaryMatrix(self, grid: list[list[int]]) -> int:
        n = len(grid)
        if grid[0][0] != 0 or grid[n-1][n-1] != 0: return -1
        q = deque([(0, 0, 1)])
        grid[0][0] = 1
        dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        while q:
            r, c, d = q.popleft()
            if r == n - 1 and c == n - 1: return d
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                    grid[nr][nc] = 1
                    q.append((nr, nc, d + 1))
        return -1"""
            }
        },
        "optimal": {
            "idea": "BFS with in-place visited marking: start at (0, 0, dist=1); expand 8 neighbors; return dist immediately upon reaching (n-1, n-1).",
            "steps": [
                "If grid[0][0] == 1 || grid[n-1][n-1] == 1 return -1.",
                "Queue storing (r, c, dist).",
                "grid[0][0] = 1 (mark visited).",
                "Poll (r, c, dist): if r == n - 1 && c == n - 1 return dist.",
                "For 8 directions: if valid and cell == 0, mark 1 and enqueue."
            ],
            "time": "O(n^2)",
            "space": "O(n^2)",
            "code": {
                "java": """import java.util.*;
class Solution {
    public int shortestPathBinaryMatrix(int[][] grid) {
        int n = grid.length;
        if (grid[0][0] == 1 || grid[n - 1][n - 1] == 1) return -1;
        Queue<int[]> q = new LinkedList<>();
        q.offer(new int[]{0, 0, 1});
        grid[0][0] = 1;
        int[][] dirs = {
            {-1, -1}, {-1, 0}, {-1, 1},
            {0, -1},           {0, 1},
            {1, -1},  {1, 0},  {1, 1}
        };
        while (!q.isEmpty()) {
            int[] cur = q.poll();
            int r = cur[0], c = cur[1], d = cur[2];
            if (r == n - 1 && c == n - 1) return d;
            for (int[] dir : dirs) {
                int nr = r + dir[0], nc = c + dir[1];
                if (nr >= 0 && nr < n && nc >= 0 && nc < n && grid[nr][nc] == 0) {
                    grid[nr][nc] = 1;
                    q.offer(new int[]{nr, nc, d + 1});
                }
            }
        }
        return -1;
    }
}""",
                "python": """from collections import deque

class Solution:
    def shortestPathBinaryMatrix(self, grid: list[list[int]]) -> int:
        n = len(grid)
        if grid[0][0] == 1 or grid[n - 1][n - 1] == 1:
            return -1
        q = deque([(0, 0, 1)])
        grid[0][0] = 1
        dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        while q:
            r, c, d = q.popleft()
            if r == n - 1 and c == n - 1:
                return d
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                    grid[nr][nc] = 1
                    q.append((nr, nc, d + 1))
        return -1"""
            }
        }
    },
    # 206: Word Ladder
    {
        "seq": 206,
        "whyNext": "Shortest path on implicit graph: mutate 1 character (26 choices) to find valid next words in wordSet; bidirectional BFS.",
        "brute": {
            "idea": "Build full adjacency list graph comparing every pair of words with 1-character difference, then run BFS.",
            "steps": [
                "For each word pair (w1, w2), check if diff == 1 and add edge.",
                "Run standard BFS from beginWord to endWord."
            ],
            "time": "O(N^2 * L)",
            "space": "O(N^2)",
            "whySlow": "Constructs all pairwise edges in O(N^2 * L) where N can be 5000.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public int ladderLength(String beginWord, String endWord, List<String> wordList) {
        Set<String> wordSet = new HashSet<>(wordList);
        if (!wordSet.contains(endWord)) return 0;
        Queue<String> q = new LinkedList<>();
        q.offer(beginWord);
        int steps = 1;
        while (!q.isEmpty()) {
            int size = q.size();
            for (int k = 0; k < size; k++) {
                String cur = q.poll();
                if (cur.equals(endWord)) return steps;
                char[] chars = cur.toCharArray();
                for (int i = 0; i < chars.length; i++) {
                    char orig = chars[i];
                    for (char c = 'a'; c <= 'z'; c++) {
                        chars[i] = c;
                        String next = new String(chars);
                        if (wordSet.remove(next)) {
                            q.offer(next);
                        }
                    }
                    chars[i] = orig;
                }
            }
            steps++;
        }
        return 0;
    }
}""",
                "python": """from collections import deque

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: list[str]) -> int:
        words = set(wordList)
        if endWord not in words: return 0
        q = deque([(beginWord, 1)])
        while q:
            cur, steps = q.popleft()
            if cur == endWord: return steps
            for i in range(len(cur)):
                for c in "abcdefghijklmnopqrstuvwxyz":
                    nxt = cur[:i] + c + cur[i+1:]
                    if nxt in words:
                        words.remove(nxt)
                        q.append((nxt, steps + 1))
        return 0"""
            }
        },
        "optimal": {
            "idea": "Bidirectional BFS: expand from beginSet and endSet simultaneously; always expand the smaller frontier.",
            "steps": [
                "Set<String> beginSet, endSet, wordSet.",
                "If !wordSet.contains(endWord) return 0.",
                "While !beginSet.isEmpty() and !endSet.isEmpty():",
                "If beginSet.size() > endSet.size() swap sets.",
                "For each word, try all 26 character variations; if in endSet return steps + 1; if in wordSet add to nextLevel.",
                "steps++; beginSet = nextLevel."
            ],
            "time": "O(N * 26 * L)",
            "space": "O(N * L)",
            "code": {
                "java": """import java.util.*;
class Solution {
    public int ladderLength(String beginWord, String endWord, List<String> wordList) {
        Set<String> wordSet = new HashSet<>(wordList);
        if (!wordSet.contains(endWord)) return 0;
        Set<String> beginSet = new HashSet<>();
        Set<String> endSet = new HashSet<>();
        beginSet.add(beginWord);
        endSet.add(endWord);
        int steps = 1;
        while (!beginSet.isEmpty() && !endSet.isEmpty()) {
            if (beginSet.size() > endSet.size()) {
                Set<String> temp = beginSet;
                beginSet = endSet;
                endSet = temp;
            }
            Set<String> nextSet = new HashSet<>();
            for (String word : beginSet) {
                char[] chs = word.toCharArray();
                for (int i = 0; i < chs.length; i++) {
                    char old = chs[i];
                    for (char c = 'a'; c <= 'z'; c++) {
                        chs[i] = c;
                        String target = new String(chs);
                        if (endSet.contains(target)) return steps + 1;
                        if (wordSet.contains(target)) {
                            nextSet.add(target);
                            wordSet.remove(target);
                        }
                    }
                    chs[i] = old;
                }
            }
            beginSet = nextSet;
            steps++;
        }
        return 0;
    }
}""",
                "python": """class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: list[str]) -> int:
        word_set = set(wordList)
        if endWord not in word_set:
            return 0
        begin_set = {beginWord}
        end_set = {endWord}
        steps = 1
        while begin_set and end_set:
            if len(begin_set) > len(end_set):
                begin_set, end_set = end_set, begin_set
            next_set = set()
            for word in begin_set:
                for i in range(len(word)):
                    for c in "abcdefghijklmnopqrstuvwxyz":
                        nxt = word[:i] + c + word[i+1:]
                        if nxt in end_set:
                            return steps + 1
                        if nxt in word_set:
                            next_set.add(nxt)
                            word_set.remove(nxt)
            begin_set = next_set
            steps += 1
        return 0"""
            }
        }
    },
    # 207: Clone Graph
    {
        "seq": 207,
        "whyNext": "Graph deep copy: HashMap<Node, Node> maps original nodes to copies; BFS/DFS clones neighbors.",
        "brute": {
            "idea": "Two-pass traversal: first pass creates copies of all nodes; second pass copies neighbor edges.",
            "steps": [
                "Traverse graph with BFS creating Node copy for every original Node in a HashMap.",
                "Traverse again attaching copied neighbors."
            ],
            "time": "O(V + E)",
            "space": "O(V)",
            "whySlow": "Two full graph traversal passes instead of single-pass memoized DFS.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public Node cloneGraph(Node node) {
        if (node == null) return null;
        Map<Node, Node> map = new HashMap<>();
        Queue<Node> q = new LinkedList<>();
        q.offer(node);
        map.put(node, new Node(node.val));
        while (!q.isEmpty()) {
            Node cur = q.poll();
            for (Node neighbor : cur.neighbors) {
                if (!map.containsKey(neighbor)) {
                    map.put(neighbor, new Node(neighbor.val));
                    q.offer(neighbor);
                }
            }
        }
        for (Node orig : map.keySet()) {
            for (Node neighbor : orig.neighbors) {
                map.get(orig).neighbors.add(map.get(neighbor));
            }
        }
        return map.get(node);
    }
}""",
                "python": """class Solution:
    def cloneGraph(self, node: 'Node') -> 'Node':
        if not node: return None
        from collections import deque
        mapping = {node: Node(node.val)}
        q = deque([node])
        while q:
            cur = q.popleft()
            for neighbor in cur.neighbors:
                if neighbor not in mapping:
                    mapping[neighbor] = Node(neighbor.val)
                    q.append(neighbor)
        for orig, clone in mapping.items():
            clone.neighbors = [mapping[nbr] for nbr in orig.neighbors]
        return mapping[node]"""
            }
        },
        "optimal": {
            "idea": "Single-pass recursive DFS with Map<Node, Node>: if node already in map return clone; else create clone, put in map, recurse neighbors.",
            "steps": [
                "Map<Node, Node> visited = new HashMap<>();",
                "clone(node): if node == null return null.",
                "If visited.containsKey(node) return visited.get(node).",
                "Create Node clone = new Node(node.val); visited.put(node, clone).",
                "For neighbor in node.neighbors: clone.neighbors.add(clone(neighbor)).",
                "Return clone."
            ],
            "time": "O(V + E)",
            "space": "O(V)",
            "code": {
                "java": """import java.util.*;
class Solution {
    private Map<Node, Node> visited = new HashMap<>();
    public Node cloneGraph(Node node) {
        if (node == null) return null;
        if (visited.containsKey(node)) return visited.get(node);
        Node clone = new Node(node.val);
        visited.put(node, clone);
        for (Node neighbor : node.neighbors) {
            clone.neighbors.add(cloneGraph(neighbor));
        }
        return clone;
    }
}""",
                "python": """class Solution:
    def __init__(self):
        self.visited = {}

    def cloneGraph(self, node: 'Node') -> 'Node':
        if not node:
            return None
        if node in self.visited:
            return self.visited[node]
        clone = Node(node.val)
        self.visited[node] = clone
        clone.neighbors = [self.cloneGraph(neighbor) for neighbor in node.neighbors]
        return clone"""
            }
        }
    },
    # 208: Is Graph Bipartite?
    {
        "seq": 208,
        "whyNext": "2-coloring graph check: color each unvisited component with 1; adjacent nodes must have color -1; conflict => not bipartite.",
        "brute": {
            "idea": "Try all 2^V partitions of vertices into two sets and verify whether any edge connects two vertices in the same set.",
            "steps": [
                "Generate all subsets of vertices.",
                "Verify whether any subset is valid independent set."
            ],
            "time": "O(2^V * (V + E))",
            "space": "O(V)",
            "whySlow": "Exponential combination search.",
            "code": {
                "java": """class Solution {
    public boolean isBipartite(int[][] graph) {
        int n = graph.length;
        int[] color = new int[n];
        for (int i = 0; i < n; i++) {
            if (color[i] == 0 && !dfs(graph, i, 1, color)) {
                return false;
            }
        }
        return true;
    }
    private boolean dfs(int[][] g, int u, int c, int[] color) {
        color[u] = c;
        for (int v : g[u]) {
            if (color[v] == c) return false;
            if (color[v] == 0 && !dfs(g, v, -c, color)) return false;
        }
        return true;
    }
}""",
                "python": """class Solution:
    def isBipartite(self, graph: list[list[int]]) -> bool:
        color = {}
        for node in range(len(graph)):
            if node not in color:
                stack = [node]
                color[node] = 0
                while stack:
                    u = stack.pop()
                    for v in graph[u]:
                        if v not in color:
                            color[v] = 1 - color[u]
                            stack.append(v)
                        elif color[v] == color[u]:
                            return False
        return True"""
            }
        },
        "optimal": {
            "idea": "BFS/DFS 2-coloring: for each component, assign color 1 to start; assign -color to neighbors; return false if neighbor has same color.",
            "steps": [
                "int[] colors = new int[n] (0 unvisited, 1 color A, -1 color B).",
                "Loop through all vertices: if unvisited, launch BFS.",
                "Enqueue start with color 1.",
                "For each neighbor: if color == curColor return false; if uncolored, set color = -curColor and enqueue.",
                "Return true."
            ],
            "time": "O(V + E)",
            "space": "O(V)",
            "code": {
                "java": """import java.util.*;
class Solution {
    public boolean isBipartite(int[][] graph) {
        int n = graph.length;
        int[] color = new int[n];
        for (int i = 0; i < n; i++) {
            if (color[i] != 0) continue;
            Queue<Integer> q = new LinkedList<>();
            q.offer(i);
            color[i] = 1;
            while (!q.isEmpty()) {
                int u = q.poll();
                for (int v : graph[u]) {
                    if (color[v] == color[u]) return false;
                    if (color[v] == 0) {
                        color[v] = -color[u];
                        q.offer(v);
                    }
                }
            }
        }
        return true;
    }
}""",
                "python": """from collections import deque

class Solution:
    def isBipartite(self, graph: list[list[int]]) -> bool:
        n = len(graph)
        color = [0] * n
        for i in range(n):
            if color[i] != 0:
                continue
            q = deque([i])
            color[i] = 1
            while q:
                u = q.popleft()
                for v in graph[u]:
                    if color[v] == color[u]:
                        return False
                    if color[v] == 0:
                        color[v] = -color[u]
                        q.append(v)
        return True"""
            }
        }
    },
    # 209: Possible Bipartition
    {
        "seq": 209,
        "whyNext": "Builds on Is Graph Bipartite: dislikes edge list represents undirected conflict edges; verify if graph is 2-colorable.",
        "brute": {
            "idea": "Backtracking: assign each person to group 1 or group 2; backtrack if conflict detected.",
            "steps": [
                "Recursively assign each person to group 1 or 2.",
                "Check dislike edges."
            ],
            "time": "O(2^n)",
            "space": "O(n)",
            "whySlow": "Exponential assignment search.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public boolean possibleBipartition(int n, int[][] dislikes) {
        List<Integer>[] adj = new List[n + 1];
        for (int i = 1; i <= n; i++) adj[i] = new ArrayList<>();
        for (int[] d : dislikes) {
            adj[d[0]].add(d[1]);
            adj[d[1]].add(d[0]);
        }
        int[] color = new int[n + 1];
        for (int i = 1; i <= n; i++) {
            if (color[i] == 0 && !dfs(adj, i, 1, color)) return false;
        }
        return true;
    }
    private boolean dfs(List<Integer>[] adj, int u, int c, int[] color) {
        color[u] = c;
        for (int v : adj[u]) {
            if (color[v] == c) return false;
            if (color[v] == 0 && !dfs(adj, v, -c, color)) return false;
        }
        return true;
    }
}""",
                "python": """from collections import defaultdict

class Solution:
    def possibleBipartition(self, n: int, dislikes: list[list[int]]) -> bool:
        adj = defaultdict(list)
        for u, v in dislikes:
            adj[u].append(v)
            adj[v].append(u)
        color = {}
        for i in range(1, n + 1):
            if i not in color:
                color[i] = 1
                q = [i]
                while q:
                    u = q.pop()
                    for v in adj[u]:
                        if v in color:
                            if color[v] == color[u]: return False
                        else:
                            color[v] = -color[u]
                            q.append(v)
        return True"""
            }
        },
        "optimal": {
            "idea": "Build adjacency list from dislikes pairs; run BFS 2-coloring across all people 1..n.",
            "steps": [
                "Build adjacency list adj from dislikes (undirected edges).",
                "colors array of size n + 1.",
                "For i = 1..n: if uncolored, run BFS with color 1.",
                "If neighbor has same color, return false.",
                "Return true."
            ],
            "time": "O(V + E)",
            "space": "O(V + E)",
            "code": {
                "java": """import java.util.*;
class Solution {
    public boolean possibleBipartition(int n, int[][] dislikes) {
        List<Integer>[] adj = new List[n + 1];
        for (int i = 1; i <= n; i++) adj[i] = new ArrayList<>();
        for (int[] d : dislikes) {
            adj[d[0]].add(d[1]);
            adj[d[1]].add(d[0]);
        }
        int[] color = new int[n + 1];
        for (int i = 1; i <= n; i++) {
            if (color[i] != 0) continue;
            Queue<Integer> q = new LinkedList<>();
            q.offer(i);
            color[i] = 1;
            while (!q.isEmpty()) {
                int u = q.poll();
                for (int v : adj[u]) {
                    if (color[v] == color[u]) return false;
                    if (color[v] == 0) {
                        color[v] = -color[u];
                        q.offer(v);
                    }
                }
            }
        }
        return true;
    }
}""",
                "python": """from collections import deque, defaultdict

class Solution:
    def possibleBipartition(self, n: int, dislikes: list[list[int]]) -> bool:
        adj = defaultdict(list)
        for u, v in dislikes:
            adj[u].append(v)
            adj[v].append(u)
        color = [0] * (n + 1)
        for i in range(1, n + 1):
            if color[i] != 0:
                continue
            q = deque([i])
            color[i] = 1
            while q:
                u = q.popleft()
                for v in adj[u]:
                    if color[v] == color[u]:
                        return False
                    if color[v] == 0:
                        color[v] = -color[u]
                        q.append(v)
        return True"""
            }
        }
    },
    # 210: Keys and Rooms
    {
        "seq": 210,
        "whyNext": "Reachability from source 0: standard graph traversal visiting accessible rooms; check if visited count equals n.",
        "brute": {
            "idea": "Full BFS queue with visited boolean array.",
            "steps": [
                "Enqueue room 0.",
                "While queue is not empty, collect keys and enqueue unvisited rooms.",
                "Check if all rooms visited."
            ],
            "time": "O(V + E)",
            "space": "O(V)",
            "whySlow": "Standard BFS and DFS are both linear.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public boolean canVisitAllRooms(List<List<Integer>> rooms) {
        int n = rooms.size();
        boolean[] visited = new boolean[n];
        Queue<Integer> q = new LinkedList<>();
        q.offer(0);
        visited[0] = true;
        int count = 1;
        while (!q.isEmpty()) {
            int cur = q.poll();
            for (int key : rooms.get(cur)) {
                if (!visited[key]) {
                    visited[key] = true;
                    count++;
                    q.offer(key);
                }
            }
        }
        return count == n;
    }
}""",
                "python": """from collections import deque

class Solution:
    def canVisitAllRooms(self, rooms: list[list[int]]) -> bool:
        n = len(rooms)
        visited = {0}
        q = deque([0])
        while q:
            cur = q.popleft()
            for key in rooms[cur]:
                if key not in visited:
                    visited.add(key)
                    q.append(key)
        return len(visited) == n"""
            }
        },
        "optimal": {
            "idea": "Iterative DFS with Stack / boolean[] visited: start at 0, push adjacent keys; return visitedCount == n.",
            "steps": [
                "boolean[] visited = new boolean[n].",
                "Stack with 0; visited[0] = true; count = 1.",
                "While stack not empty: pop room, for each key: if not visited: mark visited, count++, push key.",
                "Return count == n."
            ],
            "time": "O(V + E)",
            "space": "O(V)",
            "code": {
                "java": """import java.util.*;
class Solution {
    public boolean canVisitAllRooms(List<List<Integer>> rooms) {
        int n = rooms.size();
        boolean[] visited = new boolean[n];
        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(0);
        visited[0] = true;
        int count = 1;
        while (!stack.isEmpty()) {
            int room = stack.pop();
            for (int key : rooms.get(room)) {
                if (!visited[key]) {
                    visited[key] = true;
                    count++;
                    stack.push(key);
                }
            }
        }
        return count == n;
    }
}""",
                "python": """class Solution:
    def canVisitAllRooms(self, rooms: list[list[int]]) -> bool:
        visited = set([0])
        stack = [0]
        while stack:
            room = stack.pop()
            for key in rooms[room]:
                if key not in visited:
                    visited.add(key)
                    stack.append(key)
        return len(visited) == len(rooms)"""
            }
        }
    },
    # 211: Number of Provinces
    {
        "seq": 211,
        "whyNext": "Adjacency matrix connected components: count unvisited vertices while launching DFS to visit entire province component.",
        "brute": {
            "idea": "Floyd-Warshall algorithm to compute reachability closure between all pairs; count distinct reachability equivalence classes.",
            "steps": [
                "Compute transitive closure of isConnected.",
                "Count unique rows."
            ],
            "time": "O(n^3)",
            "space": "O(n^2)",
            "whySlow": "Floyd-Warshall is cubic when DFS/BFS finds connected components in O(n^2).",
            "code": {
                "java": """class Solution {
    public int findCircleNum(int[][] isConnected) {
        int n = isConnected.length;
        boolean[] visited = new boolean[n];
        int count = 0;
        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                count++;
                dfs(isConnected, i, visited);
            }
        }
        return count;
    }
    private void dfs(int[][] g, int u, boolean[] visited) {
        visited[u] = true;
        for (int v = 0; v < g.length; v++) {
            if (g[u][v] == 1 && !visited[v]) {
                dfs(g, v, visited);
            }
        }
    }
}""",
                "python": """class Solution:
    def findCircleNum(self, isConnected: list[list[int]]) -> int:
        n = len(isConnected)
        visited = set()
        count = 0
        def dfs(u):
            visited.add(u)
            for v in range(n):
                if isConnected[u][v] and v not in visited:
                    dfs(v)
        for i in range(n):
            if i not in visited:
                count += 1
                dfs(i)
        return count"""
            }
        },
        "optimal": {
            "idea": "Simple boolean[] visited array + DFS: for each unvisited city, increment province count and DFS all connected cities.",
            "steps": [
                "boolean[] visited = new boolean[n].",
                "provinces = 0.",
                "For i from 0 to n - 1: if not visited[i]: provinces++, dfs(i).",
                "dfs(u): visited[u] = true; for v in 0..n-1: if isConnected[u][v] == 1 && !visited[v] dfs(v)."
            ],
            "time": "O(n^2)",
            "space": "O(n)",
            "code": {
                "java": """class Solution {
    public int findCircleNum(int[][] isConnected) {
        int n = isConnected.length;
        boolean[] visited = new boolean[n];
        int provinces = 0;
        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                provinces++;
                dfs(isConnected, i, visited);
            }
        }
        return provinces;
    }
    private void dfs(int[][] isConnected, int u, boolean[] visited) {
        visited[u] = true;
        for (int v = 0; v < isConnected.length; v++) {
            if (isConnected[u][v] == 1 && !visited[v]) {
                dfs(isConnected, v, visited);
            }
        }
    }
}""",
                "python": """class Solution:
    def findCircleNum(self, isConnected: list[list[int]]) -> int:
        n = len(isConnected)
        visited = [False] * n
        provinces = 0
        def dfs(u: int):
            visited[u] = True
            for v in range(n):
                if isConnected[u][v] == 1 and not visited[v]:
                    dfs(v)
        for i in range(n):
            if not visited[i]:
                provinces += 1
                dfs(i)
        return provinces"""
            }
        }
    },
    # 212: Find if Path Exists in Graph
    {
        "seq": 212,
        "whyNext": "Direct s-t connectivity: Union-Find (DSU) or BFS checks if source and destination belong to the same component.",
        "brute": {
            "idea": "Build adjacency list; perform DFS from source searching for destination.",
            "steps": [
                "Build adjacency graph.",
                "Run DFS from source to find destination."
            ],
            "time": "O(V + E)",
            "space": "O(V + E)",
            "whySlow": "Recursion stack limit can be reached on deep degenerate graphs.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public boolean validPath(int n, int[][] edges, int source, int destination) {
        if (source == destination) return true;
        List<Integer>[] adj = new List[n];
        for (int i = 0; i < n; i++) adj[i] = new ArrayList<>();
        for (int[] e : edges) {
            adj[e[0]].add(e[1]);
            adj[e[1]].add(e[0]);
        }
        boolean[] visited = new boolean[n];
        Queue<Integer> q = new LinkedList<>();
        q.offer(source);
        visited[source] = true;
        while (!q.isEmpty()) {
            int cur = q.poll();
            if (cur == destination) return true;
            for (int nxt : adj[cur]) {
                if (!visited[nxt]) {
                    visited[nxt] = true;
                    q.offer(nxt);
                }
            }
        }
        return false;
    }
}""",
                "python": """from collections import deque, defaultdict

class Solution:
    def validPath(self, n: int, edges: list[list[int]], source: int, destination: int) -> bool:
        if source == destination: return True
        adj = defaultdict(list)
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        q = deque([source])
        visited = {source}
        while q:
            cur = q.popleft()
            if cur == destination: return True
            for nxt in adj[cur]:
                if nxt not in visited:
                    visited.add(nxt)
                    q.append(nxt)
        return False"""
            }
        },
        "optimal": {
            "idea": "Disjoint Set Union (DSU) with path compression and union by rank: return find(source) == find(destination).",
            "steps": [
                "Initialize parent array where parent[i] = i.",
                "For each edge [u, v]: union(u, v).",
                "Return find(source) == find(destination)."
            ],
            "time": "O(V + E * alpha(V))",
            "space": "O(V)",
            "code": {
                "java": """class Solution {
    public boolean validPath(int n, int[][] edges, int source, int destination) {
        int[] parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
        for (int[] e : edges) {
            union(parent, e[0], e[1]);
        }
        return find(parent, source) == find(parent, destination);
    }
    private int find(int[] parent, int i) {
        if (parent[i] == i) return i;
        return parent[i] = find(parent, parent[i]);
    }
    private void union(int[] parent, int i, int j) {
        int rootI = find(parent, i);
        int rootJ = find(parent, j);
        if (rootI != rootJ) parent[rootI] = rootJ;
    }
}""",
                "python": """class Solution:
    def validPath(self, n: int, edges: list[list[int]], source: int, destination: int) -> bool:
        parent = list(range(n))
        def find(i):
            if parent[i] == i: return i
            parent[i] = find(parent[i])
            return parent[i]
        def union(i, j):
            root_i, root_j = find(i), find(j)
            if root_i != root_j:
                parent[root_i] = root_j
        for u, v in edges:
            union(u, v)
        return find(source) == find(destination)"""
            }
        }
    },
    # 213: All Paths From Source to Target
    {
        "seq": 213,
        "whyNext": "DAG path enumeration: directed acyclic graph allows backtracking without visited set (cannot cycle).",
        "brute": {
            "idea": "BFS queue storing all partial paths from 0 to n - 1.",
            "steps": [
                "Queue storing lists of paths.",
                "At each step, pop path, extend to all outgoing neighbors."
            ],
            "time": "O(2^n * n)",
            "space": "O(2^n * n)",
            "whySlow": "Allocates many intermediate lists in queue.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> allPathsSourceTarget(int[][] graph) {
        List<List<Integer>> res = new ArrayList<>();
        Queue<List<Integer>> q = new LinkedList<>();
        q.offer(Arrays.asList(0));
        int target = graph.length - 1;
        while (!q.isEmpty()) {
            List<Integer> path = q.poll();
            int last = path.get(path.size() - 1);
            if (last == target) {
                res.add(path);
                continue;
            }
            for (int next : graph[last]) {
                List<Integer> newPath = new ArrayList<>(path);
                newPath.add(next);
                q.offer(newPath);
            }
        }
        return res;
    }
}""",
                "python": """from collections import deque

class Solution:
    def allPathsSourceTarget(self, graph: list[list[int]]) -> list[list[int]]:
        target = len(graph) - 1
        q = deque([[0]])
        res = []
        while q:
            path = q.popleft()
            if path[-1] == target:
                res.append(path)
            else:
                for nxt in graph[path[-1]]:
                    q.append(path + [nxt])
        return res"""
            }
        },
        "optimal": {
            "idea": "Backtracking with single path list: DAG guarantees no cycles; append node, recurse, pop.",
            "steps": [
                "path list initialized with 0.",
                "In backtrack(node): if node == n - 1: add copy of path to res; return.",
                "For neighbor in graph[node]: path.add(neighbor), backtrack(neighbor), path.remove(size - 1)."
            ],
            "time": "O(2^n * n)",
            "space": "O(n)",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> allPathsSourceTarget(int[][] graph) {
        List<List<Integer>> res = new ArrayList<>();
        List<Integer> path = new ArrayList<>();
        path.add(0);
        dfs(graph, 0, path, res);
        return res;
    }
    private void dfs(int[][] graph, int node, List<Integer> path, List<List<Integer>> res) {
        if (node == graph.length - 1) {
            res.add(new ArrayList<>(path));
            return;
        }
        for (int next : graph[node]) {
            path.add(next);
            dfs(graph, next, path, res);
            path.remove(path.size() - 1);
        }
    }
}""",
                "python": """class Solution:
    def allPathsSourceTarget(self, graph: list[list[int]]) -> list[list[int]]:
        res = []
        path = [0]
        target = len(graph) - 1
        def dfs(node: int):
            if node == target:
                res.append(list(path))
                return
            for nxt in graph[node]:
                path.append(nxt)
                dfs(nxt)
                path.pop()
        dfs(0)
        return res"""
            }
        }
    },
    # 214: Shortest Bridge
    {
        "seq": 214,
        "whyNext": "Two-phase graph algorithm: DFS identifies and enqueues all cells of the first island; multi-source BFS expands to find the second island.",
        "brute": {
            "idea": "Collect all cells of island 1 and all cells of island 2; find min Manhattan distance between all pairs.",
            "steps": [
                "DFS to extract coordinates of island 1.",
                "DFS to extract coordinates of island 2.",
                "Check |r1 - r2| + |c1 - c2| - 1 for all pairs."
            ],
            "time": "O(I1 * I2)",
            "space": "O(n^2)",
            "whySlow": "Pairwise distance comparison costs up to O(n^4).",
            "code": {
                "java": """import java.util.*;
class Solution {
    public int shortestBridge(int[][] grid) {
        int n = grid.length;
        List<int[]> island1 = new ArrayList<>();
        List<int[]> island2 = new ArrayList<>();
        boolean found = false;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 1) {
                    if (!found) {
                        dfs(grid, i, j, island1);
                        found = true;
                    } else if (grid[i][j] == 1) {
                        dfs(grid, i, j, island2);
                    }
                }
            }
        }
        int minD = Integer.MAX_VALUE;
        for (int[] p1 : island1) {
            for (int[] p2 : island2) {
                minD = Math.min(minD, Math.abs(p1[0] - p2[0]) + Math.abs(p1[1] - p2[1]) - 1);
            }
        }
        return minD;
    }
    private void dfs(int[][] g, int r, int c, List<int[]> list) {
        if (r < 0 || r >= g.length || c < 0 || c >= g.length || g[r][c] != 1) return;
        g[r][c] = 2;
        list.add(new int[]{r, c});
        dfs(g, r + 1, c, list);
        dfs(g, r - 1, c, list);
        dfs(g, r, c + 1, list);
        dfs(g, r, c - 1, list);
    }
}""",
                "python": """class Solution:
    def shortestBridge(self, grid: list[list[int]]) -> int:
        n = len(grid)
        i1, i2 = [], []
        found = False
        def dfs(r, c, lst):
            if not (0 <= r < n and 0 <= c < n) or grid[r][c] != 1: return
            grid[r][c] = 2
            lst.append((r, c))
            dfs(r+1, c, lst); dfs(r-1, c, lst); dfs(r, c+1, lst); dfs(r, c-1, lst)
        for i in range(n):
            for j in range(n):
                if grid[i][j] == 1:
                    if not found:
                        dfs(i, j, i1)
                        found = True
                    else:
                        dfs(i, j, i2)
        return min(abs(r1-r2) + abs(c1-c2) - 1 for r1, c1 in i1 for r2, c2 in i2)"""
            }
        },
        "optimal": {
            "idea": "DFS to color first island 2 and add all cells to BFS queue; multi-source BFS expands layers until reaching a cell with 1.",
            "steps": [
                "Find first '1' cell and DFS all its connected cells, mutating to 2 and offering to queue.",
                "Run BFS by levels: for each popped cell, check 4 neighbors.",
                "If neighbor is 1, return current distance steps.",
                "If neighbor is 0, mark 2 and enqueue.",
                "Increment steps after each level."
            ],
            "time": "O(n^2)",
            "space": "O(n^2)",
            "code": {
                "java": """import java.util.*;
class Solution {
    public int shortestBridge(int[][] grid) {
        int n = grid.length;
        Queue<int[]> q = new LinkedList<>();
        boolean found = false;
        for (int i = 0; i < n && !found; i++) {
            for (int j = 0; j < n && !found; j++) {
                if (grid[i][j] == 1) {
                    dfs(grid, i, j, n, q);
                    found = true;
                }
            }
        }
        int steps = 0;
        int[][] dirs = {{1,0}, {-1,0}, {0,1}, {0,-1}};
        while (!q.isEmpty()) {
            int size = q.size();
            for (int k = 0; k < size; k++) {
                int[] cur = q.poll();
                for (int[] d : dirs) {
                    int nr = cur[0] + d[0], nc = cur[1] + d[1];
                    if (nr >= 0 && nr < n && nc >= 0 && nc < n) {
                        if (grid[nr][nc] == 1) return steps;
                        if (grid[nr][nc] == 0) {
                            grid[nr][nc] = 2;
                            q.offer(new int[]{nr, nc});
                        }
                    }
                }
            }
            steps++;
        }
        return -1;
    }
    private void dfs(int[][] g, int r, int c, int n, Queue<int[]> q) {
        if (r < 0 || r >= n || c < 0 || c >= n || g[r][c] != 1) return;
        g[r][c] = 2;
        q.offer(new int[]{r, c});
        dfs(g, r + 1, c, n, q);
        dfs(g, r - 1, c, n, q);
        dfs(g, r, c + 1, n, q);
        dfs(g, r, c - 1, n, q);
    }
}""",
                "python": """from collections import deque

class Solution:
    def shortestBridge(self, grid: list[list[int]]) -> int:
        n = len(grid)
        q = deque()
        found = False
        def dfs(r, c):
            if not (0 <= r < n and 0 <= c < n) or grid[r][c] != 1: return
            grid[r][c] = 2
            q.append((r, c))
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)
        for i in range(n):
            if found: break
            for j in range(n):
                if grid[i][j] == 1:
                    dfs(i, j)
                    found = True
                    break
        steps = 0
        while q:
            for _ in range(len(q)):
                r, c = q.popleft()
                for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n:
                        if grid[nr][nc] == 1:
                            return steps
                        if grid[nr][nc] == 0:
                            grid[nr][nc] = 2
                            q.append((nr, nc))
            steps += 1
        return -1"""
            }
        }
    },
    # 215: Evaluate Division
    {
        "seq": 215,
        "whyNext": "Weighted directed graph: a/b = k is edge a -> b with weight k, b -> a with weight 1/k; answer queries via path product.",
        "brute": {
            "idea": "Floyd-Warshall algorithm to compute all-pairs multiplicative transitive closure.",
            "steps": [
                "Map unique variables to indices 0..V-1.",
                "Initialize dist[V][V] with -1, dist[i][i] = 1.",
                "For k, i, j: if dist[i][k] > 0 && dist[k][j] > 0, dist[i][j] = dist[i][k] * dist[k][j]."
            ],
            "time": "O(V^3 + Q)",
            "space": "O(V^2)",
            "whySlow": "Computes all V^3 pairs when queries only ask for a few specific paths.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public double[] calcEquation(List<List<String>> equations, double[] values, List<List<String>> queries) {
        Map<String, Map<String, Double>> g = new HashMap<>();
        for (int i = 0; i < equations.size(); i++) {
            String u = equations.get(i).get(0), v = equations.get(i).get(1);
            double val = values[i];
            g.computeIfAbsent(u, k -> new HashMap<>()).put(v, val);
            g.computeIfAbsent(v, k -> new HashMap<>()).put(u, 1.0 / val);
        }
        double[] res = new double[queries.size()];
        for (int i = 0; i < queries.size(); i++) {
            String u = queries.get(i).get(0), v = queries.get(i).get(1);
            if (!g.containsKey(u) || !g.containsKey(v)) res[i] = -1.0;
            else if (u.equals(v)) res[i] = 1.0;
            else res[i] = dfs(g, u, v, 1.0, new HashSet<>());
        }
        return res;
    }
    private double dfs(Map<String, Map<String, Double>> g, String cur, String target, double p, Set<String> visited) {
        visited.add(cur);
        if (cur.equals(target)) return p;
        for (String next : g.get(cur).keySet()) {
            if (!visited.contains(next)) {
                double ans = dfs(g, next, target, p * g.get(cur).get(next), visited);
                if (ans != -1.0) return ans;
            }
        }
        return -1.0;
    }
}""",
                "python": """from collections import defaultdict

class Solution:
    def calcEquation(self, equations: list[list[str]], values: list[float], queries: list[list[str]]) -> list[float]:
        g = defaultdict(dict)
        for (u, v), val in zip(equations, values):
            g[u][v] = val
            g[v][u] = 1.0 / val
        def dfs(cur, target, visited):
            if cur not in g or target not in g: return -1.0
            if cur == target: return 1.0
            visited.add(cur)
            for nxt, weight in g[cur].items():
                if nxt not in visited:
                    res = dfs(nxt, target, visited)
                    if res != -1.0: return res * weight
            return -1.0
        return [dfs(q[0], q[1], set()) for q in queries]"""
            }
        },
        "optimal": {
            "idea": "DFS path product with visited set per query: walk from query[0] to query[1] accumulating product along edges in O(V + E) per query.",
            "steps": [
                "Build graph: Map<String, Map<String, Double>> g.",
                "For query [u, v]: if u or v not in graph, return -1.0.",
                "Run DFS with visited Set accumulating running product.",
                "Return accumulated product if path reached, else -1.0."
            ],
            "time": "O(Q * (V + E))",
            "space": "O(V + E)",
            "code": {
                "java": """import java.util.*;
class Solution {
    public double[] calcEquation(List<List<String>> equations, double[] values, List<List<String>> queries) {
        Map<String, Map<String, Double>> graph = new HashMap<>();
        for (int i = 0; i < equations.size(); i++) {
            String u = equations.get(i).get(0);
            String v = equations.get(i).get(1);
            double val = values[i];
            graph.computeIfAbsent(u, k -> new HashMap<>()).put(v, val);
            graph.computeIfAbsent(v, k -> new HashMap<>()).put(u, 1.0 / val);
        }
        double[] res = new double[queries.size()];
        for (int i = 0; i < queries.size(); i++) {
            String start = queries.get(i).get(0);
            String end = queries.get(i).get(1);
            if (!graph.containsKey(start) || !graph.containsKey(end)) {
                res[i] = -1.0;
            } else if (start.equals(end)) {
                res[i] = 1.0;
            } else {
                res[i] = dfs(graph, start, end, 1.0, new HashSet<>());
            }
        }
        return res;
    }
    private double dfs(Map<String, Map<String, Double>> g, String cur, String target, double product, Set<String> visited) {
        visited.add(cur);
        if (cur.equals(target)) return product;
        for (Map.Entry<String, Double> edge : g.get(cur).entrySet()) {
            if (!visited.contains(edge.getKey())) {
                double sub = dfs(g, edge.getKey(), target, product * edge.getValue(), visited);
                if (sub != -1.0) return sub;
            }
        }
        return -1.0;
    }
}""",
                "python": """from collections import defaultdict

class Solution:
    def calcEquation(self, equations: list[list[str]], values: list[float], queries: list[list[str]]) -> list[float]:
        graph = defaultdict(dict)
        for (u, v), val in zip(equations, values):
            graph[u][v] = val
            graph[v][u] = 1.0 / val
        def dfs(cur: str, target: str, product: float, visited: set) -> float:
            if cur == target:
                return product
            visited.add(cur)
            for nxt, weight in graph[cur].items():
                if nxt not in visited:
                    res = dfs(nxt, target, product * weight, visited)
                    if res != -1.0:
                        return res
            return -1.0
        ans = []
        for u, v in queries:
            if u not in graph or v not in graph:
                ans.append(-1.0)
            elif u == v:
                ans.append(1.0)
            else:
                ans.append(dfs(u, v, 1.0, set()))
        return ans"""
            }
        }
    },
    # 216: Open the Lock
    {
        "seq": 216,
        "whyNext": "Shortest path on 10,000 state combination lock: bidirectional BFS from '0000' to target avoiding deadends.",
        "brute": {
            "idea": "Single-direction BFS from '0000' expanding 8 wheel moves (+1/-1 on 4 wheels) avoiding deadends.",
            "steps": [
                "Queue with '0000', distance 0.",
                "Expand 8 neighbors.",
                "Return distance when target reached."
            ],
            "time": "O(10^4)",
            "space": "O(10^4)",
            "whySlow": "Single-direction BFS explores a wider search sphere than bidirectional BFS.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public int openLock(String[] deadends, String target) {
        Set<String> dead = new HashSet<>(Arrays.asList(deadends));
        if (dead.contains("0000")) return -1;
        Queue<String> q = new LinkedList<>();
        q.offer("0000");
        dead.add("0000");
        int steps = 0;
        while (!q.isEmpty()) {
            int size = q.size();
            for (int k = 0; k < size; k++) {
                String cur = q.poll();
                if (cur.equals(target)) return steps;
                for (String next : getNeighbors(cur)) {
                    if (!dead.contains(next)) {
                        dead.add(next);
                        q.offer(next);
                    }
                }
            }
            steps++;
        }
        return -1;
    }
    private List<String> getNeighbors(String s) {
        List<String> res = new ArrayList<>();
        char[] chs = s.toCharArray();
        for (int i = 0; i < 4; i++) {
            char orig = chs[i];
            chs[i] = (char) ((orig - '0' + 1) % 10 + '0');
            res.add(new String(chs));
            chs[i] = (char) ((orig - '0' + 9) % 10 + '0');
            res.add(new String(chs));
            chs[i] = orig;
        }
        return res;
    }
}""",
                "python": """from collections import deque

class Solution:
    def openLock(self, deadends: list[str], target: str) -> int:
        dead = set(deadends)
        if "0000" in dead: return -1
        q = deque([("0000", 0)])
        dead.add("0000")
        while q:
            cur, d = q.popleft()
            if cur == target: return d
            for i in range(4):
                digit = int(cur[i])
                for diff in (1, -1):
                    nxt_digit = (digit + diff) % 10
                    nxt = cur[:i] + str(nxt_digit) + cur[i+1:]
                    if nxt not in dead:
                        dead.add(nxt)
                        q.append((nxt, d + 1))
        return -1"""
            }
        },
        "optimal": {
            "idea": "Bidirectional BFS: expand from startSet {'0000'} and endSet {target}; meets in the middle, reducing states explored.",
            "steps": [
                "Set<String> dead, beginSet, endSet.",
                "If dead.contains('0000') || dead.contains(target) return -1.",
                "While !beginSet.isEmpty() and !endSet.isEmpty(): swap to smaller set.",
                "For each code: generate 8 neighbors. If in endSet return steps + 1; if not dead add to nextLevel.",
                "steps++; beginSet = nextLevel."
            ],
            "time": "O(10^4)",
            "space": "O(10^4)",
            "code": {
                "java": """import java.util.*;
class Solution {
    public int openLock(String[] deadends, String target) {
        Set<String> dead = new HashSet<>(Arrays.asList(deadends));
        if (dead.contains("0000") || dead.contains(target)) return -1;
        if (target.equals("0000")) return 0;
        Set<String> beginSet = new HashSet<>();
        Set<String> endSet = new HashSet<>();
        beginSet.add("0000");
        endSet.add(target);
        int steps = 0;
        while (!beginSet.isEmpty() && !endSet.isEmpty()) {
            if (beginSet.size() > endSet.size()) {
                Set<String> temp = beginSet;
                beginSet = endSet;
                endSet = temp;
            }
            Set<String> nextSet = new HashSet<>();
            for (String cur : beginSet) {
                for (String next : getNeighbors(cur)) {
                    if (endSet.contains(next)) return steps + 1;
                    if (!dead.contains(next)) {
                        dead.add(next);
                        nextSet.add(next);
                    }
                }
            }
            beginSet = nextSet;
            steps++;
        }
        return -1;
    }
    private List<String> getNeighbors(String s) {
        List<String> res = new ArrayList<>();
        char[] chs = s.toCharArray();
        for (int i = 0; i < 4; i++) {
            char orig = chs[i];
            chs[i] = (char) ((orig - '0' + 1) % 10 + '0');
            res.add(new String(chs));
            chs[i] = (char) ((orig - '0' + 9) % 10 + '0');
            res.add(new String(chs));
            chs[i] = orig;
        }
        return res;
    }
}""",
                "python": """class Solution:
    def openLock(self, deadends: list[str], target: str) -> int:
        dead = set(deadends)
        if "0000" in dead or target in dead:
            return -1
        if target == "0000":
            return 0
        begin_set = {"0000"}
        end_set = {target}
        steps = 0
        while begin_set and end_set:
            if len(begin_set) > len(end_set):
                begin_set, end_set = end_set, begin_set
            next_set = set()
            for cur in begin_set:
                for i in range(4):
                    digit = int(cur[i])
                    for diff in (1, -1):
                        nxt = cur[:i] + str((digit + diff) % 10) + cur[i+1:]
                        if nxt in end_set:
                            return steps + 1
                        if nxt not in dead:
                            dead.add(nxt)
                            next_set.add(nxt)
            begin_set = next_set
            steps += 1
        return -1"""
            }
        }
    },
    # 217: Minimum Height Trees
    {
        "seq": 217,
        "whyNext": "Graph topological peeling: repeatedly remove degree-1 leaf nodes; centroids of tree (at most 2 nodes) remain.",
        "brute": {
            "idea": "For every node i from 0 to n - 1, calculate tree height using BFS; return nodes achieving minimum height.",
            "steps": [
                "For each node, run BFS to compute max depth.",
                "Find minimum depth across all nodes and collect best roots."
            ],
            "time": "O(V * (V + E))",
            "space": "O(V + E)",
            "whySlow": "Runs full BFS from every vertex in O(V^2).",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<Integer> findMinHeightTrees(int n, int[][] edges) {
        if (n <= 2) {
            List<Integer> res = new ArrayList<>();
            for (int i = 0; i < n; i++) res.add(i);
            return res;
        }
        List<Set<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new HashSet<>());
        for (int[] e : edges) {
            adj.get(e[0]).add(e[1]);
            adj.get(e[1]).add(e[0]);
        }
        List<Integer> leaves = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            if (adj.get(i).size() == 1) leaves.add(i);
        }
        int remaining = n;
        while (remaining > 2) {
            remaining -= leaves.size();
            List<Integer> newLeaves = new ArrayList<>();
            for (int leaf : leaves) {
                int neighbor = adj.get(leaf).iterator().next();
                adj.get(neighbor).remove(leaf);
                if (adj.get(neighbor).size() == 1) newLeaves.add(neighbor);
            }
            leaves = newLeaves;
        }
        return leaves;
    }
}""",
                "python": """class Solution:
    def findMinHeightTrees(self, n: int, edges: list[list[int]]) -> list[int]:
        if n <= 2: return list(range(n))
        adj = [set() for _ in range(n)]
        for u, v in edges:
            adj[u].add(v)
            adj[v].add(u)
        leaves = [i for i in range(n) if len(adj[i]) == 1]
        rem = n
        while rem > 2:
            rem -= len(leaves)
            new_leaves = []
            for leaf in leaves:
                nbr = adj[leaf].pop()
                adj[nbr].remove(leaf)
                if len(adj[nbr]) == 1:
                    new_leaves.append(nbr)
            leaves = new_leaves
        return leaves"""
            }
        },
        "optimal": {
            "idea": "Topological leaf trimming: trim leaves (degree == 1) layer by layer until <= 2 nodes remain; remaining nodes are the centroids (MHT roots).",
            "steps": [
                "If n <= 2 return [0..n-1].",
                "Build adjacency list and degree array.",
                "Collect all nodes with degree == 1 in leaves queue.",
                "While remainingNodes > 2: decrement remainingNodes by leaves.size(); for each leaf, decrement neighbor degrees; if neighbor degree becomes 1, enqueue."
            ],
            "time": "O(V + E)",
            "space": "O(V + E)",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<Integer> findMinHeightTrees(int n, int[][] edges) {
        if (n <= 2) {
            List<Integer> res = new ArrayList<>();
            for (int i = 0; i < n; i++) res.add(i);
            return res;
        }
        List<Set<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new HashSet<>());
        for (int[] e : edges) {
            adj.get(e[0]).add(e[1]);
            adj.get(e[1]).add(e[0]);
        }
        List<Integer> leaves = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            if (adj.get(i).size() == 1) leaves.add(i);
        }
        int remaining = n;
        while (remaining > 2) {
            remaining -= leaves.size();
            List<Integer> newLeaves = new ArrayList<>();
            for (int leaf : leaves) {
                int neighbor = adj.get(leaf).iterator().next();
                adj.get(neighbor).remove(leaf);
                if (adj.get(neighbor).size() == 1) {
                    newLeaves.add(neighbor);
                }
            }
            leaves = newLeaves;
        }
        return leaves;
    }
}""",
                "python": """class Solution:
    def findMinHeightTrees(self, n: int, edges: list[list[int]]) -> list[int]:
        if n <= 2:
            return list(range(n))
        adj = [set() for _ in range(n)]
        for u, v in edges:
            adj[u].add(v)
            adj[v].add(u)
        leaves = [i for i in range(n) if len(adj[i]) == 1]
        remaining = n
        while remaining > 2:
            remaining -= len(leaves)
            new_leaves = []
            for leaf in leaves:
                neighbor = adj[leaf].pop()
                adj[neighbor].remove(leaf)
                if len(adj[neighbor]) == 1:
                    new_leaves.append(neighbor)
            leaves = new_leaves
        return leaves"""
            }
        }
    },
    # 218: Course Schedule
    {
        "seq": 218,
        "whyNext": "Directed cycle detection / topological sort (Kahn's algorithm): if all courses processed (inDegree == 0), graph is DAG.",
        "brute": {
            "idea": "DFS from each node tracking path to detect back-edges.",
            "steps": [
                "From each unvisited course, run DFS.",
                "If node already in current path, cycle exists."
            ],
            "time": "O(V + E)",
            "space": "O(V + E)",
            "whySlow": "Recursive call stack can overflow on long graphs.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public boolean canFinish(int numCourses, int[][] prerequisites) {
        List<Integer>[] adj = new List[numCourses];
        for (int i = 0; i < numCourses; i++) adj[i] = new ArrayList<>();
        for (int[] p : prerequisites) adj[p[1]].add(p[0]);
        int[] visited = new int[numCourses];
        for (int i = 0; i < numCourses; i++) {
            if (visited[i] == 0 && hasCycle(adj, i, visited)) return false;
        }
        return true;
    }
    private boolean hasCycle(List<Integer>[] adj, int u, int[] visited) {
        visited[u] = 1;
        for (int v : adj[u]) {
            if (visited[v] == 1) return true;
            if (visited[v] == 0 && hasCycle(adj, v, visited)) return true;
        }
        visited[u] = 2;
        return false;
    }
}""",
                "python": """from collections import defaultdict

class Solution:
    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:
        adj = defaultdict(list)
        for dest, src in prerequisites:
            adj[src].append(dest)
        visited = [0] * numCourses
        def dfs(u):
            visited[u] = 1
            for v in adj[u]:
                if visited[v] == 1: return True
                if visited[v] == 0 and dfs(v): return True
            visited[u] = 2
            return False
        for i in range(numCourses):
            if visited[i] == 0 and dfs(i): return False
        return True"""
            }
        },
        "optimal": {
            "idea": "Kahn's Algorithm (BFS topological sort): inDegree array; push all inDegree == 0 courses into queue; decrement neighbor inDegrees; check count == numCourses.",
            "steps": [
                "int[] inDegree = new int[numCourses]; build adjacency list adj.",
                "For [course, pre] in prerequisites: adj[pre].add(course), inDegree[course]++.",
                "Queue with all courses having inDegree == 0.",
                "While queue not empty: poll u, count++, for v in adj[u]: if (--inDegree[v] == 0) q.offer(v).",
                "Return count == numCourses."
            ],
            "time": "O(V + E)",
            "space": "O(V + E)",
            "code": {
                "java": """import java.util.*;
class Solution {
    public boolean canFinish(int numCourses, int[][] prerequisites) {
        int[] inDegree = new int[numCourses];
        List<Integer>[] adj = new List[numCourses];
        for (int i = 0; i < numCourses; i++) adj[i] = new ArrayList<>();
        for (int[] p : prerequisites) {
            adj[p[1]].add(p[0]);
            inDegree[p[0]]++;
        }
        Queue<Integer> q = new LinkedList<>();
        for (int i = 0; i < numCourses; i++) {
            if (inDegree[i] == 0) q.offer(i);
        }
        int count = 0;
        while (!q.isEmpty()) {
            int u = q.poll();
            count++;
            for (int v : adj[u]) {
                if (--inDegree[v] == 0) {
                    q.offer(v);
                }
            }
        }
        return count == numCourses;
    }
}""",
                "python": """from collections import deque, defaultdict

class Solution:
    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:
        in_degree = [0] * numCourses
        adj = defaultdict(list)
        for dest, src in prerequisites:
            adj[src].append(dest)
            in_degree[dest] += 1
        q = deque([i for i in range(numCourses) if in_degree[i] == 0])
        count = 0
        while q:
            u = q.popleft()
            count += 1
            for v in adj[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    q.append(v)
        return count == numCourses"""
            }
        }
    },
    # 219: Course Schedule II
    {
        "seq": 219,
        "whyNext": "Builds on Course Schedule: record the order in which inDegree == 0 courses are popped; return array or empty array if cycle.",
        "brute": {
            "idea": "Post-order DFS topological sort: prepend to list upon finishing children; reverse if no cycle.",
            "steps": [
                "Run 3-state DFS cycle detection.",
                "Accumulate finish times in reverse order."
            ],
            "time": "O(V + E)",
            "space": "O(V + E)",
            "whySlow": "Recursive call stack overhead compared to iterative Kahn's algorithm.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public int[] findOrder(int numCourses, int[][] prerequisites) {
        List<Integer>[] adj = new List[numCourses];
        for (int i = 0; i < numCourses; i++) adj[i] = new ArrayList<>();
        for (int[] p : prerequisites) adj[p[1]].add(p[0]);
        int[] visited = new int[numCourses];
        List<Integer> order = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) {
            if (visited[i] == 0 && dfs(adj, i, visited, order)) return new int[0];
        }
        Collections.reverse(order);
        int[] res = new int[numCourses];
        for (int i = 0; i < numCourses; i++) res[i] = order.get(i);
        return res;
    }
    private boolean dfs(List<Integer>[] adj, int u, int[] visited, List<Integer> order) {
        visited[u] = 1;
        for (int v : adj[u]) {
            if (visited[v] == 1) return true;
            if (visited[v] == 0 && dfs(adj, v, visited, order)) return true;
        }
        visited[u] = 2;
        order.add(u);
        return false;
    }
}""",
                "python": """from collections import defaultdict

class Solution:
    def findOrder(self, numCourses: int, prerequisites: list[list[int]]) -> list[int]:
        adj = defaultdict(list)
        for dest, src in prerequisites:
            adj[src].append(dest)
        visited = [0] * numCourses
        order = []
        def dfs(u):
            visited[u] = 1
            for v in adj[u]:
                if visited[v] == 1: return True
                if visited[v] == 0 and dfs(v): return True
            visited[u] = 2
            order.append(u)
            return False
        for i in range(numCourses):
            if visited[i] == 0 and dfs(i): return []
        return order[::-1]"""
            }
        },
        "optimal": {
            "idea": "Kahn's BFS: store each popped course directly into result array res[idx++]. If idx == numCourses return res; else return empty array.",
            "steps": [
                "int[] order = new int[numCourses], inDegree = new int[numCourses].",
                "Queue with inDegree == 0 courses.",
                "int idx = 0; while queue not empty: u = poll(), order[idx++] = u.",
                "For v in adj[u]: if (--inDegree[v] == 0) q.offer(v).",
                "Return idx == numCourses ? order : new int[0]."
            ],
            "time": "O(V + E)",
            "space": "O(V + E)",
            "code": {
                "java": """import java.util.*;
class Solution {
    public int[] findOrder(int numCourses, int[][] prerequisites) {
        int[] inDegree = new int[numCourses];
        List<Integer>[] adj = new List[numCourses];
        for (int i = 0; i < numCourses; i++) adj[i] = new ArrayList<>();
        for (int[] p : prerequisites) {
            adj[p[1]].add(p[0]);
            inDegree[p[0]]++;
        }
        Queue<Integer> q = new LinkedList<>();
        for (int i = 0; i < numCourses; i++) {
            if (inDegree[i] == 0) q.offer(i);
        }
        int[] order = new int[numCourses];
        int idx = 0;
        while (!q.isEmpty()) {
            int u = q.poll();
            order[idx++] = u;
            for (int v : adj[u]) {
                if (--inDegree[v] == 0) {
                    q.offer(v);
                }
            }
        }
        return idx == numCourses ? order : new int[0];
    }
}""",
                "python": """from collections import deque, defaultdict

class Solution:
    def findOrder(self, numCourses: int, prerequisites: list[list[int]]) -> list[int]:
        in_degree = [0] * numCourses
        adj = defaultdict(list)
        for dest, src in prerequisites:
            adj[src].append(dest)
            in_degree[dest] += 1
        q = deque([i for i in range(numCourses) if in_degree[i] == 0])
        order = []
        while q:
            u = q.popleft()
            order.append(u)
            for v in adj[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    q.append(v)
        return order if len(order) == numCourses else []"""
            }
        }
    },
    # 220: Find Eventual Safe States
    {
        "seq": 220,
        "whyNext": "Terminal state reachability: 3-state coloring (0 unvisited, 1 visiting, 2 safe); nodes not in any cycle are safe.",
        "brute": {
            "idea": "Reverse all edges, start from terminal nodes (outDegree == 0), and run Kahn's algorithm backwards.",
            "steps": [
                "Build reversed graph and inDegrees.",
                "Enqueue initial terminal nodes; peel backwards."
            ],
            "time": "O(V + E)",
            "space": "O(V + E)",
            "whySlow": "Allocating reverse graph takes extra memory compared to in-place DFS 3-coloring.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<Integer> eventualSafeNodes(int[][] graph) {
        int n = graph.length;
        int[] color = new int[n];
        List<Integer> res = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            if (isSafe(graph, i, color)) res.add(i);
        }
        return res;
    }
    private boolean isSafe(int[][] g, int u, int[] color) {
        if (color[u] != 0) return color[u] == 2;
        color[u] = 1;
        for (int v : g[u]) {
            if (!isSafe(g, v, color)) return false;
        }
        color[u] = 2;
        return true;
    }
}""",
                "python": """class Solution:
    def eventualSafeNodes(self, graph: list[list[int]]) -> list[int]:
        n = len(graph)
        color = [0] * n
        def is_safe(u):
            if color[u] != 0: return color[u] == 2
            color[u] = 1
            for v in graph[u]:
                if not is_safe(v): return False
            color[u] = 2
            return True
        return [i for i in range(n) if is_safe(i)]"""
            }
        },
        "optimal": {
            "idea": "3-state coloring DFS: color[u] = 0 (unvisited), 1 (visiting/in cycle), 2 (safe). If any branch hits state 1, it is unsafe.",
            "steps": [
                "int[] color = new int[n];",
                "dfs(u): if color[u] != 0 return color[u] == 2.",
                "color[u] = 1; for v in graph[u]: if !dfs(v) return false.",
                "color[u] = 2; return true.",
                "Loop i from 0 to n - 1: if dfs(i) add i to res."
            ],
            "time": "O(V + E)",
            "space": "O(V)",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<Integer> eventualSafeNodes(int[][] graph) {
        int n = graph.length;
        int[] color = new int[n];
        List<Integer> safe = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            if (dfs(graph, i, color)) {
                safe.add(i);
            }
        }
        return safe;
    }
    private boolean dfs(int[][] graph, int u, int[] color) {
        if (color[u] != 0) return color[u] == 2;
        color[u] = 1;
        for (int v : graph[u]) {
            if (!dfs(graph, v, color)) return false;
        }
        color[u] = 2;
        return true;
    }
}""",
                "python": """class Solution:
    def eventualSafeNodes(self, graph: list[list[int]]) -> list[int]:
        n = len(graph)
        color = [0] * n
        def dfs(u: int) -> bool:
            if color[u] != 0:
                return color[u] == 2
            color[u] = 1
            for v in graph[u]:
                if not dfs(v):
                    return False
            color[u] = 2
            return True
        return [i for i in range(n) if dfs(i)]"""
            }
        }
    },
    # 221: Longest Increasing Path in a Matrix
    {
        "seq": 221,
        "whyNext": "Grid DAG with memoization: strictly increasing paths are acyclic; memo[r][c] = 1 + max(neighbors with higher value).",
        "brute": {
            "idea": "Brute force DFS from every cell without memoization.",
            "steps": [
                "For every cell, explore all strictly increasing paths.",
                "Track maximum path length."
            ],
            "time": "O(4^(m*n))",
            "space": "O(m * n)",
            "whySlow": "Exponential redundant path exploration.",
            "code": {
                "java": """class Solution {
    public int longestIncreasingPath(int[][] matrix) {
        int m = matrix.length, n = matrix[0].length;
        int max = 0;
        int[][] memo = new int[m][n];
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                max = Math.max(max, dfs(matrix, i, j, memo));
            }
        }
        return max;
    }
    private int dfs(int[][] mat, int r, int c, int[][] memo) {
        if (memo[r][c] != 0) return memo[r][c];
        int max = 1;
        int[][] dirs = {{1,0}, {-1,0}, {0,1}, {0,-1}};
        for (int[] d : dirs) {
            int nr = r + d[0], nc = c + d[1];
            if (nr >= 0 && nr < mat.length && nc >= 0 && nc < mat[0].length && mat[nr][nc] > mat[r][c]) {
                max = Math.max(max, 1 + dfs(mat, nr, nc, memo));
            }
        }
        return memo[r][c] = max;
    }
}""",
                "python": """class Solution:
    def longestIncreasingPath(self, matrix: list[list[int]]) -> int:
        m, n = len(matrix), len(matrix[0])
        memo = {}
        def dfs(r, c):
            if (r, c) in memo: return memo[(r, c)]
            ans = 1
            for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] > matrix[r][c]:
                    ans = max(ans, 1 + dfs(nr, nc))
            memo[(r, c)] = ans
            return ans
        return max(dfs(i, j) for i in range(m) for j in range(n))"""
            }
        },
        "optimal": {
            "idea": "Memoized DFS: memo[r][c] caches the longest increasing path starting at (r, c). Each cell evaluated once in O(1) amortized.",
            "steps": [
                "int[][] memo = new int[m][n];",
                "dfs(r, c): if memo[r][c] != 0 return memo[r][c].",
                "len = 1; for 4 directions: if next inside and matrix[nr][nc] > matrix[r][c]: len = max(len, 1 + dfs(nr, nc)).",
                "return memo[r][c] = len.",
                "Answer is max over all cells."
            ],
            "time": "O(m * n)",
            "space": "O(m * n)",
            "code": {
                "java": """class Solution {
    public int longestIncreasingPath(int[][] matrix) {
        int m = matrix.length, n = matrix[0].length;
        int[][] memo = new int[m][n];
        int maxPath = 0;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                maxPath = Math.max(maxPath, dfs(matrix, i, j, memo, m, n));
            }
        }
        return maxPath;
    }
    private int dfs(int[][] mat, int r, int c, int[][] memo, int m, int n) {
        if (memo[r][c] != 0) return memo[r][c];
        int max = 1;
        int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        for (int[] d : dirs) {
            int nr = r + d[0], nc = c + d[1];
            if (nr >= 0 && nr < m && nc >= 0 && nc < n && mat[nr][nc] > mat[r][c]) {
                max = Math.max(max, 1 + dfs(mat, nr, nc, memo, m, n));
            }
        }
        return memo[r][c] = max;
    }
}""",
                "python": """class Solution:
    def longestIncreasingPath(self, matrix: list[list[int]]) -> int:
        m, n = len(matrix), len(matrix[0])
        memo = [[0] * n for _ in range(m)]
        def dfs(r: int, c: int) -> int:
            if memo[r][c] != 0:
                return memo[r][c]
            max_len = 1
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] > matrix[r][c]:
                    max_len = max(max_len, 1 + dfs(nr, nc))
            memo[r][c] = max_len
            return max_len
        return max(dfs(i, j) for i in range(m) for j in range(n))"""
            }
        }
    },
    # 222: Redundant Connection
    {
        "seq": 222,
        "whyNext": "Entry to Advanced Graphs / DSU: cycle detection in undirected graph; first edge connecting two already-connected nodes is redundant.",
        "brute": {
            "idea": "For every edge, check if there already exists a path between u and v using DFS on existing edges.",
            "steps": [
                "Build adjacency graph incrementally.",
                "Before adding edge (u, v), run DFS from u: if v is reachable, return [u, v]."
            ],
            "time": "O(n^2)",
            "space": "O(n)",
            "whySlow": "Runs DFS on graph for every edge in quadratic time.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public int[] findRedundantConnection(int[][] edges) {
        int n = edges.length;
        List<Integer>[] adj = new List[n + 1];
        for (int i = 1; i <= n; i++) adj[i] = new ArrayList<>();
        for (int[] e : edges) {
            boolean[] visited = new boolean[n + 1];
            if (hasPath(adj, e[0], e[1], visited)) return e;
            adj[e[0]].add(e[1]);
            adj[e[1]].add(e[0]);
        }
        return new int[0];
    }
    private boolean hasPath(List<Integer>[] adj, int u, int target, boolean[] visited) {
        if (u == target) return true;
        visited[u] = true;
        for (int v : adj[u]) {
            if (!visited[v] && hasPath(adj, v, target, visited)) return true;
        }
        return false;
    }
}""",
                "python": """from collections import defaultdict

class Solution:
    def findRedundantConnection(self, edges: list[list[int]]) -> list[int]:
        adj = defaultdict(list)
        def has_path(u, target, visited):
            if u == target: return True
            visited.add(u)
            for v in adj[u]:
                if v not in visited and has_path(v, target, visited):
                    return True
            return False
        for u, v in edges:
            if u in adj and v in adj and has_path(u, v, set()):
                return [u, v]
            adj[u].append(v)
            adj[v].append(u)
        return []"""
            }
        },
        "optimal": {
            "idea": "Disjoint Set Union (DSU): for each edge (u, v), find roots; if find(u) == find(v), edge creates cycle (return edge); else union(u, v).",
            "steps": [
                "parent = new int[n + 1] where parent[i] = i.",
                "For edge [u, v] in edges:",
                "rootU = find(u), rootV = find(v).",
                "If rootU == rootV return [u, v].",
                "parent[rootU] = rootV."
            ],
            "time": "O(n * alpha(n))",
            "space": "O(n)",
            "code": {
                "java": """class Solution {
    public int[] findRedundantConnection(int[][] edges) {
        int n = edges.length;
        int[] parent = new int[n + 1];
        for (int i = 1; i <= n; i++) parent[i] = i;
        for (int[] edge : edges) {
            int rootU = find(parent, edge[0]);
            int rootV = find(parent, edge[1]);
            if (rootU == rootV) return edge;
            parent[rootU] = rootV;
        }
        return new int[0];
    }
    private int find(int[] parent, int i) {
        if (parent[i] == i) return i;
        return parent[i] = find(parent, parent[i]);
    }
}""",
                "python": """class Solution:
    def findRedundantConnection(self, edges: list[list[int]]) -> list[int]:
        parent = list(range(len(edges) + 1))
        def find(i):
            if parent[i] == i:
                return i
            parent[i] = find(parent[i])
            return parent[i]
        for u, v in edges:
            ru, rv = find(u), find(v)
            if ru == rv:
                return [u, v]
            parent[ru] = rv
        return []"""
            }
        }
    },
    # 223: Accounts Merge
    {
        "seq": 223,
        "whyNext": "DSU connected components on string identifiers: map emails to integer IDs; union emails within same account; sort emails per root.",
        "brute": {
            "idea": "Represent emails as an undirected graph where emails sharing an account have edges; run DFS to collect connected components.",
            "steps": [
                "Build adjacency graph between all emails sharing account.",
                "Map each email to account name.",
                "Run DFS from each unvisited email to collect connected emails.",
                "Sort and format."
            ],
            "time": "O(N * K log K)",
            "space": "O(N * K)",
            "whySlow": "Constructs explicit email-to-email adjacency graph.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<List<String>> accountsMerge(List<List<String>> accounts) {
        Map<String, List<String>> g = new HashMap<>();
        Map<String, String> emailToName = new HashMap<>();
        for (List<String> acc : accounts) {
            String name = acc.get(0);
            String first = acc.get(1);
            for (int i = 1; i < acc.size(); i++) {
                String email = acc.get(i);
                emailToName.put(email, name);
                g.computeIfAbsent(first, k -> new ArrayList<>()).add(email);
                g.computeIfAbsent(email, k -> new ArrayList<>()).add(first);
            }
        }
        Set<String> visited = new HashSet<>();
        List<List<String>> res = new ArrayList<>();
        for (String email : emailToName.keySet()) {
            if (visited.add(email)) {
                List<String> comp = new ArrayList<>();
                dfs(g, email, visited, comp);
                Collections.sort(comp);
                comp.add(0, emailToName.get(email));
                res.add(comp);
            }
        }
        return res;
    }
    private void dfs(Map<String, List<String>> g, String u, Set<String> visited, List<String> comp) {
        comp.add(u);
        for (String v : g.getOrDefault(u, Collections.emptyList())) {
            if (visited.add(v)) dfs(g, v, visited, comp);
        }
    }
}""",
                "python": """from collections import defaultdict

class Solution:
    def accountsMerge(self, accounts: list[list[str]]) -> list[list[str]]:
        g = defaultdict(list)
        email_to_name = {}
        for acc in accounts:
            name = acc[0]
            first = acc[1]
            for email in acc[1:]:
                email_to_name[email] = name
                g[first].append(email)
                g[email].append(first)
        visited = set()
        res = []
        for email in email_to_name:
            if email not in visited:
                comp = []
                stack = [email]
                visited.add(email)
                while stack:
                    cur = stack.pop()
                    comp.append(cur)
                    for nxt in g[cur]:
                        if nxt not in visited:
                            visited.add(nxt)
                            stack.append(nxt)
                comp.sort()
                res.append([email_to_name[email]] + comp)
        return res"""
            }
        },
        "optimal": {
            "idea": "DSU by email string: parent map (email -> email); union all emails in account with first email; group emails by find(email).",
            "steps": [
                "Map emailToName (email -> name), parent (email -> email).",
                "Helper find(email) with path compression.",
                "For account in accounts: union all acc[i] with acc[1].",
                "Group emails by find(email) into Map<String, TreeSet<String>>.",
                "Format result with account name."
            ],
            "time": "O(N * K log(N * K))",
            "space": "O(N * K)",
            "code": {
                "java": """import java.util.*;
class Solution {
    private Map<String, String> parent = new HashMap<>();
    public List<List<String>> accountsMerge(List<List<String>> accounts) {
        Map<String, String> owner = new HashMap<>();
        for (List<String> acc : accounts) {
            String name = acc.get(0);
            for (int i = 1; i < acc.size(); i++) {
                String email = acc.get(i);
                owner.put(email, name);
                parent.putIfAbsent(email, email);
                union(acc.get(1), email);
            }
        }
        Map<String, TreeSet<String>> unions = new HashMap<>();
        for (String email : owner.keySet()) {
            String root = find(email);
            unions.computeIfAbsent(root, k -> new TreeSet<>()).add(email);
        }
        List<List<String>> res = new ArrayList<>();
        for (String root : unions.keySet()) {
            List<String> emails = new ArrayList<>(unions.get(root));
            emails.add(0, owner.get(root));
            res.add(emails);
        }
        return res;
    }
    private String find(String s) {
        if (parent.get(s).equals(s)) return s;
        parent.put(s, find(parent.get(s)));
        return parent.get(s);
    }
    private void union(String a, String b) {
        String ra = find(a), rb = find(b);
        if (!ra.equals(rb)) parent.put(ra, rb);
    }
}""",
                "python": """class Solution:
    def accountsMerge(self, accounts: list[list[str]]) -> list[list[str]]:
        parent = {}
        owner = {}
        def find(s):
            if parent[s] == s: return s
            parent[s] = find(parent[s])
            return parent[s]
        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb: parent[ra] = rb
        for acc in accounts:
            name = acc[0]
            first = acc[1]
            for email in acc[1:]:
                owner[email] = name
                if email not in parent: parent[email] = email
                if first not in parent: parent[first] = first
                union(first, email)
        from collections import defaultdict
        groups = defaultdict(list)
        for email in owner:
            groups[find(email)].append(email)
        return [[owner[root]] + sorted(emails) for root, emails in groups.items()]"""
            }
        }
    },
    # 224: Satisfiability of Equality Equations
    {
        "seq": 224,
        "whyNext": "Two-phase DSU on 26 variables: pass 1 unions all '==' equations; pass 2 checks '!='' equations for contradictory find(u) == find(v).",
        "brute": {
            "idea": "Build adjacency graph for '==' equations; for each '!=' equation run BFS to verify u and v are not reachable.",
            "steps": [
                "Build graph for '==' equations.",
                "For '!=' equations, verify disconnected via BFS."
            ],
            "time": "O(E * V)",
            "space": "O(V + E)",
            "whySlow": "BFS per inequality query when DSU checks equivalence in O(1).",
            "code": {
                "java": """class Solution {
    public boolean equationsPossible(String[] equations) {
        int[] parent = new int[26];
        for (int i = 0; i < 26; i++) parent[i] = i;
        for (String eq : equations) {
            if (eq.charAt(1) == '=') {
                union(parent, eq.charAt(0) - 'a', eq.charAt(3) - 'a');
            }
        }
        for (String eq : equations) {
            if (eq.charAt(1) == '!') {
                if (find(parent, eq.charAt(0) - 'a') == find(parent, eq.charAt(3) - 'a')) {
                    return false;
                }
            }
        }
        return true;
    }
    private int find(int[] p, int i) {
        if (p[i] == i) return i;
        return p[i] = find(p, p[i]);
    }
    private void union(int[] p, int i, int j) {
        int ri = find(p, i), rj = find(p, j);
        if (ri != rj) p[ri] = rj;
    }
}""",
                "python": """class Solution:
    def equationsPossible(self, equations: list[str]) -> bool:
        parent = list(range(26))
        def find(i):
            if parent[i] == i: return i
            parent[i] = find(parent[i])
            return parent[i]
        def union(i, j):
            ri, rj = find(i), find(j)
            if ri != rj: parent[ri] = rj
        for eq in equations:
            if eq[1] == '=':
                union(ord(eq[0]) - ord('a'), ord(eq[3]) - ord('a'))
        for eq in equations:
            if eq[1] == '!':
                if find(ord(eq[0]) - ord('a')) == find(ord(eq[3]) - ord('a')):
                    return False
        return True"""
            }
        },
        "optimal": {
            "idea": "DSU: pass 1 unions variables for all '==' equations; pass 2 verifies find(u) != find(v) for all '!=' equations.",
            "steps": [
                "int[] parent = new int[26] initialized to parent[i] = i.",
                "First pass: for each eq with eq.charAt(1) == '=', union(eq[0], eq[3]).",
                "Second pass: for each eq with eq.charAt(1) == '!', if find(eq[0]) == find(eq[3]) return false.",
                "Return true."
            ],
            "time": "O(N * alpha(26))",
            "space": "O(1) (fixed 26 letters)",
            "code": {
                "java": """class Solution {
    public boolean equationsPossible(String[] equations) {
        int[] parent = new int[26];
        for (int i = 0; i < 26; i++) parent[i] = i;
        for (String eq : equations) {
            if (eq.charAt(1) == '=') {
                int u = eq.charAt(0) - 'a';
                int v = eq.charAt(3) - 'a';
                union(parent, u, v);
            }
        }
        for (String eq : equations) {
            if (eq.charAt(1) == '!') {
                int u = eq.charAt(0) - 'a';
                int v = eq.charAt(3) - 'a';
                if (find(parent, u) == find(parent, v)) {
                    return false;
                }
            }
        }
        return true;
    }
    private int find(int[] p, int i) {
        if (p[i] == i) return i;
        return p[i] = find(p, p[i]);
    }
    private void union(int[] p, int i, int j) {
        int ri = find(p, i);
        int rj = find(p, j);
        if (ri != rj) p[ri] = rj;
    }
}""",
                "python": """class Solution:
    def equationsPossible(self, equations: list[str]) -> bool:
        parent = list(range(26))
        def find(i: int) -> int:
            if parent[i] == i:
                return i
            parent[i] = find(parent[i])
            return parent[i]
        def union(i: int, j: int):
            ri, rj = find(i), find(j)
            if ri != rj:
                parent[ri] = rj
        for eq in equations:
            if eq[1] == '=':
                union(ord(eq[0]) - ord('a'), ord(eq[3]) - ord('a'))
        for eq in equations:
            if eq[1] == '!':
                if find(ord(eq[0]) - ord('a')) == find(ord(eq[3]) - ord('a')):
                    return False
        return True"""
            }
        }
    },
    # 225: Number of Operations to Make Network Connected
    {
        "seq": 225,
        "whyNext": "DSU connected components: need at least n - 1 total cables; if cables >= n - 1, answer is (components - 1).",
        "brute": {
            "idea": "Build graph and run DFS to count number of connected components.",
            "steps": [
                "If connections.length < n - 1 return -1.",
                "Run DFS across all vertices to count components.",
                "Return components - 1."
            ],
            "time": "O(V + E)",
            "space": "O(V + E)",
            "whySlow": "Allocates graph adjacency list when DSU only needs parent array.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public int makeConnected(int n, int[][] connections) {
        if (connections.length < n - 1) return -1;
        List<Integer>[] adj = new List[n];
        for (int i = 0; i < n; i++) adj[i] = new ArrayList<>();
        for (int[] c : connections) {
            adj[c[0]].add(c[1]);
            adj[c[1]].add(c[0]);
        }
        boolean[] visited = new boolean[n];
        int components = 0;
        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                components++;
                dfs(adj, i, visited);
            }
        }
        return components - 1;
    }
    private void dfs(List<Integer>[] adj, int u, boolean[] visited) {
        visited[u] = true;
        for (int v : adj[u]) {
            if (!visited[v]) dfs(adj, v, visited);
        }
    }
}""",
                "python": """class Solution:
    def makeConnected(self, n: int, connections: list[list[int]]) -> int:
        if len(connections) < n - 1: return -1
        from collections import defaultdict
        adj = defaultdict(list)
        for u, v in connections:
            adj[u].append(v)
            adj[v].append(u)
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
        return comp - 1"""
            }
        },
        "optimal": {
            "idea": "DSU component counter: if connections.length < n - 1 return -1. Count components via DSU: answer is components - 1.",
            "steps": [
                "If connections.length < n - 1 return -1.",
                "int components = n; parent array.",
                "For edge [u, v]: if find(u) != find(v): union(u, v), components--.",
                "Return components - 1."
            ],
            "time": "O(V + E * alpha(V))",
            "space": "O(V)",
            "code": {
                "java": """class Solution {
    public int makeConnected(int n, int[][] connections) {
        if (connections.length < n - 1) return -1;
        int[] parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
        int components = n;
        for (int[] c : connections) {
            int ru = find(parent, c[0]);
            int rv = find(parent, c[1]);
            if (ru != rv) {
                parent[ru] = rv;
                components--;
            }
        }
        return components - 1;
    }
    private int find(int[] p, int i) {
        if (p[i] == i) return i;
        return p[i] = find(p, p[i]);
    }
}""",
                "python": """class Solution:
    def makeConnected(self, n: int, connections: list[list[int]]) -> int:
        if len(connections) < n - 1:
            return -1
        parent = list(range(n))
        def find(i: int) -> int:
            if parent[i] == i:
                return i
            parent[i] = find(parent[i])
            return parent[i]
        components = n
        for u, v in connections:
            ru, rv = find(u), find(v)
            if ru != rv:
                parent[ru] = rv
                components -= 1
        return components - 1"""
            }
        }
    }
]

with open('scripts/batches/batch_09.py', 'w', encoding='utf-8') as f:
    f.write("# Batch 9: Questions 201 to 225\n\n")
    f.write("def get_batch():\n")
    f.write("    return " + json.dumps(batch_9, indent=4) + "\n")

print("Wrote scripts/batches/batch_09.py with", len(batch_9), "questions.")


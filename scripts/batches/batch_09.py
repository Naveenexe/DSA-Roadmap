# Batch 9: Questions 201 to 225

def get_batch():
    return [
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
                "java": "import java.util.*;\nclass Solution {\n    public List<List<Integer>> pacificAtlantic(int[][] heights) {\n        List<List<Integer>> res = new ArrayList<>();\n        int m = heights.length, n = heights[0].length;\n        for (int i = 0; i < m; i++) {\n            for (int j = 0; j < n; j++) {\n                boolean[] ocean = new boolean[2];\n                dfs(heights, i, j, new boolean[m][n], ocean);\n                if (ocean[0] && ocean[1]) res.add(Arrays.asList(i, j));\n            }\n        }\n        return res;\n    }\n    private void dfs(int[][] h, int r, int c, boolean[][] visited, boolean[] ocean) {\n        visited[r][c] = true;\n        if (r == 0 || c == 0) ocean[0] = true;\n        if (r == h.length - 1 || c == h[0].length - 1) ocean[1] = true;\n        int[][] dirs = {{1,0}, {-1,0}, {0,1}, {0,-1}};\n        for (int[] d : dirs) {\n            int nr = r + d[0], nc = c + d[1];\n            if (nr >= 0 && nr < h.length && nc >= 0 && nc < h[0].length && !visited[nr][nc] && h[nr][nc] <= h[r][c]) {\n                dfs(h, nr, nc, visited, ocean);\n            }\n        }\n    }\n}",
                "python": "class Solution:\n    def pacificAtlantic(self, heights: list[list[int]]) -> list[list[int]]:\n        m, n = len(heights), len(heights[0])\n        res = []\n        for i in range(m):\n            for j in range(n):\n                ocean = [False, False]\n                visited = [[False]*n for _ in range(m)]\n                def dfs(r, c):\n                    visited[r][c] = True\n                    if r == 0 or c == 0: ocean[0] = True\n                    if r == m - 1 or c == n - 1: ocean[1] = True\n                    for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):\n                        nr, nc = r + dr, c + dc\n                        if 0 <= nr < m and 0 <= nc < n and not visited[nr][nc] and heights[nr][nc] <= heights[r][c]:\n                            dfs(nr, nc)\n                dfs(i, j)\n                if ocean[0] and ocean[1]: res.append([i, j])\n        return res"
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
                "java": "import java.util.*;\nclass Solution {\n    public List<List<Integer>> pacificAtlantic(int[][] heights) {\n        List<List<Integer>> res = new ArrayList<>();\n        int m = heights.length, n = heights[0].length;\n        boolean[][] pac = new boolean[m][n];\n        boolean[][] atl = new boolean[m][n];\n        for (int i = 0; i < m; i++) {\n            dfs(heights, i, 0, pac, heights[i][0]);\n            dfs(heights, i, n - 1, atl, heights[i][n - 1]);\n        }\n        for (int j = 0; j < n; j++) {\n            dfs(heights, 0, j, pac, heights[0][j]);\n            dfs(heights, m - 1, j, atl, heights[m - 1][j]);\n        }\n        for (int i = 0; i < m; i++) {\n            for (int j = 0; j < n; j++) {\n                if (pac[i][j] && atl[i][j]) {\n                    res.add(Arrays.asList(i, j));\n                }\n            }\n        }\n        return res;\n    }\n    private void dfs(int[][] h, int r, int c, boolean[][] visited, int prevH) {\n        if (r < 0 || r >= h.length || c < 0 || c >= h[0].length || visited[r][c] || h[r][c] < prevH) return;\n        visited[r][c] = true;\n        dfs(h, r + 1, c, visited, h[r][c]);\n        dfs(h, r - 1, c, visited, h[r][c]);\n        dfs(h, r, c + 1, visited, h[r][c]);\n        dfs(h, r, c - 1, visited, h[r][c]);\n    }\n}",
                "python": "class Solution:\n    def pacificAtlantic(self, heights: list[list[int]]) -> list[list[int]]:\n        m, n = len(heights), len(heights[0])\n        pac = [[False] * n for _ in range(m)]\n        atl = [[False] * n for _ in range(m)]\n        def dfs(r, c, visited, prev_h):\n            if not (0 <= r < m and 0 <= c < n) or visited[r][c] or heights[r][c] < prev_h:\n                return\n            visited[r][c] = True\n            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n                dfs(r + dr, c + dc, visited, heights[r][c])\n        for i in range(m):\n            dfs(i, 0, pac, heights[i][0])\n            dfs(i, n - 1, atl, heights[i][n - 1])\n        for j in range(n):\n            dfs(0, j, pac, heights[0][j])\n            dfs(m - 1, j, atl, heights[m - 1][j])\n        res = []\n        for i in range(m):\n            for j in range(n):\n                if pac[i][j] and atl[i][j]:\n                    res.append([i, j])\n        return res"
            }
        }
    },
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
                "java": "class Solution {\n    public int numEnclaves(int[][] grid) {\n        int m = grid.length, n = grid[0].length;\n        for (int i = 0; i < m; i++) {\n            sink(grid, i, 0);\n            sink(grid, i, n - 1);\n        }\n        for (int j = 0; j < n; j++) {\n            sink(grid, 0, j);\n            sink(grid, m - 1, j);\n        }\n        int count = 0;\n        for (int i = 0; i < m; i++) {\n            for (int j = 0; j < n; j++) {\n                if (grid[i][j] == 1) count++;\n            }\n        }\n        return count;\n    }\n    private void sink(int[][] g, int r, int c) {\n        if (r < 0 || r >= g.length || c < 0 || c >= g[0].length || g[r][c] != 1) return;\n        g[r][c] = 0;\n        sink(g, r + 1, c);\n        sink(g, r - 1, c);\n        sink(g, r, c + 1);\n        sink(g, r, c - 1);\n    }\n}",
                "python": "class Solution:\n    def numEnclaves(self, grid: list[list[int]]) -> int:\n        m, n = len(grid), len(grid[0])\n        def sink(r, c):\n            if not (0 <= r < m and 0 <= c < n) or grid[r][c] != 1: return\n            grid[r][c] = 0\n            sink(r + 1, c)\n            sink(r - 1, c)\n            sink(r, c + 1)\n            sink(r, c - 1)\n        for i in range(m):\n            sink(i, 0)\n            sink(i, n - 1)\n        for j in range(n):\n            sink(0, j)\n            sink(m - 1, j)\n        return sum(grid[i][j] for i in range(m) for j in range(n))"
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
                "java": "class Solution {\n    public int numEnclaves(int[][] grid) {\n        int m = grid.length, n = grid[0].length;\n        for (int i = 0; i < m; i++) {\n            if (grid[i][0] == 1) dfs(grid, i, 0, m, n);\n            if (grid[i][n - 1] == 1) dfs(grid, i, n - 1, m, n);\n        }\n        for (int j = 0; j < n; j++) {\n            if (grid[0][j] == 1) dfs(grid, 0, j, m, n);\n            if (grid[m - 1][j] == 1) dfs(grid, m - 1, j, m, n);\n        }\n        int count = 0;\n        for (int i = 0; i < m; i++) {\n            for (int j = 0; j < n; j++) {\n                if (grid[i][j] == 1) count++;\n            }\n        }\n        return count;\n    }\n    private void dfs(int[][] g, int r, int c, int m, int n) {\n        if (r < 0 || r >= m || c < 0 || c >= n || g[r][c] != 1) return;\n        g[r][c] = 0;\n        dfs(g, r + 1, c, m, n);\n        dfs(g, r - 1, c, m, n);\n        dfs(g, r, c + 1, m, n);\n        dfs(g, r, c - 1, m, n);\n    }\n}",
                "python": "class Solution:\n    def numEnclaves(self, grid: list[list[int]]) -> int:\n        m, n = len(grid), len(grid[0])\n        def dfs(r: int, c: int):\n            if not (0 <= r < m and 0 <= c < n) or grid[r][c] != 1:\n                return\n            grid[r][c] = 0\n            dfs(r + 1, c)\n            dfs(r - 1, c)\n            dfs(r, c + 1)\n            dfs(r, c - 1)\n        for i in range(m):\n            if grid[i][0] == 1: dfs(i, 0)\n            if grid[i][n - 1] == 1: dfs(i, n - 1)\n        for j in range(n):\n            if grid[0][j] == 1: dfs(0, j)\n            if grid[m - 1][j] == 1: dfs(m - 1, j)\n        return sum(row.count(1) for row in grid)"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public int orangesRotting(int[][] grid) {\n        int m = grid.length, n = grid[0].length;\n        Queue<int[]> q = new LinkedList<>();\n        int fresh = 0;\n        for (int i = 0; i < m; i++) {\n            for (int j = 0; j < n; j++) {\n                if (grid[i][j] == 2) q.offer(new int[]{i, j});\n                else if (grid[i][j] == 1) fresh++;\n            }\n        }\n        if (fresh == 0) return 0;\n        int minutes = 0;\n        int[][] dirs = {{1,0}, {-1,0}, {0,1}, {0,-1}};\n        while (!q.isEmpty()) {\n            int size = q.size();\n            boolean rotted = false;\n            for (int i = 0; i < size; i++) {\n                int[] cur = q.poll();\n                for (int[] d : dirs) {\n                    int r = cur[0] + d[0], c = cur[1] + d[1];\n                    if (r >= 0 && r < m && c >= 0 && c < n && grid[r][c] == 1) {\n                        grid[r][c] = 2;\n                        fresh--;\n                        rotted = true;\n                        q.offer(new int[]{r, c});\n                    }\n                }\n            }\n            if (rotted) minutes++;\n        }\n        return fresh == 0 ? minutes : -1;\n    }\n}",
                "python": "from collections import deque\n\nclass Solution:\n    def orangesRotting(self, grid: list[list[int]]) -> int:\n        m, n = len(grid), len(grid[0])\n        q = deque()\n        fresh = 0\n        for i in range(m):\n            for j in range(n):\n                if grid[i][j] == 2: q.append((i, j))\n                elif grid[i][j] == 1: fresh += 1\n        if fresh == 0: return 0\n        minutes = 0\n        while q:\n            rotted = False\n            for _ in range(len(q)):\n                r, c = q.popleft()\n                for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):\n                    nr, nc = r + dr, c + dc\n                    if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:\n                        grid[nr][nc] = 2\n                        fresh -= 1\n                        rotted = True\n                        q.append((nr, nc))\n            if rotted: minutes += 1\n        return minutes if fresh == 0 else -1"
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
                "java": "import java.util.*;\nclass Solution {\n    public int orangesRotting(int[][] grid) {\n        int m = grid.length, n = grid[0].length;\n        Queue<int[]> q = new LinkedList<>();\n        int fresh = 0;\n        for (int i = 0; i < m; i++) {\n            for (int j = 0; j < n; j++) {\n                if (grid[i][j] == 2) q.offer(new int[]{i, j});\n                else if (grid[i][j] == 1) fresh++;\n            }\n        }\n        if (fresh == 0) return 0;\n        int minutes = 0;\n        int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};\n        while (!q.isEmpty() && fresh > 0) {\n            minutes++;\n            int size = q.size();\n            for (int i = 0; i < size; i++) {\n                int[] cur = q.poll();\n                for (int[] d : dirs) {\n                    int r = cur[0] + d[0], c = cur[1] + d[1];\n                    if (r >= 0 && r < m && c >= 0 && c < n && grid[r][c] == 1) {\n                        grid[r][c] = 2;\n                        fresh--;\n                        q.offer(new int[]{r, c});\n                    }\n                }\n            }\n        }\n        return fresh == 0 ? minutes : -1;\n    }\n}",
                "python": "from collections import deque\n\nclass Solution:\n    def orangesRotting(self, grid: list[list[int]]) -> int:\n        m, n = len(grid), len(grid[0])\n        q = deque()\n        fresh = 0\n        for i in range(m):\n            for j in range(n):\n                if grid[i][j] == 2:\n                    q.append((i, j))\n                elif grid[i][j] == 1:\n                    fresh += 1\n        if fresh == 0:\n            return 0\n        minutes = 0\n        while q and fresh > 0:\n            minutes += 1\n            for _ in range(len(q)):\n                r, c = q.popleft()\n                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n                    nr, nc = r + dr, c + dc\n                    if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:\n                        grid[nr][nc] = 2\n                        fresh -= 1\n                        q.append((nr, nc))\n        return minutes if fresh == 0 else -1"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public int[][] updateMatrix(int[][] mat) {\n        int m = mat.length, n = mat[0].length;\n        int[][] res = new int[m][n];\n        for (int[] row : res) Arrays.fill(row, -1);\n        Queue<int[]> q = new LinkedList<>();\n        for (int i = 0; i < m; i++) {\n            for (int j = 0; j < n; j++) {\n                if (mat[i][j] == 0) {\n                    res[i][j] = 0;\n                    q.offer(new int[]{i, j});\n                }\n            }\n        }\n        int[][] dirs = {{1,0}, {-1,0}, {0,1}, {0,-1}};\n        while (!q.isEmpty()) {\n            int[] cur = q.poll();\n            for (int[] d : dirs) {\n                int r = cur[0] + d[0], c = cur[1] + d[1];\n                if (r >= 0 && r < m && c >= 0 && c < n && res[r][c] == -1) {\n                    res[r][c] = res[cur[0]][cur[1]] + 1;\n                    q.offer(new int[]{r, c});\n                }\n            }\n        }\n        return res;\n    }\n}",
                "python": "from collections import deque\n\nclass Solution:\n    def updateMatrix(self, mat: list[list[int]]) -> list[list[int]]:\n        m, n = len(mat), len(mat[0])\n        dist = [[-1] * n for _ in range(m)]\n        q = deque()\n        for i in range(m):\n            for j in range(n):\n                if mat[i][j] == 0:\n                    dist[i][j] = 0\n                    q.append((i, j))\n        while q:\n            r, c = q.popleft()\n            for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):\n                nr, nc = r + dr, c + dc\n                if 0 <= nr < m and 0 <= nc < n and dist[nr][nc] == -1:\n                    dist[nr][nc] = dist[r][c] + 1\n                    q.append((nr, nc))\n        return dist"
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
                "java": "class Solution {\n    public int[][] updateMatrix(int[][] mat) {\n        int m = mat.length, n = mat[0].length;\n        int INF = m + n;\n        for (int i = 0; i < m; i++) {\n            for (int j = 0; j < n; j++) {\n                if (mat[i][j] != 0) {\n                    int top = (i > 0) ? mat[i - 1][j] : INF;\n                    int left = (j > 0) ? mat[i][j - 1] : INF;\n                    mat[i][j] = Math.min(top, left) + 1;\n                }\n            }\n        }\n        for (int i = m - 1; i >= 0; i--) {\n            for (int j = n - 1; j >= 0; j--) {\n                if (mat[i][j] != 0) {\n                    int bottom = (i < m - 1) ? mat[i + 1][j] : INF;\n                    int right = (j < n - 1) ? mat[i][j + 1] : INF;\n                    mat[i][j] = Math.min(mat[i][j], Math.min(bottom, right) + 1);\n                }\n            }\n        }\n        return mat;\n    }\n}",
                "python": "class Solution:\n    def updateMatrix(self, mat: list[list[int]]) -> list[list[int]]:\n        m, n = len(mat), len(mat[0])\n        INF = m + n\n        for i in range(m):\n            for j in range(n):\n                if mat[i][j] != 0:\n                    top = mat[i - 1][j] if i > 0 else INF\n                    left = mat[i][j - 1] if j > 0 else INF\n                    mat[i][j] = min(top, left) + 1\n        for i in range(m - 1, -1, -1):\n            for j in range(n - 1, -1, -1):\n                if mat[i][j] != 0:\n                    bottom = mat[i + 1][j] if i < m - 1 else INF\n                    right = mat[i][j + 1] if j < n - 1 else INF\n                    mat[i][j] = min(mat[i][j], min(bottom, right) + 1)\n        return mat"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public int shortestPathBinaryMatrix(int[][] grid) {\n        int n = grid.length;\n        if (grid[0][0] != 0 || grid[n - 1][n - 1] != 0) return -1;\n        Queue<int[]> q = new LinkedList<>();\n        q.offer(new int[]{0, 0, 1});\n        grid[0][0] = 1;\n        int[][] dirs = {\n            {-1,-1},{-1,0},{-1,1},{0,-1},{0,1},{1,-1},{1,0},{1,1}\n        };\n        while (!q.isEmpty()) {\n            int[] cur = q.poll();\n            int r = cur[0], c = cur[1], d = cur[2];\n            if (r == n - 1 && c == n - 1) return d;\n            for (int[] dir : dirs) {\n                int nr = r + dir[0], nc = c + dir[1];\n                if (nr >= 0 && nr < n && nc >= 0 && nc < n && grid[nr][nc] == 0) {\n                    grid[nr][nc] = 1;\n                    q.offer(new int[]{nr, nc, d + 1});\n                }\n            }\n        }\n        return -1;\n    }\n}",
                "python": "from collections import deque\n\nclass Solution:\n    def shortestPathBinaryMatrix(self, grid: list[list[int]]) -> int:\n        n = len(grid)\n        if grid[0][0] != 0 or grid[n-1][n-1] != 0: return -1\n        q = deque([(0, 0, 1)])\n        grid[0][0] = 1\n        dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]\n        while q:\n            r, c, d = q.popleft()\n            if r == n - 1 and c == n - 1: return d\n            for dr, dc in dirs:\n                nr, nc = r + dr, c + dc\n                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:\n                    grid[nr][nc] = 1\n                    q.append((nr, nc, d + 1))\n        return -1"
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
                "java": "import java.util.*;\nclass Solution {\n    public int shortestPathBinaryMatrix(int[][] grid) {\n        int n = grid.length;\n        if (grid[0][0] == 1 || grid[n - 1][n - 1] == 1) return -1;\n        Queue<int[]> q = new LinkedList<>();\n        q.offer(new int[]{0, 0, 1});\n        grid[0][0] = 1;\n        int[][] dirs = {\n            {-1, -1}, {-1, 0}, {-1, 1},\n            {0, -1},           {0, 1},\n            {1, -1},  {1, 0},  {1, 1}\n        };\n        while (!q.isEmpty()) {\n            int[] cur = q.poll();\n            int r = cur[0], c = cur[1], d = cur[2];\n            if (r == n - 1 && c == n - 1) return d;\n            for (int[] dir : dirs) {\n                int nr = r + dir[0], nc = c + dir[1];\n                if (nr >= 0 && nr < n && nc >= 0 && nc < n && grid[nr][nc] == 0) {\n                    grid[nr][nc] = 1;\n                    q.offer(new int[]{nr, nc, d + 1});\n                }\n            }\n        }\n        return -1;\n    }\n}",
                "python": "from collections import deque\n\nclass Solution:\n    def shortestPathBinaryMatrix(self, grid: list[list[int]]) -> int:\n        n = len(grid)\n        if grid[0][0] == 1 or grid[n - 1][n - 1] == 1:\n            return -1\n        q = deque([(0, 0, 1)])\n        grid[0][0] = 1\n        dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]\n        while q:\n            r, c, d = q.popleft()\n            if r == n - 1 and c == n - 1:\n                return d\n            for dr, dc in dirs:\n                nr, nc = r + dr, c + dc\n                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:\n                    grid[nr][nc] = 1\n                    q.append((nr, nc, d + 1))\n        return -1"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public int ladderLength(String beginWord, String endWord, List<String> wordList) {\n        Set<String> wordSet = new HashSet<>(wordList);\n        if (!wordSet.contains(endWord)) return 0;\n        Queue<String> q = new LinkedList<>();\n        q.offer(beginWord);\n        int steps = 1;\n        while (!q.isEmpty()) {\n            int size = q.size();\n            for (int k = 0; k < size; k++) {\n                String cur = q.poll();\n                if (cur.equals(endWord)) return steps;\n                char[] chars = cur.toCharArray();\n                for (int i = 0; i < chars.length; i++) {\n                    char orig = chars[i];\n                    for (char c = 'a'; c <= 'z'; c++) {\n                        chars[i] = c;\n                        String next = new String(chars);\n                        if (wordSet.remove(next)) {\n                            q.offer(next);\n                        }\n                    }\n                    chars[i] = orig;\n                }\n            }\n            steps++;\n        }\n        return 0;\n    }\n}",
                "python": "from collections import deque\n\nclass Solution:\n    def ladderLength(self, beginWord: str, endWord: str, wordList: list[str]) -> int:\n        words = set(wordList)\n        if endWord not in words: return 0\n        q = deque([(beginWord, 1)])\n        while q:\n            cur, steps = q.popleft()\n            if cur == endWord: return steps\n            for i in range(len(cur)):\n                for c in \"abcdefghijklmnopqrstuvwxyz\":\n                    nxt = cur[:i] + c + cur[i+1:]\n                    if nxt in words:\n                        words.remove(nxt)\n                        q.append((nxt, steps + 1))\n        return 0"
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
                "java": "import java.util.*;\nclass Solution {\n    public int ladderLength(String beginWord, String endWord, List<String> wordList) {\n        Set<String> wordSet = new HashSet<>(wordList);\n        if (!wordSet.contains(endWord)) return 0;\n        Set<String> beginSet = new HashSet<>();\n        Set<String> endSet = new HashSet<>();\n        beginSet.add(beginWord);\n        endSet.add(endWord);\n        int steps = 1;\n        while (!beginSet.isEmpty() && !endSet.isEmpty()) {\n            if (beginSet.size() > endSet.size()) {\n                Set<String> temp = beginSet;\n                beginSet = endSet;\n                endSet = temp;\n            }\n            Set<String> nextSet = new HashSet<>();\n            for (String word : beginSet) {\n                char[] chs = word.toCharArray();\n                for (int i = 0; i < chs.length; i++) {\n                    char old = chs[i];\n                    for (char c = 'a'; c <= 'z'; c++) {\n                        chs[i] = c;\n                        String target = new String(chs);\n                        if (endSet.contains(target)) return steps + 1;\n                        if (wordSet.contains(target)) {\n                            nextSet.add(target);\n                            wordSet.remove(target);\n                        }\n                    }\n                    chs[i] = old;\n                }\n            }\n            beginSet = nextSet;\n            steps++;\n        }\n        return 0;\n    }\n}",
                "python": "class Solution:\n    def ladderLength(self, beginWord: str, endWord: str, wordList: list[str]) -> int:\n        word_set = set(wordList)\n        if endWord not in word_set:\n            return 0\n        begin_set = {beginWord}\n        end_set = {endWord}\n        steps = 1\n        while begin_set and end_set:\n            if len(begin_set) > len(end_set):\n                begin_set, end_set = end_set, begin_set\n            next_set = set()\n            for word in begin_set:\n                for i in range(len(word)):\n                    for c in \"abcdefghijklmnopqrstuvwxyz\":\n                        nxt = word[:i] + c + word[i+1:]\n                        if nxt in end_set:\n                            return steps + 1\n                        if nxt in word_set:\n                            next_set.add(nxt)\n                            word_set.remove(nxt)\n            begin_set = next_set\n            steps += 1\n        return 0"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public Node cloneGraph(Node node) {\n        if (node == null) return null;\n        Map<Node, Node> map = new HashMap<>();\n        Queue<Node> q = new LinkedList<>();\n        q.offer(node);\n        map.put(node, new Node(node.val));\n        while (!q.isEmpty()) {\n            Node cur = q.poll();\n            for (Node neighbor : cur.neighbors) {\n                if (!map.containsKey(neighbor)) {\n                    map.put(neighbor, new Node(neighbor.val));\n                    q.offer(neighbor);\n                }\n            }\n        }\n        for (Node orig : map.keySet()) {\n            for (Node neighbor : orig.neighbors) {\n                map.get(orig).neighbors.add(map.get(neighbor));\n            }\n        }\n        return map.get(node);\n    }\n}",
                "python": "class Solution:\n    def cloneGraph(self, node: 'Node') -> 'Node':\n        if not node: return None\n        from collections import deque\n        mapping = {node: Node(node.val)}\n        q = deque([node])\n        while q:\n            cur = q.popleft()\n            for neighbor in cur.neighbors:\n                if neighbor not in mapping:\n                    mapping[neighbor] = Node(neighbor.val)\n                    q.append(neighbor)\n        for orig, clone in mapping.items():\n            clone.neighbors = [mapping[nbr] for nbr in orig.neighbors]\n        return mapping[node]"
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
                "java": "import java.util.*;\nclass Solution {\n    private Map<Node, Node> visited = new HashMap<>();\n    public Node cloneGraph(Node node) {\n        if (node == null) return null;\n        if (visited.containsKey(node)) return visited.get(node);\n        Node clone = new Node(node.val);\n        visited.put(node, clone);\n        for (Node neighbor : node.neighbors) {\n            clone.neighbors.add(cloneGraph(neighbor));\n        }\n        return clone;\n    }\n}",
                "python": "class Solution:\n    def __init__(self):\n        self.visited = {}\n\n    def cloneGraph(self, node: 'Node') -> 'Node':\n        if not node:\n            return None\n        if node in self.visited:\n            return self.visited[node]\n        clone = Node(node.val)\n        self.visited[node] = clone\n        clone.neighbors = [self.cloneGraph(neighbor) for neighbor in node.neighbors]\n        return clone"
            }
        }
    },
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
                "java": "class Solution {\n    public boolean isBipartite(int[][] graph) {\n        int n = graph.length;\n        int[] color = new int[n];\n        for (int i = 0; i < n; i++) {\n            if (color[i] == 0 && !dfs(graph, i, 1, color)) {\n                return false;\n            }\n        }\n        return true;\n    }\n    private boolean dfs(int[][] g, int u, int c, int[] color) {\n        color[u] = c;\n        for (int v : g[u]) {\n            if (color[v] == c) return false;\n            if (color[v] == 0 && !dfs(g, v, -c, color)) return false;\n        }\n        return true;\n    }\n}",
                "python": "class Solution:\n    def isBipartite(self, graph: list[list[int]]) -> bool:\n        color = {}\n        for node in range(len(graph)):\n            if node not in color:\n                stack = [node]\n                color[node] = 0\n                while stack:\n                    u = stack.pop()\n                    for v in graph[u]:\n                        if v not in color:\n                            color[v] = 1 - color[u]\n                            stack.append(v)\n                        elif color[v] == color[u]:\n                            return False\n        return True"
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
                "java": "import java.util.*;\nclass Solution {\n    public boolean isBipartite(int[][] graph) {\n        int n = graph.length;\n        int[] color = new int[n];\n        for (int i = 0; i < n; i++) {\n            if (color[i] != 0) continue;\n            Queue<Integer> q = new LinkedList<>();\n            q.offer(i);\n            color[i] = 1;\n            while (!q.isEmpty()) {\n                int u = q.poll();\n                for (int v : graph[u]) {\n                    if (color[v] == color[u]) return false;\n                    if (color[v] == 0) {\n                        color[v] = -color[u];\n                        q.offer(v);\n                    }\n                }\n            }\n        }\n        return true;\n    }\n}",
                "python": "from collections import deque\n\nclass Solution:\n    def isBipartite(self, graph: list[list[int]]) -> bool:\n        n = len(graph)\n        color = [0] * n\n        for i in range(n):\n            if color[i] != 0:\n                continue\n            q = deque([i])\n            color[i] = 1\n            while q:\n                u = q.popleft()\n                for v in graph[u]:\n                    if color[v] == color[u]:\n                        return False\n                    if color[v] == 0:\n                        color[v] = -color[u]\n                        q.append(v)\n        return True"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public boolean possibleBipartition(int n, int[][] dislikes) {\n        List<Integer>[] adj = new List[n + 1];\n        for (int i = 1; i <= n; i++) adj[i] = new ArrayList<>();\n        for (int[] d : dislikes) {\n            adj[d[0]].add(d[1]);\n            adj[d[1]].add(d[0]);\n        }\n        int[] color = new int[n + 1];\n        for (int i = 1; i <= n; i++) {\n            if (color[i] == 0 && !dfs(adj, i, 1, color)) return false;\n        }\n        return true;\n    }\n    private boolean dfs(List<Integer>[] adj, int u, int c, int[] color) {\n        color[u] = c;\n        for (int v : adj[u]) {\n            if (color[v] == c) return false;\n            if (color[v] == 0 && !dfs(adj, v, -c, color)) return false;\n        }\n        return true;\n    }\n}",
                "python": "from collections import defaultdict\n\nclass Solution:\n    def possibleBipartition(self, n: int, dislikes: list[list[int]]) -> bool:\n        adj = defaultdict(list)\n        for u, v in dislikes:\n            adj[u].append(v)\n            adj[v].append(u)\n        color = {}\n        for i in range(1, n + 1):\n            if i not in color:\n                color[i] = 1\n                q = [i]\n                while q:\n                    u = q.pop()\n                    for v in adj[u]:\n                        if v in color:\n                            if color[v] == color[u]: return False\n                        else:\n                            color[v] = -color[u]\n                            q.append(v)\n        return True"
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
                "java": "import java.util.*;\nclass Solution {\n    public boolean possibleBipartition(int n, int[][] dislikes) {\n        List<Integer>[] adj = new List[n + 1];\n        for (int i = 1; i <= n; i++) adj[i] = new ArrayList<>();\n        for (int[] d : dislikes) {\n            adj[d[0]].add(d[1]);\n            adj[d[1]].add(d[0]);\n        }\n        int[] color = new int[n + 1];\n        for (int i = 1; i <= n; i++) {\n            if (color[i] != 0) continue;\n            Queue<Integer> q = new LinkedList<>();\n            q.offer(i);\n            color[i] = 1;\n            while (!q.isEmpty()) {\n                int u = q.poll();\n                for (int v : adj[u]) {\n                    if (color[v] == color[u]) return false;\n                    if (color[v] == 0) {\n                        color[v] = -color[u];\n                        q.offer(v);\n                    }\n                }\n            }\n        }\n        return true;\n    }\n}",
                "python": "from collections import deque, defaultdict\n\nclass Solution:\n    def possibleBipartition(self, n: int, dislikes: list[list[int]]) -> bool:\n        adj = defaultdict(list)\n        for u, v in dislikes:\n            adj[u].append(v)\n            adj[v].append(u)\n        color = [0] * (n + 1)\n        for i in range(1, n + 1):\n            if color[i] != 0:\n                continue\n            q = deque([i])\n            color[i] = 1\n            while q:\n                u = q.popleft()\n                for v in adj[u]:\n                    if color[v] == color[u]:\n                        return False\n                    if color[v] == 0:\n                        color[v] = -color[u]\n                        q.append(v)\n        return True"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public boolean canVisitAllRooms(List<List<Integer>> rooms) {\n        int n = rooms.size();\n        boolean[] visited = new boolean[n];\n        Queue<Integer> q = new LinkedList<>();\n        q.offer(0);\n        visited[0] = true;\n        int count = 1;\n        while (!q.isEmpty()) {\n            int cur = q.poll();\n            for (int key : rooms.get(cur)) {\n                if (!visited[key]) {\n                    visited[key] = true;\n                    count++;\n                    q.offer(key);\n                }\n            }\n        }\n        return count == n;\n    }\n}",
                "python": "from collections import deque\n\nclass Solution:\n    def canVisitAllRooms(self, rooms: list[list[int]]) -> bool:\n        n = len(rooms)\n        visited = {0}\n        q = deque([0])\n        while q:\n            cur = q.popleft()\n            for key in rooms[cur]:\n                if key not in visited:\n                    visited.add(key)\n                    q.append(key)\n        return len(visited) == n"
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
                "java": "import java.util.*;\nclass Solution {\n    public boolean canVisitAllRooms(List<List<Integer>> rooms) {\n        int n = rooms.size();\n        boolean[] visited = new boolean[n];\n        Deque<Integer> stack = new ArrayDeque<>();\n        stack.push(0);\n        visited[0] = true;\n        int count = 1;\n        while (!stack.isEmpty()) {\n            int room = stack.pop();\n            for (int key : rooms.get(room)) {\n                if (!visited[key]) {\n                    visited[key] = true;\n                    count++;\n                    stack.push(key);\n                }\n            }\n        }\n        return count == n;\n    }\n}",
                "python": "class Solution:\n    def canVisitAllRooms(self, rooms: list[list[int]]) -> bool:\n        visited = set([0])\n        stack = [0]\n        while stack:\n            room = stack.pop()\n            for key in rooms[room]:\n                if key not in visited:\n                    visited.add(key)\n                    stack.append(key)\n        return len(visited) == len(rooms)"
            }
        }
    },
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
                "java": "class Solution {\n    public int findCircleNum(int[][] isConnected) {\n        int n = isConnected.length;\n        boolean[] visited = new boolean[n];\n        int count = 0;\n        for (int i = 0; i < n; i++) {\n            if (!visited[i]) {\n                count++;\n                dfs(isConnected, i, visited);\n            }\n        }\n        return count;\n    }\n    private void dfs(int[][] g, int u, boolean[] visited) {\n        visited[u] = true;\n        for (int v = 0; v < g.length; v++) {\n            if (g[u][v] == 1 && !visited[v]) {\n                dfs(g, v, visited);\n            }\n        }\n    }\n}",
                "python": "class Solution:\n    def findCircleNum(self, isConnected: list[list[int]]) -> int:\n        n = len(isConnected)\n        visited = set()\n        count = 0\n        def dfs(u):\n            visited.add(u)\n            for v in range(n):\n                if isConnected[u][v] and v not in visited:\n                    dfs(v)\n        for i in range(n):\n            if i not in visited:\n                count += 1\n                dfs(i)\n        return count"
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
                "java": "class Solution {\n    public int findCircleNum(int[][] isConnected) {\n        int n = isConnected.length;\n        boolean[] visited = new boolean[n];\n        int provinces = 0;\n        for (int i = 0; i < n; i++) {\n            if (!visited[i]) {\n                provinces++;\n                dfs(isConnected, i, visited);\n            }\n        }\n        return provinces;\n    }\n    private void dfs(int[][] isConnected, int u, boolean[] visited) {\n        visited[u] = true;\n        for (int v = 0; v < isConnected.length; v++) {\n            if (isConnected[u][v] == 1 && !visited[v]) {\n                dfs(isConnected, v, visited);\n            }\n        }\n    }\n}",
                "python": "class Solution:\n    def findCircleNum(self, isConnected: list[list[int]]) -> int:\n        n = len(isConnected)\n        visited = [False] * n\n        provinces = 0\n        def dfs(u: int):\n            visited[u] = True\n            for v in range(n):\n                if isConnected[u][v] == 1 and not visited[v]:\n                    dfs(v)\n        for i in range(n):\n            if not visited[i]:\n                provinces += 1\n                dfs(i)\n        return provinces"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public boolean validPath(int n, int[][] edges, int source, int destination) {\n        if (source == destination) return true;\n        List<Integer>[] adj = new List[n];\n        for (int i = 0; i < n; i++) adj[i] = new ArrayList<>();\n        for (int[] e : edges) {\n            adj[e[0]].add(e[1]);\n            adj[e[1]].add(e[0]);\n        }\n        boolean[] visited = new boolean[n];\n        Queue<Integer> q = new LinkedList<>();\n        q.offer(source);\n        visited[source] = true;\n        while (!q.isEmpty()) {\n            int cur = q.poll();\n            if (cur == destination) return true;\n            for (int nxt : adj[cur]) {\n                if (!visited[nxt]) {\n                    visited[nxt] = true;\n                    q.offer(nxt);\n                }\n            }\n        }\n        return false;\n    }\n}",
                "python": "from collections import deque, defaultdict\n\nclass Solution:\n    def validPath(self, n: int, edges: list[list[int]], source: int, destination: int) -> bool:\n        if source == destination: return True\n        adj = defaultdict(list)\n        for u, v in edges:\n            adj[u].append(v)\n            adj[v].append(u)\n        q = deque([source])\n        visited = {source}\n        while q:\n            cur = q.popleft()\n            if cur == destination: return True\n            for nxt in adj[cur]:\n                if nxt not in visited:\n                    visited.add(nxt)\n                    q.append(nxt)\n        return False"
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
                "java": "class Solution {\n    public boolean validPath(int n, int[][] edges, int source, int destination) {\n        int[] parent = new int[n];\n        for (int i = 0; i < n; i++) parent[i] = i;\n        for (int[] e : edges) {\n            union(parent, e[0], e[1]);\n        }\n        return find(parent, source) == find(parent, destination);\n    }\n    private int find(int[] parent, int i) {\n        if (parent[i] == i) return i;\n        return parent[i] = find(parent, parent[i]);\n    }\n    private void union(int[] parent, int i, int j) {\n        int rootI = find(parent, i);\n        int rootJ = find(parent, j);\n        if (rootI != rootJ) parent[rootI] = rootJ;\n    }\n}",
                "python": "class Solution:\n    def validPath(self, n: int, edges: list[list[int]], source: int, destination: int) -> bool:\n        parent = list(range(n))\n        def find(i):\n            if parent[i] == i: return i\n            parent[i] = find(parent[i])\n            return parent[i]\n        def union(i, j):\n            root_i, root_j = find(i), find(j)\n            if root_i != root_j:\n                parent[root_i] = root_j\n        for u, v in edges:\n            union(u, v)\n        return find(source) == find(destination)"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public List<List<Integer>> allPathsSourceTarget(int[][] graph) {\n        List<List<Integer>> res = new ArrayList<>();\n        Queue<List<Integer>> q = new LinkedList<>();\n        q.offer(Arrays.asList(0));\n        int target = graph.length - 1;\n        while (!q.isEmpty()) {\n            List<Integer> path = q.poll();\n            int last = path.get(path.size() - 1);\n            if (last == target) {\n                res.add(path);\n                continue;\n            }\n            for (int next : graph[last]) {\n                List<Integer> newPath = new ArrayList<>(path);\n                newPath.add(next);\n                q.offer(newPath);\n            }\n        }\n        return res;\n    }\n}",
                "python": "from collections import deque\n\nclass Solution:\n    def allPathsSourceTarget(self, graph: list[list[int]]) -> list[list[int]]:\n        target = len(graph) - 1\n        q = deque([[0]])\n        res = []\n        while q:\n            path = q.popleft()\n            if path[-1] == target:\n                res.append(path)\n            else:\n                for nxt in graph[path[-1]]:\n                    q.append(path + [nxt])\n        return res"
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
                "java": "import java.util.*;\nclass Solution {\n    public List<List<Integer>> allPathsSourceTarget(int[][] graph) {\n        List<List<Integer>> res = new ArrayList<>();\n        List<Integer> path = new ArrayList<>();\n        path.add(0);\n        dfs(graph, 0, path, res);\n        return res;\n    }\n    private void dfs(int[][] graph, int node, List<Integer> path, List<List<Integer>> res) {\n        if (node == graph.length - 1) {\n            res.add(new ArrayList<>(path));\n            return;\n        }\n        for (int next : graph[node]) {\n            path.add(next);\n            dfs(graph, next, path, res);\n            path.remove(path.size() - 1);\n        }\n    }\n}",
                "python": "class Solution:\n    def allPathsSourceTarget(self, graph: list[list[int]]) -> list[list[int]]:\n        res = []\n        path = [0]\n        target = len(graph) - 1\n        def dfs(node: int):\n            if node == target:\n                res.append(list(path))\n                return\n            for nxt in graph[node]:\n                path.append(nxt)\n                dfs(nxt)\n                path.pop()\n        dfs(0)\n        return res"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public int shortestBridge(int[][] grid) {\n        int n = grid.length;\n        List<int[]> island1 = new ArrayList<>();\n        List<int[]> island2 = new ArrayList<>();\n        boolean found = false;\n        for (int i = 0; i < n; i++) {\n            for (int j = 0; j < n; j++) {\n                if (grid[i][j] == 1) {\n                    if (!found) {\n                        dfs(grid, i, j, island1);\n                        found = true;\n                    } else if (grid[i][j] == 1) {\n                        dfs(grid, i, j, island2);\n                    }\n                }\n            }\n        }\n        int minD = Integer.MAX_VALUE;\n        for (int[] p1 : island1) {\n            for (int[] p2 : island2) {\n                minD = Math.min(minD, Math.abs(p1[0] - p2[0]) + Math.abs(p1[1] - p2[1]) - 1);\n            }\n        }\n        return minD;\n    }\n    private void dfs(int[][] g, int r, int c, List<int[]> list) {\n        if (r < 0 || r >= g.length || c < 0 || c >= g.length || g[r][c] != 1) return;\n        g[r][c] = 2;\n        list.add(new int[]{r, c});\n        dfs(g, r + 1, c, list);\n        dfs(g, r - 1, c, list);\n        dfs(g, r, c + 1, list);\n        dfs(g, r, c - 1, list);\n    }\n}",
                "python": "class Solution:\n    def shortestBridge(self, grid: list[list[int]]) -> int:\n        n = len(grid)\n        i1, i2 = [], []\n        found = False\n        def dfs(r, c, lst):\n            if not (0 <= r < n and 0 <= c < n) or grid[r][c] != 1: return\n            grid[r][c] = 2\n            lst.append((r, c))\n            dfs(r+1, c, lst); dfs(r-1, c, lst); dfs(r, c+1, lst); dfs(r, c-1, lst)\n        for i in range(n):\n            for j in range(n):\n                if grid[i][j] == 1:\n                    if not found:\n                        dfs(i, j, i1)\n                        found = True\n                    else:\n                        dfs(i, j, i2)\n        return min(abs(r1-r2) + abs(c1-c2) - 1 for r1, c1 in i1 for r2, c2 in i2)"
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
                "java": "import java.util.*;\nclass Solution {\n    public int shortestBridge(int[][] grid) {\n        int n = grid.length;\n        Queue<int[]> q = new LinkedList<>();\n        boolean found = false;\n        for (int i = 0; i < n && !found; i++) {\n            for (int j = 0; j < n && !found; j++) {\n                if (grid[i][j] == 1) {\n                    dfs(grid, i, j, n, q);\n                    found = true;\n                }\n            }\n        }\n        int steps = 0;\n        int[][] dirs = {{1,0}, {-1,0}, {0,1}, {0,-1}};\n        while (!q.isEmpty()) {\n            int size = q.size();\n            for (int k = 0; k < size; k++) {\n                int[] cur = q.poll();\n                for (int[] d : dirs) {\n                    int nr = cur[0] + d[0], nc = cur[1] + d[1];\n                    if (nr >= 0 && nr < n && nc >= 0 && nc < n) {\n                        if (grid[nr][nc] == 1) return steps;\n                        if (grid[nr][nc] == 0) {\n                            grid[nr][nc] = 2;\n                            q.offer(new int[]{nr, nc});\n                        }\n                    }\n                }\n            }\n            steps++;\n        }\n        return -1;\n    }\n    private void dfs(int[][] g, int r, int c, int n, Queue<int[]> q) {\n        if (r < 0 || r >= n || c < 0 || c >= n || g[r][c] != 1) return;\n        g[r][c] = 2;\n        q.offer(new int[]{r, c});\n        dfs(g, r + 1, c, n, q);\n        dfs(g, r - 1, c, n, q);\n        dfs(g, r, c + 1, n, q);\n        dfs(g, r, c - 1, n, q);\n    }\n}",
                "python": "from collections import deque\n\nclass Solution:\n    def shortestBridge(self, grid: list[list[int]]) -> int:\n        n = len(grid)\n        q = deque()\n        found = False\n        def dfs(r, c):\n            if not (0 <= r < n and 0 <= c < n) or grid[r][c] != 1: return\n            grid[r][c] = 2\n            q.append((r, c))\n            dfs(r + 1, c)\n            dfs(r - 1, c)\n            dfs(r, c + 1)\n            dfs(r, c - 1)\n        for i in range(n):\n            if found: break\n            for j in range(n):\n                if grid[i][j] == 1:\n                    dfs(i, j)\n                    found = True\n                    break\n        steps = 0\n        while q:\n            for _ in range(len(q)):\n                r, c = q.popleft()\n                for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):\n                    nr, nc = r + dr, c + dc\n                    if 0 <= nr < n and 0 <= nc < n:\n                        if grid[nr][nc] == 1:\n                            return steps\n                        if grid[nr][nc] == 0:\n                            grid[nr][nc] = 2\n                            q.append((nr, nc))\n            steps += 1\n        return -1"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public double[] calcEquation(List<List<String>> equations, double[] values, List<List<String>> queries) {\n        Map<String, Map<String, Double>> g = new HashMap<>();\n        for (int i = 0; i < equations.size(); i++) {\n            String u = equations.get(i).get(0), v = equations.get(i).get(1);\n            double val = values[i];\n            g.computeIfAbsent(u, k -> new HashMap<>()).put(v, val);\n            g.computeIfAbsent(v, k -> new HashMap<>()).put(u, 1.0 / val);\n        }\n        double[] res = new double[queries.size()];\n        for (int i = 0; i < queries.size(); i++) {\n            String u = queries.get(i).get(0), v = queries.get(i).get(1);\n            if (!g.containsKey(u) || !g.containsKey(v)) res[i] = -1.0;\n            else if (u.equals(v)) res[i] = 1.0;\n            else res[i] = dfs(g, u, v, 1.0, new HashSet<>());\n        }\n        return res;\n    }\n    private double dfs(Map<String, Map<String, Double>> g, String cur, String target, double p, Set<String> visited) {\n        visited.add(cur);\n        if (cur.equals(target)) return p;\n        for (String next : g.get(cur).keySet()) {\n            if (!visited.contains(next)) {\n                double ans = dfs(g, next, target, p * g.get(cur).get(next), visited);\n                if (ans != -1.0) return ans;\n            }\n        }\n        return -1.0;\n    }\n}",
                "python": "from collections import defaultdict\n\nclass Solution:\n    def calcEquation(self, equations: list[list[str]], values: list[float], queries: list[list[str]]) -> list[float]:\n        g = defaultdict(dict)\n        for (u, v), val in zip(equations, values):\n            g[u][v] = val\n            g[v][u] = 1.0 / val\n        def dfs(cur, target, visited):\n            if cur not in g or target not in g: return -1.0\n            if cur == target: return 1.0\n            visited.add(cur)\n            for nxt, weight in g[cur].items():\n                if nxt not in visited:\n                    res = dfs(nxt, target, visited)\n                    if res != -1.0: return res * weight\n            return -1.0\n        return [dfs(q[0], q[1], set()) for q in queries]"
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
                "java": "import java.util.*;\nclass Solution {\n    public double[] calcEquation(List<List<String>> equations, double[] values, List<List<String>> queries) {\n        Map<String, Map<String, Double>> graph = new HashMap<>();\n        for (int i = 0; i < equations.size(); i++) {\n            String u = equations.get(i).get(0);\n            String v = equations.get(i).get(1);\n            double val = values[i];\n            graph.computeIfAbsent(u, k -> new HashMap<>()).put(v, val);\n            graph.computeIfAbsent(v, k -> new HashMap<>()).put(u, 1.0 / val);\n        }\n        double[] res = new double[queries.size()];\n        for (int i = 0; i < queries.size(); i++) {\n            String start = queries.get(i).get(0);\n            String end = queries.get(i).get(1);\n            if (!graph.containsKey(start) || !graph.containsKey(end)) {\n                res[i] = -1.0;\n            } else if (start.equals(end)) {\n                res[i] = 1.0;\n            } else {\n                res[i] = dfs(graph, start, end, 1.0, new HashSet<>());\n            }\n        }\n        return res;\n    }\n    private double dfs(Map<String, Map<String, Double>> g, String cur, String target, double product, Set<String> visited) {\n        visited.add(cur);\n        if (cur.equals(target)) return product;\n        for (Map.Entry<String, Double> edge : g.get(cur).entrySet()) {\n            if (!visited.contains(edge.getKey())) {\n                double sub = dfs(g, edge.getKey(), target, product * edge.getValue(), visited);\n                if (sub != -1.0) return sub;\n            }\n        }\n        return -1.0;\n    }\n}",
                "python": "from collections import defaultdict\n\nclass Solution:\n    def calcEquation(self, equations: list[list[str]], values: list[float], queries: list[list[str]]) -> list[float]:\n        graph = defaultdict(dict)\n        for (u, v), val in zip(equations, values):\n            graph[u][v] = val\n            graph[v][u] = 1.0 / val\n        def dfs(cur: str, target: str, product: float, visited: set) -> float:\n            if cur == target:\n                return product\n            visited.add(cur)\n            for nxt, weight in graph[cur].items():\n                if nxt not in visited:\n                    res = dfs(nxt, target, product * weight, visited)\n                    if res != -1.0:\n                        return res\n            return -1.0\n        ans = []\n        for u, v in queries:\n            if u not in graph or v not in graph:\n                ans.append(-1.0)\n            elif u == v:\n                ans.append(1.0)\n            else:\n                ans.append(dfs(u, v, 1.0, set()))\n        return ans"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public int openLock(String[] deadends, String target) {\n        Set<String> dead = new HashSet<>(Arrays.asList(deadends));\n        if (dead.contains(\"0000\")) return -1;\n        Queue<String> q = new LinkedList<>();\n        q.offer(\"0000\");\n        dead.add(\"0000\");\n        int steps = 0;\n        while (!q.isEmpty()) {\n            int size = q.size();\n            for (int k = 0; k < size; k++) {\n                String cur = q.poll();\n                if (cur.equals(target)) return steps;\n                for (String next : getNeighbors(cur)) {\n                    if (!dead.contains(next)) {\n                        dead.add(next);\n                        q.offer(next);\n                    }\n                }\n            }\n            steps++;\n        }\n        return -1;\n    }\n    private List<String> getNeighbors(String s) {\n        List<String> res = new ArrayList<>();\n        char[] chs = s.toCharArray();\n        for (int i = 0; i < 4; i++) {\n            char orig = chs[i];\n            chs[i] = (char) ((orig - '0' + 1) % 10 + '0');\n            res.add(new String(chs));\n            chs[i] = (char) ((orig - '0' + 9) % 10 + '0');\n            res.add(new String(chs));\n            chs[i] = orig;\n        }\n        return res;\n    }\n}",
                "python": "from collections import deque\n\nclass Solution:\n    def openLock(self, deadends: list[str], target: str) -> int:\n        dead = set(deadends)\n        if \"0000\" in dead: return -1\n        q = deque([(\"0000\", 0)])\n        dead.add(\"0000\")\n        while q:\n            cur, d = q.popleft()\n            if cur == target: return d\n            for i in range(4):\n                digit = int(cur[i])\n                for diff in (1, -1):\n                    nxt_digit = (digit + diff) % 10\n                    nxt = cur[:i] + str(nxt_digit) + cur[i+1:]\n                    if nxt not in dead:\n                        dead.add(nxt)\n                        q.append((nxt, d + 1))\n        return -1"
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
                "java": "import java.util.*;\nclass Solution {\n    public int openLock(String[] deadends, String target) {\n        Set<String> dead = new HashSet<>(Arrays.asList(deadends));\n        if (dead.contains(\"0000\") || dead.contains(target)) return -1;\n        if (target.equals(\"0000\")) return 0;\n        Set<String> beginSet = new HashSet<>();\n        Set<String> endSet = new HashSet<>();\n        beginSet.add(\"0000\");\n        endSet.add(target);\n        int steps = 0;\n        while (!beginSet.isEmpty() && !endSet.isEmpty()) {\n            if (beginSet.size() > endSet.size()) {\n                Set<String> temp = beginSet;\n                beginSet = endSet;\n                endSet = temp;\n            }\n            Set<String> nextSet = new HashSet<>();\n            for (String cur : beginSet) {\n                for (String next : getNeighbors(cur)) {\n                    if (endSet.contains(next)) return steps + 1;\n                    if (!dead.contains(next)) {\n                        dead.add(next);\n                        nextSet.add(next);\n                    }\n                }\n            }\n            beginSet = nextSet;\n            steps++;\n        }\n        return -1;\n    }\n    private List<String> getNeighbors(String s) {\n        List<String> res = new ArrayList<>();\n        char[] chs = s.toCharArray();\n        for (int i = 0; i < 4; i++) {\n            char orig = chs[i];\n            chs[i] = (char) ((orig - '0' + 1) % 10 + '0');\n            res.add(new String(chs));\n            chs[i] = (char) ((orig - '0' + 9) % 10 + '0');\n            res.add(new String(chs));\n            chs[i] = orig;\n        }\n        return res;\n    }\n}",
                "python": "class Solution:\n    def openLock(self, deadends: list[str], target: str) -> int:\n        dead = set(deadends)\n        if \"0000\" in dead or target in dead:\n            return -1\n        if target == \"0000\":\n            return 0\n        begin_set = {\"0000\"}\n        end_set = {target}\n        steps = 0\n        while begin_set and end_set:\n            if len(begin_set) > len(end_set):\n                begin_set, end_set = end_set, begin_set\n            next_set = set()\n            for cur in begin_set:\n                for i in range(4):\n                    digit = int(cur[i])\n                    for diff in (1, -1):\n                        nxt = cur[:i] + str((digit + diff) % 10) + cur[i+1:]\n                        if nxt in end_set:\n                            return steps + 1\n                        if nxt not in dead:\n                            dead.add(nxt)\n                            next_set.add(nxt)\n            begin_set = next_set\n            steps += 1\n        return -1"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public List<Integer> findMinHeightTrees(int n, int[][] edges) {\n        if (n <= 2) {\n            List<Integer> res = new ArrayList<>();\n            for (int i = 0; i < n; i++) res.add(i);\n            return res;\n        }\n        List<Set<Integer>> adj = new ArrayList<>();\n        for (int i = 0; i < n; i++) adj.add(new HashSet<>());\n        for (int[] e : edges) {\n            adj.get(e[0]).add(e[1]);\n            adj.get(e[1]).add(e[0]);\n        }\n        List<Integer> leaves = new ArrayList<>();\n        for (int i = 0; i < n; i++) {\n            if (adj.get(i).size() == 1) leaves.add(i);\n        }\n        int remaining = n;\n        while (remaining > 2) {\n            remaining -= leaves.size();\n            List<Integer> newLeaves = new ArrayList<>();\n            for (int leaf : leaves) {\n                int neighbor = adj.get(leaf).iterator().next();\n                adj.get(neighbor).remove(leaf);\n                if (adj.get(neighbor).size() == 1) newLeaves.add(neighbor);\n            }\n            leaves = newLeaves;\n        }\n        return leaves;\n    }\n}",
                "python": "class Solution:\n    def findMinHeightTrees(self, n: int, edges: list[list[int]]) -> list[int]:\n        if n <= 2: return list(range(n))\n        adj = [set() for _ in range(n)]\n        for u, v in edges:\n            adj[u].add(v)\n            adj[v].add(u)\n        leaves = [i for i in range(n) if len(adj[i]) == 1]\n        rem = n\n        while rem > 2:\n            rem -= len(leaves)\n            new_leaves = []\n            for leaf in leaves:\n                nbr = adj[leaf].pop()\n                adj[nbr].remove(leaf)\n                if len(adj[nbr]) == 1:\n                    new_leaves.append(nbr)\n            leaves = new_leaves\n        return leaves"
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
                "java": "import java.util.*;\nclass Solution {\n    public List<Integer> findMinHeightTrees(int n, int[][] edges) {\n        if (n <= 2) {\n            List<Integer> res = new ArrayList<>();\n            for (int i = 0; i < n; i++) res.add(i);\n            return res;\n        }\n        List<Set<Integer>> adj = new ArrayList<>();\n        for (int i = 0; i < n; i++) adj.add(new HashSet<>());\n        for (int[] e : edges) {\n            adj.get(e[0]).add(e[1]);\n            adj.get(e[1]).add(e[0]);\n        }\n        List<Integer> leaves = new ArrayList<>();\n        for (int i = 0; i < n; i++) {\n            if (adj.get(i).size() == 1) leaves.add(i);\n        }\n        int remaining = n;\n        while (remaining > 2) {\n            remaining -= leaves.size();\n            List<Integer> newLeaves = new ArrayList<>();\n            for (int leaf : leaves) {\n                int neighbor = adj.get(leaf).iterator().next();\n                adj.get(neighbor).remove(leaf);\n                if (adj.get(neighbor).size() == 1) {\n                    newLeaves.add(neighbor);\n                }\n            }\n            leaves = newLeaves;\n        }\n        return leaves;\n    }\n}",
                "python": "class Solution:\n    def findMinHeightTrees(self, n: int, edges: list[list[int]]) -> list[int]:\n        if n <= 2:\n            return list(range(n))\n        adj = [set() for _ in range(n)]\n        for u, v in edges:\n            adj[u].add(v)\n            adj[v].add(u)\n        leaves = [i for i in range(n) if len(adj[i]) == 1]\n        remaining = n\n        while remaining > 2:\n            remaining -= len(leaves)\n            new_leaves = []\n            for leaf in leaves:\n                neighbor = adj[leaf].pop()\n                adj[neighbor].remove(leaf)\n                if len(adj[neighbor]) == 1:\n                    new_leaves.append(neighbor)\n            leaves = new_leaves\n        return leaves"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public boolean canFinish(int numCourses, int[][] prerequisites) {\n        List<Integer>[] adj = new List[numCourses];\n        for (int i = 0; i < numCourses; i++) adj[i] = new ArrayList<>();\n        for (int[] p : prerequisites) adj[p[1]].add(p[0]);\n        int[] visited = new int[numCourses];\n        for (int i = 0; i < numCourses; i++) {\n            if (visited[i] == 0 && hasCycle(adj, i, visited)) return false;\n        }\n        return true;\n    }\n    private boolean hasCycle(List<Integer>[] adj, int u, int[] visited) {\n        visited[u] = 1;\n        for (int v : adj[u]) {\n            if (visited[v] == 1) return true;\n            if (visited[v] == 0 && hasCycle(adj, v, visited)) return true;\n        }\n        visited[u] = 2;\n        return false;\n    }\n}",
                "python": "from collections import defaultdict\n\nclass Solution:\n    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:\n        adj = defaultdict(list)\n        for dest, src in prerequisites:\n            adj[src].append(dest)\n        visited = [0] * numCourses\n        def dfs(u):\n            visited[u] = 1\n            for v in adj[u]:\n                if visited[v] == 1: return True\n                if visited[v] == 0 and dfs(v): return True\n            visited[u] = 2\n            return False\n        for i in range(numCourses):\n            if visited[i] == 0 and dfs(i): return False\n        return True"
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
                "java": "import java.util.*;\nclass Solution {\n    public boolean canFinish(int numCourses, int[][] prerequisites) {\n        int[] inDegree = new int[numCourses];\n        List<Integer>[] adj = new List[numCourses];\n        for (int i = 0; i < numCourses; i++) adj[i] = new ArrayList<>();\n        for (int[] p : prerequisites) {\n            adj[p[1]].add(p[0]);\n            inDegree[p[0]]++;\n        }\n        Queue<Integer> q = new LinkedList<>();\n        for (int i = 0; i < numCourses; i++) {\n            if (inDegree[i] == 0) q.offer(i);\n        }\n        int count = 0;\n        while (!q.isEmpty()) {\n            int u = q.poll();\n            count++;\n            for (int v : adj[u]) {\n                if (--inDegree[v] == 0) {\n                    q.offer(v);\n                }\n            }\n        }\n        return count == numCourses;\n    }\n}",
                "python": "from collections import deque, defaultdict\n\nclass Solution:\n    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:\n        in_degree = [0] * numCourses\n        adj = defaultdict(list)\n        for dest, src in prerequisites:\n            adj[src].append(dest)\n            in_degree[dest] += 1\n        q = deque([i for i in range(numCourses) if in_degree[i] == 0])\n        count = 0\n        while q:\n            u = q.popleft()\n            count += 1\n            for v in adj[u]:\n                in_degree[v] -= 1\n                if in_degree[v] == 0:\n                    q.append(v)\n        return count == numCourses"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public int[] findOrder(int numCourses, int[][] prerequisites) {\n        List<Integer>[] adj = new List[numCourses];\n        for (int i = 0; i < numCourses; i++) adj[i] = new ArrayList<>();\n        for (int[] p : prerequisites) adj[p[1]].add(p[0]);\n        int[] visited = new int[numCourses];\n        List<Integer> order = new ArrayList<>();\n        for (int i = 0; i < numCourses; i++) {\n            if (visited[i] == 0 && dfs(adj, i, visited, order)) return new int[0];\n        }\n        Collections.reverse(order);\n        int[] res = new int[numCourses];\n        for (int i = 0; i < numCourses; i++) res[i] = order.get(i);\n        return res;\n    }\n    private boolean dfs(List<Integer>[] adj, int u, int[] visited, List<Integer> order) {\n        visited[u] = 1;\n        for (int v : adj[u]) {\n            if (visited[v] == 1) return true;\n            if (visited[v] == 0 && dfs(adj, v, visited, order)) return true;\n        }\n        visited[u] = 2;\n        order.add(u);\n        return false;\n    }\n}",
                "python": "from collections import defaultdict\n\nclass Solution:\n    def findOrder(self, numCourses: int, prerequisites: list[list[int]]) -> list[int]:\n        adj = defaultdict(list)\n        for dest, src in prerequisites:\n            adj[src].append(dest)\n        visited = [0] * numCourses\n        order = []\n        def dfs(u):\n            visited[u] = 1\n            for v in adj[u]:\n                if visited[v] == 1: return True\n                if visited[v] == 0 and dfs(v): return True\n            visited[u] = 2\n            order.append(u)\n            return False\n        for i in range(numCourses):\n            if visited[i] == 0 and dfs(i): return []\n        return order[::-1]"
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
                "java": "import java.util.*;\nclass Solution {\n    public int[] findOrder(int numCourses, int[][] prerequisites) {\n        int[] inDegree = new int[numCourses];\n        List<Integer>[] adj = new List[numCourses];\n        for (int i = 0; i < numCourses; i++) adj[i] = new ArrayList<>();\n        for (int[] p : prerequisites) {\n            adj[p[1]].add(p[0]);\n            inDegree[p[0]]++;\n        }\n        Queue<Integer> q = new LinkedList<>();\n        for (int i = 0; i < numCourses; i++) {\n            if (inDegree[i] == 0) q.offer(i);\n        }\n        int[] order = new int[numCourses];\n        int idx = 0;\n        while (!q.isEmpty()) {\n            int u = q.poll();\n            order[idx++] = u;\n            for (int v : adj[u]) {\n                if (--inDegree[v] == 0) {\n                    q.offer(v);\n                }\n            }\n        }\n        return idx == numCourses ? order : new int[0];\n    }\n}",
                "python": "from collections import deque, defaultdict\n\nclass Solution:\n    def findOrder(self, numCourses: int, prerequisites: list[list[int]]) -> list[int]:\n        in_degree = [0] * numCourses\n        adj = defaultdict(list)\n        for dest, src in prerequisites:\n            adj[src].append(dest)\n            in_degree[dest] += 1\n        q = deque([i for i in range(numCourses) if in_degree[i] == 0])\n        order = []\n        while q:\n            u = q.popleft()\n            order.append(u)\n            for v in adj[u]:\n                in_degree[v] -= 1\n                if in_degree[v] == 0:\n                    q.append(v)\n        return order if len(order) == numCourses else []"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public List<Integer> eventualSafeNodes(int[][] graph) {\n        int n = graph.length;\n        int[] color = new int[n];\n        List<Integer> res = new ArrayList<>();\n        for (int i = 0; i < n; i++) {\n            if (isSafe(graph, i, color)) res.add(i);\n        }\n        return res;\n    }\n    private boolean isSafe(int[][] g, int u, int[] color) {\n        if (color[u] != 0) return color[u] == 2;\n        color[u] = 1;\n        for (int v : g[u]) {\n            if (!isSafe(g, v, color)) return false;\n        }\n        color[u] = 2;\n        return true;\n    }\n}",
                "python": "class Solution:\n    def eventualSafeNodes(self, graph: list[list[int]]) -> list[int]:\n        n = len(graph)\n        color = [0] * n\n        def is_safe(u):\n            if color[u] != 0: return color[u] == 2\n            color[u] = 1\n            for v in graph[u]:\n                if not is_safe(v): return False\n            color[u] = 2\n            return True\n        return [i for i in range(n) if is_safe(i)]"
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
                "java": "import java.util.*;\nclass Solution {\n    public List<Integer> eventualSafeNodes(int[][] graph) {\n        int n = graph.length;\n        int[] color = new int[n];\n        List<Integer> safe = new ArrayList<>();\n        for (int i = 0; i < n; i++) {\n            if (dfs(graph, i, color)) {\n                safe.add(i);\n            }\n        }\n        return safe;\n    }\n    private boolean dfs(int[][] graph, int u, int[] color) {\n        if (color[u] != 0) return color[u] == 2;\n        color[u] = 1;\n        for (int v : graph[u]) {\n            if (!dfs(graph, v, color)) return false;\n        }\n        color[u] = 2;\n        return true;\n    }\n}",
                "python": "class Solution:\n    def eventualSafeNodes(self, graph: list[list[int]]) -> list[int]:\n        n = len(graph)\n        color = [0] * n\n        def dfs(u: int) -> bool:\n            if color[u] != 0:\n                return color[u] == 2\n            color[u] = 1\n            for v in graph[u]:\n                if not dfs(v):\n                    return False\n            color[u] = 2\n            return True\n        return [i for i in range(n) if dfs(i)]"
            }
        }
    },
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
                "java": "class Solution {\n    public int longestIncreasingPath(int[][] matrix) {\n        int m = matrix.length, n = matrix[0].length;\n        int max = 0;\n        int[][] memo = new int[m][n];\n        for (int i = 0; i < m; i++) {\n            for (int j = 0; j < n; j++) {\n                max = Math.max(max, dfs(matrix, i, j, memo));\n            }\n        }\n        return max;\n    }\n    private int dfs(int[][] mat, int r, int c, int[][] memo) {\n        if (memo[r][c] != 0) return memo[r][c];\n        int max = 1;\n        int[][] dirs = {{1,0}, {-1,0}, {0,1}, {0,-1}};\n        for (int[] d : dirs) {\n            int nr = r + d[0], nc = c + d[1];\n            if (nr >= 0 && nr < mat.length && nc >= 0 && nc < mat[0].length && mat[nr][nc] > mat[r][c]) {\n                max = Math.max(max, 1 + dfs(mat, nr, nc, memo));\n            }\n        }\n        return memo[r][c] = max;\n    }\n}",
                "python": "class Solution:\n    def longestIncreasingPath(self, matrix: list[list[int]]) -> int:\n        m, n = len(matrix), len(matrix[0])\n        memo = {}\n        def dfs(r, c):\n            if (r, c) in memo: return memo[(r, c)]\n            ans = 1\n            for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):\n                nr, nc = r + dr, c + dc\n                if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] > matrix[r][c]:\n                    ans = max(ans, 1 + dfs(nr, nc))\n            memo[(r, c)] = ans\n            return ans\n        return max(dfs(i, j) for i in range(m) for j in range(n))"
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
                "java": "class Solution {\n    public int longestIncreasingPath(int[][] matrix) {\n        int m = matrix.length, n = matrix[0].length;\n        int[][] memo = new int[m][n];\n        int maxPath = 0;\n        for (int i = 0; i < m; i++) {\n            for (int j = 0; j < n; j++) {\n                maxPath = Math.max(maxPath, dfs(matrix, i, j, memo, m, n));\n            }\n        }\n        return maxPath;\n    }\n    private int dfs(int[][] mat, int r, int c, int[][] memo, int m, int n) {\n        if (memo[r][c] != 0) return memo[r][c];\n        int max = 1;\n        int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};\n        for (int[] d : dirs) {\n            int nr = r + d[0], nc = c + d[1];\n            if (nr >= 0 && nr < m && nc >= 0 && nc < n && mat[nr][nc] > mat[r][c]) {\n                max = Math.max(max, 1 + dfs(mat, nr, nc, memo, m, n));\n            }\n        }\n        return memo[r][c] = max;\n    }\n}",
                "python": "class Solution:\n    def longestIncreasingPath(self, matrix: list[list[int]]) -> int:\n        m, n = len(matrix), len(matrix[0])\n        memo = [[0] * n for _ in range(m)]\n        def dfs(r: int, c: int) -> int:\n            if memo[r][c] != 0:\n                return memo[r][c]\n            max_len = 1\n            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n                nr, nc = r + dr, c + dc\n                if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] > matrix[r][c]:\n                    max_len = max(max_len, 1 + dfs(nr, nc))\n            memo[r][c] = max_len\n            return max_len\n        return max(dfs(i, j) for i in range(m) for j in range(n))"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public int[] findRedundantConnection(int[][] edges) {\n        int n = edges.length;\n        List<Integer>[] adj = new List[n + 1];\n        for (int i = 1; i <= n; i++) adj[i] = new ArrayList<>();\n        for (int[] e : edges) {\n            boolean[] visited = new boolean[n + 1];\n            if (hasPath(adj, e[0], e[1], visited)) return e;\n            adj[e[0]].add(e[1]);\n            adj[e[1]].add(e[0]);\n        }\n        return new int[0];\n    }\n    private boolean hasPath(List<Integer>[] adj, int u, int target, boolean[] visited) {\n        if (u == target) return true;\n        visited[u] = true;\n        for (int v : adj[u]) {\n            if (!visited[v] && hasPath(adj, v, target, visited)) return true;\n        }\n        return false;\n    }\n}",
                "python": "from collections import defaultdict\n\nclass Solution:\n    def findRedundantConnection(self, edges: list[list[int]]) -> list[int]:\n        adj = defaultdict(list)\n        def has_path(u, target, visited):\n            if u == target: return True\n            visited.add(u)\n            for v in adj[u]:\n                if v not in visited and has_path(v, target, visited):\n                    return True\n            return False\n        for u, v in edges:\n            if u in adj and v in adj and has_path(u, v, set()):\n                return [u, v]\n            adj[u].append(v)\n            adj[v].append(u)\n        return []"
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
                "java": "class Solution {\n    public int[] findRedundantConnection(int[][] edges) {\n        int n = edges.length;\n        int[] parent = new int[n + 1];\n        for (int i = 1; i <= n; i++) parent[i] = i;\n        for (int[] edge : edges) {\n            int rootU = find(parent, edge[0]);\n            int rootV = find(parent, edge[1]);\n            if (rootU == rootV) return edge;\n            parent[rootU] = rootV;\n        }\n        return new int[0];\n    }\n    private int find(int[] parent, int i) {\n        if (parent[i] == i) return i;\n        return parent[i] = find(parent, parent[i]);\n    }\n}",
                "python": "class Solution:\n    def findRedundantConnection(self, edges: list[list[int]]) -> list[int]:\n        parent = list(range(len(edges) + 1))\n        def find(i):\n            if parent[i] == i:\n                return i\n            parent[i] = find(parent[i])\n            return parent[i]\n        for u, v in edges:\n            ru, rv = find(u), find(v)\n            if ru == rv:\n                return [u, v]\n            parent[ru] = rv\n        return []"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public List<List<String>> accountsMerge(List<List<String>> accounts) {\n        Map<String, List<String>> g = new HashMap<>();\n        Map<String, String> emailToName = new HashMap<>();\n        for (List<String> acc : accounts) {\n            String name = acc.get(0);\n            String first = acc.get(1);\n            for (int i = 1; i < acc.size(); i++) {\n                String email = acc.get(i);\n                emailToName.put(email, name);\n                g.computeIfAbsent(first, k -> new ArrayList<>()).add(email);\n                g.computeIfAbsent(email, k -> new ArrayList<>()).add(first);\n            }\n        }\n        Set<String> visited = new HashSet<>();\n        List<List<String>> res = new ArrayList<>();\n        for (String email : emailToName.keySet()) {\n            if (visited.add(email)) {\n                List<String> comp = new ArrayList<>();\n                dfs(g, email, visited, comp);\n                Collections.sort(comp);\n                comp.add(0, emailToName.get(email));\n                res.add(comp);\n            }\n        }\n        return res;\n    }\n    private void dfs(Map<String, List<String>> g, String u, Set<String> visited, List<String> comp) {\n        comp.add(u);\n        for (String v : g.getOrDefault(u, Collections.emptyList())) {\n            if (visited.add(v)) dfs(g, v, visited, comp);\n        }\n    }\n}",
                "python": "from collections import defaultdict\n\nclass Solution:\n    def accountsMerge(self, accounts: list[list[str]]) -> list[list[str]]:\n        g = defaultdict(list)\n        email_to_name = {}\n        for acc in accounts:\n            name = acc[0]\n            first = acc[1]\n            for email in acc[1:]:\n                email_to_name[email] = name\n                g[first].append(email)\n                g[email].append(first)\n        visited = set()\n        res = []\n        for email in email_to_name:\n            if email not in visited:\n                comp = []\n                stack = [email]\n                visited.add(email)\n                while stack:\n                    cur = stack.pop()\n                    comp.append(cur)\n                    for nxt in g[cur]:\n                        if nxt not in visited:\n                            visited.add(nxt)\n                            stack.append(nxt)\n                comp.sort()\n                res.append([email_to_name[email]] + comp)\n        return res"
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
                "java": "import java.util.*;\nclass Solution {\n    private Map<String, String> parent = new HashMap<>();\n    public List<List<String>> accountsMerge(List<List<String>> accounts) {\n        Map<String, String> owner = new HashMap<>();\n        for (List<String> acc : accounts) {\n            String name = acc.get(0);\n            for (int i = 1; i < acc.size(); i++) {\n                String email = acc.get(i);\n                owner.put(email, name);\n                parent.putIfAbsent(email, email);\n                union(acc.get(1), email);\n            }\n        }\n        Map<String, TreeSet<String>> unions = new HashMap<>();\n        for (String email : owner.keySet()) {\n            String root = find(email);\n            unions.computeIfAbsent(root, k -> new TreeSet<>()).add(email);\n        }\n        List<List<String>> res = new ArrayList<>();\n        for (String root : unions.keySet()) {\n            List<String> emails = new ArrayList<>(unions.get(root));\n            emails.add(0, owner.get(root));\n            res.add(emails);\n        }\n        return res;\n    }\n    private String find(String s) {\n        if (parent.get(s).equals(s)) return s;\n        parent.put(s, find(parent.get(s)));\n        return parent.get(s);\n    }\n    private void union(String a, String b) {\n        String ra = find(a), rb = find(b);\n        if (!ra.equals(rb)) parent.put(ra, rb);\n    }\n}",
                "python": "class Solution:\n    def accountsMerge(self, accounts: list[list[str]]) -> list[list[str]]:\n        parent = {}\n        owner = {}\n        def find(s):\n            if parent[s] == s: return s\n            parent[s] = find(parent[s])\n            return parent[s]\n        def union(a, b):\n            ra, rb = find(a), find(b)\n            if ra != rb: parent[ra] = rb\n        for acc in accounts:\n            name = acc[0]\n            first = acc[1]\n            for email in acc[1:]:\n                owner[email] = name\n                if email not in parent: parent[email] = email\n                if first not in parent: parent[first] = first\n                union(first, email)\n        from collections import defaultdict\n        groups = defaultdict(list)\n        for email in owner:\n            groups[find(email)].append(email)\n        return [[owner[root]] + sorted(emails) for root, emails in groups.items()]"
            }
        }
    },
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
                "java": "class Solution {\n    public boolean equationsPossible(String[] equations) {\n        int[] parent = new int[26];\n        for (int i = 0; i < 26; i++) parent[i] = i;\n        for (String eq : equations) {\n            if (eq.charAt(1) == '=') {\n                union(parent, eq.charAt(0) - 'a', eq.charAt(3) - 'a');\n            }\n        }\n        for (String eq : equations) {\n            if (eq.charAt(1) == '!') {\n                if (find(parent, eq.charAt(0) - 'a') == find(parent, eq.charAt(3) - 'a')) {\n                    return false;\n                }\n            }\n        }\n        return true;\n    }\n    private int find(int[] p, int i) {\n        if (p[i] == i) return i;\n        return p[i] = find(p, p[i]);\n    }\n    private void union(int[] p, int i, int j) {\n        int ri = find(p, i), rj = find(p, j);\n        if (ri != rj) p[ri] = rj;\n    }\n}",
                "python": "class Solution:\n    def equationsPossible(self, equations: list[str]) -> bool:\n        parent = list(range(26))\n        def find(i):\n            if parent[i] == i: return i\n            parent[i] = find(parent[i])\n            return parent[i]\n        def union(i, j):\n            ri, rj = find(i), find(j)\n            if ri != rj: parent[ri] = rj\n        for eq in equations:\n            if eq[1] == '=':\n                union(ord(eq[0]) - ord('a'), ord(eq[3]) - ord('a'))\n        for eq in equations:\n            if eq[1] == '!':\n                if find(ord(eq[0]) - ord('a')) == find(ord(eq[3]) - ord('a')):\n                    return False\n        return True"
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
                "java": "class Solution {\n    public boolean equationsPossible(String[] equations) {\n        int[] parent = new int[26];\n        for (int i = 0; i < 26; i++) parent[i] = i;\n        for (String eq : equations) {\n            if (eq.charAt(1) == '=') {\n                int u = eq.charAt(0) - 'a';\n                int v = eq.charAt(3) - 'a';\n                union(parent, u, v);\n            }\n        }\n        for (String eq : equations) {\n            if (eq.charAt(1) == '!') {\n                int u = eq.charAt(0) - 'a';\n                int v = eq.charAt(3) - 'a';\n                if (find(parent, u) == find(parent, v)) {\n                    return false;\n                }\n            }\n        }\n        return true;\n    }\n    private int find(int[] p, int i) {\n        if (p[i] == i) return i;\n        return p[i] = find(p, p[i]);\n    }\n    private void union(int[] p, int i, int j) {\n        int ri = find(p, i);\n        int rj = find(p, j);\n        if (ri != rj) p[ri] = rj;\n    }\n}",
                "python": "class Solution:\n    def equationsPossible(self, equations: list[str]) -> bool:\n        parent = list(range(26))\n        def find(i: int) -> int:\n            if parent[i] == i:\n                return i\n            parent[i] = find(parent[i])\n            return parent[i]\n        def union(i: int, j: int):\n            ri, rj = find(i), find(j)\n            if ri != rj:\n                parent[ri] = rj\n        for eq in equations:\n            if eq[1] == '=':\n                union(ord(eq[0]) - ord('a'), ord(eq[3]) - ord('a'))\n        for eq in equations:\n            if eq[1] == '!':\n                if find(ord(eq[0]) - ord('a')) == find(ord(eq[3]) - ord('a')):\n                    return False\n        return True"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public int makeConnected(int n, int[][] connections) {\n        if (connections.length < n - 1) return -1;\n        List<Integer>[] adj = new List[n];\n        for (int i = 0; i < n; i++) adj[i] = new ArrayList<>();\n        for (int[] c : connections) {\n            adj[c[0]].add(c[1]);\n            adj[c[1]].add(c[0]);\n        }\n        boolean[] visited = new boolean[n];\n        int components = 0;\n        for (int i = 0; i < n; i++) {\n            if (!visited[i]) {\n                components++;\n                dfs(adj, i, visited);\n            }\n        }\n        return components - 1;\n    }\n    private void dfs(List<Integer>[] adj, int u, boolean[] visited) {\n        visited[u] = true;\n        for (int v : adj[u]) {\n            if (!visited[v]) dfs(adj, v, visited);\n        }\n    }\n}",
                "python": "class Solution:\n    def makeConnected(self, n: int, connections: list[list[int]]) -> int:\n        if len(connections) < n - 1: return -1\n        from collections import defaultdict\n        adj = defaultdict(list)\n        for u, v in connections:\n            adj[u].append(v)\n            adj[v].append(u)\n        visited = set()\n        comp = 0\n        def dfs(u):\n            visited.add(u)\n            for v in adj[u]:\n                if v not in visited: dfs(v)\n        for i in range(n):\n            if i not in visited:\n                comp += 1\n                dfs(i)\n        return comp - 1"
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
                "java": "class Solution {\n    public int makeConnected(int n, int[][] connections) {\n        if (connections.length < n - 1) return -1;\n        int[] parent = new int[n];\n        for (int i = 0; i < n; i++) parent[i] = i;\n        int components = n;\n        for (int[] c : connections) {\n            int ru = find(parent, c[0]);\n            int rv = find(parent, c[1]);\n            if (ru != rv) {\n                parent[ru] = rv;\n                components--;\n            }\n        }\n        return components - 1;\n    }\n    private int find(int[] p, int i) {\n        if (p[i] == i) return i;\n        return p[i] = find(p, p[i]);\n    }\n}",
                "python": "class Solution:\n    def makeConnected(self, n: int, connections: list[list[int]]) -> int:\n        if len(connections) < n - 1:\n            return -1\n        parent = list(range(n))\n        def find(i: int) -> int:\n            if parent[i] == i:\n                return i\n            parent[i] = find(parent[i])\n            return parent[i]\n        components = n\n        for u, v in connections:\n            ru, rv = find(u), find(v)\n            if ru != rv:\n                parent[ru] = rv\n                components -= 1\n        return components - 1"
            }
        }
    }
]

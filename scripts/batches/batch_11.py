# Batch 11: Questions 251 to 275

def get_batch():
    return [
    {
        "seq": 251,
        "whyNext": "0/1 Knapsack boolean subset sum: if totalSum % 2 != 0 return false; target = totalSum / 2; backwards 1D DP.",
        "brute": {
            "idea": "Recursively test all subsets to see if any sums to totalSum / 2.",
            "steps": [
                "dfs(index, target): include or exclude nums[index]."
            ],
            "time": "O(2^n)",
            "space": "O(n)",
            "whySlow": "Exponential recursion.",
            "code": {
                "java": "class Solution {\n    public boolean canPartition(int[] nums) {\n        int sum = 0;\n        for (int x : nums) sum += x;\n        if (sum % 2 != 0) return false;\n        int target = sum / 2;\n        boolean[] dp = new boolean[target + 1];\n        dp[0] = true;\n        for (int num : nums) {\n            for (int j = target; j >= num; j--) {\n                dp[j] = dp[j] || dp[j - num];\n            }\n        }\n        return dp[target];\n    }\n}",
                "python": "class Solution:\n    def canPartition(self, nums: list[int]) -> bool:\n        total = sum(nums)\n        if total % 2 != 0: return False\n        target = total // 2\n        dp = [False] * (target + 1)\n        dp[0] = True\n        for num in nums:\n            for j in range(target, num - 1, -1):\n                dp[j] = dp[j] or dp[j - num]\n        return dp[target]"
            }
        },
        "optimal": {
            "idea": "0/1 Knapsack with 1D boolean array: loop backwards from target down to num: dp[j] |= dp[j - num].",
            "steps": [
                "Sum all elements. If sum % 2 != 0 return false.",
                "target = sum / 2; boolean[] dp = new boolean[target + 1]; dp[0] = true.",
                "For num in nums: for j from target down to num: dp[j] |= dp[j - num].",
                "Return dp[target]."
            ],
            "time": "O(n * target)",
            "space": "O(target)",
            "code": {
                "java": "class Solution {\n    public boolean canPartition(int[] nums) {\n        int sum = 0;\n        for (int x : nums) sum += x;\n        if (sum % 2 != 0) return false;\n        int target = sum / 2;\n        boolean[] dp = new boolean[target + 1];\n        dp[0] = true;\n        for (int num : nums) {\n            for (int j = target; j >= num; j--) {\n                dp[j] = dp[j] || dp[j - num];\n            }\n        }\n        return dp[target];\n    }\n}",
                "python": "class Solution:\n    def canPartition(self, nums: list[int]) -> bool:\n        total = sum(nums)\n        if total % 2 != 0:\n            return False\n        target = total // 2\n        dp = [False] * (target + 1)\n        dp[0] = True\n        for num in nums:\n            for j in range(target, num - 1, -1):\n                dp[j] = dp[j] or dp[j - num]\n        return dp[target]"
            }
        }
    },
    {
        "seq": 252,
        "whyNext": "Builds on Partition Equal Subset Sum: smash stones into two subsets S1 and S2; minimize |S1 - S2| <=> maximize S1 <= total / 2.",
        "brute": {
            "idea": "Explore all 2^n partitions of signs (+/-) and find minimum non-negative sum.",
            "steps": [
                "dfs(idx, sum): try adding or subtracting stones[idx]."
            ],
            "time": "O(2^n)",
            "space": "O(n)",
            "whySlow": "Exponential recursion.",
            "code": {
                "java": "class Solution {\n    public int lastStoneWeightII(int[] stones) {\n        int sum = 0;\n        for (int s : stones) sum += s;\n        int target = sum / 2;\n        boolean[] dp = new boolean[target + 1];\n        dp[0] = true;\n        for (int s : stones) {\n            for (int j = target; j >= s; j--) {\n                dp[j] = dp[j] || dp[j - s];\n            }\n        }\n        for (int j = target; j >= 0; j--) {\n            if (dp[j]) return sum - 2 * j;\n        }\n        return 0;\n    }\n}",
                "python": "class Solution:\n    def lastStoneWeightII(self, stones: list[int]) -> int:\n        total = sum(stones)\n        target = total // 2\n        dp = [False] * (target + 1)\n        dp[0] = True\n        for s in stones:\n            for j in range(target, s - 1, -1):\n                dp[j] = dp[j] or dp[j - s]\n        for j in range(target, -1, -1):\n            if dp[j]:\n                return total - 2 * j\n        return 0"
            }
        },
        "optimal": {
            "idea": "Find largest subset sum <= sum / 2 using 0/1 knapsack. Min weight remaining is total - 2 * max_subset_sum.",
            "steps": [
                "Calculate totalSum and target = totalSum / 2.",
                "boolean[] dp = new boolean[target + 1]; dp[0] = true.",
                "For stone in stones: for j from target down to stone: dp[j] |= dp[j - stone].",
                "Find largest j where dp[j] == true; return totalSum - 2 * j."
            ],
            "time": "O(n * target)",
            "space": "O(target)",
            "code": {
                "java": "class Solution {\n    public int lastStoneWeightII(int[] stones) {\n        int total = 0;\n        for (int s : stones) total += s;\n        int target = total / 2;\n        boolean[] dp = new boolean[target + 1];\n        dp[0] = true;\n        for (int s : stones) {\n            for (int j = target; j >= s; j--) {\n                dp[j] = dp[j] || dp[j - s];\n            }\n        }\n        for (int j = target; j >= 0; j--) {\n            if (dp[j]) return total - 2 * j;\n        }\n        return 0;\n    }\n}",
                "python": "class Solution:\n    def lastStoneWeightII(self, stones: list[int]) -> int:\n        total = sum(stones)\n        target = total // 2\n        dp = [False] * (target + 1)\n        dp[0] = True\n        for s in stones:\n            for j in range(target, s - 1, -1):\n                dp[j] = dp[j] or dp[j - s]\n        for j in range(target, -1, -1):\n            if dp[j]:\n                return total - 2 * j\n        return 0"
            }
        }
    },
    {
        "seq": 253,
        "whyNext": "Mathematical integer division: break into maximum number of 3s; if remainder is 1, take 2*2 instead of 3*1; if 2, take 2.",
        "brute": {
            "idea": "DP: dp[i] = max(j * (i - j), j * dp[i - j]) for j from 1 to i - 1.",
            "steps": [
                "Compute dp[i] for i = 2..n."
            ],
            "time": "O(n^2)",
            "space": "O(n)",
            "whySlow": "Quadratic dynamic programming when math solution runs in O(log n) or O(1).",
            "code": {
                "java": "class Solution {\n    public int integerBreak(int n) {\n        int[] dp = new int[n + 1];\n        dp[1] = 1;\n        for (int i = 2; i <= n; i++) {\n            for (int j = 1; j < i; j++) {\n                dp[i] = Math.max(dp[i], Math.max(j * (i - j), j * dp[i - j]));\n            }\n        }\n        return dp[n];\n    }\n}",
                "python": "class Solution:\n    def integerBreak(self, n: int) -> int:\n        dp = [0] * (n + 1)\n        dp[1] = 1\n        for i in range(2, n + 1):\n            for j in range(1, i):\n                dp[i] = max(dp[i], j * (i - j), j * dp[i - j])\n        return dp[n]"
            }
        },
        "optimal": {
            "idea": "Greedy factors of 3: base cases n <= 3 return n - 1. For n > 3: multiply by 3 while n > 4; multiply remaining n.",
            "steps": [
                "If n <= 3 return n - 1.",
                "prod = 1.",
                "While n > 4: prod *= 3, n -= 3.",
                "Return prod * n."
            ],
            "time": "O(n)",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public int integerBreak(int n) {\n        if (n <= 3) return n - 1;\n        int prod = 1;\n        while (n > 4) {\n            prod *= 3;\n            n -= 3;\n        }\n        return prod * n;\n    }\n}",
                "python": "class Solution:\n    def integerBreak(self, n: int) -> int:\n        if n <= 3:\n            return n - 1\n        prod = 1\n        while n > 4:\n            prod *= 3\n            n -= 3\n        return prod * n"
            }
        }
    },
    {
        "seq": 254,
        "whyNext": "Entry to Chapter 15 (2D DP): dp[r][c] = dp[r-1][c] + dp[r][c-1]; 1D row array compresses space to O(n).",
        "brute": {
            "idea": "Recursively branch right and down.",
            "steps": [
                "dfs(r, c): dfs(r + 1, c) + dfs(r, c + 1)."
            ],
            "time": "O(2^(m + n))",
            "space": "O(m + n)",
            "whySlow": "Exponential recursive branching.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int uniquePaths(int m, int n) {\n        int[] row = new int[n];\n        Arrays.fill(row, 1);\n        for (int i = 1; i < m; i++) {\n            for (int j = 1; j < n; j++) {\n                row[j] += row[j - 1];\n            }\n        }\n        return row[n - 1];\n    }\n}",
                "python": "class Solution:\n    def uniquePaths(self, m: int, n: int) -> int:\n        row = [1] * n\n        for _ in range(1, m):\n            for j in range(1, n):\n                row[j] += row[j - 1]\n        return row[-1]"
            }
        },
        "optimal": {
            "idea": "1D DP: row array initialized to 1; for each new row: row[j] += row[j-1].",
            "steps": [
                "int[] dp = new int[n]; Arrays.fill(dp, 1);",
                "For i = 1..m-1: for j = 1..n-1: dp[j] += dp[j - 1].",
                "Return dp[n - 1]."
            ],
            "time": "O(m * n)",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int uniquePaths(int m, int n) {\n        int[] dp = new int[n];\n        Arrays.fill(dp, 1);\n        for (int i = 1; i < m; i++) {\n            for (int j = 1; j < n; j++) {\n                dp[j] += dp[j - 1];\n            }\n        }\n        return dp[n - 1];\n    }\n}",
                "python": "class Solution:\n    def uniquePaths(self, m: int, n: int) -> int:\n        dp = [1] * n\n        for _ in range(1, m):\n            for j in range(1, n):\n                dp[j] += dp[j - 1]\n        return dp[-1]"
            }
        }
    },
    {
        "seq": 255,
        "whyNext": "Builds on Unique Paths: if obstacleGrid[r][c] == 1, dp[c] = 0 (blocked paths cannot pass through).",
        "brute": {
            "idea": "Recursively explore right and down paths, returning 0 if cell contains obstacle.",
            "steps": [
                "Check bounds and obstacle; sum branches."
            ],
            "time": "O(2^(m+n))",
            "space": "O(m+n)",
            "whySlow": "Exponential recursion.",
            "code": {
                "java": "class Solution {\n    public int uniquePathsWithObstacles(int[][] obstacleGrid) {\n        int n = obstacleGrid[0].length;\n        int[] dp = new int[n];\n        dp[0] = obstacleGrid[0][0] == 1 ? 0 : 1;\n        for (int[] row : obstacleGrid) {\n            for (int j = 0; j < n; j++) {\n                if (row[j] == 1) {\n                    dp[j] = 0;\n                } else if (j > 0) {\n                    dp[j] += dp[j - 1];\n                }\n            }\n        }\n        return dp[n - 1];\n    }\n}",
                "python": "class Solution:\n    def uniquePathsWithObstacles(self, obstacleGrid: list[list[int]]) -> int:\n        n = len(obstacleGrid[0])\n        dp = [0] * n\n        dp[0] = 1 if obstacleGrid[0][0] == 0 else 0\n        for row in obstacleGrid:\n            for j in range(n):\n                if row[j] == 1:\n                    dp[j] = 0\n                elif j > 0:\n                    dp[j] += dp[j - 1]\n        return dp[-1]"
            }
        },
        "optimal": {
            "idea": "1D DP array of size n: if grid[i][j] == 1 set dp[j] = 0; else if j > 0 add dp[j] += dp[j-1].",
            "steps": [
                "int[] dp = new int[n]; dp[0] = (grid[0][0] == 0) ? 1 : 0.",
                "For each row in obstacleGrid:",
                "For j = 0..n-1: if row[j] == 1 dp[j] = 0; else if j > 0 dp[j] += dp[j - 1].",
                "Return dp[n - 1]."
            ],
            "time": "O(m * n)",
            "space": "O(n)",
            "code": {
                "java": "class Solution {\n    public int uniquePathsWithObstacles(int[][] obstacleGrid) {\n        int n = obstacleGrid[0].length;\n        int[] dp = new int[n];\n        dp[0] = obstacleGrid[0][0] == 0 ? 1 : 0;\n        for (int[] row : obstacleGrid) {\n            for (int j = 0; j < n; j++) {\n                if (row[j] == 1) {\n                    dp[j] = 0;\n                } else if (j > 0) {\n                    dp[j] += dp[j - 1];\n                }\n            }\n        }\n        return dp[n - 1];\n    }\n}",
                "python": "class Solution:\n    def uniquePathsWithObstacles(self, obstacleGrid: list[list[int]]) -> int:\n        n = len(obstacleGrid[0])\n        dp = [0] * n\n        dp[0] = 1 if obstacleGrid[0][0] == 0 else 0\n        for row in obstacleGrid:\n            for j in range(n):\n                if row[j] == 1:\n                    dp[j] = 0\n                elif j > 0:\n                    dp[j] += dp[j - 1]\n        return dp[-1]"
            }
        }
    },
    {
        "seq": 256,
        "whyNext": "Grid path minimization: grid[r][c] += min(top, left); compute in-place in O(1) auxiliary space.",
        "brute": {
            "idea": "Recursive search exploring all paths from (0,0) to (m-1, n-1) adding cell values.",
            "steps": [
                "dfs(r, c): grid[r][c] + min(dfs(r+1, c), dfs(r, c+1))."
            ],
            "time": "O(2^(m+n))",
            "space": "O(m+n)",
            "whySlow": "Exponential recursion.",
            "code": {
                "java": "class Solution {\n    public int minPathSum(int[][] grid) {\n        int m = grid.length, n = grid[0].length;\n        for (int i = 0; i < m; i++) {\n            for (int j = 0; j < n; j++) {\n                if (i == 0 && j == 0) continue;\n                if (i == 0) grid[i][j] += grid[i][j - 1];\n                else if (j == 0) grid[i][j] += grid[i - 1][j];\n                else grid[i][j] += Math.min(grid[i - 1][j], grid[i][j - 1]);\n            }\n        }\n        return grid[m - 1][n - 1];\n    }\n}",
                "python": "class Solution:\n    def minPathSum(self, grid: list[list[int]]) -> int:\n        m, n = len(grid), len(grid[0])\n        for i in range(m):\n            for j in range(n):\n                if i == 0 and j == 0: continue\n                if i == 0: grid[i][j] += grid[i][j - 1]\n                elif j == 0: grid[i][j] += grid[i - 1][j]\n                else: grid[i][j] += min(grid[i - 1][j], grid[i][j - 1])\n        return grid[-1][-1]"
            }
        },
        "optimal": {
            "idea": "In-place grid DP: grid[i][j] += min(grid[i-1][j], grid[i][j-1]) in O(1) space.",
            "steps": [
                "First row: grid[0][j] += grid[0][j-1].",
                "First col: grid[i][0] += grid[i-1][0].",
                "Internal cells: grid[i][j] += min(grid[i-1][j], grid[i][j-1]).",
                "Return grid[m-1][n-1]."
            ],
            "time": "O(m * n)",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public int minPathSum(int[][] grid) {\n        int m = grid.length, n = grid[0].length;\n        for (int j = 1; j < n; j++) grid[0][j] += grid[0][j - 1];\n        for (int i = 1; i < m; i++) grid[i][0] += grid[i - 1][0];\n        for (int i = 1; i < m; i++) {\n            for (int j = 1; j < n; j++) {\n                grid[i][j] += Math.min(grid[i - 1][j], grid[i][j - 1]);\n            }\n        }\n        return grid[m - 1][n - 1];\n    }\n}",
                "python": "class Solution:\n    def minPathSum(self, grid: list[list[int]]) -> int:\n        m, n = len(grid), len(grid[0])\n        for j in range(1, n): grid[0][j] += grid[0][j - 1]\n        for i in range(1, m): grid[i][0] += grid[i - 1][0]\n        for i in range(1, m):\n            for j in range(1, n):\n                grid[i][j] += min(grid[i - 1][j], grid[i][j - 1])\n        return grid[-1][-1]"
            }
        }
    },
    {
        "seq": 257,
        "whyNext": "Bottom-up triangle DP: start from second to last row; dp[j] = val + min(dp[j], dp[j+1]); top element is answer.",
        "brute": {
            "idea": "Recursively explore both adjacent children down the triangle.",
            "steps": [
                "dfs(row, col): val + min(dfs(row+1, col), dfs(row+1, col+1))."
            ],
            "time": "O(2^n)",
            "space": "O(n)",
            "whySlow": "Exponential recursion.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int minimumTotal(List<List<Integer>> triangle) {\n        int n = triangle.size();\n        int[] dp = new int[n + 1];\n        for (int r = n - 1; r >= 0; r--) {\n            for (int c = 0; c <= r; c++) {\n                dp[c] = triangle.get(r).get(c) + Math.min(dp[c], dp[c + 1]);\n            }\n        }\n        return dp[0];\n    }\n}",
                "python": "class Solution:\n    def minimumTotal(self, triangle: list[list[int]]) -> int:\n        dp = list(triangle[-1])\n        for r in range(len(triangle) - 2, -1, -1):\n            for c in range(r + 1):\n                dp[c] = triangle[r][c] + min(dp[c], dp[c + 1])\n        return dp[0]"
            }
        },
        "optimal": {
            "idea": "Bottom-up 1D DP: copy bottom row; iterate row backwards from n-2 down to 0: dp[c] = triangle[r][c] + min(dp[c], dp[c+1]).",
            "steps": [
                "int[] dp initialized with bottom row values.",
                "For r from n - 2 down to 0: for c from 0 to r: dp[c] = triangle[r][c] + min(dp[c], dp[c + 1]).",
                "Return dp[0]."
            ],
            "time": "O(n^2)",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int minimumTotal(List<List<Integer>> triangle) {\n        int n = triangle.size();\n        int[] dp = new int[n];\n        for (int i = 0; i < n; i++) dp[i] = triangle.get(n - 1).get(i);\n        for (int r = n - 2; r >= 0; r--) {\n            for (int c = 0; c <= r; c++) {\n                dp[c] = triangle.get(r).get(c) + Math.min(dp[c], dp[c + 1]);\n            }\n        }\n        return dp[0];\n    }\n}",
                "python": "class Solution:\n    def minimumTotal(self, triangle: list[list[int]]) -> int:\n        dp = list(triangle[-1])\n        for r in range(len(triangle) - 2, -1, -1):\n            for c in range(r + 1):\n                dp[c] = triangle[r][c] + min(dp[c], dp[c + 1])\n        return dp[0]"
            }
        }
    },
    {
        "seq": 258,
        "whyNext": "3-way falling path: matrix[r][c] += min(up-left, up, up-right); take minimum of bottom row.",
        "brute": {
            "idea": "Recursively check all 3 branches from top row to bottom row.",
            "steps": [
                "dfs(r, c): matrix[r][c] + min(3 falling directions)."
            ],
            "time": "O(3^n)",
            "space": "O(n)",
            "whySlow": "Exponential recursion.",
            "code": {
                "java": "class Solution {\n    public int minFallingPathSum(int[][] matrix) {\n        int n = matrix.length;\n        for (int r = 1; r < n; r++) {\n            for (int c = 0; c < n; c++) {\n                int left = c > 0 ? matrix[r - 1][c - 1] : Integer.MAX_VALUE;\n                int mid = matrix[r - 1][c];\n                int right = c < n - 1 ? matrix[r - 1][c + 1] : Integer.MAX_VALUE;\n                matrix[r][c] += Math.min(mid, Math.min(left, right));\n            }\n        }\n        int min = Integer.MAX_VALUE;\n        for (int v : matrix[n - 1]) min = Math.min(min, v);\n        return min;\n    }\n}",
                "python": "class Solution:\n    def minFallingPathSum(self, matrix: list[list[int]]) -> int:\n        n = len(matrix)\n        for r in range(1, n):\n            for c in range(n):\n                left = matrix[r - 1][c - 1] if c > 0 else float('inf')\n                mid = matrix[r - 1][c]\n                right = matrix[r - 1][c + 1] if c < n - 1 else float('inf')\n                matrix[r][c] += min(mid, left, right)\n        return min(matrix[-1])"
            }
        },
        "optimal": {
            "idea": "In-place DP: for r = 1..n-1: matrix[r][c] += min(matrix[r-1][c-1], matrix[r-1][c], matrix[r-1][c+1]); return min of last row.",
            "steps": [
                "For r = 1..n-1: for c = 0..n-1:",
                "bestPrev = matrix[r-1][c]; if c > 0 min with matrix[r-1][c-1]; if c < n - 1 min with matrix[r-1][c+1].",
                "matrix[r][c] += bestPrev.",
                "Return min(matrix[n-1])."
            ],
            "time": "O(n^2)",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public int minFallingPathSum(int[][] matrix) {\n        int n = matrix.length;\n        for (int r = 1; r < n; r++) {\n            for (int c = 0; c < n; c++) {\n                int best = matrix[r - 1][c];\n                if (c > 0) best = Math.min(best, matrix[r - 1][c - 1]);\n                if (c < n - 1) best = Math.min(best, matrix[r - 1][c + 1]);\n                matrix[r][c] += best;\n            }\n        }\n        int min = Integer.MAX_VALUE;\n        for (int val : matrix[n - 1]) min = Math.min(min, val);\n        return min;\n    }\n}",
                "python": "class Solution:\n    def minFallingPathSum(self, matrix: list[list[int]]) -> int:\n        n = len(matrix)\n        for r in range(1, n):\n            for c in range(n):\n                best = matrix[r - 1][c]\n                if c > 0: best = min(best, matrix[r - 1][c - 1])\n                if c < n - 1: best = min(best, matrix[r - 1][c + 1])\n                matrix[r][c] += best\n        return min(matrix[-1])"
            }
        }
    },
    {
        "seq": 259,
        "whyNext": "Square geometric DP: dp[r][c] = 1 + min(dp[r-1][c], dp[r][c-1], dp[r-1][c-1]) gives side length of maximal square.",
        "brute": {
            "idea": "For every '1' cell, expand square side k = 1, 2, ... checking if all added cells are '1'.",
            "steps": [
                "For each (r, c) with '1', expand square while all cells are 1."
            ],
            "time": "O(m * n * min(m, n)^2)",
            "space": "O(1)",
            "whySlow": "Examines all cells in quadratic expansions.",
            "code": {
                "java": "class Solution {\n    public int maximalSquare(char[][] matrix) {\n        int m = matrix.length, n = matrix[0].length;\n        int[][] dp = new int[m + 1][n + 1];\n        int maxSide = 0;\n        for (int i = 1; i <= m; i++) {\n            for (int j = 1; j <= n; j++) {\n                if (matrix[i - 1][j - 1] == '1') {\n                    dp[i][j] = 1 + Math.min(dp[i - 1][j], Math.min(dp[i][j - 1], dp[i - 1][j - 1]));\n                    maxSide = Math.max(maxSide, dp[i][j]);\n                }\n            }\n        }\n        return maxSide * maxSide;\n    }\n}",
                "python": "class Solution:\n    def maximalSquare(self, matrix: list[list[str]]) -> int:\n        m, n = len(matrix), len(matrix[0])\n        dp = [[0] * (n + 1) for _ in range(m + 1)]\n        max_s = 0\n        for i in range(1, m + 1):\n            for j in range(1, n + 1):\n                if matrix[i - 1][j - 1] == '1':\n                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])\n                    max_s = max(max_s, dp[i][j])\n        return max_s * max_s"
            }
        },
        "optimal": {
            "idea": "2D/1D DP: if cell == '1', dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]); answer is maxSide * maxSide.",
            "steps": [
                "int[][] dp = new int[m + 1][n + 1]; maxSide = 0.",
                "For i = 1..m: for j = 1..n:",
                "If matrix[i-1][j-1] == '1': dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]); maxSide = max(maxSide, dp[i][j]).",
                "Return maxSide * maxSide."
            ],
            "time": "O(m * n)",
            "space": "O(m * n)",
            "code": {
                "java": "class Solution {\n    public int maximalSquare(char[][] matrix) {\n        int m = matrix.length, n = matrix[0].length;\n        int[][] dp = new int[m + 1][n + 1];\n        int maxSide = 0;\n        for (int i = 1; i <= m; i++) {\n            for (int j = 1; j <= n; j++) {\n                if (matrix[i - 1][j - 1] == '1') {\n                    dp[i][j] = 1 + Math.min(dp[i - 1][j], Math.min(dp[i][j - 1], dp[i - 1][j - 1]));\n                    maxSide = Math.max(maxSide, dp[i][j]);\n                }\n            }\n        }\n        return maxSide * maxSide;\n    }\n}",
                "python": "class Solution:\n    def maximalSquare(self, matrix: list[list[str]]) -> int:\n        m, n = len(matrix), len(matrix[0])\n        dp = [[0] * (n + 1) for _ in range(m + 1)]\n        max_side = 0\n        for i in range(1, m + 1):\n            for j in range(1, n + 1):\n                if matrix[i - 1][j - 1] == '1':\n                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])\n                    max_side = max(max_side, dp[i][j])\n        return max_side * max_side"
            }
        }
    },
    {
        "seq": 260,
        "whyNext": "Reverse DP: health requirement must be >= 1 at all times; dp[r][c] = max(1, min(down, right) - dungeon[r][c]).",
        "brute": {
            "idea": "Binary search on knight's initial health in [1, 10^7]; run DFS to check if knight survives with health > 0 throughout.",
            "steps": [
                "Binary search initial health.",
                "DFS path check."
            ],
            "time": "O(2^(m+n) * log H)",
            "space": "O(m + n)",
            "whySlow": "Exponential paths.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int calculateMinimumHP(int[][] dungeon) {\n        int m = dungeon.length, n = dungeon[0].length;\n        int[][] dp = new int[m + 1][n + 1];\n        for (int[] row : dp) Arrays.fill(row, Integer.MAX_VALUE);\n        dp[m][n - 1] = 1;\n        dp[m - 1][n] = 1;\n        for (int i = m - 1; i >= 0; i--) {\n            for (int j = n - 1; j >= 0; j--) {\n                int minNeed = Math.min(dp[i + 1][j], dp[i][j + 1]) - dungeon[i][j];\n                dp[i][j] = Math.max(1, minNeed);\n            }\n        }\n        return dp[0][0];\n    }\n}",
                "python": "class Solution:\n    def calculateMinimumHP(self, dungeon: list[list[int]]) -> int:\n        m, n = len(dungeon), len(dungeon[0])\n        dp = [[float('inf')] * (n + 1) for _ in range(m + 1)]\n        dp[m][n - 1] = dp[m - 1][n] = 1\n        for i in range(m - 1, -1, -1):\n            for j in range(n - 1, -1, -1):\n                dp[i][j] = max(1, min(dp[i + 1][j], dp[i][j + 1]) - dungeon[i][j])\n        return dp[0][0]"
            }
        },
        "optimal": {
            "idea": "Reverse 2D DP from bottom-right (princess) to top-left (knight): dp[i][j] = max(1, min(dp[i+1][j], dp[i][j+1]) - dungeon[i][j]).",
            "steps": [
                "Pad dp matrix with INF of size (m + 1) x (n + 1).",
                "dp[m][n-1] = 1, dp[m-1][n] = 1.",
                "For i = m-1 down to 0: for j = n-1 down to 0: dp[i][j] = max(1, min(dp[i+1][j], dp[i][j+1]) - dungeon[i][j]).",
                "Return dp[0][0]."
            ],
            "time": "O(m * n)",
            "space": "O(m * n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int calculateMinimumHP(int[][] dungeon) {\n        int m = dungeon.length, n = dungeon[0].length;\n        int[][] dp = new int[m + 1][n + 1];\n        for (int[] row : dp) Arrays.fill(row, Integer.MAX_VALUE);\n        dp[m][n - 1] = 1;\n        dp[m - 1][n] = 1;\n        for (int i = m - 1; i >= 0; i--) {\n            for (int j = n - 1; j >= 0; j--) {\n                int minNext = Math.min(dp[i + 1][j], dp[i][j + 1]);\n                dp[i][j] = Math.max(1, minNext - dungeon[i][j]);\n            }\n        }\n        return dp[0][0];\n    }\n}",
                "python": "class Solution:\n    def calculateMinimumHP(self, dungeon: list[list[int]]) -> int:\n        m, n = len(dungeon), len(dungeon[0])\n        dp = [[float('inf')] * (n + 1) for _ in range(m + 1)]\n        dp[m][n - 1] = dp[m - 1][n] = 1\n        for i in range(m - 1, -1, -1):\n            for j in range(n - 1, -1, -1):\n                min_next = min(dp[i + 1][j], dp[i][j + 1])\n                dp[i][j] = max(1, min_next - dungeon[i][j])\n        return dp[0][0]"
            }
        }
    },
    {
        "seq": 261,
        "whyNext": "Canonical 2-string DP: if s1[i-1] == s2[j-1], dp[i][j] = 1 + dp[i-1][j-1]; else max(dp[i-1][j], dp[i][j-1]).",
        "brute": {
            "idea": "Naive recursion: if chars match recurse (i-1, j-1); else max(recurse(i-1, j), recurse(i, j-1)).",
            "steps": [
                "dfs(i, j) comparing tails."
            ],
            "time": "O(2^(m+n))",
            "space": "O(m+n)",
            "whySlow": "Exponential recursion.",
            "code": {
                "java": "class Solution {\n    public int longestCommonSubsequence(String text1, String text2) {\n        int m = text1.length(), n = text2.length();\n        int[][] dp = new int[m + 1][n + 1];\n        for (int i = 1; i <= m; i++) {\n            for (int j = 1; j <= n; j++) {\n                if (text1.charAt(i - 1) == text2.charAt(j - 1)) {\n                    dp[i][j] = 1 + dp[i - 1][j - 1];\n                } else {\n                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);\n                }\n            }\n        }\n        return dp[m][n];\n    }\n}",
                "python": "class Solution:\n    def longestCommonSubsequence(self, text1: str, text2: str) -> int:\n        m, n = len(text1), len(text2)\n        dp = [[0] * (n + 1) for _ in range(m + 1)]\n        for i in range(1, m + 1):\n            for j in range(1, n + 1):\n                if text1[i - 1] == text2[j - 1]:\n                    dp[i][j] = 1 + dp[i - 1][j - 1]\n                else:\n                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])\n        return dp[m][n]"
            }
        },
        "optimal": {
            "idea": "2D / 1D DP: dp[i][j] = 1 + dp[i-1][j-1] if match; else max(dp[i-1][j], dp[i][j-1]). Space compressed to 1 row.",
            "steps": [
                "int[] dp = new int[n + 1];",
                "For i = 1..m: prev = 0; for j = 1..n: temp = dp[j]; if text1[i-1] == text2[j-1] dp[j] = 1 + prev; else dp[j] = max(dp[j], dp[j-1]); prev = temp.",
                "Return dp[n]."
            ],
            "time": "O(m * n)",
            "space": "O(n)",
            "code": {
                "java": "class Solution {\n    public int longestCommonSubsequence(String text1, String text2) {\n        int m = text1.length(), n = text2.length();\n        int[] dp = new int[n + 1];\n        for (int i = 1; i <= m; i++) {\n            int prev = 0;\n            for (int j = 1; j <= n; j++) {\n                int temp = dp[j];\n                if (text1.charAt(i - 1) == text2.charAt(j - 1)) {\n                    dp[j] = 1 + prev;\n                } else {\n                    dp[j] = Math.max(dp[j], dp[j - 1]);\n                }\n                prev = temp;\n            }\n        }\n        return dp[n];\n    }\n}",
                "python": "class Solution:\n    def longestCommonSubsequence(self, text1: str, text2: str) -> int:\n        m, n = len(text1), len(text2)\n        dp = [0] * (n + 1)\n        for i in range(1, m + 1):\n            prev = 0\n            for j in range(1, n + 1):\n                temp = dp[j]\n                if text1[i - 1] == text2[j - 1]:\n                    dp[j] = 1 + prev\n                else:\n                    dp[j] = max(dp[j], dp[j - 1])\n                prev = temp\n        return dp[n]"
            }
        }
    },
    {
        "seq": 262,
        "whyNext": "Identical mathematical structure to LCS: connecting nums1[i] == nums2[j] without crossing lines is LCS of the two number arrays.",
        "brute": {
            "idea": "Recursively match matching numbers without crossing indices.",
            "steps": [
                "dfs(i, j): if nums1[i] == nums2[j] 1 + dfs(i+1, j+1); else max(dfs(i+1, j), dfs(i, j+1))."
            ],
            "time": "O(2^(m+n))",
            "space": "O(m+n)",
            "whySlow": "Exponential recursion.",
            "code": {
                "java": "class Solution {\n    public int maxUncrossedLines(int[] nums1, int[] nums2) {\n        int m = nums1.length, n = nums2.length;\n        int[][] dp = new int[m + 1][n + 1];\n        for (int i = 1; i <= m; i++) {\n            for (int j = 1; j <= n; j++) {\n                if (nums1[i - 1] == nums2[j - 1]) {\n                    dp[i][j] = 1 + dp[i - 1][j - 1];\n                } else {\n                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);\n                }\n            }\n        }\n        return dp[m][n];\n    }\n}",
                "python": "class Solution:\n    def maxUncrossedLines(self, nums1: list[int], nums2: list[int]) -> int:\n        m, n = len(nums1), len(nums2)\n        dp = [[0] * (n + 1) for _ in range(m + 1)]\n        for i in range(1, m + 1):\n            for j in range(1, n + 1):\n                if nums1[i - 1] == nums2[j - 1]:\n                    dp[i][j] = 1 + dp[i - 1][j - 1]\n                else:\n                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])\n        return dp[m][n]"
            }
        },
        "optimal": {
            "idea": "Equivalent to LCS: dp[i][j] = 1 + dp[i-1][j-1] if nums1[i-1] == nums2[j-1]; else max(dp[i-1][j], dp[i][j-1]).",
            "steps": [
                "int[] dp = new int[n + 1];",
                "For i = 1..m: prev = 0; for j = 1..n: temp = dp[j]; if nums1[i-1] == nums2[j-1] dp[j] = 1 + prev; else dp[j] = max(dp[j], dp[j-1]); prev = temp.",
                "Return dp[n]."
            ],
            "time": "O(m * n)",
            "space": "O(n)",
            "code": {
                "java": "class Solution {\n    public int maxUncrossedLines(int[] nums1, int[] nums2) {\n        int m = nums1.length, n = nums2.length;\n        int[] dp = new int[n + 1];\n        for (int i = 1; i <= m; i++) {\n            int prev = 0;\n            for (int j = 1; j <= n; j++) {\n                int temp = dp[j];\n                if (nums1[i - 1] == nums2[j - 1]) {\n                    dp[j] = 1 + prev;\n                } else {\n                    dp[j] = Math.max(dp[j], dp[j - 1]);\n                }\n                prev = temp;\n            }\n        }\n        return dp[n];\n    }\n}",
                "python": "class Solution:\n    def maxUncrossedLines(self, nums1: list[int], nums2: list[int]) -> int:\n        m, n = len(nums1), len(nums2)\n        dp = [0] * (n + 1)\n        for i in range(1, m + 1):\n            prev = 0\n            for j in range(1, n + 1):\n                temp = dp[j]\n                if nums1[i - 1] == nums2[j - 1]:\n                    dp[j] = 1 + prev\n                else:\n                    dp[j] = max(dp[j], dp[j - 1])\n                prev = temp\n        return dp[n]"
            }
        }
    },
    {
        "seq": 263,
        "whyNext": "Reduction to LCS: characters to delete = len(word1) + len(word2) - 2 * LCS(word1, word2).",
        "brute": {
            "idea": "Recursively delete characters until strings match.",
            "steps": [
                "dfs(i, j): if chars match recurse (i+1, j+1); else 1 + min(delete from w1, delete from w2)."
            ],
            "time": "O(2^(m+n))",
            "space": "O(m+n)",
            "whySlow": "Exponential recursion.",
            "code": {
                "java": "class Solution {\n    public int minDistance(String word1, String word2) {\n        int m = word1.length(), n = word2.length();\n        int[][] dp = new int[m + 1][n + 1];\n        for (int i = 1; i <= m; i++) {\n            for (int j = 1; j <= n; j++) {\n                if (word1.charAt(i - 1) == word2.charAt(j - 1)) {\n                    dp[i][j] = 1 + dp[i - 1][j - 1];\n                } else {\n                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);\n                }\n            }\n        }\n        int lcs = dp[m][n];\n        return m + n - 2 * lcs;\n    }\n}",
                "python": "class Solution:\n    def minDistance(self, word1: str, word2: str) -> int:\n        m, n = len(word1), len(word2)\n        dp = [[0] * (n + 1) for _ in range(m + 1)]\n        for i in range(1, m + 1):\n            for j in range(1, n + 1):\n                if word1[i - 1] == word2[j - 1]:\n                    dp[i][j] = 1 + dp[i - 1][j - 1]\n                else:\n                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])\n        return m + n - 2 * dp[m][n]"
            }
        },
        "optimal": {
            "idea": "Formula: len(w1) + len(w2) - 2 * LCS(w1, w2). Compute LCS in O(min(m, n)) space.",
            "steps": [
                "Compute LCS length lcs between word1 and word2.",
                "Return word1.length() + word2.length() - 2 * lcs."
            ],
            "time": "O(m * n)",
            "space": "O(n)",
            "code": {
                "java": "class Solution {\n    public int minDistance(String word1, String word2) {\n        int m = word1.length(), n = word2.length();\n        int[] dp = new int[n + 1];\n        for (int i = 1; i <= m; i++) {\n            int prev = 0;\n            for (int j = 1; j <= n; j++) {\n                int temp = dp[j];\n                if (word1.charAt(i - 1) == word2.charAt(j - 1)) {\n                    dp[j] = 1 + prev;\n                } else {\n                    dp[j] = Math.max(dp[j], dp[j - 1]);\n                }\n                prev = temp;\n            }\n        }\n        return m + n - 2 * dp[n];\n    }\n}",
                "python": "class Solution:\n    def minDistance(self, word1: str, word2: str) -> int:\n        m, n = len(word1), len(word2)\n        dp = [0] * (n + 1)\n        for i in range(1, m + 1):\n            prev = 0\n            for j in range(1, n + 1):\n                temp = dp[j]\n                if word1[i - 1] == word2[j - 1]:\n                    dp[j] = 1 + prev\n                else:\n                    dp[j] = max(dp[j], dp[j - 1])\n                prev = temp\n        return m + n - 2 * dp[n]"
            }
        }
    },
    {
        "seq": 264,
        "whyNext": "Levenshtein distance: dp[i][j] = dp[i-1][j-1] if match; else 1 + min(insert dp[i][j-1], delete dp[i-1][j], replace dp[i-1][j-1]).",
        "brute": {
            "idea": "Recursive branching for insert, delete, and replace operations.",
            "steps": [
                "dfs(i, j): if chars match dfs(i-1, j-1); else 1 + min(insert, delete, replace)."
            ],
            "time": "O(3^(m+n))",
            "space": "O(m+n)",
            "whySlow": "Exponential recursion.",
            "code": {
                "java": "class Solution {\n    public int minDistance(String word1, String word2) {\n        int m = word1.length(), n = word2.length();\n        int[][] dp = new int[m + 1][n + 1];\n        for (int i = 0; i <= m; i++) dp[i][0] = i;\n        for (int j = 0; j <= n; j++) dp[0][j] = j;\n        for (int i = 1; i <= m; i++) {\n            for (int j = 1; j <= n; j++) {\n                if (word1.charAt(i - 1) == word2.charAt(j - 1)) {\n                    dp[i][j] = dp[i - 1][j - 1];\n                } else {\n                    dp[i][j] = 1 + Math.min(dp[i - 1][j - 1], Math.min(dp[i - 1][j], dp[i][j - 1]));\n                }\n            }\n        }\n        return dp[m][n];\n    }\n}",
                "python": "class Solution:\n    def minDistance(self, word1: str, word2: str) -> int:\n        m, n = len(word1), len(word2)\n        dp = [[0] * (n + 1) for _ in range(m + 1)]\n        for i in range(m + 1): dp[i][0] = i\n        for j in range(n + 1): dp[0][j] = j\n        for i in range(1, m + 1):\n            for j in range(1, n + 1):\n                if word1[i - 1] == word2[j - 1]:\n                    dp[i][j] = dp[i - 1][j - 1]\n                else:\n                    dp[i][j] = 1 + min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1])\n        return dp[m][n]"
            }
        },
        "optimal": {
            "idea": "Levenshtein 2D DP: base cases dp[i][0] = i, dp[0][j] = j. dp[i][j] = dp[i-1][j-1] if match; else 1 + min(replace, delete, insert).",
            "steps": [
                "int[][] dp = new int[m + 1][n + 1].",
                "Init borders dp[i][0] = i, dp[0][j] = j.",
                "For i = 1..m: for j = 1..n: if match dp[i][j] = dp[i-1][j-1]; else dp[i][j] = 1 + min(dp[i-1][j-1], min(dp[i-1][j], dp[i][j-1])).",
                "Return dp[m][n]."
            ],
            "time": "O(m * n)",
            "space": "O(m * n)",
            "code": {
                "java": "class Solution {\n    public int minDistance(String word1, String word2) {\n        int m = word1.length(), n = word2.length();\n        int[][] dp = new int[m + 1][n + 1];\n        for (int i = 0; i <= m; i++) dp[i][0] = i;\n        for (int j = 0; j <= n; j++) dp[0][j] = j;\n        for (int i = 1; i <= m; i++) {\n            for (int j = 1; j <= n; j++) {\n                if (word1.charAt(i - 1) == word2.charAt(j - 1)) {\n                    dp[i][j] = dp[i - 1][j - 1];\n                } else {\n                    dp[i][j] = 1 + Math.min(dp[i - 1][j - 1], Math.min(dp[i - 1][j], dp[i][j - 1]));\n                }\n            }\n        }\n        return dp[m][n];\n    }\n}",
                "python": "class Solution:\n    def minDistance(self, word1: str, word2: str) -> int:\n        m, n = len(word1), len(word2)\n        dp = [[0] * (n + 1) for _ in range(m + 1)]\n        for i in range(m + 1): dp[i][0] = i\n        for j in range(n + 1): dp[0][j] = j\n        for i in range(1, m + 1):\n            for j in range(1, n + 1):\n                if word1[i - 1] == word2[j - 1]:\n                    dp[i][j] = dp[i - 1][j - 1]\n                else:\n                    dp[i][j] = 1 + min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1])\n        return dp[m][n]"
            }
        }
    },
    {
        "seq": 265,
        "whyNext": "Matching subsequence counter: dp[i][j] = dp[i-1][j] + (s[i-1] == t[j-1] ? dp[i-1][j-1] : 0).",
        "brute": {
            "idea": "Recursively match characters of t against s.",
            "steps": [
                "dfs(i, j): if j == len(t) return 1; if i == len(s) return 0.",
                "Sum match and skip branches."
            ],
            "time": "O(2^m)",
            "space": "O(m)",
            "whySlow": "Exponential recursion.",
            "code": {
                "java": "class Solution {\n    public int numDistinct(String s, String t) {\n        int m = s.length(), n = t.length();\n        int[][] dp = new int[m + 1][n + 1];\n        for (int i = 0; i <= m; i++) dp[i][0] = 1;\n        for (int i = 1; i <= m; i++) {\n            for (int j = 1; j <= n; j++) {\n                dp[i][j] = dp[i - 1][j];\n                if (s.charAt(i - 1) == t.charAt(j - 1)) {\n                    dp[i][j] += dp[i - 1][j - 1];\n                }\n            }\n        }\n        return dp[m][n];\n    }\n}",
                "python": "class Solution:\n    def numDistinct(self, s: str, t: str) -> int:\n        m, n = len(s), len(t)\n        dp = [[0] * (n + 1) for _ in range(m + 1)]\n        for i in range(m + 1): dp[i][0] = 1\n        for i in range(1, m + 1):\n            for j in range(1, n + 1):\n                dp[i][j] = dp[i - 1][j]\n                if s[i - 1] == t[j - 1]:\n                    dp[i][j] += dp[i - 1][j - 1]\n        return dp[m][n]"
            }
        },
        "optimal": {
            "idea": "1D DP running backwards: dp[j] += dp[j - 1] when s[i] == t[j] in O(n) space.",
            "steps": [
                "int[] dp = new int[n + 1]; dp[0] = 1.",
                "For i = 0..m-1: for j = n down to 1: if s[i] == t[j-1] dp[j] += dp[j - 1].",
                "Return dp[n]."
            ],
            "time": "O(m * n)",
            "space": "O(n)",
            "code": {
                "java": "class Solution {\n    public int numDistinct(String s, String t) {\n        int m = s.length(), n = t.length();\n        int[] dp = new int[n + 1];\n        dp[0] = 1;\n        for (int i = 0; i < m; i++) {\n            char c = s.charAt(i);\n            for (int j = n; j >= 1; j--) {\n                if (c == t.charAt(j - 1)) {\n                    dp[j] += dp[j - 1];\n                }\n            }\n        }\n        return dp[n];\n    }\n}",
                "python": "class Solution:\n    def numDistinct(self, s: str, t: str) -> int:\n        n = len(t)\n        dp = [0] * (n + 1)\n        dp[0] = 1\n        for c in s:\n            for j in range(n, 0, -1):\n                if c == t[j - 1]:\n                    dp[j] += dp[j - 1]\n        return dp[n]"
            }
        }
    },
    {
        "seq": 266,
        "whyNext": "Two-string merge check: dp[i][j] is true if s3[0..i+j-1] can be formed by interleaving s1[0..i-1] and s2[0..j-1].",
        "brute": {
            "idea": "Recursively check matching character from s1 or s2 against s3.",
            "steps": [
                "dfs(i, j, k): match s1[i] == s3[k] or s2[j] == s3[k]."
            ],
            "time": "O(2^(m+n))",
            "space": "O(m+n)",
            "whySlow": "Exponential recursion.",
            "code": {
                "java": "class Solution {\n    public boolean isInterleave(String s1, String s2, String s3) {\n        if (s1.length() + s2.length() != s3.length()) return false;\n        int m = s1.length(), n = s2.length();\n        boolean[][] dp = new boolean[m + 1][n + 1];\n        dp[0][0] = true;\n        for (int i = 1; i <= m; i++) dp[i][0] = dp[i - 1][0] && s1.charAt(i - 1) == s3.charAt(i - 1);\n        for (int j = 1; j <= n; j++) dp[0][j] = dp[0][j - 1] && s2.charAt(j - 1) == s3.charAt(j - 1);\n        for (int i = 1; i <= m; i++) {\n            for (int j = 1; j <= n; j++) {\n                char c = s3.charAt(i + j - 1);\n                dp[i][j] = (dp[i - 1][j] && s1.charAt(i - 1) == c) ||\n                           (dp[i][j - 1] && s2.charAt(j - 1) == c);\n            }\n        }\n        return dp[m][n];\n    }\n}",
                "python": "class Solution:\n    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:\n        if len(s1) + len(s2) != len(s3): return False\n        m, n = len(s1), len(s2)\n        dp = [[False] * (n + 1) for _ in range(m + 1)]\n        dp[0][0] = True\n        for i in range(1, m + 1): dp[i][0] = dp[i - 1][0] and s1[i - 1] == s3[i - 1]\n        for j in range(1, n + 1): dp[0][j] = dp[0][j - 1] and s2[j - 1] == s3[j - 1]\n        for i in range(1, m + 1):\n            for j in range(1, n + 1):\n                c = s3[i + j - 1]\n                dp[i][j] = (dp[i - 1][j] and s1[i - 1] == c) or (dp[i][j - 1] and s2[j - 1] == c)\n        return dp[m][n]"
            }
        },
        "optimal": {
            "idea": "1D boolean DP: dp[j] is true if s3[0..i+j-1] is formed by s1[0..i-1] and s2[0..j-1].",
            "steps": [
                "If len(s1) + len(s2) != len(s3) return false.",
                "boolean[] dp = new boolean[n + 1]; dp[0] = true.",
                "Init row 0: dp[j] = dp[j-1] && s2[j-1] == s3[j-1].",
                "For i = 1..m: dp[0] = dp[0] && s1[i-1] == s3[i-1]; for j = 1..n: dp[j] = (dp[j] && s1[i-1] == s3[i+j-1]) || (dp[j-1] && s2[j-1] == s3[i+j-1]).",
                "Return dp[n]."
            ],
            "time": "O(m * n)",
            "space": "O(n)",
            "code": {
                "java": "class Solution {\n    public boolean isInterleave(String s1, String s2, String s3) {\n        if (s1.length() + s2.length() != s3.length()) return false;\n        int m = s1.length(), n = s2.length();\n        boolean[] dp = new boolean[n + 1];\n        dp[0] = true;\n        for (int j = 1; j <= n; j++) dp[j] = dp[j - 1] && s2.charAt(j - 1) == s3.charAt(j - 1);\n        for (int i = 1; i <= m; i++) {\n            dp[0] = dp[0] && s1.charAt(i - 1) == s3.charAt(i - 1);\n            for (int j = 1; j <= n; j++) {\n                char c = s3.charAt(i + j - 1);\n                dp[j] = (dp[j] && s1.charAt(i - 1) == c) || (dp[j - 1] && s2.charAt(j - 1) == c);\n            }\n        }\n        return dp[n];\n    }\n}",
                "python": "class Solution:\n    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:\n        if len(s1) + len(s2) != len(s3):\n            return False\n        m, n = len(s1), len(s2)\n        dp = [False] * (n + 1)\n        dp[0] = True\n        for j in range(1, n + 1):\n            dp[j] = dp[j - 1] and s2[j - 1] == s3[j - 1]\n        for i in range(1, m + 1):\n            dp[0] = dp[0] and s1[i - 1] == s3[i - 1]\n            for j in range(1, n + 1):\n                c = s3[i + j - 1]\n                dp[j] = (dp[j] and s1[i - 1] == c) or (dp[j - 1] and s2[j - 1] == c)\n        return dp[n]"
            }
        }
    },
    {
        "seq": 267,
        "whyNext": "Center expansion: 2n - 1 possible centers (single character or between two); expand outward in O(1) space and O(n^2) total time.",
        "brute": {
            "idea": "Test all O(n^2) substrings: check if each is palindrome by two pointers.",
            "steps": [
                "For i = 0..n-1, j = i..n-1: check isPalindrome(s[i..j]).",
                "Keep longest."
            ],
            "time": "O(n^3)",
            "space": "O(1)",
            "whySlow": "Cubic running time.",
            "code": {
                "java": "class Solution {\n    public String longestPalindrome(String s) {\n        int start = 0, end = 0;\n        for (int i = 0; i < s.length(); i++) {\n            int len1 = expand(s, i, i);\n            int len2 = expand(s, i, i + 1);\n            int len = Math.max(len1, len2);\n            if (len > end - start + 1) {\n                start = i - (len - 1) / 2;\n                end = i + len / 2;\n            }\n        }\n        return s.substring(start, end + 1);\n    }\n    private int expand(String s, int l, int r) {\n        while (l >= 0 && r < s.length() && s.charAt(l) == s.charAt(r)) {\n            l--; r++;\n        }\n        return r - l - 1;\n    }\n}",
                "python": "class Solution:\n    def longestPalindrome(self, s: str) -> str:\n        start = end = 0\n        def expand(l, r):\n            while l >= 0 and r < len(s) and s[l] == s[r]:\n                l -= 1\n                r += 1\n            return r - l - 1\n        for i in range(len(s)):\n            l1 = expand(i, i)\n            l2 = expand(i, i + 1)\n            length = max(l1, l2)\n            if length > end - start + 1:\n                start = i - (length - 1) // 2\n                end = i + length // 2\n        return s[start:end+1]"
            }
        },
        "optimal": {
            "idea": "Expand around centers: test 2n - 1 centers (i, i) and (i, i + 1); track max length and start index in O(1) space.",
            "steps": [
                "start = 0, maxLen = 0.",
                "For i = 0..n-1:",
                "len1 = expand(i, i), len2 = expand(i, i + 1).",
                "len = max(len1, len2).",
                "If len > maxLen: maxLen = len; start = i - (len - 1) / 2.",
                "Return s.substring(start, start + maxLen)."
            ],
            "time": "O(n^2)",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public String longestPalindrome(String s) {\n        if (s == null || s.length() < 1) return \"\";\n        int start = 0, maxLen = 0;\n        for (int i = 0; i < s.length(); i++) {\n            int len1 = expand(s, i, i);\n            int len2 = expand(s, i, i + 1);\n            int len = Math.max(len1, len2);\n            if (len > maxLen) {\n                maxLen = len;\n                start = i - (len - 1) / 2;\n            }\n        }\n        return s.substring(start, start + maxLen);\n    }\n    private int expand(String s, int l, int r) {\n        while (l >= 0 && r < s.length() && s.charAt(l) == s.charAt(r)) {\n            l--;\n            r++;\n        }\n        return r - l - 1;\n    }\n}",
                "python": "class Solution:\n    def longestPalindrome(self, s: str) -> str:\n        if not s:\n            return \"\"\n        start = max_len = 0\n        def expand(l: int, r: int) -> int:\n            while l >= 0 and r < len(s) and s[l] == s[r]:\n                l -= 1\n                r += 1\n            return r - l - 1\n        for i in range(len(s)):\n            l1 = expand(i, i)\n            l2 = expand(i, i + 1)\n            length = max(l1, l2)\n            if length > max_len:\n                max_len = length\n                start = i - (length - 1) // 2\n        return s[start:start + max_len]"
            }
        }
    },
    {
        "seq": 268,
        "whyNext": "Builds on Longest Palindromic Substring: count total number of palindromic expansions from all 2n - 1 centers.",
        "brute": {
            "idea": "Check all O(n^2) substrings if they are palindromes.",
            "steps": [
                "Nested loops checking isPalindrome(s[i..j])."
            ],
            "time": "O(n^3)",
            "space": "O(1)",
            "whySlow": "Cubic brute force.",
            "code": {
                "java": "class Solution {\n    public int countSubstrings(String s) {\n        int count = 0;\n        for (int i = 0; i < s.length(); i++) {\n            count += expand(s, i, i);\n            count += expand(s, i, i + 1);\n        }\n        return count;\n    }\n    private int expand(String s, int l, int r) {\n        int c = 0;\n        while (l >= 0 && r < s.length() && s.charAt(l--) == s.charAt(r++)) {\n            c++;\n        }\n        return c;\n    }\n}",
                "python": "class Solution:\n    def countSubstrings(self, s: str) -> int:\n        count = 0\n        def expand(l, r):\n            c = 0\n            while l >= 0 and r < len(s) and s[l] == s[r]:\n                c += 1\n                l -= 1\n                r += 1\n            return c\n        for i in range(len(s)):\n            count += expand(i, i) + expand(i, i + 1)\n        return count"
            }
        },
        "optimal": {
            "idea": "Expand around centers: for each center, while s[l] == s[r], increment count, l--, r++ in O(1) space.",
            "steps": [
                "int count = 0.",
                "For i = 0..n-1: count += countPalindromes(i, i) + countPalindromes(i, i + 1).",
                "Return count."
            ],
            "time": "O(n^2)",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public int countSubstrings(String s) {\n        int count = 0;\n        for (int i = 0; i < s.length(); i++) {\n            count += expand(s, i, i);\n            count += expand(s, i, i + 1);\n        }\n        return count;\n    }\n    private int expand(String s, int l, int r) {\n        int cnt = 0;\n        while (l >= 0 && r < s.length() && s.charAt(l) == s.charAt(r)) {\n            cnt++;\n            l--;\n            r++;\n        }\n        return cnt;\n    }\n}",
                "python": "class Solution:\n    def countSubstrings(self, s: str) -> int:\n        count = 0\n        def expand(l: int, r: int) -> int:\n            cnt = 0\n            while l >= 0 and r < len(s) and s[l] == s[r]:\n                cnt += 1\n                l -= 1\n                r += 1\n            return cnt\n        for i in range(len(s)):\n            count += expand(i, i) + expand(i, i + 1)\n        return count"
            }
        }
    },
    {
        "seq": 269,
        "whyNext": "Interval DP / LCS: LPS(s) equals LCS(s, reverse(s)); if s[i] == s[j], dp[i][j] = 2 + dp[i+1][j-1].",
        "brute": {
            "idea": "Check all 2^n subsequences if they are palindromes.",
            "steps": [
                "Enumerate subsequences.",
                "Filter palindromes."
            ],
            "time": "O(2^n * n)",
            "space": "O(n)",
            "whySlow": "Exponential enumeration.",
            "code": {
                "java": "class Solution {\n    public int longestPalindromeSubseq(String s) {\n        int n = s.length();\n        int[][] dp = new int[n][n];\n        for (int i = n - 1; i >= 0; i--) {\n            dp[i][i] = 1;\n            for (int j = i + 1; j < n; j++) {\n                if (s.charAt(i) == s.charAt(j)) {\n                    dp[i][j] = 2 + dp[i + 1][j - 1];\n                } else {\n                    dp[i][j] = Math.max(dp[i + 1][j], dp[i][j - 1]);\n                }\n            }\n        }\n        return dp[0][n - 1];\n    }\n}",
                "python": "class Solution:\n    def longestPalindromeSubseq(self, s: str) -> int:\n        n = len(s)\n        dp = [[0] * n for _ in range(n)]\n        for i in range(n - 1, -1, -1):\n            dp[i][i] = 1\n            for j in range(i + 1, n):\n                if s[i] == s[j]:\n                    dp[i][j] = 2 + dp[i + 1][j - 1]\n                else:\n                    dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])\n        return dp[0][n - 1]"
            }
        },
        "optimal": {
            "idea": "Interval DP: dp[i][j] = longest palindromic subsequence in s[i..j]. Base: dp[i][i] = 1. If s[i] == s[j] dp[i][j] = 2 + dp[i+1][j-1]; else max(dp[i+1][j], dp[i][j-1]).",
            "steps": [
                "int[][] dp = new int[n][n];",
                "Loop i from n - 1 down to 0: dp[i][i] = 1; for j from i + 1 to n - 1:",
                "If s[i] == s[j] dp[i][j] = 2 + dp[i+1][j-1]; else dp[i][j] = max(dp[i+1][j], dp[i][j-1]).",
                "Return dp[0][n - 1]."
            ],
            "time": "O(n^2)",
            "space": "O(n^2)",
            "code": {
                "java": "class Solution {\n    public int longestPalindromeSubseq(String s) {\n        int n = s.length();\n        int[][] dp = new int[n][n];\n        for (int i = n - 1; i >= 0; i--) {\n            dp[i][i] = 1;\n            for (int j = i + 1; j < n; j++) {\n                if (s.charAt(i) == s.charAt(j)) {\n                    dp[i][j] = 2 + dp[i + 1][j - 1];\n                } else {\n                    dp[i][j] = Math.max(dp[i + 1][j], dp[i][j - 1]);\n                }\n            }\n        }\n        return dp[0][n - 1];\n    }\n}",
                "python": "class Solution:\n    def longestPalindromeSubseq(self, s: str) -> int:\n        n = len(s)\n        dp = [[0] * n for _ in range(n)]\n        for i in range(n - 1, -1, -1):\n            dp[i][i] = 1\n            for j in range(i + 1, n):\n                if s[i] == s[j]:\n                    dp[i][j] = 2 + dp[i + 1][j - 1]\n                else:\n                    dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])\n        return dp[0][n - 1]"
            }
        }
    },
    {
        "seq": 270,
        "whyNext": "Min cut palindrome partition: dp[i] = min cuts for prefix s[0..i]; if s[j..i] is palindrome, dp[i] = min(dp[i], dp[j-1] + 1).",
        "brute": {
            "idea": "Backtracking finding all valid palindrome partitions and finding minimum cuts.",
            "steps": [
                "Find all partitions.",
                "Return min(len(partition) - 1)."
            ],
            "time": "O(2^n * n)",
            "space": "O(n)",
            "whySlow": "Exponential partition enumeration.",
            "code": {
                "java": "class Solution {\n    public int minCut(String s) {\n        int n = s.length();\n        int[] dp = new int[n];\n        for (int i = 0; i < n; i++) dp[i] = i;\n        for (int mid = 0; mid < n; mid++) {\n            expand(s, mid, mid, dp);\n            expand(s, mid, mid + 1, dp);\n        }\n        return dp[n - 1];\n    }\n    private void expand(String s, int l, int r, int[] dp) {\n        while (l >= 0 && r < s.length() && s.charAt(l) == s.charAt(r)) {\n            int cuts = (l == 0) ? 0 : dp[l - 1] + 1;\n            dp[r] = Math.min(dp[r], cuts);\n            l--; r++;\n        }\n    }\n}",
                "python": "class Solution:\n    def minCut(self, s: str) -> int:\n        n = len(s)\n        dp = list(range(n))\n        def expand(l, r):\n            while l >= 0 and r < n and s[l] == s[r]:\n                cuts = 0 if l == 0 else dp[l - 1] + 1\n                dp[r] = min(dp[r], cuts)\n                l -= 1\n                r += 1\n        for mid in range(n):\n            expand(mid, mid)\n            expand(mid, mid + 1)\n        return dp[-1]"
            }
        },
        "optimal": {
            "idea": "Expand centers directly updating cuts: dp[r] = min(dp[r], (l == 0 ? 0 : dp[l - 1] + 1)) while s[l] == s[r].",
            "steps": [
                "int[] dp = new int[n]; dp[i] = i (max cuts).",
                "For mid = 0..n-1: expand(mid, mid), expand(mid, mid + 1).",
                "expand(l, r): while l >= 0 && r < n && s[l] == s[r]: cuts = (l == 0) ? 0 : dp[l-1] + 1; dp[r] = min(dp[r], cuts); l--; r++.",
                "Return dp[n - 1]."
            ],
            "time": "O(n^2)",
            "space": "O(n)",
            "code": {
                "java": "class Solution {\n    public int minCut(String s) {\n        int n = s.length();\n        int[] dp = new int[n];\n        for (int i = 0; i < n; i++) dp[i] = i;\n        for (int mid = 0; mid < n; mid++) {\n            expand(s, mid, mid, dp);\n            expand(s, mid, mid + 1, dp);\n        }\n        return dp[n - 1];\n    }\n    private void expand(String s, int l, int r, int[] dp) {\n        while (l >= 0 && r < s.length() && s.charAt(l) == s.charAt(r)) {\n            int cuts = (l == 0) ? 0 : dp[l - 1] + 1;\n            dp[r] = Math.min(dp[r], cuts);\n            l--;\n            r++;\n        }\n    }\n}",
                "python": "class Solution:\n    def minCut(self, s: str) -> int:\n        n = len(s)\n        dp = list(range(n))\n        def expand(l: int, r: int):\n            while l >= 0 and r < n and s[l] == s[r]:\n                cuts = 0 if l == 0 else dp[l - 1] + 1\n                dp[r] = min(dp[r], cuts)\n                l -= 1\n                r += 1\n        for mid in range(n):\n            expand(mid, mid)\n            expand(mid, mid + 1)\n        return dp[-1]"
            }
        }
    },
    {
        "seq": 271,
        "whyNext": "Regex dynamic programming with '.' (any char) and '*' (zero or more of preceding element).",
        "brute": {
            "idea": "Recursive pattern matching: if p[1] == '*', try 0 matches or 1+ matches.",
            "steps": [
                "dfs(s, p): if p is empty return s is empty.",
                "Handle '*' branching."
            ],
            "time": "O((|s|+|p|)! )",
            "space": "O(|s|+|p|)",
            "whySlow": "Exponential recursive branching on '*'.",
            "code": {
                "java": "class Solution {\n    public boolean isMatch(String s, String p) {\n        int m = s.length(), n = p.length();\n        boolean[][] dp = new boolean[m + 1][n + 1];\n        dp[0][0] = true;\n        for (int j = 2; j <= n; j += 2) {\n            if (p.charAt(j - 1) == '*') dp[0][j] = dp[0][j - 2];\n        }\n        for (int i = 1; i <= m; i++) {\n            for (int j = 1; j <= n; j++) {\n                if (p.charAt(j - 1) == '*') {\n                    dp[i][j] = dp[i][j - 2];\n                    if (p.charAt(j - 2) == '.' || p.charAt(j - 2) == s.charAt(i - 1)) {\n                        dp[i][j] = dp[i][j] || dp[i - 1][j];\n                    }\n                } else if (p.charAt(j - 1) == '.' || p.charAt(j - 1) == s.charAt(i - 1)) {\n                    dp[i][j] = dp[i - 1][j - 1];\n                }\n            }\n        }\n        return dp[m][n];\n    }\n}",
                "python": "class Solution:\n    def isMatch(self, s: str, p: str) -> bool:\n        m, n = len(s), len(p)\n        dp = [[False] * (n + 1) for _ in range(m + 1)]\n        dp[0][0] = True\n        for j in range(2, n + 1, 2):\n            if p[j - 1] == '*': dp[0][j] = dp[0][j - 2]\n        for i in range(1, m + 1):\n            for j in range(1, n + 1):\n                if p[j - 1] == '*':\n                    dp[i][j] = dp[i][j - 2]\n                    if p[j - 2] == '.' or p[j - 2] == s[i - 1]:\n                        dp[i][j] = dp[i][j] or dp[i - 1][j]\n                elif p[j - 1] == '.' or p[j - 1] == s[i - 1]:\n                    dp[i][j] = dp[i - 1][j - 1]\n        return dp[m][n]"
            }
        },
        "optimal": {
            "idea": "2D DP: dp[i][j] matches s[0..i-1] with p[0..j-1]. If p[j-1] == '*': dp[i][j] = dp[i][j-2] || ((p[j-2]=='.' || p[j-2]==s[i-1]) && dp[i-1][j]).",
            "steps": [
                "boolean[][] dp = new boolean[m + 1][n + 1]; dp[0][0] = true.",
                "Init empty string matches: for j = 2..n: if p[j-1] == '*' dp[0][j] = dp[0][j-2].",
                "For i = 1..m: for j = 1..n:",
                "If p[j-1] == '*': dp[i][j] = dp[i][j-2]; if match(s[i-1], p[j-2]) dp[i][j] |= dp[i-1][j].",
                "Else if match(s[i-1], p[j-1]): dp[i][j] = dp[i-1][j-1].",
                "Return dp[m][n]."
            ],
            "time": "O(m * n)",
            "space": "O(m * n)",
            "code": {
                "java": "class Solution {\n    public boolean isMatch(String s, String p) {\n        int m = s.length(), n = p.length();\n        boolean[][] dp = new boolean[m + 1][n + 1];\n        dp[0][0] = true;\n        for (int j = 2; j <= n; j++) {\n            if (p.charAt(j - 1) == '*') {\n                dp[0][j] = dp[0][j - 2];\n            }\n        }\n        for (int i = 1; i <= m; i++) {\n            for (int j = 1; j <= n; j++) {\n                if (p.charAt(j - 1) == '*') {\n                    dp[i][j] = dp[i][j - 2];\n                    if (p.charAt(j - 2) == '.' || p.charAt(j - 2) == s.charAt(i - 1)) {\n                        dp[i][j] = dp[i][j] || dp[i - 1][j];\n                    }\n                } else if (p.charAt(j - 1) == '.' || p.charAt(j - 1) == s.charAt(i - 1)) {\n                    dp[i][j] = dp[i - 1][j - 1];\n                }\n            }\n        }\n        return dp[m][n];\n    }\n}",
                "python": "class Solution:\n    def isMatch(self, s: str, p: str) -> bool:\n        m, n = len(s), len(p)\n        dp = [[False] * (n + 1) for _ in range(m + 1)]\n        dp[0][0] = True\n        for j in range(2, n + 1):\n            if p[j - 1] == '*':\n                dp[0][j] = dp[0][j - 2]\n        for i in range(1, m + 1):\n            for j in range(1, n + 1):\n                if p[j - 1] == '*':\n                    dp[i][j] = dp[i][j - 2]\n                    if p[j - 2] == '.' or p[j - 2] == s[i - 1]:\n                        dp[i][j] = dp[i][j] or dp[i - 1][j]\n                elif p[j - 1] == '.' or p[j - 1] == s[i - 1]:\n                    dp[i][j] = dp[i - 1][j - 1]\n        return dp[m][n]"
            }
        }
    },
    {
        "seq": 272,
        "whyNext": "Wildcard matching with '?' (any single char) and '*' (any sequence of chars); greedy two-pointer or 2D DP.",
        "brute": {
            "idea": "Recursion on '*' matching 0 characters, 1 character, or more.",
            "steps": [
                "dfs(s, p)."
            ],
            "time": "O(2^(m+n))",
            "space": "O(m+n)",
            "whySlow": "Exponential recursion.",
            "code": {
                "java": "class Solution {\n    public boolean isMatch(String s, String p) {\n        int m = s.length(), n = p.length();\n        boolean[][] dp = new boolean[m + 1][n + 1];\n        dp[0][0] = true;\n        for (int j = 1; j <= n; j++) {\n            if (p.charAt(j - 1) == '*') dp[0][j] = dp[0][j - 1];\n        }\n        for (int i = 1; i <= m; i++) {\n            for (int j = 1; j <= n; j++) {\n                if (p.charAt(j - 1) == '*') {\n                    dp[i][j] = dp[i - 1][j] || dp[i][j - 1];\n                } else if (p.charAt(j - 1) == '?' || p.charAt(j - 1) == s.charAt(i - 1)) {\n                    dp[i][j] = dp[i - 1][j - 1];\n                }\n            }\n        }\n        return dp[m][n];\n    }\n}",
                "python": "class Solution:\n    def isMatch(self, s: str, p: str) -> bool:\n        m, n = len(s), len(p)\n        dp = [[False] * (n + 1) for _ in range(m + 1)]\n        dp[0][0] = True\n        for j in range(1, n + 1):\n            if p[j - 1] == '*': dp[0][j] = dp[0][j - 1]\n        for i in range(1, m + 1):\n            for j in range(1, n + 1):\n                if p[j - 1] == '*':\n                    dp[i][j] = dp[i - 1][j] or dp[i][j - 1]\n                elif p[j - 1] == '?' or p[j - 1] == s[i - 1]:\n                    dp[i][j] = dp[i - 1][j - 1]\n        return dp[m][n]"
            }
        },
        "optimal": {
            "idea": "Greedy two-pointer with backtrack: record starIdx and matchIdx when '*' encountered; backtrack to '*' on mismatch in O(1) space.",
            "steps": [
                "sIdx = 0, pIdx = 0, starIdx = -1, match = 0.",
                "While sIdx < s.length():",
                "If p matches s[sIdx]: sIdx++, pIdx++.",
                "Else if p[pIdx] == '*': starIdx = pIdx++, match = sIdx.",
                "Else if starIdx != -1: pIdx = starIdx + 1; match++; sIdx = match.",
                "Else return false.",
                "Check remaining p characters are all '*'."
            ],
            "time": "O(m * n) worst case, O(m + n) average",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public boolean isMatch(String s, String p) {\n        int sIdx = 0, pIdx = 0, starIdx = -1, match = 0;\n        while (sIdx < s.length()) {\n            if (pIdx < p.length() && (p.charAt(pIdx) == '?' || p.charAt(pIdx) == s.charAt(sIdx))) {\n                sIdx++;\n                pIdx++;\n            } else if (pIdx < p.length() && p.charAt(pIdx) == '*') {\n                starIdx = pIdx;\n                match = sIdx;\n                pIdx++;\n            } else if (starIdx != -1) {\n                pIdx = starIdx + 1;\n                match++;\n                sIdx = match;\n            } else {\n                return false;\n            }\n        }\n        while (pIdx < p.length() && p.charAt(pIdx) == '*') pIdx++;\n        return pIdx == p.length();\n    }\n}",
                "python": "class Solution:\n    def isMatch(self, s: str, p: str) -> bool:\n        s_idx = p_idx = 0\n        star_idx = -1\n        match = 0\n        while s_idx < len(s):\n            if p_idx < len(p) and (p[p_idx] == '?' or p[p_idx] == s[s_idx]):\n                s_idx += 1\n                p_idx += 1\n            elif p_idx < len(p) and p[p_idx] == '*':\n                star_idx = p_idx\n                match = s_idx\n                p_idx += 1\n            elif star_idx != -1:\n                p_idx = star_idx + 1\n                match += 1\n                s_idx = match\n            else:\n                return False\n        while p_idx < len(p) and p[p_idx] == '*':\n            p_idx += 1\n        return p_idx == len(p)"
            }
        }
    },
    {
        "seq": 273,
        "whyNext": "Interval DP / think backwards: choose which balloon to burst LAST in range (l, r); dp[l][r] = max(dp[l][k] + dp[k][r] + nums[l]*nums[k]*nums[r]).",
        "brute": {
            "idea": "Recursively try bursting every balloon first, creating subproblems on list.",
            "steps": [
                "Burst balloon i, earn nums[i-1]*nums[i]*nums[i+1], recurse on remaining list."
            ],
            "time": "O(n!)",
            "space": "O(n)",
            "whySlow": "Factorial branching.",
            "code": {
                "java": "class Solution {\n    public int maxCoins(int[] nums) {\n        int n = nums.length;\n        int[] arr = new int[n + 2];\n        arr[0] = 1; arr[n + 1] = 1;\n        for (int i = 0; i < n; i++) arr[i + 1] = nums[i];\n        int[][] dp = new int[n + 2][n + 2];\n        for (int len = 1; len <= n; len++) {\n            for (int l = 1; l <= n - len + 1; l++) {\n                int r = l + len - 1;\n                for (int k = l; k <= r; k++) {\n                    int gain = arr[l - 1] * arr[k] * arr[r + 1];\n                    dp[l][r] = Math.max(dp[l][r], dp[l][k - 1] + gain + dp[k + 1][r]);\n                }\n            }\n        }\n        return dp[1][n];\n    }\n}",
                "python": "class Solution:\n    def maxCoins(self, nums: list[int]) -> int:\n        arr = [1] + nums + [1]\n        n = len(nums)\n        dp = [[0] * (n + 2) for _ in range(n + 2)]\n        for length in range(1, n + 1):\n            for l in range(1, n - length + 2):\n                r = l + length - 1\n                for k in range(l, r + 1):\n                    dp[l][r] = max(dp[l][r], dp[l][k - 1] + arr[l - 1] * arr[k] * arr[r + 1] + dp[k + 1][r])\n        return dp[1][n]"
            }
        },
        "optimal": {
            "idea": "Reverse interval DP: think of balloon k as LAST balloon burst in (l, r). dp[l][r] = max(dp[l][k-1] + arr[l-1]*arr[k]*arr[r+1] + dp[k+1][r]).",
            "steps": [
                "Pad array: arr = [1, ...nums, 1] of size n + 2.",
                "int[][] dp = new int[n + 2][n + 2].",
                "Loop length from 1 to n: loop l from 1 to n - len + 1: r = l + len - 1.",
                "For k from l to r: dp[l][r] = max(dp[l][r], dp[l][k-1] + arr[l-1]*arr[k]*arr[r+1] + dp[k+1][r]).",
                "Return dp[1][n]."
            ],
            "time": "O(n^3)",
            "space": "O(n^2)",
            "code": {
                "java": "class Solution {\n    public int maxCoins(int[] nums) {\n        int n = nums.length;\n        int[] arr = new int[n + 2];\n        arr[0] = 1;\n        arr[n + 1] = 1;\n        for (int i = 0; i < n; i++) arr[i + 1] = nums[i];\n        int[][] dp = new int[n + 2][n + 2];\n        for (int len = 1; len <= n; len++) {\n            for (int l = 1; l <= n - len + 1; l++) {\n                int r = l + len - 1;\n                for (int k = l; k <= r; k++) {\n                    int coins = arr[l - 1] * arr[k] * arr[r + 1];\n                    dp[l][r] = Math.max(dp[l][r], dp[l][k - 1] + coins + dp[k + 1][r]);\n                }\n            }\n        }\n        return dp[1][n];\n    }\n}",
                "python": "class Solution:\n    def maxCoins(self, nums: list[int]) -> int:\n        arr = [1] + nums + [1]\n        n = len(nums)\n        dp = [[0] * (n + 2) for _ in range(n + 2)]\n        for length in range(1, n + 1):\n            for l in range(1, n - length + 2):\n                r = l + length - 1\n                for k in range(l, r + 1):\n                    coins = arr[l - 1] * arr[k] * arr[r + 1]\n                    dp[l][r] = max(dp[l][r], dp[l][k - 1] + coins + dp[k + 1][r])\n        return dp[1][n]"
            }
        }
    },
    {
        "seq": 274,
        "whyNext": "State Machine DP: 3 states held, sold, reset. held = max(held, reset - price); sold = held + price; reset = max(reset, prev_sold).",
        "brute": {
            "idea": "Recursive simulation deciding buy, sell, cooldown on each day.",
            "steps": [
                "dfs(day, state)."
            ],
            "time": "O(2^n)",
            "space": "O(n)",
            "whySlow": "Exponential recursion.",
            "code": {
                "java": "class Solution {\n    public int maxProfit(int[] prices) {\n        int held = -prices[0], sold = 0, reset = 0;\n        for (int i = 1; i < prices.length; i++) {\n            int p = prices[i];\n            int prevSold = sold;\n            sold = held + p;\n            held = Math.max(held, reset - p);\n            reset = Math.max(reset, prevSold);\n        }\n        return Math.max(sold, reset);\n    }\n}",
                "python": "class Solution:\n    def maxProfit(self, prices: list[int]) -> int:\n        if not prices: return 0\n        held, sold, reset = -prices[0], 0, 0\n        for p in prices[1:]:\n            prev_sold = sold\n            sold = held + p\n            held = max(held, reset - p)\n            reset = max(reset, prev_sold)\n        return max(sold, reset)"
            }
        },
        "optimal": {
            "idea": "State machine DP in O(1) space: held = max(held, reset - p); sold = held + p; reset = max(reset, prevSold).",
            "steps": [
                "held = -prices[0], sold = 0, reset = 0.",
                "For p in prices[1..]:",
                "prevSold = sold.",
                "sold = held + p.",
                "held = max(held, reset - p).",
                "reset = max(reset, prevSold).",
                "Return max(sold, reset)."
            ],
            "time": "O(n)",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public int maxProfit(int[] prices) {\n        if (prices.length <= 1) return 0;\n        int held = -prices[0], sold = 0, reset = 0;\n        for (int i = 1; i < prices.length; i++) {\n            int prevSold = sold;\n            sold = held + prices[i];\n            held = Math.max(held, reset - prices[i]);\n            reset = Math.max(reset, prevSold);\n        }\n        return Math.max(sold, reset);\n    }\n}",
                "python": "class Solution:\n    def maxProfit(self, prices: list[int]) -> int:\n        if len(prices) <= 1:\n            return 0\n        held, sold, reset = -prices[0], 0, 0\n        for p in prices[1:]:\n            prev_sold = sold\n            sold = held + p\n            held = max(held, reset - p)\n            reset = max(reset, prev_sold)\n        return max(sold, reset)"
            }
        }
    },
    {
        "seq": 275,
        "whyNext": "Two-state DP with fee: cash = max(cash, hold + price - fee); hold = max(hold, cash - price); O(1) space.",
        "brute": {
            "idea": "Recursively test all buy and sell decisions subtracting fee on every sell.",
            "steps": [
                "dfs(day, holding)."
            ],
            "time": "O(2^n)",
            "space": "O(n)",
            "whySlow": "Exponential recursion.",
            "code": {
                "java": "class Solution {\n    public int maxProfit(int[] prices, int fee) {\n        int cash = 0, hold = -prices[0];\n        for (int i = 1; i < prices.length; i++) {\n            cash = Math.max(cash, hold + prices[i] - fee);\n            hold = Math.max(hold, cash - prices[i]);\n        }\n        return cash;\n    }\n}",
                "python": "class Solution:\n    def maxProfit(self, prices: list[int], fee: int) -> int:\n        cash, hold = 0, -prices[0]\n        for p in prices[1:]:\n            cash = max(cash, hold + p - fee)\n            hold = max(hold, cash - p)\n        return cash"
            }
        },
        "optimal": {
            "idea": "Two rolling states: cash (not holding stock) and hold (holding stock). cash = max(cash, hold + p - fee), hold = max(hold, cash - p).",
            "steps": [
                "cash = 0, hold = -prices[0].",
                "For i = 1..n-1: p = prices[i].",
                "cash = Math.max(cash, hold + p - fee).",
                "hold = Math.max(hold, cash - p).",
                "Return cash."
            ],
            "time": "O(n)",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public int maxProfit(int[] prices, int fee) {\n        int cash = 0, hold = -prices[0];\n        for (int i = 1; i < prices.length; i++) {\n            cash = Math.max(cash, hold + prices[i] - fee);\n            hold = Math.max(hold, cash - prices[i]);\n        }\n        return cash;\n    }\n}",
                "python": "class Solution:\n    def maxProfit(self, prices: list[int], fee: int) -> int:\n        cash, hold = 0, -prices[0]\n        for p in prices[1:]:\n            cash = max(cash, hold + p - fee)\n            hold = max(hold, cash - p)\n        return cash"
            }
        }
    }
]

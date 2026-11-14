# Batch 5: Questions 101 to 125

def get_batch():
    return [
    {
        "seq": 101,
        "whyNext": "Entry to recursion and divide-and-conquer: fast exponentiation computes x^n in O(log n) time.",
        "brute": {
            "idea": "Multiply x by itself |n| times in a simple loop.",
            "steps": [
                "Handle n < 0 by setting x = 1/x and n = -n.",
                "Loop from 1 to n, accumulating product.",
                "Return accumulated result."
            ],
            "time": "O(n)",
            "space": "O(1)",
            "whySlow": "For n up to 2^31 - 1, doing linear multiplications leads to Time Limit Exceeded.",
            "code": {
                "java": "class Solution {\n    public double myPow(double x, int n) {\n        long N = n;\n        if (N < 0) {\n            x = 1 / x;\n            N = -N;\n        }\n        double ans = 1;\n        for (long i = 0; i < N; i++) {\n            ans = ans * x;\n        }\n        return ans;\n    }\n}",
                "python": "class Solution:\n    def myPow(self, x: float, n: int) -> float:\n        N = n\n        if N < 0:\n            x = 1 / x\n            N = -N\n        ans = 1.0\n        for _ in range(N):\n            ans *= x\n        return ans"
            }
        },
        "optimal": {
            "idea": "Binary exponentiation: x^n = (x*x)^(n/2) if n is even, and x * (x*x)^(n//2) if odd.",
            "steps": [
                "Handle long N = n to prevent integer overflow when n = -2^31.",
                "If N < 0, invert x = 1.0 / x and N = -N.",
                "Maintain ans = 1.0; while N > 0, if N is odd multiply ans *= x, then square x *= x and halve N /= 2.",
                "Return ans."
            ],
            "time": "O(log n)",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public double myPow(double x, int n) {\n        long N = n;\n        if (N < 0) {\n            x = 1.0 / x;\n            N = -N;\n        }\n        double ans = 1.0;\n        double current = x;\n        while (N > 0) {\n            if ((N & 1) == 1) {\n                ans *= current;\n            }\n            current *= current;\n            N >>= 1;\n        }\n        return ans;\n    }\n}",
                "python": "class Solution:\n    def myPow(self, x: float, n: int) -> float:\n        N = n\n        if N < 0:\n            x = 1.0 / x\n            N = -N\n        ans = 1.0\n        current = x\n        while N > 0:\n            if N % 2 == 1:\n                ans *= current\n            current *= current\n            N //= 2\n        return ans"
            }
        }
    },
    {
        "seq": 102,
        "whyNext": "Builds on recursion fundamentals: canonical backtracking generating power set (2^n choices: include or exclude).",
        "brute": {
            "idea": "Generate all 2^n binary masks from 0 to 2^n - 1 and pick corresponding elements.",
            "steps": [
                "Iterate mask from 0 to (1 << n) - 1.",
                "For each bit i from 0 to n - 1, if bit i is set, include nums[i].",
                "Collect subset."
            ],
            "time": "O(n * 2^n)",
            "space": "O(n * 2^n)",
            "whySlow": "Generates subsets via bit manipulation without pruning; standard backtracking is cleaner for general combinatorial patterns.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<List<Integer>> subsets(int[] nums) {\n        List<List<Integer>> result = new ArrayList<>();\n        int n = nums.length;\n        for (int i = 0; i < (1 << n); i++) {\n            List<Integer> sub = new ArrayList<>();\n            for (int j = 0; j < n; j++) {\n                if ((i & (1 << j)) != 0) {\n                    sub.add(nums[j]);\n                }\n            }\n            result.add(sub);\n        }\n        return result;\n    }\n}",
                "python": "class Solution:\n    def subsets(self, nums: list[int]) -> list[list[int]]:\n        n = len(nums)\n        res = []\n        for i in range(1 << n):\n            sub = []\n            for j in range(n):\n                if (i >> j) & 1:\n                    sub.append(nums[j])\n            res.append(sub)\n        return res"
            }
        },
        "optimal": {
            "idea": "Backtracking (DFS): at each index, recurse by either including the current element or choosing next elements.",
            "steps": [
                "Define backtrack(start, currentPath).",
                "Add a copy of currentPath to result.",
                "For i from start to n - 1: add nums[i] to path, recurse backtrack(i + 1, path), then pop nums[i].",
                "Start at backtrack(0, [])."
            ],
            "time": "O(n * 2^n)",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<List<Integer>> subsets(int[] nums) {\n        List<List<Integer>> res = new ArrayList<>();\n        backtrack(0, nums, new ArrayList<>(), res);\n        return res;\n    }\n    private void backtrack(int start, int[] nums, List<Integer> path, List<List<Integer>> res) {\n        res.add(new ArrayList<>(path));\n        for (int i = start; i < nums.length; i++) {\n            path.add(nums[i]);\n            backtrack(i + 1, nums, path, res);\n            path.remove(path.size() - 1);\n        }\n    }\n}",
                "python": "class Solution:\n    def subsets(self, nums: list[int]) -> list[list[int]]:\n        res = []\n        path = []\n        def backtrack(start: int):\n            res.append(list(path))\n            for i in range(start, len(nums)):\n                path.append(nums[i])\n                backtrack(i + 1)\n                path.pop()\n        backtrack(0)\n        return res"
            }
        }
    },
    {
        "seq": 103,
        "whyNext": "Builds on Subsets: handles duplicate numbers by sorting and skipping identical sibling branches.",
        "brute": {
            "idea": "Generate all subsets like Subsets I, sort each subset and put into a Set to filter duplicates.",
            "steps": [
                "Generate all subsets using bitmasks or simple recursion.",
                "Sort each subset and store in a HashSet to deduplicate.",
                "Convert set back to list."
            ],
            "time": "O(n * log n * 2^n)",
            "space": "O(n * 2^n)",
            "whySlow": "Generates 2^n duplicate combinations and spends extra time hashing and sorting subsets.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<List<Integer>> subsetsWithDup(int[] nums) {\n        Arrays.sort(nums);\n        Set<List<Integer>> set = new HashSet<>();\n        int n = nums.length;\n        for (int i = 0; i < (1 << n); i++) {\n            List<Integer> sub = new ArrayList<>();\n            for (int j = 0; j < n; j++) {\n                if ((i & (1 << j)) != 0) sub.add(nums[j]);\n            }\n            set.add(sub);\n        }\n        return new ArrayList<>(set);\n    }\n}",
                "python": "class Solution:\n    def subsetsWithDup(self, nums: list[int]) -> list[list[int]]:\n        nums.sort()\n        res = set()\n        n = len(nums)\n        for i in range(1 << n):\n            sub = []\n            for j in range(n):\n                if (i >> j) & 1:\n                    sub.append(nums[j])\n            res.add(tuple(sub))\n        return [list(x) for x in res]"
            }
        },
        "optimal": {
            "idea": "Sort the array upfront; in the loop, if nums[i] == nums[i - 1] and i > start, skip to avoid duplicate branches.",
            "steps": [
                "Sort nums array.",
                "In backtrack(start, path), append copy of path to result.",
                "Loop i from start to n - 1: if i > start and nums[i] == nums[i - 1], continue.",
                "Push nums[i], recurse backtrack(i + 1), pop nums[i]."
            ],
            "time": "O(n * 2^n)",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<List<Integer>> subsetsWithDup(int[] nums) {\n        Arrays.sort(nums);\n        List<List<Integer>> res = new ArrayList<>();\n        backtrack(0, nums, new ArrayList<>(), res);\n        return res;\n    }\n    private void backtrack(int start, int[] nums, List<Integer> path, List<List<Integer>> res) {\n        res.add(new ArrayList<>(path));\n        for (int i = start; i < nums.length; i++) {\n            if (i > start && nums[i] == nums[i - 1]) continue;\n            path.add(nums[i]);\n            backtrack(i + 1, nums, path, res);\n            path.remove(path.size() - 1);\n        }\n    }\n}",
                "python": "class Solution:\n    def subsetsWithDup(self, nums: list[int]) -> list[list[int]]:\n        nums.sort()\n        res = []\n        path = []\n        def backtrack(start: int):\n            res.append(list(path))\n            for i in range(start, len(nums)):\n                if i > start and nums[i] == nums[i - 1]:\n                    continue\n                path.append(nums[i])\n                backtrack(i + 1)\n                path.pop()\n        backtrack(0)\n        return res"
            }
        }
    },
    {
        "seq": 104,
        "whyNext": "Builds on Subsets: allows reusing elements infinitely until target is reached or exceeded.",
        "brute": {
            "idea": "Try all combinations of counts for each candidate up to target / candidate.",
            "steps": [
                "Recursively try adding each candidate from 0 up to target / candidate times.",
                "If remaining target == 0, record path.",
                "If remaining target < 0, terminate branch."
            ],
            "time": "O(N^(T/M))",
            "space": "O(T/M)",
            "whySlow": "Without sorting and pruning early, explores many redundant overshooting branches.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<List<Integer>> combinationSum(int[] candidates, int target) {\n        List<List<Integer>> res = new ArrayList<>();\n        dfs(0, candidates, target, new ArrayList<>(), res);\n        return res;\n    }\n    private void dfs(int idx, int[] c, int rem, List<Integer> path, List<List<Integer>> res) {\n        if (rem == 0) {\n            res.add(new ArrayList<>(path));\n            return;\n        }\n        if (idx == c.length || rem < 0) return;\n        dfs(idx + 1, c, rem, path, res);\n        path.add(c[idx]);\n        dfs(idx, c, rem - c[idx], path, res);\n        path.remove(path.size() - 1);\n    }\n}",
                "python": "class Solution:\n    def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]:\n        res = []\n        def dfs(idx: int, rem: int, path: list[int]):\n            if rem == 0:\n                res.append(list(path))\n                return\n            if idx == len(candidates) or rem < 0:\n                return\n            dfs(idx + 1, rem, path)\n            path.append(candidates[idx])\n            dfs(idx, rem - candidates[idx], path)\n            path.pop()\n        dfs(0, target, [])\n        return res"
            }
        },
        "optimal": {
            "idea": "Sort candidates; backtrack from start index. If candidates[i] > rem, break immediately to prune entire search subtree.",
            "steps": [
                "Sort candidates in ascending order.",
                "In backtrack(start, rem, path): if rem == 0, save copy of path.",
                "Loop i from start to len - 1: if candidates[i] > rem, break.",
                "path.add(candidates[i]), backtrack(i, rem - candidates[i], path), path.pop()."
            ],
            "time": "O(2^target)",
            "space": "O(target / min(candidate))",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<List<Integer>> combinationSum(int[] candidates, int target) {\n        Arrays.sort(candidates);\n        List<List<Integer>> res = new ArrayList<>();\n        backtrack(0, target, candidates, new ArrayList<>(), res);\n        return res;\n    }\n    private void backtrack(int start, int rem, int[] candidates, List<Integer> path, List<List<Integer>> res) {\n        if (rem == 0) {\n            res.add(new ArrayList<>(path));\n            return;\n        }\n        for (int i = start; i < candidates.length; i++) {\n            if (candidates[i] > rem) break;\n            path.add(candidates[i]);\n            backtrack(i, rem - candidates[i], candidates, path, res);\n            path.remove(path.size() - 1);\n        }\n    }\n}",
                "python": "class Solution:\n    def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]:\n        candidates.sort()\n        res = []\n        path = []\n        def backtrack(start: int, rem: int):\n            if rem == 0:\n                res.append(list(path))\n                return\n            for i in range(start, len(candidates)):\n                if candidates[i] > rem:\n                    break\n                path.append(candidates[i])\n                backtrack(i, rem - candidates[i])\n                path.pop()\n        backtrack(0, target)\n        return res"
            }
        }
    },
    {
        "seq": 105,
        "whyNext": "Combines Combination Sum with duplicate skipping from Subsets II: each element can only be used once.",
        "brute": {
            "idea": "Explore all subsets summing to target, use set to filter duplicate combinations.",
            "steps": [
                "Sort candidates.",
                "Generate all combinations where each element is used at most once.",
                "Store valid paths in a Set to eliminate duplicates."
            ],
            "time": "O(2^n * n)",
            "space": "O(2^n * n)",
            "whySlow": "Generating duplicate combinations and hashing lists causes high memory overhead and TLE.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<List<Integer>> combinationSum2(int[] candidates, int target) {\n        Arrays.sort(candidates);\n        Set<List<Integer>> set = new HashSet<>();\n        dfs(0, candidates, target, new ArrayList<>(), set);\n        return new ArrayList<>(set);\n    }\n    private void dfs(int idx, int[] c, int rem, List<Integer> path, Set<List<Integer>> set) {\n        if (rem == 0) {\n            set.add(new ArrayList<>(path));\n            return;\n        }\n        if (idx == c.length || rem < 0) return;\n        dfs(idx + 1, c, rem, path, set);\n        path.add(c[idx]);\n        dfs(idx + 1, c, rem - c[idx], path, set);\n        path.remove(path.size() - 1);\n    }\n}",
                "python": "class Solution:\n    def combinationSum2(self, candidates: list[int], target: int) -> list[list[int]]:\n        candidates.sort()\n        res = set()\n        def dfs(idx: int, rem: int, path: list[int]):\n            if rem == 0:\n                res.add(tuple(path))\n                return\n            if idx == len(candidates) or rem < 0:\n                return\n            dfs(idx + 1, rem, path)\n            path.append(candidates[idx])\n            dfs(idx + 1, rem - candidates[idx], path)\n            path.pop()\n        dfs(0, target, [])\n        return [list(x) for x in res]"
            }
        },
        "optimal": {
            "idea": "Sort candidates. When looping over candidates, skip if candidates[i] == candidates[i - 1] when i > start; break early if candidates[i] > rem.",
            "steps": [
                "Sort candidates.",
                "Define backtrack(start, rem, path): if rem == 0 add path to res and return.",
                "Loop i from start to n - 1: if candidates[i] > rem break.",
                "If i > start and candidates[i] == candidates[i - 1] continue.",
                "path.add(candidates[i]), backtrack(i + 1, rem - candidates[i], path), path.pop()."
            ],
            "time": "O(2^n)",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<List<Integer>> combinationSum2(int[] candidates, int target) {\n        Arrays.sort(candidates);\n        List<List<Integer>> res = new ArrayList<>();\n        backtrack(0, target, candidates, new ArrayList<>(), res);\n        return res;\n    }\n    private void backtrack(int start, int rem, int[] candidates, List<Integer> path, List<List<Integer>> res) {\n        if (rem == 0) {\n            res.add(new ArrayList<>(path));\n            return;\n        }\n        for (int i = start; i < candidates.length; i++) {\n            if (candidates[i] > rem) break;\n            if (i > start && candidates[i] == candidates[i - 1]) continue;\n            path.add(candidates[i]);\n            backtrack(i + 1, rem - candidates[i], candidates, path, res);\n            path.remove(path.size() - 1);\n        }\n    }\n}",
                "python": "class Solution:\n    def combinationSum2(self, candidates: list[int], target: int) -> list[list[int]]:\n        candidates.sort()\n        res = []\n        path = []\n        def backtrack(start: int, rem: int):\n            if rem == 0:\n                res.append(list(path))\n                return\n            for i in range(start, len(candidates)):\n                if candidates[i] > rem:\n                    break\n                if i > start and candidates[i] == candidates[i - 1]:\n                    continue\n                path.append(candidates[i])\n                backtrack(i + 1, rem - candidates[i])\n                path.pop()\n        backtrack(0, target)\n        return res"
            }
        }
    },
    {
        "seq": 106,
        "whyNext": "Constrains combination size to exactly k numbers from 1 to 9 with target sum n.",
        "brute": {
            "idea": "Try all subsets of {1..9}; filter those of size k that sum to n.",
            "steps": [
                "Iterate through 2^9 masks.",
                "For each mask, check if count of set bits is k and sum of elements equals n.",
                "If both match, add subset to result."
            ],
            "time": "O(2^9 * 9)",
            "space": "O(2^9 * 9)",
            "whySlow": "Evaluates all subsets blindly even when sum already exceeds n or size cannot reach k.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<List<Integer>> combinationSum3(int k, int n) {\n        List<List<Integer>> res = new ArrayList<>();\n        for (int mask = 0; mask < (1 << 9); mask++) {\n            if (Integer.bitCount(mask) != k) continue;\n            int sum = 0;\n            List<Integer> list = new ArrayList<>();\n            for (int i = 0; i < 9; i++) {\n                if ((mask & (1 << i)) != 0) {\n                    sum += (i + 1);\n                    list.add(i + 1);\n                }\n            }\n            if (sum == n) res.add(list);\n        }\n        return res;\n    }\n}",
                "python": "class Solution:\n    def combinationSum3(self, k: int, n: int) -> list[list[int]]:\n        res = []\n        for mask in range(1 << 9):\n            if bin(mask).count('1') != k:\n                continue\n            sub = [i + 1 for i in range(9) if (mask >> i) & 1]\n            if sum(sub) == n:\n                res.append(sub)\n        return res"
            }
        },
        "optimal": {
            "idea": "Backtracking with size and sum pruning: choose numbers from start to 9; prune if remaining sum < 0 or path.size() > k.",
            "steps": [
                "Define backtrack(start, rem, k, path).",
                "If path.size() == k and rem == 0, add copy to res and return.",
                "If path.size() >= k or rem < start, return.",
                "Loop i from start to 9: path.add(i), backtrack(i + 1, rem - i, k, path), path.pop()."
            ],
            "time": "O(C(9, k))",
            "space": "O(k)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<List<Integer>> combinationSum3(int k, int n) {\n        List<List<Integer>> res = new ArrayList<>();\n        backtrack(1, n, k, new ArrayList<>(), res);\n        return res;\n    }\n    private void backtrack(int start, int rem, int k, List<Integer> path, List<List<Integer>> res) {\n        if (path.size() == k) {\n            if (rem == 0) res.add(new ArrayList<>(path));\n            return;\n        }\n        for (int i = start; i <= 9; i++) {\n            if (i > rem) break;\n            path.add(i);\n            backtrack(i + 1, rem - i, k, path, res);\n            path.remove(path.size() - 1);\n        }\n    }\n}",
                "python": "class Solution:\n    def combinationSum3(self, k: int, n: int) -> list[list[int]]:\n        res = []\n        path = []\n        def backtrack(start: int, rem: int):\n            if len(path) == k:\n                if rem == 0:\n                    res.append(list(path))\n                return\n            for i in range(start, 10):\n                if i > rem:\n                    break\n                path.append(i)\n                backtrack(i + 1, rem - i)\n                path.pop()\n        backtrack(1, n)\n        return res"
            }
        }
    },
    {
        "seq": 107,
        "whyNext": "Classic n choose k combinations; introduces recursive tree pruning based on remaining needed count.",
        "brute": {
            "idea": "Generate all subsets of {1..n} and select subsets of length exactly k.",
            "steps": [
                "Recurse through all numbers from 1 to n with include/exclude.",
                "If subset size reaches k and index reaches n, add subset to result."
            ],
            "time": "O(2^n)",
            "space": "O(n)",
            "whySlow": "Visits all 2^n subsets instead of just C(n, k).",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<List<Integer>> combine(int n, int k) {\n        List<List<Integer>> res = new ArrayList<>();\n        dfs(1, n, k, new ArrayList<>(), res);\n        return res;\n    }\n    private void dfs(int cur, int n, int k, List<Integer> path, List<List<Integer>> res) {\n        if (path.size() == k) {\n            res.add(new ArrayList<>(path));\n            return;\n        }\n        if (cur > n) return;\n        path.add(cur);\n        dfs(cur + 1, n, k, path, res);\n        path.remove(path.size() - 1);\n        dfs(cur + 1, n, k, path, res);\n    }\n}",
                "python": "class Solution:\n    def combine(self, n: int, k: int) -> list[list[int]]:\n        res = []\n        path = []\n        def dfs(cur: int):\n            if len(path) == k:\n                res.append(list(path))\n                return\n            if cur > n:\n                return\n            path.append(cur)\n            dfs(cur + 1)\n            path.pop()\n            dfs(cur + 1)\n        dfs(1)\n        return res"
            }
        },
        "optimal": {
            "idea": "Backtracking with upper bound pruning: loop i from start up to n - (k - path.size()) + 1.",
            "steps": [
                "If path.size() == k, add to res and return.",
                "Only iterate up to n - (k - path.size()) + 1, ensuring enough elements remain to fill k slots.",
                "path.add(i), backtrack(i + 1), path.pop()."
            ],
            "time": "O(k * C(n, k))",
            "space": "O(k)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<List<Integer>> combine(int n, int k) {\n        List<List<Integer>> res = new ArrayList<>();\n        backtrack(1, n, k, new ArrayList<>(), res);\n        return res;\n    }\n    private void backtrack(int start, int n, int k, List<Integer> path, List<List<Integer>> res) {\n        if (path.size() == k) {\n            res.add(new ArrayList<>(path));\n            return;\n        }\n        int need = k - path.size();\n        for (int i = start; i <= n - need + 1; i++) {\n            path.add(i);\n            backtrack(i + 1, n, k, path, res);\n            path.remove(path.size() - 1);\n        }\n    }\n}",
                "python": "class Solution:\n    def combine(self, n: int, k: int) -> list[list[int]]:\n        res = []\n        path = []\n        def backtrack(start: int):\n            if len(path) == k:\n                res.append(list(path))\n                return\n            need = k - len(path)\n            for i in range(start, n - need + 2):\n                path.append(i)\n                backtrack(i + 1)\n                path.pop()\n        backtrack(1)\n        return res"
            }
        }
    },
    {
        "seq": 108,
        "whyNext": "Transitions from combinations (order doesn't matter) to permutations (order matters; use visited array or swap).",
        "brute": {
            "idea": "Generate all n^n sequences of elements and retain only those with all unique elements.",
            "steps": [
                "Generate all combinations of length n with replacement.",
                "Check each combination if it contains all unique elements of nums.",
                "Collect valid permutations."
            ],
            "time": "O(n^n)",
            "space": "O(n^n)",
            "whySlow": "Exponentially generates redundant sequences containing repeated elements.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<List<Integer>> permute(int[] nums) {\n        List<List<Integer>> res = new ArrayList<>();\n        dfs(nums, new ArrayList<>(), res);\n        return res;\n    }\n    private void dfs(int[] nums, List<Integer> path, List<List<Integer>> res) {\n        if (path.size() == nums.length) {\n            res.add(new ArrayList<>(path));\n            return;\n        }\n        for (int num : nums) {\n            if (path.contains(num)) continue;\n            path.add(num);\n            dfs(nums, path, res);\n            path.remove(path.size() - 1);\n        }\n    }\n}",
                "python": "class Solution:\n    def permute(self, nums: list[int]) -> list[list[int]]:\n        res = []\n        path = []\n        def dfs():\n            if len(path) == len(nums):\n                res.append(list(path))\n                return\n            for x in nums:\n                if x not in path:\n                    path.append(x)\n                    dfs()\n                    path.pop()\n        dfs()\n        return res"
            }
        },
        "optimal": {
            "idea": "In-place swapping backtracking avoids extra visited state and achieves O(1) auxiliary space.",
            "steps": [
                "Define backtrack(first): if first == n, add current list state to res.",
                "For i from first to n - 1: swap(first, i), backtrack(first + 1), swap(first, i)."
            ],
            "time": "O(n * n!)",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<List<Integer>> permute(int[] nums) {\n        List<List<Integer>> res = new ArrayList<>();\n        List<Integer> list = new ArrayList<>();\n        for (int x : nums) list.add(x);\n        backtrack(0, list, res);\n        return res;\n    }\n    private void backtrack(int first, List<Integer> list, List<List<Integer>> res) {\n        if (first == list.size()) {\n            res.add(new ArrayList<>(list));\n            return;\n        }\n        for (int i = first; i < list.size(); i++) {\n            Collections.swap(list, first, i);\n            backtrack(first + 1, list, res);\n            Collections.swap(list, first, i);\n        }\n    }\n}",
                "python": "class Solution:\n    def permute(self, nums: list[int]) -> list[list[int]]:\n        res = []\n        def backtrack(first: int):\n            if first == len(nums):\n                res.append(list(nums))\n                return\n            for i in range(first, len(nums)):\n                nums[first], nums[i] = nums[i], nums[first]\n                backtrack(first + 1)\n                nums[first], nums[i] = nums[i], nums[first]\n        backtrack(0)\n        return res"
            }
        }
    },
    {
        "seq": 109,
        "whyNext": "Builds on Permutations: duplicate elements require sorting and a boolean used[] array to skip duplicate choices.",
        "brute": {
            "idea": "Generate all permutations like Permutations I, then use a Set to eliminate duplicates.",
            "steps": [
                "Run standard permutations algorithm.",
                "Insert every generated permutation into a Set.",
                "Return list of set elements."
            ],
            "time": "O(n * n!)",
            "space": "O(n * n!)",
            "whySlow": "Does work exploring permutations that are identical, wasting time and memory.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<List<Integer>> permuteUnique(int[] nums) {\n        Set<List<Integer>> set = new HashSet<>();\n        boolean[] used = new boolean[nums.length];\n        dfs(nums, used, new ArrayList<>(), set);\n        return new ArrayList<>(set);\n    }\n    private void dfs(int[] nums, boolean[] used, List<Integer> path, Set<List<Integer>> set) {\n        if (path.size() == nums.length) {\n            set.add(new ArrayList<>(path));\n            return;\n        }\n        for (int i = 0; i < nums.length; i++) {\n            if (used[i]) continue;\n            used[i] = true;\n            path.add(nums[i]);\n            dfs(nums, used, path, set);\n            path.remove(path.size() - 1);\n            used[i] = false;\n        }\n    }\n}",
                "python": "class Solution:\n    def permuteUnique(self, nums: list[int]) -> list[list[int]]:\n        res = set()\n        used = [False] * len(nums)\n        path = []\n        def dfs():\n            if len(path) == len(nums):\n                res.add(tuple(path))\n                return\n            for i in range(len(nums)):\n                if not used[i]:\n                    used[i] = True\n                    path.append(nums[i])\n                    dfs()\n                    path.pop()\n                    used[i] = False\n        dfs()\n        return [list(x) for x in res]"
            }
        },
        "optimal": {
            "idea": "Sort nums; track used[i]. Skip element i if nums[i] == nums[i - 1] and !used[i - 1] (meaning sibling branch just finished).",
            "steps": [
                "Sort nums array.",
                "In backtrack(path, used): if path.size() == nums.length, add to result.",
                "Loop i from 0 to n - 1: if used[i], continue.",
                "If i > 0 and nums[i] == nums[i - 1] and !used[i - 1], continue.",
                "Set used[i] = true, path.add(nums[i]), backtrack(), path.pop(), used[i] = false."
            ],
            "time": "O(n * n!)",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<List<Integer>> permuteUnique(int[] nums) {\n        Arrays.sort(nums);\n        List<List<Integer>> res = new ArrayList<>();\n        boolean[] used = new boolean[nums.length];\n        backtrack(nums, used, new ArrayList<>(), res);\n        return res;\n    }\n    private void backtrack(int[] nums, boolean[] used, List<Integer> path, List<List<Integer>> res) {\n        if (path.size() == nums.length) {\n            res.add(new ArrayList<>(path));\n            return;\n        }\n        for (int i = 0; i < nums.length; i++) {\n            if (used[i]) continue;\n            if (i > 0 && nums[i] == nums[i - 1] && !used[i - 1]) continue;\n            used[i] = true;\n            path.add(nums[i]);\n            backtrack(nums, used, path, res);\n            path.remove(path.size() - 1);\n            used[i] = false;\n        }\n    }\n}",
                "python": "class Solution:\n    def permuteUnique(self, nums: list[int]) -> list[list[int]]:\n        nums.sort()\n        res = []\n        used = [False] * len(nums)\n        path = []\n        def backtrack():\n            if len(path) == len(nums):\n                res.append(list(path))\n                return\n            for i in range(len(nums)):\n                if used[i]:\n                    continue\n                if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:\n                    continue\n                used[i] = True\n                path.append(nums[i])\n                backtrack()\n                path.pop()\n                used[i] = False\n        backtrack()\n        return res"
            }
        }
    },
    {
        "seq": 110,
        "whyNext": "Branching factor of 2 at letter positions and 1 at digits: builds binary tree of character cases.",
        "brute": {
            "idea": "For every character, generate all 2^k case combinations using recursion building full string copies.",
            "steps": [
                "Recursively append lowercase and uppercase choices at each index.",
                "Accumulate strings into result list."
            ],
            "time": "O(n * 2^n)",
            "space": "O(n * 2^n)",
            "whySlow": "Allocating new strings at each intermediate recursive level increases memory churn.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<String> letterCasePermutation(String s) {\n        List<String> res = new ArrayList<>();\n        dfs(s, 0, \"\", res);\n        return res;\n    }\n    private void dfs(String s, int idx, String cur, List<String> res) {\n        if (idx == s.length()) {\n            res.add(cur);\n            return;\n        }\n        char c = s.charAt(idx);\n        if (Character.isLetter(c)) {\n            dfs(s, idx + 1, cur + Character.toLowerCase(c), res);\n            dfs(s, idx + 1, cur + Character.toUpperCase(c), res);\n        } else {\n            dfs(s, idx + 1, cur + c, res);\n        }\n    }\n}",
                "python": "class Solution:\n    def letterCasePermutation(self, s: str) -> list[str]:\n        res = []\n        def dfs(idx: int, cur: str):\n            if idx == len(s):\n                res.append(cur)\n                return\n            c = s[idx]\n            if c.isalpha():\n                dfs(idx + 1, cur + c.lower())\n                dfs(idx + 1, cur + c.upper())\n            else:\n                dfs(idx + 1, cur + c)\n        dfs(0, \"\")\n        return res"
            }
        },
        "optimal": {
            "idea": "Backtrack in-place modifying a single char array.",
            "steps": [
                "Convert string to char array chars.",
                "In backtrack(idx): if idx == chars.length, add String.valueOf(chars) to res and return.",
                "If chars[idx] is a letter, mutate to lowercase, backtrack(idx + 1), mutate to uppercase, backtrack(idx + 1).",
                "If digit, simply backtrack(idx + 1)."
            ],
            "time": "O(n * 2^k)",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<String> letterCasePermutation(String s) {\n        List<String> res = new ArrayList<>();\n        char[] chars = s.toCharArray();\n        backtrack(chars, 0, res);\n        return res;\n    }\n    private void backtrack(char[] chars, int idx, List<String> res) {\n        if (idx == chars.length) {\n            res.add(new String(chars));\n            return;\n        }\n        if (Character.isLetter(chars[idx])) {\n            chars[idx] = Character.toLowerCase(chars[idx]);\n            backtrack(chars, idx + 1, res);\n            chars[idx] = Character.toUpperCase(chars[idx]);\n            backtrack(chars, idx + 1, res);\n        } else {\n            backtrack(chars, idx + 1, res);\n        }\n    }\n}",
                "python": "class Solution:\n    def letterCasePermutation(self, s: str) -> list[str]:\n        res = []\n        chars = list(s)\n        def backtrack(idx: int):\n            if idx == len(chars):\n                res.append(\"\".join(chars))\n                return\n            if chars[idx].isalpha():\n                chars[idx] = chars[idx].lower()\n                backtrack(idx + 1)\n                chars[idx] = chars[idx].upper()\n                backtrack(idx + 1)\n            else:\n                backtrack(idx + 1)\n        backtrack(0)\n        return res"
            }
        }
    },
    {
        "seq": 111,
        "whyNext": "Multi-way tree recursion: each digit expands to 3 or 4 letter choices mapped via lookup array.",
        "brute": {
            "idea": "Cartesian product of character lists for each digit.",
            "steps": [
                "Map each digit to its list of letters.",
                "Take cross product across all mapped lists."
            ],
            "time": "O(4^n * n)",
            "space": "O(4^n * n)",
            "whySlow": "Constructs temporary lists across iterations instead of DFS with single StringBuilder.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<String> letterCombinations(String digits) {\n        if (digits.isEmpty()) return Collections.emptyList();\n        String[] map = {\"\", \"\", \"abc\", \"def\", \"ghi\", \"jkl\", \"mno\", \"pqrs\", \"tuv\", \"wxyz\"};\n        List<String> res = new ArrayList<>();\n        res.add(\"\");\n        for (char d : digits.toCharArray()) {\n            List<String> next = new ArrayList<>();\n            for (String s : res) {\n                for (char c : map[d - '0'].toCharArray()) {\n                    next.add(s + c);\n                }\n            }\n            res = next;\n        }\n        return res;\n    }\n}",
                "python": "class Solution:\n    def letterCombinations(self, digits: str) -> list[str]:\n        if not digits:\n            return []\n        phone = [\"\", \"\", \"abc\", \"def\", \"ghi\", \"jkl\", \"mno\", \"pqrs\", \"tuv\", \"wxyz\"]\n        res = [\"\"]\n        for d in digits:\n            res = [s + c for s in res for c in phone[int(d)]]\n        return res"
            }
        },
        "optimal": {
            "idea": "Backtracking with StringBuilder: recurse on digit index, push letter, recurse, pop letter.",
            "steps": [
                "Define constant mapping array for digits 2-9.",
                "In backtrack(index, path): if index == digits.length, add path.toString() to res.",
                "Loop through mapped letters of digits[index]: append char, backtrack(index + 1), delete last char."
            ],
            "time": "O(4^n * n)",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    private static final String[] MAPPING = {\n        \"\", \"\", \"abc\", \"def\", \"ghi\", \"jkl\", \"mno\", \"pqrs\", \"tuv\", \"wxyz\"\n    };\n    public List<String> letterCombinations(String digits) {\n        List<String> res = new ArrayList<>();\n        if (digits == null || digits.isEmpty()) return res;\n        backtrack(digits, 0, new StringBuilder(), res);\n        return res;\n    }\n    private void backtrack(String digits, int idx, StringBuilder path, List<String> res) {\n        if (idx == digits.length()) {\n            res.add(path.toString());\n            return;\n        }\n        String letters = MAPPING[digits.charAt(idx) - '0'];\n        for (int i = 0; i < letters.length(); i++) {\n            path.append(letters.charAt(i));\n            backtrack(digits, idx + 1, path, res);\n            path.deleteCharAt(path.length() - 1);\n        }\n    }\n}",
                "python": "class Solution:\n    def letterCombinations(self, digits: str) -> list[str]:\n        if not digits:\n            return []\n        mapping = [\"\", \"\", \"abc\", \"def\", \"ghi\", \"jkl\", \"mno\", \"pqrs\", \"tuv\", \"wxyz\"]\n        res = []\n        path = []\n        def backtrack(idx: int):\n            if idx == len(digits):\n                res.append(\"\".join(path))\n                return\n            for c in mapping[int(digits[idx])]:\n                path.append(c)\n                backtrack(idx + 1)\n                path.pop()\n        backtrack(0)\n        return res"
            }
        }
    },
    {
        "seq": 112,
        "whyNext": "Catalan number branching with invariant: close parenthesis can only be placed when close < open.",
        "brute": {
            "idea": "Generate all 2^(2n) sequences of '(' and ')' and validate parentheses with a balance counter.",
            "steps": [
                "Recursively generate all binary strings of length 2n consisting of '(' and ')'.",
                "For each generated string, verify if every prefix has balance >= 0 and final balance == 0.",
                "Keep valid strings."
            ],
            "time": "O(2^(2n) * n)",
            "space": "O(2^(2n) * n)",
            "whySlow": "Generates 2^(2n) strings where only C_n strings are valid; vast majority are invalid early on.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<String> generateParenthesis(int n) {\n        List<String> res = new ArrayList<>();\n        generateAll(new char[2 * n], 0, res);\n        return res;\n    }\n    private void generateAll(char[] current, int pos, List<String> result) {\n        if (pos == current.length) {\n            if (valid(current)) result.add(new String(current));\n            return;\n        }\n        current[pos] = '(';\n        generateAll(current, pos + 1, result);\n        current[pos] = ')';\n        generateAll(current, pos + 1, result);\n    }\n    private boolean valid(char[] current) {\n        int balance = 0;\n        for (char c : current) {\n            if (c == '(') balance++;\n            else balance--;\n            if (balance < 0) return false;\n        }\n        return balance == 0;\n    }\n}",
                "python": "class Solution:\n    def generateParenthesis(self, n: int) -> list[str]:\n        res = []\n        def valid(s: str) -> bool:\n            bal = 0\n            for c in s:\n                bal += 1 if c == '(' else -1\n                if bal < 0: return False\n            return bal == 0\n        def generate(s: str):\n            if len(s) == 2 * n:\n                if valid(s): res.append(s)\n                return\n            generate(s + '(')\n            generate(s + ')')\n        generate('')\n        return res"
            }
        },
        "optimal": {
            "idea": "Backtracking with open/close counts: only add '(' if open < n; only add ')' if close < open.",
            "steps": [
                "Maintain open count and close count.",
                "If open == n and close == n, append current string to result.",
                "If open < n: append '(', backtrack(open + 1, close), pop.",
                "If close < open: append ')', backtrack(open, close + 1), pop."
            ],
            "time": "O(4^n / sqrt(n))",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<String> generateParenthesis(int n) {\n        List<String> res = new ArrayList<>();\n        backtrack(new StringBuilder(), 0, 0, n, res);\n        return res;\n    }\n    private void backtrack(StringBuilder sb, int open, int close, int n, List<String> res) {\n        if (sb.length() == 2 * n) {\n            res.add(sb.toString());\n            return;\n        }\n        if (open < n) {\n            sb.append('(');\n            backtrack(sb, open + 1, close, n, res);\n            sb.deleteCharAt(sb.length() - 1);\n        }\n        if (close < open) {\n            sb.append(')');\n            backtrack(sb, open, close + 1, n, res);\n            sb.deleteCharAt(sb.length() - 1);\n        }\n    }\n}",
                "python": "class Solution:\n    def generateParenthesis(self, n: int) -> list[str]:\n        res = []\n        path = []\n        def backtrack(open_cnt: int, close_cnt: int):\n            if len(path) == 2 * n:\n                res.append(\"\".join(path))\n                return\n            if open_cnt < n:\n                path.append('(')\n                backtrack(open_cnt + 1, close_cnt)\n                path.pop()\n            if close_cnt < open_cnt:\n                path.append(')')\n                backtrack(open_cnt, close_cnt + 1)\n                path.pop()\n        backtrack(0, 0)\n        return res"
            }
        }
    },
    {
        "seq": 113,
        "whyNext": "String partition backtracking: split string into substrings such that every substring is a palindrome.",
        "brute": {
            "idea": "Try all 2^(n-1) split points; for each partition check whether all substrings are palindromes.",
            "steps": [
                "Recursively test every end index for the current substring.",
                "Check palindrome by reversing substring each time."
            ],
            "time": "O(n * 2^n)",
            "space": "O(n)",
            "whySlow": "Checks palindrome repeatedly on the fly with string reversals.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<List<String>> partition(String s) {\n        List<List<String>> res = new ArrayList<>();\n        dfs(0, s, new ArrayList<>(), res);\n        return res;\n    }\n    private void dfs(int start, String s, List<String> path, List<List<String>> res) {\n        if (start == s.length()) {\n            res.add(new ArrayList<>(path));\n            return;\n        }\n        for (int end = start; end < s.length(); end++) {\n            if (isPalindrome(s, start, end)) {\n                path.add(s.substring(start, end + 1));\n                dfs(end + 1, s, path, res);\n                path.remove(path.size() - 1);\n            }\n        }\n    }\n    private boolean isPalindrome(String s, int l, int r) {\n        while (l < r) {\n            if (s.charAt(l++) != s.charAt(r--)) return false;\n        }\n        return true;\n    }\n}",
                "python": "class Solution:\n    def partition(self, s: str) -> list[list[str]]:\n        res = []\n        path = []\n        def is_pal(sub: str) -> bool:\n            return sub == sub[::-1]\n        def dfs(start: int):\n            if start == len(s):\n                res.append(list(path))\n                return\n            for end in range(start, len(s)):\n                sub = s[start:end+1]\n                if is_pal(sub):\n                    path.append(sub)\n                    dfs(end + 1)\n                    path.pop()\n        dfs(0)\n        return res"
            }
        },
        "optimal": {
            "idea": "Precompute palindrome table dp[i][j] in O(n^2), then backtrack using the table in O(1) per lookup.",
            "steps": [
                "Create boolean[][] dp of size n x n.",
                "dp[i][j] is true if s[i] == s[j] and (j - i <= 2 || dp[i+1][j-1]).",
                "In backtrack(start): if start == n add path to res.",
                "Loop end from start to n - 1: if dp[start][end], path.add(s[start..end]), backtrack(end + 1), path.pop()."
            ],
            "time": "O(n * 2^n)",
            "space": "O(n^2)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<List<String>> partition(String s) {\n        int n = s.length();\n        boolean[][] dp = new boolean[n][n];\n        for (int len = 1; len <= n; len++) {\n            for (int i = 0; i <= n - len; i++) {\n                int j = i + len - 1;\n                if (s.charAt(i) == s.charAt(j)) {\n                    dp[i][j] = (len <= 2) || dp[i + 1][j - 1];\n                }\n            }\n        }\n        List<List<String>> res = new ArrayList<>();\n        backtrack(0, s, dp, new ArrayList<>(), res);\n        return res;\n    }\n    private void backtrack(int start, String s, boolean[][] dp, List<String> path, List<List<String>> res) {\n        if (start == s.length()) {\n            res.add(new ArrayList<>(path));\n            return;\n        }\n        for (int end = start; end < s.length(); end++) {\n            if (dp[start][end]) {\n                path.add(s.substring(start, end + 1));\n                backtrack(end + 1, s, dp, path, res);\n                path.remove(path.size() - 1);\n            }\n        }\n    }\n}",
                "python": "class Solution:\n    def partition(self, s: str) -> list[list[str]]:\n        n = len(s)\n        dp = [[False] * n for _ in range(n)]\n        for length in range(1, n + 1):\n            for i in range(n - length + 1):\n                j = i + length - 1\n                if s[i] == s[j]:\n                    dp[i][j] = (length <= 2) or dp[i + 1][j - 1]\n        res = []\n        path = []\n        def backtrack(start: int):\n            if start == n:\n                res.append(list(path))\n                return\n            for end in range(start, n):\n                if dp[start][end]:\n                    path.append(s[start:end+1])\n                    backtrack(end + 1)\n                    path.pop()\n        backtrack(0)\n        return res"
            }
        }
    },
    {
        "seq": 114,
        "whyNext": "Constrained string partition: partition into exactly 4 segments with value between 0 and 255 without leading zeros.",
        "brute": {
            "idea": "Try all 3-way split points (i, j, k) across the string length and validate all 4 parts.",
            "steps": [
                "Iterate over 3 split positions i, j, k in the string.",
                "Extract 4 segments: s[0..i], s[i..j], s[j..k], s[k..n].",
                "Validate each segment for valid integer in [0, 255] and no leading zeros."
            ],
            "time": "O(n^3)",
            "space": "O(1)",
            "whySlow": "Checks invalid segment splits that could be pruned immediately.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<String> restoreIpAddresses(String s) {\n        List<String> res = new ArrayList<>();\n        int n = s.length();\n        for (int i = 1; i < 4 && i < n; i++) {\n            for (int j = i + 1; j < i + 4 && j < n; j++) {\n                for (int k = j + 1; k < j + 4 && k < n; k++) {\n                    String s1 = s.substring(0, i), s2 = s.substring(i, j);\n                    String s3 = s.substring(j, k), s4 = s.substring(k);\n                    if (isValid(s1) && isValid(s2) && isValid(s3) && isValid(s4)) {\n                        res.add(s1 + \".\" + s2 + \".\" + s3 + \".\" + s4);\n                    }\n                }\n            }\n        }\n        return res;\n    }\n    private boolean isValid(String seg) {\n        if (seg.isEmpty() || seg.length() > 3) return false;\n        if (seg.charAt(0) == '0' && seg.length() > 1) return false;\n        int val = Integer.parseInt(seg);\n        return val >= 0 && val <= 255;\n    }\n}",
                "python": "class Solution:\n    def restoreIpAddresses(self, s: str) -> list[str]:\n        n = len(s)\n        res = []\n        def valid(seg: str) -> bool:\n            if not seg or len(seg) > 3: return False\n            if seg[0] == '0' and len(seg) > 1: return False\n            return 0 <= int(seg) <= 255\n        for i in range(1, min(4, n)):\n            for j in range(i + 1, min(i + 4, n)):\n                for k in range(j + 1, min(j + 4, n)):\n                    s1, s2, s3, s4 = s[:i], s[i:j], s[j:k], s[k:]\n                    if valid(s1) and valid(s2) and valid(s3) and valid(s4):\n                        res.append(f\"{s1}.{s2}.{s3}.{s4}\")\n        return res"
            }
        },
        "optimal": {
            "idea": "Backtracking with length pruning: if remaining characters cannot fit into remaining segments, prune branch immediately.",
            "steps": [
                "Define backtrack(start, dots, currentPath).",
                "If dots == 4 and start == s.length(), record valid IP.",
                "If (4 - dots) * 3 < s.length() - start or (4 - dots) > s.length() - start, prune.",
                "Try segment lengths 1 to 3: check leading zero and value <= 255, then recurse."
            ],
            "time": "O(1) (fixed max 3^4 = 81 leaves)",
            "space": "O(1)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<String> restoreIpAddresses(String s) {\n        List<String> res = new ArrayList<>();\n        if (s.length() < 4 || s.length() > 12) return res;\n        backtrack(s, 0, 0, new ArrayList<>(), res);\n        return res;\n    }\n    private void backtrack(String s, int start, int segCount, List<String> path, List<String> res) {\n        if (segCount == 4) {\n            if (start == s.length()) res.add(String.join(\".\", path));\n            return;\n        }\n        int remainingChars = s.length() - start;\n        int remainingSegs = 4 - segCount;\n        if (remainingChars < remainingSegs || remainingChars > remainingSegs * 3) return;\n        for (int len = 1; len <= 3 && start + len <= s.length(); len++) {\n            String seg = s.substring(start, start + len);\n            if (seg.charAt(0) == '0' && len > 1) break;\n            if (Integer.parseInt(seg) > 255) break;\n            path.add(seg);\n            backtrack(s, start + len, segCount + 1, path, res);\n            path.remove(path.size() - 1);\n        }\n    }\n}",
                "python": "class Solution:\n    def restoreIpAddresses(self, s: str) -> list[str]:\n        res = []\n        if not (4 <= len(s) <= 12):\n            return res\n        path = []\n        def backtrack(start: int, seg_count: int):\n            if seg_count == 4:\n                if start == len(s):\n                    res.append(\".\".join(path))\n                return\n            rem_chars = len(s) - start\n            rem_segs = 4 - seg_count\n            if not (rem_segs <= rem_chars <= rem_segs * 3):\n                return\n            for length in range(1, min(4, rem_chars + 1)):\n                seg = s[start:start+length]\n                if seg[0] == '0' and length > 1:\n                    break\n                if int(seg) > 255:\n                    break\n                path.append(seg)\n                backtrack(start + length, seg_count + 1)\n                path.pop()\n        backtrack(0, 0)\n        return res"
            }
        }
    },
    {
        "seq": 115,
        "whyNext": "2D grid backtracking (DFS): explores 4-directional paths with cell marking and unmarking.",
        "brute": {
            "idea": "From every cell, launch DFS exploring all 4 directions keeping a 2D visited array.",
            "steps": [
                "Iterate over every cell (r, c) as starting point.",
                "Run DFS checking matching characters using a visited boolean[][] array."
            ],
            "time": "O(m * n * 4^L)",
            "space": "O(m * n + L)",
            "whySlow": "Allocating or copying visited sets/arrays causes performance drop; in-place grid mutation avoids extra space.",
            "code": {
                "java": "class Solution {\n    public boolean exist(char[][] board, String word) {\n        int m = board.length, n = board[0].length;\n        boolean[][] visited = new boolean[m][n];\n        for (int i = 0; i < m; i++) {\n            for (int j = 0; j < n; j++) {\n                if (dfs(board, word, 0, i, j, visited)) return true;\n            }\n        }\n        return false;\n    }\n    private boolean dfs(char[][] b, String w, int idx, int r, int c, boolean[][] visited) {\n        if (idx == w.length()) return true;\n        if (r < 0 || r >= b.length || c < 0 || c >= b[0].length || visited[r][c] || b[r][c] != w.charAt(idx)) {\n            return false;\n        }\n        visited[r][c] = true;\n        boolean found = dfs(b, w, idx + 1, r + 1, c, visited) ||\n                        dfs(b, w, idx + 1, r - 1, c, visited) ||\n                        dfs(b, w, idx + 1, r, c + 1, visited) ||\n                        dfs(b, w, idx + 1, r, c - 1, visited);\n        visited[r][c] = false;\n        return found;\n    }\n}",
                "python": "class Solution:\n    def exist(self, board: list[list[str]], word: str) -> bool:\n        m, n = len(board), len(board[0])\n        visited = [[False] * n for _ in range(m)]\n        def dfs(r: int, c: int, idx: int) -> bool:\n            if idx == len(word):\n                return True\n            if not (0 <= r < m and 0 <= c < n) or visited[r][c] or board[r][c] != word[idx]:\n                return False\n            visited[r][c] = True\n            found = (dfs(r + 1, c, idx + 1) or\n                     dfs(r - 1, c, idx + 1) or\n                     dfs(r, c + 1, idx + 1) or\n                     dfs(r, c - 1, idx + 1))\n            visited[r][c] = False\n            return found\n        for i in range(m):\n            for j in range(n):\n                if dfs(i, j, 0):\n                    return True\n        return False"
            }
        },
        "optimal": {
            "idea": "In-place grid backtracking: temporarily replace board[r][c] with '#' while recursing to avoid extra space, then restore.",
            "steps": [
                "If word length exceeds m * n, return false.",
                "Check starting letter matches word.charAt(0).",
                "Save temp = board[r][c], mark board[r][c] = '#'.",
                "Explore 4 orthogonal directions; restore board[r][c] = temp before returning."
            ],
            "time": "O(m * n * 3^L)",
            "space": "O(L)",
            "code": {
                "java": "class Solution {\n    public boolean exist(char[][] board, String word) {\n        int m = board.length, n = board[0].length;\n        if (word.length() > m * n) return false;\n        for (int i = 0; i < m; i++) {\n            for (int j = 0; j < n; j++) {\n                if (board[i][j] == word.charAt(0) && dfs(board, word, 0, i, j)) {\n                    return true;\n                }\n            }\n        }\n        return false;\n    }\n    private boolean dfs(char[][] board, String word, int idx, int r, int c) {\n        if (idx == word.length()) return true;\n        if (r < 0 || r >= board.length || c < 0 || c >= board[0].length || board[r][c] != word.charAt(idx)) {\n            return false;\n        }\n        char temp = board[r][c];\n        board[r][c] = '#';\n        boolean found = dfs(board, word, idx + 1, r + 1, c) ||\n                        dfs(board, word, idx + 1, r - 1, c) ||\n                        dfs(board, word, idx + 1, r, c + 1) ||\n                        dfs(board, word, idx + 1, r, c - 1);\n        board[r][c] = temp;\n        return found;\n    }\n}",
                "python": "class Solution:\n    def exist(self, board: list[list[str]], word: str) -> bool:\n        m, n = len(board), len(board[0])\n        if len(word) > m * n:\n            return False\n        def dfs(r: int, c: int, idx: int) -> bool:\n            if idx == len(word):\n                return True\n            if not (0 <= r < m and 0 <= c < n) or board[r][c] != word[idx]:\n                return False\n            temp = board[r][c]\n            board[r][c] = '#'\n            found = (dfs(r + 1, c, idx + 1) or\n                     dfs(r - 1, c, idx + 1) or\n                     dfs(r, c + 1, idx + 1) or\n                     dfs(r, c - 1, idx + 1))\n            board[r][c] = temp\n            return found\n        for i in range(m):\n            for j in range(n):\n                if board[i][j] == word[0] and dfs(i, j, 0):\n                    return True\n        return False"
            }
        }
    },
    {
        "seq": 116,
        "whyNext": "Classic constraint satisfaction: column, diagonal (r - c), and anti-diagonal (r + c) tracking with bitsets/boolean arrays.",
        "brute": {
            "idea": "Place n queens anywhere on the board (C(n^2, n) placements) and test if any two attack each other.",
            "steps": [
                "Generate all combinations of n squares on n x n board.",
                "Verify whether any two queens share row, column, or diagonal."
            ],
            "time": "O(C(n^2, n))",
            "space": "O(n^2)",
            "whySlow": "Generates astronomically many configurations without row-by-row pruning.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<List<String>> solveNQueens(int n) {\n        List<List<String>> res = new ArrayList<>();\n        int[] queens = new int[n];\n        placeQueens(0, n, queens, res);\n        return res;\n    }\n    private void placeQueens(int row, int n, int[] queens, List<List<String>> res) {\n        if (row == n) {\n            res.add(format(queens, n));\n            return;\n        }\n        for (int col = 0; col < n; col++) {\n            if (isValid(row, col, queens)) {\n                queens[row] = col;\n                placeQueens(row + 1, n, queens, res);\n            }\n        }\n    }\n    private boolean isValid(int row, int col, int[] queens) {\n        for (int r = 0; r < row; r++) {\n            int c = queens[r];\n            if (c == col || Math.abs(r - row) == Math.abs(c - col)) return false;\n        }\n        return true;\n    }\n    private List<String> format(int[] queens, int n) {\n        List<String> board = new ArrayList<>();\n        for (int r = 0; r < n; r++) {\n            char[] row = new char[n];\n            Arrays.fill(row, '.');\n            row[queens[r]] = 'Q';\n            board.add(new String(row));\n        }\n        return board;\n    }\n}",
                "python": "class Solution:\n    def solveNQueens(self, n: int) -> list[list[str]]:\n        res = []\n        queens = [-1] * n\n        def is_valid(row: int, col: int) -> bool:\n            for r in range(row):\n                c = queens[r]\n                if c == col or abs(r - row) == abs(c - col):\n                    return False\n            return True\n        def place(row: int):\n            if row == n:\n                board = []\n                for r in range(n):\n                    line = ['.'] * n\n                    line[queens[r]] = 'Q'\n                    board.append(\"\".join(line))\n                res.append(board)\n                return\n            for col in range(n):\n                if is_valid(row, col):\n                    queens[row] = col\n                    place(row + 1)\n        place(0)\n        return res"
            }
        },
        "optimal": {
            "idea": "Backtracking row by row with boolean sets or bitmasks for cols, diag1 (r + c), and diag2 (r - c + n - 1) in O(1) checks.",
            "steps": [
                "Track cols[n], diag1[2n], diag2[2n].",
                "At row r, loop col c from 0 to n - 1: if cols[c] or diag1[r + c] or diag2[r - c + n - 1] is occupied, skip.",
                "Mark arrays true, place queen, backtrack(r + 1), unmark arrays false."
            ],
            "time": "O(n!)",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<List<String>> solveNQueens(int n) {\n        List<List<String>> res = new ArrayList<>();\n        char[][] board = new char[n][n];\n        for (char[] row : board) Arrays.fill(row, '.');\n        boolean[] cols = new boolean[n];\n        boolean[] diag1 = new boolean[2 * n];\n        boolean[] diag2 = new boolean[2 * n];\n        backtrack(0, n, board, cols, diag1, diag2, res);\n        return res;\n    }\n    private void backtrack(int r, int n, char[][] board, boolean[] cols, boolean[] d1, boolean[] d2, List<List<String>> res) {\n        if (r == n) {\n            List<String> list = new ArrayList<>();\n            for (char[] row : board) list.add(new String(row));\n            res.add(list);\n            return;\n        }\n        for (int c = 0; c < n; c++) {\n            int id1 = r + c;\n            int id2 = r - c + n;\n            if (cols[c] || d1[id1] || d2[id2]) continue;\n            board[r][c] = 'Q';\n            cols[c] = d1[id1] = d2[id2] = true;\n            backtrack(r + 1, n, board, cols, d1, d2, res);\n            cols[c] = d1[id1] = d2[id2] = false;\n            board[r][c] = '.';\n        }\n    }\n}",
                "python": "class Solution:\n    def solveNQueens(self, n: int) -> list[list[str]]:\n        res = []\n        board = [[\".\"] * n for _ in range(n)]\n        cols = [False] * n\n        diag1 = [False] * (2 * n)\n        diag2 = [False] * (2 * n)\n        def backtrack(r: int):\n            if r == n:\n                res.append([\"\".join(row) for row in board])\n                return\n            for c in range(n):\n                if cols[c] or diag1[r + c] or diag2[r - c + n]:\n                    continue\n                board[r][c] = 'Q'\n                cols[c] = diag1[r + c] = diag2[r - c + n] = True\n                backtrack(r + 1)\n                cols[c] = diag1[r + c] = diag2[r - c + n] = False\n                board[r][c] = '.'\n        backtrack(0)\n        return res"
            }
        }
    },
    {
        "seq": 117,
        "whyNext": "Builds on N-Queens: instead of constructing board strings, simply count distinct valid configurations using bitwise operations.",
        "brute": {
            "idea": "Run N-Queens backtracking with array tracking and count valid terminal leaves.",
            "steps": [
                "Recursively place queens row by row.",
                "Increment counter when reaching row == n."
            ],
            "time": "O(n!)",
            "space": "O(n)",
            "whySlow": "Uses array lookups instead of ultra-fast bitwise masks.",
            "code": {
                "java": "class Solution {\n    private int count = 0;\n    public int totalNQueens(int n) {\n        boolean[] cols = new boolean[n];\n        boolean[] d1 = new boolean[2 * n];\n        boolean[] d2 = new boolean[2 * n];\n        dfs(0, n, cols, d1, d2);\n        return count;\n    }\n    private void dfs(int r, int n, boolean[] cols, boolean[] d1, boolean[] d2) {\n        if (r == n) {\n            count++;\n            return;\n        }\n        for (int c = 0; c < n; c++) {\n            if (cols[c] || d1[r + c] || d2[r - c + n]) continue;\n            cols[c] = d1[r + c] = d2[r - c + n] = true;\n            dfs(r + 1, n, cols, d1, d2);\n            cols[c] = d1[r + c] = d2[r - c + n] = false;\n        }\n    }\n}",
                "python": "class Solution:\n    def totalNQueens(self, n: int) -> int:\n        count = 0\n        cols = [False] * n\n        d1 = [False] * (2 * n)\n        d2 = [False] * (2 * n)\n        def dfs(r: int):\n            nonlocal count\n            if r == n:\n                count += 1\n                return\n            for c in range(n):\n                if cols[c] or d1[r + c] or d2[r - c + n]:\n                    continue\n                cols[c] = d1[r + c] = d2[r - c + n] = True\n                dfs(r + 1)\n                cols[c] = d1[r + c] = d2[r - c + n] = False\n        dfs(0)\n        return count"
            }
        },
        "optimal": {
            "idea": "Bitmask backtracking: cols, d1, d2 represented by integer bitmasks. Available positions = ~(cols | d1 | d2) & ((1 << n) - 1).",
            "steps": [
                "Compute available positions bitmask.",
                "Extract lowest set bit p = bits & (-bits).",
                "Recurse with updated masks: cols | p, (d1 | p) << 1, (d2 | p) >> 1.",
                "Turn off bit: bits &= (bits - 1)."
            ],
            "time": "O(n!)",
            "space": "O(n)",
            "code": {
                "java": "class Solution {\n    private int count = 0;\n    public int totalNQueens(int n) {\n        backtrack(0, 0, 0, 0, n);\n        return count;\n    }\n    private void backtrack(int row, int cols, int d1, int d2, int n) {\n        if (row == n) {\n            count++;\n            return;\n        }\n        int available = ((1 << n) - 1) & ~(cols | d1 | d2);\n        while (available != 0) {\n            int p = available & (-available);\n            available &= available - 1;\n            backtrack(row + 1, cols | p, (d1 | p) << 1, (d2 | p) >> 1, n);\n        }\n    }\n}",
                "python": "class Solution:\n    def totalNQueens(self, n: int) -> int:\n        count = 0\n        def backtrack(row: int, cols: int, d1: int, d2: int):\n            nonlocal count\n            if row == n:\n                count += 1\n                return\n            available = ((1 << n) - 1) & ~(cols | d1 | d2)\n            while available:\n                p = available & (-available)\n                available &= available - 1\n                backtrack(row + 1, cols | p, (d1 | p) << 1, (d2 | p) >> 1)\n        backtrack(0, 0, 0, 0)\n        return count"
            }
        }
    },
    {
        "seq": 118,
        "whyNext": "Advanced constraint satisfaction: row, column, and 3x3 box validity checks on 9x9 board.",
        "brute": {
            "idea": "Try every digit 1-9 for every empty cell without caching constraints.",
            "steps": [
                "Find next empty cell ('.').",
                "Try digits '1' through '9'.",
                "Check entire row, col, and 3x3 box for conflicts on each attempt.",
                "Recurse; backtrack if no digit fits."
            ],
            "time": "O(9^(m))",
            "space": "O(81)",
            "whySlow": "Scans row, col, and box on every digit check in O(9) instead of bitmask/array in O(1).",
            "code": {
                "java": "class Solution {\n    public void solveSudoku(char[][] board) {\n        solve(board);\n    }\n    private boolean solve(char[][] board) {\n        for (int r = 0; r < 9; r++) {\n            for (int c = 0; c < 9; c++) {\n                if (board[r][c] == '.') {\n                    for (char d = '1'; d <= '9'; d++) {\n                        if (isValid(board, r, c, d)) {\n                            board[r][c] = d;\n                            if (solve(board)) return true;\n                            board[r][c] = '.';\n                        }\n                    }\n                    return false;\n                }\n            }\n        }\n        return true;\n    }\n    private boolean isValid(char[][] board, int r, int c, char d) {\n        for (int i = 0; i < 9; i++) {\n            if (board[r][i] == d || board[i][c] == d) return false;\n            int boxR = 3 * (r / 3) + i / 3;\n            int boxC = 3 * (c / 3) + i % 3;\n            if (board[boxR][boxC] == d) return false;\n        }\n        return true;\n    }\n}",
                "python": "class Solution:\n    def solveSudoku(self, board: list[list[str]]) -> None:\n        def is_valid(r: int, c: int, d: str) -> bool:\n            for i in range(9):\n                if board[r][i] == d or board[i][c] == d:\n                    return False\n                if board[3 * (r // 3) + i // 3][3 * (c // 3) + i % 3] == d:\n                    return False\n            return True\n        def solve() -> bool:\n            for r in range(9):\n                for c in range(9):\n                    if board[r][c] == '.':\n                        for d in \"123456789\":\n                            if is_valid(r, c, d):\n                                board[r][c] = d\n                                if solve(): return True\n                                board[r][c] = '.'\n                        return False\n            return True\n        solve()"
            }
        },
        "optimal": {
            "idea": "Precompute row, col, and box bitmasks for O(1) candidate evaluation and pre-collect empty cells to avoid nested grid scans.",
            "steps": [
                "Track rows[9], cols[9], boxes[9] bitmasks.",
                "Collect all empty cell coordinates in a list empties.",
                "Define backtrack(idx): if idx == empties.size(), board is solved.",
                "Candidate mask = ~(rows[r] | cols[c] | boxes[boxId]) & 0x1FF.",
                "Iterate over candidate digits, update bitmasks and recurse."
            ],
            "time": "O(9^(m)) pruned with bitwise constraints",
            "space": "O(81)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    private int[] rows = new int[9];\n    private int[] cols = new int[9];\n    private int[] boxes = new int[9];\n    private List<int[]> empties = new ArrayList<>();\n    public void solveSudoku(char[][] board) {\n        for (int r = 0; r < 9; r++) {\n            for (int c = 0; c < 9; c++) {\n                if (board[r][c] == '.') {\n                    empties.add(new int[]{r, c});\n                } else {\n                    int d = board[r][c] - '1';\n                    int mask = 1 << d;\n                    rows[r] |= mask;\n                    cols[c] |= mask;\n                    boxes[(r / 3) * 3 + c / 3] |= mask;\n                }\n            }\n        }\n        backtrack(board, 0);\n    }\n    private boolean backtrack(char[][] board, int idx) {\n        if (idx == empties.size()) return true;\n        int r = empties.get(idx)[0], c = empties.get(idx)[1];\n        int b = (r / 3) * 3 + c / 3;\n        int available = ~(rows[r] | cols[c] | boxes[b]) & 0x1FF;\n        while (available != 0) {\n            int p = available & (-available);\n            int d = Integer.numberOfTrailingZeros(p);\n            available &= available - 1;\n            board[r][c] = (char) ('1' + d);\n            rows[r] |= p; cols[c] |= p; boxes[b] |= p;\n            if (backtrack(board, idx + 1)) return true;\n            rows[r] &= ~p; cols[c] &= ~p; boxes[b] &= ~p;\n            board[r][c] = '.';\n        }\n        return false;\n    }\n}",
                "python": "class Solution:\n    def solveSudoku(self, board: list[list[str]]) -> None:\n        rows = [0] * 9\n        cols = [0] * 9\n        boxes = [0] * 9\n        empties = []\n        for r in range(9):\n            for c in range(9):\n                if board[r][c] == '.':\n                    empties.append((r, c))\n                else:\n                    d = int(board[r][c]) - 1\n                    mask = 1 << d\n                    rows[r] |= mask\n                    cols[c] |= mask\n                    boxes[(r // 3) * 3 + c // 3] |= mask\n        def backtrack(idx: int) -> bool:\n            if idx == len(empties):\n                return True\n            r, c = empties[idx]\n            b = (r // 3) * 3 + c // 3\n            available = ~(rows[r] | cols[c] | boxes[b]) & 0x1FF\n            while available:\n                p = available & (-available)\n                d = (p).bit_length() - 1\n                available &= available - 1\n                board[r][c] = str(d + 1)\n                rows[r] |= p\n                cols[c] |= p\n                boxes[b] |= p\n                if backtrack(idx + 1):\n                    return True\n                rows[r] &= ~p\n                cols[c] &= ~p\n                boxes[b] &= ~p\n                board[r][c] = '.'\n            return False\n        backtrack(0)"
            }
        }
    },
    {
        "seq": 119,
        "whyNext": "Transitions from backtracking to memoized recursion / subset sum DP: assign + or - to each number.",
        "brute": {
            "idea": "Explore all 2^n combinations of signs recursively.",
            "steps": [
                "At index i, recursively evaluate curSum + nums[i] and curSum - nums[i].",
                "When i == n, if curSum == target return 1 else 0."
            ],
            "time": "O(2^n)",
            "space": "O(n)",
            "whySlow": "Examines all 2^n paths with many duplicate intermediate (index, sum) subproblems.",
            "code": {
                "java": "class Solution {\n    public int findTargetSumWays(int[] nums, int target) {\n        return dfs(nums, 0, 0, target);\n    }\n    private int dfs(int[] nums, int idx, int curSum, int target) {\n        if (idx == nums.length) {\n            return curSum == target ? 1 : 0;\n        }\n        return dfs(nums, idx + 1, curSum + nums[idx], target) +\n               dfs(nums, idx + 1, curSum - nums[idx], target);\n    }\n}",
                "python": "class Solution:\n    def findTargetSumWays(self, nums: list[int], target: int) -> int:\n        def dfs(idx: int, cur_sum: int) -> int:\n            if idx == len(nums):\n                return 1 if cur_sum == target else 0\n            return dfs(idx + 1, cur_sum + nums[idx]) + dfs(idx + 1, cur_sum - nums[idx])\n        return dfs(0, 0)"
            }
        },
        "optimal": {
            "idea": "Transform into 0/1 knapsack: P - N = target and P + N = sum => 2P = target + sum => P = (target + sum) / 2.",
            "steps": [
                "Sum all elements totalSum. If totalSum < abs(target) or (totalSum + target) % 2 != 0, return 0.",
                "Let subsetTarget = (totalSum + target) / 2.",
                "Use 1D dp array dp[subsetTarget + 1] initialized with dp[0] = 1.",
                "For each num in nums, update backwards: dp[s] += dp[s - num].",
                "Return dp[subsetTarget]."
            ],
            "time": "O(n * target)",
            "space": "O(target)",
            "code": {
                "java": "class Solution {\n    public int findTargetSumWays(int[] nums, int target) {\n        int sum = 0;\n        for (int x : nums) sum += x;\n        if (sum < Math.abs(target) || (sum + target) % 2 != 0) return 0;\n        int s = (sum + target) / 2;\n        int[] dp = new int[s + 1];\n        dp[0] = 1;\n        for (int num : nums) {\n            for (int j = s; j >= num; j--) {\n                dp[j] += dp[j - num];\n            }\n        }\n        return dp[s];\n    }\n}",
                "python": "class Solution:\n    def findTargetSumWays(self, nums: list[int], target: int) -> int:\n        total = sum(nums)\n        if total < abs(target) or (total + target) % 2 != 0:\n            return 0\n        s = (total + target) // 2\n        dp = [0] * (s + 1)\n        dp[0] = 1\n        for num in nums:\n            for j in range(s, num - 1, -1):\n                dp[j] += dp[j - num]\n        return dp[s]"
            }
        }
    },
    {
        "seq": 120,
        "whyNext": "NP-complete bin packing / backtracking: partition into k buckets each with target sum = total / k.",
        "brute": {
            "idea": "Try putting each number into each of the k buckets.",
            "steps": [
                "Calculate total sum. If sum % k != 0 return false.",
                "Maintain bucket sums array of length k.",
                "Try placing nums[i] into each bucket recursively."
            ],
            "time": "O(k^n)",
            "space": "O(k + n)",
            "whySlow": "Tries all k assignments per element leading to O(k^n) combinations without pruning symmetry.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public boolean canPartitionKSubsets(int[] nums, int k) {\n        int sum = 0;\n        for (int x : nums) sum += x;\n        if (sum % k != 0) return false;\n        int target = sum / k;\n        int[] buckets = new int[k];\n        return dfs(nums, 0, buckets, target);\n    }\n    private boolean dfs(int[] nums, int idx, int[] buckets, int target) {\n        if (idx == nums.length) return true;\n        for (int i = 0; i < buckets.length; i++) {\n            if (buckets[i] + nums[idx] <= target) {\n                buckets[i] += nums[idx];\n                if (dfs(nums, idx + 1, buckets, target)) return true;\n                buckets[i] -= nums[idx];\n            }\n            if (buckets[i] == 0) break;\n        }\n        return false;\n    }\n}",
                "python": "class Solution:\n    def canPartitionKSubsets(self, nums: list[int], k: int) -> bool:\n        total = sum(nums)\n        if total % k != 0: return False\n        target = total // k\n        buckets = [0] * k\n        def dfs(idx: int) -> bool:\n            if idx == len(nums):\n                return True\n            for i in range(k):\n                if buckets[i] + nums[idx] <= target:\n                    buckets[i] += nums[idx]\n                    if dfs(idx + 1): return True\n                    buckets[i] -= nums[idx]\n                if buckets[i] == 0:\n                    break\n            return False\n        return dfs(0)"
            }
        },
        "optimal": {
            "idea": "Sort nums descending. Fill buckets one by one: when a bucket reaches target, recurse on next bucket; prune duplicate values.",
            "steps": [
                "Sort nums in descending order; if nums[0] > target, return false.",
                "Use a boolean used[] array to track selected numbers.",
                "In backtrack(k, bucketSum, startIdx): if k == 0 return true.",
                "If bucketSum == target, recurse backtrack(k - 1, 0, 0).",
                "Loop i from startIdx to n - 1: if used[i] or bucketSum + nums[i] > target continue.",
                "Mark used, recurse; if bucketSum == 0, break immediately (empty bucket symmetry)."
            ],
            "time": "O(k * 2^n)",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public boolean canPartitionKSubsets(int[] nums, int k) {\n        int sum = 0;\n        for (int x : nums) sum += x;\n        if (sum % k != 0) return false;\n        int target = sum / k;\n        Arrays.sort(nums);\n        int n = nums.length;\n        if (nums[n - 1] > target) return false;\n        boolean[] used = new boolean[n];\n        return backtrack(nums, used, k, 0, target, n - 1);\n    }\n    private boolean backtrack(int[] nums, boolean[] used, int k, int currentSum, int target, int start) {\n        if (k == 1) return true;\n        if (currentSum == target) {\n            return backtrack(nums, used, k - 1, 0, target, nums.length - 1);\n        }\n        for (int i = start; i >= 0; i--) {\n            if (used[i] || currentSum + nums[i] > target) continue;\n            used[i] = true;\n            if (backtrack(nums, used, k, currentSum + nums[i], target, i - 1)) return true;\n            used[i] = false;\n            if (currentSum == 0 || currentSum + nums[i] == target) break;\n        }\n        return false;\n    }\n}",
                "python": "class Solution:\n    def canPartitionKSubsets(self, nums: list[int], k: int) -> bool:\n        total = sum(nums)\n        if total % k != 0: return False\n        target = total // k\n        nums.sort(reverse=True)\n        if nums[0] > target: return False\n        n = len(nums)\n        used = [False] * n\n        def backtrack(k_rem: int, cur_sum: int, start: int) -> bool:\n            if k_rem == 1:\n                return True\n            if cur_sum == target:\n                return backtrack(k_rem - 1, 0, 0)\n            for i in range(start, n):\n                if used[i] or cur_sum + nums[i] > target:\n                    continue\n                used[i] = True\n                if backtrack(k_rem, cur_sum + nums[i], i + 1):\n                    return True\n                used[i] = False\n                if cur_sum == 0 or cur_sum + nums[i] == target:\n                    break\n            return False\n        return backtrack(k, 0, 0)"
            }
        }
    },
    {
        "seq": 121,
        "whyNext": "Entry to Chapter 8 (Binary Trees): DFS recursion on tree nodes computes 1 + max(left, right).",
        "brute": {
            "idea": "Perform level-order traversal (BFS) with a queue and count the number of levels.",
            "steps": [
                "If root is null, return 0.",
                "Initialize queue with root.",
                "While queue is not empty, pop all nodes in current level and push their children.",
                "Increment depth count at each level."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "whySlow": "BFS queue requires storing an entire tree level (up to n/2 nodes in memory).",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int maxDepth(TreeNode root) {\n        if (root == null) return 0;\n        Queue<TreeNode> q = new LinkedList<>();\n        q.offer(root);\n        int depth = 0;\n        while (!q.isEmpty()) {\n            int size = q.size();\n            for (int i = 0; i < size; i++) {\n                TreeNode node = q.poll();\n                if (node.left != null) q.offer(node.left);\n                if (node.right != null) q.offer(node.right);\n            }\n            depth++;\n        }\n        return depth;\n    }\n}",
                "python": "from collections import deque\n\nclass Solution:\n    def maxDepth(self, root: TreeNode | None) -> int:\n        if not root:\n            return 0\n        q = deque([root])\n        depth = 0\n        while q:\n            for _ in range(len(q)):\n                node = q.popleft()\n                if node.left: q.append(node.left)\n                if node.right: q.append(node.right)\n            depth += 1\n        return depth"
            }
        },
        "optimal": {
            "idea": "Recursive post-order DFS: depth of null node is 0; depth of node is 1 + max(depth(left), depth(right)).",
            "steps": [
                "If root == null, return 0.",
                "Return 1 + Math.max(maxDepth(root.left), maxDepth(root.right))."
            ],
            "time": "O(n)",
            "space": "O(h) where h is tree height",
            "code": {
                "java": "class Solution {\n    public int maxDepth(TreeNode root) {\n        if (root == null) return 0;\n        return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));\n    }\n}",
                "python": "class Solution:\n    def maxDepth(self, root: TreeNode | None) -> int:\n        if not root:\n            return 0\n        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))"
            }
        }
    },
    {
        "seq": 122,
        "whyNext": "Builds on Maximum Depth: min depth requires terminating only at LEAF nodes (both left and right null).",
        "brute": {
            "idea": "Full DFS traversal to find all leaf depths and take the minimum.",
            "steps": [
                "Traverse every node in the tree.",
                "When a leaf is reached, update minDepth."
            ],
            "time": "O(n)",
            "space": "O(h)",
            "whySlow": "Visits all nodes in the tree even when a leaf is found early near the root.",
            "code": {
                "java": "class Solution {\n    public int minDepth(TreeNode root) {\n        if (root == null) return 0;\n        if (root.left == null) return 1 + minDepth(root.right);\n        if (root.right == null) return 1 + minDepth(root.left);\n        return 1 + Math.min(minDepth(root.left), minDepth(root.right));\n    }\n}",
                "python": "class Solution:\n    def minDepth(self, root: TreeNode | None) -> int:\n        if not root:\n            return 0\n        if not root.left:\n            return 1 + self.minDepth(root.right)\n        if not root.right:\n            return 1 + self.minDepth(root.left)\n        return 1 + min(self.minDepth(root.left), self.minDepth(root.right))"
            }
        },
        "optimal": {
            "idea": "BFS level order: return immediately upon encountering the first leaf node.",
            "steps": [
                "If root == null, return 0.",
                "Enqueue root with depth 1.",
                "For each node, if both left and right are null, return current depth.",
                "Enqueue children and increment depth."
            ],
            "time": "O(n) worst case, O(min leaf depth) best case",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int minDepth(TreeNode root) {\n        if (root == null) return 0;\n        Queue<TreeNode> q = new LinkedList<>();\n        q.offer(root);\n        int depth = 1;\n        while (!q.isEmpty()) {\n            int size = q.size();\n            for (int i = 0; i < size; i++) {\n                TreeNode node = q.poll();\n                if (node.left == null && node.right == null) return depth;\n                if (node.left != null) q.offer(node.left);\n                if (node.right != null) q.offer(node.right);\n            }\n            depth++;\n        }\n        return depth;\n    }\n}",
                "python": "from collections import deque\n\nclass Solution:\n    def minDepth(self, root: TreeNode | None) -> int:\n        if not root:\n            return 0\n        q = deque([(root, 1)])\n        while q:\n            node, depth = q.popleft()\n            if not node.left and not node.right:\n                return depth\n            if node.left:\n                q.append((node.left, depth + 1))\n            if node.right:\n                q.append((node.right, depth + 1))\n        return 0"
            }
        }
    },
    {
        "seq": 123,
        "whyNext": "Tree mutation recursion: swap left and right subtrees recursively.",
        "brute": {
            "idea": "Perform iterative level-order traversal, swapping left and right pointers of every node.",
            "steps": [
                "Push root to queue.",
                "While queue is not empty, pop node, swap node.left and node.right, enqueue non-null children.",
                "Return root."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "whySlow": "Iterative queue overhead compared to clean 3-line DFS recursion.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public TreeNode invertTree(TreeNode root) {\n        if (root == null) return null;\n        Queue<TreeNode> q = new LinkedList<>();\n        q.offer(root);\n        while (!q.isEmpty()) {\n            TreeNode node = q.poll();\n            TreeNode temp = node.left;\n            node.left = node.right;\n            node.right = temp;\n            if (node.left != null) q.offer(node.left);\n            if (node.right != null) q.offer(node.right);\n        }\n        return root;\n    }\n}",
                "python": "from collections import deque\n\nclass Solution:\n    def invertTree(self, root: TreeNode | None) -> TreeNode | None:\n        if not root:\n            return None\n        q = deque([root])\n        while q:\n            node = q.popleft()\n            node.left, node.right = node.right, node.left\n            if node.left: q.append(node.left)\n            if node.right: q.append(node.right)\n        return root"
            }
        },
        "optimal": {
            "idea": "Recursive post-order/pre-order: swap node's left and right subtrees after inverting both.",
            "steps": [
                "Base case: if root == null, return null.",
                "Recursively invert root.left and root.right.",
                "Swap root.left and root.right.",
                "Return root."
            ],
            "time": "O(n)",
            "space": "O(h)",
            "code": {
                "java": "class Solution {\n    public TreeNode invertTree(TreeNode root) {\n        if (root == null) return null;\n        TreeNode left = invertTree(root.left);\n        TreeNode right = invertTree(root.right);\n        root.left = right;\n        root.right = left;\n        return root;\n    }\n}",
                "python": "class Solution:\n    def invertTree(self, root: TreeNode | None) -> TreeNode | None:\n        if not root:\n            return None\n        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)\n        return root"
            }
        }
    },
    {
        "seq": 124,
        "whyNext": "Simultaneous dual-tree recursion: both nodes must match in value, left subtrees must match, and right subtrees must match.",
        "brute": {
            "idea": "Serialize both trees into preorder strings with null markers and compare strings.",
            "steps": [
                "Serialize tree p with null delimiters.",
                "Serialize tree q with null delimiters.",
                "Compare the serialized strings."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "whySlow": "Allocates large strings for both trees instead of short-circuiting on first mismatch.",
            "code": {
                "java": "class Solution {\n    public boolean isSameTree(TreeNode p, TreeNode q) {\n        StringBuilder sb1 = new StringBuilder();\n        StringBuilder sb2 = new StringBuilder();\n        serialize(p, sb1);\n        serialize(q, sb2);\n        return sb1.toString().equals(sb2.toString());\n    }\n    private void serialize(TreeNode node, StringBuilder sb) {\n        if (node == null) {\n            sb.append(\"#,\");\n            return;\n        }\n        sb.append(node.val).append(\",\");\n        serialize(node.left, sb);\n        serialize(node.right, sb);\n    }\n}",
                "python": "class Solution:\n    def isSameTree(self, p: TreeNode | None, q: TreeNode | None) -> bool:\n        def serialize(node: TreeNode | None) -> str:\n            if not node:\n                return \"#,\"\n            return f\"{node.val},\" + serialize(node.left) + serialize(node.right)\n        return serialize(p) == serialize(q)"
            }
        },
        "optimal": {
            "idea": "Short-circuit recursive DFS: if both null return true; if one null or vals differ return false; recurse left and right.",
            "steps": [
                "If p == null && q == null, return true.",
                "If p == null || q == null || p.val != q.val, return false.",
                "Return isSameTree(p.left, q.left) && isSameTree(p.right, q.right)."
            ],
            "time": "O(n)",
            "space": "O(h)",
            "code": {
                "java": "class Solution {\n    public boolean isSameTree(TreeNode p, TreeNode q) {\n        if (p == null && q == null) return true;\n        if (p == null || q == null || p.val != q.val) return false;\n        return isSameTree(p.left, q.left) && isSameTree(p.right, q.right);\n    }\n}",
                "python": "class Solution:\n    def isSameTree(self, p: TreeNode | None, q: TreeNode | None) -> bool:\n        if not p and not q:\n            return True\n        if not p or not q or p.val != q.val:\n            return False\n        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)"
            }
        }
    },
    {
        "seq": 125,
        "whyNext": "Builds on Same Tree: mirror symmetry check compares left.left with right.right and left.right with right.left.",
        "brute": {
            "idea": "Clone and invert the left subtree, then check if it is the same tree as the right subtree.",
            "steps": [
                "Invert root.left using invertTree.",
                "Compare inverted root.left with root.right using isSameTree."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "whySlow": "Inverting the tree mutates structure or requires cloning before comparison.",
            "code": {
                "java": "class Solution {\n    public boolean isSymmetric(TreeNode root) {\n        if (root == null) return true;\n        invert(root.left);\n        return isSame(root.left, root.right);\n    }\n    private void invert(TreeNode node) {\n        if (node == null) return;\n        TreeNode temp = node.left;\n        node.left = node.right;\n        node.right = temp;\n        invert(node.left);\n        invert(node.right);\n    }\n    private boolean isSame(TreeNode p, TreeNode q) {\n        if (p == null && q == null) return true;\n        if (p == null || q == null || p.val != q.val) return false;\n        return isSame(p.left, q.left) && isSame(p.right, q.right);\n    }\n}",
                "python": "class Solution:\n    def isSymmetric(self, root: TreeNode | None) -> bool:\n        if not root:\n            return True\n        def invert(node: TreeNode | None):\n            if not node: return\n            node.left, node.right = node.right, node.left\n            invert(node.left)\n            invert(node.right)\n        def is_same(p, q):\n            if not p and not q: return True\n            if not p or not q or p.val != q.val: return False\n            return is_same(p.left, q.left) and is_same(p.right, q.right)\n        invert(root.left)\n        return is_same(root.left, root.right)"
            }
        },
        "optimal": {
            "idea": "Mirror recursive helper isMirror(t1, t2): check t1.val == t2.val and isMirror(t1.left, t2.right) and isMirror(t1.right, t2.left).",
            "steps": [
                "If root == null return true.",
                "Define helper isMirror(t1, t2):",
                "If both null return true; if one null or t1.val != t2.val return false.",
                "Return isMirror(t1.left, t2.right) && isMirror(t1.right, t2.left)."
            ],
            "time": "O(n)",
            "space": "O(h)",
            "code": {
                "java": "class Solution {\n    public boolean isSymmetric(TreeNode root) {\n        if (root == null) return true;\n        return isMirror(root.left, root.right);\n    }\n    private boolean isMirror(TreeNode t1, TreeNode t2) {\n        if (t1 == null && t2 == null) return true;\n        if (t1 == null || t2 == null || t1.val != t2.val) return false;\n        return isMirror(t1.left, t2.right) && isMirror(t1.right, t2.left);\n    }\n}",
                "python": "class Solution:\n    def isSymmetric(self, root: TreeNode | None) -> bool:\n        if not root:\n            return True\n        def is_mirror(t1: TreeNode | None, t2: TreeNode | None) -> bool:\n            if not t1 and not t2:\n                return True\n            if not t1 or not t2 or t1.val != t2.val:\n                return False\n            return is_mirror(t1.left, t2.right) and is_mirror(t1.right, t2.left)\n        return is_mirror(root.left, root.right)"
            }
        }
    }
]

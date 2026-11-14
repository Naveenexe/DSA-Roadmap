# scripts/gen_batch_05.py
import json

batch_5 = [
    # 101: Pow(x, n)
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
                "java": """class Solution {
    public double myPow(double x, int n) {
        long N = n;
        if (N < 0) {
            x = 1 / x;
            N = -N;
        }
        double ans = 1;
        for (long i = 0; i < N; i++) {
            ans = ans * x;
        }
        return ans;
    }
}""",
                "python": """class Solution:
    def myPow(self, x: float, n: int) -> float:
        N = n
        if N < 0:
            x = 1 / x
            N = -N
        ans = 1.0
        for _ in range(N):
            ans *= x
        return ans"""
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
                "java": """class Solution {
    public double myPow(double x, int n) {
        long N = n;
        if (N < 0) {
            x = 1.0 / x;
            N = -N;
        }
        double ans = 1.0;
        double current = x;
        while (N > 0) {
            if ((N & 1) == 1) {
                ans *= current;
            }
            current *= current;
            N >>= 1;
        }
        return ans;
    }
}""",
                "python": """class Solution:
    def myPow(self, x: float, n: int) -> float:
        N = n
        if N < 0:
            x = 1.0 / x
            N = -N
        ans = 1.0
        current = x
        while N > 0:
            if N % 2 == 1:
                ans *= current
            current *= current
            N //= 2
        return ans"""
            }
        }
    },
    # 102: Subsets
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
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        int n = nums.length;
        for (int i = 0; i < (1 << n); i++) {
            List<Integer> sub = new ArrayList<>();
            for (int j = 0; j < n; j++) {
                if ((i & (1 << j)) != 0) {
                    sub.add(nums[j]);
                }
            }
            result.add(sub);
        }
        return result;
    }
}""",
                "python": """class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        n = len(nums)
        res = []
        for i in range(1 << n):
            sub = []
            for j in range(n):
                if (i >> j) & 1:
                    sub.append(nums[j])
            res.append(sub)
        return res"""
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
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> res = new ArrayList<>();
        backtrack(0, nums, new ArrayList<>(), res);
        return res;
    }
    private void backtrack(int start, int[] nums, List<Integer> path, List<List<Integer>> res) {
        res.add(new ArrayList<>(path));
        for (int i = start; i < nums.length; i++) {
            path.add(nums[i]);
            backtrack(i + 1, nums, path, res);
            path.remove(path.size() - 1);
        }
    }
}""",
                "python": """class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        res = []
        path = []
        def backtrack(start: int):
            res.append(list(path))
            for i in range(start, len(nums)):
                path.append(nums[i])
                backtrack(i + 1)
                path.pop()
        backtrack(0)
        return res"""
            }
        }
    },
    # 103: Subsets II
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
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> subsetsWithDup(int[] nums) {
        Arrays.sort(nums);
        Set<List<Integer>> set = new HashSet<>();
        int n = nums.length;
        for (int i = 0; i < (1 << n); i++) {
            List<Integer> sub = new ArrayList<>();
            for (int j = 0; j < n; j++) {
                if ((i & (1 << j)) != 0) sub.add(nums[j]);
            }
            set.add(sub);
        }
        return new ArrayList<>(set);
    }
}""",
                "python": """class Solution:
    def subsetsWithDup(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        res = set()
        n = len(nums)
        for i in range(1 << n):
            sub = []
            for j in range(n):
                if (i >> j) & 1:
                    sub.append(nums[j])
            res.add(tuple(sub))
        return [list(x) for x in res]"""
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
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> subsetsWithDup(int[] nums) {
        Arrays.sort(nums);
        List<List<Integer>> res = new ArrayList<>();
        backtrack(0, nums, new ArrayList<>(), res);
        return res;
    }
    private void backtrack(int start, int[] nums, List<Integer> path, List<List<Integer>> res) {
        res.add(new ArrayList<>(path));
        for (int i = start; i < nums.length; i++) {
            if (i > start && nums[i] == nums[i - 1]) continue;
            path.add(nums[i]);
            backtrack(i + 1, nums, path, res);
            path.remove(path.size() - 1);
        }
    }
}""",
                "python": """class Solution:
    def subsetsWithDup(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        res = []
        path = []
        def backtrack(start: int):
            res.append(list(path))
            for i in range(start, len(nums)):
                if i > start and nums[i] == nums[i - 1]:
                    continue
                path.append(nums[i])
                backtrack(i + 1)
                path.pop()
        backtrack(0)
        return res"""
            }
        }
    },
    # 104: Combination Sum
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
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> combinationSum(int[] candidates, int target) {
        List<List<Integer>> res = new ArrayList<>();
        dfs(0, candidates, target, new ArrayList<>(), res);
        return res;
    }
    private void dfs(int idx, int[] c, int rem, List<Integer> path, List<List<Integer>> res) {
        if (rem == 0) {
            res.add(new ArrayList<>(path));
            return;
        }
        if (idx == c.length || rem < 0) return;
        dfs(idx + 1, c, rem, path, res);
        path.add(c[idx]);
        dfs(idx, c, rem - c[idx], path, res);
        path.remove(path.size() - 1);
    }
}""",
                "python": """class Solution:
    def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]:
        res = []
        def dfs(idx: int, rem: int, path: list[int]):
            if rem == 0:
                res.append(list(path))
                return
            if idx == len(candidates) or rem < 0:
                return
            dfs(idx + 1, rem, path)
            path.append(candidates[idx])
            dfs(idx, rem - candidates[idx], path)
            path.pop()
        dfs(0, target, [])
        return res"""
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
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> combinationSum(int[] candidates, int target) {
        Arrays.sort(candidates);
        List<List<Integer>> res = new ArrayList<>();
        backtrack(0, target, candidates, new ArrayList<>(), res);
        return res;
    }
    private void backtrack(int start, int rem, int[] candidates, List<Integer> path, List<List<Integer>> res) {
        if (rem == 0) {
            res.add(new ArrayList<>(path));
            return;
        }
        for (int i = start; i < candidates.length; i++) {
            if (candidates[i] > rem) break;
            path.add(candidates[i]);
            backtrack(i, rem - candidates[i], candidates, path, res);
            path.remove(path.size() - 1);
        }
    }
}""",
                "python": """class Solution:
    def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]:
        candidates.sort()
        res = []
        path = []
        def backtrack(start: int, rem: int):
            if rem == 0:
                res.append(list(path))
                return
            for i in range(start, len(candidates)):
                if candidates[i] > rem:
                    break
                path.append(candidates[i])
                backtrack(i, rem - candidates[i])
                path.pop()
        backtrack(0, target)
        return res"""
            }
        }
    },
    # 105: Combination Sum II
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
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> combinationSum2(int[] candidates, int target) {
        Arrays.sort(candidates);
        Set<List<Integer>> set = new HashSet<>();
        dfs(0, candidates, target, new ArrayList<>(), set);
        return new ArrayList<>(set);
    }
    private void dfs(int idx, int[] c, int rem, List<Integer> path, Set<List<Integer>> set) {
        if (rem == 0) {
            set.add(new ArrayList<>(path));
            return;
        }
        if (idx == c.length || rem < 0) return;
        dfs(idx + 1, c, rem, path, set);
        path.add(c[idx]);
        dfs(idx + 1, c, rem - c[idx], path, set);
        path.remove(path.size() - 1);
    }
}""",
                "python": """class Solution:
    def combinationSum2(self, candidates: list[int], target: int) -> list[list[int]]:
        candidates.sort()
        res = set()
        def dfs(idx: int, rem: int, path: list[int]):
            if rem == 0:
                res.add(tuple(path))
                return
            if idx == len(candidates) or rem < 0:
                return
            dfs(idx + 1, rem, path)
            path.append(candidates[idx])
            dfs(idx + 1, rem - candidates[idx], path)
            path.pop()
        dfs(0, target, [])
        return [list(x) for x in res]"""
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
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> combinationSum2(int[] candidates, int target) {
        Arrays.sort(candidates);
        List<List<Integer>> res = new ArrayList<>();
        backtrack(0, target, candidates, new ArrayList<>(), res);
        return res;
    }
    private void backtrack(int start, int rem, int[] candidates, List<Integer> path, List<List<Integer>> res) {
        if (rem == 0) {
            res.add(new ArrayList<>(path));
            return;
        }
        for (int i = start; i < candidates.length; i++) {
            if (candidates[i] > rem) break;
            if (i > start && candidates[i] == candidates[i - 1]) continue;
            path.add(candidates[i]);
            backtrack(i + 1, rem - candidates[i], candidates, path, res);
            path.remove(path.size() - 1);
        }
    }
}""",
                "python": """class Solution:
    def combinationSum2(self, candidates: list[int], target: int) -> list[list[int]]:
        candidates.sort()
        res = []
        path = []
        def backtrack(start: int, rem: int):
            if rem == 0:
                res.append(list(path))
                return
            for i in range(start, len(candidates)):
                if candidates[i] > rem:
                    break
                if i > start and candidates[i] == candidates[i - 1]:
                    continue
                path.append(candidates[i])
                backtrack(i + 1, rem - candidates[i])
                path.pop()
        backtrack(0, target)
        return res"""
            }
        }
    },
    # 106: Combination Sum III
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
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> combinationSum3(int k, int n) {
        List<List<Integer>> res = new ArrayList<>();
        for (int mask = 0; mask < (1 << 9); mask++) {
            if (Integer.bitCount(mask) != k) continue;
            int sum = 0;
            List<Integer> list = new ArrayList<>();
            for (int i = 0; i < 9; i++) {
                if ((mask & (1 << i)) != 0) {
                    sum += (i + 1);
                    list.add(i + 1);
                }
            }
            if (sum == n) res.add(list);
        }
        return res;
    }
}""",
                "python": """class Solution:
    def combinationSum3(self, k: int, n: int) -> list[list[int]]:
        res = []
        for mask in range(1 << 9):
            if bin(mask).count('1') != k:
                continue
            sub = [i + 1 for i in range(9) if (mask >> i) & 1]
            if sum(sub) == n:
                res.append(sub)
        return res"""
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
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> combinationSum3(int k, int n) {
        List<List<Integer>> res = new ArrayList<>();
        backtrack(1, n, k, new ArrayList<>(), res);
        return res;
    }
    private void backtrack(int start, int rem, int k, List<Integer> path, List<List<Integer>> res) {
        if (path.size() == k) {
            if (rem == 0) res.add(new ArrayList<>(path));
            return;
        }
        for (int i = start; i <= 9; i++) {
            if (i > rem) break;
            path.add(i);
            backtrack(i + 1, rem - i, k, path, res);
            path.remove(path.size() - 1);
        }
    }
}""",
                "python": """class Solution:
    def combinationSum3(self, k: int, n: int) -> list[list[int]]:
        res = []
        path = []
        def backtrack(start: int, rem: int):
            if len(path) == k:
                if rem == 0:
                    res.append(list(path))
                return
            for i in range(start, 10):
                if i > rem:
                    break
                path.append(i)
                backtrack(i + 1, rem - i)
                path.pop()
        backtrack(1, n)
        return res"""
            }
        }
    },
    # 107: Combinations
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
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> combine(int n, int k) {
        List<List<Integer>> res = new ArrayList<>();
        dfs(1, n, k, new ArrayList<>(), res);
        return res;
    }
    private void dfs(int cur, int n, int k, List<Integer> path, List<List<Integer>> res) {
        if (path.size() == k) {
            res.add(new ArrayList<>(path));
            return;
        }
        if (cur > n) return;
        path.add(cur);
        dfs(cur + 1, n, k, path, res);
        path.remove(path.size() - 1);
        dfs(cur + 1, n, k, path, res);
    }
}""",
                "python": """class Solution:
    def combine(self, n: int, k: int) -> list[list[int]]:
        res = []
        path = []
        def dfs(cur: int):
            if len(path) == k:
                res.append(list(path))
                return
            if cur > n:
                return
            path.append(cur)
            dfs(cur + 1)
            path.pop()
            dfs(cur + 1)
        dfs(1)
        return res"""
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
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> combine(int n, int k) {
        List<List<Integer>> res = new ArrayList<>();
        backtrack(1, n, k, new ArrayList<>(), res);
        return res;
    }
    private void backtrack(int start, int n, int k, List<Integer> path, List<List<Integer>> res) {
        if (path.size() == k) {
            res.add(new ArrayList<>(path));
            return;
        }
        int need = k - path.size();
        for (int i = start; i <= n - need + 1; i++) {
            path.add(i);
            backtrack(i + 1, n, k, path, res);
            path.remove(path.size() - 1);
        }
    }
}""",
                "python": """class Solution:
    def combine(self, n: int, k: int) -> list[list[int]]:
        res = []
        path = []
        def backtrack(start: int):
            if len(path) == k:
                res.append(list(path))
                return
            need = k - len(path)
            for i in range(start, n - need + 2):
                path.append(i)
                backtrack(i + 1)
                path.pop()
        backtrack(1)
        return res"""
            }
        }
    },
    # 108: Permutations
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
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> permute(int[] nums) {
        List<List<Integer>> res = new ArrayList<>();
        dfs(nums, new ArrayList<>(), res);
        return res;
    }
    private void dfs(int[] nums, List<Integer> path, List<List<Integer>> res) {
        if (path.size() == nums.length) {
            res.add(new ArrayList<>(path));
            return;
        }
        for (int num : nums) {
            if (path.contains(num)) continue;
            path.add(num);
            dfs(nums, path, res);
            path.remove(path.size() - 1);
        }
    }
}""",
                "python": """class Solution:
    def permute(self, nums: list[int]) -> list[list[int]]:
        res = []
        path = []
        def dfs():
            if len(path) == len(nums):
                res.append(list(path))
                return
            for x in nums:
                if x not in path:
                    path.append(x)
                    dfs()
                    path.pop()
        dfs()
        return res"""
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
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> permute(int[] nums) {
        List<List<Integer>> res = new ArrayList<>();
        List<Integer> list = new ArrayList<>();
        for (int x : nums) list.add(x);
        backtrack(0, list, res);
        return res;
    }
    private void backtrack(int first, List<Integer> list, List<List<Integer>> res) {
        if (first == list.size()) {
            res.add(new ArrayList<>(list));
            return;
        }
        for (int i = first; i < list.size(); i++) {
            Collections.swap(list, first, i);
            backtrack(first + 1, list, res);
            Collections.swap(list, first, i);
        }
    }
}""",
                "python": """class Solution:
    def permute(self, nums: list[int]) -> list[list[int]]:
        res = []
        def backtrack(first: int):
            if first == len(nums):
                res.append(list(nums))
                return
            for i in range(first, len(nums)):
                nums[first], nums[i] = nums[i], nums[first]
                backtrack(first + 1)
                nums[first], nums[i] = nums[i], nums[first]
        backtrack(0)
        return res"""
            }
        }
    },
    # 109: Permutations II
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
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> permuteUnique(int[] nums) {
        Set<List<Integer>> set = new HashSet<>();
        boolean[] used = new boolean[nums.length];
        dfs(nums, used, new ArrayList<>(), set);
        return new ArrayList<>(set);
    }
    private void dfs(int[] nums, boolean[] used, List<Integer> path, Set<List<Integer>> set) {
        if (path.size() == nums.length) {
            set.add(new ArrayList<>(path));
            return;
        }
        for (int i = 0; i < nums.length; i++) {
            if (used[i]) continue;
            used[i] = true;
            path.add(nums[i]);
            dfs(nums, used, path, set);
            path.remove(path.size() - 1);
            used[i] = false;
        }
    }
}""",
                "python": """class Solution:
    def permuteUnique(self, nums: list[int]) -> list[list[int]]:
        res = set()
        used = [False] * len(nums)
        path = []
        def dfs():
            if len(path) == len(nums):
                res.add(tuple(path))
                return
            for i in range(len(nums)):
                if not used[i]:
                    used[i] = True
                    path.append(nums[i])
                    dfs()
                    path.pop()
                    used[i] = False
        dfs()
        return [list(x) for x in res]"""
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
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> permuteUnique(int[] nums) {
        Arrays.sort(nums);
        List<List<Integer>> res = new ArrayList<>();
        boolean[] used = new boolean[nums.length];
        backtrack(nums, used, new ArrayList<>(), res);
        return res;
    }
    private void backtrack(int[] nums, boolean[] used, List<Integer> path, List<List<Integer>> res) {
        if (path.size() == nums.length) {
            res.add(new ArrayList<>(path));
            return;
        }
        for (int i = 0; i < nums.length; i++) {
            if (used[i]) continue;
            if (i > 0 && nums[i] == nums[i - 1] && !used[i - 1]) continue;
            used[i] = true;
            path.add(nums[i]);
            backtrack(nums, used, path, res);
            path.remove(path.size() - 1);
            used[i] = false;
        }
    }
}""",
                "python": """class Solution:
    def permuteUnique(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        res = []
        used = [False] * len(nums)
        path = []
        def backtrack():
            if len(path) == len(nums):
                res.append(list(path))
                return
            for i in range(len(nums)):
                if used[i]:
                    continue
                if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                    continue
                used[i] = True
                path.append(nums[i])
                backtrack()
                path.pop()
                used[i] = False
        backtrack()
        return res"""
            }
        }
    },
    # 110: Letter Case Permutation
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
                "java": """import java.util.*;
class Solution {
    public List<String> letterCasePermutation(String s) {
        List<String> res = new ArrayList<>();
        dfs(s, 0, "", res);
        return res;
    }
    private void dfs(String s, int idx, String cur, List<String> res) {
        if (idx == s.length()) {
            res.add(cur);
            return;
        }
        char c = s.charAt(idx);
        if (Character.isLetter(c)) {
            dfs(s, idx + 1, cur + Character.toLowerCase(c), res);
            dfs(s, idx + 1, cur + Character.toUpperCase(c), res);
        } else {
            dfs(s, idx + 1, cur + c, res);
        }
    }
}""",
                "python": """class Solution:
    def letterCasePermutation(self, s: str) -> list[str]:
        res = []
        def dfs(idx: int, cur: str):
            if idx == len(s):
                res.append(cur)
                return
            c = s[idx]
            if c.isalpha():
                dfs(idx + 1, cur + c.lower())
                dfs(idx + 1, cur + c.upper())
            else:
                dfs(idx + 1, cur + c)
        dfs(0, "")
        return res"""
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
                "java": """import java.util.*;
class Solution {
    public List<String> letterCasePermutation(String s) {
        List<String> res = new ArrayList<>();
        char[] chars = s.toCharArray();
        backtrack(chars, 0, res);
        return res;
    }
    private void backtrack(char[] chars, int idx, List<String> res) {
        if (idx == chars.length) {
            res.add(new String(chars));
            return;
        }
        if (Character.isLetter(chars[idx])) {
            chars[idx] = Character.toLowerCase(chars[idx]);
            backtrack(chars, idx + 1, res);
            chars[idx] = Character.toUpperCase(chars[idx]);
            backtrack(chars, idx + 1, res);
        } else {
            backtrack(chars, idx + 1, res);
        }
    }
}""",
                "python": """class Solution:
    def letterCasePermutation(self, s: str) -> list[str]:
        res = []
        chars = list(s)
        def backtrack(idx: int):
            if idx == len(chars):
                res.append("".join(chars))
                return
            if chars[idx].isalpha():
                chars[idx] = chars[idx].lower()
                backtrack(idx + 1)
                chars[idx] = chars[idx].upper()
                backtrack(idx + 1)
            else:
                backtrack(idx + 1)
        backtrack(0)
        return res"""
            }
        }
    },
    # 111: Letter Combinations of a Phone Number
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
                "java": """import java.util.*;
class Solution {
    public List<String> letterCombinations(String digits) {
        if (digits.isEmpty()) return Collections.emptyList();
        String[] map = {"", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"};
        List<String> res = new ArrayList<>();
        res.add("");
        for (char d : digits.toCharArray()) {
            List<String> next = new ArrayList<>();
            for (String s : res) {
                for (char c : map[d - '0'].toCharArray()) {
                    next.add(s + c);
                }
            }
            res = next;
        }
        return res;
    }
}""",
                "python": """class Solution:
    def letterCombinations(self, digits: str) -> list[str]:
        if not digits:
            return []
        phone = ["", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"]
        res = [""]
        for d in digits:
            res = [s + c for s in res for c in phone[int(d)]]
        return res"""
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
                "java": """import java.util.*;
class Solution {
    private static final String[] MAPPING = {
        "", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"
    };
    public List<String> letterCombinations(String digits) {
        List<String> res = new ArrayList<>();
        if (digits == null || digits.isEmpty()) return res;
        backtrack(digits, 0, new StringBuilder(), res);
        return res;
    }
    private void backtrack(String digits, int idx, StringBuilder path, List<String> res) {
        if (idx == digits.length()) {
            res.add(path.toString());
            return;
        }
        String letters = MAPPING[digits.charAt(idx) - '0'];
        for (int i = 0; i < letters.length(); i++) {
            path.append(letters.charAt(i));
            backtrack(digits, idx + 1, path, res);
            path.deleteCharAt(path.length() - 1);
        }
    }
}""",
                "python": """class Solution:
    def letterCombinations(self, digits: str) -> list[str]:
        if not digits:
            return []
        mapping = ["", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"]
        res = []
        path = []
        def backtrack(idx: int):
            if idx == len(digits):
                res.append("".join(path))
                return
            for c in mapping[int(digits[idx])]:
                path.append(c)
                backtrack(idx + 1)
                path.pop()
        backtrack(0)
        return res"""
            }
        }
    },
    # 112: Generate Parentheses
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
                "java": """import java.util.*;
class Solution {
    public List<String> generateParenthesis(int n) {
        List<String> res = new ArrayList<>();
        generateAll(new char[2 * n], 0, res);
        return res;
    }
    private void generateAll(char[] current, int pos, List<String> result) {
        if (pos == current.length) {
            if (valid(current)) result.add(new String(current));
            return;
        }
        current[pos] = '(';
        generateAll(current, pos + 1, result);
        current[pos] = ')';
        generateAll(current, pos + 1, result);
    }
    private boolean valid(char[] current) {
        int balance = 0;
        for (char c : current) {
            if (c == '(') balance++;
            else balance--;
            if (balance < 0) return false;
        }
        return balance == 0;
    }
}""",
                "python": """class Solution:
    def generateParenthesis(self, n: int) -> list[str]:
        res = []
        def valid(s: str) -> bool:
            bal = 0
            for c in s:
                bal += 1 if c == '(' else -1
                if bal < 0: return False
            return bal == 0
        def generate(s: str):
            if len(s) == 2 * n:
                if valid(s): res.append(s)
                return
            generate(s + '(')
            generate(s + ')')
        generate('')
        return res"""
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
                "java": """import java.util.*;
class Solution {
    public List<String> generateParenthesis(int n) {
        List<String> res = new ArrayList<>();
        backtrack(new StringBuilder(), 0, 0, n, res);
        return res;
    }
    private void backtrack(StringBuilder sb, int open, int close, int n, List<String> res) {
        if (sb.length() == 2 * n) {
            res.add(sb.toString());
            return;
        }
        if (open < n) {
            sb.append('(');
            backtrack(sb, open + 1, close, n, res);
            sb.deleteCharAt(sb.length() - 1);
        }
        if (close < open) {
            sb.append(')');
            backtrack(sb, open, close + 1, n, res);
            sb.deleteCharAt(sb.length() - 1);
        }
    }
}""",
                "python": """class Solution:
    def generateParenthesis(self, n: int) -> list[str]:
        res = []
        path = []
        def backtrack(open_cnt: int, close_cnt: int):
            if len(path) == 2 * n:
                res.append("".join(path))
                return
            if open_cnt < n:
                path.append('(')
                backtrack(open_cnt + 1, close_cnt)
                path.pop()
            if close_cnt < open_cnt:
                path.append(')')
                backtrack(open_cnt, close_cnt + 1)
                path.pop()
        backtrack(0, 0)
        return res"""
            }
        }
    },
    # 113: Palindrome Partitioning
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
                "java": """import java.util.*;
class Solution {
    public List<List<String>> partition(String s) {
        List<List<String>> res = new ArrayList<>();
        dfs(0, s, new ArrayList<>(), res);
        return res;
    }
    private void dfs(int start, String s, List<String> path, List<List<String>> res) {
        if (start == s.length()) {
            res.add(new ArrayList<>(path));
            return;
        }
        for (int end = start; end < s.length(); end++) {
            if (isPalindrome(s, start, end)) {
                path.add(s.substring(start, end + 1));
                dfs(end + 1, s, path, res);
                path.remove(path.size() - 1);
            }
        }
    }
    private boolean isPalindrome(String s, int l, int r) {
        while (l < r) {
            if (s.charAt(l++) != s.charAt(r--)) return false;
        }
        return true;
    }
}""",
                "python": """class Solution:
    def partition(self, s: str) -> list[list[str]]:
        res = []
        path = []
        def is_pal(sub: str) -> bool:
            return sub == sub[::-1]
        def dfs(start: int):
            if start == len(s):
                res.append(list(path))
                return
            for end in range(start, len(s)):
                sub = s[start:end+1]
                if is_pal(sub):
                    path.append(sub)
                    dfs(end + 1)
                    path.pop()
        dfs(0)
        return res"""
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
                "java": """import java.util.*;
class Solution {
    public List<List<String>> partition(String s) {
        int n = s.length();
        boolean[][] dp = new boolean[n][n];
        for (int len = 1; len <= n; len++) {
            for (int i = 0; i <= n - len; i++) {
                int j = i + len - 1;
                if (s.charAt(i) == s.charAt(j)) {
                    dp[i][j] = (len <= 2) || dp[i + 1][j - 1];
                }
            }
        }
        List<List<String>> res = new ArrayList<>();
        backtrack(0, s, dp, new ArrayList<>(), res);
        return res;
    }
    private void backtrack(int start, String s, boolean[][] dp, List<String> path, List<List<String>> res) {
        if (start == s.length()) {
            res.add(new ArrayList<>(path));
            return;
        }
        for (int end = start; end < s.length(); end++) {
            if (dp[start][end]) {
                path.add(s.substring(start, end + 1));
                backtrack(end + 1, s, dp, path, res);
                path.remove(path.size() - 1);
            }
        }
    }
}""",
                "python": """class Solution:
    def partition(self, s: str) -> list[list[str]]:
        n = len(s)
        dp = [[False] * n for _ in range(n)]
        for length in range(1, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] == s[j]:
                    dp[i][j] = (length <= 2) or dp[i + 1][j - 1]
        res = []
        path = []
        def backtrack(start: int):
            if start == n:
                res.append(list(path))
                return
            for end in range(start, n):
                if dp[start][end]:
                    path.append(s[start:end+1])
                    backtrack(end + 1)
                    path.pop()
        backtrack(0)
        return res"""
            }
        }
    },
    # 114: Restore IP Addresses
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
                "java": """import java.util.*;
class Solution {
    public List<String> restoreIpAddresses(String s) {
        List<String> res = new ArrayList<>();
        int n = s.length();
        for (int i = 1; i < 4 && i < n; i++) {
            for (int j = i + 1; j < i + 4 && j < n; j++) {
                for (int k = j + 1; k < j + 4 && k < n; k++) {
                    String s1 = s.substring(0, i), s2 = s.substring(i, j);
                    String s3 = s.substring(j, k), s4 = s.substring(k);
                    if (isValid(s1) && isValid(s2) && isValid(s3) && isValid(s4)) {
                        res.add(s1 + "." + s2 + "." + s3 + "." + s4);
                    }
                }
            }
        }
        return res;
    }
    private boolean isValid(String seg) {
        if (seg.isEmpty() || seg.length() > 3) return false;
        if (seg.charAt(0) == '0' && seg.length() > 1) return false;
        int val = Integer.parseInt(seg);
        return val >= 0 && val <= 255;
    }
}""",
                "python": """class Solution:
    def restoreIpAddresses(self, s: str) -> list[str]:
        n = len(s)
        res = []
        def valid(seg: str) -> bool:
            if not seg or len(seg) > 3: return False
            if seg[0] == '0' and len(seg) > 1: return False
            return 0 <= int(seg) <= 255
        for i in range(1, min(4, n)):
            for j in range(i + 1, min(i + 4, n)):
                for k in range(j + 1, min(j + 4, n)):
                    s1, s2, s3, s4 = s[:i], s[i:j], s[j:k], s[k:]
                    if valid(s1) and valid(s2) and valid(s3) and valid(s4):
                        res.append(f"{s1}.{s2}.{s3}.{s4}")
        return res"""
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
                "java": """import java.util.*;
class Solution {
    public List<String> restoreIpAddresses(String s) {
        List<String> res = new ArrayList<>();
        if (s.length() < 4 || s.length() > 12) return res;
        backtrack(s, 0, 0, new ArrayList<>(), res);
        return res;
    }
    private void backtrack(String s, int start, int segCount, List<String> path, List<String> res) {
        if (segCount == 4) {
            if (start == s.length()) res.add(String.join(".", path));
            return;
        }
        int remainingChars = s.length() - start;
        int remainingSegs = 4 - segCount;
        if (remainingChars < remainingSegs || remainingChars > remainingSegs * 3) return;
        for (int len = 1; len <= 3 && start + len <= s.length(); len++) {
            String seg = s.substring(start, start + len);
            if (seg.charAt(0) == '0' && len > 1) break;
            if (Integer.parseInt(seg) > 255) break;
            path.add(seg);
            backtrack(s, start + len, segCount + 1, path, res);
            path.remove(path.size() - 1);
        }
    }
}""",
                "python": """class Solution:
    def restoreIpAddresses(self, s: str) -> list[str]:
        res = []
        if not (4 <= len(s) <= 12):
            return res
        path = []
        def backtrack(start: int, seg_count: int):
            if seg_count == 4:
                if start == len(s):
                    res.append(".".join(path))
                return
            rem_chars = len(s) - start
            rem_segs = 4 - seg_count
            if not (rem_segs <= rem_chars <= rem_segs * 3):
                return
            for length in range(1, min(4, rem_chars + 1)):
                seg = s[start:start+length]
                if seg[0] == '0' and length > 1:
                    break
                if int(seg) > 255:
                    break
                path.append(seg)
                backtrack(start + length, seg_count + 1)
                path.pop()
        backtrack(0, 0)
        return res"""
            }
        }
    },
    # 115: Word Search
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
                "java": """class Solution {
    public boolean exist(char[][] board, String word) {
        int m = board.length, n = board[0].length;
        boolean[][] visited = new boolean[m][n];
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (dfs(board, word, 0, i, j, visited)) return true;
            }
        }
        return false;
    }
    private boolean dfs(char[][] b, String w, int idx, int r, int c, boolean[][] visited) {
        if (idx == w.length()) return true;
        if (r < 0 || r >= b.length || c < 0 || c >= b[0].length || visited[r][c] || b[r][c] != w.charAt(idx)) {
            return false;
        }
        visited[r][c] = true;
        boolean found = dfs(b, w, idx + 1, r + 1, c, visited) ||
                        dfs(b, w, idx + 1, r - 1, c, visited) ||
                        dfs(b, w, idx + 1, r, c + 1, visited) ||
                        dfs(b, w, idx + 1, r, c - 1, visited);
        visited[r][c] = false;
        return found;
    }
}""",
                "python": """class Solution:
    def exist(self, board: list[list[str]], word: str) -> bool:
        m, n = len(board), len(board[0])
        visited = [[False] * n for _ in range(m)]
        def dfs(r: int, c: int, idx: int) -> bool:
            if idx == len(word):
                return True
            if not (0 <= r < m and 0 <= c < n) or visited[r][c] or board[r][c] != word[idx]:
                return False
            visited[r][c] = True
            found = (dfs(r + 1, c, idx + 1) or
                     dfs(r - 1, c, idx + 1) or
                     dfs(r, c + 1, idx + 1) or
                     dfs(r, c - 1, idx + 1))
            visited[r][c] = False
            return found
        for i in range(m):
            for j in range(n):
                if dfs(i, j, 0):
                    return True
        return False"""
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
                "java": """class Solution {
    public boolean exist(char[][] board, String word) {
        int m = board.length, n = board[0].length;
        if (word.length() > m * n) return false;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (board[i][j] == word.charAt(0) && dfs(board, word, 0, i, j)) {
                    return true;
                }
            }
        }
        return false;
    }
    private boolean dfs(char[][] board, String word, int idx, int r, int c) {
        if (idx == word.length()) return true;
        if (r < 0 || r >= board.length || c < 0 || c >= board[0].length || board[r][c] != word.charAt(idx)) {
            return false;
        }
        char temp = board[r][c];
        board[r][c] = '#';
        boolean found = dfs(board, word, idx + 1, r + 1, c) ||
                        dfs(board, word, idx + 1, r - 1, c) ||
                        dfs(board, word, idx + 1, r, c + 1) ||
                        dfs(board, word, idx + 1, r, c - 1);
        board[r][c] = temp;
        return found;
    }
}""",
                "python": """class Solution:
    def exist(self, board: list[list[str]], word: str) -> bool:
        m, n = len(board), len(board[0])
        if len(word) > m * n:
            return False
        def dfs(r: int, c: int, idx: int) -> bool:
            if idx == len(word):
                return True
            if not (0 <= r < m and 0 <= c < n) or board[r][c] != word[idx]:
                return False
            temp = board[r][c]
            board[r][c] = '#'
            found = (dfs(r + 1, c, idx + 1) or
                     dfs(r - 1, c, idx + 1) or
                     dfs(r, c + 1, idx + 1) or
                     dfs(r, c - 1, idx + 1))
            board[r][c] = temp
            return found
        for i in range(m):
            for j in range(n):
                if board[i][j] == word[0] and dfs(i, j, 0):
                    return True
        return False"""
            }
        }
    },
    # 116: N-Queens
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
                "java": """import java.util.*;
class Solution {
    public List<List<String>> solveNQueens(int n) {
        List<List<String>> res = new ArrayList<>();
        int[] queens = new int[n];
        placeQueens(0, n, queens, res);
        return res;
    }
    private void placeQueens(int row, int n, int[] queens, List<List<String>> res) {
        if (row == n) {
            res.add(format(queens, n));
            return;
        }
        for (int col = 0; col < n; col++) {
            if (isValid(row, col, queens)) {
                queens[row] = col;
                placeQueens(row + 1, n, queens, res);
            }
        }
    }
    private boolean isValid(int row, int col, int[] queens) {
        for (int r = 0; r < row; r++) {
            int c = queens[r];
            if (c == col || Math.abs(r - row) == Math.abs(c - col)) return false;
        }
        return true;
    }
    private List<String> format(int[] queens, int n) {
        List<String> board = new ArrayList<>();
        for (int r = 0; r < n; r++) {
            char[] row = new char[n];
            Arrays.fill(row, '.');
            row[queens[r]] = 'Q';
            board.add(new String(row));
        }
        return board;
    }
}""",
                "python": """class Solution:
    def solveNQueens(self, n: int) -> list[list[str]]:
        res = []
        queens = [-1] * n
        def is_valid(row: int, col: int) -> bool:
            for r in range(row):
                c = queens[r]
                if c == col or abs(r - row) == abs(c - col):
                    return False
            return True
        def place(row: int):
            if row == n:
                board = []
                for r in range(n):
                    line = ['.'] * n
                    line[queens[r]] = 'Q'
                    board.append("".join(line))
                res.append(board)
                return
            for col in range(n):
                if is_valid(row, col):
                    queens[row] = col
                    place(row + 1)
        place(0)
        return res"""
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
                "java": """import java.util.*;
class Solution {
    public List<List<String>> solveNQueens(int n) {
        List<List<String>> res = new ArrayList<>();
        char[][] board = new char[n][n];
        for (char[] row : board) Arrays.fill(row, '.');
        boolean[] cols = new boolean[n];
        boolean[] diag1 = new boolean[2 * n];
        boolean[] diag2 = new boolean[2 * n];
        backtrack(0, n, board, cols, diag1, diag2, res);
        return res;
    }
    private void backtrack(int r, int n, char[][] board, boolean[] cols, boolean[] d1, boolean[] d2, List<List<String>> res) {
        if (r == n) {
            List<String> list = new ArrayList<>();
            for (char[] row : board) list.add(new String(row));
            res.add(list);
            return;
        }
        for (int c = 0; c < n; c++) {
            int id1 = r + c;
            int id2 = r - c + n;
            if (cols[c] || d1[id1] || d2[id2]) continue;
            board[r][c] = 'Q';
            cols[c] = d1[id1] = d2[id2] = true;
            backtrack(r + 1, n, board, cols, d1, d2, res);
            cols[c] = d1[id1] = d2[id2] = false;
            board[r][c] = '.';
        }
    }
}""",
                "python": """class Solution:
    def solveNQueens(self, n: int) -> list[list[str]]:
        res = []
        board = [["."] * n for _ in range(n)]
        cols = [False] * n
        diag1 = [False] * (2 * n)
        diag2 = [False] * (2 * n)
        def backtrack(r: int):
            if r == n:
                res.append(["".join(row) for row in board])
                return
            for c in range(n):
                if cols[c] or diag1[r + c] or diag2[r - c + n]:
                    continue
                board[r][c] = 'Q'
                cols[c] = diag1[r + c] = diag2[r - c + n] = True
                backtrack(r + 1)
                cols[c] = diag1[r + c] = diag2[r - c + n] = False
                board[r][c] = '.'
        backtrack(0)
        return res"""
            }
        }
    },
    # 117: N-Queens II
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
                "java": """class Solution {
    private int count = 0;
    public int totalNQueens(int n) {
        boolean[] cols = new boolean[n];
        boolean[] d1 = new boolean[2 * n];
        boolean[] d2 = new boolean[2 * n];
        dfs(0, n, cols, d1, d2);
        return count;
    }
    private void dfs(int r, int n, boolean[] cols, boolean[] d1, boolean[] d2) {
        if (r == n) {
            count++;
            return;
        }
        for (int c = 0; c < n; c++) {
            if (cols[c] || d1[r + c] || d2[r - c + n]) continue;
            cols[c] = d1[r + c] = d2[r - c + n] = true;
            dfs(r + 1, n, cols, d1, d2);
            cols[c] = d1[r + c] = d2[r - c + n] = false;
        }
    }
}""",
                "python": """class Solution:
    def totalNQueens(self, n: int) -> int:
        count = 0
        cols = [False] * n
        d1 = [False] * (2 * n)
        d2 = [False] * (2 * n)
        def dfs(r: int):
            nonlocal count
            if r == n:
                count += 1
                return
            for c in range(n):
                if cols[c] or d1[r + c] or d2[r - c + n]:
                    continue
                cols[c] = d1[r + c] = d2[r - c + n] = True
                dfs(r + 1)
                cols[c] = d1[r + c] = d2[r - c + n] = False
        dfs(0)
        return count"""
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
                "java": """class Solution {
    private int count = 0;
    public int totalNQueens(int n) {
        backtrack(0, 0, 0, 0, n);
        return count;
    }
    private void backtrack(int row, int cols, int d1, int d2, int n) {
        if (row == n) {
            count++;
            return;
        }
        int available = ((1 << n) - 1) & ~(cols | d1 | d2);
        while (available != 0) {
            int p = available & (-available);
            available &= available - 1;
            backtrack(row + 1, cols | p, (d1 | p) << 1, (d2 | p) >> 1, n);
        }
    }
}""",
                "python": """class Solution:
    def totalNQueens(self, n: int) -> int:
        count = 0
        def backtrack(row: int, cols: int, d1: int, d2: int):
            nonlocal count
            if row == n:
                count += 1
                return
            available = ((1 << n) - 1) & ~(cols | d1 | d2)
            while available:
                p = available & (-available)
                available &= available - 1
                backtrack(row + 1, cols | p, (d1 | p) << 1, (d2 | p) >> 1)
        backtrack(0, 0, 0, 0)
        return count"""
            }
        }
    },
    # 118: Sudoku Solver
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
                "java": """class Solution {
    public void solveSudoku(char[][] board) {
        solve(board);
    }
    private boolean solve(char[][] board) {
        for (int r = 0; r < 9; r++) {
            for (int c = 0; c < 9; c++) {
                if (board[r][c] == '.') {
                    for (char d = '1'; d <= '9'; d++) {
                        if (isValid(board, r, c, d)) {
                            board[r][c] = d;
                            if (solve(board)) return true;
                            board[r][c] = '.';
                        }
                    }
                    return false;
                }
            }
        }
        return true;
    }
    private boolean isValid(char[][] board, int r, int c, char d) {
        for (int i = 0; i < 9; i++) {
            if (board[r][i] == d || board[i][c] == d) return false;
            int boxR = 3 * (r / 3) + i / 3;
            int boxC = 3 * (c / 3) + i % 3;
            if (board[boxR][boxC] == d) return false;
        }
        return true;
    }
}""",
                "python": """class Solution:
    def solveSudoku(self, board: list[list[str]]) -> None:
        def is_valid(r: int, c: int, d: str) -> bool:
            for i in range(9):
                if board[r][i] == d or board[i][c] == d:
                    return False
                if board[3 * (r // 3) + i // 3][3 * (c // 3) + i % 3] == d:
                    return False
            return True
        def solve() -> bool:
            for r in range(9):
                for c in range(9):
                    if board[r][c] == '.':
                        for d in "123456789":
                            if is_valid(r, c, d):
                                board[r][c] = d
                                if solve(): return True
                                board[r][c] = '.'
                        return False
            return True
        solve()"""
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
                "java": """import java.util.*;
class Solution {
    private int[] rows = new int[9];
    private int[] cols = new int[9];
    private int[] boxes = new int[9];
    private List<int[]> empties = new ArrayList<>();
    public void solveSudoku(char[][] board) {
        for (int r = 0; r < 9; r++) {
            for (int c = 0; c < 9; c++) {
                if (board[r][c] == '.') {
                    empties.add(new int[]{r, c});
                } else {
                    int d = board[r][c] - '1';
                    int mask = 1 << d;
                    rows[r] |= mask;
                    cols[c] |= mask;
                    boxes[(r / 3) * 3 + c / 3] |= mask;
                }
            }
        }
        backtrack(board, 0);
    }
    private boolean backtrack(char[][] board, int idx) {
        if (idx == empties.size()) return true;
        int r = empties.get(idx)[0], c = empties.get(idx)[1];
        int b = (r / 3) * 3 + c / 3;
        int available = ~(rows[r] | cols[c] | boxes[b]) & 0x1FF;
        while (available != 0) {
            int p = available & (-available);
            int d = Integer.numberOfTrailingZeros(p);
            available &= available - 1;
            board[r][c] = (char) ('1' + d);
            rows[r] |= p; cols[c] |= p; boxes[b] |= p;
            if (backtrack(board, idx + 1)) return true;
            rows[r] &= ~p; cols[c] &= ~p; boxes[b] &= ~p;
            board[r][c] = '.';
        }
        return false;
    }
}""",
                "python": """class Solution:
    def solveSudoku(self, board: list[list[str]]) -> None:
        rows = [0] * 9
        cols = [0] * 9
        boxes = [0] * 9
        empties = []
        for r in range(9):
            for c in range(9):
                if board[r][c] == '.':
                    empties.append((r, c))
                else:
                    d = int(board[r][c]) - 1
                    mask = 1 << d
                    rows[r] |= mask
                    cols[c] |= mask
                    boxes[(r // 3) * 3 + c // 3] |= mask
        def backtrack(idx: int) -> bool:
            if idx == len(empties):
                return True
            r, c = empties[idx]
            b = (r // 3) * 3 + c // 3
            available = ~(rows[r] | cols[c] | boxes[b]) & 0x1FF
            while available:
                p = available & (-available)
                d = (p).bit_length() - 1
                available &= available - 1
                board[r][c] = str(d + 1)
                rows[r] |= p
                cols[c] |= p
                boxes[b] |= p
                if backtrack(idx + 1):
                    return True
                rows[r] &= ~p
                cols[c] &= ~p
                boxes[b] &= ~p
                board[r][c] = '.'
            return False
        backtrack(0)"""
            }
        }
    },
    # 119: Target Sum
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
                "java": """class Solution {
    public int findTargetSumWays(int[] nums, int target) {
        return dfs(nums, 0, 0, target);
    }
    private int dfs(int[] nums, int idx, int curSum, int target) {
        if (idx == nums.length) {
            return curSum == target ? 1 : 0;
        }
        return dfs(nums, idx + 1, curSum + nums[idx], target) +
               dfs(nums, idx + 1, curSum - nums[idx], target);
    }
}""",
                "python": """class Solution:
    def findTargetSumWays(self, nums: list[int], target: int) -> int:
        def dfs(idx: int, cur_sum: int) -> int:
            if idx == len(nums):
                return 1 if cur_sum == target else 0
            return dfs(idx + 1, cur_sum + nums[idx]) + dfs(idx + 1, cur_sum - nums[idx])
        return dfs(0, 0)"""
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
                "java": """class Solution {
    public int findTargetSumWays(int[] nums, int target) {
        int sum = 0;
        for (int x : nums) sum += x;
        if (sum < Math.abs(target) || (sum + target) % 2 != 0) return 0;
        int s = (sum + target) / 2;
        int[] dp = new int[s + 1];
        dp[0] = 1;
        for (int num : nums) {
            for (int j = s; j >= num; j--) {
                dp[j] += dp[j - num];
            }
        }
        return dp[s];
    }
}""",
                "python": """class Solution:
    def findTargetSumWays(self, nums: list[int], target: int) -> int:
        total = sum(nums)
        if total < abs(target) or (total + target) % 2 != 0:
            return 0
        s = (total + target) // 2
        dp = [0] * (s + 1)
        dp[0] = 1
        for num in nums:
            for j in range(s, num - 1, -1):
                dp[j] += dp[j - num]
        return dp[s]"""
            }
        }
    },
    # 120: Partition to K Equal Sum Subsets
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
                "java": """import java.util.*;
class Solution {
    public boolean canPartitionKSubsets(int[] nums, int k) {
        int sum = 0;
        for (int x : nums) sum += x;
        if (sum % k != 0) return false;
        int target = sum / k;
        int[] buckets = new int[k];
        return dfs(nums, 0, buckets, target);
    }
    private boolean dfs(int[] nums, int idx, int[] buckets, int target) {
        if (idx == nums.length) return true;
        for (int i = 0; i < buckets.length; i++) {
            if (buckets[i] + nums[idx] <= target) {
                buckets[i] += nums[idx];
                if (dfs(nums, idx + 1, buckets, target)) return true;
                buckets[i] -= nums[idx];
            }
            if (buckets[i] == 0) break;
        }
        return false;
    }
}""",
                "python": """class Solution:
    def canPartitionKSubsets(self, nums: list[int], k: int) -> bool:
        total = sum(nums)
        if total % k != 0: return False
        target = total // k
        buckets = [0] * k
        def dfs(idx: int) -> bool:
            if idx == len(nums):
                return True
            for i in range(k):
                if buckets[i] + nums[idx] <= target:
                    buckets[i] += nums[idx]
                    if dfs(idx + 1): return True
                    buckets[i] -= nums[idx]
                if buckets[i] == 0:
                    break
            return False
        return dfs(0)"""
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
                "java": """import java.util.*;
class Solution {
    public boolean canPartitionKSubsets(int[] nums, int k) {
        int sum = 0;
        for (int x : nums) sum += x;
        if (sum % k != 0) return false;
        int target = sum / k;
        Arrays.sort(nums);
        int n = nums.length;
        if (nums[n - 1] > target) return false;
        boolean[] used = new boolean[n];
        return backtrack(nums, used, k, 0, target, n - 1);
    }
    private boolean backtrack(int[] nums, boolean[] used, int k, int currentSum, int target, int start) {
        if (k == 1) return true;
        if (currentSum == target) {
            return backtrack(nums, used, k - 1, 0, target, nums.length - 1);
        }
        for (int i = start; i >= 0; i--) {
            if (used[i] || currentSum + nums[i] > target) continue;
            used[i] = true;
            if (backtrack(nums, used, k, currentSum + nums[i], target, i - 1)) return true;
            used[i] = false;
            if (currentSum == 0 || currentSum + nums[i] == target) break;
        }
        return false;
    }
}""",
                "python": """class Solution:
    def canPartitionKSubsets(self, nums: list[int], k: int) -> bool:
        total = sum(nums)
        if total % k != 0: return False
        target = total // k
        nums.sort(reverse=True)
        if nums[0] > target: return False
        n = len(nums)
        used = [False] * n
        def backtrack(k_rem: int, cur_sum: int, start: int) -> bool:
            if k_rem == 1:
                return True
            if cur_sum == target:
                return backtrack(k_rem - 1, 0, 0)
            for i in range(start, n):
                if used[i] or cur_sum + nums[i] > target:
                    continue
                used[i] = True
                if backtrack(k_rem, cur_sum + nums[i], i + 1):
                    return True
                used[i] = False
                if cur_sum == 0 or cur_sum + nums[i] == target:
                    break
            return False
        return backtrack(k, 0, 0)"""
            }
        }
    },
    # 121: Maximum Depth of Binary Tree
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
                "java": """import java.util.*;
class Solution {
    public int maxDepth(TreeNode root) {
        if (root == null) return 0;
        Queue<TreeNode> q = new LinkedList<>();
        q.offer(root);
        int depth = 0;
        while (!q.isEmpty()) {
            int size = q.size();
            for (int i = 0; i < size; i++) {
                TreeNode node = q.poll();
                if (node.left != null) q.offer(node.left);
                if (node.right != null) q.offer(node.right);
            }
            depth++;
        }
        return depth;
    }
}""",
                "python": """from collections import deque

class Solution:
    def maxDepth(self, root: TreeNode | None) -> int:
        if not root:
            return 0
        q = deque([root])
        depth = 0
        while q:
            for _ in range(len(q)):
                node = q.popleft()
                if node.left: q.append(node.left)
                if node.right: q.append(node.right)
            depth += 1
        return depth"""
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
                "java": """class Solution {
    public int maxDepth(TreeNode root) {
        if (root == null) return 0;
        return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
    }
}""",
                "python": """class Solution:
    def maxDepth(self, root: TreeNode | None) -> int:
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))"""
            }
        }
    },
    # 122: Minimum Depth of Binary Tree
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
                "java": """class Solution {
    public int minDepth(TreeNode root) {
        if (root == null) return 0;
        if (root.left == null) return 1 + minDepth(root.right);
        if (root.right == null) return 1 + minDepth(root.left);
        return 1 + Math.min(minDepth(root.left), minDepth(root.right));
    }
}""",
                "python": """class Solution:
    def minDepth(self, root: TreeNode | None) -> int:
        if not root:
            return 0
        if not root.left:
            return 1 + self.minDepth(root.right)
        if not root.right:
            return 1 + self.minDepth(root.left)
        return 1 + min(self.minDepth(root.left), self.minDepth(root.right))"""
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
                "java": """import java.util.*;
class Solution {
    public int minDepth(TreeNode root) {
        if (root == null) return 0;
        Queue<TreeNode> q = new LinkedList<>();
        q.offer(root);
        int depth = 1;
        while (!q.isEmpty()) {
            int size = q.size();
            for (int i = 0; i < size; i++) {
                TreeNode node = q.poll();
                if (node.left == null && node.right == null) return depth;
                if (node.left != null) q.offer(node.left);
                if (node.right != null) q.offer(node.right);
            }
            depth++;
        }
        return depth;
    }
}""",
                "python": """from collections import deque

class Solution:
    def minDepth(self, root: TreeNode | None) -> int:
        if not root:
            return 0
        q = deque([(root, 1)])
        while q:
            node, depth = q.popleft()
            if not node.left and not node.right:
                return depth
            if node.left:
                q.append((node.left, depth + 1))
            if node.right:
                q.append((node.right, depth + 1))
        return 0"""
            }
        }
    },
    # 123: Invert Binary Tree
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
                "java": """import java.util.*;
class Solution {
    public TreeNode invertTree(TreeNode root) {
        if (root == null) return null;
        Queue<TreeNode> q = new LinkedList<>();
        q.offer(root);
        while (!q.isEmpty()) {
            TreeNode node = q.poll();
            TreeNode temp = node.left;
            node.left = node.right;
            node.right = temp;
            if (node.left != null) q.offer(node.left);
            if (node.right != null) q.offer(node.right);
        }
        return root;
    }
}""",
                "python": """from collections import deque

class Solution:
    def invertTree(self, root: TreeNode | None) -> TreeNode | None:
        if not root:
            return None
        q = deque([root])
        while q:
            node = q.popleft()
            node.left, node.right = node.right, node.left
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
        return root"""
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
                "java": """class Solution {
    public TreeNode invertTree(TreeNode root) {
        if (root == null) return null;
        TreeNode left = invertTree(root.left);
        TreeNode right = invertTree(root.right);
        root.left = right;
        root.right = left;
        return root;
    }
}""",
                "python": """class Solution:
    def invertTree(self, root: TreeNode | None) -> TreeNode | None:
        if not root:
            return None
        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root"""
            }
        }
    },
    # 124: Same Tree
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
                "java": """class Solution {
    public boolean isSameTree(TreeNode p, TreeNode q) {
        StringBuilder sb1 = new StringBuilder();
        StringBuilder sb2 = new StringBuilder();
        serialize(p, sb1);
        serialize(q, sb2);
        return sb1.toString().equals(sb2.toString());
    }
    private void serialize(TreeNode node, StringBuilder sb) {
        if (node == null) {
            sb.append("#,");
            return;
        }
        sb.append(node.val).append(",");
        serialize(node.left, sb);
        serialize(node.right, sb);
    }
}""",
                "python": """class Solution:
    def isSameTree(self, p: TreeNode | None, q: TreeNode | None) -> bool:
        def serialize(node: TreeNode | None) -> str:
            if not node:
                return "#,"
            return f"{node.val}," + serialize(node.left) + serialize(node.right)
        return serialize(p) == serialize(q)"""
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
                "java": """class Solution {
    public boolean isSameTree(TreeNode p, TreeNode q) {
        if (p == null && q == null) return true;
        if (p == null || q == null || p.val != q.val) return false;
        return isSameTree(p.left, q.left) && isSameTree(p.right, q.right);
    }
}""",
                "python": """class Solution:
    def isSameTree(self, p: TreeNode | None, q: TreeNode | None) -> bool:
        if not p and not q:
            return True
        if not p or not q or p.val != q.val:
            return False
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)"""
            }
        }
    },
    # 125: Symmetric Tree
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
                "java": """class Solution {
    public boolean isSymmetric(TreeNode root) {
        if (root == null) return true;
        invert(root.left);
        return isSame(root.left, root.right);
    }
    private void invert(TreeNode node) {
        if (node == null) return;
        TreeNode temp = node.left;
        node.left = node.right;
        node.right = temp;
        invert(node.left);
        invert(node.right);
    }
    private boolean isSame(TreeNode p, TreeNode q) {
        if (p == null && q == null) return true;
        if (p == null || q == null || p.val != q.val) return false;
        return isSame(p.left, q.left) && isSame(p.right, q.right);
    }
}""",
                "python": """class Solution:
    def isSymmetric(self, root: TreeNode | None) -> bool:
        if not root:
            return True
        def invert(node: TreeNode | None):
            if not node: return
            node.left, node.right = node.right, node.left
            invert(node.left)
            invert(node.right)
        def is_same(p, q):
            if not p and not q: return True
            if not p or not q or p.val != q.val: return False
            return is_same(p.left, q.left) and is_same(p.right, q.right)
        invert(root.left)
        return is_same(root.left, root.right)"""
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
                "java": """class Solution {
    public boolean isSymmetric(TreeNode root) {
        if (root == null) return true;
        return isMirror(root.left, root.right);
    }
    private boolean isMirror(TreeNode t1, TreeNode t2) {
        if (t1 == null && t2 == null) return true;
        if (t1 == null || t2 == null || t1.val != t2.val) return false;
        return isMirror(t1.left, t2.right) && isMirror(t1.right, t2.left);
    }
}""",
                "python": """class Solution:
    def isSymmetric(self, root: TreeNode | None) -> bool:
        if not root:
            return True
        def is_mirror(t1: TreeNode | None, t2: TreeNode | None) -> bool:
            if not t1 and not t2:
                return True
            if not t1 or not t2 or t1.val != t2.val:
                return False
            return is_mirror(t1.left, t2.right) and is_mirror(t1.right, t2.left)
        return is_mirror(root.left, root.right)"""
            }
        }
    }
]

with open('scripts/batches/batch_05.py', 'w', encoding='utf-8') as f:
    f.write("# Batch 5: Questions 101 to 125\n\n")
    f.write("def get_batch():\n")
    f.write("    return " + json.dumps(batch_5, indent=4) + "\n")

print("Wrote scripts/batches/batch_05.py with", len(batch_5), "questions.")

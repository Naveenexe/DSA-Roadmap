# Batch 8: Questions 176 to 200

def get_batch():
    return [
    {
        "seq": 176,
        "whyNext": "Kadane's algorithm: curSum = max(num, curSum + num) resets negative prefix sums in O(n) single pass.",
        "brute": {
            "idea": "Check all O(n^2) subarrays by fixing start index and expanding end index, keeping maximum sum.",
            "steps": [
                "Outer loop for start from 0 to n - 1.",
                "Inner loop for end from start to n - 1, maintaining running sum.",
                "Update maxSum."
            ],
            "time": "O(n^2)",
            "space": "O(1)",
            "whySlow": "Tests all quadratic subarrays instead of resetting at negative running sums.",
            "code": {
                "java": "class Solution {\n    public int maxSubArray(int[] nums) {\n        int maxSum = Integer.MIN_VALUE;\n        for (int i = 0; i < nums.length; i++) {\n            int cur = 0;\n            for (int j = i; j < nums.length; j++) {\n                cur += nums[j];\n                maxSum = Math.max(maxSum, cur);\n            }\n        }\n        return maxSum;\n    }\n}",
                "python": "class Solution:\n    def maxSubArray(self, nums: list[int]) -> int:\n        max_sum = float('-inf')\n        for i in range(len(nums)):\n            cur = 0\n            for j in range(i, len(nums)):\n                cur += nums[j]\n                max_sum = max(max_sum, cur)\n        return max_sum"
            }
        },
        "optimal": {
            "idea": "Kadane's Algorithm: at each element, either start fresh at nums[i] or add to curSum; update global max.",
            "steps": [
                "curSum = 0, maxSum = nums[0].",
                "For each x in nums: curSum = Math.max(x, curSum + x); maxSum = Math.max(maxSum, curSum).",
                "Return maxSum."
            ],
            "time": "O(n)",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public int maxSubArray(int[] nums) {\n        int maxSum = nums[0];\n        int curSum = 0;\n        for (int x : nums) {\n            curSum = Math.max(x, curSum + x);\n            maxSum = Math.max(maxSum, curSum);\n        }\n        return maxSum;\n    }\n}",
                "python": "class Solution:\n    def maxSubArray(self, nums: list[int]) -> int:\n        max_sum = nums[0]\n        cur_sum = 0\n        for x in nums:\n            cur_sum = max(x, cur_sum + x)\n            max_sum = max(max_sum, cur_sum)\n        return max_sum"
            }
        }
    },
    {
        "seq": 177,
        "whyNext": "Builds on Kadane's: circular max is either normal Kadane max OR totalSum - minKadane (wrapped case).",
        "brute": {
            "idea": "Concatenate nums with itself or test all starting positions of length up to n.",
            "steps": [
                "For every starting index i from 0 to n - 1:",
                "Accumulate sum up to length n, keeping maximum."
            ],
            "time": "O(n^2)",
            "space": "O(1)",
            "whySlow": "Checks all circular subarray spans explicitly in quadratic time.",
            "code": {
                "java": "class Solution {\n    public int maxSubarraySumCircular(int[] nums) {\n        int n = nums.length;\n        int max = Integer.MIN_VALUE;\n        for (int i = 0; i < n; i++) {\n            int cur = 0;\n            for (int k = 0; k < n; k++) {\n                cur += nums[(i + k) % n];\n                max = Math.max(max, cur);\n            }\n        }\n        return max;\n    }\n}",
                "python": "class Solution:\n    def maxSubarraySumCircular(self, nums: list[int]) -> int:\n        n = len(nums)\n        ans = float('-inf')\n        for i in range(n):\n            cur = 0\n            for k in range(n):\n                cur += nums[(i + k) % n]\n                ans = max(ans, cur)\n        return ans"
            }
        },
        "optimal": {
            "idea": "Simultaneously compute maxSubarray and minSubarray in one pass; wrapped max is total - minSubarray (unless all negative).",
            "steps": [
                "Track totalSum, curMax, maxKadane, curMin, minKadane.",
                "In loop over nums: update curMax = max(x, curMax + x), maxKadane = max(maxKadane, curMax).",
                "update curMin = min(x, curMin + x), minKadane = min(minKadane, curMin), totalSum += x.",
                "If maxKadane < 0 (all elements negative), return maxKadane.",
                "Return max(maxKadane, totalSum - minKadane)."
            ],
            "time": "O(n)",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public int maxSubarraySumCircular(int[] nums) {\n        int total = 0, curMax = 0, maxKadane = nums[0];\n        int curMin = 0, minKadane = nums[0];\n        for (int x : nums) {\n            curMax = Math.max(x, curMax + x);\n            maxKadane = Math.max(maxKadane, curMax);\n            curMin = Math.min(x, curMin + x);\n            minKadane = Math.min(minKadane, curMin);\n            total += x;\n        }\n        return maxKadane > 0 ? Math.max(maxKadane, total - minKadane) : maxKadane;\n    }\n}",
                "python": "class Solution:\n    def maxSubarraySumCircular(self, nums: list[int]) -> int:\n        total = 0\n        cur_max = 0\n        max_kadane = nums[0]\n        cur_min = 0\n        min_kadane = nums[0]\n        for x in nums:\n            cur_max = max(x, cur_max + x)\n            max_kadane = max(max_kadane, cur_max)\n            cur_min = min(x, cur_min + x)\n            min_kadane = min(min_kadane, cur_min)\n            total += x\n        return max(max_kadane, total - min_kadane) if max_kadane > 0 else max_kadane"
            }
        }
    },
    {
        "seq": 178,
        "whyNext": "Greedy reachability: track furthest reachable index maxReach = max(maxReach, i + nums[i]); fail if i > maxReach.",
        "brute": {
            "idea": "Recursively check all jump lengths from 1 to nums[index].",
            "steps": [
                "canJump(pos): if pos >= n - 1 return true.",
                "For jump 1 to nums[pos], if canJump(pos + jump) return true."
            ],
            "time": "O(2^n)",
            "space": "O(n)",
            "whySlow": "Explores exponential paths branching at each index.",
            "code": {
                "java": "class Solution {\n    public boolean canJump(int[] nums) {\n        return canJumpFrom(0, nums);\n    }\n    private boolean canJumpFrom(int pos, int[] nums) {\n        if (pos >= nums.length - 1) return true;\n        int furthest = Math.min(pos + nums[pos], nums.length - 1);\n        for (int next = furthest; next > pos; next--) {\n            if (canJumpFrom(next, nums)) return true;\n        }\n        return false;\n    }\n}",
                "python": "class Solution:\n    def canJump(self, nums: list[int]) -> bool:\n        def dfs(pos):\n            if pos >= len(nums) - 1: return True\n            furthest = min(pos + nums[pos], len(nums) - 1)\n            for nxt in range(furthest, pos, -1):\n                if dfs(nxt): return True\n            return False\n        return dfs(0)"
            }
        },
        "optimal": {
            "idea": "Greedy maximum reach: maintain maxReach; if i > maxReach return false; if maxReach >= n - 1 return true.",
            "steps": [
                "maxReach = 0.",
                "For i from 0 to n - 1:",
                "If i > maxReach return false.",
                "maxReach = Math.max(maxReach, i + nums[i]).",
                "If maxReach >= n - 1 return true.",
                "Return true."
            ],
            "time": "O(n)",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public boolean canJump(int[] nums) {\n        int maxReach = 0;\n        for (int i = 0; i < nums.length; i++) {\n            if (i > maxReach) return false;\n            maxReach = Math.max(maxReach, i + nums[i]);\n            if (maxReach >= nums.length - 1) return true;\n        }\n        return true;\n    }\n}",
                "python": "class Solution:\n    def canJump(self, nums: list[int]) -> bool:\n        max_reach = 0\n        for i, jump in enumerate(nums):\n            if i > max_reach:\n                return False\n            max_reach = max(max_reach, i + jump)\n            if max_reach >= len(nums) - 1:\n                return True\n        return True"
            }
        }
    },
    {
        "seq": 179,
        "whyNext": "BFS level interval greedy: current jump boundary curEnd; when i reaches curEnd, increment jumps and set curEnd = curFarthest.",
        "brute": {
            "idea": "Dynamic programming: dp[i] = min jumps to reach index i from any j < i.",
            "steps": [
                "Initialize dp array with infinity, dp[0] = 0.",
                "For i from 0 to n - 1, for j from 1 to nums[i], dp[i + j] = min(dp[i + j], dp[i] + 1)."
            ],
            "time": "O(n^2)",
            "space": "O(n)",
            "whySlow": "Examines all quadratic edges between indices.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int jump(int[] nums) {\n        int n = nums.length;\n        int[] dp = new int[n];\n        Arrays.fill(dp, 100000);\n        dp[0] = 0;\n        for (int i = 0; i < n; i++) {\n            for (int j = 1; j <= nums[i] && i + j < n; j++) {\n                dp[i + j] = Math.min(dp[i + j], dp[i] + 1);\n            }\n        }\n        return dp[n - 1];\n    }\n}",
                "python": "class Solution:\n    def jump(self, nums: list[int]) -> int:\n        n = len(nums)\n        dp = [float('inf')] * n\n        dp[0] = 0\n        for i in range(n):\n            for j in range(1, nums[i] + 1):\n                if i + j < n:\n                    dp[i + j] = min(dp[i + j], dp[i] + 1)\n        return dp[-1]"
            }
        },
        "optimal": {
            "idea": "Implicit BFS in O(n) time and O(1) space: track current level boundary curEnd and next level farthest curFarthest.",
            "steps": [
                "jumps = 0, curEnd = 0, curFarthest = 0.",
                "Loop i from 0 to n - 2 (stop before last element):",
                "curFarthest = Math.max(curFarthest, i + nums[i]).",
                "If i == curEnd: jumps++, curEnd = curFarthest.",
                "Return jumps."
            ],
            "time": "O(n)",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public int jump(int[] nums) {\n        int jumps = 0, curEnd = 0, curFarthest = 0;\n        for (int i = 0; i < nums.length - 1; i++) {\n            curFarthest = Math.max(curFarthest, i + nums[i]);\n            if (i == curEnd) {\n                jumps++;\n                curEnd = curFarthest;\n            }\n        }\n        return jumps;\n    }\n}",
                "python": "class Solution:\n    def jump(self, nums: list[int]) -> int:\n        jumps = 0\n        cur_end = 0\n        cur_farthest = 0\n        for i in range(len(nums) - 1):\n            cur_farthest = max(cur_farthest, i + nums[i])\n            if i == cur_end:\n                jumps += 1\n                cur_end = cur_farthest\n        return jumps"
            }
        }
    },
    {
        "seq": 180,
        "whyNext": "Circular circuit invariant: if total gas >= total cost, a solution exists; if tank drops below 0 at i, start index must be i + 1.",
        "brute": {
            "idea": "Simulate circular tour starting from every station i from 0 to n - 1.",
            "steps": [
                "For start from 0 to n - 1:",
                "Simulate tank over n steps.",
                "If tank never drops below 0, return start."
            ],
            "time": "O(n^2)",
            "space": "O(1)",
            "whySlow": "Simulates full cycle for each starting index instead of resetting past failed segments in O(n).",
            "code": {
                "java": "class Solution {\n    public int canCompleteCircuit(int[] gas, int[] cost) {\n        int n = gas.length;\n        for (int start = 0; start < n; start++) {\n            int tank = 0;\n            boolean ok = true;\n            for (int k = 0; k < n; k++) {\n                int cur = (start + k) % n;\n                tank += gas[cur] - cost[cur];\n                if (tank < 0) {\n                    ok = false;\n                    break;\n                }\n            }\n            if (ok) return start;\n        }\n        return -1;\n    }\n}",
                "python": "class Solution:\n    def canCompleteCircuit(self, gas: list[int], cost: list[int]) -> int:\n        n = len(gas)\n        for start in range(n):\n            tank = 0\n            ok = True\n            for k in range(n):\n                cur = (start + k) % n\n                tank += gas[cur] - cost[cur]\n                if tank < 0:\n                    ok = False\n                    break\n            if ok: return start\n        return -1"
            }
        },
        "optimal": {
            "idea": "Single pass: if totalGas < totalCost return -1; if curTank < 0, reset start = i + 1 and curTank = 0.",
            "steps": [
                "totalGas = 0, curTank = 0, start = 0.",
                "For i from 0 to n - 1:",
                "diff = gas[i] - cost[i].",
                "totalGas += diff; curTank += diff.",
                "If curTank < 0: start = i + 1, curTank = 0.",
                "Return totalGas >= 0 ? start : -1."
            ],
            "time": "O(n)",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public int canCompleteCircuit(int[] gas, int[] cost) {\n        int total = 0, cur = 0, start = 0;\n        for (int i = 0; i < gas.length; i++) {\n            int diff = gas[i] - cost[i];\n            total += diff;\n            cur += diff;\n            if (cur < 0) {\n                start = i + 1;\n                cur = 0;\n            }\n        }\n        return total >= 0 ? start : -1;\n    }\n}",
                "python": "class Solution:\n    def canCompleteCircuit(self, gas: list[int], cost: list[int]) -> int:\n        total = 0\n        cur = 0\n        start = 0\n        for i in range(len(gas)):\n            diff = gas[i] - cost[i]\n            total += diff\n            cur += diff\n            if cur < 0:\n                start = i + 1\n                cur = 0\n        return start if total >= 0 else -1"
            }
        }
    },
    {
        "seq": 181,
        "whyNext": "Two-pass greedy: left-to-right pass ensures higher rating than left neighbor gets more; right-to-left ensures same for right neighbor.",
        "brute": {
            "idea": "Repeatedly update candy counts for all children until no child violates neighbor rules.",
            "steps": [
                "Initialize candies = [1, ..., 1].",
                "Loop until no updates occur: if ratings[i] > ratings[i-1] && candies[i] <= candies[i-1], candies[i] = candies[i-1] + 1; same for right neighbor."
            ],
            "time": "O(n^2)",
            "space": "O(n)",
            "whySlow": "Propagation of changes can take O(n) passes in the worst case (e.g. descending ratings).",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int candy(int[] ratings) {\n        int n = ratings.length;\n        int[] candies = new int[n];\n        Arrays.fill(candies, 1);\n        boolean changed = true;\n        while (changed) {\n            changed = false;\n            for (int i = 0; i < n; i++) {\n                if (i > 0 && ratings[i] > ratings[i - 1] && candies[i] <= candies[i - 1]) {\n                    candies[i] = candies[i - 1] + 1;\n                    changed = true;\n                }\n                if (i < n - 1 && ratings[i] > ratings[i + 1] && candies[i] <= candies[i + 1]) {\n                    candies[i] = candies[i + 1] + 1;\n                    changed = true;\n                }\n            }\n        }\n        int sum = 0;\n        for (int c : candies) sum += c;\n        return sum;\n    }\n}",
                "python": "class Solution:\n    def candy(self, ratings: list[int]) -> int:\n        n = len(ratings)\n        candies = [1] * n\n        changed = True\n        while changed:\n            changed = False\n            for i in range(n):\n                if i > 0 and ratings[i] > ratings[i - 1] and candies[i] <= candies[i - 1]:\n                    candies[i] = candies[i - 1] + 1\n                    changed = True\n                if i < n - 1 and ratings[i] > ratings[i + 1] and candies[i] <= candies[i + 1]:\n                    candies[i] = candies[i + 1] + 1\n                    changed = True\n        return sum(candies)"
            }
        },
        "optimal": {
            "idea": "Two passes: pass 1 (left to right) sets candies[i] = candies[i-1] + 1 if ratings[i] > ratings[i-1]; pass 2 (right to left) sets candies[i] = max(candies[i], candies[i+1] + 1).",
            "steps": [
                "Initialize int[] candies filled with 1.",
                "Left-to-right: for i = 1..n-1: if ratings[i] > ratings[i-1], candies[i] = candies[i-1] + 1.",
                "Right-to-left: for i = n-2..0: if ratings[i] > ratings[i+1], candies[i] = Math.max(candies[i], candies[i+1] + 1).",
                "Sum candies array."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int candy(int[] ratings) {\n        int n = ratings.length;\n        int[] candies = new int[n];\n        Arrays.fill(candies, 1);\n        for (int i = 1; i < n; i++) {\n            if (ratings[i] > ratings[i - 1]) {\n                candies[i] = candies[i - 1] + 1;\n            }\n        }\n        for (int i = n - 2; i >= 0; i--) {\n            if (ratings[i] > ratings[i + 1]) {\n                candies[i] = Math.max(candies[i], candies[i + 1] + 1);\n            }\n        }\n        int sum = 0;\n        for (int c : candies) sum += c;\n        return sum;\n    }\n}",
                "python": "class Solution:\n    def candy(self, ratings: list[int]) -> int:\n        n = len(ratings)\n        candies = [1] * n\n        for i in range(1, n):\n            if ratings[i] > ratings[i - 1]:\n                candies[i] = candies[i - 1] + 1\n        for i in range(n - 2, -1, -1):\n            if ratings[i] > ratings[i + 1]:\n                candies[i] = max(candies[i], candies[i + 1] + 1)\n        return sum(candies)"
            }
        }
    },
    {
        "seq": 182,
        "whyNext": "Last occurrence hash map: partition can end at index i only when i reaches the maximum last occurrence of all characters seen so far.",
        "brute": {
            "idea": "For every character in current partition, check if it appears anywhere after current split point; expand split until none do.",
            "steps": [
                "While string not exhausted, find smallest prefix where all its characters do not appear in suffix.",
                "Record prefix length and repeat."
            ],
            "time": "O(n^2)",
            "space": "O(1)",
            "whySlow": "Scans remainder of string repeatedly for each character.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<Integer> partitionLabels(String s) {\n        List<Integer> res = new ArrayList<>();\n        int i = 0;\n        while (i < s.length()) {\n            int end = s.lastIndexOf(s.charAt(i));\n            for (int j = i; j <= end; j++) {\n                end = Math.max(end, s.lastIndexOf(s.charAt(j)));\n            }\n            res.add(end - i + 1);\n            i = end + 1;\n        }\n        return res;\n    }\n}",
                "python": "class Solution:\n    def partitionLabels(self, s: str) -> list[int]:\n        res = []\n        i = 0\n        while i < len(s):\n            end = s.rfind(s[i])\n            j = i\n            while j <= end:\n                end = max(end, s.rfind(s[j]))\n                j += 1\n            res.append(end - i + 1)\n            i = end + 1\n        return res"
            }
        },
        "optimal": {
            "idea": "Precompute last appearance of each character: int[26] last; partition boundary is max(last[char]); split when i == maxLast.",
            "steps": [
                "int[] last = new int[26]; record last index for every char.",
                "start = 0, end = 0.",
                "For i from 0 to n - 1: end = Math.max(end, last[s[i] - 'a']).",
                "If i == end: res.add(end - start + 1), start = i + 1."
            ],
            "time": "O(n)",
            "space": "O(1) (fixed 26 letters)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<Integer> partitionLabels(String s) {\n        int[] last = new int[26];\n        for (int i = 0; i < s.length(); i++) {\n            last[s.charAt(i) - 'a'] = i;\n        }\n        List<Integer> res = new ArrayList<>();\n        int start = 0, end = 0;\n        for (int i = 0; i < s.length(); i++) {\n            end = Math.max(end, last[s.charAt(i) - 'a']);\n            if (i == end) {\n                res.add(end - start + 1);\n                start = i + 1;\n            }\n        }\n        return res;\n    }\n}",
                "python": "class Solution:\n    def partitionLabels(self, s: str) -> list[int]:\n        last = {c: i for i, c in enumerate(s)}\n        res = []\n        start = end = 0\n        for i, c in enumerate(s):\n            end = max(end, last[c])\n            if i == end:\n                res.append(end - start + 1)\n                start = i + 1\n        return res"
            }
        }
    },
    {
        "seq": 183,
        "whyNext": "Monotonic stack with last-occurrence lookahead: pop stack top if top > current char AND top appears again later.",
        "brute": {
            "idea": "Find smallest character that can be picked as the first letter without starving any remaining unique letters; recurse.",
            "steps": [
                "Count frequencies.",
                "Find smallest character in prefix before any character's count drops to 0.",
                "Append that char and recurse on suffix with that char removed."
            ],
            "time": "O(26 * n)",
            "space": "O(n)",
            "whySlow": "Recursive string slicing and character removal costs extra work.",
            "code": {
                "java": "class Solution {\n    public String removeDuplicateLetters(String s) {\n        int[] count = new int[26];\n        for (char c : s.toCharArray()) count[c - 'a']++;\n        int pos = 0;\n        for (int i = 0; i < s.length(); i++) {\n            if (s.charAt(i) < s.charAt(pos)) pos = i;\n            if (--count[s.charAt(i) - 'a'] == 0) break;\n        }\n        if (s.isEmpty()) return \"\";\n        char c = s.charAt(pos);\n        return c + removeDuplicateLetters(s.substring(pos + 1).replaceAll(\"\" + c, \"\"));\n    }\n}",
                "python": "class Solution:\n    def removeDuplicateLetters(self, s: str) -> str:\n        from collections import Counter\n        count = Counter(s)\n        pos = 0\n        for i, c in enumerate(s):\n            if c < s[pos]: pos = i\n            count[c] -= 1\n            if count[c] == 0: break\n        return s[pos] + self.removeDuplicateLetters(s[pos+1:].replace(s[pos], \"\")) if s else \"\" "
            }
        },
        "optimal": {
            "idea": "Monotonic increasing stack + boolean[] inStack + int[] lastIndex: pop stack top if top > c and lastIndex[top] > i.",
            "steps": [
                "Record last occurrence index for every char.",
                "Maintain boolean[] inStack and a Deque / StringBuilder stack.",
                "For char c at index i: if inStack[c], continue.",
                "While !stack.isEmpty() and stack.peek() > c and lastIndex[stack.peek()] > i: inStack[stack.pop()] = false.",
                "stack.push(c), inStack[c] = true."
            ],
            "time": "O(n)",
            "space": "O(1) (fixed 26 letters)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public String removeDuplicateLetters(String s) {\n        int[] last = new int[26];\n        for (int i = 0; i < s.length(); i++) {\n            last[s.charAt(i) - 'a'] = i;\n        }\n        boolean[] inStack = new boolean[26];\n        StringBuilder sb = new StringBuilder();\n        for (int i = 0; i < s.length(); i++) {\n            char c = s.charAt(i);\n            int idx = c - 'a';\n            if (inStack[idx]) continue;\n            while (sb.length() > 0 && sb.charAt(sb.length() - 1) > c && last[sb.charAt(sb.length() - 1) - 'a'] > i) {\n                inStack[sb.charAt(sb.length() - 1) - 'a'] = false;\n                sb.deleteCharAt(sb.length() - 1);\n            }\n            sb.append(c);\n            inStack[idx] = true;\n        }\n        return sb.toString();\n    }\n}",
                "python": "class Solution:\n    def removeDuplicateLetters(self, s: str) -> str:\n        last = {c: i for i, c in enumerate(s)}\n        stack = []\n        in_stack = set()\n        for i, c in enumerate(s):\n            if c in in_stack:\n                continue\n            while stack and stack[-1] > c and last[stack[-1]] > i:\n                in_stack.remove(stack.pop())\n            stack.append(c)\n            in_stack.add(c)\n        return \"\".join(stack)"
            }
        }
    },
    {
        "seq": 184,
        "whyNext": "Greedy range extension: maintain covered range [1, miss); if nums[i] <= miss, extend to miss + nums[i]; else patch miss and double range.",
        "brute": {
            "idea": "For every number from 1 to n, verify if it can be formed as a subset sum; if not, add it as a patch.",
            "steps": [
                "Track reachable numbers using a boolean set.",
                "Find smallest unreachable number, patch it, and update reachable set."
            ],
            "time": "O(2^k * n)",
            "space": "O(n)",
            "whySlow": "Evaluating all subset sums up to n (which can be 2^31 - 1) causes memory and time limit exceeded.",
            "code": {
                "java": "class Solution {\n    public int minPatches(int[] nums, int n) {\n        long miss = 1;\n        int patches = 0, i = 0;\n        while (miss <= n) {\n            if (i < nums.length && nums[i] <= miss) {\n                miss += nums[i++];\n            } else {\n                miss += miss;\n                patches++;\n            }\n        }\n        return patches;\n    }\n}",
                "python": "class Solution:\n    def minPatches(self, nums: list[int], n: int) -> int:\n        miss = 1\n        patches = 0\n        i = 0\n        while miss <= n:\n            if i < len(nums) and nums[i] <= miss:\n                miss += nums[i]\n                i += 1\n            else:\n                miss += miss\n                patches += 1\n        return patches"
            }
        },
        "optimal": {
            "idea": "Greedy coverage expansion: can form [1, miss). If nums[i] <= miss, extend range to miss + nums[i]; else patch 'miss' directly, doubling range.",
            "steps": [
                "long miss = 1; int patches = 0, i = 0.",
                "While miss <= n:",
                "If i < nums.length && nums[i] <= miss: miss += nums[i++].",
                "Else: miss += miss; patches++.",
                "Return patches."
            ],
            "time": "O(m + log n)",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public int minPatches(int[] nums, int n) {\n        long miss = 1;\n        int patches = 0, i = 0;\n        while (miss <= n) {\n            if (i < nums.length && nums[i] <= miss) {\n                miss += nums[i++];\n            } else {\n                miss += miss;\n                patches++;\n            }\n        }\n        return patches;\n    }\n}",
                "python": "class Solution:\n    def minPatches(self, nums: list[int], n: int) -> int:\n        miss = 1\n        patches = 0\n        i = 0\n        while miss <= n:\n            if i < len(nums) and nums[i] <= miss:\n                miss += nums[i]\n                i += 1\n            else:\n                miss += miss\n                patches += 1\n        return patches"
            }
        }
    },
    {
        "seq": 185,
        "whyNext": "Opportunity cost sorting: sort people by costA - costB; send first n to city A and remaining n to city B.",
        "brute": {
            "idea": "Try all C(2n, n) assignments of people to city A and city B, keeping minimum total cost.",
            "steps": [
                "Recursively choose city A or city B for each person.",
                "Count people in city A and B.",
                "Return minimum cost among valid partitions."
            ],
            "time": "O(2^(2n))",
            "space": "O(n)",
            "whySlow": "Exponential combination search.",
            "code": {
                "java": "class Solution {\n    public int twoCitySchedCost(int[][] costs) {\n        return dfs(costs, 0, 0, 0, costs.length / 2);\n    }\n    private int dfs(int[][] costs, int idx, int a, int b, int n) {\n        if (idx == costs.length) return 0;\n        int chooseA = Integer.MAX_VALUE, chooseB = Integer.MAX_VALUE;\n        if (a < n) chooseA = costs[idx][0] + dfs(costs, idx + 1, a + 1, b, n);\n        if (b < n) chooseB = costs[idx][1] + dfs(costs, idx + 1, a, b + 1, n);\n        return Math.min(chooseA, chooseB);\n    }\n}",
                "python": "class Solution:\n    def twoCitySchedCost(self, costs: list[list[int]]) -> int:\n        n = len(costs) // 2\n        def dfs(i, a, b):\n            if i == len(costs): return 0\n            res = float('inf')\n            if a < n:\n                res = min(res, costs[i][0] + dfs(i + 1, a + 1, b))\n            if b < n:\n                res = min(res, costs[i][1] + dfs(i + 1, a, b + 1))\n            return res\n        return dfs(0, 0, 0)"
            }
        },
        "optimal": {
            "idea": "Greedy relative savings: sort costs by (costA - costB) ascending; send first n to city A, remaining n to city B.",
            "steps": [
                "Sort costs array using comparator: (a[0] - a[1]) - (b[0] - b[1]).",
                "Total cost = sum of costs[i][0] for first n people + sum of costs[i][1] for next n people.",
                "Return total."
            ],
            "time": "O(n log n)",
            "space": "O(1)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int twoCitySchedCost(int[][] costs) {\n        Arrays.sort(costs, (a, b) -> (a[0] - a[1]) - (b[0] - b[1]));\n        int total = 0;\n        int n = costs.length / 2;\n        for (int i = 0; i < n; i++) total += costs[i][0];\n        for (int i = n; i < 2 * n; i++) total += costs[i][1];\n        return total;\n    }\n}",
                "python": "class Solution:\n    def twoCitySchedCost(self, costs: list[list[int]]) -> int:\n        costs.sort(key=lambda x: x[0] - x[1])\n        n = len(costs) // 2\n        return sum(costs[i][0] for i in range(n)) + sum(costs[i][1] for i in range(n, 2 * n))"
            }
        }
    },
    {
        "seq": 186,
        "whyNext": "Greedy insertion sort: sort tallest people first (h desc, k asc); insert each person at index person.k.",
        "brute": {
            "idea": "Generate all permutations of people and test if every person has exactly k people >= h ahead of them.",
            "steps": [
                "Generate permutations of people array.",
                "Verify k constraint for each position."
            ],
            "time": "O(n! * n)",
            "space": "O(n)",
            "whySlow": "Examines all permutations instead of greedy deterministic insertion.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int[][] reconstructQueue(int[][] people) {\n        Arrays.sort(people, (a, b) -> a[0] != b[0] ? b[0] - a[0] : a[1] - b[1]);\n        List<int[]> list = new LinkedList<>();\n        for (int[] p : people) {\n            list.add(p[1], p);\n        }\n        return list.toArray(new int[people.length][]);\n    }\n}",
                "python": "class Solution:\n    def reconstructQueue(self, people: list[list[int]]) -> list[list[int]]:\n        people.sort(key=lambda p: (-p[0], p[1]))\n        res = []\n        for p in people:\n            res.insert(p[1], p)\n        return res"
            }
        },
        "optimal": {
            "idea": "Sort descending by height h, then ascending by k. Inserting shorter person at index k does not disturb already placed taller people.",
            "steps": [
                "Sort people: primary by h descending, secondary by k ascending.",
                "Initialize LinkedList<int[]> res.",
                "For each p in people: res.add(p[1], p).",
                "Convert list to 2D array."
            ],
            "time": "O(n^2)",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int[][] reconstructQueue(int[][] people) {\n        Arrays.sort(people, (a, b) -> a[0] != b[0] ? b[0] - a[0] : a[1] - b[1]);\n        List<int[]> res = new LinkedList<>();\n        for (int[] p : people) {\n            res.add(p[1], p);\n        }\n        return res.toArray(new int[people.length][]);\n    }\n}",
                "python": "class Solution:\n    def reconstructQueue(self, people: list[list[int]]) -> list[list[int]]:\n        people.sort(key=lambda x: (-x[0], x[1]))\n        res = []\n        for p in people:\n            res.insert(p[1], p)\n        return res"
            }
        }
    },
    {
        "seq": 187,
        "whyNext": "Wildcard parentheses: track possible range of open parentheses [cmin, cmax]; string is valid if cmin reaches 0 at end.",
        "brute": {
            "idea": "Recursively treat '*' as '(', ')', or empty string.",
            "steps": [
                "At each '*', branch 3 ways.",
                "Track open parenthesis balance; prune if balance < 0.",
                "Return true if any leaf has balance == 0."
            ],
            "time": "O(3^n)",
            "space": "O(n)",
            "whySlow": "3-way branching per '*' leads to exponential recursive tree.",
            "code": {
                "java": "class Solution {\n    public boolean checkValidString(String s) {\n        return dfs(s, 0, 0);\n    }\n    private boolean dfs(String s, int idx, int open) {\n        if (open < 0) return false;\n        if (idx == s.length()) return open == 0;\n        char c = s.charAt(idx);\n        if (c == '(') return dfs(s, idx + 1, open + 1);\n        if (c == ')') return dfs(s, idx + 1, open - 1);\n        return dfs(s, idx + 1, open + 1) || dfs(s, idx + 1, open - 1) || dfs(s, idx + 1, open);\n    }\n}",
                "python": "class Solution:\n    def checkValidString(self, s: str) -> bool:\n        def dfs(i, open_cnt):\n            if open_cnt < 0: return False\n            if i == len(s): return open_cnt == 0\n            if s[i] == '(': return dfs(i + 1, open_cnt + 1)\n            if s[i] == ')': return dfs(i + 1, open_cnt - 1)\n            return dfs(i + 1, open_cnt + 1) or dfs(i + 1, open_cnt - 1) or dfs(i + 1, open_cnt)\n        return dfs(0, 0)"
            }
        },
        "optimal": {
            "idea": "Track range of possible open parentheses [cmin, cmax]: '(' -> cmin++, cmax++; ')' -> cmin--, cmax--; '*' -> cmin--, cmax++. Clamp cmin = max(0, cmin).",
            "steps": [
                "cmin = 0, cmax = 0.",
                "For char c in s:",
                "If c == '(': cmin++, cmax++.",
                "Else if c == ')': cmin--, cmax--.",
                "Else: cmin--, cmax++ (treat '*' as ')', empty, or '(').",
                "If cmax < 0 return false.",
                "cmin = Math.max(0, cmin).",
                "Return cmin == 0."
            ],
            "time": "O(n)",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public boolean checkValidString(String s) {\n        int cmin = 0, cmax = 0;\n        for (char c : s.toCharArray()) {\n            if (c == '(') {\n                cmin++;\n                cmax++;\n            } else if (c == ')') {\n                cmin--;\n                cmax--;\n            } else {\n                cmin--;\n                cmax++;\n            }\n            if (cmax < 0) return false;\n            cmin = Math.max(0, cmin);\n        }\n        return cmin == 0;\n    }\n}",
                "python": "class Solution:\n    def checkValidString(self, s: str) -> bool:\n        cmin = cmax = 0\n        for c in s:\n            if c == '(':\n                cmin += 1\n                cmax += 1\n            elif c == ')':\n                cmin -= 1\n                cmax -= 1\n            else:\n                cmin -= 1\n                cmax += 1\n            if cmax < 0:\n                return False\n            cmin = max(0, cmin)\n        return cmin == 0"
            }
        }
    },
    {
        "seq": 188,
        "whyNext": "Entry to Chapter 12 (Intervals): sort by start time; if cur.start <= last.end merge by extending last.end = max(last.end, cur.end).",
        "brute": {
            "idea": "Represent intervals as a graph of overlapping components; compute connected components and merge intervals in each.",
            "steps": [
                "Build adjacency graph where edge exists if intervals overlap.",
                "Run DFS to find connected components.",
                "For each component, take min(start) and max(end)."
            ],
            "time": "O(n^2)",
            "space": "O(n^2)",
            "whySlow": "Graph construction and traversal requires O(n^2) edge comparisons.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int[][] merge(int[][] intervals) {\n        Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));\n        List<int[]> merged = new ArrayList<>();\n        for (int[] interval : intervals) {\n            if (merged.isEmpty() || merged.get(merged.size() - 1)[1] < interval[0]) {\n                merged.add(interval);\n            } else {\n                merged.get(merged.size() - 1)[1] = Math.max(merged.get(merged.size() - 1)[1], interval[1]);\n            }\n        }\n        return merged.toArray(new int[merged.size()][]);\n    }\n}",
                "python": "class Solution:\n    def merge(self, intervals: list[list[int]]) -> list[list[int]]:\n        intervals.sort(key=lambda x: x[0])\n        merged = []\n        for start, end in intervals:\n            if not merged or merged[-1][1] < start:\n                merged.append([start, end])\n            else:\n                merged[-1][1] = max(merged[-1][1], end)\n        return merged"
            }
        },
        "optimal": {
            "idea": "Sort by start time: iterate through intervals; if cur overlaps with last merged interval, extend end = max(end, cur.end); else append new.",
            "steps": [
                "Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0])).",
                "List<int[]> res = new ArrayList<>();",
                "For each interval in intervals: if res is empty or res.last().end < cur.start, add cur.",
                "Else res.last().end = Math.max(res.last().end, cur.end).",
                "Convert res to int[][] array."
            ],
            "time": "O(n log n)",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int[][] merge(int[][] intervals) {\n        Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));\n        List<int[]> res = new ArrayList<>();\n        for (int[] cur : intervals) {\n            if (res.isEmpty() || res.get(res.size() - 1)[1] < cur[0]) {\n                res.add(cur);\n            } else {\n                res.get(res.size() - 1)[1] = Math.max(res.get(res.size() - 1)[1], cur[1]);\n            }\n        }\n        return res.toArray(new int[res.size()][]);\n    }\n}",
                "python": "class Solution:\n    def merge(self, intervals: list[list[int]]) -> list[list[int]]:\n        intervals.sort(key=lambda x: x[0])\n        res = []\n        for cur in intervals:\n            if not res or res[-1][1] < cur[0]:\n                res.append(cur)\n            else:\n                res[-1][1] = max(res[-1][1], cur[1])\n        return res"
            }
        }
    },
    {
        "seq": 189,
        "whyNext": "Builds on Merge Intervals: input intervals already sorted and non-overlapping; 3 phases: before, overlapping merge, after.",
        "brute": {
            "idea": "Append newInterval to intervals list, sort by start time, and run Merge Intervals.",
            "steps": [
                "Insert newInterval into array.",
                "Sort array.",
                "Call merge(intervals)."
            ],
            "time": "O(n log n)",
            "space": "O(n)",
            "whySlow": "Sorting ignores existing sorted order of input intervals.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int[][] insert(int[][] intervals, int[] newInterval) {\n        List<int[]> list = new ArrayList<>(Arrays.asList(intervals));\n        list.add(newInterval);\n        list.sort(Comparator.comparingInt(a -> a[0]));\n        List<int[]> merged = new ArrayList<>();\n        for (int[] cur : list) {\n            if (merged.isEmpty() || merged.get(merged.size() - 1)[1] < cur[0]) {\n                merged.add(cur);\n            } else {\n                merged.get(merged.size() - 1)[1] = Math.max(merged.get(merged.size() - 1)[1], cur[1]);\n            }\n        }\n        return merged.toArray(new int[merged.size()][]);\n    }\n}",
                "python": "class Solution:\n    def insert(self, intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:\n        intervals.append(newInterval)\n        intervals.sort(key=lambda x: x[0])\n        res = []\n        for cur in intervals:\n            if not res or res[-1][1] < cur[0]:\n                res.append(cur)\n            else:\n                res[-1][1] = max(res[-1][1], cur[1])\n        return res"
            }
        },
        "optimal": {
            "idea": "Three linear phases: 1) add all intervals strictly ending before newInterval; 2) merge all overlapping intervals; 3) add remaining.",
            "steps": [
                "Phase 1: while i < n and intervals[i][1] < newInterval[0], add intervals[i++].",
                "Phase 2: while i < n and intervals[i][0] <= newInterval[1], merge: newInterval[0] = min(newInterval[0], intervals[i][0]), newInterval[1] = max(newInterval[1], intervals[i++][1]). Add newInterval.",
                "Phase 3: while i < n, add intervals[i++]."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int[][] insert(int[][] intervals, int[] newInterval) {\n        List<int[]> res = new ArrayList<>();\n        int i = 0, n = intervals.length;\n        while (i < n && intervals[i][1] < newInterval[0]) {\n            res.add(intervals[i++]);\n        }\n        while (i < n && intervals[i][0] <= newInterval[1]) {\n            newInterval[0] = Math.min(newInterval[0], intervals[i][0]);\n            newInterval[1] = Math.max(newInterval[1], intervals[i][1]);\n            i++;\n        }\n        res.add(newInterval);\n        while (i < n) {\n            res.add(intervals[i++]);\n        }\n        return res.toArray(new int[res.size()][]);\n    }\n}",
                "python": "class Solution:\n    def insert(self, intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:\n        res = []\n        i, n = 0, len(intervals)\n        while i < n and intervals[i][1] < newInterval[0]:\n            res.append(intervals[i])\n            i += 1\n        while i < n and intervals[i][0] <= newInterval[1]:\n            newInterval[0] = min(newInterval[0], intervals[i][0])\n            newInterval[1] = max(newInterval[1], intervals[i][1])\n            i += 1\n        res.append(newInterval)\n        while i < n:\n            res.append(intervals[i])\n            i += 1\n        return res"
            }
        }
    },
    {
        "seq": 190,
        "whyNext": "Interval scheduling greedy: sort intervals by end time; keep intervals with earliest end times to maximize non-overlapping count.",
        "brute": {
            "idea": "DP / recursion: find Longest Increasing Subsequence of non-overlapping intervals; answer is total - LIS length.",
            "steps": [
                "Sort intervals by start time.",
                "Compute dp[i] = max non-overlapping intervals ending at i.",
                "Return n - max(dp)."
            ],
            "time": "O(n^2)",
            "space": "O(n)",
            "whySlow": "Quadratic dynamic programming when greedy earliest-deadline-first is optimal.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int eraseOverlapIntervals(int[][] intervals) {\n        Arrays.sort(intervals, Comparator.comparingInt(a -> a[1]));\n        int count = 0;\n        int end = intervals[0][1];\n        for (int i = 1; i < intervals.length; i++) {\n            if (intervals[i][0] < end) {\n                count++;\n            } else {\n                end = intervals[i][1];\n            }\n        }\n        return count;\n    }\n}",
                "python": "class Solution:\n    def eraseOverlapIntervals(self, intervals: list[list[int]]) -> int:\n        intervals.sort(key=lambda x: x[1])\n        count = 0\n        end = intervals[0][1]\n        for i in range(1, len(intervals)):\n            if intervals[i][0] < end:\n                count += 1\n            else:\n                end = intervals[i][1]\n        return count"
            }
        },
        "optimal": {
            "idea": "Greedy interval scheduling: sort by end time; if cur.start < prevEnd, conflict exists (increment removals); else update prevEnd = cur.end.",
            "steps": [
                "Sort intervals ascending by end time (interval[1]).",
                "Track count = 0, prevEnd = intervals[0][1].",
                "For i from 1 to n - 1: if intervals[i][0] < prevEnd: count++; else prevEnd = intervals[i][1].",
                "Return count."
            ],
            "time": "O(n log n)",
            "space": "O(1)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int eraseOverlapIntervals(int[][] intervals) {\n        if (intervals.length == 0) return 0;\n        Arrays.sort(intervals, Comparator.comparingInt(a -> a[1]));\n        int removals = 0;\n        int end = intervals[0][1];\n        for (int i = 1; i < intervals.length; i++) {\n            if (intervals[i][0] < end) {\n                removals++;\n            } else {\n                end = intervals[i][1];\n            }\n        }\n        return removals;\n    }\n}",
                "python": "class Solution:\n    def eraseOverlapIntervals(self, intervals: list[list[int]]) -> int:\n        if not intervals:\n            return 0\n        intervals.sort(key=lambda x: x[1])\n        removals = 0\n        end = intervals[0][1]\n        for i in range(1, len(intervals)):\n            if intervals[i][0] < end:\n                removals += 1\n            else:\n                end = intervals[i][1]\n        return removals"
            }
        }
    },
    {
        "seq": 191,
        "whyNext": "Builds on Non-overlapping Intervals: shoot arrow at balloon's end point to pop maximum overlapping balloons.",
        "brute": {
            "idea": "Try shooting arrows at all possible x coordinates, keeping set of popped balloons.",
            "steps": [
                "Collect all unique x coordinates.",
                "Solve set cover problem to find minimum arrows popping all balloons."
            ],
            "time": "O(2^k)",
            "space": "O(n)",
            "whySlow": "Set cover is NP-hard without using sorted interval structure.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int findMinArrowShots(int[][] points) {\n        Arrays.sort(points, Comparator.comparingInt(a -> a[1]));\n        int arrows = 1;\n        long arrowPos = points[0][1];\n        for (int i = 1; i < points.length; i++) {\n            if (points[i][0] > arrowPos) {\n                arrows++;\n                arrowPos = points[i][1];\n            }\n        }\n        return arrows;\n    }\n}",
                "python": "class Solution:\n    def findMinArrowShots(self, points: list[list[int]]) -> int:\n        points.sort(key=lambda x: x[1])\n        arrows = 1\n        pos = points[0][1]\n        for i in range(1, len(points)):\n            if points[i][0] > pos:\n                arrows += 1\n                pos = points[i][1]\n        return arrows"
            }
        },
        "optimal": {
            "idea": "Sort by end coordinate using Integer.compare (avoids 32-bit underflow); shoot arrow at end; if next.start > arrowPos, shoot new arrow.",
            "steps": [
                "Arrays.sort(points, (a, b) -> Integer.compare(a[1], b[1])).",
                "arrows = 1, arrowPos = points[0][1].",
                "For i from 1 to n - 1: if points[i][0] > arrowPos: arrows++, arrowPos = points[i][1].",
                "Return arrows."
            ],
            "time": "O(n log n)",
            "space": "O(1)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int findMinArrowShots(int[][] points) {\n        if (points.length == 0) return 0;\n        Arrays.sort(points, (a, b) -> Integer.compare(a[1], b[1]));\n        int arrows = 1;\n        int arrowPos = points[0][1];\n        for (int i = 1; i < points.length; i++) {\n            if (points[i][0] > arrowPos) {\n                arrows++;\n                arrowPos = points[i][1];\n            }\n        }\n        return arrows;\n    }\n}",
                "python": "class Solution:\n    def findMinArrowShots(self, points: list[list[int]]) -> int:\n        if not points:\n            return 0\n        points.sort(key=lambda x: x[1])\n        arrows = 1\n        pos = points[0][1]\n        for i in range(1, len(points)):\n            if points[i][0] > pos:\n                arrows += 1\n                pos = points[i][1]\n        return arrows"
            }
        }
    },
    {
        "seq": 192,
        "whyNext": "Two-pointer interval intersection: intersection is [max(s1, s2), min(e1, e2)]; advance pointer with smaller end time.",
        "brute": {
            "idea": "Nested loops comparing every interval in firstList with every interval in secondList.",
            "steps": [
                "Check overlap between each pair (A[i], B[j]).",
                "If overlapping, add intersection [max(start), min(end)]."
            ],
            "time": "O(m * n)",
            "space": "O(min(m, n))",
            "whySlow": "Examines all pairs in quadratic time ignoring that both lists are already sorted.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int[][] intervalIntersection(int[][] firstList, int[][] secondList) {\n        List<int[]> res = new ArrayList<>();\n        int i = 0, j = 0;\n        while (i < firstList.length && j < secondList.length) {\n            int lo = Math.max(firstList[i][0], secondList[j][0]);\n            int hi = Math.min(firstList[i][1], secondList[j][1]);\n            if (lo <= hi) res.add(new int[]{lo, hi});\n            if (firstList[i][1] < secondList[j][1]) i++;\n            else j++;\n        }\n        return res.toArray(new int[res.size()][]);\n    }\n}",
                "python": "class Solution:\n    def intervalIntersection(self, firstList: list[list[int]], secondList: list[list[int]]) -> list[list[int]]:\n        res = []\n        i = j = 0\n        while i < len(firstList) and j < len(secondList):\n            lo = max(firstList[i][0], secondList[j][0])\n            hi = min(firstList[i][1], secondList[j][1])\n            if lo <= hi:\n                res.append([lo, hi])\n            if firstList[i][1] < secondList[j][1]:\n                i += 1\n            else:\n                j += 1\n        return res"
            }
        },
        "optimal": {
            "idea": "Two pointers i and j: compute lo = max(A.start, B.start), hi = min(A.end, B.end). If lo <= hi add to res; advance pointer with smaller end.",
            "steps": [
                "i = 0, j = 0.",
                "While i < len(A) and j < len(B):",
                "lo = max(firstList[i][0], secondList[j][0]), hi = min(firstList[i][1], secondList[j][1]).",
                "If lo <= hi, res.add([lo, hi]).",
                "If firstList[i][1] < secondList[j][1] i++; else j++."
            ],
            "time": "O(m + n)",
            "space": "O(m + n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int[][] intervalIntersection(int[][] firstList, int[][] secondList) {\n        List<int[]> res = new ArrayList<>();\n        int i = 0, j = 0;\n        while (i < firstList.length && j < secondList.length) {\n            int lo = Math.max(firstList[i][0], secondList[j][0]);\n            int hi = Math.min(firstList[i][1], secondList[j][1]);\n            if (lo <= hi) {\n                res.add(new int[]{lo, hi});\n            }\n            if (firstList[i][1] < secondList[j][1]) {\n                i++;\n            } else {\n                j++;\n            }\n        }\n        return res.toArray(new int[res.size()][]);\n    }\n}",
                "python": "class Solution:\n    def intervalIntersection(self, firstList: list[list[int]], secondList: list[list[int]]) -> list[list[int]]:\n        res = []\n        i = j = 0\n        while i < len(firstList) and j < len(secondList):\n            lo = max(firstList[i][0], secondList[j][0])\n            hi = min(firstList[i][1], secondList[j][1])\n            if lo <= hi:\n                res.append([lo, hi])\n            if firstList[i][1] < secondList[j][1]:\n                i += 1\n            else:\n                j += 1\n        return res"
            }
        }
    },
    {
        "seq": 193,
        "whyNext": "Sort by start asc, end desc: any interval with end <= maxEnd seen so far is strictly covered.",
        "brute": {
            "idea": "For every interval, check whether any other interval covers it in O(n^2).",
            "steps": [
                "For each i, check all j != i.",
                "If intervals[j][0] <= intervals[i][0] and intervals[j][1] >= intervals[i][1], mark i covered.",
                "Count uncovered intervals."
            ],
            "time": "O(n^2)",
            "space": "O(n)",
            "whySlow": "Checks all pairs in quadratic time.",
            "code": {
                "java": "class Solution {\n    public int removeCoveredIntervals(int[][] intervals) {\n        int n = intervals.length;\n        int covered = 0;\n        for (int i = 0; i < n; i++) {\n            for (int j = 0; j < n; j++) {\n                if (i != j && intervals[j][0] <= intervals[i][0] && intervals[j][1] >= intervals[i][1]) {\n                    covered++;\n                    break;\n                }\n            }\n        }\n        return n - covered;\n    }\n}",
                "python": "class Solution:\n    def removeCoveredIntervals(self, intervals: list[list[int]]) -> int:\n        n = len(intervals)\n        covered = 0\n        for i in range(n):\n            for j in range(n):\n                if i != j and intervals[j][0] <= intervals[i][0] and intervals[j][1] >= intervals[i][1]:\n                    covered += 1\n                    break\n        return n - covered"
            }
        },
        "optimal": {
            "idea": "Sort start asc, end desc. Track maxRight: if interval[1] <= maxRight it is covered; else count++ and update maxRight.",
            "steps": [
                "Arrays.sort(intervals, (a, b) -> a[0] != b[0] ? a[0] - b[0] : b[1] - a[1]).",
                "count = 0, maxRight = 0.",
                "For int[] cur : intervals:",
                "If cur[1] > maxRight: count++; maxRight = cur[1].",
                "Return count."
            ],
            "time": "O(n log n)",
            "space": "O(1)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int removeCoveredIntervals(int[][] intervals) {\n        Arrays.sort(intervals, (a, b) -> a[0] != b[0] ? a[0] - b[0] : b[1] - a[1]);\n        int count = 0;\n        int maxRight = 0;\n        for (int[] cur : intervals) {\n            if (cur[1] > maxRight) {\n                count++;\n                maxRight = cur[1];\n            }\n        }\n        return count;\n    }\n}",
                "python": "class Solution:\n    def removeCoveredIntervals(self, intervals: list[list[int]]) -> int:\n        intervals.sort(key=lambda x: (x[0], -x[1]))\n        count = 0\n        max_right = 0\n        for _, r in intervals:\n            if r > max_right:\n                count += 1\n                max_right = r\n        return count"
            }
        }
    },
    {
        "seq": 194,
        "whyNext": "BST / TreeMap interval collision check: floorKey and ceilingKey check adjacent bookings in O(log n).",
        "brute": {
            "idea": "Store all booked intervals in a list; for new booking check overlap with all existing bookings.",
            "steps": [
                "For each booking in list, check if max(start, b[0]) < min(end, b[1]).",
                "If no overlap, append to list and return true."
            ],
            "time": "O(n) per book",
            "space": "O(n)",
            "whySlow": "Linear scan across all bookings on each book() query.",
            "code": {
                "java": "import java.util.*;\npublic class MyCalendar {\n    private List<int[]> books = new ArrayList<>();\n    public MyCalendar() {}\n    public boolean book(int start, int end) {\n        for (int[] b : books) {\n            if (Math.max(start, b[0]) < Math.min(end, b[1])) {\n                return false;\n            }\n        }\n        books.add(new int[]{start, end});\n        return true;\n    }\n}",
                "python": "class MyCalendar:\n    def __init__(self):\n        self.books = []\n\n    def book(self, start: int, end: int) -> bool:\n        for s, e in self.books:\n            if max(start, s) < min(end, e):\n                return False\n        self.books.append((start, end))\n        return True"
            }
        },
        "optimal": {
            "idea": "TreeMap: floorKey(start) gives preceding booking, ceilingKey(start) gives next booking. Check overlap with only those two in O(log n).",
            "steps": [
                "TreeMap<Integer, Integer> map stores (start -> end).",
                "prev = map.floorKey(start); if prev != null && map.get(prev) > start return false.",
                "next = map.ceilingKey(start); if next != null && next < end return false.",
                "map.put(start, end); return true."
            ],
            "time": "O(log n) per book",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\npublic class MyCalendar {\n    private TreeMap<Integer, Integer> calendar = new TreeMap<>();\n    public MyCalendar() {}\n    public boolean book(int start, int end) {\n        Integer prev = calendar.floorKey(start);\n        if (prev != null && calendar.get(prev) > start) return false;\n        Integer next = calendar.ceilingKey(start);\n        if (next != null && next < end) return false;\n        calendar.put(start, end);\n        return true;\n    }\n}",
                "python": "import bisect\n\nclass MyCalendar:\n    def __init__(self):\n        self.starts = []\n        self.ends = []\n\n    def book(self, start: int, end: int) -> bool:\n        idx = bisect.bisect_right(self.starts, start)\n        if idx > 0 and self.ends[idx - 1] > start:\n            return False\n        if idx < len(self.starts) and self.starts[idx] < end:\n            return False\n        self.starts.insert(idx, start)\n        self.ends.insert(idx, end)\n        return True"
            }
        }
    },
    {
        "seq": 195,
        "whyNext": "Difference array (Prefix sweep line): increment passenger delta at trip.from, decrement at trip.to; running sum <= capacity.",
        "brute": {
            "idea": "Simulate passenger count kilometer by kilometer up to 1000.",
            "steps": [
                "Maintain array of passenger counts at every mile.",
                "For each trip, add passengers to range [from, to - 1].",
                "Verify no mile exceeds capacity."
            ],
            "time": "O(n * L)",
            "space": "O(1001)",
            "whySlow": "Updates every mile inside trip range individually.",
            "code": {
                "java": "class Solution {\n    public boolean carPooling(int[][] trips, int capacity) {\n        int[] miles = new int[1001];\n        for (int[] t : trips) {\n            for (int i = t[1]; i < t[2]; i++) {\n                miles[i] += t[0];\n                if (miles[i] > capacity) return false;\n            }\n        }\n        return true;\n    }\n}",
                "python": "class Solution:\n    def carPooling(self, trips: list[list[int]], capacity: int) -> bool:\n        miles = [0] * 1001\n        for num, start, end in trips:\n            for i in range(start, end):\n                miles[i] += num\n                if miles[i] > capacity:\n                    return False\n        return True"
            }
        },
        "optimal": {
            "idea": "Difference array: delta[trip.from] += num, delta[trip.to] -= num. Running sum gives current load in O(n + max_pos).",
            "steps": [
                "int[] diff = new int[1001];",
                "For trip: diff[trip[1]] += trip[0], diff[trip[2]] -= trip[0].",
                "Running sum load = 0; for d in diff: load += d; if load > capacity return false.",
                "Return true."
            ],
            "time": "O(n + 1001)",
            "space": "O(1001)",
            "code": {
                "java": "class Solution {\n    public boolean carPooling(int[][] trips, int capacity) {\n        int[] diff = new int[1001];\n        for (int[] t : trips) {\n            diff[t[1]] += t[0];\n            diff[t[2]] -= t[0];\n        }\n        int cur = 0;\n        for (int d : diff) {\n            cur += d;\n            if (cur > capacity) return false;\n        }\n        return true;\n    }\n}",
                "python": "class Solution:\n    def carPooling(self, trips: list[list[int]], capacity: int) -> bool:\n        diff = [0] * 1001\n        for num, start, end in trips:\n            diff[start] += num\n            diff[end] -= num\n        cur = 0\n        for d in diff:\n            cur += d\n            if cur > capacity:\n                return False\n        return True"
            }
        }
    },
    {
        "seq": 196,
        "whyNext": "Entry to Chapter 13 (Graph BFS/DFS): connected component pixel recoloring using 4-directional recursion.",
        "brute": {
            "idea": "BFS queue with explicit visited boolean matrix.",
            "steps": [
                "Encounter starting pixel.",
                "Queue up 4-directional neighbors of matching original color, keeping visited set."
            ],
            "time": "O(m * n)",
            "space": "O(m * n)",
            "whySlow": "Allocates extra visited matrix when in-place color change serves as visited check.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int[][] floodFill(int[][] image, int sr, int sc, int color) {\n        int orig = image[sr][sc];\n        if (orig == color) return image;\n        int m = image.length, n = image[0].length;\n        Queue<int[]> q = new LinkedList<>();\n        q.offer(new int[]{sr, sc});\n        image[sr][sc] = color;\n        int[][] dirs = {{1,0}, {-1,0}, {0,1}, {0,-1}};\n        while (!q.isEmpty()) {\n            int[] cur = q.poll();\n            for (int[] d : dirs) {\n                int r = cur[0] + d[0], c = cur[1] + d[1];\n                if (r >= 0 && r < m && c >= 0 && c < n && image[r][c] == orig) {\n                    image[r][c] = color;\n                    q.offer(new int[]{r, c});\n                }\n            }\n        }\n        return image;\n    }\n}",
                "python": "from collections import deque\n\nclass Solution:\n    def floodFill(self, image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:\n        orig = image[sr][sc]\n        if orig == color: return image\n        m, n = len(image), len(image[0])\n        q = deque([(sr, sc)])\n        image[sr][sc] = color\n        while q:\n            r, c = q.popleft()\n            for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):\n                nr, nc = r + dr, c + dc\n                if 0 <= nr < m and 0 <= nc < n and image[nr][nc] == orig:\n                    image[nr][nc] = color\n                    q.append((nr, nc))\n        return image"
            }
        },
        "optimal": {
            "idea": "In-place DFS: if image[sr][sc] == color return image; recolor cell to color and recurse on 4 neighbors with matching original color.",
            "steps": [
                "If image[sr][sc] == color return image.",
                "Define dfs(r, c, origColor, newColor).",
                "If out of bounds or image[r][c] != origColor return.",
                "image[r][c] = newColor.",
                "Recurse 4 directions."
            ],
            "time": "O(m * n)",
            "space": "O(m * n)",
            "code": {
                "java": "class Solution {\n    public int[][] floodFill(int[][] image, int sr, int sc, int color) {\n        if (image[sr][sc] != color) {\n            dfs(image, sr, sc, image[sr][sc], color);\n        }\n        return image;\n    }\n    private void dfs(int[][] img, int r, int c, int orig, int color) {\n        if (r < 0 || r >= img.length || c < 0 || c >= img[0].length || img[r][c] != orig) {\n            return;\n        }\n        img[r][c] = color;\n        dfs(img, r + 1, c, orig, color);\n        dfs(img, r - 1, c, orig, color);\n        dfs(img, r, c + 1, orig, color);\n        dfs(img, r, c - 1, orig, color);\n    }\n}",
                "python": "class Solution:\n    def floodFill(self, image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:\n        orig = image[sr][sc]\n        if orig == color:\n            return image\n        m, n = len(image), len(image[0])\n        def dfs(r: int, c: int):\n            if not (0 <= r < m and 0 <= c < n) or image[r][c] != orig:\n                return\n            image[r][c] = color\n            dfs(r + 1, c)\n            dfs(r - 1, c)\n            dfs(r, c + 1)\n            dfs(r, c - 1)\n        dfs(sr, sc)\n        return image"
            }
        }
    },
    {
        "seq": 197,
        "whyNext": "Connected components on grid: iterate cells; when '1' found, increment count and sink island ('1' -> '0') with DFS.",
        "brute": {
            "idea": "Disjoint Set Union (Union-Find) connecting adjacent '1' cells and counting root components.",
            "steps": [
                "Initialize DSU for m * n cells.",
                "For every '1' cell, union with adjacent right and down '1' cells.",
                "Count unique parents."
            ],
            "time": "O(m * n * alpha(mn))",
            "space": "O(m * n)",
            "whySlow": "Union-Find structure requires extra memory arrays compared to simple in-place DFS sinking.",
            "code": {
                "java": "class Solution {\n    public int numIslands(char[][] grid) {\n        int m = grid.length, n = grid[0].length;\n        int count = 0;\n        for (int i = 0; i < m; i++) {\n            for (int j = 0; j < n; j++) {\n                if (grid[i][j] == '1') {\n                    count++;\n                    dfs(grid, i, j);\n                }\n            }\n        }\n        return count;\n    }\n    private void dfs(char[][] grid, int r, int c) {\n        if (r < 0 || r >= grid.length || c < 0 || c >= grid[0].length || grid[r][c] != '1') return;\n        grid[r][c] = '0';\n        dfs(grid, r + 1, c);\n        dfs(grid, r - 1, c);\n        dfs(grid, r, c + 1);\n        dfs(grid, r, c - 1);\n    }\n}",
                "python": "class Solution:\n    def numIslands(self, grid: list[list[str]]) -> int:\n        m, n = len(grid), len(grid[0])\n        count = 0\n        def dfs(r, c):\n            if not (0 <= r < m and 0 <= c < n) or grid[r][c] != '1':\n                return\n            grid[r][c] = '0'\n            dfs(r + 1, c)\n            dfs(r - 1, c)\n            dfs(r, c + 1)\n            dfs(r, c - 1)\n        for i in range(m):\n            for j in range(n):\n                if grid[i][j] == '1':\n                    count += 1\n                    dfs(i, j)\n        return count"
            }
        },
        "optimal": {
            "idea": "In-place DFS sinking: when grid[r][c] == '1', increment island count and sink connected land by mutating '1' -> '0'.",
            "steps": [
                "Loop through all grid cells (r, c).",
                "If grid[r][c] == '1': increment count, call sink(r, c).",
                "sink(r, c): if out of bounds or grid[r][c] != '1' return.",
                "grid[r][c] = '0'; recurse on 4 cardinal neighbors."
            ],
            "time": "O(m * n)",
            "space": "O(m * n) recursion stack",
            "code": {
                "java": "class Solution {\n    public int numIslands(char[][] grid) {\n        int count = 0;\n        int m = grid.length, n = grid[0].length;\n        for (int i = 0; i < m; i++) {\n            for (int j = 0; j < n; j++) {\n                if (grid[i][j] == '1') {\n                    count++;\n                    sink(grid, i, j, m, n);\n                }\n            }\n        }\n        return count;\n    }\n    private void sink(char[][] grid, int r, int c, int m, int n) {\n        if (r < 0 || r >= m || c < 0 || c >= n || grid[r][c] != '1') return;\n        grid[r][c] = '0';\n        sink(grid, r + 1, c, m, n);\n        sink(grid, r - 1, c, m, n);\n        sink(grid, r, c + 1, m, n);\n        sink(grid, r, c - 1, m, n);\n    }\n}",
                "python": "class Solution:\n    def numIslands(self, grid: list[list[str]]) -> int:\n        m, n = len(grid), len(grid[0])\n        count = 0\n        def sink(r: int, c: int):\n            if not (0 <= r < m and 0 <= c < n) or grid[r][c] != '1':\n                return\n            grid[r][c] = '0'\n            sink(r + 1, c)\n            sink(r - 1, c)\n            sink(r, c + 1)\n            sink(r, c - 1)\n        for i in range(m):\n            for j in range(n):\n                if grid[i][j] == '1':\n                    count += 1\n                    sink(i, j)\n        return count"
            }
        }
    },
    {
        "seq": 198,
        "whyNext": "Builds on Number of Islands: return area 1 + sum of areas of 4 cardinal neighbors; track global max area.",
        "brute": {
            "idea": "BFS queue for each unvisited 1 cell, keeping a visited set.",
            "steps": [
                "Run BFS from each 1 cell counting popped nodes.",
                "Track maximum area."
            ],
            "time": "O(m * n)",
            "space": "O(m * n)",
            "whySlow": "Allocates queue and sets instead of DFS returning 1 + children areas.",
            "code": {
                "java": "class Solution {\n    public int maxAreaOfIsland(int[][] grid) {\n        int max = 0;\n        int m = grid.length, n = grid[0].length;\n        for (int i = 0; i < m; i++) {\n            for (int j = 0; j < n; j++) {\n                if (grid[i][j] == 1) {\n                    max = Math.max(max, area(grid, i, j));\n                }\n            }\n        }\n        return max;\n    }\n    private int area(int[][] grid, int r, int c) {\n        if (r < 0 || r >= grid.length || c < 0 || c >= grid[0].length || grid[r][c] != 1) return 0;\n        grid[r][c] = 0;\n        return 1 + area(grid, r + 1, c) + area(grid, r - 1, c) + area(grid, r, c + 1) + area(grid, r, c - 1);\n    }\n}",
                "python": "class Solution:\n    def maxAreaOfIsland(self, grid: list[list[int]]) -> int:\n        m, n = len(grid), len(grid[0])\n        max_a = 0\n        def area(r, c):\n            if not (0 <= r < m and 0 <= c < n) or grid[r][c] != 1:\n                return 0\n            grid[r][c] = 0\n            return 1 + area(r + 1, c) + area(r - 1, c) + area(r, c + 1) + area(r, c - 1)\n        for i in range(m):\n            for j in range(n):\n                if grid[i][j] == 1:\n                    max_a = max(max_a, area(i, j))\n        return max_a"
            }
        },
        "optimal": {
            "idea": "In-place DFS: area = 1 + dfs(up) + dfs(down) + dfs(left) + dfs(right); mark grid[r][c] = 0 to prevent revisiting.",
            "steps": [
                "maxArea = 0.",
                "For each cell (r, c): if grid[r][c] == 1, maxArea = max(maxArea, getArea(r, c)).",
                "getArea(r, c): if out of bounds or grid[r][c] != 1 return 0.",
                "grid[r][c] = 0; return 1 + 4 neighbor calls."
            ],
            "time": "O(m * n)",
            "space": "O(m * n)",
            "code": {
                "java": "class Solution {\n    public int maxAreaOfIsland(int[][] grid) {\n        int maxArea = 0;\n        int m = grid.length, n = grid[0].length;\n        for (int i = 0; i < m; i++) {\n            for (int j = 0; j < n; j++) {\n                if (grid[i][j] == 1) {\n                    maxArea = Math.max(maxArea, dfs(grid, i, j, m, n));\n                }\n            }\n        }\n        return maxArea;\n    }\n    private int dfs(int[][] grid, int r, int c, int m, int n) {\n        if (r < 0 || r >= m || c < 0 || c >= n || grid[r][c] != 1) return 0;\n        grid[r][c] = 0;\n        return 1 + dfs(grid, r + 1, c, m, n) + dfs(grid, r - 1, c, m, n) +\n                   dfs(grid, r, c + 1, m, n) + dfs(grid, r, c - 1, m, n);\n    }\n}",
                "python": "class Solution:\n    def maxAreaOfIsland(self, grid: list[list[int]]) -> int:\n        m, n = len(grid), len(grid[0])\n        max_area = 0\n        def dfs(r: int, c: int) -> int:\n            if not (0 <= r < m and 0 <= c < n) or grid[r][c] != 1:\n                return 0\n            grid[r][c] = 0\n            return 1 + dfs(r + 1, c) + dfs(r - 1, c) + dfs(r, c + 1) + dfs(r, c - 1)\n        for i in range(m):\n            for j in range(n):\n                if grid[i][j] == 1:\n                    max_area = max(max_area, dfs(i, j))\n        return max_area"
            }
        }
    },
    {
        "seq": 199,
        "whyNext": "Perimeter geometry: each land cell adds 4 edges minus 2 for every adjacent neighbor that is also land.",
        "brute": {
            "idea": "For every land cell, check all 4 neighbors: if neighbor is water or out of bounds, add 1 to perimeter.",
            "steps": [
                "Iterate over every cell.",
                "If cell == 1, check all 4 directions; count borders."
            ],
            "time": "O(m * n)",
            "space": "O(1)",
            "whySlow": "Checks 4 directions for every land cell instead of counting shared edges in single forward pass.",
            "code": {
                "java": "class Solution {\n    public int islandPerimeter(int[][] grid) {\n        int p = 0;\n        int m = grid.length, n = grid[0].length;\n        for (int i = 0; i < m; i++) {\n            for (int j = 0; j < n; j++) {\n                if (grid[i][j] == 1) {\n                    if (i == 0 || grid[i - 1][j] == 0) p++;\n                    if (i == m - 1 || grid[i + 1][j] == 0) p++;\n                    if (j == 0 || grid[i][j - 1] == 0) p++;\n                    if (j == n - 1 || grid[i][j + 1] == 0) p++;\n                }\n            }\n        }\n        return p;\n    }\n}",
                "python": "class Solution:\n    def islandPerimeter(self, grid: list[list[int]]) -> int:\n        p = 0\n        m, n = len(grid), len(grid[0])\n        for i in range(m):\n            for j in range(n):\n                if grid[i][j] == 1:\n                    if i == 0 or grid[i - 1][j] == 0: p += 1\n                    if i == m - 1 or grid[i + 1][j] == 0: p += 1\n                    if j == 0 or grid[i][j - 1] == 0: p += 1\n                    if j == n - 1 or grid[i][j + 1] == 0: p += 1\n        return p"
            }
        },
        "optimal": {
            "idea": "Math formula: perimeter = 4 * land - 2 * shared_edges (only check up and left neighbors to count shared edges).",
            "steps": [
                "land = 0, shared = 0.",
                "For each (r, c): if grid[r][c] == 1: land++.",
                "If r > 0 && grid[r - 1][c] == 1 shared++.",
                "If c > 0 && grid[r][c - 1] == 1 shared++.",
                "Return 4 * land - 2 * shared."
            ],
            "time": "O(m * n)",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public int islandPerimeter(int[][] grid) {\n        int land = 0, shared = 0;\n        int m = grid.length, n = grid[0].length;\n        for (int i = 0; i < m; i++) {\n            for (int j = 0; j < n; j++) {\n                if (grid[i][j] == 1) {\n                    land++;\n                    if (i > 0 && grid[i - 1][j] == 1) shared++;\n                    if (j > 0 && grid[i][j - 1] == 1) shared++;\n                }\n            }\n        }\n        return 4 * land - 2 * shared;\n    }\n}",
                "python": "class Solution:\n    def islandPerimeter(self, grid: list[list[int]]) -> int:\n        land = 0\n        shared = 0\n        m, n = len(grid), len(grid[0])\n        for i in range(m):\n            for j in range(n):\n                if grid[i][j] == 1:\n                    land += 1\n                    if i > 0 and grid[i - 1][j] == 1: shared += 1\n                    if j > 0 and grid[i][j - 1] == 1: shared += 1\n        return 4 * land - 2 * shared"
            }
        }
    },
    {
        "seq": 200,
        "whyNext": "Boundary DFS: any 'O' connected to the grid boundary cannot be surrounded; mark boundary 'O's as safe, capture the rest.",
        "brute": {
            "idea": "From every 'O' cell, run DFS to detect if any path reaches the boundary; flip only surrounded components.",
            "steps": [
                "For each 'O', launch search.",
                "If boundary is reached, keep 'O'.",
                "If trapped, flip all to 'X'."
            ],
            "time": "O(m * n)",
            "space": "O(m * n)",
            "whySlow": "Searching outward from every interior cell repeatedly is complex compared to searching inward from boundary.",
            "code": {
                "java": "class Solution {\n    public void solve(char[][] board) {\n        int m = board.length, n = board[0].length;\n        for (int i = 0; i < m; i++) {\n            dfs(board, i, 0);\n            dfs(board, i, n - 1);\n        }\n        for (int j = 0; j < n; j++) {\n            dfs(board, 0, j);\n            dfs(board, m - 1, j);\n        }\n        for (int i = 0; i < m; i++) {\n            for (int j = 0; j < n; j++) {\n                if (board[i][j] == 'O') board[i][j] = 'X';\n                else if (board[i][j] == '#') board[i][j] = 'O';\n            }\n        }\n    }\n    private void dfs(char[][] b, int r, int c) {\n        if (r < 0 || r >= b.length || c < 0 || c >= b[0].length || b[r][c] != 'O') return;\n        b[r][c] = '#';\n        dfs(b, r + 1, c);\n        dfs(b, r - 1, c);\n        dfs(b, r, c + 1);\n        dfs(b, r, c - 1);\n    }\n}",
                "python": "class Solution:\n    def solve(self, board: list[list[str]]) -> None:\n        m, n = len(board), len(board[0])\n        def dfs(r, c):\n            if not (0 <= r < m and 0 <= c < n) or board[r][c] != 'O':\n                return\n            board[r][c] = '#'\n            dfs(r + 1, c)\n            dfs(r - 1, c)\n            dfs(r, c + 1)\n            dfs(r, c - 1)\n        for i in range(m):\n            dfs(i, 0)\n            dfs(i, n - 1)\n        for j in range(n):\n            dfs(0, j)\n            dfs(m - 1, j)\n        for i in range(m):\n            for j in range(n):\n                if board[i][j] == 'O':\n                    board[i][j] = 'X'\n                elif board[i][j] == '#':\n                    board[i][j] = 'O'"
            }
        },
        "optimal": {
            "idea": "Boundary flood fill: run DFS from all 'O's on the 4 borders marking them as '#'. Finally, flip all remaining 'O' to 'X' and '#' back to 'O'.",
            "steps": [
                "Run DFS along all border cells (first/last row and first/last col): mark connected 'O' -> '#'.",
                "Iterate over whole board:",
                "If cell == 'O', flip to 'X' (captured).",
                "If cell == '#', restore to 'O' (safe)."
            ],
            "time": "O(m * n)",
            "space": "O(m * n)",
            "code": {
                "java": "class Solution {\n    public void solve(char[][] board) {\n        int m = board.length, n = board[0].length;\n        for (int i = 0; i < m; i++) {\n            if (board[i][0] == 'O') dfs(board, i, 0, m, n);\n            if (board[i][n - 1] == 'O') dfs(board, i, n - 1, m, n);\n        }\n        for (int j = 0; j < n; j++) {\n            if (board[0][j] == 'O') dfs(board, 0, j, m, n);\n            if (board[m - 1][j] == 'O') dfs(board, m - 1, j, m, n);\n        }\n        for (int i = 0; i < m; i++) {\n            for (int j = 0; j < n; j++) {\n                if (board[i][j] == 'O') board[i][j] = 'X';\n                else if (board[i][j] == '#') board[i][j] = 'O';\n            }\n        }\n    }\n    private void dfs(char[][] board, int r, int c, int m, int n) {\n        if (r < 0 || r >= m || c < 0 || c >= n || board[r][c] != 'O') return;\n        board[r][c] = '#';\n        dfs(board, r + 1, c, m, n);\n        dfs(board, r - 1, c, m, n);\n        dfs(board, r, c + 1, m, n);\n        dfs(board, r, c - 1, m, n);\n    }\n}",
                "python": "class Solution:\n    def solve(self, board: list[list[str]]) -> None:\n        m, n = len(board), len(board[0])\n        def dfs(r: int, c: int):\n            if not (0 <= r < m and 0 <= c < n) or board[r][c] != 'O':\n                return\n            board[r][c] = '#'\n            dfs(r + 1, c)\n            dfs(r - 1, c)\n            dfs(r, c + 1)\n            dfs(r, c - 1)\n        for i in range(m):\n            if board[i][0] == 'O': dfs(i, 0)\n            if board[i][n - 1] == 'O': dfs(i, n - 1)\n        for j in range(n):\n            if board[0][j] == 'O': dfs(0, j)\n            if board[m - 1][j] == 'O': dfs(m - 1, j)\n        for i in range(m):\n            for j in range(n):\n                if board[i][j] == 'O':\n                    board[i][j] = 'X'\n                elif board[i][j] == '#':\n                    board[i][j] = 'O'"
            }
        }
    }
]

# scripts/gen_batch_08.py
import json

batch_8 = [
    # 176: Maximum Subarray
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
                "java": """class Solution {
    public int maxSubArray(int[] nums) {
        int maxSum = Integer.MIN_VALUE;
        for (int i = 0; i < nums.length; i++) {
            int cur = 0;
            for (int j = i; j < nums.length; j++) {
                cur += nums[j];
                maxSum = Math.max(maxSum, cur);
            }
        }
        return maxSum;
    }
}""",
                "python": """class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        max_sum = float('-inf')
        for i in range(len(nums)):
            cur = 0
            for j in range(i, len(nums)):
                cur += nums[j]
                max_sum = max(max_sum, cur)
        return max_sum"""
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
                "java": """class Solution {
    public int maxSubArray(int[] nums) {
        int maxSum = nums[0];
        int curSum = 0;
        for (int x : nums) {
            curSum = Math.max(x, curSum + x);
            maxSum = Math.max(maxSum, curSum);
        }
        return maxSum;
    }
}""",
                "python": """class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        max_sum = nums[0]
        cur_sum = 0
        for x in nums:
            cur_sum = max(x, cur_sum + x)
            max_sum = max(max_sum, cur_sum)
        return max_sum"""
            }
        }
    },
    # 177: Maximum Sum Circular Subarray
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
                "java": """class Solution {
    public int maxSubarraySumCircular(int[] nums) {
        int n = nums.length;
        int max = Integer.MIN_VALUE;
        for (int i = 0; i < n; i++) {
            int cur = 0;
            for (int k = 0; k < n; k++) {
                cur += nums[(i + k) % n];
                max = Math.max(max, cur);
            }
        }
        return max;
    }
}""",
                "python": """class Solution:
    def maxSubarraySumCircular(self, nums: list[int]) -> int:
        n = len(nums)
        ans = float('-inf')
        for i in range(n):
            cur = 0
            for k in range(n):
                cur += nums[(i + k) % n]
                ans = max(ans, cur)
        return ans"""
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
                "java": """class Solution {
    public int maxSubarraySumCircular(int[] nums) {
        int total = 0, curMax = 0, maxKadane = nums[0];
        int curMin = 0, minKadane = nums[0];
        for (int x : nums) {
            curMax = Math.max(x, curMax + x);
            maxKadane = Math.max(maxKadane, curMax);
            curMin = Math.min(x, curMin + x);
            minKadane = Math.min(minKadane, curMin);
            total += x;
        }
        return maxKadane > 0 ? Math.max(maxKadane, total - minKadane) : maxKadane;
    }
}""",
                "python": """class Solution:
    def maxSubarraySumCircular(self, nums: list[int]) -> int:
        total = 0
        cur_max = 0
        max_kadane = nums[0]
        cur_min = 0
        min_kadane = nums[0]
        for x in nums:
            cur_max = max(x, cur_max + x)
            max_kadane = max(max_kadane, cur_max)
            cur_min = min(x, cur_min + x)
            min_kadane = min(min_kadane, cur_min)
            total += x
        return max(max_kadane, total - min_kadane) if max_kadane > 0 else max_kadane"""
            }
        }
    },
    # 178: Jump Game
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
                "java": """class Solution {
    public boolean canJump(int[] nums) {
        return canJumpFrom(0, nums);
    }
    private boolean canJumpFrom(int pos, int[] nums) {
        if (pos >= nums.length - 1) return true;
        int furthest = Math.min(pos + nums[pos], nums.length - 1);
        for (int next = furthest; next > pos; next--) {
            if (canJumpFrom(next, nums)) return true;
        }
        return false;
    }
}""",
                "python": """class Solution:
    def canJump(self, nums: list[int]) -> bool:
        def dfs(pos):
            if pos >= len(nums) - 1: return True
            furthest = min(pos + nums[pos], len(nums) - 1)
            for nxt in range(furthest, pos, -1):
                if dfs(nxt): return True
            return False
        return dfs(0)"""
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
                "java": """class Solution {
    public boolean canJump(int[] nums) {
        int maxReach = 0;
        for (int i = 0; i < nums.length; i++) {
            if (i > maxReach) return false;
            maxReach = Math.max(maxReach, i + nums[i]);
            if (maxReach >= nums.length - 1) return true;
        }
        return true;
    }
}""",
                "python": """class Solution:
    def canJump(self, nums: list[int]) -> bool:
        max_reach = 0
        for i, jump in enumerate(nums):
            if i > max_reach:
                return False
            max_reach = max(max_reach, i + jump)
            if max_reach >= len(nums) - 1:
                return True
        return True"""
            }
        }
    },
    # 179: Jump Game II
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
                "java": """import java.util.*;
class Solution {
    public int jump(int[] nums) {
        int n = nums.length;
        int[] dp = new int[n];
        Arrays.fill(dp, 100000);
        dp[0] = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 1; j <= nums[i] && i + j < n; j++) {
                dp[i + j] = Math.min(dp[i + j], dp[i] + 1);
            }
        }
        return dp[n - 1];
    }
}""",
                "python": """class Solution:
    def jump(self, nums: list[int]) -> int:
        n = len(nums)
        dp = [float('inf')] * n
        dp[0] = 0
        for i in range(n):
            for j in range(1, nums[i] + 1):
                if i + j < n:
                    dp[i + j] = min(dp[i + j], dp[i] + 1)
        return dp[-1]"""
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
                "java": """class Solution {
    public int jump(int[] nums) {
        int jumps = 0, curEnd = 0, curFarthest = 0;
        for (int i = 0; i < nums.length - 1; i++) {
            curFarthest = Math.max(curFarthest, i + nums[i]);
            if (i == curEnd) {
                jumps++;
                curEnd = curFarthest;
            }
        }
        return jumps;
    }
}""",
                "python": """class Solution:
    def jump(self, nums: list[int]) -> int:
        jumps = 0
        cur_end = 0
        cur_farthest = 0
        for i in range(len(nums) - 1):
            cur_farthest = max(cur_farthest, i + nums[i])
            if i == cur_end:
                jumps += 1
                cur_end = cur_farthest
        return jumps"""
            }
        }
    },
    # 180: Gas Station
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
                "java": """class Solution {
    public int canCompleteCircuit(int[] gas, int[] cost) {
        int n = gas.length;
        for (int start = 0; start < n; start++) {
            int tank = 0;
            boolean ok = true;
            for (int k = 0; k < n; k++) {
                int cur = (start + k) % n;
                tank += gas[cur] - cost[cur];
                if (tank < 0) {
                    ok = false;
                    break;
                }
            }
            if (ok) return start;
        }
        return -1;
    }
}""",
                "python": """class Solution:
    def canCompleteCircuit(self, gas: list[int], cost: list[int]) -> int:
        n = len(gas)
        for start in range(n):
            tank = 0
            ok = True
            for k in range(n):
                cur = (start + k) % n
                tank += gas[cur] - cost[cur]
                if tank < 0:
                    ok = False
                    break
            if ok: return start
        return -1"""
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
                "java": """class Solution {
    public int canCompleteCircuit(int[] gas, int[] cost) {
        int total = 0, cur = 0, start = 0;
        for (int i = 0; i < gas.length; i++) {
            int diff = gas[i] - cost[i];
            total += diff;
            cur += diff;
            if (cur < 0) {
                start = i + 1;
                cur = 0;
            }
        }
        return total >= 0 ? start : -1;
    }
}""",
                "python": """class Solution:
    def canCompleteCircuit(self, gas: list[int], cost: list[int]) -> int:
        total = 0
        cur = 0
        start = 0
        for i in range(len(gas)):
            diff = gas[i] - cost[i]
            total += diff
            cur += diff
            if cur < 0:
                start = i + 1
                cur = 0
        return start if total >= 0 else -1"""
            }
        }
    },
    # 181: Candy
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
                "java": """import java.util.*;
class Solution {
    public int candy(int[] ratings) {
        int n = ratings.length;
        int[] candies = new int[n];
        Arrays.fill(candies, 1);
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int i = 0; i < n; i++) {
                if (i > 0 && ratings[i] > ratings[i - 1] && candies[i] <= candies[i - 1]) {
                    candies[i] = candies[i - 1] + 1;
                    changed = true;
                }
                if (i < n - 1 && ratings[i] > ratings[i + 1] && candies[i] <= candies[i + 1]) {
                    candies[i] = candies[i + 1] + 1;
                    changed = true;
                }
            }
        }
        int sum = 0;
        for (int c : candies) sum += c;
        return sum;
    }
}""",
                "python": """class Solution:
    def candy(self, ratings: list[int]) -> int:
        n = len(ratings)
        candies = [1] * n
        changed = True
        while changed:
            changed = False
            for i in range(n):
                if i > 0 and ratings[i] > ratings[i - 1] and candies[i] <= candies[i - 1]:
                    candies[i] = candies[i - 1] + 1
                    changed = True
                if i < n - 1 and ratings[i] > ratings[i + 1] and candies[i] <= candies[i + 1]:
                    candies[i] = candies[i + 1] + 1
                    changed = True
        return sum(candies)"""
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
                "java": """import java.util.*;
class Solution {
    public int candy(int[] ratings) {
        int n = ratings.length;
        int[] candies = new int[n];
        Arrays.fill(candies, 1);
        for (int i = 1; i < n; i++) {
            if (ratings[i] > ratings[i - 1]) {
                candies[i] = candies[i - 1] + 1;
            }
        }
        for (int i = n - 2; i >= 0; i--) {
            if (ratings[i] > ratings[i + 1]) {
                candies[i] = Math.max(candies[i], candies[i + 1] + 1);
            }
        }
        int sum = 0;
        for (int c : candies) sum += c;
        return sum;
    }
}""",
                "python": """class Solution:
    def candy(self, ratings: list[int]) -> int:
        n = len(ratings)
        candies = [1] * n
        for i in range(1, n):
            if ratings[i] > ratings[i - 1]:
                candies[i] = candies[i - 1] + 1
        for i in range(n - 2, -1, -1):
            if ratings[i] > ratings[i + 1]:
                candies[i] = max(candies[i], candies[i + 1] + 1)
        return sum(candies)"""
            }
        }
    },
    # 182: Partition Labels
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
                "java": """import java.util.*;
class Solution {
    public List<Integer> partitionLabels(String s) {
        List<Integer> res = new ArrayList<>();
        int i = 0;
        while (i < s.length()) {
            int end = s.lastIndexOf(s.charAt(i));
            for (int j = i; j <= end; j++) {
                end = Math.max(end, s.lastIndexOf(s.charAt(j)));
            }
            res.add(end - i + 1);
            i = end + 1;
        }
        return res;
    }
}""",
                "python": """class Solution:
    def partitionLabels(self, s: str) -> list[int]:
        res = []
        i = 0
        while i < len(s):
            end = s.rfind(s[i])
            j = i
            while j <= end:
                end = max(end, s.rfind(s[j]))
                j += 1
            res.append(end - i + 1)
            i = end + 1
        return res"""
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
                "java": """import java.util.*;
class Solution {
    public List<Integer> partitionLabels(String s) {
        int[] last = new int[26];
        for (int i = 0; i < s.length(); i++) {
            last[s.charAt(i) - 'a'] = i;
        }
        List<Integer> res = new ArrayList<>();
        int start = 0, end = 0;
        for (int i = 0; i < s.length(); i++) {
            end = Math.max(end, last[s.charAt(i) - 'a']);
            if (i == end) {
                res.add(end - start + 1);
                start = i + 1;
            }
        }
        return res;
    }
}""",
                "python": """class Solution:
    def partitionLabels(self, s: str) -> list[int]:
        last = {c: i for i, c in enumerate(s)}
        res = []
        start = end = 0
        for i, c in enumerate(s):
            end = max(end, last[c])
            if i == end:
                res.append(end - start + 1)
                start = i + 1
        return res"""
            }
        }
    },
    # 183: Remove Duplicate Letters
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
                "java": """class Solution {
    public String removeDuplicateLetters(String s) {
        int[] count = new int[26];
        for (char c : s.toCharArray()) count[c - 'a']++;
        int pos = 0;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) < s.charAt(pos)) pos = i;
            if (--count[s.charAt(i) - 'a'] == 0) break;
        }
        if (s.isEmpty()) return "";
        char c = s.charAt(pos);
        return c + removeDuplicateLetters(s.substring(pos + 1).replaceAll("" + c, ""));
    }
}""",
                "python": """class Solution:
    def removeDuplicateLetters(self, s: str) -> str:
        from collections import Counter
        count = Counter(s)
        pos = 0
        for i, c in enumerate(s):
            if c < s[pos]: pos = i
            count[c] -= 1
            if count[c] == 0: break
        return s[pos] + self.removeDuplicateLetters(s[pos+1:].replace(s[pos], "")) if s else "" """
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
                "java": """import java.util.*;
class Solution {
    public String removeDuplicateLetters(String s) {
        int[] last = new int[26];
        for (int i = 0; i < s.length(); i++) {
            last[s.charAt(i) - 'a'] = i;
        }
        boolean[] inStack = new boolean[26];
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            int idx = c - 'a';
            if (inStack[idx]) continue;
            while (sb.length() > 0 && sb.charAt(sb.length() - 1) > c && last[sb.charAt(sb.length() - 1) - 'a'] > i) {
                inStack[sb.charAt(sb.length() - 1) - 'a'] = false;
                sb.deleteCharAt(sb.length() - 1);
            }
            sb.append(c);
            inStack[idx] = true;
        }
        return sb.toString();
    }
}""",
                "python": """class Solution:
    def removeDuplicateLetters(self, s: str) -> str:
        last = {c: i for i, c in enumerate(s)}
        stack = []
        in_stack = set()
        for i, c in enumerate(s):
            if c in in_stack:
                continue
            while stack and stack[-1] > c and last[stack[-1]] > i:
                in_stack.remove(stack.pop())
            stack.append(c)
            in_stack.add(c)
        return "".join(stack)"""
            }
        }
    },
    # 184: Patching Array
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
                "java": """class Solution {
    public int minPatches(int[] nums, int n) {
        long miss = 1;
        int patches = 0, i = 0;
        while (miss <= n) {
            if (i < nums.length && nums[i] <= miss) {
                miss += nums[i++];
            } else {
                miss += miss;
                patches++;
            }
        }
        return patches;
    }
}""",
                "python": """class Solution:
    def minPatches(self, nums: list[int], n: int) -> int:
        miss = 1
        patches = 0
        i = 0
        while miss <= n:
            if i < len(nums) and nums[i] <= miss:
                miss += nums[i]
                i += 1
            else:
                miss += miss
                patches += 1
        return patches"""
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
                "java": """class Solution {
    public int minPatches(int[] nums, int n) {
        long miss = 1;
        int patches = 0, i = 0;
        while (miss <= n) {
            if (i < nums.length && nums[i] <= miss) {
                miss += nums[i++];
            } else {
                miss += miss;
                patches++;
            }
        }
        return patches;
    }
}""",
                "python": """class Solution:
    def minPatches(self, nums: list[int], n: int) -> int:
        miss = 1
        patches = 0
        i = 0
        while miss <= n:
            if i < len(nums) and nums[i] <= miss:
                miss += nums[i]
                i += 1
            else:
                miss += miss
                patches += 1
        return patches"""
            }
        }
    },
    # 185: Two City Scheduling
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
                "java": """class Solution {
    public int twoCitySchedCost(int[][] costs) {
        return dfs(costs, 0, 0, 0, costs.length / 2);
    }
    private int dfs(int[][] costs, int idx, int a, int b, int n) {
        if (idx == costs.length) return 0;
        int chooseA = Integer.MAX_VALUE, chooseB = Integer.MAX_VALUE;
        if (a < n) chooseA = costs[idx][0] + dfs(costs, idx + 1, a + 1, b, n);
        if (b < n) chooseB = costs[idx][1] + dfs(costs, idx + 1, a, b + 1, n);
        return Math.min(chooseA, chooseB);
    }
}""",
                "python": """class Solution:
    def twoCitySchedCost(self, costs: list[list[int]]) -> int:
        n = len(costs) // 2
        def dfs(i, a, b):
            if i == len(costs): return 0
            res = float('inf')
            if a < n:
                res = min(res, costs[i][0] + dfs(i + 1, a + 1, b))
            if b < n:
                res = min(res, costs[i][1] + dfs(i + 1, a, b + 1))
            return res
        return dfs(0, 0, 0)"""
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
                "java": """import java.util.*;
class Solution {
    public int twoCitySchedCost(int[][] costs) {
        Arrays.sort(costs, (a, b) -> (a[0] - a[1]) - (b[0] - b[1]));
        int total = 0;
        int n = costs.length / 2;
        for (int i = 0; i < n; i++) total += costs[i][0];
        for (int i = n; i < 2 * n; i++) total += costs[i][1];
        return total;
    }
}""",
                "python": """class Solution:
    def twoCitySchedCost(self, costs: list[list[int]]) -> int:
        costs.sort(key=lambda x: x[0] - x[1])
        n = len(costs) // 2
        return sum(costs[i][0] for i in range(n)) + sum(costs[i][1] for i in range(n, 2 * n))"""
            }
        }
    },
    # 186: Queue Reconstruction by Height
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
                "java": """import java.util.*;
class Solution {
    public int[][] reconstructQueue(int[][] people) {
        Arrays.sort(people, (a, b) -> a[0] != b[0] ? b[0] - a[0] : a[1] - b[1]);
        List<int[]> list = new LinkedList<>();
        for (int[] p : people) {
            list.add(p[1], p);
        }
        return list.toArray(new int[people.length][]);
    }
}""",
                "python": """class Solution:
    def reconstructQueue(self, people: list[list[int]]) -> list[list[int]]:
        people.sort(key=lambda p: (-p[0], p[1]))
        res = []
        for p in people:
            res.insert(p[1], p)
        return res"""
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
                "java": """import java.util.*;
class Solution {
    public int[][] reconstructQueue(int[][] people) {
        Arrays.sort(people, (a, b) -> a[0] != b[0] ? b[0] - a[0] : a[1] - b[1]);
        List<int[]> res = new LinkedList<>();
        for (int[] p : people) {
            res.add(p[1], p);
        }
        return res.toArray(new int[people.length][]);
    }
}""",
                "python": """class Solution:
    def reconstructQueue(self, people: list[list[int]]) -> list[list[int]]:
        people.sort(key=lambda x: (-x[0], x[1]))
        res = []
        for p in people:
            res.insert(p[1], p)
        return res"""
            }
        }
    },
    # 187: Valid Parenthesis String
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
                "java": """class Solution {
    public boolean checkValidString(String s) {
        return dfs(s, 0, 0);
    }
    private boolean dfs(String s, int idx, int open) {
        if (open < 0) return false;
        if (idx == s.length()) return open == 0;
        char c = s.charAt(idx);
        if (c == '(') return dfs(s, idx + 1, open + 1);
        if (c == ')') return dfs(s, idx + 1, open - 1);
        return dfs(s, idx + 1, open + 1) || dfs(s, idx + 1, open - 1) || dfs(s, idx + 1, open);
    }
}""",
                "python": """class Solution:
    def checkValidString(self, s: str) -> bool:
        def dfs(i, open_cnt):
            if open_cnt < 0: return False
            if i == len(s): return open_cnt == 0
            if s[i] == '(': return dfs(i + 1, open_cnt + 1)
            if s[i] == ')': return dfs(i + 1, open_cnt - 1)
            return dfs(i + 1, open_cnt + 1) or dfs(i + 1, open_cnt - 1) or dfs(i + 1, open_cnt)
        return dfs(0, 0)"""
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
                "java": """class Solution {
    public boolean checkValidString(String s) {
        int cmin = 0, cmax = 0;
        for (char c : s.toCharArray()) {
            if (c == '(') {
                cmin++;
                cmax++;
            } else if (c == ')') {
                cmin--;
                cmax--;
            } else {
                cmin--;
                cmax++;
            }
            if (cmax < 0) return false;
            cmin = Math.max(0, cmin);
        }
        return cmin == 0;
    }
}""",
                "python": """class Solution:
    def checkValidString(self, s: str) -> bool:
        cmin = cmax = 0
        for c in s:
            if c == '(':
                cmin += 1
                cmax += 1
            elif c == ')':
                cmin -= 1
                cmax -= 1
            else:
                cmin -= 1
                cmax += 1
            if cmax < 0:
                return False
            cmin = max(0, cmin)
        return cmin == 0"""
            }
        }
    },
    # 188: Merge Intervals
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
                "java": """import java.util.*;
class Solution {
    public int[][] merge(int[][] intervals) {
        Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));
        List<int[]> merged = new ArrayList<>();
        for (int[] interval : intervals) {
            if (merged.isEmpty() || merged.get(merged.size() - 1)[1] < interval[0]) {
                merged.add(interval);
            } else {
                merged.get(merged.size() - 1)[1] = Math.max(merged.get(merged.size() - 1)[1], interval[1]);
            }
        }
        return merged.toArray(new int[merged.size()][]);
    }
}""",
                "python": """class Solution:
    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        intervals.sort(key=lambda x: x[0])
        merged = []
        for start, end in intervals:
            if not merged or merged[-1][1] < start:
                merged.append([start, end])
            else:
                merged[-1][1] = max(merged[-1][1], end)
        return merged"""
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
                "java": """import java.util.*;
class Solution {
    public int[][] merge(int[][] intervals) {
        Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));
        List<int[]> res = new ArrayList<>();
        for (int[] cur : intervals) {
            if (res.isEmpty() || res.get(res.size() - 1)[1] < cur[0]) {
                res.add(cur);
            } else {
                res.get(res.size() - 1)[1] = Math.max(res.get(res.size() - 1)[1], cur[1]);
            }
        }
        return res.toArray(new int[res.size()][]);
    }
}""",
                "python": """class Solution:
    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        intervals.sort(key=lambda x: x[0])
        res = []
        for cur in intervals:
            if not res or res[-1][1] < cur[0]:
                res.append(cur)
            else:
                res[-1][1] = max(res[-1][1], cur[1])
        return res"""
            }
        }
    },
    # 189: Insert Interval
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
                "java": """import java.util.*;
class Solution {
    public int[][] insert(int[][] intervals, int[] newInterval) {
        List<int[]> list = new ArrayList<>(Arrays.asList(intervals));
        list.add(newInterval);
        list.sort(Comparator.comparingInt(a -> a[0]));
        List<int[]> merged = new ArrayList<>();
        for (int[] cur : list) {
            if (merged.isEmpty() || merged.get(merged.size() - 1)[1] < cur[0]) {
                merged.add(cur);
            } else {
                merged.get(merged.size() - 1)[1] = Math.max(merged.get(merged.size() - 1)[1], cur[1]);
            }
        }
        return merged.toArray(new int[merged.size()][]);
    }
}""",
                "python": """class Solution:
    def insert(self, intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:
        intervals.append(newInterval)
        intervals.sort(key=lambda x: x[0])
        res = []
        for cur in intervals:
            if not res or res[-1][1] < cur[0]:
                res.append(cur)
            else:
                res[-1][1] = max(res[-1][1], cur[1])
        return res"""
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
                "java": """import java.util.*;
class Solution {
    public int[][] insert(int[][] intervals, int[] newInterval) {
        List<int[]> res = new ArrayList<>();
        int i = 0, n = intervals.length;
        while (i < n && intervals[i][1] < newInterval[0]) {
            res.add(intervals[i++]);
        }
        while (i < n && intervals[i][0] <= newInterval[1]) {
            newInterval[0] = Math.min(newInterval[0], intervals[i][0]);
            newInterval[1] = Math.max(newInterval[1], intervals[i][1]);
            i++;
        }
        res.add(newInterval);
        while (i < n) {
            res.add(intervals[i++]);
        }
        return res.toArray(new int[res.size()][]);
    }
}""",
                "python": """class Solution:
    def insert(self, intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:
        res = []
        i, n = 0, len(intervals)
        while i < n and intervals[i][1] < newInterval[0]:
            res.append(intervals[i])
            i += 1
        while i < n and intervals[i][0] <= newInterval[1]:
            newInterval[0] = min(newInterval[0], intervals[i][0])
            newInterval[1] = max(newInterval[1], intervals[i][1])
            i += 1
        res.append(newInterval)
        while i < n:
            res.append(intervals[i])
            i += 1
        return res"""
            }
        }
    },
    # 190: Non-overlapping Intervals
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
                "java": """import java.util.*;
class Solution {
    public int eraseOverlapIntervals(int[][] intervals) {
        Arrays.sort(intervals, Comparator.comparingInt(a -> a[1]));
        int count = 0;
        int end = intervals[0][1];
        for (int i = 1; i < intervals.length; i++) {
            if (intervals[i][0] < end) {
                count++;
            } else {
                end = intervals[i][1];
            }
        }
        return count;
    }
}""",
                "python": """class Solution:
    def eraseOverlapIntervals(self, intervals: list[list[int]]) -> int:
        intervals.sort(key=lambda x: x[1])
        count = 0
        end = intervals[0][1]
        for i in range(1, len(intervals)):
            if intervals[i][0] < end:
                count += 1
            else:
                end = intervals[i][1]
        return count"""
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
                "java": """import java.util.*;
class Solution {
    public int eraseOverlapIntervals(int[][] intervals) {
        if (intervals.length == 0) return 0;
        Arrays.sort(intervals, Comparator.comparingInt(a -> a[1]));
        int removals = 0;
        int end = intervals[0][1];
        for (int i = 1; i < intervals.length; i++) {
            if (intervals[i][0] < end) {
                removals++;
            } else {
                end = intervals[i][1];
            }
        }
        return removals;
    }
}""",
                "python": """class Solution:
    def eraseOverlapIntervals(self, intervals: list[list[int]]) -> int:
        if not intervals:
            return 0
        intervals.sort(key=lambda x: x[1])
        removals = 0
        end = intervals[0][1]
        for i in range(1, len(intervals)):
            if intervals[i][0] < end:
                removals += 1
            else:
                end = intervals[i][1]
        return removals"""
            }
        }
    },
    # 191: Minimum Number of Arrows to Burst Balloons
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
                "java": """import java.util.*;
class Solution {
    public int findMinArrowShots(int[][] points) {
        Arrays.sort(points, Comparator.comparingInt(a -> a[1]));
        int arrows = 1;
        long arrowPos = points[0][1];
        for (int i = 1; i < points.length; i++) {
            if (points[i][0] > arrowPos) {
                arrows++;
                arrowPos = points[i][1];
            }
        }
        return arrows;
    }
}""",
                "python": """class Solution:
    def findMinArrowShots(self, points: list[list[int]]) -> int:
        points.sort(key=lambda x: x[1])
        arrows = 1
        pos = points[0][1]
        for i in range(1, len(points)):
            if points[i][0] > pos:
                arrows += 1
                pos = points[i][1]
        return arrows"""
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
                "java": """import java.util.*;
class Solution {
    public int findMinArrowShots(int[][] points) {
        if (points.length == 0) return 0;
        Arrays.sort(points, (a, b) -> Integer.compare(a[1], b[1]));
        int arrows = 1;
        int arrowPos = points[0][1];
        for (int i = 1; i < points.length; i++) {
            if (points[i][0] > arrowPos) {
                arrows++;
                arrowPos = points[i][1];
            }
        }
        return arrows;
    }
}""",
                "python": """class Solution:
    def findMinArrowShots(self, points: list[list[int]]) -> int:
        if not points:
            return 0
        points.sort(key=lambda x: x[1])
        arrows = 1
        pos = points[0][1]
        for i in range(1, len(points)):
            if points[i][0] > pos:
                arrows += 1
                pos = points[i][1]
        return arrows"""
            }
        }
    },
    # 192: Interval List Intersections
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
                "java": """import java.util.*;
class Solution {
    public int[][] intervalIntersection(int[][] firstList, int[][] secondList) {
        List<int[]> res = new ArrayList<>();
        int i = 0, j = 0;
        while (i < firstList.length && j < secondList.length) {
            int lo = Math.max(firstList[i][0], secondList[j][0]);
            int hi = Math.min(firstList[i][1], secondList[j][1]);
            if (lo <= hi) res.add(new int[]{lo, hi});
            if (firstList[i][1] < secondList[j][1]) i++;
            else j++;
        }
        return res.toArray(new int[res.size()][]);
    }
}""",
                "python": """class Solution:
    def intervalIntersection(self, firstList: list[list[int]], secondList: list[list[int]]) -> list[list[int]]:
        res = []
        i = j = 0
        while i < len(firstList) and j < len(secondList):
            lo = max(firstList[i][0], secondList[j][0])
            hi = min(firstList[i][1], secondList[j][1])
            if lo <= hi:
                res.append([lo, hi])
            if firstList[i][1] < secondList[j][1]:
                i += 1
            else:
                j += 1
        return res"""
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
                "java": """import java.util.*;
class Solution {
    public int[][] intervalIntersection(int[][] firstList, int[][] secondList) {
        List<int[]> res = new ArrayList<>();
        int i = 0, j = 0;
        while (i < firstList.length && j < secondList.length) {
            int lo = Math.max(firstList[i][0], secondList[j][0]);
            int hi = Math.min(firstList[i][1], secondList[j][1]);
            if (lo <= hi) {
                res.add(new int[]{lo, hi});
            }
            if (firstList[i][1] < secondList[j][1]) {
                i++;
            } else {
                j++;
            }
        }
        return res.toArray(new int[res.size()][]);
    }
}""",
                "python": """class Solution:
    def intervalIntersection(self, firstList: list[list[int]], secondList: list[list[int]]) -> list[list[int]]:
        res = []
        i = j = 0
        while i < len(firstList) and j < len(secondList):
            lo = max(firstList[i][0], secondList[j][0])
            hi = min(firstList[i][1], secondList[j][1])
            if lo <= hi:
                res.append([lo, hi])
            if firstList[i][1] < secondList[j][1]:
                i += 1
            else:
                j += 1
        return res"""
            }
        }
    },
    # 193: Remove Covered Intervals
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
                "java": """class Solution {
    public int removeCoveredIntervals(int[][] intervals) {
        int n = intervals.length;
        int covered = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (i != j && intervals[j][0] <= intervals[i][0] && intervals[j][1] >= intervals[i][1]) {
                    covered++;
                    break;
                }
            }
        }
        return n - covered;
    }
}""",
                "python": """class Solution:
    def removeCoveredIntervals(self, intervals: list[list[int]]) -> int:
        n = len(intervals)
        covered = 0
        for i in range(n):
            for j in range(n):
                if i != j and intervals[j][0] <= intervals[i][0] and intervals[j][1] >= intervals[i][1]:
                    covered += 1
                    break
        return n - covered"""
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
                "java": """import java.util.*;
class Solution {
    public int removeCoveredIntervals(int[][] intervals) {
        Arrays.sort(intervals, (a, b) -> a[0] != b[0] ? a[0] - b[0] : b[1] - a[1]);
        int count = 0;
        int maxRight = 0;
        for (int[] cur : intervals) {
            if (cur[1] > maxRight) {
                count++;
                maxRight = cur[1];
            }
        }
        return count;
    }
}""",
                "python": """class Solution:
    def removeCoveredIntervals(self, intervals: list[list[int]]) -> int:
        intervals.sort(key=lambda x: (x[0], -x[1]))
        count = 0
        max_right = 0
        for _, r in intervals:
            if r > max_right:
                count += 1
                max_right = r
        return count"""
            }
        }
    },
    # 194: My Calendar I
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
                "java": """import java.util.*;
public class MyCalendar {
    private List<int[]> books = new ArrayList<>();
    public MyCalendar() {}
    public boolean book(int start, int end) {
        for (int[] b : books) {
            if (Math.max(start, b[0]) < Math.min(end, b[1])) {
                return false;
            }
        }
        books.add(new int[]{start, end});
        return true;
    }
}""",
                "python": """class MyCalendar:
    def __init__(self):
        self.books = []

    def book(self, start: int, end: int) -> bool:
        for s, e in self.books:
            if max(start, s) < min(end, e):
                return False
        self.books.append((start, end))
        return True"""
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
                "java": """import java.util.*;
public class MyCalendar {
    private TreeMap<Integer, Integer> calendar = new TreeMap<>();
    public MyCalendar() {}
    public boolean book(int start, int end) {
        Integer prev = calendar.floorKey(start);
        if (prev != null && calendar.get(prev) > start) return false;
        Integer next = calendar.ceilingKey(start);
        if (next != null && next < end) return false;
        calendar.put(start, end);
        return true;
    }
}""",
                "python": """import bisect

class MyCalendar:
    def __init__(self):
        self.starts = []
        self.ends = []

    def book(self, start: int, end: int) -> bool:
        idx = bisect.bisect_right(self.starts, start)
        if idx > 0 and self.ends[idx - 1] > start:
            return False
        if idx < len(self.starts) and self.starts[idx] < end:
            return False
        self.starts.insert(idx, start)
        self.ends.insert(idx, end)
        return True"""
            }
        }
    },
    # 195: Car Pooling
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
                "java": """class Solution {
    public boolean carPooling(int[][] trips, int capacity) {
        int[] miles = new int[1001];
        for (int[] t : trips) {
            for (int i = t[1]; i < t[2]; i++) {
                miles[i] += t[0];
                if (miles[i] > capacity) return false;
            }
        }
        return true;
    }
}""",
                "python": """class Solution:
    def carPooling(self, trips: list[list[int]], capacity: int) -> bool:
        miles = [0] * 1001
        for num, start, end in trips:
            for i in range(start, end):
                miles[i] += num
                if miles[i] > capacity:
                    return False
        return True"""
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
                "java": """class Solution {
    public boolean carPooling(int[][] trips, int capacity) {
        int[] diff = new int[1001];
        for (int[] t : trips) {
            diff[t[1]] += t[0];
            diff[t[2]] -= t[0];
        }
        int cur = 0;
        for (int d : diff) {
            cur += d;
            if (cur > capacity) return false;
        }
        return true;
    }
}""",
                "python": """class Solution:
    def carPooling(self, trips: list[list[int]], capacity: int) -> bool:
        diff = [0] * 1001
        for num, start, end in trips:
            diff[start] += num
            diff[end] -= num
        cur = 0
        for d in diff:
            cur += d
            if cur > capacity:
                return False
        return True"""
            }
        }
    },
    # 196: Flood Fill
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
                "java": """import java.util.*;
class Solution {
    public int[][] floodFill(int[][] image, int sr, int sc, int color) {
        int orig = image[sr][sc];
        if (orig == color) return image;
        int m = image.length, n = image[0].length;
        Queue<int[]> q = new LinkedList<>();
        q.offer(new int[]{sr, sc});
        image[sr][sc] = color;
        int[][] dirs = {{1,0}, {-1,0}, {0,1}, {0,-1}};
        while (!q.isEmpty()) {
            int[] cur = q.poll();
            for (int[] d : dirs) {
                int r = cur[0] + d[0], c = cur[1] + d[1];
                if (r >= 0 && r < m && c >= 0 && c < n && image[r][c] == orig) {
                    image[r][c] = color;
                    q.offer(new int[]{r, c});
                }
            }
        }
        return image;
    }
}""",
                "python": """from collections import deque

class Solution:
    def floodFill(self, image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:
        orig = image[sr][sc]
        if orig == color: return image
        m, n = len(image), len(image[0])
        q = deque([(sr, sc)])
        image[sr][sc] = color
        while q:
            r, c = q.popleft()
            for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and image[nr][nc] == orig:
                    image[nr][nc] = color
                    q.append((nr, nc))
        return image"""
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
                "java": """class Solution {
    public int[][] floodFill(int[][] image, int sr, int sc, int color) {
        if (image[sr][sc] != color) {
            dfs(image, sr, sc, image[sr][sc], color);
        }
        return image;
    }
    private void dfs(int[][] img, int r, int c, int orig, int color) {
        if (r < 0 || r >= img.length || c < 0 || c >= img[0].length || img[r][c] != orig) {
            return;
        }
        img[r][c] = color;
        dfs(img, r + 1, c, orig, color);
        dfs(img, r - 1, c, orig, color);
        dfs(img, r, c + 1, orig, color);
        dfs(img, r, c - 1, orig, color);
    }
}""",
                "python": """class Solution:
    def floodFill(self, image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:
        orig = image[sr][sc]
        if orig == color:
            return image
        m, n = len(image), len(image[0])
        def dfs(r: int, c: int):
            if not (0 <= r < m and 0 <= c < n) or image[r][c] != orig:
                return
            image[r][c] = color
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)
        dfs(sr, sc)
        return image"""
            }
        }
    },
    # 197: Number of Islands
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
                "java": """class Solution {
    public int numIslands(char[][] grid) {
        int m = grid.length, n = grid[0].length;
        int count = 0;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == '1') {
                    count++;
                    dfs(grid, i, j);
                }
            }
        }
        return count;
    }
    private void dfs(char[][] grid, int r, int c) {
        if (r < 0 || r >= grid.length || c < 0 || c >= grid[0].length || grid[r][c] != '1') return;
        grid[r][c] = '0';
        dfs(grid, r + 1, c);
        dfs(grid, r - 1, c);
        dfs(grid, r, c + 1);
        dfs(grid, r, c - 1);
    }
}""",
                "python": """class Solution:
    def numIslands(self, grid: list[list[str]]) -> int:
        m, n = len(grid), len(grid[0])
        count = 0
        def dfs(r, c):
            if not (0 <= r < m and 0 <= c < n) or grid[r][c] != '1':
                return
            grid[r][c] = '0'
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '1':
                    count += 1
                    dfs(i, j)
        return count"""
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
                "java": """class Solution {
    public int numIslands(char[][] grid) {
        int count = 0;
        int m = grid.length, n = grid[0].length;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == '1') {
                    count++;
                    sink(grid, i, j, m, n);
                }
            }
        }
        return count;
    }
    private void sink(char[][] grid, int r, int c, int m, int n) {
        if (r < 0 || r >= m || c < 0 || c >= n || grid[r][c] != '1') return;
        grid[r][c] = '0';
        sink(grid, r + 1, c, m, n);
        sink(grid, r - 1, c, m, n);
        sink(grid, r, c + 1, m, n);
        sink(grid, r, c - 1, m, n);
    }
}""",
                "python": """class Solution:
    def numIslands(self, grid: list[list[str]]) -> int:
        m, n = len(grid), len(grid[0])
        count = 0
        def sink(r: int, c: int):
            if not (0 <= r < m and 0 <= c < n) or grid[r][c] != '1':
                return
            grid[r][c] = '0'
            sink(r + 1, c)
            sink(r - 1, c)
            sink(r, c + 1)
            sink(r, c - 1)
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '1':
                    count += 1
                    sink(i, j)
        return count"""
            }
        }
    },
    # 198: Max Area of Island
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
                "java": """class Solution {
    public int maxAreaOfIsland(int[][] grid) {
        int max = 0;
        int m = grid.length, n = grid[0].length;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 1) {
                    max = Math.max(max, area(grid, i, j));
                }
            }
        }
        return max;
    }
    private int area(int[][] grid, int r, int c) {
        if (r < 0 || r >= grid.length || c < 0 || c >= grid[0].length || grid[r][c] != 1) return 0;
        grid[r][c] = 0;
        return 1 + area(grid, r + 1, c) + area(grid, r - 1, c) + area(grid, r, c + 1) + area(grid, r, c - 1);
    }
}""",
                "python": """class Solution:
    def maxAreaOfIsland(self, grid: list[list[int]]) -> int:
        m, n = len(grid), len(grid[0])
        max_a = 0
        def area(r, c):
            if not (0 <= r < m and 0 <= c < n) or grid[r][c] != 1:
                return 0
            grid[r][c] = 0
            return 1 + area(r + 1, c) + area(r - 1, c) + area(r, c + 1) + area(r, c - 1)
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    max_a = max(max_a, area(i, j))
        return max_a"""
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
                "java": """class Solution {
    public int maxAreaOfIsland(int[][] grid) {
        int maxArea = 0;
        int m = grid.length, n = grid[0].length;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 1) {
                    maxArea = Math.max(maxArea, dfs(grid, i, j, m, n));
                }
            }
        }
        return maxArea;
    }
    private int dfs(int[][] grid, int r, int c, int m, int n) {
        if (r < 0 || r >= m || c < 0 || c >= n || grid[r][c] != 1) return 0;
        grid[r][c] = 0;
        return 1 + dfs(grid, r + 1, c, m, n) + dfs(grid, r - 1, c, m, n) +
                   dfs(grid, r, c + 1, m, n) + dfs(grid, r, c - 1, m, n);
    }
}""",
                "python": """class Solution:
    def maxAreaOfIsland(self, grid: list[list[int]]) -> int:
        m, n = len(grid), len(grid[0])
        max_area = 0
        def dfs(r: int, c: int) -> int:
            if not (0 <= r < m and 0 <= c < n) or grid[r][c] != 1:
                return 0
            grid[r][c] = 0
            return 1 + dfs(r + 1, c) + dfs(r - 1, c) + dfs(r, c + 1) + dfs(r, c - 1)
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    max_area = max(max_area, dfs(i, j))
        return max_area"""
            }
        }
    },
    # 199: Island Perimeter
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
                "java": """class Solution {
    public int islandPerimeter(int[][] grid) {
        int p = 0;
        int m = grid.length, n = grid[0].length;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 1) {
                    if (i == 0 || grid[i - 1][j] == 0) p++;
                    if (i == m - 1 || grid[i + 1][j] == 0) p++;
                    if (j == 0 || grid[i][j - 1] == 0) p++;
                    if (j == n - 1 || grid[i][j + 1] == 0) p++;
                }
            }
        }
        return p;
    }
}""",
                "python": """class Solution:
    def islandPerimeter(self, grid: list[list[int]]) -> int:
        p = 0
        m, n = len(grid), len(grid[0])
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    if i == 0 or grid[i - 1][j] == 0: p += 1
                    if i == m - 1 or grid[i + 1][j] == 0: p += 1
                    if j == 0 or grid[i][j - 1] == 0: p += 1
                    if j == n - 1 or grid[i][j + 1] == 0: p += 1
        return p"""
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
                "java": """class Solution {
    public int islandPerimeter(int[][] grid) {
        int land = 0, shared = 0;
        int m = grid.length, n = grid[0].length;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 1) {
                    land++;
                    if (i > 0 && grid[i - 1][j] == 1) shared++;
                    if (j > 0 && grid[i][j - 1] == 1) shared++;
                }
            }
        }
        return 4 * land - 2 * shared;
    }
}""",
                "python": """class Solution:
    def islandPerimeter(self, grid: list[list[int]]) -> int:
        land = 0
        shared = 0
        m, n = len(grid), len(grid[0])
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    land += 1
                    if i > 0 and grid[i - 1][j] == 1: shared += 1
                    if j > 0 and grid[i][j - 1] == 1: shared += 1
        return 4 * land - 2 * shared"""
            }
        }
    },
    # 200: Surrounded Regions
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
                "java": """class Solution {
    public void solve(char[][] board) {
        int m = board.length, n = board[0].length;
        for (int i = 0; i < m; i++) {
            dfs(board, i, 0);
            dfs(board, i, n - 1);
        }
        for (int j = 0; j < n; j++) {
            dfs(board, 0, j);
            dfs(board, m - 1, j);
        }
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (board[i][j] == 'O') board[i][j] = 'X';
                else if (board[i][j] == '#') board[i][j] = 'O';
            }
        }
    }
    private void dfs(char[][] b, int r, int c) {
        if (r < 0 || r >= b.length || c < 0 || c >= b[0].length || b[r][c] != 'O') return;
        b[r][c] = '#';
        dfs(b, r + 1, c);
        dfs(b, r - 1, c);
        dfs(b, r, c + 1);
        dfs(b, r, c - 1);
    }
}""",
                "python": """class Solution:
    def solve(self, board: list[list[str]]) -> None:
        m, n = len(board), len(board[0])
        def dfs(r, c):
            if not (0 <= r < m and 0 <= c < n) or board[r][c] != 'O':
                return
            board[r][c] = '#'
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)
        for i in range(m):
            dfs(i, 0)
            dfs(i, n - 1)
        for j in range(n):
            dfs(0, j)
            dfs(m - 1, j)
        for i in range(m):
            for j in range(n):
                if board[i][j] == 'O':
                    board[i][j] = 'X'
                elif board[i][j] == '#':
                    board[i][j] = 'O'"""
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
                "java": """class Solution {
    public void solve(char[][] board) {
        int m = board.length, n = board[0].length;
        for (int i = 0; i < m; i++) {
            if (board[i][0] == 'O') dfs(board, i, 0, m, n);
            if (board[i][n - 1] == 'O') dfs(board, i, n - 1, m, n);
        }
        for (int j = 0; j < n; j++) {
            if (board[0][j] == 'O') dfs(board, 0, j, m, n);
            if (board[m - 1][j] == 'O') dfs(board, m - 1, j, m, n);
        }
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (board[i][j] == 'O') board[i][j] = 'X';
                else if (board[i][j] == '#') board[i][j] = 'O';
            }
        }
    }
    private void dfs(char[][] board, int r, int c, int m, int n) {
        if (r < 0 || r >= m || c < 0 || c >= n || board[r][c] != 'O') return;
        board[r][c] = '#';
        dfs(board, r + 1, c, m, n);
        dfs(board, r - 1, c, m, n);
        dfs(board, r, c + 1, m, n);
        dfs(board, r, c - 1, m, n);
    }
}""",
                "python": """class Solution:
    def solve(self, board: list[list[str]]) -> None:
        m, n = len(board), len(board[0])
        def dfs(r: int, c: int):
            if not (0 <= r < m and 0 <= c < n) or board[r][c] != 'O':
                return
            board[r][c] = '#'
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)
        for i in range(m):
            if board[i][0] == 'O': dfs(i, 0)
            if board[i][n - 1] == 'O': dfs(i, n - 1)
        for j in range(n):
            if board[0][j] == 'O': dfs(0, j)
            if board[m - 1][j] == 'O': dfs(m - 1, j)
        for i in range(m):
            for j in range(n):
                if board[i][j] == 'O':
                    board[i][j] = 'X'
                elif board[i][j] == '#':
                    board[i][j] = 'O'"""
            }
        }
    }
]

with open('scripts/batches/batch_08.py', 'w', encoding='utf-8') as f:
    f.write("# Batch 8: Questions 176 to 200\n\n")
    f.write("def get_batch():\n")
    f.write("    return " + json.dumps(batch_8, indent=4) + "\n")

print("Wrote scripts/batches/batch_08.py with", len(batch_8), "questions.")


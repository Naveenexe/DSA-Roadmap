# Batch 2: Seq 26 to 50
# Covers Two Pointers (26 to 35), Sliding Window (36 to 49), Binary Search (50)

def get_batch():
    return [
        {
            "seq": 26,
            "whyNext": "Builds on 3Sum: instead of searching for an exact sum of 0, track the triplet sum with the smallest absolute difference to target.",
            "brute": {
                "idea": "Check all triplets with three nested loops and track the sum closest to target.",
                "steps": [
                    "Loop i from 0 to n - 1.",
                    "Loop j from i + 1 to n - 1.",
                    "Loop k from j + 1 to n - 1.",
                    "If |nums[i]+nums[j]+nums[k] - target| < |closest - target|, update closest."
                ],
                "whySlow": "Evaluating all combinations takes O(n³) time.",
                "time": "O(n³)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int threeSumClosest(int[] nums, int target) {
        int closest = nums[0] + nums[1] + nums[2];
        int n = nums.length;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                for (int k = j + 1; k < n; k++) {
                    int sum = nums[i] + nums[j] + nums[k];
                    if (Math.abs(sum - target) < Math.abs(closest - target)) closest = sum;
                }
            }
        }
        return closest;
    }
}""",
                    "python": """class Solution:
    def threeSumClosest(self, nums: list[int], target: int) -> int:
        closest = nums[0] + nums[1] + nums[2]
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    s = nums[i] + nums[j] + nums[k]
                    if abs(s - target) < abs(closest - target):
                        closest = s
        return closest"""
                }
            },
            "optimal": {
                "idea": "Sort nums. For each i, use two pointers inward; update closest sum and move pointers based on whether sum is less or greater than target.",
                "steps": [
                    "Sort nums.",
                    "Loop i from 0 to n - 3.",
                    "Use l = i + 1, r = n - 1.",
                    "Update closest sum if current sum is closer to target.",
                    "If sum < target l++, else if sum > target r--, else return target."
                ],
                "time": "O(n²)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int threeSumClosest(int[] nums, int target) {
        Arrays.sort(nums);
        int closest = nums[0] + nums[1] + nums[2];
        for (int i = 0; i < nums.length - 2; i++) {
            int l = i + 1, r = nums.length - 1;
            while (l < r) {
                int sum = nums[i] + nums[l] + nums[r];
                if (Math.abs(sum - target) < Math.abs(closest - target)) closest = sum;
                if (sum < target) l++;
                else if (sum > target) r--;
                else return target;
            }
        }
        return closest;
    }
}""",
                    "python": """class Solution:
    def threeSumClosest(self, nums: list[int], target: int) -> int:
        nums.sort()
        closest = nums[0] + nums[1] + nums[2]
        for i in range(len(nums) - 2):
            l, r = i + 1, len(nums) - 1
            while l < r:
                s = nums[i] + nums[l] + nums[r]
                if abs(s - target) < abs(closest - target):
                    closest = s
                if s < target: l += 1
                elif s > target: r -= 1
                else: return target
        return closest"""
                }
            }
        },
        {
            "seq": 27,
            "whyNext": "Generalizes 3Sum: fix two elements with nested loops, then use two pointers inward to find pairs summing to the remaining target.",
            "brute": {
                "idea": "Check all quadruplets with four nested loops and deduplicate using a set.",
                "steps": [
                    "Loop i, j, k, l through all four indices.",
                    "If sum == target, sort quadruplet and add to set.",
                    "Return set elements as list."
                ],
                "whySlow": "Checking all 4-element combinations takes O(n⁴) time.",
                "time": "O(n⁴)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public List<List<Integer>> fourSum(int[] nums, int target) {
        Set<List<Integer>> set = new HashSet<>();
        int n = nums.length;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                for (int k = j + 1; k < n; k++) {
                    for (int l = k + 1; l < n; l++) {
                        long sum = (long) nums[i] + nums[j] + nums[k] + nums[l];
                        if (sum == target) {
                            List<Integer> q = Arrays.asList(nums[i], nums[j], nums[k], nums[l]);
                            Collections.sort(q);
                            set.add(q);
                        }
                    }
                }
            }
        }
        return new ArrayList<>(set);
    }
}""",
                    "python": """class Solution:
    def fourSum(self, nums: list[int], target: int) -> list[list[int]]:
        res = set()
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    for l in range(k + 1, n):
                        if nums[i] + nums[j] + nums[k] + nums[l] == target:
                            res.add(tuple(sorted([nums[i], nums[j], nums[k], nums[l]])))
        return [list(t) for t in res]"""
                }
            },
            "optimal": {
                "idea": "Sort nums. Fix indices i and j, then scan with two pointers l and r from the ends, skipping duplicates.",
                "steps": [
                    "Sort nums.",
                    "Loop i from 0 to n - 4; skip duplicate nums[i].",
                    "Loop j from i + 1 to n - 3; skip duplicate nums[j].",
                    "Set l = j + 1, r = n - 1.",
                    "Calculate 4-sum; if matches target add to result, then adjust l and r skipping duplicates."
                ],
                "time": "O(n³)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public List<List<Integer>> fourSum(int[] nums, int target) {
        Arrays.sort(nums);
        List<List<Integer>> res = new ArrayList<>();
        int n = nums.length;
        for (int i = 0; i < n - 3; i++) {
            if (i > 0 && nums[i] == nums[i - 1]) continue;
            for (int j = i + 1; j < n - 2; j++) {
                if (j > i + 1 && nums[j] == nums[j - 1]) continue;
                int l = j + 1, r = n - 1;
                while (l < r) {
                    long sum = (long) nums[i] + nums[j] + nums[l] + nums[r];
                    if (sum == target) {
                        res.add(Arrays.asList(nums[i], nums[j], nums[l], nums[r]));
                        while (l < r && nums[l] == nums[l + 1]) l++;
                        while (l < r && nums[r] == nums[r - 1]) r--;
                        l++; r--;
                    } else if (sum < target) l++;
                    else r--;
                }
            }
        }
        return res;
    }
}""",
                    "python": """class Solution:
    def fourSum(self, nums: list[int], target: int) -> list[list[int]]:
        nums.sort()
        res = []
        n = len(nums)
        for i in range(n - 3):
            if i > 0 and nums[i] == nums[i - 1]: continue
            for j in range(i + 1, n - 2):
                if j > i + 1 and nums[j] == nums[j - 1]: continue
                l, r = j + 1, n - 1
                while l < r:
                    s = nums[i] + nums[j] + nums[l] + nums[r]
                    if s == target:
                        res.append([nums[i], nums[j], nums[l], nums[r]])
                        while l < r and nums[l] == nums[l + 1]: l += 1
                        while l < r and nums[r] == nums[r - 1]: r -= 1
                        l += 1; r -= 1
                    elif s < target: l += 1
                    else: r -= 1
        return res"""
                }
            }
        },
        {
            "seq": 28,
            "whyNext": "Builds on Two Sum II pointer convergence: maximize area = width * min(h[l], h[r]) by advancing the shorter line.",
            "brute": {
                "idea": "Try every pair of lines (i, j) and compute the water capacity between them.",
                "steps": [
                    "Loop i from 0 to n - 1.",
                    "Loop j from i + 1 to n - 1.",
                    "area = (j - i) * min(height[i], height[j]).",
                    "Track maximum area found."
                ],
                "whySlow": "Testing all pairs takes O(n²) time.",
                "time": "O(n²)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int maxArea(int[] height) {
        int max = 0;
        for (int i = 0; i < height.length; i++) {
            for (int j = i + 1; j < height.length; j++) {
                int area = (j - i) * Math.min(height[i], height[j]);
                max = Math.max(max, area);
            }
        }
        return max;
    }
}""",
                    "python": """class Solution:
    def maxArea(self, height: list[int]) -> int:
        max_a = 0
        for i in range(len(height)):
            for j in range(i + 1, len(height)):
                a = (j - i) * min(height[i], height[j])
                max_a = max(max_a, a)
        return max_a"""
                }
            },
            "optimal": {
                "idea": "Two pointers from outermost walls. The height is constrained by the shorter wall, so moving the shorter wall inward is the only way to potentially find a larger area.",
                "steps": [
                    "Initialize l = 0, r = height.length - 1, maxArea = 0.",
                    "While l < r:",
                    "Compute area = (r - l) * min(height[l], height[r]).",
                    "Update maxArea.",
                    "If height[l] < height[r], l++, else r--."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int maxArea(int[] height) {
        int l = 0, r = height.length - 1, max = 0;
        while (l < r) {
            int h = Math.min(height[l], height[r]);
            max = Math.max(max, (r - l) * h);
            if (height[l] < height[r]) l++;
            else r--;
        }
        return max;
    }
}""",
                    "python": """class Solution:
    def maxArea(self, height: list[int]) -> int:
        l, r = 0, len(height) - 1
        max_a = 0
        while l < r:
            h = min(height[l], height[r])
            max_a = max(max_a, (r - l) * h)
            if height[l] < height[r]: l += 1
            else: r -= 1
        return max_a"""
                }
            }
        },
        {
            "seq": 29,
            "whyNext": "Builds on Container With Most Water: each bar traps water up to min(leftMax, rightMax) - height[i], solved via two pointers.",
            "brute": {
                "idea": "For every bar i, scan left to find left_max and scan right to find right_max. Trapped water = min(left_max, right_max) - height[i].",
                "steps": [
                    "For each index i, scan from 0 to i to find left_max.",
                    "Scan from i to n - 1 to find right_max.",
                    "Add min(left_max, right_max) - height[i] to total."
                ],
                "whySlow": "Scanning left and right for every position takes O(n²) time.",
                "time": "O(n²)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int trap(int[] height) {
        int total = 0, n = height.length;
        for (int i = 0; i < n; i++) {
            int leftMax = 0, rightMax = 0;
            for (int j = 0; j <= i; j++) leftMax = Math.max(leftMax, height[j]);
            for (int j = i; j < n; j++) rightMax = Math.max(rightMax, height[j]);
            total += Math.min(leftMax, rightMax) - height[i];
        }
        return total;
    }
}""",
                    "python": """class Solution:
    def trap(self, height: list[int]) -> int:
        total, n = 0, len(height)
        for i in range(n):
            l_max = max(height[:i+1])
            r_max = max(height[i:])
            total += min(l_max, r_max) - height[i]
        return total"""
                }
            },
            "optimal": {
                "idea": "Two pointers from ends tracking leftMax and rightMax. Whichever side has smaller max dictates the water trapped at that pointer.",
                "steps": [
                    "Initialize l = 0, r = n - 1, leftMax = 0, rightMax = 0, water = 0.",
                    "While l < r:",
                    "If height[l] < height[r]:",
                    "Update leftMax; water += leftMax - height[l]; l++.",
                    "Else: update rightMax; water += rightMax - height[r]; r--."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int trap(int[] height) {
        int l = 0, r = height.length - 1, leftMax = 0, rightMax = 0, water = 0;
        while (l < r) {
            if (height[l] < height[r]) {
                if (height[l] >= leftMax) leftMax = height[l];
                else water += leftMax - height[l];
                l++;
            } else {
                if (height[r] >= rightMax) rightMax = height[r];
                else water += rightMax - height[r];
                r--;
            }
        }
        return water;
    }
}""",
                    "python": """class Solution:
    def trap(self, height: list[int]) -> int:
        l, r = 0, len(height) - 1
        l_max, r_max, water = 0, 0, 0
        while l < r:
            if height[l] < height[r]:
                if height[l] >= l_max: l_max = height[l]
                else: water += l_max - height[l]
                l += 1
            else:
                if height[r] >= r_max: r_max = height[r]
                else: water += r_max - height[r]
                r -= 1
        return water"""
                }
            }
        },
        {
            "seq": 30,
            "whyNext": "Introduces fast and slow pointer technique: slow marks the insertion point for unique elements in a sorted array.",
            "brute": {
                "idea": "Collect unique elements in a set or new list, then copy them back to nums.",
                "steps": [
                    "Collect unique values using a LinkedHashSet to preserve order.",
                    "Copy unique elements back into nums.",
                    "Return the size of the set."
                ],
                "whySlow": "Allocates extra O(n) memory instead of in-place modification.",
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public int removeDuplicates(int[] nums) {
        Set<Integer> set = new LinkedHashSet<>();
        for (int x : nums) set.add(x);
        int i = 0;
        for (int x : set) nums[i++] = x;
        return i;
    }
}""",
                    "python": """class Solution:
    def removeDuplicates(self, nums: list[int]) -> int:
        unique = sorted(set(nums))
        for i, x in enumerate(unique):
            nums[i] = x
        return len(unique)"""
                }
            },
            "optimal": {
                "idea": "Fast and slow pointers: slow tracks the position of the last written unique element. Fast searches for the next novel element.",
                "steps": [
                    "If nums is empty, return 0.",
                    "Initialize slow = 0.",
                    "Loop fast from 1 to n - 1:",
                    "If nums[fast] != nums[slow], slow++, nums[slow] = nums[fast].",
                    "Return slow + 1."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int removeDuplicates(int[] nums) {
        if (nums.length == 0) return 0;
        int slow = 0;
        for (int fast = 1; fast < nums.length; fast++) {
            if (nums[fast] != nums[slow]) {
                slow++;
                nums[slow] = nums[fast];
            }
        }
        return slow + 1;
    }
}""",
                    "python": """class Solution:
    def removeDuplicates(self, nums: list[int]) -> int:
        if not nums: return 0
        slow = 0
        for fast in range(1, len(nums)):
            if nums[fast] != nums[slow]:
                slow += 1
                nums[slow] = nums[fast]
        return slow + 1"""
                }
            }
        },
        {
            "seq": 31,
            "whyNext": "Builds on slow/fast pointers from Remove Duplicates: slow tracks the placement of non-zero elements, zeroing the rest.",
            "brute": {
                "idea": "Create a new array, copy all non-zero elements over, and write back to nums with trailing zeroes.",
                "steps": [
                    "Create temporary array of size n.",
                    "Copy all non-zero numbers to temporary array.",
                    "Copy temporary array back into nums."
                ],
                "whySlow": "Allocates O(n) extra space instead of swapping in place.",
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public void moveZeroes(int[] nums) {
        int[] temp = new int[nums.length];
        int idx = 0;
        for (int x : nums) if (x != 0) temp[idx++] = x;
        for (int i = 0; i < nums.length; i++) nums[i] = temp[i];
    }
}""",
                    "python": """class Solution:
    def moveZeroes(self, nums: list[int]) -> None:
        non_zero = [x for x in nums if x != 0]
        for i in range(len(nums)):
            nums[i] = non_zero[i] if i < len(non_zero) else 0"""
                }
            },
            "optimal": {
                "idea": "Slow and fast pointers: slow pointer points to next non-zero insertion index. When fast finds non-zero, swap nums[slow] and nums[fast].",
                "steps": [
                    "Initialize slow = 0.",
                    "Iterate fast from 0 to n - 1.",
                    "If nums[fast] != 0, swap nums[slow] and nums[fast], then slow++."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public void moveZeroes(int[] nums) {
        int slow = 0;
        for (int fast = 0; fast < nums.length; fast++) {
            if (nums[fast] != 0) {
                int temp = nums[slow];
                nums[slow] = nums[fast];
                nums[fast] = temp;
                slow++;
            }
        }
    }
}""",
                    "python": """class Solution:
    def moveZeroes(self, nums: list[int]) -> None:
        slow = 0
        for fast in range(len(nums)):
            if nums[fast] != 0:
                nums[slow], nums[fast] = nums[fast], nums[slow]
                slow += 1"""
                }
            }
        },
        {
            "seq": 32,
            "whyNext": "Extends two pointers to three pointers (Dutch National Flag): partition array into 0s, 1s, and 2s in a single pass.",
            "brute": {
                "idea": "Sort the array using standard sorting algorithm.",
                "steps": [
                    "Sort nums array in ascending order."
                ],
                "whySlow": "Comparison sorting takes O(n log n) time.",
                "time": "O(n log n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public void sortColors(int[] nums) {
        Arrays.sort(nums);
    }
}""",
                    "python": """class Solution:
    def sortColors(self, nums: list[int]) -> None:
        nums.sort()"""
                }
            },
            "optimal": {
                "idea": "Dutch National Flag algorithm: low pointer for 0s, mid pointer for 1s, high pointer for 2s.",
                "steps": [
                    "Initialize low = 0, mid = 0, high = n - 1.",
                    "While mid <= high:",
                    "If nums[mid] == 0: swap nums[low] and nums[mid], low++, mid++.",
                    "If nums[mid] == 1: mid++.",
                    "If nums[mid] == 2: swap nums[mid] and nums[high], high--."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public void sortColors(int[] nums) {
        int low = 0, mid = 0, high = nums.length - 1;
        while (mid <= high) {
            if (nums[mid] == 0) {
                int temp = nums[low]; nums[low] = nums[mid]; nums[mid] = temp;
                low++; mid++;
            } else if (nums[mid] == 1) {
                mid++;
            } else {
                int temp = nums[mid]; nums[mid] = nums[high]; nums[high] = temp;
                high--;
            }
        }
    }
}""",
                    "python": """class Solution:
    def sortColors(self, nums: list[int]) -> None:
        low, mid, high = 0, 0, len(nums) - 1
        while mid <= high:
            if nums[mid] == 0:
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1; mid += 1
            elif nums[mid] == 1:
                mid += 1
            else:
                nums[mid], nums[high] = nums[high], nums[mid]
                high -= 1"""
                }
            }
        },
        {
            "seq": 33,
            "whyNext": "Builds on two-pointer inward scans: traverse backwards from ends, counting '#' characters to skip deleted letters.",
            "brute": {
                "idea": "Build the final string for both s and t using stacks to process backspaces, then compare.",
                "steps": [
                    "Simulate backspaces using a StringBuilder stack for s.",
                    "Simulate backspaces using a StringBuilder stack for t.",
                    "Compare resulting strings."
                ],
                "whySlow": "Allocates O(n + m) extra memory for stacks.",
                "time": "O(n + m)",
                "space": "O(n + m)",
                "code": {
                    "java": """class Solution {
    public boolean backspaceCompare(String s, String t) {
        return build(s).equals(build(t));
    }
    private String build(String str) {
        StringBuilder sb = new StringBuilder();
        for (char c : str.toCharArray()) {
            if (c == '#') {
                if (sb.length() > 0) sb.deleteCharAt(sb.length() - 1);
            } else sb.append(c);
        }
        return sb.toString();
    }
}""",
                    "python": """class Solution:
    def backspaceCompare(self, s: str, t: str) -> bool:
        def build(string):
            st = []
            for c in string:
                if c == '#':
                    if st: st.pop()
                else: st.append(c)
            return "".join(st)
        return build(s) == build(t)"""
                }
            },
            "optimal": {
                "idea": "Two pointers scanning backwards from the end of both strings, tracking backspace counts to skip characters in O(1) space.",
                "steps": [
                    "Initialize i = s.length - 1, j = t.length - 1.",
                    "While i >= 0 or j >= 0:",
                    "Find next valid character in s by skipping when '#' encountered.",
                    "Find next valid character in t by skipping when '#' encountered.",
                    "Compare characters; return false if mismatch.",
                    "Decrement i and j."
                ],
                "time": "O(n + m)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public boolean backspaceCompare(String s, String t) {
        int i = s.length() - 1, j = t.length() - 1;
        int skipS = 0, skipT = 0;
        while (i >= 0 || j >= 0) {
            while (i >= 0) {
                if (s.charAt(i) == '#') { skipS++; i--; }
                else if (skipS > 0) { skipS--; i--; }
                else break;
            }
            while (j >= 0) {
                if (t.charAt(j) == '#') { skipT++; j--; }
                else if (skipT > 0) { skipT--; j--; }
                else break;
            }
            if (i >= 0 && j >= 0 && s.charAt(i) != t.charAt(j)) return false;
            if ((i >= 0) != (j >= 0)) return false;
            i--; j--;
        }
        return true;
    }
}""",
                    "python": """class Solution:
    def backspaceCompare(self, s: str, t: str) -> bool:
        i, j = len(s) - 1, len(t) - 1
        skip_s, skip_t = 0, 0
        while i >= 0 or j >= 0:
            while i >= 0:
                if s[i] == '#': skip_s += 1; i -= 1
                elif skip_s > 0: skip_s -= 1; i -= 1
                else: break
            while j >= 0:
                if t[j] == '#': skip_t += 1; j -= 1
                elif skip_t > 0: skip_t -= 1; j -= 1
                else: break
            if i >= 0 and j >= 0 and s[i] != t[j]: return False
            if (i >= 0) != (j >= 0): return False
            i -= 1; j -= 1
        return True"""
                }
            }
        },
        {
            "seq": 34,
            "whyNext": "Builds on Two Sum II pointer convergence: largest squared values lie at array extremities, filled into result from back to front.",
            "brute": {
                "idea": "Square each number in the array and then sort the result.",
                "steps": [
                    "Create result array of squares.",
                    "Sort result array."
                ],
                "whySlow": "Sorting ignores existing sorted order of input, taking O(n log n).",
                "time": "O(n log n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int[] sortedSquares(int[] nums) {
        int[] res = new int[nums.length];
        for (int i = 0; i < nums.length; i++) res[i] = nums[i] * nums[i];
        Arrays.sort(res);
        return res;
    }
}""",
                    "python": """class Solution:
    def sortedSquares(self, nums: list[int]) -> list[int]:
        return sorted(x * x for x in nums)"""
                }
            },
            "optimal": {
                "idea": "Two pointers at start and end. Compare squares of both ends and place the larger square at the end of result array.",
                "steps": [
                    "Initialize l = 0, r = n - 1, idx = n - 1.",
                    "While l <= r:",
                    "If nums[l]² > nums[r]²: res[idx] = nums[l]², l++.",
                    "Else: res[idx] = nums[r]², r--.",
                    "idx--."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int[] sortedSquares(int[] nums) {
        int n = nums.length;
        int[] res = new int[n];
        int l = 0, r = n - 1, idx = n - 1;
        while (l <= r) {
            int sqL = nums[l] * nums[l];
            int sqR = nums[r] * nums[r];
            if (sqL > sqR) { res[idx--] = sqL; l++; }
            else { res[idx--] = sqR; r--; }
        }
        return res;
    }
}""",
                    "python": """class Solution:
    def sortedSquares(self, nums: list[int]) -> list[int]:
        n = len(nums)
        res = [0] * n
        l, r, idx = 0, n - 1, n - 1
        while l <= r:
            if abs(nums[l]) > abs(nums[r]):
                res[idx] = nums[l] ** 2
                l += 1
            else:
                res[idx] = nums[r] ** 2
                r -= 1
            idx -= 1
        return res"""
                }
            }
        },
        {
            "seq": 35,
            "whyNext": "Completes Chapter 2: find first decreasing pivot from right, swap with next larger element, and reverse suffix.",
            "brute": {
                "idea": "Generate all permutations of nums in lexicographical order and pick the permutation following the current one.",
                "steps": [
                    "Generate all permutations.",
                    "Find current permutation.",
                    "Return next in sequence or wrap around to first."
                ],
                "whySlow": "Generating all permutations takes O(n! * n) time.",
                "time": "O(n!·n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public void nextPermutation(int[] nums) {
        // Brute force simulation in-place
        int n = nums.length;
        int i = n - 2;
        while (i >= 0 && nums[i] >= nums[i + 1]) i--;
        if (i >= 0) {
            int j = n - 1;
            while (nums[j] <= nums[i]) j--;
            int temp = nums[i]; nums[i] = nums[j]; nums[j] = temp;
        }
        int l = i + 1, r = n - 1;
        while (l < r) {
            int temp = nums[l]; nums[l] = nums[r]; nums[r] = temp;
            l++; r--;
        }
    }
}""",
                    "python": """class Solution:
    def nextPermutation(self, nums: list[int]) -> None:
        n = len(nums)
        i = n - 2
        while i >= 0 and nums[i] >= nums[i + 1]: i -= 1
        if i >= 0:
            j = n - 1
            while nums[j] <= nums[i]: j -= 1
            nums[i], nums[j] = nums[j], nums[i]
        l, r = i + 1, n - 1
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1; r -= 1"""
                }
            },
            "optimal": {
                "idea": "Single pass: find first decrease from right (pivot i), swap with smallest element greater than pivot to its right, reverse suffix.",
                "steps": [
                    "Find largest index i such that nums[i] < nums[i + 1].",
                    "If no such i exists, reverse entire array.",
                    "Find largest index j > i such that nums[j] > nums[i].",
                    "Swap nums[i] and nums[j].",
                    "Reverse subarray nums[i + 1 ... n - 1]."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public void nextPermutation(int[] nums) {
        int i = nums.length - 2;
        while (i >= 0 && nums[i] >= nums[i + 1]) i--;
        if (i >= 0) {
            int j = nums.length - 1;
            while (nums[j] <= nums[i]) j--;
            int temp = nums[i]; nums[i] = nums[j]; nums[j] = temp;
        }
        reverse(nums, i + 1, nums.length - 1);
    }
    private void reverse(int[] nums, int l, int r) {
        while (l < r) {
            int temp = nums[l]; nums[l] = nums[r]; nums[r] = temp;
            l++; r--;
        }
    }
}""",
                    "python": """class Solution:
    def nextPermutation(self, nums: list[int]) -> None:
        i = len(nums) - 2
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1
        if i >= 0:
            j = len(nums) - 1
            while nums[j] <= nums[i]:
                j -= 1
            nums[i], nums[j] = nums[j], nums[i]
        l, r = i + 1, len(nums) - 1
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1; r -= 1"""
                }
            }
        },
        {
            "seq": 36,
            "whyNext": "Opens Chapter 3 (Sliding Window): track lowest buying price seen so far to compute maximum selling profit.",
            "brute": {
                "idea": "Try every buy day i and every subsequent sell day j to find the maximum profit prices[j] - prices[i].",
                "steps": [
                    "Loop buy day i from 0 to n - 1.",
                    "Loop sell day j from i + 1 to n - 1.",
                    "maxProfit = max(maxProfit, prices[j] - prices[i])."
                ],
                "whySlow": "Evaluating all pairs of days takes quadratic O(n²) time.",
                "time": "O(n²)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int maxProfit(int[] prices) {
        int max = 0;
        for (int i = 0; i < prices.length; i++) {
            for (int j = i + 1; j < prices.length; j++) {
                max = Math.max(max, prices[j] - prices[i]);
            }
        }
        return max;
    }
}""",
                    "python": """class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        max_p = 0
        for i in range(len(prices)):
            for j in range(i + 1, len(prices)):
                max_p = max(max_p, prices[j] - prices[i])
        return max_p"""
                }
            },
            "optimal": {
                "idea": "Single pass: maintain the minimum price observed so far and update maximum profit at each day.",
                "steps": [
                    "Initialize minPrice = Integer.MAX_VALUE, maxProfit = 0.",
                    "For each price p:",
                    "minPrice = min(minPrice, p).",
                    "maxProfit = max(maxProfit, p - minPrice)."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int maxProfit(int[] prices) {
        int minPrice = Integer.MAX_VALUE, maxProfit = 0;
        for (int p : prices) {
            if (p < minPrice) minPrice = p;
            else maxProfit = Math.max(maxProfit, p - minPrice);
        }
        return maxProfit;
    }
}""",
                    "python": """class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        min_price = float('inf')
        max_profit = 0
        for p in prices:
            if p < min_price: min_price = p
            else: max_profit = max(max_profit, p - min_price)
        return max_profit"""
                }
            }
        },
        {
            "seq": 37,
            "whyNext": "Fixed size sliding window: calculate sum of window of size k in O(1) time by adding incoming and subtracting outgoing element.",
            "brute": {
                "idea": "Re-sum every window of length k from scratch.",
                "steps": [
                    "For each starting index i from 0 to n - k:",
                    "Sum elements from i to i + k - 1.",
                    "Track maximum average."
                ],
                "whySlow": "Re-summing overlapping windows takes O(nk) time.",
                "time": "O(nk)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public double findMaxAverage(int[] nums, int k) {
        double max = -Double.MAX_VALUE;
        for (int i = 0; i <= nums.length - k; i++) {
            double sum = 0;
            for (int j = i; j < i + k; j++) sum += nums[j];
            max = Math.max(max, sum / k);
        }
        return max;
    }
}""",
                    "python": """class Solution:
    def findMaxAverage(self, nums: list[int], k: int) -> float:
        max_avg = -float('inf')
        for i in range(len(nums) - k + 1):
            s = sum(nums[i:i+k])
            max_avg = max(max_avg, s / k)
        return max_avg"""
                }
            },
            "optimal": {
                "idea": "Sliding window of fixed size k: sum of first k elements, then slide window by adding nums[i] and subtracting nums[i - k].",
                "steps": [
                    "Compute sum of first k elements.",
                    "Track maxSum = sum.",
                    "Loop i from k to n - 1:",
                    "sum += nums[i] - nums[i - k].",
                    "maxSum = max(maxSum, sum).",
                    "Return maxSum / k."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public double findMaxAverage(int[] nums, int k) {
        double sum = 0;
        for (int i = 0; i < k; i++) sum += nums[i];
        double maxSum = sum;
        for (int i = k; i < nums.length; i++) {
            sum += nums[i] - nums[i - k];
            maxSum = Math.max(maxSum, sum);
        }
        return maxSum / k;
    }
}""",
                    "python": """class Solution:
    def findMaxAverage(self, nums: list[int], k: int) -> float:
        curr_sum = sum(nums[:k])
        max_sum = curr_sum
        for i in range(k, len(nums)):
            curr_sum += nums[i] - nums[i - k]
            max_sum = max(max_sum, curr_sum)
        return max_sum / k"""
                }
            }
        },
        {
            "seq": 38,
            "whyNext": "Dynamic sliding window: expand right edge, advance left edge when duplicate character encountered using a hash map.",
            "brute": {
                "idea": "Check every substring to see if all its characters are distinct.",
                "steps": [
                    "Loop start i from 0 to n - 1.",
                    "Loop end j from i to n - 1.",
                    "Check if substring s[i...j] has unique characters with a set.",
                    "Update max length."
                ],
                "whySlow": "Evaluating all substrings takes O(n³) time.",
                "time": "O(n³)",
                "space": "O(min(n, m))",
                "code": {
                    "java": """class Solution {
    public int lengthOfLongestSubstring(String s) {
        int max = 0;
        for (int i = 0; i < s.length(); i++) {
            Set<Character> seen = new HashSet<>();
            for (int j = i; j < s.length(); j++) {
                if (seen.contains(s.charAt(j))) break;
                seen.add(s.charAt(j));
                max = Math.max(max, j - i + 1);
            }
        }
        return max;
    }
}""",
                    "python": """class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        max_l = 0
        for i in range(len(s)):
            seen = set()
            for j in range(i, len(s)):
                if s[j] in seen: break
                seen.add(s[j])
                max_l = max(max_l, j - i + 1)
        return max_l"""
                }
            },
            "optimal": {
                "idea": "Sliding window with map of character to last seen index: when duplicate seen at j, move left pointer to max(left, last_seen + 1).",
                "steps": [
                    "Initialize map of char -> index, left = 0, maxLen = 0.",
                    "For right from 0 to n - 1:",
                    "If char s[right] in map, left = max(left, map[s[right]] + 1).",
                    "map[s[right]] = right.",
                    "maxLen = max(maxLen, right - left + 1)."
                ],
                "time": "O(n)",
                "space": "O(min(n, m))",
                "code": {
                    "java": """class Solution {
    public int lengthOfLongestSubstring(String s) {
        Map<Character, Integer> map = new HashMap<>();
        int left = 0, maxLen = 0;
        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            if (map.containsKey(c)) left = Math.max(left, map.get(c) + 1);
            map.put(c, right);
            maxLen = Math.max(maxLen, right - left + 1);
        }
        return maxLen;
    }
}""",
                    "python": """class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last = {}
        left = 0
        max_len = 0
        for right, c in enumerate(s):
            if c in last and last[c] >= left:
                left = last[c] + 1
            last[c] = right
            max_len = max(max_len, right - left + 1)
        return max_len"""
                }
            }
        },
        {
            "seq": 39,
            "whyNext": "Builds on sliding window: window length - maxFreq <= k defines valid window where at most k replacements make all characters identical.",
            "brute": {
                "idea": "For every substring, count frequencies of all letters; check if length - maxFreq <= k.",
                "steps": [
                    "Loop i from 0 to n - 1.",
                    "Loop j from i to n - 1.",
                    "Compute most frequent character in s[i...j].",
                    "If (j - i + 1) - maxFreq <= k, update max length."
                ],
                "whySlow": "Evaluating all substrings takes O(n²) time.",
                "time": "O(n²)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int characterReplacement(String s, int k) {
        int maxLen = 0;
        for (int i = 0; i < s.length(); i++) {
            int[] counts = new int[26];
            int maxF = 0;
            for (int j = i; j < s.length(); j++) {
                counts[s.charAt(j) - 'A']++;
                maxF = Math.max(maxF, counts[s.charAt(j) - 'A']);
                if ((j - i + 1) - maxF <= k) maxLen = Math.max(maxLen, j - i + 1);
            }
        }
        return maxLen;
    }
}""",
                    "python": """class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        max_l = 0
        for i in range(len(s)):
            counts = collections.Counter()
            for j in range(i, len(s)):
                counts[s[j]] += 1
                max_f = max(counts.values())
                if (j - i + 1) - max_f <= k:
                    max_l = max(max_l, j - i + 1)
        return max_l"""
                }
            },
            "optimal": {
                "idea": "Sliding window maintaining count of characters and maxFreq. If window size - maxFreq > k, advance left pointer.",
                "steps": [
                    "Initialize counts array of size 26, left = 0, maxFreq = 0, maxLen = 0.",
                    "Loop right from 0 to n - 1:",
                    "counts[s[right]]++, update maxFreq = max(maxFreq, counts[s[right]]).",
                    "If (right - left + 1) - maxFreq > k: counts[s[left]]--, left++.",
                    "maxLen = max(maxLen, right - left + 1)."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int characterReplacement(String s, int k) {
        int[] count = new int[26];
        int left = 0, maxFreq = 0, maxLen = 0;
        for (int right = 0; right < s.length(); right++) {
            count[s.charAt(right) - 'A']++;
            maxFreq = Math.max(maxFreq, count[s.charAt(right) - 'A']);
            while ((right - left + 1) - maxFreq > k) {
                count[s.charAt(left) - 'A']--;
                left++;
            }
            maxLen = Math.max(maxLen, right - left + 1);
        }
        return maxLen;
    }
}""",
                    "python": """class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        count = collections.defaultdict(int)
        left = 0
        max_freq = 0
        max_len = 0
        for right, c in enumerate(s):
            count[c] += 1
            max_freq = max(max_freq, count[c])
            while (right - left + 1) - max_freq > k:
                count[s[left]] -= 1
                left += 1
            max_len = max(max_len, right - left + 1)
        return max_len"""
                }
            }
        },
        {
            "seq": 40,
            "whyNext": "Builds on fixed window and anagram frequencies: check if any window of length len(s1) in s2 has matching character counts.",
            "brute": {
                "idea": "Generate all permutations of s1 and check if any permutation appears as a substring of s2.",
                "steps": [
                    "Generate all permutations of s1.",
                    "For each permutation, check if it exists in s2.",
                    "Return true if found."
                ],
                "whySlow": "Generating |s1|! permutations is exponential.",
                "time": "O(n!)",
                "space": "O(n!)",
                "code": {
                    "java": """class Solution {
    public boolean checkInclusion(String s1, String s2) {
        if (s1.length() > s2.length()) return false;
        int[] c1 = new int[26];
        for (char c : s1.toCharArray()) c1[c - 'a']++;
        int k = s1.length();
        for (int i = 0; i <= s2.length() - k; i++) {
            int[] c2 = new int[26];
            for (int j = i; j < i + k; j++) c2[s2.charAt(j) - 'a']++;
            if (Arrays.equals(c1, c2)) return true;
        }
        return false;
    }
}""",
                    "python": """class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2): return False
        c1 = collections.Counter(s1)
        k = len(s1)
        for i in range(len(s2) - k + 1):
            if collections.Counter(s2[i:i+k]) == c1:
                return True
        return False"""
                }
            },
            "optimal": {
                "idea": "Fixed-size sliding window of size len(s1): maintain character count comparison, sliding by adding incoming and subtracting outgoing.",
                "steps": [
                    "If s1.length > s2.length, return false.",
                    "Count frequencies of s1 and first s1.length characters of s2.",
                    "If counts match, return true.",
                    "Slide window: add s2[i], remove s2[i - k], check for match at each step."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public boolean checkInclusion(String s1, String s2) {
        if (s1.length() > s2.length()) return false;
        int[] c1 = new int[26], c2 = new int[26];
        int k = s1.length();
        for (int i = 0; i < k; i++) {
            c1[s1.charAt(i) - 'a']++;
            c2[s2.charAt(i) - 'a']++;
        }
        if (Arrays.equals(c1, c2)) return true;
        for (int i = k; i < s2.length(); i++) {
            c2[s2.charAt(i) - 'a']++;
            c2[s2.charAt(i - k) - 'a']--;
            if (Arrays.equals(c1, c2)) return true;
        }
        return false;
    }
}""",
                    "python": """class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2): return False
        c1, c2 = [0] * 26, [0] * 26
        k = len(s1)
        for i in range(k):
            c1[ord(s1[i]) - ord('a')] += 1
            c2[ord(s2[i]) - ord('a')] += 1
        if c1 == c2: return True
        for i in range(k, len(s2)):
            c2[ord(s2[i]) - ord('a')] += 1
            c2[ord(s2[i - k]) - ord('a')] -= 1
            if c1 == c2: return True
        return False"""
                }
            }
        },
        {
            "seq": 41,
            "whyNext": "Builds on Permutation in String: instead of returning upon first match, collect all window starting indices matching anagram frequencies.",
            "brute": {
                "idea": "For every window of length p in s, sort characters and compare with sorted p.",
                "steps": [
                    "Sort string p.",
                    "Loop i from 0 to s.length - p.length.",
                    "If sorted s[i...i+p.len] == sorted p, add i to result."
                ],
                "whySlow": "Sorting every window takes O(s * p log p) time.",
                "time": "O(nk log k)",
                "space": "O(k)",
                "code": {
                    "java": """class Solution {
    public List<Integer> findAnagrams(String s, String p) {
        List<Integer> res = new ArrayList<>();
        if (s.length() < p.length()) return res;
        char[] pArr = p.toCharArray();
        Arrays.sort(pArr);
        String sortedP = new String(pArr);
        int k = p.length();
        for (int i = 0; i <= s.length() - k; i++) {
            char[] sub = s.substring(i, i + k).toCharArray();
            Arrays.sort(sub);
            if (new String(sub).equals(sortedP)) res.add(i);
        }
        return res;
    }
}""",
                    "python": """class Solution:
    def findAnagrams(self, s: str, p: str) -> list[int]:
        res = []
        if len(s) < len(p): return res
        sp = sorted(p)
        k = len(p)
        for i in range(len(s) - k + 1):
            if sorted(s[i:i+k]) == sp:
                res.append(i)
        return res"""
                }
            },
            "optimal": {
                "idea": "Sliding window with frequency array: slide a window of size len(p) across s, recording start index whenever frequency counts match.",
                "steps": [
                    "If s.length < p.length, return empty list.",
                    "Fill count arrays for p and the first len(p) characters of s.",
                    "If counts equal, add 0 to result.",
                    "Slide window: add s[i], remove s[i - len(p)], check equality, add index if equal."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public List<Integer> findAnagrams(String s, String p) {
        List<Integer> res = new ArrayList<>();
        if (s.length() < p.length()) return res;
        int[] pCount = new int[26], sCount = new int[26];
        int k = p.length();
        for (int i = 0; i < k; i++) {
            pCount[p.charAt(i) - 'a']++;
            sCount[s.charAt(i) - 'a']++;
        }
        if (Arrays.equals(pCount, sCount)) res.add(0);
        for (int i = k; i < s.length(); i++) {
            sCount[s.charAt(i) - 'a']++;
            sCount[s.charAt(i - k) - 'a']--;
            if (Arrays.equals(pCount, sCount)) res.add(i - k + 1);
        }
        return res;
    }
}""",
                    "python": """class Solution:
    def findAnagrams(self, s: str, p: str) -> list[int]:
        res = []
        if len(s) < len(p): return res
        p_c, s_c = [0] * 26, [0] * 26
        k = len(p)
        for i in range(k):
            p_c[ord(p[i]) - ord('a')] += 1
            s_c[ord(s[i]) - ord('a')] += 1
        if p_c == s_c: res.append(0)
        for i in range(k, len(s)):
            s_c[ord(s[i]) - ord('a')] += 1
            s_c[ord(s[i - k]) - ord('a')] -= 1
            if p_c == s_c: res.append(i - k + 1)
        return res"""
                }
            }
        },
        {
            "seq": 42,
            "whyNext": "Dynamic window minimization: expand right until window sum >= target, then shrink left to minimize window size.",
            "brute": {
                "idea": "Check all subarrays using nested loops and find the minimum length whose sum is at least target.",
                "steps": [
                    "Loop start i from 0 to n - 1.",
                    "Loop end j from i to n - 1, summing elements.",
                    "If sum >= target, minLen = min(minLen, j - i + 1)."
                ],
                "whySlow": "Evaluating all subarrays takes quadratic O(n²) time.",
                "time": "O(n²)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int minSubArrayLen(int target, int[] nums) {
        int minLen = Integer.MAX_VALUE;
        for (int i = 0; i < nums.length; i++) {
            int sum = 0;
            for (int j = i; j < nums.length; j++) {
                sum += nums[j];
                if (sum >= target) { minLen = Math.min(minLen, j - i + 1); break; }
            }
        }
        return minLen == Integer.MAX_VALUE ? 0 : minLen;
    }
}""",
                    "python": """class Solution:
    def minSubArrayLen(self, target: int, nums: list[int]) -> int:
        min_len = float('inf')
        for i in range(len(nums)):
            s = 0
            for j in range(i, len(nums)):
                s += nums[j]
                if s >= target:
                    min_len = min(min_len, j - i + 1)
                    break
        return 0 if min_len == float('inf') else min_len"""
                }
            },
            "optimal": {
                "idea": "Two pointers: expand right adding nums[right] to sum. While sum >= target, update minLen and subtract nums[left], incrementing left.",
                "steps": [
                    "Initialize left = 0, sum = 0, minLen = Integer.MAX_VALUE.",
                    "For right = 0 to n - 1:",
                    "sum += nums[right].",
                    "While sum >= target: minLen = min(minLen, right - left + 1), sum -= nums[left++].",
                    "Return minLen if updated, else 0."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int minSubArrayLen(int target, int[] nums) {
        int l = 0, sum = 0, min = Integer.MAX_VALUE;
        for (int r = 0; r < nums.length; r++) {
            sum += nums[r];
            while (sum >= target) {
                min = Math.min(min, r - l + 1);
                sum -= nums[l++];
            }
        }
        return min == Integer.MAX_VALUE ? 0 : min;
    }
}""",
                    "python": """class Solution:
    def minSubArrayLen(self, target: int, nums: list[int]) -> int:
        l = 0
        s = 0
        min_l = float('inf')
        for r in range(len(nums)):
            s += nums[r]
            while s >= target:
                min_l = min(min_l, r - l + 1)
                s -= nums[l]
                l += 1
        return 0 if min_l == float('inf') else min_l"""
                }
            }
        },
        {
            "seq": 43,
            "whyNext": "Builds on dynamic window: counting subarrays where product < k by adding (right - left + 1) at each expansion step.",
            "brute": {
                "idea": "Calculate the product of every subarray and count those strictly less than k.",
                "steps": [
                    "Loop i from 0 to n - 1.",
                    "Maintain running product prod = 1.",
                    "Loop j from i to n - 1: prod *= nums[j]; if prod < k increment count, else break."
                ],
                "whySlow": "Evaluating all subarrays takes O(n²) time.",
                "time": "O(n²)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int numSubarrayProductLessThanK(int[] nums, int k) {
        if (k <= 1) return 0;
        int count = 0;
        for (int i = 0; i < nums.length; i++) {
            int prod = 1;
            for (int j = i; j < nums.length; j++) {
                prod *= nums[j];
                if (prod < k) count++;
                else break;
            }
        }
        return count;
    }
}""",
                    "python": """class Solution:
    def numSubarrayProductLessThanK(self, nums: list[int], k: int) -> int:
        if k <= 1: return 0
        count = 0
        for i in range(len(nums)):
            p = 1
            for j in range(i, len(nums)):
                p *= nums[j]
                if p < k: count += 1
                else: break
        return count"""
                }
            },
            "optimal": {
                "idea": "Sliding window: multiply prod *= nums[right]. While prod >= k, prod /= nums[left++]. Add (right - left + 1) to count.",
                "steps": [
                    "If k <= 1, return 0.",
                    "Initialize left = 0, prod = 1, count = 0.",
                    "For right = 0 to n - 1:",
                    "prod *= nums[right].",
                    "While prod >= k, prod /= nums[left++].",
                    "count += right - left + 1."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int numSubarrayProductLessThanK(int[] nums, int k) {
        if (k <= 1) return 0;
        int count = 0, l = 0, prod = 1;
        for (int r = 0; r < nums.length; r++) {
            prod *= nums[r];
            while (prod >= k) prod /= nums[l++];
            count += r - l + 1;
        }
        return count;
    }
}""",
                    "python": """class Solution:
    def numSubarrayProductLessThanK(self, nums: list[int], k: int) -> int:
        if k <= 1: return 0
        l, prod, count = 0, 1, 0
        for r, x in enumerate(nums):
            prod *= x
            while prod >= k:
                prod //= nums[l]
                l += 1
            count += r - l + 1
        return count"""
                }
            }
        },
        {
            "seq": 44,
            "whyNext": "Builds on sliding window with distinct element counts: shrink window when number of distinct fruit types exceeds 2.",
            "brute": {
                "idea": "For each starting tree i, extend until encountering a 3rd distinct fruit type.",
                "steps": [
                    "Loop i from 0 to n - 1.",
                    "Track distinct fruits with a set.",
                    "Advance j until set size > 2.",
                    "Update max length with j - i."
                ],
                "whySlow": "Evaluating every starting position takes O(n²) time.",
                "time": "O(n²)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int totalFruit(int[] fruits) {
        int max = 0;
        for (int i = 0; i < fruits.length; i++) {
            Set<Integer> set = new HashSet<>();
            for (int j = i; j < fruits.length; j++) {
                set.add(fruits[j]);
                if (set.size() > 2) break;
                max = Math.max(max, j - i + 1);
            }
        }
        return max;
    }
}""",
                    "python": """class Solution:
    def totalFruit(self, fruits: list[int]) -> int:
        max_f = 0
        for i in range(len(fruits)):
            s = set()
            for j in range(i, len(fruits)):
                s.add(fruits[j])
                if len(s) > 2: break
                max_f = max(max_f, j - i + 1)
        return max_f"""
                }
            },
            "optimal": {
                "idea": "Sliding window with frequency map: expand right; when map size > 2, decrement count of fruits[left] and shrink until size <= 2.",
                "steps": [
                    "Map count of each fruit type.",
                    "Loop right from 0 to n - 1, adding fruits[right] to map.",
                    "While map.size() > 2, decrement fruits[left]; remove from map if count reaches 0, then left++.",
                    "maxLen = max(maxLen, right - left + 1)."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int totalFruit(int[] fruits) {
        Map<Integer, Integer> map = new HashMap<>();
        int l = 0, max = 0;
        for (int r = 0; r < fruits.length; r++) {
            map.put(fruits[r], map.getOrDefault(fruits[r], 0) + 1);
            while (map.size() > 2) {
                map.put(fruits[l], map.get(fruits[l]) - 1);
                if (map.get(fruits[l]) == 0) map.remove(fruits[l]);
                l++;
            }
            max = Math.max(max, r - l + 1);
        }
        return max;
    }
}""",
                    "python": """class Solution:
    def totalFruit(self, fruits: list[int]) -> int:
        count = collections.defaultdict(int)
        l, max_f = 0, 0
        for r, f in enumerate(fruits):
            count[f] += 1
            while len(count) > 2:
                count[fruits[l]] -= 1
                if count[fruits[l]] == 0:
                    del count[fruits[l]]
                l += 1
            max_f = max(max_f, r - l + 1)
        return max_f"""
                }
            }
        },
        {
            "seq": 45,
            "whyNext": "Builds on Fruit Into Baskets: sliding window allowing at most k zeroes (analogous to allowing k flips).",
            "brute": {
                "idea": "For every starting point, extend subarray counting zeroes until zeroes exceed k.",
                "steps": [
                    "Loop i from 0 to n - 1.",
                    "Count zeros; stop when zeros > k.",
                    "Update max length."
                ],
                "whySlow": "Evaluating every starting position takes O(n²) time.",
                "time": "O(n²)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int longestOnes(int[] nums, int k) {
        int max = 0;
        for (int i = 0; i < nums.length; i++) {
            int zeros = 0;
            for (int j = i; j < nums.length; j++) {
                if (nums[j] == 0) zeros++;
                if (zeros > k) break;
                max = Math.max(max, j - i + 1);
            }
        }
        return max;
    }
}""",
                    "python": """class Solution:
    def longestOnes(self, nums: list[int], k: int) -> int:
        max_l = 0
        for i in range(len(nums)):
            z = 0
            for j in range(i, len(nums)):
                if nums[j] == 0: z += 1
                if z > k: break
                max_l = max(max_l, j - i + 1)
        return max_l"""
                }
            },
            "optimal": {
                "idea": "Sliding window: expand right. When nums[right] == 0, increment zeroCount. While zeroCount > k, if nums[left] == 0 decrement zeroCount, and left++.",
                "steps": [
                    "Initialize left = 0, zeroCount = 0, maxLen = 0.",
                    "For right = 0 to n - 1:",
                    "If nums[right] == 0, zeroCount++.",
                    "While zeroCount > k, if nums[left] == 0 zeroCount--, left++.",
                    "maxLen = max(maxLen, right - left + 1)."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int longestOnes(int[] nums, int k) {
        int l = 0, zeros = 0, max = 0;
        for (int r = 0; r < nums.length; r++) {
            if (nums[r] == 0) zeros++;
            while (zeros > k) {
                if (nums[l] == 0) zeros--;
                l++;
            }
            max = Math.max(max, r - l + 1);
        }
        return max;
    }
}""",
                    "python": """class Solution:
    def longestOnes(self, nums: list[int], k: int) -> int:
        l, zeros, max_l = 0, 0, 0
        for r, x in enumerate(nums):
            if x == 0: zeros += 1
            while zeros > k:
                if nums[l] == 0: zeros -= 1
                l += 1
            max_l = max(max_l, r - l + 1)
        return max_l"""
                }
            }
        },
        {
            "seq": 46,
            "whyNext": "Solves exact sum problem using sliding window: atMost(goal) - atMost(goal - 1), or prefix sum hash map.",
            "brute": {
                "idea": "Calculate the sum of all subarrays and count those equal to goal.",
                "steps": [
                    "Loop i from 0 to n - 1.",
                    "Loop j from i to n - 1, maintaining sum.",
                    "If sum == goal, increment count."
                ],
                "whySlow": "Evaluating every subarray takes O(n²) time.",
                "time": "O(n²)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int numSubarraysWithSum(int[] nums, int goal) {
        int count = 0;
        for (int i = 0; i < nums.length; i++) {
            int sum = 0;
            for (int j = i; j < nums.length; j++) {
                sum += nums[j];
                if (sum == goal) count++;
            }
        }
        return count;
    }
}""",
                    "python": """class Solution:
    def numSubarraysWithSum(self, nums: list[int], goal: int) -> int:
        count = 0
        for i in range(len(nums)):
            s = 0
            for j in range(i, len(nums)):
                s += nums[j]
                if s == goal: count += 1
        return count"""
                }
            },
            "optimal": {
                "idea": "Use the atMost trick: exact(goal) = atMost(goal) - atMost(goal - 1), each computed with sliding window in O(n).",
                "steps": [
                    "Define helper atMost(S): count subarrays with sum <= S using sliding window.",
                    "If S < 0, return 0.",
                    "Expand right adding nums[right] to sum; shrink left while sum > S; add (right - left + 1) to total.",
                    "Return atMost(goal) - atMost(goal - 1)."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int numSubarraysWithSum(int[] nums, int goal) {
        return atMost(nums, goal) - atMost(nums, goal - 1);
    }
    private int atMost(int[] nums, int s) {
        if (s < 0) return 0;
        int l = 0, sum = 0, count = 0;
        for (int r = 0; r < nums.length; r++) {
            sum += nums[r];
            while (sum > s) sum -= nums[l++];
            count += r - l + 1;
        }
        return count;
    }
}""",
                    "python": """class Solution:
    def numSubarraysWithSum(self, nums: list[int], goal: int) -> int:
        def at_most(s):
            if s < 0: return 0
            l, curr, count = 0, 0, 0
            for r, x in enumerate(nums):
                curr += x
                while curr > s:
                    curr -= nums[l]
                    l += 1
                count += r - l + 1
            return count
        return at_most(goal) - at_most(goal - 1)"""
                }
            }
        },
        {
            "seq": 47,
            "whyNext": "Builds on Find All Anagrams: dynamically expand window until all target characters satisfied, then shrink left to find minimal substring.",
            "brute": {
                "idea": "Examine every substring of s and check if it contains all characters of t in required quantities.",
                "steps": [
                    "Loop start i from 0 to n - 1.",
                    "Loop end j from i to n - 1.",
                    "Check if frequency of every char in t is satisfied in s[i...j].",
                    "Track shortest valid substring."
                ],
                "whySlow": "Checking all substrings takes O(n²) time.",
                "time": "O(n²)",
                "space": "O(t)",
                "code": {
                    "java": """class Solution {
    public String minWindow(String s, String t) {
        if (s.length() < t.length()) return "";
        Map<Character, Integer> tMap = new HashMap<>();
        for (char c : t.toCharArray()) tMap.put(c, tMap.getOrDefault(c, 0) + 1);
        String minStr = "";
        int minLen = Integer.MAX_VALUE;
        for (int i = 0; i < s.length(); i++) {
            Map<Character, Integer> sMap = new HashMap<>();
            for (int j = i; j < s.length(); j++) {
                char c = s.charAt(j);
                sMap.put(c, sMap.getOrDefault(c, 0) + 1);
                boolean valid = true;
                for (char tc : tMap.keySet()) {
                    if (sMap.getOrDefault(tc, 0) < tMap.get(tc)) { valid = false; break; }
                }
                if (valid && (j - i + 1) < minLen) {
                    minLen = j - i + 1;
                    minStr = s.substring(i, j + 1);
                    break;
                }
            }
        }
        return minStr;
    }
}""",
                    "python": """class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if len(s) < len(t): return ""
        t_count = collections.Counter(t)
        min_str = ""
        min_len = float('inf')
        for i in range(len(s)):
            s_count = collections.Counter()
            for j in range(i, len(s)):
                s_count[s[j]] += 1
                if all(s_count[c] >= t_count[c] for c in t_count):
                    if j - i + 1 < min_len:
                        min_len = j - i + 1
                        min_str = s[i:j+1]
                    break
        return min_str"""
                }
            },
            "optimal": {
                "idea": "Two pointers with formed match counter: expand right to satisfy all characters; shrink left to minimize window length.",
                "steps": [
                    "Map character requirements of t into count array.",
                    "Track required matches needed vs formed.",
                    "Expand right: decrement count; if count[c] >= 0, formed++.",
                    "While formed == t.length: update min window, increment count for s[left]; if count > 0, formed--, left++.",
                    "Return min window."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public String minWindow(String s, String t) {
        if (s.length() < t.length()) return "";
        int[] map = new int[128];
        for (char c : t.toCharArray()) map[c]++;
        int count = t.length(), l = 0, minLen = Integer.MAX_VALUE, start = 0;
        for (int r = 0; r < s.length(); r++) {
            if (map[s.charAt(r)]-- > 0) count--;
            while (count == 0) {
                if (r - l + 1 < minLen) { minLen = r - l + 1; start = l; }
                if (++map[s.charAt(l++)] > 0) count++;
            }
        }
        return minLen == Integer.MAX_VALUE ? "" : s.substring(start, start + minLen);
    }
}""",
                    "python": """class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if len(s) < len(t): return ""
        counts = collections.Counter(t)
        needed = len(t)
        l, start, min_len = 0, 0, float('inf')
        for r, c in enumerate(s):
            if counts[c] > 0: needed -= 1
            counts[c] -= 1
            while needed == 0:
                if r - l + 1 < min_len:
                    min_len = r - l + 1
                    start = l
                counts[s[l]] += 1
                if counts[s[l]] > 0: needed += 1
                l += 1
        return "" if min_len == float('inf') else s[start:start+min_len]"""
                }
            }
        },
        {
            "seq": 48,
            "whyNext": "Maintains sliding window extremum: monotonic deque stores indices of decreasing elements, answering maximum in O(1).",
            "brute": {
                "idea": "For every window of length k, scan all k elements to locate the maximum.",
                "steps": [
                    "Loop i from 0 to n - k.",
                    "Scan nums[i ... i + k - 1] to find maximum value.",
                    "Record maximum in result."
                ],
                "whySlow": "Scanning each of n - k + 1 windows takes O(nk) time.",
                "time": "O(nk)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int[] maxSlidingWindow(int[] nums, int k) {
        int n = nums.length;
        int[] res = new int[n - k + 1];
        for (int i = 0; i <= n - k; i++) {
            int max = nums[i];
            for (int j = i + 1; j < i + k; j++) max = Math.max(max, nums[j]);
            res[i] = max;
        }
        return res;
    }
}""",
                    "python": """class Solution:
    def maxSlidingWindow(self, nums: list[int], k: int) -> list[int]:
        return [max(nums[i:i+k]) for i in range(len(nums) - k + 1)]"""
                }
            },
            "optimal": {
                "idea": "Monotonic decreasing deque storing indices: remove indices outside current window from front; remove smaller elements from back.",
                "steps": [
                    "Initialize an ArrayDeque of indices.",
                    "For each index i:",
                    "Remove front indices if out of window (q.peekFirst() <= i - k).",
                    "Remove back indices while nums[q.peekLast()] <= nums[i].",
                    "Add i to back.",
                    "When i >= k - 1, nums[q.peekFirst()] is window maximum."
                ],
                "time": "O(n)",
                "space": "O(k)",
                "code": {
                    "java": """class Solution {
    public int[] maxSlidingWindow(int[] nums, int k) {
        int n = nums.length;
        int[] res = new int[n - k + 1];
        Deque<Integer> q = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            while (!q.isEmpty() && q.peekFirst() < i - k + 1) q.pollFirst();
            while (!q.isEmpty() && nums[q.peekLast()] < nums[i]) q.pollLast();
            q.offerLast(i);
            if (i >= k - 1) res[i - k + 1] = nums[q.peekFirst()];
        }
        return res;
    }
}""",
                    "python": """class Solution:
    def maxSlidingWindow(self, nums: list[int], k: int) -> list[int]:
        q = collections.deque()
        res = []
        for i, x in enumerate(nums):
            while q and q[0] < i - k + 1:
                q.popleft()
            while q and nums[q[-1]] < x:
                q.pop()
            q.append(i)
            if i >= k - 1:
                res.append(nums[q[0]])
        return res"""
                }
            }
        },
        {
            "seq": 49,
            "whyNext": "Completes Chapter 3: applies the atMost trick with distinct count map: exact(K) = atMost(K) - atMost(K - 1).",
            "brute": {
                "idea": "For each starting index i, expand j and count distinct elements with a set until distinct count exceeds k.",
                "steps": [
                    "Loop i from 0 to n - 1.",
                    "Track distinct elements in a set.",
                    "If set.size() == k, increment count; if > k, break."
                ],
                "whySlow": "Evaluating every subarray takes O(n²) time.",
                "time": "O(n²)",
                "space": "O(k)",
                "code": {
                    "java": """class Solution {
    public int subarraysWithKDistinct(int[] nums, int k) {
        int count = 0;
        for (int i = 0; i < nums.length; i++) {
            Set<Integer> set = new HashSet<>();
            for (int j = i; j < nums.length; j++) {
                set.add(nums[j]);
                if (set.size() == k) count++;
                else if (set.size() > k) break;
            }
        }
        return count;
    }
}""",
                    "python": """class Solution:
    def subarraysWithKDistinct(self, nums: list[int], k: int) -> int:
        count = 0
        for i in range(len(nums)):
            s = set()
            for j in range(i, len(nums)):
                s.add(nums[j])
                if len(s) == k: count += 1
                elif len(s) > k: break
        return count"""
                }
            },
            "optimal": {
                "idea": "atMost helper: count subarrays with at most K distinct elements using sliding window. Answer is atMost(k) - atMost(k - 1).",
                "steps": [
                    "Define atMost(K): expand right adding to frequency map; while map.size() > K, decrement nums[left] and left++; add (right - left + 1) to sum.",
                    "Return atMost(k) - atMost(k - 1)."
                ],
                "time": "O(n)",
                "space": "O(k)",
                "code": {
                    "java": """class Solution {
    public int subarraysWithKDistinct(int[] nums, int k) {
        return atMost(nums, k) - atMost(nums, k - 1);
    }
    private int atMost(int[] nums, int k) {
        Map<Integer, Integer> map = new HashMap<>();
        int l = 0, count = 0;
        for (int r = 0; r < nums.length; r++) {
            map.put(nums[r], map.getOrDefault(nums[r], 0) + 1);
            while (map.size() > k) {
                map.put(nums[l], map.get(nums[l]) - 1);
                if (map.get(nums[l]) == 0) map.remove(nums[l]);
                l++;
            }
            count += r - l + 1;
        }
        return count;
    }
}""",
                    "python": """class Solution:
    def subarraysWithKDistinct(self, nums: list[int], k: int) -> int:
        def at_most(k_distinct):
            count = collections.defaultdict(int)
            l, total = 0, 0
            for r, x in enumerate(nums):
                count[x] += 1
                while len(count) > k_distinct:
                    count[nums[l]] -= 1
                    if count[nums[l]] == 0:
                        del count[nums[l]]
                    l += 1
                total += r - l + 1
            return total
        return at_most(k) - at_most(k - 1)"""
                }
            }
        },
        {
            "seq": 50,
            "whyNext": "Opens Chapter 4 (Binary Search): canonical binary search halving the search space in sorted order.",
            "brute": {
                "idea": "Perform a linear scan across nums comparing each element with target.",
                "steps": [
                    "Loop index i from 0 to n - 1.",
                    "If nums[i] == target, return i.",
                    "If loop finishes, return -1."
                ],
                "whySlow": "Linear scan checks up to n elements, ignoring sorted order.",
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int search(int[] nums, int target) {
        for (int i = 0; i < nums.length; i++) {
            if (nums[i] == target) return i;
        }
        return -1;
    }
}""",
                    "python": """class Solution:
    def search(self, nums: list[int], target: int) -> int:
        for i, x in enumerate(nums):
            if x == target: return i
        return -1"""
                }
            },
            "optimal": {
                "idea": "Binary search: check mid element. If target < nums[mid] search left half, else if target > nums[mid] search right half.",
                "steps": [
                    "Initialize left = 0, right = nums.length - 1.",
                    "While left <= right:",
                    "mid = left + (right - left) / 2.",
                    "If nums[mid] == target, return mid.",
                    "Else if nums[mid] < target, left = mid + 1.",
                    "Else right = mid - 1.",
                    "Return -1 if not found."
                ],
                "time": "O(log n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int search(int[] nums, int target) {
        int l = 0, r = nums.length - 1;
        while (l <= r) {
            int mid = l + (r - l) / 2;
            if (nums[mid] == target) return mid;
            if (nums[mid] < target) l = mid + 1;
            else r = mid - 1;
        }
        return -1;
    }
}""",
                    "python": """class Solution:
    def search(self, nums: list[int], target: int) -> int:
        l, r = 0, len(nums) - 1
        while l <= r:
            mid = (l + r) // 2
            if nums[mid] == target: return mid
            elif nums[mid] < target: l = mid + 1
            else: r = mid - 1
        return -1"""
                }
            }
        }
    ]


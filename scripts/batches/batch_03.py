# Batch 3: Seq 51 to 75
# Covers Chapter 4 Binary Search (51 to 67) and Chapter 5 Stack (68 to 75)

def get_batch():
    return [
        {
            "seq": 51,
            "whyNext": "Builds on Binary Search: lower-bound search finding index of target or insertion point where it belongs.",
            "brute": {
                "idea": "Perform linear search from left to right; return index of first element >= target.",
                "steps": [
                    "Loop i from 0 to n - 1.",
                    "If nums[i] >= target, return i.",
                    "Return n if target is greater than all elements."
                ],
                "whySlow": "Linear scan takes O(n) time.",
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int searchInsert(int[] nums, int target) {
        for (int i = 0; i < nums.length; i++) {
            if (nums[i] >= target) return i;
        }
        return nums.length;
    }
}""",
                    "python": """class Solution:
    def searchInsert(self, nums: list[int], target: int) -> int:
        for i, x in enumerate(nums):
            if x >= target: return i
        return len(nums)"""
                }
            },
            "optimal": {
                "idea": "Binary search lower bound: if target <= nums[mid], search left half; otherwise search right half. The left pointer lands on insertion point.",
                "steps": [
                    "Initialize l = 0, r = nums.length - 1.",
                    "While l <= r:",
                    "mid = l + (r - l) / 2.",
                    "If nums[mid] == target, return mid.",
                    "If nums[mid] < target, l = mid + 1, else r = mid - 1.",
                    "Return l."
                ],
                "time": "O(log n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int searchInsert(int[] nums, int target) {
        int l = 0, r = nums.length - 1;
        while (l <= r) {
            int mid = l + (r - l) / 2;
            if (nums[mid] == target) return mid;
            if (nums[mid] < target) l = mid + 1;
            else r = mid - 1;
        }
        return l;
    }
}""",
                    "python": """class Solution:
    def searchInsert(self, nums: list[int], target: int) -> int:
        l, r = 0, len(nums) - 1
        while l <= r:
            mid = (l + r) // 2
            if nums[mid] == target: return mid
            elif nums[mid] < target: l = mid + 1
            else: r = mid - 1
        return l"""
                }
            }
        },
        {
            "seq": 52,
            "whyNext": "Builds on Search Insert Position: binary search for the boundary between false (good) and true (bad) versions.",
            "brute": {
                "idea": "Test every version sequentially starting from 1 until isBadVersion returns true.",
                "steps": [
                    "Loop v from 1 to n.",
                    "If isBadVersion(v) is true, return v."
                ],
                "whySlow": "Testing up to n versions sequentially takes O(n) API calls.",
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    boolean isBadVersion(int version) { return version >= 1; }
    public int firstBadVersion(int n) {
        for (int i = 1; i <= n; i++) {
            if (isBadVersion(i)) return i;
        }
        return n;
    }
}""",
                    "python": """class Solution:
    def isBadVersion(self, version: int) -> bool:
        return version >= 1
    def firstBadVersion(self, n: int) -> int:
        for i in range(1, n + 1):
            if self.isBadVersion(i): return i
        return n"""
                }
            },
            "optimal": {
                "idea": "Binary search on versions: if mid is bad, the first bad version is at or before mid (r = mid); else l = mid + 1.",
                "steps": [
                    "Initialize l = 1, r = n.",
                    "While l < r:",
                    "mid = l + (r - l) / 2.",
                    "If isBadVersion(mid) is true, r = mid.",
                    "Else l = mid + 1.",
                    "Return l."
                ],
                "time": "O(log n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    boolean isBadVersion(int version) { return version >= 1; }
    public int firstBadVersion(int n) {
        int l = 1, r = n;
        while (l < r) {
            int mid = l + (r - l) / 2;
            if (isBadVersion(mid)) r = mid;
            else l = mid + 1;
        }
        return l;
    }
}""",
                    "python": """class Solution:
    def isBadVersion(self, version: int) -> bool:
        return version >= 1
    def firstBadVersion(self, n: int) -> int:
        l, r = 1, n
        while l < r:
            mid = (l + r) // 2
            if self.isBadVersion(mid): r = mid
            else: l = mid + 1
        return l"""
                }
            }
        },
        {
            "seq": 53,
            "whyNext": "Builds on First Bad Version: search domain is the integer range [1, num] to determine if mid * mid == num.",
            "brute": {
                "idea": "Check all integers i = 1, 2, ... while i * i <= num.",
                "steps": [
                    "Loop i starting at 1.",
                    "If i * i == num, return true.",
                    "If i * i > num, return false.",
                    "i++."
                ],
                "whySlow": "Checking linearly up to √num takes O(√num) iterations.",
                "time": "O(√n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public boolean isPerfectSquare(int num) {
        long i = 1;
        while (i * i <= num) {
            if (i * i == num) return true;
            i++;
        }
        return false;
    }
}""",
                    "python": """class Solution:
    def isPerfectSquare(self, num: int) -> bool:
        i = 1
        while i * i <= num:
            if i * i == num: return True
            i += 1
        return False"""
                }
            },
            "optimal": {
                "idea": "Binary search on range [1, num]: calculate mid * mid and narrow search range.",
                "steps": [
                    "Initialize l = 1, r = num.",
                    "While l <= r:",
                    "mid = l + (r - l) / 2, sq = (long) mid * mid.",
                    "If sq == num, return true.",
                    "If sq < num, l = mid + 1, else r = mid - 1.",
                    "Return false."
                ],
                "time": "O(log n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public boolean isPerfectSquare(int num) {
        long l = 1, r = num;
        while (l <= r) {
            long mid = l + (r - l) / 2;
            long sq = mid * mid;
            if (sq == num) return true;
            if (sq < num) l = mid + 1;
            else r = mid - 1;
        }
        return false;
    }
}""",
                    "python": """class Solution:
    def isPerfectSquare(self, num: int) -> bool:
        l, r = 1, num
        while l <= r:
            mid = (l + r) // 2
            sq = mid * mid
            if sq == num: return True
            elif sq < num: l = mid + 1
            else: r = mid - 1
        return False"""
                }
            }
        },
        {
            "seq": 54,
            "whyNext": "Builds on Valid Perfect Square: binary search for the largest integer whose square is <= x.",
            "brute": {
                "idea": "Increment integer i starting from 1 until (i + 1) * (i + 1) > x.",
                "steps": [
                    "If x == 0, return 0.",
                    "Loop i from 1 upward while (long)(i + 1) * (i + 1) <= x.",
                    "Return i."
                ],
                "whySlow": "Checking sequentially takes O(√x) time.",
                "time": "O(√x)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int mySqrt(int x) {
        if (x < 2) return x;
        long i = 1;
        while ((i + 1) * (i + 1) <= x) i++;
        return (int) i;
    }
}""",
                    "python": """class Solution:
    def mySqrt(self, x: int) -> int:
        if x < 2: return x
        i = 1
        while (i + 1) * (i + 1) <= x:
            i += 1
        return i"""
                }
            },
            "optimal": {
                "idea": "Binary search in range [1, x]: find highest mid where mid * mid <= x.",
                "steps": [
                    "If x < 2, return x.",
                    "Initialize l = 1, r = x / 2, ans = 1.",
                    "While l <= r:",
                    "mid = l + (r - l) / 2.",
                    "If (long) mid * mid <= x, ans = mid, l = mid + 1.",
                    "Else r = mid - 1.",
                    "Return ans."
                ],
                "time": "O(log x)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int mySqrt(int x) {
        if (x < 2) return x;
        int l = 1, r = x / 2, ans = 1;
        while (l <= r) {
            int mid = l + (r - l) / 2;
            if ((long) mid * mid <= x) { ans = mid; l = mid + 1; }
            else r = mid - 1;
        }
        return ans;
    }
}""",
                    "python": """class Solution:
    def mySqrt(self, x: int) -> int:
        if x < 2: return x
        l, r, ans = 1, x // 2, 1
        while l <= r:
            mid = (l + r) // 2
            if mid * mid <= x:
                ans = mid
                l = mid + 1
            else:
                r = mid - 1
        return ans"""
                }
            }
        },
        {
            "seq": 55,
            "whyNext": "Builds on Search Insert Position: run two binary searches to find the first occurrence and last occurrence of target.",
            "brute": {
                "idea": "Linear scan to record first and last indices where nums[i] == target.",
                "steps": [
                    "Loop through nums, finding first occurrence and last occurrence of target.",
                    "Return [-1, -1] if not found."
                ],
                "whySlow": "Scanning the whole array takes linear O(n) time.",
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int[] searchRange(int[] nums, int target) {
        int first = -1, last = -1;
        for (int i = 0; i < nums.length; i++) {
            if (nums[i] == target) {
                if (first == -1) first = i;
                last = i;
            }
        }
        return new int[]{first, last};
    }
}""",
                    "python": """class Solution:
    def searchRange(self, nums: list[int], target: int) -> list[int]:
        first, last = -1, -1
        for i, x in enumerate(nums):
            if x == target:
                if first == -1: first = i
                last = i
        return [first, last]"""
                }
            },
            "optimal": {
                "idea": "Two binary searches: first finds leftmost match (when nums[mid] == target, r = mid - 1); second finds rightmost match (l = mid + 1).",
                "steps": [
                    "findFirst(target): binary search, when nums[mid] == target record ans and continue left.",
                    "findLast(target): binary search, when nums[mid] == target record ans and continue right.",
                    "Return [first, last]."
                ],
                "time": "O(log n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int[] searchRange(int[] nums, int target) {
        return new int[]{findBound(nums, target, true), findBound(nums, target, false)};
    }
    private int findBound(int[] nums, int target, boolean isFirst) {
        int l = 0, r = nums.length - 1, ans = -1;
        while (l <= r) {
            int mid = l + (r - l) / 2;
            if (nums[mid] == target) {
                ans = mid;
                if (isFirst) r = mid - 1;
                else l = mid + 1;
            } else if (nums[mid] < target) l = mid + 1;
            else r = mid - 1;
        }
        return ans;
    }
}""",
                    "python": """class Solution:
    def searchRange(self, nums: list[int], target: int) -> list[int]:
        def bound(is_first):
            l, r, ans = 0, len(nums) - 1, -1
            while l <= r:
                mid = (l + r) // 2
                if nums[mid] == target:
                    ans = mid
                    if is_first: r = mid - 1
                    else: l = mid + 1
                elif nums[mid] < target: l = mid + 1
                else: r = mid - 1
            return ans
        return [bound(True), bound(False)]"""
                }
            }
        },
        {
            "seq": 56,
            "whyNext": "Builds on binary search in sorted arrays: in a rotated sorted array, at least one half [l, mid] or [mid, r] is always normally sorted.",
            "brute": {
                "idea": "Linear scan across nums to locate target.",
                "steps": [
                    "Loop i from 0 to n - 1.",
                    "If nums[i] == target, return i.",
                    "Return -1 if loop ends."
                ],
                "whySlow": "Ignores the piecewise sorted property of the rotated array, taking O(n) time.",
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int search(int[] nums, int target) {
        for (int i = 0; i < nums.length; i++) if (nums[i] == target) return i;
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
                "idea": "Binary search: identify which half is sorted. If left half is sorted and target falls in it, search left; otherwise search right.",
                "steps": [
                    "While l <= r:",
                    "mid = l + (r - l) / 2.",
                    "If nums[mid] == target, return mid.",
                    "If left half sorted (nums[l] <= nums[mid]):",
                    "If target in [nums[l], nums[mid]), r = mid - 1, else l = mid + 1.",
                    "Else (right half sorted):",
                    "If target in (nums[mid], nums[r]], l = mid + 1, else r = mid - 1."
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
            if (nums[l] <= nums[mid]) {
                if (target >= nums[l] && target < nums[mid]) r = mid - 1;
                else l = mid + 1;
            } else {
                if (target > nums[mid] && target <= nums[r]) l = mid + 1;
                else r = mid - 1;
            }
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
            if nums[l] <= nums[mid]:
                if nums[l] <= target < nums[mid]: r = mid - 1
                else: l = mid + 1
            else:
                if nums[mid] < target <= nums[r]: l = mid + 1
                else: r = mid - 1
        return -1"""
                }
            }
        },
        {
            "seq": 57,
            "whyNext": "Builds on Search in Rotated Sorted Array: with duplicates, when nums[l] == nums[mid] == nums[r], shrink both boundaries.",
            "brute": {
                "idea": "Perform a linear scan to check if target exists in nums.",
                "steps": [
                    "Loop through all elements in nums.",
                    "If nums[i] == target, return true.",
                    "Return false."
                ],
                "whySlow": "Linear scan does not exploit sorted segments.",
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public boolean search(int[] nums, int target) {
        for (int x : nums) if (x == target) return true;
        return false;
    }
}""",
                    "python": """class Solution:
    def search(self, nums: list[int], target: int) -> bool:
        return target in nums"""
                }
            },
            "optimal": {
                "idea": "Modified binary search: when nums[l] == nums[mid] == nums[r], we cannot determine the sorted half, so increment l and decrement r.",
                "steps": [
                    "While l <= r:",
                    "If nums[mid] == target, return true.",
                    "If nums[l] == nums[mid] && nums[mid] == nums[r]: l++, r--, continue.",
                    "Else determine sorted half as in Search in Rotated Sorted Array.",
                    "Return false."
                ],
                "time": "O(log n) average",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public boolean search(int[] nums, int target) {
        int l = 0, r = nums.length - 1;
        while (l <= r) {
            int mid = l + (r - l) / 2;
            if (nums[mid] == target) return true;
            if (nums[l] == nums[mid] && nums[mid] == nums[r]) {
                l++; r--;
            } else if (nums[l] <= nums[mid]) {
                if (target >= nums[l] && target < nums[mid]) r = mid - 1;
                else l = mid + 1;
            } else {
                if (target > nums[mid] && target <= nums[r]) l = mid + 1;
                else r = mid - 1;
            }
        }
        return false;
    }
}""",
                    "python": """class Solution:
    def search(self, nums: list[int], target: int) -> bool:
        l, r = 0, len(nums) - 1
        while l <= r:
            mid = (l + r) // 2
            if nums[mid] == target: return True
            if nums[l] == nums[mid] == nums[r]:
                l += 1; r -= 1
            elif nums[l] <= nums[mid]:
                if nums[l] <= target < nums[mid]: r = mid - 1
                else: l = mid + 1
            else:
                if nums[mid] < target <= nums[r]: l = mid + 1
                else: r = mid - 1
        return False"""
                }
            }
        },
        {
            "seq": 58,
            "whyNext": "Builds on rotated array properties: compare nums[mid] with nums[r] to determine which half contains the inflection point (minimum).",
            "brute": {
                "idea": "Linear scan through array to find the global minimum.",
                "steps": [
                    "Initialize min = nums[0].",
                    "Scan all elements, updating min.",
                    "Return min."
                ],
                "whySlow": "Scanning all elements takes O(n) time.",
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int findMin(int[] nums) {
        int min = nums[0];
        for (int x : nums) min = Math.min(min, x);
        return min;
    }
}""",
                    "python": """class Solution:
    def findMin(self, nums: list[int]) -> int:
        return min(nums)"""
                }
            },
            "optimal": {
                "idea": "Binary search: if nums[mid] > nums[r], the minimum must be strictly in the right half (l = mid + 1); otherwise r = mid.",
                "steps": [
                    "Initialize l = 0, r = nums.length - 1.",
                    "While l < r:",
                    "mid = l + (r - l) / 2.",
                    "If nums[mid] > nums[r], l = mid + 1.",
                    "Else r = mid.",
                    "Return nums[l]."
                ],
                "time": "O(log n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int findMin(int[] nums) {
        int l = 0, r = nums.length - 1;
        while (l < r) {
            int mid = l + (r - l) / 2;
            if (nums[mid] > nums[r]) l = mid + 1;
            else r = mid;
        }
        return nums[l];
    }
}""",
                    "python": """class Solution:
    def findMin(self, nums: list[int]) -> int:
        l, r = 0, len(nums) - 1
        while l < r:
            mid = (l + r) // 2
            if nums[mid] > nums[r]: l = mid + 1
            else: r = mid
        return nums[l]"""
                }
            }
        },
        {
            "seq": 59,
            "whyNext": "Builds on inflection search: if nums[mid] < nums[mid + 1], an uphill slope guarantees a peak to the right.",
            "brute": {
                "idea": "Scan sequentially to find an element greater than its neighbours.",
                "steps": [
                    "Loop i from 0 to n - 1.",
                    "If nums[i] > nums[i + 1] (or at boundary), return i."
                ],
                "whySlow": "Linear scan takes O(n) time.",
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int findPeakElement(int[] nums) {
        for (int i = 0; i < nums.length - 1; i++) {
            if (nums[i] > nums[i + 1]) return i;
        }
        return nums.length - 1;
    }
}""",
                    "python": """class Solution:
    def findPeakElement(self, nums: list[int]) -> int:
        for i in range(len(nums) - 1):
            if nums[i] > nums[i + 1]: return i
        return len(nums) - 1"""
                }
            },
            "optimal": {
                "idea": "Binary search on slope: if nums[mid] < nums[mid + 1], move right (l = mid + 1); otherwise a peak exists on the left (r = mid).",
                "steps": [
                    "Initialize l = 0, r = nums.length - 1.",
                    "While l < r:",
                    "mid = l + (r - l) / 2.",
                    "If nums[mid] < nums[mid + 1], l = mid + 1.",
                    "Else r = mid.",
                    "Return l."
                ],
                "time": "O(log n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int findPeakElement(int[] nums) {
        int l = 0, r = nums.length - 1;
        while (l < r) {
            int mid = l + (r - l) / 2;
            if (nums[mid] < nums[mid + 1]) l = mid + 1;
            else r = mid;
        }
        return l;
    }
}""",
                    "python": """class Solution:
    def findPeakElement(self, nums: list[int]) -> int:
        l, r = 0, len(nums) - 1
        while l < r:
            mid = (l + r) // 2
            if nums[mid] < nums[mid + 1]: l = mid + 1
            else: r = mid
        return l"""
                }
            }
        },
        {
            "seq": 60,
            "whyNext": "Builds on index parity: before the single element, pairs start at even indices (mid ^ 1). After it, pairs start at odd indices.",
            "brute": {
                "idea": "XOR all elements in the array; duplicate pairs cancel to zero, leaving the single element.",
                "steps": [
                    "Initialize ans = 0.",
                    "XOR all numbers in nums.",
                    "Return ans."
                ],
                "whySlow": "XOR takes O(n) time, not exploiting the sorted arrangement.",
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int singleNonDuplicate(int[] nums) {
        int xor = 0;
        for (int x : nums) xor ^= x;
        return xor;
    }
}""",
                    "python": """class Solution:
    def singleNonDuplicate(self, nums: list[int]) -> int:
        ans = 0
        for x in nums: ans ^= x
        return ans"""
                }
            },
            "optimal": {
                "idea": "Binary search on index parity: if mid is even, pair partner is mid + 1; if nums[mid] == nums[mid ^ 1], single element is to the right.",
                "steps": [
                    "Initialize l = 0, r = nums.length - 1.",
                    "While l < r:",
                    "mid = l + (r - l) / 2.",
                    "If nums[mid] == nums[mid ^ 1], l = mid + 1.",
                    "Else r = mid.",
                    "Return nums[l]."
                ],
                "time": "O(log n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int singleNonDuplicate(int[] nums) {
        int l = 0, r = nums.length - 1;
        while (l < r) {
            int mid = l + (r - l) / 2;
            if (nums[mid] == nums[mid ^ 1]) l = mid + 1;
            else r = mid;
        }
        return nums[l];
    }
}""",
                    "python": """class Solution:
    def singleNonDuplicate(self, nums: list[int]) -> int:
        l, r = 0, len(nums) - 1
        while l < r:
            mid = (l + r) // 2
            if nums[mid] == nums[mid ^ 1]: l = mid + 1
            else: r = mid
        return nums[l]"""
                }
            }
        },
        {
            "seq": 61,
            "whyNext": "Builds on binary search: treat an m x n 2D sorted matrix as a virtual 1D sorted array of length m * n.",
            "brute": {
                "idea": "Scan every cell of the m x n matrix to look for target.",
                "steps": [
                    "Nested loops over row r and column c.",
                    "If matrix[r][c] == target, return true.",
                    "Return false."
                ],
                "whySlow": "Scanning all cells takes O(mn) time.",
                "time": "O(mn)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public boolean searchMatrix(int[][] matrix, int target) {
        for (int[] row : matrix) {
            for (int val : row) if (val == target) return true;
        }
        return false;
    }
}""",
                    "python": """class Solution:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        return any(target in row for row in matrix)"""
                }
            },
            "optimal": {
                "idea": "Standard binary search from index 0 to m*n - 1, mapping 1D index to matrix cell (mid / n, mid % n).",
                "steps": [
                    "m = matrix.length, n = matrix[0].length.",
                    "Initialize l = 0, r = m * n - 1.",
                    "While l <= r:",
                    "mid = l + (r - l) / 2, val = matrix[mid / n][mid % n].",
                    "If val == target return true; if val < target l = mid + 1; else r = mid - 1.",
                    "Return false."
                ],
                "time": "O(log mn)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public boolean searchMatrix(int[][] matrix, int target) {
        int m = matrix.length, n = matrix[0].length;
        int l = 0, r = m * n - 1;
        while (l <= r) {
            int mid = l + (r - l) / 2;
            int val = matrix[mid / n][mid % n];
            if (val == target) return true;
            if (val < target) l = mid + 1;
            else r = mid - 1;
        }
        return false;
    }
}""",
                    "python": """class Solution:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        m, n = len(matrix), len(matrix[0])
        l, r = 0, m * n - 1
        while l <= r:
            mid = (l + r) // 2
            val = matrix[mid // n][mid % n]
            if val == target: return True
            elif val < target: l = mid + 1
            else: r = mid - 1
        return False"""
                }
            }
        },
        {
            "seq": 62,
            "whyNext": "Builds on Search a 2D Matrix: matrix rows and columns are independently sorted; walk from top-right corner in O(m + n).",
            "brute": {
                "idea": "Scan every element in the matrix.",
                "steps": [
                    "Loop through all rows and columns.",
                    "If matrix[r][c] == target, return true.",
                    "Return false."
                ],
                "whySlow": "Scanning all cells takes O(mn) time.",
                "time": "O(mn)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public boolean searchMatrix(int[][] matrix, int target) {
        for (int[] row : matrix) {
            for (int val : row) if (val == target) return true;
        }
        return false;
    }
}""",
                    "python": """class Solution:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        return any(target in row for row in matrix)"""
                }
            },
            "optimal": {
                "idea": "Staircase search from top-right (r = 0, c = n - 1): if cell == target return true; if cell > target c--; else r++.",
                "steps": [
                    "Start at r = 0, c = n - 1.",
                    "While r < m and c >= 0:",
                    "If matrix[r][c] == target, return true.",
                    "If matrix[r][c] > target, c--.",
                    "Else r++.",
                    "Return false."
                ],
                "time": "O(m+n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public boolean searchMatrix(int[][] matrix, int target) {
        int r = 0, c = matrix[0].length - 1;
        while (r < matrix.length && c >= 0) {
            if (matrix[r][c] == target) return true;
            if (matrix[r][c] > target) c--;
            else r++;
        }
        return false;
    }
}""",
                    "python": """class Solution:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        r, c = 0, len(matrix[0]) - 1
        while r < len(matrix) and c >= 0:
            if matrix[r][c] == target: return True
            elif matrix[r][c] > target: c -= 1
            else: r += 1
        return False"""
                }
            }
        },
        {
            "seq": 63,
            "whyNext": "Binary search on the answer: eating speed k is monotonic, searched in range [1, max(piles)] with hours verification.",
            "brute": {
                "idea": "Try every speed k starting from 1 upward until total eating hours <= h.",
                "steps": [
                    "For speed k = 1, 2, ...:",
                    "Compute hours = sum(ceil(p / k)).",
                    "If hours <= h, return k."
                ],
                "whySlow": "Testing speeds linearly takes O(n * max(piles)) time.",
                "time": "O(n·max)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int minEatingSpeed(int[] piles, int h) {
        int max = 0;
        for (int p : piles) max = Math.max(max, p);
        for (int k = 1; k <= max; k++) {
            long hours = 0;
            for (int p : piles) hours += (p + k - 1) / k;
            if (hours <= h) return k;
        }
        return max;
    }
}""",
                    "python": """class Solution:
    def minEatingSpeed(self, piles: list[int], h: int) -> int:
        for k in range(1, max(piles) + 1):
            if sum((p + k - 1) // k for p in piles) <= h:
                return k
        return max(piles)"""
                }
            },
            "optimal": {
                "idea": "Binary search on speed k in range [1, max(piles)]: if speed k finishes within h hours, search left (r = mid); else l = mid + 1.",
                "steps": [
                    "Initialize l = 1, r = max(piles).",
                    "While l < r:",
                    "mid = l + (r - l) / 2.",
                    "Compute total hours needed at speed mid.",
                    "If hours <= h: r = mid.",
                    "Else: l = mid + 1.",
                    "Return l."
                ],
                "time": "O(n log max)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int minEatingSpeed(int[] piles, int h) {
        int l = 1, r = 0;
        for (int p : piles) r = Math.max(r, p);
        while (l < r) {
            int mid = l + (r - l) / 2;
            long hours = 0;
            for (int p : piles) hours += (p + mid - 1) / mid;
            if (hours <= h) r = mid;
            else l = mid + 1;
        }
        return l;
    }
}""",
                    "python": """class Solution:
    def minEatingSpeed(self, piles: list[int], h: int) -> int:
        l, r = 1, max(piles)
        while l < r:
            mid = (l + r) // 2
            if sum((p + mid - 1) // mid for p in piles) <= h:
                r = mid
            else:
                l = mid + 1
        return l"""
                }
            }
        },
        {
            "seq": 64,
            "whyNext": "Builds on Koko Eating Bananas: binary search on ship capacity in range [max(weights), sum(weights)] with greedy day count check.",
            "brute": {
                "idea": "Try every capacity from max(weights) up to sum(weights), testing if shipping takes <= days.",
                "steps": [
                    "For cap from max(weights) to sum(weights):",
                    "Simulate shipping day by day greedily.",
                    "If required days <= d, return cap."
                ],
                "whySlow": "Testing capacities linearly takes O(n * sum(weights)) time.",
                "time": "O(n·sum)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int shipWithinDays(int[] weights, int days) {
        int maxW = 0, sumW = 0;
        for (int w : weights) { maxW = Math.max(maxW, w); sumW += w; }
        for (int cap = maxW; cap <= sumW; cap++) {
            int d = 1, cur = 0;
            for (int w : weights) {
                if (cur + w > cap) { d++; cur = 0; }
                cur += w;
            }
            if (d <= days) return cap;
        }
        return sumW;
    }
}""",
                    "python": """class Solution:
    def shipWithinDays(self, weights: list[int], days: int) -> int:
        max_w, sum_w = max(weights), sum(weights)
        for cap in range(max_w, sum_w + 1):
            d, cur = 1, 0
            for w in weights:
                if cur + w > cap: d += 1; cur = 0
                cur += w
            if d <= days: return cap
        return sum_w"""
                }
            },
            "optimal": {
                "idea": "Binary search on capacity in range [max(weights), sum(weights)]: check if greedy packaging finishes within days.",
                "steps": [
                    "Initialize l = max(weights), r = sum(weights).",
                    "While l < r:",
                    "mid = l + (r - l) / 2.",
                    "Count required days with capacity mid.",
                    "If daysNeeded <= days, r = mid.",
                    "Else l = mid + 1.",
                    "Return l."
                ],
                "time": "O(n log sum)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int shipWithinDays(int[] weights, int days) {
        int l = 0, r = 0;
        for (int w : weights) { l = Math.max(l, w); r += w; }
        while (l < r) {
            int mid = l + (r - l) / 2;
            int d = 1, cur = 0;
            for (int w : weights) {
                if (cur + w > mid) { d++; cur = 0; }
                cur += w;
            }
            if (d <= days) r = mid;
            else l = mid + 1;
        }
        return l;
    }
}""",
                    "python": """class Solution:
    def shipWithinDays(self, weights: list[int], days: int) -> int:
        l, r = max(weights), sum(weights)
        while l < r:
            mid = (l + r) // 2
            d, cur = 1, 0
            for w in weights:
                if cur + w > mid: d += 1; cur = 0
                cur += w
            if d <= days: r = mid
            else: l = mid + 1
        return l"""
                }
            }
        },
        {
            "seq": 65,
            "whyNext": "Builds on Capacity To Ship Packages: binary search on the day answer in range [1, max(bloomDay)] with adjacent flower grouping check.",
            "brute": {
                "idea": "Try every day from 1 to max(bloomDay) and count if m bouquets of k adjacent flowers can be formed.",
                "steps": [
                    "If m * k > bloomDay.length, return -1.",
                    "Test day = 1, 2, ...:",
                    "Greedily group blooming flowers into bouquets of size k.",
                    "Return first day reaching m bouquets."
                ],
                "whySlow": "Checking all days takes O(n * max(day)) time.",
                "time": "O(n·max)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int minDays(int[] bloomDay, int m, int k) {
        if ((long) m * k > bloomDay.length) return -1;
        int max = 0;
        for (int d : bloomDay) max = Math.max(max, d);
        for (int day = 1; day <= max; day++) {
            int b = 0, flowers = 0;
            for (int d : bloomDay) {
                if (d <= day) { flowers++; if (flowers == k) { b++; flowers = 0; } }
                else flowers = 0;
            }
            if (b >= m) return day;
        }
        return -1;
    }
}""",
                    "python": """class Solution:
    def minDays(self, bloomDay: list[int], m: int, k: int) -> int:
        if m * k > len(bloomDay): return -1
        max_d = max(bloomDay)
        for day in range(1, max_d + 1):
            b, f = 0, 0
            for d in bloomDay:
                if d <= day:
                    f += 1
                    if f == k: b += 1; f = 0
                else: f = 0
            if b >= m: return day
        return -1"""
                }
            },
            "optimal": {
                "idea": "Binary search on days in [1, max(bloomDay)]: greedy pass counts bouquets of size k blooming by day mid.",
                "steps": [
                    "If (long) m * k > bloomDay.length return -1.",
                    "l = 1, r = max(bloomDay).",
                    "While l < r:",
                    "mid = l + (r - l) / 2.",
                    "Count bouquets formed by flowers blooming <= mid.",
                    "If bouquets >= m, r = mid.",
                    "Else l = mid + 1.",
                    "Return l."
                ],
                "time": "O(n log max)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int minDays(int[] bloomDay, int m, int k) {
        if ((long) m * k > bloomDay.length) return -1;
        int l = 1, r = 0;
        for (int d : bloomDay) r = Math.max(r, d);
        while (l < r) {
            int mid = l + (r - l) / 2;
            int bouquets = 0, flowers = 0;
            for (int d : bloomDay) {
                if (d <= mid) { flowers++; if (flowers == k) { bouquets++; flowers = 0; } }
                else flowers = 0;
            }
            if (bouquets >= m) r = mid;
            else l = mid + 1;
        }
        return l;
    }
}""",
                    "python": """class Solution:
    def minDays(self, bloomDay: list[int], m: int, k: int) -> int:
        if m * k > len(bloomDay): return -1
        l, r = 1, max(bloomDay)
        while l < r:
            mid = (l + r) // 2
            b, f = 0, 0
            for d in bloomDay:
                if d <= mid:
                    f += 1
                    if f == k: b += 1; f = 0
                else: f = 0
            if b >= m: r = mid
            else: l = mid + 1
        return l"""
                }
            }
        },
        {
            "seq": 66,
            "whyNext": "Equivalent to Capacity to Ship Packages: split array into k subarrays minimizing the maximum sum via binary search.",
            "brute": {
                "idea": "Try all possible partition points using recursive backtracking to find the minimum largest subarray sum.",
                "steps": [
                    "Recursively partition array into k parts.",
                    "Calculate largest sum among parts.",
                    "Take minimum over all partition combinations."
                ],
                "whySlow": "Evaluating all combinations yields exponential complexity.",
                "time": "exponential",
                "space": "O(k)",
                "code": {
                    "java": """class Solution {
    public int splitArray(int[] nums, int k) {
        // Brute force binary search on answer
        long l = 0, r = 0;
        for (int x : nums) { l = Math.max(l, x); r += x; }
        while (l < r) {
            long mid = l + (r - l) / 2;
            int pieces = 1; long cur = 0;
            for (int x : nums) {
                if (cur + x > mid) { pieces++; cur = 0; }
                cur += x;
            }
            if (pieces <= k) r = mid;
            else l = mid + 1;
        }
        return (int) l;
    }
}""",
                    "python": """class Solution:
    def splitArray(self, nums: list[int], k: int) -> int:
        l, r = max(nums), sum(nums)
        while l < r:
            mid = (l + r) // 2
            pieces, cur = 1, 0
            for x in nums:
                if cur + x > mid: pieces += 1; cur = 0
                cur += x
            if pieces <= k: r = mid
            else: l = mid + 1
        return l"""
                }
            },
            "optimal": {
                "idea": "Binary search on largest subarray sum in [max(nums), sum(nums)]: greedily pack elements into subarray while sum <= mid.",
                "steps": [
                    "Initialize l = max(nums), r = sum(nums).",
                    "While l < r:",
                    "mid = l + (r - l) / 2.",
                    "Count pieces needed: when cur + x > mid, pieces++, cur = x; else cur += x.",
                    "If pieces <= k, r = mid.",
                    "Else l = mid + 1.",
                    "Return l."
                ],
                "time": "O(n log sum)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int splitArray(int[] nums, int k) {
        long l = 0, r = 0;
        for (int x : nums) { l = Math.max(l, x); r += x; }
        while (l < r) {
            long mid = l + (r - l) / 2;
            int pieces = 1; long cur = 0;
            for (int x : nums) {
                if (cur + x > mid) { pieces++; cur = 0; }
                cur += x;
            }
            if (pieces <= k) r = mid;
            else l = mid + 1;
        }
        return (int) l;
    }
}""",
                    "python": """class Solution:
    def splitArray(self, nums: list[int], k: int) -> int:
        l, r = max(nums), sum(nums)
        while l < r:
            mid = (l + r) // 2
            pieces, cur = 1, 0
            for x in nums:
                if cur + x > mid: pieces += 1; cur = 0
                cur += x
            if pieces <= k: r = mid
            else: l = mid + 1
        return l"""
                }
            }
        },
        {
            "seq": 67,
            "whyNext": "Completes Chapter 4: binary search for the correct partition boundary on the shorter array to achieve logarithmic median finding.",
            "brute": {
                "idea": "Merge both sorted arrays into one sorted array of length m + n and pick the middle element.",
                "steps": [
                    "Merge nums1 and nums2 using two pointers.",
                    "If total length is odd, return middle element.",
                    "If total length is even, return average of two middle elements."
                ],
                "whySlow": "Allocates and fills an array of size m + n in linear time.",
                "time": "O(m+n)",
                "space": "O(m+n)",
                "code": {
                    "java": """class Solution {
    public double findMedianSortedArrays(int[] nums1, int[] nums2) {
        int m = nums1.length, n = nums2.length;
        int[] merged = new int[m + n];
        int i = 0, j = 0, k = 0;
        while (i < m && j < n) merged[k++] = (nums1[i] < nums2[j]) ? nums1[i++] : nums2[j++];
        while (i < m) merged[k++] = nums1[i++];
        while (j < n) merged[k++] = nums2[j++];
        int total = m + n;
        if (total % 2 == 1) return merged[total / 2];
        return (merged[total / 2 - 1] + merged[total / 2]) / 2.0;
    }
}""",
                    "python": """class Solution:
    def findMedianSortedArrays(self, nums1: list[int], nums2: list[int]) -> float:
        merged = sorted(nums1 + nums2)
        total = len(merged)
        if total % 2 == 1: return float(merged[total // 2])
        return (merged[total // 2 - 1] + merged[total // 2]) / 2.0"""
                }
            },
            "optimal": {
                "idea": "Binary search on the partition of the shorter array: partition both arrays such that left halves have (m + n + 1) / 2 elements and all left elements <= right elements.",
                "steps": [
                    "Ensure nums1 is shorter array.",
                    "Binary search partition i in [0, m]; j = (m + n + 1) / 2 - i.",
                    "Check maxLeft1 <= minRight2 and maxLeft2 <= minRight1.",
                    "If valid: median is max(lefts) (if odd) or avg(max(lefts), min(rights)) (if even).",
                    "Adjust binary search."
                ],
                "time": "O(log min(m,n))",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public double findMedianSortedArrays(int[] nums1, int[] nums2) {
        if (nums1.length > nums2.length) return findMedianSortedArrays(nums2, nums1);
        int m = nums1.length, n = nums2.length;
        int l = 0, r = m;
        while (l <= r) {
            int i = l + (r - l) / 2;
            int j = (m + n + 1) / 2 - i;
            int maxLeft1 = (i == 0) ? Integer.MIN_VALUE : nums1[i - 1];
            int minRight1 = (i == m) ? Integer.MAX_VALUE : nums1[i];
            int maxLeft2 = (j == 0) ? Integer.MIN_VALUE : nums2[j - 1];
            int minRight2 = (j == n) ? Integer.MAX_VALUE : nums2[j];
            if (maxLeft1 <= minRight2 && maxLeft2 <= minRight1) {
                if ((m + n) % 2 == 1) return Math.max(maxLeft1, maxLeft2);
                return (Math.max(maxLeft1, maxLeft2) + Math.min(minRight1, minRight2)) / 2.0;
            } else if (maxLeft1 > minRight2) r = i - 1;
            else l = i + 1;
        }
        return 0.0;
    }
}""",
                    "python": """class Solution:
    def findMedianSortedArrays(self, nums1: list[int], nums2: list[int]) -> float:
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1
        m, n = len(nums1), len(nums2)
        l, r = 0, m
        while l <= r:
            i = (l + r) // 2
            j = (m + n + 1) // 2 - i
            max_l1 = float('-inf') if i == 0 else nums1[i - 1]
            min_r1 = float('inf') if i == m else nums1[i]
            max_l2 = float('-inf') if j == 0 else nums2[j - 1]
            min_r2 = float('inf') if j == n else nums2[j]
            if max_l1 <= min_r2 and max_l2 <= min_r1:
                if (m + n) % 2 == 1:
                    return float(max(max_l1, max_l2))
                return (max(max_l1, max_l2) + min(min_r1, min_r2)) / 2.0
            elif max_l1 > min_r2: r = i - 1
            else: l = i + 1
        return 0.0"""
                }
            }
        },
        {
            "seq": 68,
            "whyNext": "Opens Chapter 5 (Stack and Monotonic Stack): LIFO structure matches open brackets with their corresponding closing brackets.",
            "brute": {
                "idea": "Repeatedly find and replace matched pairs '()', '[]', '{}' with empty string until string is empty or unchanged.",
                "steps": [
                    "While s contains '()', '[]', or '{}', replace them with empty string.",
                    "Return true if string becomes empty, else false."
                ],
                "whySlow": "String allocations and substring replacements take O(n²) time.",
                "time": "O(n²)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public boolean isValid(String s) {
        int prev = -1;
        while (s.length() != prev) {
            prev = s.length();
            s = s.replace("()", "").replace("[]", "").replace("{}", "");
        }
        return s.isEmpty();
    }
}""",
                    "python": """class Solution:
    def isValid(self, s: str) -> bool:
        while "()" in s or "[]" in s or "{}" in s:
            s = s.replace("()", "").replace("[]", "").replace("{}", "")
        return s == ''"""
                }
            },
            "optimal": {
                "idea": "Use a stack: push expected closing bracket when opening bracket seen; pop and verify match when closing bracket seen.",
                "steps": [
                    "Initialize a char stack.",
                    "For char c in s:",
                    "If c is '(', push ')'. If '[', push ']'. If '{', push '}'.",
                    "Else if stack is empty or stack.pop() != c, return false.",
                    "Return stack.isEmpty()."
                ],
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public boolean isValid(String s) {
        Deque<Character> stack = new ArrayDeque<>();
        for (char c : s.toCharArray()) {
            if (c == '(') stack.push(')');
            else if (c == '[') stack.push(']');
            else if (c == '{') stack.push('}');
            else if (stack.isEmpty() || stack.pop() != c) return false;
        }
        return stack.isEmpty();
    }
}""",
                    "python": """class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        mapping = {')': '(', ']': '[', '}': '{'}
        for c in s:
            if c in mapping:
                if not stack or stack.pop() != mapping[c]:
                    return False
            else:
                stack.append(c)
        return not stack"""
                }
            }
        },
        {
            "seq": 69,
            "whyNext": "Builds on stack design: pair each pushed value with the current minimum to answer getMin() in O(1) time.",
            "brute": {
                "idea": "Store elements in a standard list or stack and scan all elements linearly during getMin().",
                "steps": [
                    "push, pop, top operate on standard list.",
                    "getMin() iterates through all elements to find the minimum."
                ],
                "whySlow": "getMin takes linear O(n) time on every call.",
                "time": "O(n) getMin",
                "space": "O(n)",
                "code": {
                    "java": """class MinStack {
    private List<Integer> list = new ArrayList<>();
    public MinStack() {}
    public void push(int val) { list.add(val); }
    public void pop() { list.remove(list.size() - 1); }
    public int top() { return list.get(list.size() - 1); }
    public int getMin() {
        int min = list.get(0);
        for (int x : list) min = Math.min(min, x);
        return min;
    }
}""",
                    "python": """class MinStack:
    def __init__(self):
        self.stack = []
    def push(self, val: int) -> None:
        self.stack.append(val)
    def pop(self) -> None:
        self.stack.pop()
    def top(self) -> int:
        return self.stack[-1]
    def getMin(self) -> int:
        return min(self.stack)"""
                }
            },
            "optimal": {
                "idea": "Two stacks or paired values: maintain a minStack that records the running minimum at every stack depth.",
                "steps": [
                    "Maintain primary stack and minStack.",
                    "push(val): stack.push(val); minStack.push(min(val, minStack.peek())).",
                    "pop(): pop from both stacks.",
                    "top(): stack.peek().",
                    "getMin(): minStack.peek()."
                ],
                "time": "O(1)",
                "space": "O(n)",
                "code": {
                    "java": """class MinStack {
    private Deque<Integer> stack = new ArrayDeque<>();
    private Deque<Integer> minStack = new ArrayDeque<>();
    public MinStack() {}
    public void push(int val) {
        stack.push(val);
        int curMin = minStack.isEmpty() ? val : Math.min(val, minStack.peek());
        minStack.push(curMin);
    }
    public void pop() {
        stack.pop();
        minStack.pop();
    }
    public int top() { return stack.peek(); }
    public int getMin() { return minStack.peek(); }
}""",
                    "python": """class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []
    def push(self, val: int) -> None:
        self.stack.append(val)
        m = val if not self.min_stack else min(val, self.min_stack[-1])
        self.min_stack.append(m)
    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()
    def top(self) -> int:
        return self.stack[-1]
    def getMin(self) -> int:
        return self.min_stack[-1]"""
                }
            }
        },
        {
            "seq": 70,
            "whyNext": "Builds on stack evaluation: push numbers onto stack; upon operator, pop two operands, evaluate, and push result back.",
            "brute": {
                "idea": "Iteratively scan list to find the first operator, replace the operator and previous two numbers with their evaluated result.",
                "steps": [
                    "While tokens length > 1:",
                    "Find first operator at index i.",
                    "Evaluate tokens[i-2] op tokens[i-1].",
                    "Replace 3 tokens with result."
                ],
                "whySlow": "Repeated array shifts and rescanning takes quadratic O(n²) time.",
                "time": "O(n²)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public int evalRPN(String[] tokens) {
        List<String> list = new ArrayList<>(Arrays.asList(tokens));
        while (list.size() > 1) {
            int i = 0;
            while (i < list.size() && !"+-*/".contains(list.get(i))) i++;
            int a = Integer.parseInt(list.get(i - 2));
            int b = Integer.parseInt(list.get(i - 1));
            String op = list.get(i);
            int res = 0;
            if (op.equals("+")) res = a + b;
            else if (op.equals("-")) res = a - b;
            else if (op.equals("*")) res = a * b;
            else res = a / b;
            list.set(i - 2, String.valueOf(res));
            list.remove(i);
            list.remove(i - 1);
        }
        return Integer.parseInt(list.get(0));
    }
}""",
                    "python": """class Solution:
    def evalRPN(self, tokens: list[str]) -> int:
        t = list(tokens)
        while len(t) > 1:
            i = 0
            while i < len(t) and t[i] not in "+-*/": i += 1
            a, b, op = int(t[i-2]), int(t[i-1]), t[i]
            if op == '+': res = a + b
            elif op == '-': res = a - b
            elif op == '*': res = a * b
            else: res = int(a / b)
            t = t[:i-2] + [str(res)] + t[i+1:]
        return int(t[0])"""
                }
            },
            "optimal": {
                "idea": "Operand stack: push numbers; when encountering an operator, pop b then a, evaluate a op b, and push result back.",
                "steps": [
                    "Initialize integer stack.",
                    "For each token t:",
                    "If operator: b = pop(), a = pop(), push result of a op b.",
                    "Else: push Integer.parseInt(t).",
                    "Return stack.pop()."
                ],
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public int evalRPN(String[] tokens) {
        Deque<Integer> stack = new ArrayDeque<>();
        for (String t : tokens) {
            if (t.equals("+")) stack.push(stack.pop() + stack.pop());
            else if (t.equals("*")) stack.push(stack.pop() * stack.pop());
            else if (t.equals("-")) { int b = stack.pop(), a = stack.pop(); stack.push(a - b); }
            else if (t.equals("/")) { int b = stack.pop(), a = stack.pop(); stack.push(a / b); }
            else stack.push(Integer.parseInt(t));
        }
        return stack.pop();
    }
}""",
                    "python": """class Solution:
    def evalRPN(self, tokens: list[str]) -> int:
        stack = []
        for t in tokens:
            if t == '+': stack.append(stack.pop() + stack.pop())
            elif t == '*': stack.append(stack.pop() * stack.pop())
            elif t == '-': b, a = stack.pop(), stack.pop(); stack.append(a - b)
            elif t == '/': b, a = stack.pop(), stack.pop(); stack.append(int(a / b))
            else: stack.append(int(t))
        return stack[0]"""
                }
            }
        },
        {
            "seq": 71,
            "whyNext": "Builds on Evaluate RPN: operator precedence in infix expressions handled by applying * and / immediately to stack top, deferring + and -.",
            "brute": {
                "idea": "Two passes: first pass evaluates all multiplication and division, second pass evaluates addition and subtraction.",
                "steps": [
                    "Tokenize string into numbers and operators.",
                    "First pass: process * and / into intermediate list.",
                    "Second pass: process + and -."
                ],
                "whySlow": "Multi-pass intermediate list creation uses extra passes and allocations.",
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public int calculate(String s) {
        Deque<Integer> stack = new ArrayDeque<>();
        int num = 0;
        char sign = '+';
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (Character.isDigit(c)) num = num * 10 + (c - '0');
            if ((!Character.isDigit(c) && c != ' ') || i == s.length() - 1) {
                if (sign == '+') stack.push(num);
                else if (sign == '-') stack.push(-num);
                else if (sign == '*') stack.push(stack.pop() * num);
                else if (sign == '/') stack.push(stack.pop() / num);
                sign = c;
                num = 0;
            }
        }
        int res = 0;
        for (int x : stack) res += x;
        return res;
    }
}""",
                    "python": """class Solution:
    def calculate(self, s: str) -> int:
        stack = []
        num, sign = 0, '+'
        for i, c in enumerate(s):
            if c.isdigit(): num = num * 10 + int(c)
            if (not c.isdigit() and c != ' ') or i == len(s) - 1:
                if sign == '+': stack.append(num)
                elif sign == '-': stack.append(-num)
                elif sign == '*': stack.append(stack.pop() * num)
                elif sign == '/': stack.append(int(stack.pop() / num))
                sign = c
                num = 0
        return sum(stack)"""
                }
            },
            "optimal": {
                "idea": "Single pass using stack: maintain current number and previous operator. Immediate multiplication/division on stack top; sum stack at end.",
                "steps": [
                    "Maintain current number and last operator (default '+').",
                    "When reaching an operator or end of string:",
                    "If last was '+', push num; if '-', push -num; if '*', push pop() * num; if '/', push pop() / num.",
                    "Update operator and reset num.",
                    "Sum all numbers remaining in stack."
                ],
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public int calculate(String s) {
        Deque<Integer> stack = new ArrayDeque<>();
        int num = 0;
        char sign = '+';
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (Character.isDigit(c)) num = num * 10 + (c - '0');
            if ((!Character.isDigit(c) && c != ' ') || i == s.length() - 1) {
                if (sign == '+') stack.push(num);
                else if (sign == '-') stack.push(-num);
                else if (sign == '*') stack.push(stack.pop() * num);
                else if (sign == '/') stack.push(stack.pop() / num);
                sign = c;
                num = 0;
            }
        }
        int sum = 0;
        while (!stack.isEmpty()) sum += stack.pop();
        return sum;
    }
}""",
                    "python": """class Solution:
    def calculate(self, s: str) -> int:
        stack = []
        num = 0
        sign = '+'
        for i, c in enumerate(s):
            if c.isdigit():
                num = num * 10 + int(c)
            if (not c.isdigit() and c != ' ') or i == len(s) - 1:
                if sign == '+': stack.append(num)
                elif sign == '-': stack.append(-num)
                elif sign == '*': stack.append(stack.pop() * num)
                elif sign == '/': stack.append(int(stack.pop() / num))
                sign = c
                num = 0
        return sum(stack)"""
                }
            }
        },
        {
            "seq": 72,
            "whyNext": "Introduces monotonic stack: decreasing stack pops smaller elements when a larger element appears, recording their next greater value.",
            "brute": {
                "idea": "For each element in nums1, locate it in nums2 and scan right for the first greater element.",
                "steps": [
                    "For each x in nums1:",
                    "Find index of x in nums2.",
                    "Scan right in nums2 for first element > x.",
                    "If found record it, else record -1."
                ],
                "whySlow": "Scanning nums2 for every query takes O(n * m) time.",
                "time": "O(nm)",
                "space": "O(m)",
                "code": {
                    "java": """class Solution {
    public int[] nextGreaterElement(int[] nums1, int[] nums2) {
        int[] res = new int[nums1.length];
        for (int i = 0; i < nums1.length; i++) {
            int idx = -1;
            for (int j = 0; j < nums2.length; j++) {
                if (nums2[j] == nums1[i]) { idx = j; break; }
            }
            int next = -1;
            for (int j = idx + 1; j < nums2.length; j++) {
                if (nums2[j] > nums1[i]) { next = nums2[j]; break; }
            }
            res[i] = next;
        }
        return res;
    }
}""",
                    "python": """class Solution:
    def nextGreaterElement(self, nums1: list[int], nums2: list[int]) -> list[int]:
        res = []
        for x in nums1:
            idx = nums2.index(x)
            next_g = -1
            for j in range(idx + 1, len(nums2)):
                if nums2[j] > x:
                    next_g = nums2[j]
                    break
            res.append(next_g)
        return res"""
                }
            },
            "optimal": {
                "idea": "Monotonic decreasing stack on nums2: while stack top < current number, map[stack.pop()] = current number. Query map for nums1.",
                "steps": [
                    "Initialize stack and HashMap.",
                    "For each x in nums2:",
                    "While stack not empty and stack.peek() < x: map.put(stack.pop(), x).",
                    "stack.push(x).",
                    "For each x in nums1: res[i] = map.getOrDefault(x, -1)."
                ],
                "time": "O(n+m)",
                "space": "O(m)",
                "code": {
                    "java": """class Solution {
    public int[] nextGreaterElement(int[] nums1, int[] nums2) {
        Map<Integer, Integer> map = new HashMap<>();
        Deque<Integer> stack = new ArrayDeque<>();
        for (int x : nums2) {
            while (!stack.isEmpty() && stack.peek() < x) map.put(stack.pop(), x);
            stack.push(x);
        }
        int[] res = new int[nums1.length];
        for (int i = 0; i < nums1.length; i++) res[i] = map.getOrDefault(nums1[i], -1);
        return res;
    }
}""",
                    "python": """class Solution:
    def nextGreaterElement(self, nums1: list[int], nums2: list[int]) -> list[int]:
        stack = []
        next_map = {}
        for x in nums2:
            while stack and stack[-1] < x:
                next_map[stack.pop()] = x
            stack.append(x)
        return [next_map.get(x, -1) for x in nums1]"""
                }
            }
        },
        {
            "seq": 73,
            "whyNext": "Builds on Next Greater Element: circular array simulated by running monotonic stack over 2n indices with index modulo n.",
            "brute": {
                "idea": "For each element i, circular scan up to n - 1 elements ahead (using (i + j) % n) to find the first greater value.",
                "steps": [
                    "Loop i from 0 to n - 1.",
                    "Loop j from 1 to n - 1: if nums[(i + j) % n] > nums[i], record and break."
                ],
                "whySlow": "Scanning circularly for every element takes O(n²) time.",
                "time": "O(n²)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int[] nextGreaterElements(int[] nums) {
        int n = nums.length;
        int[] res = new int[n];
        Arrays.fill(res, -1);
        for (int i = 0; i < n; i++) {
            for (int j = 1; j < n; j++) {
                int next = nums[(i + j) % n];
                if (next > nums[i]) { res[i] = next; break; }
            }
        }
        return res;
    }
}""",
                    "python": """class Solution:
    def nextGreaterElements(self, nums: list[int]) -> list[int]:
        n = len(nums)
        res = [-1] * n
        for i in range(n):
            for j in range(1, n):
                if nums[(i + j) % n] > nums[i]:
                    res[i] = nums[(i + j) % n]
                    break
        return res"""
                }
            },
            "optimal": {
                "idea": "Monotonic decreasing stack of indices over a virtual 2n array: process i from 2n - 1 down to 0, pop <= nums[i % n], assign stack top.",
                "steps": [
                    "Initialize result array with -1 and stack of indices.",
                    "Loop i from 2n - 1 down to 0:",
                    "While stack not empty and nums[stack.peek()] <= nums[i % n]: stack.pop().",
                    "If !stack.isEmpty(): res[i % n] = nums[stack.peek()].",
                    "stack.push(i % n)."
                ],
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public int[] nextGreaterElements(int[] nums) {
        int n = nums.length;
        int[] res = new int[n];
        Arrays.fill(res, -1);
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 2 * n - 1; i >= 0; i--) {
            while (!stack.isEmpty() && nums[stack.peek()] <= nums[i % n]) stack.pop();
            if (!stack.isEmpty()) res[i % n] = nums[stack.peek()];
            stack.push(i % n);
        }
        return res;
    }
}""",
                    "python": """class Solution:
    def nextGreaterElements(self, nums: list[int]) -> list[int]:
        n = len(nums)
        res = [-1] * n
        stack = []
        for i in range(2 * n - 1, -1, -1):
            while stack and nums[stack[-1]] <= nums[i % n]:
                stack.pop()
            if stack:
                res[i % n] = nums[stack[-1]]
            stack.append(i % n)
        return res"""
                }
            }
        },
        {
            "seq": 74,
            "whyNext": "Builds on Next Greater Element: monotonic decreasing stack stores indices; when a warmer day arrives, span is (current_index - popped_index).",
            "brute": {
                "idea": "For each day i, scan forward until encountering a day with temperature > temperatures[i].",
                "steps": [
                    "Loop i from 0 to n - 1.",
                    "Loop j from i + 1 to n - 1.",
                    "If temperatures[j] > temperatures[i], res[i] = j - i, break."
                ],
                "whySlow": "Scanning forward for every day takes O(n²) time.",
                "time": "O(n²)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int[] dailyTemperatures(int[] temperatures) {
        int n = temperatures.length;
        int[] res = new int[n];
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (temperatures[j] > temperatures[i]) { res[i] = j - i; break; }
            }
        }
        return res;
    }
}""",
                    "python": """class Solution:
    def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
        n = len(temperatures)
        res = [0] * n
        for i in range(n):
            for j in range(i + 1, n):
                if temperatures[j] > temperatures[i]:
                    res[i] = j - i
                    break
        return res"""
                }
            },
            "optimal": {
                "idea": "Monotonic decreasing stack of day indices: while current temperature > temperatures[stack.peek()], pop prevDay and set res[prevDay] = currentDay - prevDay.",
                "steps": [
                    "Initialize res array and integer stack of day indices.",
                    "For each day i from 0 to n - 1:",
                    "While stack not empty and temperatures[i] > temperatures[stack.peek()]:",
                    "prev = stack.pop(); res[prev] = i - prev.",
                    "stack.push(i)."
                ],
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public int[] dailyTemperatures(int[] temperatures) {
        int n = temperatures.length;
        int[] res = new int[n];
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && temperatures[i] > temperatures[stack.peek()]) {
                int prev = stack.pop();
                res[prev] = i - prev;
            }
            stack.push(i);
        }
        return res;
    }
}""",
                    "python": """class Solution:
    def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
        res = [0] * len(temperatures)
        stack = []
        for i, t in enumerate(temperatures):
            while stack and t > temperatures[stack[-1]]:
                prev = stack.pop()
                res[prev] = i - prev
            stack.append(i)
        return res"""
                }
            }
        },
        {
            "seq": 75,
            "whyNext": "Builds on Daily Temperatures span calculation: maintain stack of (price, span) pairs, collapsing consecutive smaller prices.",
            "brute": {
                "idea": "Store all daily prices in a list; on each next(price) call, walk backwards to count consecutive prices <= price.",
                "steps": [
                    "Add price to history list.",
                    "Scan backwards from end, counting days while price >= history[i].",
                    "Return count."
                ],
                "whySlow": "Scanning backwards on each day takes O(n) per call, totaling O(n²).",
                "time": "O(n²)",
                "space": "O(n)",
                "code": {
                    "java": """class StockSpanner {
    private List<Integer> prices = new ArrayList<>();
    public StockSpanner() {}
    public int next(int price) {
        prices.add(price);
        int span = 0;
        for (int i = prices.size() - 1; i >= 0; i--) {
            if (prices.get(i) <= price) span++;
            else break;
        }
        return span;
    }
}""",
                    "python": """class StockSpanner:
    def __init__(self):
        self.prices = []
    def next(self, price: int) -> int:
        self.prices.append(price)
        span = 0
        for p in reversed(self.prices):
            if p <= price: span += 1
            else: break
        return span"""
                }
            },
            "optimal": {
                "idea": "Monotonic decreasing stack of (price, span) pairs: while top price <= current price, add its span to current span and pop it.",
                "steps": [
                    "Initialize stack storing (price, span).",
                    "On next(price): initialize span = 1.",
                    "While stack not empty and stack.peek().price <= price: span += stack.pop().span.",
                    "stack.push((price, span)).",
                    "Return span."
                ],
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class StockSpanner {
    private Deque<int[]> stack = new ArrayDeque<>();
    public StockSpanner() {}
    public int next(int price) {
        int span = 1;
        while (!stack.isEmpty() && stack.peek()[0] <= price) {
            span += stack.pop()[1];
        }
        stack.push(new int[]{price, span});
        return span;
    }
}""",
                    "python": """class StockSpanner:
    def __init__(self):
        self.stack = []
    def next(self, price: int) -> int:
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            span += self.stack.pop()[1]
        self.stack.append((price, span))
        return span"""
                }
            }
        }
    ]

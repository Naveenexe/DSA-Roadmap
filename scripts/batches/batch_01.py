# Batch 1: Seq 1 to 25
# Covers Chapter 1 (1 to 21) and part of Chapter 2 (22 to 25)

def get_batch():
    return [
        {
            "seq": 1,
            "whyNext": "Foundation of the roadmap: introducing hash set lookups to eliminate quadratic nested loops.",
            "brute": {
                "idea": "Compare every element with every subsequent element using two nested loops.",
                "steps": [
                    "Loop i from 0 to n - 1.",
                    "Loop j from i + 1 to n - 1.",
                    "If nums[i] == nums[j], return true.",
                    "Return false if no duplicates are found."
                ],
                "whySlow": "Checking all n(n-1)/2 pairs requires O(n²) time.",
                "time": "O(n²)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public boolean containsDuplicate(int[] nums) {
        for (int i = 0; i < nums.length; i++) {
            for (int j = i + 1; j < nums.length; j++) {
                if (nums[i] == nums[j]) return true;
            }
        }
        return false;
    }
}""",
                    "python": """class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] == nums[j]:
                    return True
        return False"""
                }
            },
            "optimal": {
                "idea": "Add elements one by one into a HashSet; if an element already exists, return true immediately.",
                "steps": [
                    "Initialize an empty HashSet.",
                    "Iterate through each number in nums.",
                    "If the set already contains the number, return true.",
                    "Otherwise add the number to the set.",
                    "Return false if loop terminates."
                ],
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public boolean containsDuplicate(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        for (int x : nums) {
            if (!seen.add(x)) return true;
        }
        return false;
    }
}""",
                    "python": """class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        seen = set()
        for x in nums:
            if x in seen:
                return True
            seen.add(x)
        return False"""
                }
            }
        },
        {
            "seq": 2,
            "whyNext": "Builds on Contains Duplicate: instead of checking membership, use a map to store and retrieve complement indices.",
            "brute": {
                "idea": "Check every pair in nums to find two elements that sum to target.",
                "steps": [
                    "Loop i from 0 to n - 1.",
                    "Loop j from i + 1 to n - 1.",
                    "If nums[i] + nums[j] == target, return [i, j].",
                    "Return empty array if no pair matches."
                ],
                "whySlow": "Evaluating every pair takes quadratic O(n²) time.",
                "time": "O(n²)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int[] twoSum(int[] nums, int target) {
        for (int i = 0; i < nums.length; i++) {
            for (int j = i + 1; j < nums.length; j++) {
                if (nums[i] + nums[j] == target) return new int[]{i, j};
            }
        }
        return new int[]{};
    }
}""",
                    "python": """class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []"""
                }
            },
            "optimal": {
                "idea": "Use a HashMap to store each visited number and its index, checking for target - nums[i] on each step.",
                "steps": [
                    "Create a HashMap of value to index.",
                    "Iterate through nums with index i and value x.",
                    "Compute need = target - x.",
                    "If need is in map, return [map.get(need), i].",
                    "Otherwise put (x, i) in map."
                ],
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (map.containsKey(complement)) return new int[]{map.get(complement), i};
            map.put(nums[i], i);
        }
        return new int[]{};
    }
}""",
                    "python": """class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen = {}
        for i, x in enumerate(nums):
            need = target - x
            if need in seen:
                return [seen[need], i]
            seen[x] = i
        return []"""
                }
            }
        },
        {
            "seq": 3,
            "whyNext": "Builds on hash counting from Two Sum: comparing frequencies of characters across two strings.",
            "brute": {
                "idea": "Sort both strings alphabetically and compare if they are equal.",
                "steps": [
                    "Check if lengths match; return false if not.",
                    "Sort characters of string s.",
                    "Sort characters of string t.",
                    "Return whether the sorted strings are equal."
                ],
                "whySlow": "Sorting strings of length n requires O(n log n) comparisons.",
                "time": "O(n log n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public boolean isAnagram(String s, String t) {
        if (s.length() != t.length()) return false;
        char[] sArr = s.toCharArray();
        char[] tArr = t.toCharArray();
        Arrays.sort(sArr);
        Arrays.sort(tArr);
        return Arrays.equals(sArr, tArr);
    }
}""",
                    "python": """class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        return sorted(s) == sorted(t)"""
                }
            },
            "optimal": {
                "idea": "Count frequencies of all 26 lowercase English characters in a fixed-size array.",
                "steps": [
                    "If s.length != t.length, return false.",
                    "Allocate count array of size 26.",
                    "Increment counts for chars in s and decrement for chars in t.",
                    "Verify all counts are 0."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public boolean isAnagram(String s, String t) {
        if (s.length() != t.length()) return false;
        int[] counts = new int[26];
        for (int i = 0; i < s.length(); i++) {
            counts[s.charAt(i) - 'a']++;
            counts[t.charAt(i) - 'a']--;
        }
        for (int c : counts) if (c != 0) return false;
        return true;
    }
}""",
                    "python": """class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t): return False
        counts = [0] * 26
        for c1, c2 in zip(s, t):
            counts[ord(c1) - ord('a')] += 1
            counts[ord(c2) - ord('a')] -= 1
        return all(c == 0 for c in counts)"""
                }
            }
        },
        {
            "seq": 4,
            "whyNext": "Extends Valid Anagram to a collection of strings: group words having identical sorted character keys.",
            "brute": {
                "idea": "Compare each string against existing groups using the anagram equality check.",
                "steps": [
                    "Maintain a list of anagram groups.",
                    "For each word, compare with the first element of each group.",
                    "Add to group if match found; otherwise create a new group."
                ],
                "whySlow": "Pairwise comparisons between strings can take O(n²k) time.",
                "time": "O(n²k)",
                "space": "O(nk)",
                "code": {
                    "java": """class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        List<List<String>> res = new ArrayList<>();
        for (String s : strs) {
            boolean added = false;
            for (List<String> g : res) {
                if (isAna(g.get(0), s)) { g.add(s); added = true; break; }
            }
            if (!added) {
                List<String> ng = new ArrayList<>();
                ng.add(s);
                res.add(ng);
            }
        }
        return res;
    }
    private boolean isAna(String a, String b) {
        if (a.length() != b.length()) return false;
        char[] ca = a.toCharArray(), cb = b.toCharArray();
        Arrays.sort(ca); Arrays.sort(cb);
        return Arrays.equals(ca, cb);
    }
}""",
                    "python": """class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        groups = []
        for s in strs:
            matched = False
            for g in groups:
                if sorted(g[0]) == sorted(s):
                    g.append(s)
                    matched = True
                    break
            if not matched:
                groups.append([s])
        return groups"""
                }
            },
            "optimal": {
                "idea": "Sort each string's characters to form a canonical key in a HashMap mapping to its list of anagrams.",
                "steps": [
                    "Create a Map<String, List<String>>.",
                    "For each word, sort its letters to form the key.",
                    "Append the word to the map under key.",
                    "Return all map values as a list of lists."
                ],
                "time": "O(nk log k)",
                "space": "O(nk)",
                "code": {
                    "java": """class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> map = new HashMap<>();
        for (String s : strs) {
            char[] ca = s.toCharArray();
            Arrays.sort(ca);
            String key = String.valueOf(ca);
            map.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
        }
        return new ArrayList<>(map.values());
    }
}""",
                    "python": """class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        map_ = collections.defaultdict(list)
        for s in strs:
            map_["".join(sorted(s))].append(s)
        return list(map_.values())"""
                }
            }
        },
        {
            "seq": 5,
            "whyNext": "Builds on frequency counting from Group Anagrams: bucket sort by frequency for linear top-k selection.",
            "brute": {
                "idea": "Count frequencies using a map and sort unique elements by frequency descending.",
                "steps": [
                    "Count element occurrences in a HashMap.",
                    "Extract keys into a list.",
                    "Sort keys by descending frequency.",
                    "Return the first k keys."
                ],
                "whySlow": "Sorting unique elements takes O(n log n) time.",
                "time": "O(n log n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int n : nums) map.put(n, map.getOrDefault(n, 0) + 1);
        List<Integer> list = new ArrayList<>(map.keySet());
        list.sort((a, b) -> map.get(b) - map.get(a));
        int[] res = new int[k];
        for (int i = 0; i < k; i++) res[i] = list.get(i);
        return res;
    }
}""",
                    "python": """class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        c = collections.Counter(nums)
        return [item[0] for item in c.most_common(k)]"""
                }
            },
            "optimal": {
                "idea": "Count frequencies, place numbers into an array of buckets indexed by frequency, and collect the top k.",
                "steps": [
                    "Count frequencies with a HashMap.",
                    "Create an array of lists of size n + 1 for buckets.",
                    "Add each number to buckets[frequency].",
                    "Traverse buckets from n down to 0, appending to result until k elements are collected."
                ],
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int n : nums) map.put(n, map.getOrDefault(n, 0) + 1);
        List<Integer>[] buckets = new List[nums.length + 1];
        for (int key : map.keySet()) {
            int f = map.get(key);
            if (buckets[f] == null) buckets[f] = new ArrayList<>();
            buckets[f].add(key);
        }
        int[] res = new int[k];
        int idx = 0;
        for (int i = buckets.length - 1; i >= 0 && idx < k; i--) {
            if (buckets[i] != null) {
                for (int val : buckets[i]) {
                    res[idx++] = val;
                    if (idx == k) break;
                }
            }
        }
        return res;
    }
}""",
                    "python": """class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        counts = collections.Counter(nums)
        buckets = [[] for _ in range(len(nums) + 1)]
        for num, freq in counts.items():
            buckets[freq].append(num)
        res = []
        for i in range(len(buckets) - 1, 0, -1):
            for num in buckets[i]:
                res.append(num)
                if len(res) == k:
                    return res
        return res"""
                }
            }
        },
        {
            "seq": 6,
            "whyNext": "Builds on frequency counting: Boyer-Moore voting finds the element occurring > n/2 times in O(1) space.",
            "brute": {
                "idea": "Count frequencies with a HashMap or sort the array and take the middle element.",
                "steps": [
                    "Store frequencies of all elements in a HashMap.",
                    "Find the key whose frequency exceeds n / 2.",
                    "Return that key."
                ],
                "whySlow": "Requires O(n) auxiliary space to store frequency counts.",
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public int majorityElement(int[] nums) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int n : nums) {
            int c = map.getOrDefault(n, 0) + 1;
            if (c > nums.length / 2) return n;
            map.put(n, c);
        }
        return nums[0];
    }
}""",
                    "python": """class Solution:
    def majorityElement(self, nums: list[int]) -> int:
        c = collections.Counter(nums)
        return max(c.keys(), key=c.get)"""
                }
            },
            "optimal": {
                "idea": "Boyer-Moore Voting Algorithm: maintain a candidate and a counter, canceling out different elements to retain the majority in O(1) space.",
                "steps": [
                    "Initialize candidate = 0, count = 0.",
                    "For each number x in nums:",
                    "If count == 0, candidate = x.",
                    "Increment count if x == candidate, else decrement count.",
                    "Return candidate."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int majorityElement(int[] nums) {
        int candidate = 0, count = 0;
        for (int x : nums) {
            if (count == 0) candidate = x;
            count += (x == candidate) ? 1 : -1;
        }
        return candidate;
    }
}""",
                    "python": """class Solution:
    def majorityElement(self, nums: list[int]) -> int:
        cand, count = 0, 0
        for x in nums:
            if count == 0:
                cand = x
            count += 1 if x == cand else -1
        return cand"""
                }
            }
        },
        {
            "seq": 7,
            "whyNext": "Generalizes Majority Element: Boyer-Moore with two candidates for elements appearing > n/3 times.",
            "brute": {
                "idea": "Count element frequencies in a HashMap and collect elements with count > n / 3.",
                "steps": [
                    "Count all occurrences with a HashMap.",
                    "Iterate over map keys and keep those with count > n / 3.",
                    "Return list of matching keys."
                ],
                "whySlow": "Uses O(n) space for the hash map.",
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public List<Integer> majorityElement(int[] nums) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int n : nums) map.put(n, map.getOrDefault(n, 0) + 1);
        List<Integer> res = new ArrayList<>();
        int threshold = nums.length / 3;
        for (int k : map.keySet()) {
            if (map.get(k) > threshold) res.add(k);
        }
        return res;
    }
}""",
                    "python": """class Solution:
    def majorityElement(self, nums: list[int]) -> list[int]:
        c = collections.Counter(nums)
        return [k for k, v in c.items() if v > len(nums) // 3]"""
                }
            },
            "optimal": {
                "idea": "Boyer-Moore with two candidates and counters, followed by a verification pass.",
                "steps": [
                    "Maintain candidate1, candidate2, count1, count2.",
                    "First pass: update candidates and counts.",
                    "Second pass: count actual occurrences of both candidates.",
                    "Add candidate to result if count > n / 3."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public List<Integer> majorityElement(int[] nums) {
        int cand1 = 0, cand2 = 0, count1 = 0, count2 = 0;
        for (int n : nums) {
            if (n == cand1) count1++;
            else if (n == cand2) count2++;
            else if (count1 == 0) { cand1 = n; count1 = 1; }
            else if (count2 == 0) { cand2 = n; count2 = 1; }
            else { count1--; count2--; }
        }
        count1 = 0; count2 = 0;
        for (int n : nums) {
            if (n == cand1) count1++;
            else if (n == cand2) count2++;
        }
        List<Integer> res = new ArrayList<>();
        if (count1 > nums.length / 3) res.add(cand1);
        if (cand2 != cand1 && count2 > nums.length / 3) res.add(cand2);
        return res;
    }
}""",
                    "python": """class Solution:
    def majorityElement(self, nums: list[int]) -> list[int]:
        cand1, cand2, count1, count2 = None, None, 0, 0
        for x in nums:
            if x == cand1: count1 += 1
            elif x == cand2: count2 += 1
            elif count1 == 0: cand1, count1 = x, 1
            elif count2 == 0: cand2, count2 = x, 1
            else: count1 -= 1; count2 -= 1
        res = []
        for c in (cand1, cand2):
            if c is not None and nums.count(c) > len(nums) // 3 and c not in res:
                res.append(c)
        return res"""
                }
            }
        },
        {
            "seq": 8,
            "whyNext": "Shifts from frequency counting to prefix and suffix array calculations without division.",
            "brute": {
                "idea": "For each index i, iterate through all other indices j != i and multiply nums[j].",
                "steps": [
                    "Create result array of size n.",
                    "For each i from 0 to n - 1, compute product of all nums[j] where j != i.",
                    "Store product in result[i]."
                ],
                "whySlow": "Multiplying n-1 numbers for all n positions takes O(n²) time.",
                "time": "O(n²)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int[] productExceptSelf(int[] nums) {
        int n = nums.length;
        int[] res = new int[n];
        for (int i = 0; i < n; i++) {
            int prod = 1;
            for (int j = 0; j < n; j++) {
                if (i != j) prod *= nums[j];
            }
            res[i] = prod;
        }
        return res;
    }
}""",
                    "python": """class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        n = len(nums)
        res = [1] * n
        for i in range(n):
            prod = 1
            for j in range(n):
                if i != j:
                    prod *= nums[j]
            res[i] = prod
        return res"""
                }
            },
            "optimal": {
                "idea": "Compute running prefix products in a left-to-right pass and multiply with running suffix products in a right-to-left pass.",
                "steps": [
                    "Initialize result array with res[0] = 1.",
                    "Left pass: res[i] = res[i - 1] * nums[i - 1].",
                    "Right pass: maintain suffix product R = 1, multiply res[i] by R, then update R *= nums[i].",
                    "Return res."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int[] productExceptSelf(int[] nums) {
        int n = nums.length;
        int[] res = new int[n];
        res[0] = 1;
        for (int i = 1; i < n; i++) res[i] = res[i - 1] * nums[i - 1];
        int right = 1;
        for (int i = n - 1; i >= 0; i--) {
            res[i] *= right;
            right *= nums[i];
        }
        return res;
    }
}""",
                    "python": """class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        n = len(nums)
        res = [1] * n
        for i in range(1, n):
            res[i] = res[i - 1] * nums[i - 1]
        right = 1
        for i in range(n - 1, -1, -1):
            res[i] *= right
            right *= nums[i]
        return res"""
                }
            }
        },
        {
            "seq": 9,
            "whyNext": "Builds on prefix products to introduce prefix sums with a hash map of frequencies for range queries.",
            "brute": {
                "idea": "Sum every subarray using two nested loops and count those equal to k.",
                "steps": [
                    "Loop start i from 0 to n - 1.",
                    "Maintain running sum, looping end j from i to n - 1.",
                    "Add nums[j] to sum.",
                    "If sum == k, increment count."
                ],
                "whySlow": "Evaluating all n² subarrays takes O(n²) time.",
                "time": "O(n²)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int subarraySum(int[] nums, int k) {
        int count = 0;
        for (int i = 0; i < nums.length; i++) {
            int sum = 0;
            for (int j = i; j < nums.length; j++) {
                sum += nums[j];
                if (sum == k) count++;
            }
        }
        return count;
    }
}""",
                    "python": """class Solution:
    def subarraySum(self, nums: list[int], k: int) -> int:
        count = 0
        for i in range(len(nums)):
            curr = 0
            for j in range(i, len(nums)):
                curr += nums[j]
                if curr == k:
                    count += 1
        return count"""
                }
            },
            "optimal": {
                "idea": "Maintain a running prefix sum and a map of prefix sum frequencies. Subarray sum is k when prefix_sum - k was seen previously.",
                "steps": [
                    "Initialize map with {0: 1} and count = 0, current_sum = 0.",
                    "For each number x in nums:",
                    "current_sum += x.",
                    "count += map.getOrDefault(current_sum - k, 0).",
                    "Increment map frequency of current_sum."
                ],
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public int subarraySum(int[] nums, int k) {
        Map<Integer, Integer> map = new HashMap<>();
        map.put(0, 1);
        int sum = 0, count = 0;
        for (int x : nums) {
            sum += x;
            count += map.getOrDefault(sum - k, 0);
            map.put(sum, map.getOrDefault(sum, 0) + 1);
        }
        return count;
    }
}""",
                    "python": """class Solution:
    def subarraySum(self, nums: list[int], k: int) -> int:
        map_ = collections.defaultdict(int)
        map_[0] = 1
        curr, count = 0, 0
        for x in nums:
            curr += x
            count += map_[curr - k]
            map_[curr] += 1
        return count"""
                }
            }
        },
        {
            "seq": 10,
            "whyNext": "Builds on prefix sums from Subarray Sum Equals K: treat 0 as -1, turning equal 0s and 1s into subarray sum = 0.",
            "brute": {
                "idea": "Test every subarray to see if the count of zeros equals the count of ones.",
                "steps": [
                    "Loop i from 0 to n - 1.",
                    "Loop j from i to n - 1, tracking counts of 0s and 1s.",
                    "If zeroes == ones, update max_len with j - i + 1."
                ],
                "whySlow": "Checking all subarrays requires O(n²) operations.",
                "time": "O(n²)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int findMaxLength(int[] nums) {
        int maxLen = 0;
        for (int i = 0; i < nums.length; i++) {
            int zeros = 0, ones = 0;
            for (int j = i; j < nums.length; j++) {
                if (nums[j] == 0) zeros++; else ones++;
                if (zeros == ones) maxLen = Math.max(maxLen, j - i + 1);
            }
        }
        return maxLen;
    }
}""",
                    "python": """class Solution:
    def findMaxLength(self, nums: list[int]) -> int:
        max_len = 0
        for i in range(len(nums)):
            z, o = 0, 0
            for j in range(i, len(nums)):
                if nums[j] == 0: z += 1
                else: o += 1
                if z == o: max_len = max(max_len, j - i + 1)
        return max_len"""
                }
            },
            "optimal": {
                "idea": "Transform 0 to -1. An equal number of 0s and 1s produces a prefix sum equal to an earlier prefix sum.",
                "steps": [
                    "Use a HashMap to store the earliest index of each prefix sum, initialized with map.put(0, -1).",
                    "Iterate through nums, adding 1 for a 1 and -1 for a 0.",
                    "If current sum exists in map, maxLen = max(maxLen, i - map.get(sum)).",
                    "Otherwise, record map.put(sum, i)."
                ],
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public int findMaxLength(int[] nums) {
        Map<Integer, Integer> map = new HashMap<>();
        map.put(0, -1);
        int sum = 0, maxLen = 0;
        for (int i = 0; i < nums.length; i++) {
            sum += (nums[i] == 1 ? 1 : -1);
            if (map.containsKey(sum)) {
                maxLen = Math.max(maxLen, i - map.get(sum));
            } else {
                map.put(sum, i);
            }
        }
        return maxLen;
    }
}""",
                    "python": """class Solution:
    def findMaxLength(self, nums: list[int]) -> int:
        map_ = {0: -1}
        curr, max_len = 0, 0
        for i, x in enumerate(nums):
            curr += 1 if x == 1 else -1
            if curr in map_:
                max_len = max(max_len, i - map_[curr])
            else:
                map_[curr] = i
        return max_len"""
                }
            }
        },
        {
            "seq": 11,
            "whyNext": "Builds on prefix sums: two prefix sums with identical modulo k differ by a multiple of k.",
            "brute": {
                "idea": "Compute the sum of every subarray and check if it is divisible by k.",
                "steps": [
                    "Loop i from 0 to n - 1.",
                    "Maintain sum, looping j from i to n - 1.",
                    "Add nums[j] to sum.",
                    "If sum % k == 0, increment count."
                ],
                "whySlow": "Evaluating every subarray takes O(n²) time.",
                "time": "O(n²)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int subarraysDivByK(int[] nums, int k) {
        int count = 0;
        for (int i = 0; i < nums.length; i++) {
            int sum = 0;
            for (int j = i; j < nums.length; j++) {
                sum += nums[j];
                if (sum % k == 0) count++;
            }
        }
        return count;
    }
}""",
                    "python": """class Solution:
    def subarraysDivByK(self, nums: list[int], k: int) -> int:
        count = 0
        for i in range(len(nums)):
            s = 0
            for j in range(i, len(nums)):
                s += nums[j]
                if s % k == 0: count += 1
        return count"""
                }
            },
            "optimal": {
                "idea": "Count prefix sum remainders modulo k; any two matching remainders bound a subarray divisible by k.",
                "steps": [
                    "Create an array count of size k, initialized with count[0] = 1.",
                    "Iterate through nums, maintaining prefix sum mod k (normalized to non-negative).",
                    "Add count[rem] to answer, then increment count[rem].",
                    "Return total answer."
                ],
                "time": "O(n)",
                "space": "O(k)",
                "code": {
                    "java": """class Solution {
    public int subarraysDivByK(int[] nums, int k) {
        int[] counts = new int[k];
        counts[0] = 1;
        int sum = 0, res = 0;
        for (int x : nums) {
            sum = (sum + x) % k;
            if (sum < 0) sum += k;
            res += counts[sum];
            counts[sum]++;
        }
        return res;
    }
}""",
                    "python": """class Solution:
    def subarraysDivByK(self, nums: list[int], k: int) -> int:
        counts = [0] * k
        counts[0] = 1
        curr, res = 0, 0
        for x in nums:
            curr = (curr + x) % k
            res += counts[curr]
            counts[curr] += 1
        return res"""
                }
            }
        },
        {
            "seq": 12,
            "whyNext": "Builds on Contains Duplicate set lookup: start sequence counting only when num - 1 is absent.",
            "brute": {
                "idea": "Sort the array and then scan linearly to measure lengths of consecutive sequences.",
                "steps": [
                    "If array is empty, return 0.",
                    "Sort array.",
                    "Iterate through sorted elements, counting consecutive values and updating max streak.",
                    "Return max streak."
                ],
                "whySlow": "Sorting requires O(n log n) time.",
                "time": "O(n log n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int longestConsecutive(int[] nums) {
        if (nums.length == 0) return 0;
        Arrays.sort(nums);
        int max = 1, curr = 1;
        for (int i = 1; i < nums.length; i++) {
            if (nums[i] == nums[i - 1]) continue;
            if (nums[i] == nums[i - 1] + 1) curr++;
            else { max = Math.max(max, curr); curr = 1; }
        }
        return Math.max(max, curr);
    }
}""",
                    "python": """class Solution:
    def longestConsecutive(self, nums: list[int]) -> int:
        if not nums: return 0
        nums = sorted(set(nums))
        max_len, curr = 1, 1
        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1] + 1: curr += 1
            else: max_len = max(max_len, curr); curr = 1
        return max(max_len, curr)"""
                }
            },
            "optimal": {
                "idea": "Insert all numbers into a HashSet. Only start expanding a sequence when x - 1 is not in the set.",
                "steps": [
                    "Put all numbers in a HashSet.",
                    "For each number x in set:",
                    "If x - 1 is not in set (start of a streak):",
                    "Count how many consecutive elements x+1, x+2 exist.",
                    "Update longest streak."
                ],
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public int longestConsecutive(int[] nums) {
        Set<Integer> set = new HashSet<>();
        for (int x : nums) set.add(x);
        int longest = 0;
        for (int x : set) {
            if (!set.contains(x - 1)) {
                int curr = x, streak = 1;
                while (set.contains(curr + 1)) { curr++; streak++; }
                longest = Math.max(longest, streak);
            }
        }
        return longest;
    }
}""",
                    "python": """class Solution:
    def longestConsecutive(self, nums: list[int]) -> int:
        num_set = set(nums)
        longest = 0
        for x in num_set:
            if x - 1 not in num_set:
                curr = x
                streak = 1
                while curr + 1 in num_set:
                    curr += 1
                    streak += 1
                longest = max(longest, streak)
        return longest"""
                }
            }
        },
        {
            "seq": 13,
            "whyNext": "Builds on Contains Duplicate: uses array indices as hash keys with sign-negation for O(1) extra space.",
            "brute": {
                "idea": "Use a HashSet to keep track of seen elements and collect duplicates.",
                "steps": [
                    "Initialize a HashSet of seen numbers.",
                    "Initialize a result list.",
                    "For each number, if already in set, add to result; otherwise add to set."
                ],
                "whySlow": "Uses O(n) auxiliary memory for the set.",
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public List<Integer> findDuplicates(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        List<Integer> res = new ArrayList<>();
        for (int x : nums) {
            if (seen.contains(x)) res.add(x);
            else seen.add(x);
        }
        return res;
    }
}""",
                    "python": """class Solution:
    def findDuplicates(self, nums: list[int]) -> list[int]:
        seen = set()
        res = []
        for x in nums:
            if x in seen: res.append(x)
            else: seen.add(x)
        return res"""
                }
            },
            "optimal": {
                "idea": "Use numbers as 1-based indices and negate the value at nums[abs(x) - 1] to mark visitation.",
                "steps": [
                    "For each x in nums:",
                    "idx = abs(x) - 1.",
                    "If nums[idx] < 0, it has been visited before, so add abs(x) to result.",
                    "Otherwise negate nums[idx]."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public List<Integer> findDuplicates(int[] nums) {
        List<Integer> res = new ArrayList<>();
        for (int i = 0; i < nums.length; i++) {
            int idx = Math.abs(nums[i]) - 1;
            if (nums[idx] < 0) res.add(idx + 1);
            else nums[idx] = -nums[idx];
        }
        return res;
    }
}""",
                    "python": """class Solution:
    def findDuplicates(self, nums: list[int]) -> list[int]:
        res = []
        for x in nums:
            idx = abs(x) - 1
            if nums[idx] < 0:
                res.append(idx + 1)
            else:
                nums[idx] = -nums[idx]
        return res"""
                }
            }
        },
        {
            "seq": 14,
            "whyNext": "Builds on index-mapping from Find All Duplicates: applies Floyd's cycle detection without modifying the array.",
            "brute": {
                "idea": "Sort the array and scan adjacent elements to find the duplicate.",
                "steps": [
                    "Sort nums.",
                    "Compare each adjacent pair nums[i] and nums[i + 1].",
                    "Return matching element."
                ],
                "whySlow": "Modifies input array or requires O(n log n) sorting.",
                "time": "O(n log n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int findDuplicate(int[] nums) {
        Arrays.sort(nums);
        for (int i = 1; i < nums.length; i++) {
            if (nums[i] == nums[i - 1]) return nums[i];
        }
        return -1;
    }
}""",
                    "python": """class Solution:
    def findDuplicate(self, nums: list[int]) -> int:
        nums.sort()
        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1]:
                return nums[i]
        return -1"""
                }
            },
            "optimal": {
                "idea": "Floyd's Tortoise and Hare cycle detection treating nums[i] as a pointer to index nums[i].",
                "steps": [
                    "Initialize slow = nums[0], fast = nums[0].",
                    "Advance slow = nums[slow] and fast = nums[nums[fast]] until they meet.",
                    "Reset slow = nums[0].",
                    "Advance both slow and fast by one step until they meet at cycle entrance."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int findDuplicate(int[] nums) {
        int slow = nums[0], fast = nums[0];
        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
        } while (slow != fast);
        slow = nums[0];
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
        }
        return slow;
    }
}""",
                    "python": """class Solution:
    def findDuplicate(self, nums: list[int]) -> int:
        slow = nums[0]
        fast = nums[0]
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break
        slow = nums[0]
        while slow != fast:
            slow = nums[slow]
            fast = nums[fast]
        return slow"""
                }
            }
        },
        {
            "seq": 15,
            "whyNext": "Builds on in-place indexing: cyclic placement places each value x at index x - 1 to find the missing positive.",
            "brute": {
                "idea": "Insert all numbers into a set and test 1, 2, 3... until one is missing.",
                "steps": [
                    "Put all elements into a HashSet.",
                    "Check 1, 2, 3...",
                    "Return the first integer not present in set."
                ],
                "whySlow": "Requires O(n) auxiliary space.",
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public int firstMissingPositive(int[] nums) {
        Set<Integer> set = new HashSet<>();
        for (int x : nums) set.add(x);
        int i = 1;
        while (set.contains(i)) i++;
        return i;
    }
}""",
                    "python": """class Solution:
    def firstMissingPositive(self, nums: list[int]) -> int:
        s = set(nums)
        i = 1
        while i in s:
            i += 1
        return i"""
                }
            },
            "optimal": {
                "idea": "Cyclic sort: place each number x where 1 <= x <= n at its correct position nums[x - 1].",
                "steps": [
                    "For each index i, while nums[i] is in [1, n] and nums[nums[i] - 1] != nums[i], swap nums[i] with nums[nums[i] - 1].",
                    "Scan from 0 to n - 1; if nums[i] != i + 1, return i + 1.",
                    "If all match, return n + 1."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int firstMissingPositive(int[] nums) {
        int n = nums.length;
        for (int i = 0; i < n; i++) {
            while (nums[i] > 0 && nums[i] <= n && nums[nums[i] - 1] != nums[i]) {
                int targetIdx = nums[i] - 1;
                int temp = nums[i];
                nums[i] = nums[targetIdx];
                nums[targetIdx] = temp;
            }
        }
        for (int i = 0; i < n; i++) {
            if (nums[i] != i + 1) return i + 1;
        }
        return n + 1;
    }
}""",
                    "python": """class Solution:
    def firstMissingPositive(self, nums: list[int]) -> int:
        n = len(nums)
        for i in range(n):
            while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
                idx = nums[i] - 1
                nums[i], nums[idx] = nums[idx], nums[i]
        for i in range(n):
            if nums[i] != i + 1:
                return i + 1
        return n + 1"""
                }
            }
        },
        {
            "seq": 16,
            "whyNext": "Applies hash set duplicate detection in a 2D matrix across rows, columns, and 3x3 sub-boxes.",
            "brute": {
                "idea": "Perform three separate passes over the board: check all rows, then all columns, then all 9 boxes.",
                "steps": [
                    "Pass 1: Check each row with a set for duplicates.",
                    "Pass 2: Check each column with a set for duplicates.",
                    "Pass 3: Check each 3x3 block with a set for duplicates."
                ],
                "whySlow": "Traverses the 9x9 board 3 times separately.",
                "time": "O(1)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public boolean isValidSudoku(char[][] board) {
        for (int r = 0; r < 9; r++) {
            Set<Character> seen = new HashSet<>();
            for (int c = 0; c < 9; c++) {
                if (board[r][c] != '.' && !seen.add(board[r][c])) return false;
            }
        }
        for (int c = 0; c < 9; c++) {
            Set<Character> seen = new HashSet<>();
            for (int r = 0; r < 9; r++) {
                if (board[r][c] != '.' && !seen.add(board[r][c])) return false;
            }
        }
        for (int b = 0; b < 9; b++) {
            Set<Character> seen = new HashSet<>();
            for (int r = 0; r < 3; r++) {
                for (int c = 0; c < 3; c++) {
                    char ch = board[(b / 3) * 3 + r][(b % 3) * 3 + c];
                    if (ch != '.' && !seen.add(ch)) return false;
                }
            }
        }
        return true;
    }
}""",
                    "python": """class Solution:
    def isValidSudoku(self, board: list[list[str]]) -> bool:
        for r in range(9):
            s = set()
            for c in range(9):
                if board[r][c] != '.':
                    if board[r][c] in s: return False
                    s.add(board[r][c])
        for c in range(9):
            s = set()
            for r in range(9):
                if board[r][c] != '.':
                    if board[r][c] in s: return False
                    s.add(board[r][c])
        for b in range(9):
            s = set()
            for r in range(3):
                for c in range(3):
                    ch = board[(b // 3) * 3 + r][(b % 3) * 3 + c]
                    if ch != '.':
                        if ch in s: return False
                        s.add(ch)
        return True"""
                }
            },
            "optimal": {
                "idea": "Single pass: record digit in row, column, and box bitmasks or boolean arrays.",
                "steps": [
                    "Initialize boolean arrays rows[9][9], cols[9][9], boxes[9][9].",
                    "Iterate over every cell (r, c).",
                    "If cell contains digit d, calculate boxIdx = (r/3)*3 + c/3.",
                    "If already recorded in row, col, or box, return false.",
                    "Record digit in all three."
                ],
                "time": "O(1)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public boolean isValidSudoku(char[][] board) {
        boolean[][] rows = new boolean[9][9];
        boolean[][] cols = new boolean[9][9];
        boolean[][] boxes = new boolean[9][9];
        for (int r = 0; r < 9; r++) {
            for (int c = 0; c < 9; c++) {
                if (board[r][c] != '.') {
                    int val = board[r][c] - '1';
                    int b = (r / 3) * 3 + c / 3;
                    if (rows[r][val] || cols[c][val] || boxes[b][val]) return false;
                    rows[r][val] = cols[c][val] = boxes[b][val] = true;
                }
            }
        }
        return true;
    }
}""",
                    "python": """class Solution:
    def isValidSudoku(self, board: list[list[str]]) -> bool:
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]
        for r in range(9):
            for c in range(9):
                val = board[r][c]
                if val != '.':
                    b = (r // 3) * 3 + c // 3
                    if val in rows[r] or val in cols[c] or val in boxes[b]:
                        return False
                    rows[r].add(val)
                    cols[c].add(val)
                    boxes[b].add(val)
        return True"""
                }
            }
        },
        {
            "seq": 17,
            "whyNext": "Builds on matrix cell coordinate tracking: uses the first row and column as marker storage for O(1) space.",
            "brute": {
                "idea": "Copy the matrix, then for any cell with 0 in the copy, zero out the corresponding row and column in the original.",
                "steps": [
                    "Create a deep copy of matrix.",
                    "Scan the copy.",
                    "Whenever copy[r][c] == 0, set all cells in row r and column c of matrix to 0."
                ],
                "whySlow": "Requires O(mn) space for matrix clone.",
                "time": "O(mn)",
                "space": "O(mn)",
                "code": {
                    "java": """class Solution {
    public void setZeroes(int[][] matrix) {
        int m = matrix.length, n = matrix[0].length;
        int[][] copy = new int[m][n];
        for (int i = 0; i < m; i++) copy[i] = matrix[i].clone();
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (copy[i][j] == 0) {
                    for (int c = 0; c < n; c++) matrix[i][c] = 0;
                    for (int r = 0; r < m; r++) matrix[r][j] = 0;
                }
            }
        }
    }
}""",
                    "python": """class Solution:
    def setZeroes(self, matrix: list[list[int]]) -> None:
        m, n = len(matrix), len(matrix[0])
        copy_ = [row[:] for row in matrix]
        for r in range(m):
            for c in range(n):
                if copy_[r][c] == 0:
                    for j in range(n): matrix[r][j] = 0
                    for i in range(m): matrix[i][c] = 0"""
                }
            },
            "optimal": {
                "idea": "Use the first row and column as markers for zeroing, tracking first row and first column state with two flags.",
                "steps": [
                    "Record whether first row and first column contain zeros.",
                    "Use matrix[i][0] and matrix[0][j] to mark zero rows and columns.",
                    "Update inner cells from 1 to m-1 and 1 to n-1.",
                    "Zero out first row and column if indicated by their flags."
                ],
                "time": "O(mn)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public void setZeroes(int[][] matrix) {
        int m = matrix.length, n = matrix[0].length;
        boolean firstRowZero = false, firstColZero = false;
        for (int i = 0; i < m; i++) if (matrix[i][0] == 0) firstColZero = true;
        for (int j = 0; j < n; j++) if (matrix[0][j] == 0) firstRowZero = true;
        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                if (matrix[i][j] == 0) { matrix[i][0] = 0; matrix[0][j] = 0; }
            }
        }
        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                if (matrix[i][0] == 0 || matrix[0][j] == 0) matrix[i][j] = 0;
            }
        }
        if (firstColZero) for (int i = 0; i < m; i++) matrix[i][0] = 0;
        if (firstRowZero) for (int j = 0; j < n; j++) matrix[0][j] = 0;
    }
}""",
                    "python": """class Solution:
    def setZeroes(self, matrix: list[list[int]]) -> None:
        m, n = len(matrix), len(matrix[0])
        first_row_zero = any(matrix[0][j] == 0 for j in range(n))
        first_col_zero = any(matrix[i][0] == 0 for i in range(m))
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0
                    matrix[0][j] = 0
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0
        if first_col_zero:
            for i in range(m): matrix[i][0] = 0
        if first_row_zero:
            for j in range(n): matrix[0][j] = 0"""
                }
            }
        },
        {
            "seq": 18,
            "whyNext": "Builds on matrix cell construction: row-by-row generation where each value depends on the previous row's adjacent cells.",
            "brute": {
                "idea": "Compute each cell value using the mathematical combination formula C(n, k) = n! / (k!(n-k)!).",
                "steps": [
                    "For each row r from 0 to numRows - 1:",
                    "Compute each entry c using factorial combination calculation.",
                    "Append row to triangle."
                ],
                "whySlow": "Computing factorials repeatedly takes O(n³) and risks integer overflow.",
                "time": "O(n³)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public List<List<Integer>> generate(int numRows) {
        List<List<Integer>> res = new ArrayList<>();
        for (int i = 0; i < numRows; i++) {
            List<Integer> row = new ArrayList<>();
            for (int j = 0; j <= i; j++) {
                row.add((int) comb(i, j));
            }
            res.add(row);
        }
        return res;
    }
    private long comb(int n, int k) {
        long res = 1;
        for (int i = 1; i <= k; i++) res = res * (n - i + 1) / i;
        return res;
    }
}""",
                    "python": """class Solution:
    def generate(self, numRows: int) -> list[list[int]]:
        res = []
        for i in range(numRows):
            row = []
            for j in range(i + 1):
                row.append(math.comb(i, j))
            res.append(row)
        return res"""
                }
            },
            "optimal": {
                "idea": "Build each row from the previous row: row[j] = prev[j-1] + prev[j] with boundary 1s.",
                "steps": [
                    "Initialize triangle list.",
                    "For each row i from 0 to numRows - 1:",
                    "Create row with 1 at start and end.",
                    "Inner elements equal prevRow[j-1] + prevRow[j].",
                    "Add row to triangle."
                ],
                "time": "O(n²)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public List<List<Integer>> generate(int numRows) {
        List<List<Integer>> res = new ArrayList<>();
        for (int i = 0; i < numRows; i++) {
            List<Integer> row = new ArrayList<>();
            for (int j = 0; j <= i; j++) {
                if (j == 0 || j == i) row.add(1);
                else {
                    List<Integer> prev = res.get(i - 1);
                    row.add(prev.get(j - 1) + prev.get(j));
                }
            }
            res.add(row);
        }
        return res;
    }
}""",
                    "python": """class Solution:
    def generate(self, numRows: int) -> list[list[int]]:
        res = []
        for i in range(numRows):
            row = [1] * (i + 1)
            for j in range(1, i):
                row[j] = res[i - 1][j - 1] + res[i - 1][j]
            res.append(row)
        return res"""
                }
            }
        },
        {
            "seq": 19,
            "whyNext": "Builds on 2D grid iteration: traversing a matrix layer by layer while shrinking four boundary walls.",
            "brute": {
                "idea": "Maintain a visited 2D boolean array and attempt movement along directions, turning right when hitting a visited cell.",
                "steps": [
                    "Initialize m x n visited matrix.",
                    "Start at (0, 0) heading right.",
                    "Step forward while valid and unvisited; turn clockwise when hitting boundary or visited cell.",
                    "Stop after visiting m * n cells."
                ],
                "whySlow": "Uses O(mn) extra space for visited table.",
                "time": "O(mn)",
                "space": "O(mn)",
                "code": {
                    "java": """class Solution {
    public List<Integer> spiralOrder(int[][] matrix) {
        List<Integer> res = new ArrayList<>();
        int m = matrix.length, n = matrix[0].length;
        boolean[][] visited = new boolean[m][n];
        int[] dr = {0, 1, 0, -1}, dc = {1, 0, -1, 0};
        int r = 0, c = 0, di = 0;
        for (int i = 0; i < m * n; i++) {
            res.add(matrix[r][c]);
            visited[r][c] = true;
            int nr = r + dr[di], nc = c + dc[di];
            if (nr >= 0 && nr < m && nc >= 0 && nc < n && !visited[nr][nc]) {
                r = nr; c = nc;
            } else {
                di = (di + 1) % 4;
                r += dr[di]; c += dc[di];
            }
        }
        return res;
    }
}""",
                    "python": """class Solution:
    def spiralOrder(self, matrix: list[list[int]]) -> list[int]:
        m, n = len(matrix), len(matrix[0])
        vis = [[False]*n for _ in range(m)]
        dr, dc = [0, 1, 0, -1], [1, 0, -1, 0]
        r = c = di = 0
        res = []
        for _ in range(m * n):
            res.append(matrix[r][c])
            vis[r][c] = True
            nr, nc = r + dr[di], c + dc[di]
            if 0 <= nr < m and 0 <= nc < n and not vis[nr][nc]:
                r, c = nr, nc
            else:
                di = (di + 1) % 4
                r += dr[di]
                c += dc[di]
        return res"""
                }
            },
            "optimal": {
                "idea": "Traverse four boundaries (top, right, bottom, left), shrinking boundaries inwards after each side.",
                "steps": [
                    "Initialize top = 0, bottom = m - 1, left = 0, right = n - 1.",
                    "While left <= right and top <= bottom:",
                    "Traverse top row, increment top.",
                    "Traverse right column, decrement right.",
                    "If top <= bottom, traverse bottom row, decrement bottom.",
                    "If left <= right, traverse left column, increment left."
                ],
                "time": "O(mn)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public List<Integer> spiralOrder(int[][] matrix) {
        List<Integer> res = new ArrayList<>();
        int top = 0, bottom = matrix.length - 1, left = 0, right = matrix[0].length - 1;
        while (left <= right && top <= bottom) {
            for (int c = left; c <= right; c++) res.add(matrix[top][c]);
            top++;
            for (int r = top; r <= bottom; r++) res.add(matrix[r][right]);
            right--;
            if (top <= bottom) {
                for (int c = right; c >= left; c--) res.add(matrix[bottom][c]);
                bottom--;
            }
            if (left <= right) {
                for (int r = bottom; r >= top; r--) res.add(matrix[r][left]);
                left++;
            }
        }
        return res;
    }
}""",
                    "python": """class Solution:
    def spiralOrder(self, matrix: list[list[int]]) -> list[int]:
        res = []
        top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
        while left <= right and top <= bottom:
            for c in range(left, right + 1): res.append(matrix[top][c])
            top += 1
            for r in range(top, bottom + 1): res.append(matrix[r][right])
            right -= 1
            if top <= bottom:
                for c in range(right, left - 1, -1): res.append(matrix[bottom][c])
                bottom -= 1
            if left <= right:
                for r in range(bottom, top - 1, -1): res.append(matrix[r][left])
                left += 1
        return res"""
                }
            }
        },
        {
            "seq": 20,
            "whyNext": "Builds on matrix cell coordinate manipulation: transpose the matrix across main diagonal, then reverse each row.",
            "brute": {
                "idea": "Create a new n x n matrix and copy elements such that newMatrix[j][n - 1 - i] = matrix[i][j].",
                "steps": [
                    "Allocate new matrix rotated of size n x n.",
                    "For each (i, j), rotated[j][n - 1 - i] = matrix[i][j].",
                    "Copy back to original matrix."
                ],
                "whySlow": "Requires O(n²) extra memory.",
                "time": "O(n²)",
                "space": "O(n²)",
                "code": {
                    "java": """class Solution {
    public void rotate(int[][] matrix) {
        int n = matrix.length;
        int[][] res = new int[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) res[j][n - 1 - i] = matrix[i][j];
        }
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) matrix[i][j] = res[i][j];
        }
    }
}""",
                    "python": """class Solution:
    def rotate(self, matrix: list[list[int]]) -> None:
        n = len(matrix)
        res = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                res[j][n - 1 - i] = matrix[i][j]
        for i in range(n):
            for j in range(n):
                matrix[i][j] = res[i][j]"""
                }
            },
            "optimal": {
                "idea": "In-place rotation: transpose matrix (swap matrix[i][j] with matrix[j][i]), then reverse each row.",
                "steps": [
                    "Transpose: loop i from 0 to n-1, j from i+1 to n-1, swapping matrix[i][j] with matrix[j][i].",
                    "Reverse rows: for each row, swap elements from left to right."
                ],
                "time": "O(n²)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public void rotate(int[][] matrix) {
        int n = matrix.length;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                int temp = matrix[i][j];
                matrix[i][j] = matrix[j][i];
                matrix[j][i] = temp;
            }
        }
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n / 2; j++) {
                int temp = matrix[i][j];
                matrix[i][j] = matrix[i][n - 1 - j];
                matrix[i][n - 1 - j] = temp;
            }
        }
    }
}""",
                    "python": """class Solution:
    def rotate(self, matrix: list[list[int]]) -> None:
        n = len(matrix)
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        for i in range(n):
            matrix[i].reverse()"""
                }
            }
        },
        {
            "seq": 21,
            "whyNext": "Completes Chapter 1: in-place array reversal trick (reverse all, reverse first k, reverse remaining n-k).",
            "brute": {
                "idea": "Shift all array elements by 1 position to the right, repeated k times.",
                "steps": [
                    "k = k % n.",
                    "Repeat k times:",
                    "Save last element.",
                    "Shift all elements one step right.",
                    "Place saved element at index 0."
                ],
                "whySlow": "Repeated shifts take O(n * k) time.",
                "time": "O(nk)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public void rotate(int[] nums, int k) {
        int n = nums.length;
        k %= n;
        for (int step = 0; step < k; step++) {
            int last = nums[n - 1];
            for (int i = n - 1; i > 0; i--) nums[i] = nums[i - 1];
            nums[0] = last;
        }
    }
}""",
                    "python": """class Solution:
    def rotate(self, nums: list[int], k: int) -> None:
        n = len(nums)
        k %= n
        for _ in range(k):
            last = nums[-1]
            for i in range(n - 1, 0, -1):
                nums[i] = nums[i - 1]
            nums[0] = last"""
                }
            },
            "optimal": {
                "idea": "Reverse the entire array, reverse the first k elements, then reverse the remaining n-k elements.",
                "steps": [
                    "Normalize k = k % n.",
                    "Reverse nums[0 ... n - 1].",
                    "Reverse nums[0 ... k - 1].",
                    "Reverse nums[k ... n - 1]."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public void rotate(int[] nums, int k) {
        int n = nums.length;
        k %= n;
        reverse(nums, 0, n - 1);
        reverse(nums, 0, k - 1);
        reverse(nums, k, n - 1);
    }
    private void reverse(int[] nums, int l, int r) {
        while (l < r) {
            int temp = nums[l];
            nums[l] = nums[r];
            nums[r] = temp;
            l++; r--;
        }
    }
}""",
                    "python": """class Solution:
    def rotate(self, nums: list[int], k: int) -> None:
        n = len(nums)
        k %= n
        def rev(l, r):
            while l < r:
                nums[l], nums[r] = nums[r], nums[l]
                l += 1; r -= 1
        rev(0, n - 1)
        rev(0, k - 1)
        rev(k, n - 1)"""
                }
            }
        },
        {
            "seq": 22,
            "whyNext": "Opens Chapter 2 (Two Pointers): moving inward from opposite ends to verify palindrome symmetry.",
            "brute": {
                "idea": "Filter alphanumeric characters, convert to lowercase, reverse the string and compare with original.",
                "steps": [
                    "Build a string of cleaned alphanumeric characters in lowercase.",
                    "Compare cleaned string with its reverse."
                ],
                "whySlow": "Allocates extra memory to construct reversed strings.",
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public boolean isPalindrome(String s) {
        StringBuilder sb = new StringBuilder();
        for (char c : s.toCharArray()) {
            if (Character.isLetterOrDigit(c)) sb.append(Character.toLowerCase(c));
        }
        String clean = sb.toString();
        return clean.equals(sb.reverse().toString());
    }
}""",
                    "python": """class Solution:
    def isPalindrome(self, s: str) -> bool:
        clean = [c.lower() for c in s if c.isalnum()]
        return clean == clean[::-1]"""
                }
            },
            "optimal": {
                "idea": "Two pointers left and right moving inward, skipping non-alphanumeric characters, and comparing case-insensitively.",
                "steps": [
                    "Initialize left = 0, right = s.length() - 1.",
                    "Advance left until alphanumeric; decrement right until alphanumeric.",
                    "If characters differ, return false.",
                    "Increment left, decrement right until pointers cross."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public boolean isPalindrome(String s) {
        int l = 0, r = s.length() - 1;
        while (l < r) {
            while (l < r && !Character.isLetterOrDigit(s.charAt(l))) l++;
            while (l < r && !Character.isLetterOrDigit(s.charAt(r))) r--;
            if (Character.toLowerCase(s.charAt(l)) != Character.toLowerCase(s.charAt(r))) return false;
            l++; r--;
        }
        return true;
    }
}""",
                    "python": """class Solution:
    def isPalindrome(self, s: str) -> bool:
        l, r = 0, len(s) - 1
        while l < r:
            while l < r and not s[l].isalnum(): l += 1
            while l < r and not s[r].isalnum(): r -= 1
            if s[l].lower() != s[r].lower(): return False
            l += 1; r -= 1
        return True"""
                }
            }
        },
        {
            "seq": 23,
            "whyNext": "Builds on Valid Palindrome: when mismatch occurs, branch to check if skipping left or right character yields a palindrome.",
            "brute": {
                "idea": "Try deleting each character in turn and test whether the remaining string is a palindrome.",
                "steps": [
                    "For each index i, form string without character i.",
                    "Check if modified string is a palindrome.",
                    "Return true if any variant is valid."
                ],
                "whySlow": "Constructing and checking n string slices takes O(n²) time.",
                "time": "O(n²)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public boolean validPalindrome(String s) {
        if (isPal(s, 0, s.length() - 1)) return true;
        for (int i = 0; i < s.length(); i++) {
            String sub = s.substring(0, i) + s.substring(i + 1);
            if (isPal(sub, 0, sub.length() - 1)) return true;
        }
        return false;
    }
    private boolean isPal(String s, int l, int r) {
        while (l < r) if (s.charAt(l++) != s.charAt(r--)) return false;
        return true;
    }
}""",
                    "python": """class Solution:
    def validPalindrome(self, s: str) -> bool:
        if s == s[::-1]: return True
        for i in range(len(s)):
            sub = s[:i] + s[i+1:]
            if sub == sub[::-1]: return True
        return False"""
                }
            },
            "optimal": {
                "idea": "Two pointers inward; on the first mismatch, test if either s[l+1...r] or s[l...r-1] is a palindrome.",
                "steps": [
                    "Initialize l = 0, r = s.length() - 1.",
                    "While l < r, if s[l] == s[r], advance inward.",
                    "If s[l] != s[r], return isPal(s, l + 1, r) || isPal(s, l, r - 1).",
                    "Return true."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public boolean validPalindrome(String s) {
        int l = 0, r = s.length() - 1;
        while (l < r) {
            if (s.charAt(l) != s.charAt(r)) {
                return isPal(s, l + 1, r) || isPal(s, l, r - 1);
            }
            l++; r--;
        }
        return true;
    }
    private boolean isPal(String s, int l, int r) {
        while (l < r) if (s.charAt(l++) != s.charAt(r--)) return false;
        return true;
    }
}""",
                    "python": """class Solution:
    def validPalindrome(self, s: str) -> bool:
        l, r = 0, len(s) - 1
        while l < r:
            if s[l] != s[r]:
                s1 = s[l+1:r+1]
                s2 = s[l:r]
                return s1 == s1[::-1] or s2 == s2[::-1]
            l += 1; r -= 1
        return True"""
                }
            }
        },
        {
            "seq": 24,
            "whyNext": "Builds on Two Sum: since input array is sorted, replace hash map with inward two pointers for O(1) extra space.",
            "brute": {
                "idea": "Check every pair (i, j) with nested loops to find sum matching target.",
                "steps": [
                    "Loop i from 0 to n - 1.",
                    "Loop j from i + 1 to n - 1.",
                    "If numbers[i] + numbers[j] == target, return 1-based indices [i + 1, j + 1]."
                ],
                "whySlow": "Does not take advantage of sorted order, taking O(n²) time.",
                "time": "O(n²)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int[] twoSum(int[] numbers, int target) {
        for (int i = 0; i < numbers.length; i++) {
            for (int j = i + 1; j < numbers.length; j++) {
                if (numbers[i] + numbers[j] == target) return new int[]{i + 1, j + 1};
            }
        }
        return new int[]{};
    }
}""",
                    "python": """class Solution:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        for i in range(len(numbers)):
            for j in range(i + 1, len(numbers)):
                if numbers[i] + numbers[j] == target:
                    return [i + 1, j + 1]
        return []"""
                }
            },
            "optimal": {
                "idea": "Two pointers from ends: if sum < target, advance left; if sum > target, decrement right.",
                "steps": [
                    "Initialize left = 0, right = numbers.length - 1.",
                    "Compute sum = numbers[left] + numbers[right].",
                    "If sum == target, return [left + 1, right + 1].",
                    "If sum < target, left++.",
                    "Else right--."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int[] twoSum(int[] numbers, int target) {
        int l = 0, r = numbers.length - 1;
        while (l < r) {
            int sum = numbers[l] + numbers[r];
            if (sum == target) return new int[]{l + 1, r + 1};
            if (sum < target) l++;
            else r--;
        }
        return new int[]{};
    }
}""",
                    "python": """class Solution:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        l, r = 0, len(numbers) - 1
        while l < r:
            s = numbers[l] + numbers[r]
            if s == target: return [l + 1, r + 1]
            elif s < target: l += 1
            else: r -= 1
        return []"""
                }
            }
        },
        {
            "seq": 25,
            "whyNext": "Builds on Two Sum II: sort the array, fix one element, and use two pointers to find pairs summing to -nums[i].",
            "brute": {
                "idea": "Enumerate all triplets with three nested loops and deduplicate using a set.",
                "steps": [
                    "Loop i from 0 to n - 1.",
                    "Loop j from i + 1 to n - 1.",
                    "Loop k from j + 1 to n - 1.",
                    "If nums[i] + nums[j] + nums[k] == 0, sort triplet and add to set."
                ],
                "whySlow": "Three nested loops yield cubic O(n³) time complexity.",
                "time": "O(n³)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        Set<List<Integer>> set = new HashSet<>();
        int n = nums.length;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                for (int k = j + 1; k < n; k++) {
                    if (nums[i] + nums[j] + nums[k] == 0) {
                        List<Integer> trip = Arrays.asList(nums[i], nums[j], nums[k]);
                        Collections.sort(trip);
                        set.add(trip);
                    }
                }
            }
        }
        return new ArrayList<>(set);
    }
}""",
                    "python": """class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        res = set()
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if nums[i] + nums[j] + nums[k] == 0:
                        res.add(tuple(sorted([nums[i], nums[j], nums[k]])))
        return [list(t) for t in res]"""
                }
            },
            "optimal": {
                "idea": "Sort nums. For each i, use Two Sum II with two pointers on the remainder of the array, skipping duplicates.",
                "steps": [
                    "Sort nums.",
                    "Loop i from 0 to n - 3; skip duplicates if nums[i] == nums[i-1].",
                    "Set l = i + 1, r = n - 1, target = -nums[i].",
                    "If nums[l] + nums[r] == target, add triplet, advance l and r while skipping duplicates.",
                    "If sum < target l++, else r--."
                ],
                "time": "O(n²)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        Arrays.sort(nums);
        List<List<Integer>> res = new ArrayList<>();
        for (int i = 0; i < nums.length - 2; i++) {
            if (i > 0 && nums[i] == nums[i - 1]) continue;
            int l = i + 1, r = nums.length - 1;
            while (l < r) {
                int sum = nums[i] + nums[l] + nums[r];
                if (sum == 0) {
                    res.add(Arrays.asList(nums[i], nums[l], nums[r]));
                    while (l < r && nums[l] == nums[l + 1]) l++;
                    while (l < r && nums[r] == nums[r - 1]) r--;
                    l++; r--;
                } else if (sum < 0) l++;
                else r--;
            }
        }
        return res;
    }
}""",
                    "python": """class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        res = []
        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            l, r = i + 1, len(nums) - 1
            while l < r:
                s = nums[i] + nums[l] + nums[r]
                if s == 0:
                    res.append([nums[i], nums[l], nums[r]])
                    while l < r and nums[l] == nums[l + 1]: l += 1
                    while l < r and nums[r] == nums[r - 1]: r -= 1
                    l += 1; r -= 1
                elif s < 0: l += 1
                else: r -= 1
        return res"""
                }
            }
        }
    ]


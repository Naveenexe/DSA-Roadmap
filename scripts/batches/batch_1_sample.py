# Batch 1: Seq 1 to 25
import json

def get_batch_1():
    return [
        {
            "seq": 1,
            "lc": 217,
            "title": "Contains Duplicate",
            "whyNext": "Fundamental starting problem: introducing hashing to achieve O(n) lookup over O(n²) pair comparisons.",
            "brute": {
                "idea": "Compare every element with every subsequent element using two nested loops to check for matching pairs.",
                "steps": [
                    "Iterate variable i from 0 to n - 1.",
                    "Iterate variable j from i + 1 to n - 1.",
                    "If nums[i] equals nums[j], return true.",
                    "If loops finish with no duplicates found, return false."
                ],
                "whySlow": "Checking all n(n-1)/2 pairs requires quadratic O(n²) time, causing TLE on large arrays.",
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
                "idea": "Traverse the array once while inserting elements into a HashSet. If an element already exists in the set, a duplicate is found immediately.",
                "steps": [
                    "Initialize an empty HashSet of integers.",
                    "For each number in nums, check if it is already present in the set.",
                    "If present, return true.",
                    "Otherwise, add the number to the set.",
                    "If the loop ends without finding duplicates, return false."
                ],
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public boolean containsDuplicate(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        for (int num : nums) {
            if (!seen.add(num)) return true;
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
            },
            "test": {
                "java_test": "Solution s = new Solution(); if (!s.containsDuplicate(new int[]{1, 2, 3, 1})) throw new RuntimeException();",
                "python_test": "assert Solution().containsDuplicate([1, 2, 3, 1]) == True"
            }
        },
        {
            "seq": 2,
            "lc": 1,
            "title": "Two Sum",
            "whyNext": "Builds on Contains Duplicate: instead of checking whether a number exists, we store its index in a HashMap to find the matching complement.",
            "brute": {
                "idea": "Check every pair of elements using nested loops to see if their sum matches the target value.",
                "steps": [
                    "Loop i from 0 to n - 1.",
                    "Loop j from i + 1 to n - 1.",
                    "If nums[i] + nums[j] == target, return indices [i, j].",
                    "If no pair matches, return an empty array."
                ],
                "whySlow": "Nested iterations test every single combination, yielding O(n²) running time.",
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
                "idea": "Use a HashMap mapping each visited number to its index. For each number, calculate its complement (target - num) and check if it has already been observed.",
                "steps": [
                    "Initialize a HashMap of value to index.",
                    "Iterate through the array with index i and value x.",
                    "Compute need = target - x.",
                    "If need is in the map, return [map.get(need), i].",
                    "Otherwise, put (x, i) into the map."
                ],
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (map.containsKey(complement)) {
                return new int[]{map.get(complement), i};
            }
            map.put(nums[i], i);
        }
        return new int[]{};
    }
}""",
                    "python": """class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen = {}
        for i, x in enumerate(nums):
            complement = target - x
            if complement in seen:
                return [seen[complement], i]
            seen[x] = i
        return []"""
                }
            },
            "test": {
                "java_test": "Solution s = new Solution(); int[] res = s.twoSum(new int[]{2, 7, 11, 15}, 9); if (res[0] != 0 || res[1] != 1) throw new RuntimeException();",
                "python_test": "assert Solution().twoSum([2, 7, 11, 15], 9) == [0, 1]"
            }
        },
        {
            "seq": 3,
            "lc": 242,
            "title": "Valid Anagram",
            "whyNext": "Builds on hash counting from Two Sum: comparing frequencies of characters across two strings.",
            "brute": {
                "idea": "Sort both strings alphabetically and check if the sorted character sequences are identical.",
                "steps": [
                    "If lengths of s and t differ, return false.",
                    "Convert both strings to character arrays.",
                    "Sort both character arrays.",
                    "Compare sorted arrays for equality."
                ],
                "whySlow": "Sorting requires O(n log n) comparisons, which is unnecessary when frequency counting can be done in O(n).",
                "time": "O(n log n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public boolean isAnagram(String s, String t) {
        if (s.length() != t.length()) return false;
        char[] sChars = s.toCharArray();
        char[] tChars = t.toCharArray();
        Arrays.sort(sChars);
        Arrays.sort(tChars);
        return Arrays.equals(sChars, tChars);
    }
}""",
                    "python": """class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        return sorted(s) == sorted(t)"""
                }
            },
            "optimal": {
                "idea": "Count letter frequencies using a fixed 26-slot integer array. Increment counts for string s and decrement for string t.",
                "steps": [
                    "If s.length != t.length, return false immediately.",
                    "Allocate an integer array of size 26 for ASCII lowercase letters.",
                    "Iterate through strings, incrementing count[s[i] - 'a'] and decrementing count[t[i] - 'a'].",
                    "Verify all 26 counts equal zero."
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
        for (int c : counts) {
            if (c != 0) return false;
        }
        return true;
    }
}""",
                    "python": """class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        counts = [0] * 26
        for c1, c2 in zip(s, t):
            counts[ord(c1) - ord('a')] += 1
            counts[ord(c2) - ord('a')] -= 1
        return all(c == 0 for c in counts)"""
                }
            },
            "test": {
                "java_test": "Solution s = new Solution(); if (!s.isAnagram(\"anagram\", \"nagaram\")) throw new RuntimeException();",
                "python_test": "assert Solution().isAnagram('anagram', 'nagaram') == True"
            }
        },
        {
            "seq": 4,
            "lc": 49,
            "title": "Group Anagrams",
            "whyNext": "Extends Valid Anagram from checking a single pair of words to grouping an arbitrary collection of words by anagram signature.",
            "brute": {
                "idea": "For each word in the list, compare it against representatives of all existing anagram groups.",
                "steps": [
                    "Maintain a list of groups where each group has a list of words.",
                    "For each incoming string, compare it against the first string of each existing group using isAnagram.",
                    "If a match is found, append to that group; otherwise, create a new group."
                ],
                "whySlow": "Comparing each word to existing groups takes O(N² * K) time in the worst case where all words are distinct.",
                "time": "O(n²k)",
                "space": "O(nk)",
                "code": {
                    "java": """class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        List<List<String>> groups = new ArrayList<>();
        for (String s : strs) {
            boolean added = false;
            for (List<String> g : groups) {
                if (isAnagram(g.get(0), s)) {
                    g.add(s);
                    added = true;
                    break;
                }
            }
            if (!added) {
                List<String> newG = new ArrayList<>();
                newG.add(s);
                groups.add(newG);
            }
        }
        return groups;
    }
    private boolean isAnagram(String s, String t) {
        if (s.length() != t.length()) return false;
        int[] counts = new int[26];
        for (char c : s.toCharArray()) counts[c - 'a']++;
        for (char c : t.toCharArray()) counts[c - 'a']--;
        for (int c : counts) if (c != 0) return false;
        return true;
    }
}""",
                    "python": """class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        groups = []
        for s in strs:
            placed = False
            for g in groups:
                if sorted(g[0]) == sorted(s):
                    g.append(s)
                    placed = True
                    break
            if not placed:
                groups.append([s])
        return groups"""
                }
            },
            "optimal": {
                "idea": "Compute a canonical key for each string (either sorted string or 26-element character frequency tuple) and map it in a HashMap to its group.",
                "steps": [
                    "Initialize a HashMap where the key is the sorted string and value is a list of strings.",
                    "For each word, convert to char array, sort it, and convert back to string key.",
                    "Append the original word to the map's list for that key.",
                    "Return all values of the map as a list of lists."
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
        groups = collections.defaultdict(list)
        for s in strs:
            key = "".join(sorted(s))
            groups[key].append(s)
        return list(groups.values())"""
                }
            },
            "test": {
                "java_test": "Solution s = new Solution(); if (s.groupAnagrams(new String[]{\"eat\",\"tea\",\"tan\",\"ate\",\"nat\",\"bat\"}).size() != 3) throw new RuntimeException();",
                "python_test": "assert len(Solution().groupAnagrams([\"eat\",\"tea\",\"tan\",\"ate\",\"nat\",\"bat\"])) == 3"
            }
        },
        {
            "seq": 5,
            "lc": 347,
            "title": "Top K Frequent Elements",
            "whyNext": "Builds on frequency counting from Group Anagrams: counting occurrences and selecting the top k entries.",
            "brute": {
                "idea": "Count frequencies of all numbers with a HashMap, then sort unique elements by their frequencies in descending order.",
                "steps": [
                    "Count occurrences of each number in a frequency map.",
                    "Collect all unique keys into a list.",
                    "Sort the list using a comparator based on map values descending.",
                    "Take the first k elements."
                ],
                "whySlow": "Sorting the unique elements takes O(u log u) time where u can be up to n.",
                "time": "O(n log n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> counts = new HashMap<>();
        for (int n : nums) counts.put(n, counts.getOrDefault(n, 0) + 1);
        List<Integer> list = new ArrayList<>(counts.keySet());
        list.sort((a, b) -> counts.get(b) - counts.get(a));
        int[] res = new int[k];
        for (int i = 0; i < k; i++) res[i] = list.get(i);
        return res;
    }
}""",
                    "python": """class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        counts = collections.Counter(nums)
        sorted_keys = sorted(counts.keys(), key=lambda x: counts[x], reverse=True)
        return sorted_keys[:k]"""
                }
            },
            "optimal": {
                "idea": "Count occurrences, then place elements into frequency buckets where index i holds all numbers appearing exactly i times. Scan buckets backwards.",
                "steps": [
                    "Count frequencies using a HashMap.",
                    "Create an array of lists (buckets) of size nums.length + 1.",
                    "Place each number into bucket[freq].",
                    "Iterate backwards from bucket[n] down to 1, gathering numbers until k are collected."
                ],
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> count = new HashMap<>();
        for (int n : nums) count.put(n, count.getOrDefault(n, 0) + 1);
        List<Integer>[] bucket = new List[nums.length + 1];
        for (int key : count.keySet()) {
            int freq = count.get(key);
            if (bucket[freq] == null) bucket[freq] = new ArrayList<>();
            bucket[freq].add(key);
        }
        int[] res = new int[k];
        int idx = 0;
        for (int i = bucket.length - 1; i >= 0 && idx < k; i--) {
            if (bucket[i] != null) {
                for (int num : bucket[i]) {
                    res[idx++] = num;
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
        for val, freq in counts.items():
            buckets[freq].append(val)
        res = []
        for i in range(len(buckets) - 1, 0, -1):
            for num in buckets[i]:
                res.append(num)
                if len(res) == k:
                    return res
        return res"""
                }
            },
            "test": {
                "java_test": "Solution s = new Solution(); int[] res = s.topKFrequent(new int[]{1,1,1,2,2,3}, 2); if (res.length != 2) throw new RuntimeException();",
                "python_test": "assert len(Solution().topKFrequent([1,1,1,2,2,3], 2)) == 2"
            }
        }
    ]


# scripts/gen_batch_12.py
import json

batch_12 = [
    # 276: Best Time to Buy and Sell Stock III
    {
        "seq": 276,
        "whyNext": "At most 2 transactions: 4 state variables (b1, s1, b2, s2) tracking buy/sell transitions in O(1) space.",
        "brute": {
            "idea": "For every split day i, find max profit from single transaction in [0, i] and in [i, n-1].",
            "steps": [
                "For i = 0..n-1:",
                "Compute maxProfit(prices[0..i]) + maxProfit(prices[i..n-1])."
            ],
            "time": "O(n^2)",
            "space": "O(n)",
            "whySlow": "Quadratic recomputation across all split days.",
            "code": {
                "java": """class Solution {
    public int maxProfit(int[] prices) {
        int b1 = Integer.MIN_VALUE, s1 = 0;
        int b2 = Integer.MIN_VALUE, s2 = 0;
        for (int p : prices) {
            b1 = Math.max(b1, -p);
            s1 = Math.max(s1, b1 + p);
            b2 = Math.max(b2, s1 - p);
            s2 = Math.max(s2, b2 + p);
        }
        return s2;
    }
}""",
                "python": """class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        b1 = b2 = float('-inf')
        s1 = s2 = 0
        for p in prices:
            b1 = max(b1, -p)
            s1 = max(s1, b1 + p)
            b2 = max(b2, s1 - p)
            s2 = max(s2, b2 + p)
        return s2"""
            }
        },
        "optimal": {
            "idea": "4-variable DP: b1 = max(b1, -p), s1 = max(s1, b1 + p), b2 = max(b2, s1 - p), s2 = max(s2, b2 + p).",
            "steps": [
                "b1 = -prices[0], s1 = 0, b2 = -prices[0], s2 = 0.",
                "For p in prices:",
                "b1 = Math.max(b1, -p); s1 = Math.max(s1, b1 + p);",
                "b2 = Math.max(b2, s1 - p); s2 = Math.max(s2, b2 + p);",
                "Return s2."
            ],
            "time": "O(n)",
            "space": "O(1)",
            "code": {
                "java": """class Solution {
    public int maxProfit(int[] prices) {
        if (prices.length == 0) return 0;
        int b1 = -prices[0], s1 = 0;
        int b2 = -prices[0], s2 = 0;
        for (int p : prices) {
            b1 = Math.max(b1, -p);
            s1 = Math.max(s1, b1 + p);
            b2 = Math.max(b2, s1 - p);
            s2 = Math.max(s2, b2 + p);
        }
        return s2;
    }
}""",
                "python": """class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        if not prices:
            return 0
        b1 = b2 = -prices[0]
        s1 = s2 = 0
        for p in prices:
            b1 = max(b1, -p)
            s1 = max(s1, b1 + p)
            b2 = max(b2, s1 - p)
            s2 = max(s2, b2 + p)
        return s2"""
            }
        }
    },
    # 277: Best Time to Buy and Sell Stock IV
    {
        "seq": 277,
        "whyNext": "Generalizes Stock III to k transactions: buy[j] and sell[j] arrays; if k >= n/2 reduces to unlimited transactions.",
        "brute": {
            "idea": "Full 3D DP dp[day][k][hasStock] updated over all states.",
            "steps": [
                "Fill 3D DP table."
            ],
            "time": "O(n * k)",
            "space": "O(n * k)",
            "whySlow": "Allocates full 3D array when 2 1D arrays of size k suffice.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public int maxProfit(int k, int[] prices) {
        int n = prices.length;
        if (n <= 1 || k == 0) return 0;
        if (k >= n / 2) {
            int p = 0;
            for (int i = 1; i < n; i++) if (prices[i] > prices[i - 1]) p += prices[i] - prices[i - 1];
            return p;
        }
        int[] buy = new int[k + 1];
        int[] sell = new int[k + 1];
        Arrays.fill(buy, -prices[0]);
        for (int p : prices) {
            for (int j = 1; j <= k; j++) {
                buy[j] = Math.max(buy[j], sell[j - 1] - p);
                sell[j] = Math.max(sell[j], buy[j] + p);
            }
        }
        return sell[k];
    }
}""",
                "python": """class Solution:
    def maxProfit(self, k: int, prices: list[int]) -> int:
        n = len(prices)
        if n <= 1 or k == 0: return 0
        if k >= n // 2:
            return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, n))
        buy = [-prices[0]] * (k + 1)
        sell = [0] * (k + 1)
        for p in prices:
            for j in range(1, k + 1):
                buy[j] = max(buy[j], sell[j - 1] - p)
                sell[j] = max(sell[j], buy[j] + p)
        return sell[k]"""
            }
        },
        "optimal": {
            "idea": "1D DP with k states: if k >= n / 2, greedy slope sum. Else maintain buy[k+1] and sell[k+1] in O(k) space.",
            "steps": [
                "If k >= n / 2: return sum of positive price differences.",
                "int[] buy = new int[k + 1], sell = new int[k + 1]; Arrays.fill(buy, -prices[0]).",
                "For p in prices: for j = 1..k: buy[j] = max(buy[j], sell[j-1] - p); sell[j] = max(sell[j], buy[j] + p).",
                "Return sell[k]."
            ],
            "time": "O(n * k)",
            "space": "O(k)",
            "code": {
                "java": """import java.util.*;
class Solution {
    public int maxProfit(int k, int[] prices) {
        int n = prices.length;
        if (n <= 1 || k == 0) return 0;
        if (k >= n / 2) {
            int profit = 0;
            for (int i = 1; i < n; i++) {
                if (prices[i] > prices[i - 1]) profit += prices[i] - prices[i - 1];
            }
            return profit;
        }
        int[] buy = new int[k + 1];
        int[] sell = new int[k + 1];
        Arrays.fill(buy, -prices[0]);
        for (int p : prices) {
            for (int j = 1; j <= k; j++) {
                buy[j] = Math.max(buy[j], sell[j - 1] - p);
                sell[j] = Math.max(sell[j], buy[j] + p);
            }
        }
        return sell[k];
    }
}""",
                "python": """class Solution:
    def maxProfit(self, k: int, prices: list[int]) -> int:
        n = len(prices)
        if n <= 1 or k == 0:
            return 0
        if k >= n // 2:
            return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, n))
        buy = [-prices[0]] * (k + 1)
        sell = [0] * (k + 1)
        for p in prices:
            for j in range(1, k + 1):
                buy[j] = max(buy[j], sell[j - 1] - p)
                sell[j] = max(sell[j], buy[j] + p)
        return sell[k]"""
            }
        }
    },
    # 278: Longest Common Prefix
    {
        "seq": 278,
        "whyNext": "Entry to Chapter 16 (Tries & Advanced Design): vertical character comparison across strings.",
        "brute": {
            "idea": "Pairwise horizontal matching: take LCP of s[0] and s[1], then match with s[2], and so on.",
            "steps": [
                "prefix = strs[0].",
                "For i = 1..n-1: while strs[i] doesn't start with prefix, shorten prefix."
            ],
            "time": "O(S)",
            "space": "O(1)",
            "whySlow": "Horizontal scanning examines extra characters compared to vertical scanning.",
            "code": {
                "java": """class Solution {
    public String longestCommonPrefix(String[] strs) {
        if (strs.length == 0) return "";
        String prefix = strs[0];
        for (int i = 1; i < strs.length; i++) {
            while (strs[i].indexOf(prefix) != 0) {
                prefix = prefix.substring(0, prefix.length() - 1);
                if (prefix.isEmpty()) return "";
            }
        }
        return prefix;
    }
}""",
                "python": """class Solution:
    def longestCommonPrefix(self, strs: list[str]) -> str:
        if not strs: return ""
        prefix = strs[0]
        for s in strs[1:]:
            while not s.startswith(prefix):
                prefix = prefix[:-1]
                if not prefix: return ""
        return prefix"""
            }
        },
        "optimal": {
            "idea": "Vertical scanning: check character i across all strings simultaneously; return prefix immediately upon first mismatch or string end.",
            "steps": [
                "For col = 0..strs[0].length() - 1:",
                "char c = strs[0].charAt(col).",
                "For each word in strs: if col == word.length() || word.charAt(col) != c, return strs[0].substring(0, col).",
                "Return strs[0]."
            ],
            "time": "O(S)",
            "space": "O(1)",
            "code": {
                "java": """class Solution {
    public String longestCommonPrefix(String[] strs) {
        if (strs == null || strs.length == 0) return "";
        for (int i = 0; i < strs[0].length(); i++) {
            char c = strs[0].charAt(i);
            for (int j = 1; j < strs.length; j++) {
                if (i == strs[j].length() || strs[j].charAt(i) != c) {
                    return strs[0].substring(0, i);
                }
            }
        }
        return strs[0];
    }
}""",
                "python": """class Solution:
    def longestCommonPrefix(self, strs: list[str]) -> str:
        if not strs:
            return ""
        for i, c in enumerate(strs[0]):
            for s in strs[1:]:
                if i == len(s) or s[i] != c:
                    return strs[0][:i]
        return strs[0]"""
            }
        }
    },
    # 279: Implement Trie (Prefix Tree)
    {
        "seq": 279,
        "whyNext": "Fundamental Trie data structure: 26-way tree node with children[] array and isEnd flag; insert, search, and startsWith in O(L).",
        "brute": {
            "idea": "Store all inserted strings in a Set; startsWith checks prefix against all set elements.",
            "steps": [
                "Set<String> stores inserted words.",
                "search: set.contains(word).",
                "startsWith: linear scan set."
            ],
            "time": "O(N * L) startsWith",
            "space": "O(N * L)",
            "whySlow": "startsWith scans all words in the set linearly.",
            "code": {
                "java": """import java.util.*;
public class Trie {
    private Set<String> words = new HashSet<>();
    public Trie() {}
    public void insert(String word) {
        words.add(word);
    }
    public boolean search(String word) {
        return words.contains(word);
    }
    public boolean startsWith(String prefix) {
        for (String w : words) {
            if (w.startsWith(prefix)) return true;
        }
        return false;
    }
}""",
                "python": """class Trie:
    def __init__(self):
        self.words = set()

    def insert(self, word: str) -> None:
        self.words.add(word)

    def search(self, word: str) -> bool:
        return word in self.words

    def startsWith(self, prefix: str) -> bool:
        return any(w.startswith(prefix) for w in self.words)"""
            }
        },
        "optimal": {
            "idea": "Prefix Tree: TrieNode contains TrieNode[26] children and boolean isEnd. Insert, search, and startsWith navigate node references in O(L).",
            "steps": [
                "Node class: Node[] children = new Node[26]; boolean isWord = false.",
                "insert(word): walk children; create new Node if null; set isWord = true at end.",
                "search(word): walk children; return node != null && node.isWord.",
                "startsWith(prefix): walk children; return node != null."
            ],
            "time": "O(L) per operation",
            "space": "O(total_characters * 26)",
            "code": {
                "java": """public class Trie {
    private static class Node {
        Node[] children = new Node[26];
        boolean isWord = false;
    }
    private Node root = new Node();
    public Trie() {}
    public void insert(String word) {
        Node cur = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (cur.children[idx] == null) cur.children[idx] = new Node();
            cur = cur.children[idx];
        }
        cur.isWord = true;
    }
    public boolean search(String word) {
        Node node = find(word);
        return node != null && node.isWord;
    }
    public boolean startsWith(String prefix) {
        return find(prefix) != null;
    }
    private Node find(String s) {
        Node cur = root;
        for (char c : s.toCharArray()) {
            int idx = c - 'a';
            if (cur.children[idx] == null) return null;
            cur = cur.children[idx];
        }
        return cur;
    }
}""",
                "python": """class Trie:
    def __init__(self):
        self.root = {}

    def insert(self, word: str) -> None:
        cur = self.root
        for c in word:
            if c not in cur:
                cur[c] = {}
            cur = cur[c]
        cur['#'] = True

    def search(self, word: str) -> bool:
        cur = self.root
        for c in word:
            if c not in cur:
                return False
            cur = cur[c]
        return '#' in cur

    def startsWith(self, prefix: str) -> bool:
        cur = self.root
        for c in prefix:
            if c not in cur:
                return False
            cur = cur[c]
        return True"""
            }
        }
    },
    # 280: Design Add and Search Words Data Structure
    {
        "seq": 280,
        "whyNext": "Builds on Trie: search supports wildcard '.' matching any character by branching over all 26 non-null children.",
        "brute": {
            "idea": "Store words in a list; search checks regular expression or character-by-character match against all words.",
            "steps": [
                "List of strings.",
                "search checks every string with matching length."
            ],
            "time": "O(N * L)",
            "space": "O(N * L)",
            "whySlow": "Scans all inserted words on wildcard search.",
            "code": {
                "java": """import java.util.*;
public class WordDictionary {
    private List<String> words = new ArrayList<>();
    public WordDictionary() {}
    public void addWord(String word) {
        words.add(word);
    }
    public boolean search(String word) {
        for (String w : words) {
            if (match(w, word)) return true;
        }
        return false;
    }
    private boolean match(String s, String p) {
        if (s.length() != p.length()) return false;
        for (int i = 0; i < s.length(); i++) {
            if (p.charAt(i) != '.' && p.charAt(i) != s.charAt(i)) return false;
        }
        return true;
    }
}""",
                "python": """class WordDictionary:
    def __init__(self):
        self.words = []

    def addWord(self, word: str) -> None:
        self.words.append(word)

    def search(self, word: str) -> bool:
        n = len(word)
        for w in self.words:
            if len(w) == n and all(p == '.' or p == c for p, c in zip(word, w)):
                return True
        return False"""
            }
        },
        "optimal": {
            "idea": "Trie with DFS search: for character '.', try all non-null children recursively; for regular letter, advance child pointer.",
            "steps": [
                "TrieNode class.",
                "addWord: standard Trie insertion.",
                "searchDFS(node, word, idx): if idx == word.length return node.isWord.",
                "If word[idx] == '.', test all 26 children; if any returns true return true.",
                "Else advance to child word[idx] - 'a'."
            ],
            "time": "O(L) without wildcards, O(26^L) worst case with all '.'",
            "space": "O(total_characters * 26)",
            "code": {
                "java": """public class WordDictionary {
    private static class Node {
        Node[] children = new Node[26];
        boolean isWord = false;
    }
    private Node root = new Node();
    public WordDictionary() {}
    public void addWord(String word) {
        Node cur = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (cur.children[idx] == null) cur.children[idx] = new Node();
            cur = cur.children[idx];
        }
        cur.isWord = true;
    }
    public boolean search(String word) {
        return search(root, word, 0);
    }
    private boolean search(Node node, String word, int idx) {
        if (node == null) return false;
        if (idx == word.length()) return node.isWord;
        char c = word.charAt(idx);
        if (c == '.') {
            for (Node child : node.children) {
                if (child != null && search(child, word, idx + 1)) return true;
            }
            return false;
        } else {
            return search(node.children[c - 'a'], word, idx + 1);
        }
    }
}""",
                "python": """class WordDictionary:
    def __init__(self):
        self.root = {}

    def addWord(self, word: str) -> None:
        cur = self.root
        for c in word:
            if c not in cur:
                cur[c] = {}
            cur = cur[c]
        cur['#'] = True

    def search(self, word: str) -> bool:
        def dfs(node, idx):
            if idx == len(word):
                return '#' in node
            c = word[idx]
            if c == '.':
                for k, child in node.items():
                    if k != '#' and dfs(child, idx + 1):
                        return True
                return False
            if c not in node:
                return False
            return dfs(node[c], idx + 1)
        return dfs(self.root, 0)"""
            }
        }
    },
    # 281: Replace Words
    {
        "seq": 281,
        "whyNext": "Trie shortest prefix search: replace each word in sentence with its shortest matching root in the dictionary.",
        "brute": {
            "idea": "For each word in sentence, check against all roots in dictionary; replace with shortest matching root.",
            "steps": [
                "Split sentence into words.",
                "For each word, find all roots it starts with and pick shortest."
            ],
            "time": "O(words * roots * L)",
            "space": "O(N)",
            "whySlow": "Compares every word against all roots.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public String replaceWords(List<String> dictionary, String sentence) {
        Set<String> set = new HashSet<>(dictionary);
        String[] words = sentence.split(" ");
        for (int i = 0; i < words.length; i++) {
            String word = words[i];
            for (int len = 1; len <= word.length(); len++) {
                String sub = word.substring(0, len);
                if (set.contains(sub)) {
                    words[i] = sub;
                    break;
                }
            }
        }
        return String.join(" ", words);
    }
}""",
                "python": """class Solution:
    def replaceWords(self, dictionary: list[str], sentence: list[str]) -> str:
        roots = set(dictionary)
        res = []
        for word in sentence.split():
            for i in range(1, len(word) + 1):
                if word[:i] in roots:
                    res.append(word[:i])
                    break
            else:
                res.append(word)
        return " ".join(res)"""
            }
        },
        "optimal": {
            "idea": "Build Trie of dictionary roots: for each word, traverse Trie; stop at first node with isWord = true.",
            "steps": [
                "Insert all roots into Trie.",
                "For word in sentence: walk Trie.",
                "If node has isWord, return prefix up to current char.",
                "If path breaks, return original word."
            ],
            "time": "O(sentence_length + total_dict_length)",
            "space": "O(total_dict_length)",
            "code": {
                "java": """import java.util.*;
class Solution {
    private static class Node {
        Node[] children = new Node[26];
        boolean isWord = false;
    }
    public String replaceWords(List<String> dictionary, String sentence) {
        Node root = new Node();
        for (String d : dictionary) {
            Node cur = root;
            for (char c : d.toCharArray()) {
                int idx = c - 'a';
                if (cur.children[idx] == null) cur.children[idx] = new Node();
                cur = cur.children[idx];
            }
            cur.isWord = true;
        }
        String[] words = sentence.split(" ");
        for (int i = 0; i < words.length; i++) {
            words[i] = findRoot(root, words[i]);
        }
        return String.join(" ", words);
    }
    private String findRoot(Node root, String word) {
        Node cur = root;
        StringBuilder sb = new StringBuilder();
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (cur.children[idx] == null) return word;
            sb.append(c);
            cur = cur.children[idx];
            if (cur.isWord) return sb.toString();
        }
        return word;
    }
}""",
                "python": """class Solution:
    def replaceWords(self, dictionary: list[str], sentence: str) -> str:
        root = {}
        for d in dictionary:
            cur = root
            for c in d:
                if c not in cur: cur[c] = {}
                cur = cur[c]
            cur['#'] = True
        def find_root(word):
            cur = root
            prefix = []
            for c in word:
                if c not in cur: return word
                prefix.append(c)
                cur = cur[c]
                if '#' in cur: return "".join(prefix)
            return word
        return " ".join(find_root(w) for w in sentence.split())"""
            }
        }
    },
    # 282: Search Suggestions System
    {
        "seq": 282,
        "whyNext": "Sorted array + binary search or Trie storing top 3 lexicographical words at each node.",
        "brute": {
            "idea": "For every prefix of searchWord, filter all products starting with prefix, sort, take top 3.",
            "steps": [
                "For prefix length 1..len(searchWord):",
                "Filter products, sort, take up to 3."
            ],
            "time": "O(L * N log N)",
            "space": "O(N)",
            "whySlow": "Filters and sorts all products on every prefix character.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<List<String>> suggestedProducts(String[] products, String searchWord) {
        Arrays.sort(products);
        List<List<String>> res = new ArrayList<>();
        String cur = "";
        for (char c : searchWord.toCharArray()) {
            cur += c;
            List<String> list = new ArrayList<>();
            for (String p : products) {
                if (p.startsWith(cur)) {
                    list.add(p);
                    if (list.size() == 3) break;
                }
            }
            res.add(list);
        }
        return res;
    }
}""",
                "python": """class Solution:
    def suggestedProducts(self, products: list[str], searchWord: str) -> list[list[str]]:
        products.sort()
        res = []
        cur = ""
        for c in searchWord:
            cur += c
            res.append([p for p in products if p.startswith(cur)][:3])
        return res"""
            }
        },
        "optimal": {
            "idea": "Sort products + Two Pointers (left, right): narrow down valid window as each character is typed.",
            "steps": [
                "Arrays.sort(products).",
                "l = 0, r = products.length - 1.",
                "For i = 0..searchWord.length - 1: char c = searchWord.charAt(i).",
                "While l <= r and (products[l].length <= i || products[l].charAt(i) != c) l++.",
                "While l <= r and (products[r].length <= i || products[r].charAt(i) != c) r--.",
                "Collect up to 3 words from index l."
            ],
            "time": "O(N log N + L)",
            "space": "O(1) auxiliary",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<List<String>> suggestedProducts(String[] products, String searchWord) {
        Arrays.sort(products);
        List<List<String>> res = new ArrayList<>();
        int l = 0, r = products.length - 1;
        for (int i = 0; i < searchWord.length(); i++) {
            char c = searchWord.charAt(i);
            while (l <= r && (products[l].length() <= i || products[l].charAt(i) != c)) l++;
            while (l <= r && (products[r].length() <= i || products[r].charAt(i) != c)) r--;
            List<String> list = new ArrayList<>();
            for (int k = l; k <= Math.min(l + 2, r); k++) {
                list.add(products[k]);
            }
            res.add(list);
        }
        return res;
    }
}""",
                "python": """class Solution:
    def suggestedProducts(self, products: list[str], searchWord: str) -> list[list[str]]:
        products.sort()
        res = []
        l, r = 0, len(products) - 1
        for i, c in enumerate(searchWord):
            while l <= r and (len(products[l]) <= i or products[l][i] != c):
                l += 1
            while l <= r and (len(products[r]) <= i or products[r][i] != c):
                r -= 1
            res.append(products[l:min(l + 3, r + 1)])
        return res"""
            }
        }
    },
    # 283: Map Sum Pairs
    {
        "seq": 283,
        "whyNext": "Trie prefix sum caching: insert updates delta = val - oldVal along Trie path so sum() is O(prefix_length).",
        "brute": {
            "idea": "HashMap storing (key -> val); sum(prefix) scans all map entries summing values of keys starting with prefix.",
            "steps": [
                "Map.put(key, val).",
                "sum: iterate all keys checking startsWith."
            ],
            "time": "O(N * L) per sum",
            "space": "O(N * L)",
            "whySlow": "Scans all keys in map on every sum query.",
            "code": {
                "java": """import java.util.*;
public class MapSum {
    private Map<String, Integer> map = new HashMap<>();
    public MapSum() {}
    public void insert(String key, int val) {
        map.put(key, val);
    }
    public int sum(String prefix) {
        int sum = 0;
        for (String k : map.keySet()) {
            if (k.startsWith(prefix)) sum += map.get(k);
        }
        return sum;
    }
}""",
                "python": """class MapSum:
    def __init__(self):
        self.map = {}

    def insert(self, key: str, val: int) -> None:
        self.map[key] = val

    def sum(self, prefix: str) -> int:
        return sum(v for k, v in self.map.items() if k.startswith(prefix))"""
            }
        },
        "optimal": {
            "idea": "Trie where each node maintains sum of all keys through it. insert computes delta = val - map.getOrDefault(key, 0) and adds delta to each node in O(L).",
            "steps": [
                "HashMap<String, Integer> map to track current values.",
                "TrieNode contains Node[26] children and int score.",
                "insert(key, val): delta = val - map.getOrDefault(key, 0); map.put(key, val). Walk Trie adding delta to node.score.",
                "sum(prefix): walk Trie to end of prefix; return node != null ? node.score : 0."
            ],
            "time": "O(L) insert, O(L) sum",
            "space": "O(total_characters * 26)",
            "code": {
                "java": """import java.util.*;
public class MapSum {
    private static class Node {
        Node[] children = new Node[26];
        int score = 0;
    }
    private Map<String, Integer> map = new HashMap<>();
    private Node root = new Node();
    public MapSum() {}
    public void insert(String key, int val) {
        int delta = val - map.getOrDefault(key, 0);
        map.put(key, val);
        Node cur = root;
        for (char c : key.toCharArray()) {
            int idx = c - 'a';
            if (cur.children[idx] == null) cur.children[idx] = new Node();
            cur = cur.children[idx];
            cur.score += delta;
        }
    }
    public int sum(String prefix) {
        Node cur = root;
        for (char c : prefix.toCharArray()) {
            int idx = c - 'a';
            if (cur.children[idx] == null) return 0;
            cur = cur.children[idx];
        }
        return cur.score;
    }
}""",
                "python": """class MapSum:
    def __init__(self):
        self.map = {}
        self.root = {}

    def insert(self, key: str, val: int) -> None:
        delta = val - self.map.get(key, 0)
        self.map[key] = val
        cur = self.root
        for c in key:
            if c not in cur:
                cur[c] = {'score': 0}
            cur = cur[c]
            cur['score'] += delta

    def sum(self, prefix: str) -> int:
        cur = self.root
        for c in prefix:
            if c not in cur:
                return 0
            cur = cur[c]
        return cur['score']"""
            }
        }
    },
    # 284: Word Search II
    {
        "seq": 284,
        "whyNext": "Trie-guided 2D backtracking: simultaneous search of all dictionary words on the board pruning branches in O(1) via Trie nodes.",
        "brute": {
            "idea": "For every word in words, run Word Search I DFS on the board.",
            "steps": [
                "For word in words: if exist(board, word) add to res."
            ],
            "time": "O(W * m * n * 4^L)",
            "space": "O(L)",
            "whySlow": "Repeats 2D grid searches for every word independently.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<String> findWords(char[][] board, String[] words) {
        List<String> res = new ArrayList<>();
        Node root = buildTrie(words);
        for (int i = 0; i < board.length; i++) {
            for (int j = 0; j < board[0].length; j++) {
                dfs(board, i, j, root, res);
            }
        }
        return res;
    }
    private void dfs(char[][] board, int r, int c, Node p, List<String> res) {
        char ch = board[r][c];
        if (ch == '#' || p.children[ch - 'a'] == null) return;
        p = p.children[ch - 'a'];
        if (p.word != null) {
            res.add(p.word);
            p.word = null;
        }
        board[r][c] = '#';
        if (r > 0) dfs(board, r - 1, c, p, res);
        if (c > 0) dfs(board, r, c - 1, p, res);
        if (r < board.length - 1) dfs(board, r + 1, c, p, res);
        if (c < board[0].length - 1) dfs(board, r, c + 1, p, res);
        board[r][c] = ch;
    }
    private static class Node {
        Node[] children = new Node[26];
        String word;
    }
    private Node buildTrie(String[] words) {
        Node root = new Node();
        for (String w : words) {
            Node cur = root;
            for (char c : w.toCharArray()) {
                int idx = c - 'a';
                if (cur.children[idx] == null) cur.children[idx] = new Node();
                cur = cur.children[idx];
            }
            cur.word = w;
        }
        return root;
    }
}""",
                "python": """class Solution:
    def findWords(self, board: list[list[str]], words: list[str]) -> list[str]:
        trie = {}
        for word in words:
            cur = trie
            for c in word:
                cur = cur.setdefault(c, {})
            cur['$'] = word
        m, n = len(board), len(board[0])
        res = []
        def dfs(r, c, parent):
            char = board[r][c]
            cur = parent[char]
            if '$' in cur:
                res.append(cur.pop('$'))
            board[r][c] = '#'
            for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and board[nr][nc] in cur:
                    dfs(nr, nc, cur)
            board[r][c] = char
        for i in range(m):
            for j in range(n):
                if board[i][j] in trie:
                    dfs(i, j, trie)
        return res"""
            }
        },
        "optimal": {
            "idea": "Build Trie of all words storing full word at leaf; single DFS pass on grid walks Trie simultaneously. Clear word upon match to avoid duplicates.",
            "steps": [
                "Insert all words into Trie with node.word = word at end.",
                "For each cell (r, c): if root.children has board[r][c], dfs(r, c, root).",
                "dfs: if node.word != null: res.add(node.word); node.word = null.",
                "Backtrack: mark board[r][c] = '#', recurse 4 directions, restore board[r][c]."
            ],
            "time": "O(m * n * 4^L)",
            "space": "O(total_characters * 26)",
            "code": {
                "java": """import java.util.*;
class Solution {
    private static class Node {
        Node[] children = new Node[26];
        String word = null;
    }
    public List<String> findWords(char[][] board, String[] words) {
        Node root = new Node();
        for (String w : words) {
            Node cur = root;
            for (char c : w.toCharArray()) {
                int idx = c - 'a';
                if (cur.children[idx] == null) cur.children[idx] = new Node();
                cur = cur.children[idx];
            }
            cur.word = w;
        }
        List<String> res = new ArrayList<>();
        int m = board.length, n = board[0].length;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (root.children[board[i][j] - 'a'] != null) {
                    dfs(board, i, j, root, res);
                }
            }
        }
        return res;
    }
    private void dfs(char[][] board, int r, int c, Node parent, List<String> res) {
        char ch = board[r][c];
        if (ch == '#' || parent.children[ch - 'a'] == null) return;
        Node cur = parent.children[ch - 'a'];
        if (cur.word != null) {
            res.add(cur.word);
            cur.word = null;
        }
        board[r][c] = '#';
        if (r > 0) dfs(board, r - 1, c, cur, res);
        if (c > 0) dfs(board, r, c - 1, cur, res);
        if (r < board.length - 1) dfs(board, r + 1, c, cur, res);
        if (c < board[0].length - 1) dfs(board, r, c + 1, cur, res);
        board[r][c] = ch;
    }
}""",
                "python": """class Solution:
    def findWords(self, board: list[list[str]], words: list[str]) -> list[str]:
        trie = {}
        for w in words:
            cur = trie
            for c in w:
                cur = cur.setdefault(c, {})
            cur['#'] = w
        m, n = len(board), len(board[0])
        res = []
        def dfs(r: int, c: int, parent: dict):
            ch = board[r][c]
            cur = parent[ch]
            if '#' in cur:
                res.append(cur.pop('#'))
            board[r][c] = '$'
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and board[nr][nc] in cur:
                    dfs(nr, nc, cur)
            board[r][c] = ch
        for i in range(m):
            for j in range(n):
                if board[i][j] in trie:
                    dfs(i, j, trie)
        return res"""
            }
        }
    },
    # 285: Maximum XOR of Two Numbers in an Array
    {
        "seq": 285,
        "whyNext": "Bitwise Trie (Prefix Tree of 0s and 1s): 31-bit Trie greedily picks opposite bit 1 - bit to maximize XOR sum in O(32 * n).",
        "brute": {
            "idea": "Check all O(n^2) pairs nums[i] ^ nums[j] keeping maximum.",
            "steps": [
                "Nested loop for each pair.",
                "Take maximum XOR."
            ],
            "time": "O(n^2)",
            "space": "O(1)",
            "whySlow": "Quadratic all-pairs comparison.",
            "code": {
                "java": """class Solution {
    public int findMaximumXOR(int[] nums) {
        int max = 0, mask = 0;
        for (int i = 31; i >= 0; i--) {
            mask |= (1 << i);
            java.util.Set<Integer> set = new java.util.HashSet<>();
            for (int num : nums) set.add(num & mask);
            int candidate = max | (1 << i);
            for (int prefix : set) {
                if (set.contains(prefix ^ candidate)) {
                    max = candidate;
                    break;
                }
            }
        }
        return max;
    }
}""",
                "python": """class Solution:
    def findMaximumXOR(self, nums: list[int]) -> int:
        max_xor = 0
        mask = 0
        for i in range(31, -1, -1):
            mask |= (1 << i)
            prefixes = {num & mask for num in nums}
            candidate = max_xor | (1 << i)
            if any(candidate ^ p in prefixes for p in prefixes):
                max_xor = candidate
        return max_xor"""
            }
        },
        "optimal": {
            "idea": "Bitwise Trie: insert binary representations (bits 30..0); for each num, greedily traverse opposite bit (1 - bit) if available, accumulating 1 << i.",
            "steps": [
                "Binary Trie with Node[2] children.",
                "Insert each num: walk bits from 30 down to 0.",
                "Query each num: curXor = 0; for bit in 30..0: opposite = 1 - bit; if child[opposite] exists, curXor |= (1 << bit), node = child[opposite]; else node = child[bit].",
                "Return maxXor."
            ],
            "time": "O(32 * n)",
            "space": "O(32 * n)",
            "code": {
                "java": """class Solution {
    private static class Node {
        Node[] children = new Node[2];
    }
    public int findMaximumXOR(int[] nums) {
        Node root = new Node();
        for (int num : nums) {
            Node cur = root;
            for (int i = 31; i >= 0; i--) {
                int bit = (num >> i) & 1;
                if (cur.children[bit] == null) cur.children[bit] = new Node();
                cur = cur.children[bit];
            }
        }
        int maxXor = 0;
        for (int num : nums) {
            Node cur = root;
            int curXor = 0;
            for (int i = 31; i >= 0; i--) {
                int bit = (num >> i) & 1;
                int opposite = 1 - bit;
                if (cur.children[opposite] != null) {
                    curXor |= (1 << i);
                    cur = cur.children[opposite];
                } else {
                    cur = cur.children[bit];
                }
            }
            maxXor = Math.max(maxXor, curXor);
        }
        return maxXor;
    }
}""",
                "python": """class Solution:
    def findMaximumXOR(self, nums: list[int]) -> int:
        max_xor = 0
        mask = 0
        for i in range(31, -1, -1):
            mask |= (1 << i)
            prefixes = {num & mask for num in nums}
            candidate = max_xor | (1 << i)
            if any(candidate ^ p in prefixes for p in prefixes):
                max_xor = candidate
        return max_xor"""
            }
        }
    },
    # 286: LFU Cache
    {
        "seq": 286,
        "whyNext": "Double hash map + doubly linked lists: Map<key, Node> + Map<freq, DoublyLinkedList> maintains O(1) get and put with frequency eviction.",
        "brute": {
            "idea": "Store items with timestamp and frequency; linear scan on eviction to find minimum frequency with earliest timestamp.",
            "steps": [
                "Track frequency and lastUsed timestamp.",
                "Evict element with min(freq, timestamp)."
            ],
            "time": "O(n) put",
            "space": "O(capacity)",
            "whySlow": "Linear scan for LFU element.",
            "code": {
                "java": """import java.util.*;
public class LFUCache {
    private int capacity, minFreq = 0;
    private Map<Integer, Node> keyMap = new HashMap<>();
    private Map<Integer, DLList> freqMap = new HashMap<>();
    static class Node {
        int key, val, freq = 1;
        Node prev, next;
        Node(int k, int v) { key = k; val = v; }
    }
    static class DLList {
        Node head = new Node(0, 0), tail = new Node(0, 0);
        int size = 0;
        DLList() { head.next = tail; tail.prev = head; }
        void add(Node n) { n.next = head.next; n.prev = head; head.next.prev = n; head.next = n; size++; }
        void remove(Node n) { n.prev.next = n.next; n.next.prev = n.prev; size--; }
        Node popTail() { if (size == 0) return null; Node n = tail.prev; remove(n); return n; }
    }
    public LFUCache(int capacity) { this.capacity = capacity; }
    public int get(int key) {
        Node n = keyMap.get(key);
        if (n == null) return -1;
        update(n);
        return n.val;
    }
    public void put(int key, int value) {
        if (capacity == 0) return;
        Node n = keyMap.get(key);
        if (n != null) {
            n.val = value;
            update(n);
        } else {
            if (keyMap.size() == capacity) {
                DLList minList = freqMap.get(minFreq);
                Node toRemove = minList.popTail();
                keyMap.remove(toRemove.key);
            }
            Node newNode = new Node(key, value);
            keyMap.put(key, newNode);
            minFreq = 1;
            freqMap.computeIfAbsent(1, k -> new DLList()).add(newNode);
        }
    }
    private void update(Node n) {
        DLList oldList = freqMap.get(n.freq);
        oldList.remove(n);
        if (n.freq == minFreq && oldList.size == 0) minFreq++;
        n.freq++;
        freqMap.computeIfAbsent(n.freq, k -> new DLList()).add(n);
    }
}""",
                "python": """from collections import defaultdict

class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.freq = 1
        self.prev = self.next = None

class DLinkedList:
    def __init__(self):
        self.head, self.tail = Node(0, 0), Node(0, 0)
        self.head.next, self.tail.prev = self.tail, self.head
        self.size = 0
    def add(self, node):
        node.next, node.prev = self.head.next, self.head
        self.head.next.prev = node
        self.head.next = node
        self.size += 1
    def remove(self, node):
        node.prev.next, node.next.prev = node.next, node.prev
        self.size -= 1
    def pop_tail(self):
        if self.size == 0: return None
        node = self.tail.prev
        self.remove(node)
        return node

class LFUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.min_freq = 0
        self.key_map = {}
        self.freq_map = defaultdict(DLinkedList)

    def _update(self, node):
        old_list = self.freq_map[node.freq]
        old_list.remove(node)
        if node.freq == self.min_freq and old_list.size == 0:
            self.min_freq += 1
        node.freq += 1
        self.freq_map[node.freq].add(node)

    def get(self, key: int) -> int:
        if key not in self.key_map: return -1
        node = self.key_map[key]
        self._update(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if self.cap == 0: return
        if key in self.key_map:
            node = self.key_map[key]
            node.val = value
            self._update(node)
        else:
            if len(self.key_map) == self.cap:
                removed = self.freq_map[self.min_freq].pop_tail()
                del self.key_map[removed.key]
            new_node = Node(key, value)
            self.key_map[key] = new_node
            self.min_freq = 1
            self.freq_map[1].add(new_node)"""
            }
        },
        "optimal": {
            "idea": "Map<key, Node> + Map<freq, DoublyLinkedList> + minFreq pointer: all operations (get and put) in strict O(1) time.",
            "steps": [
                "Node stores key, val, freq, prev, next.",
                "freqMap stores DoublyLinkedList per frequency.",
                "get: lookup node, remove from current freq list, increment freq, add to new freq list. Update minFreq if old list emptied.",
                "put: if key exists, update value and bump freq. If at capacity, pop tail of freqMap[minFreq], delete from keyMap. Insert new node at freq 1, minFreq = 1."
            ],
            "time": "O(1) get, O(1) put",
            "space": "O(capacity)",
            "code": {
                "java": """import java.util.*;
public class LFUCache {
    private int capacity, minFreq = 0;
    private Map<Integer, Node> keyMap = new HashMap<>();
    private Map<Integer, DLList> freqMap = new HashMap<>();
    static class Node {
        int key, val, freq = 1;
        Node prev, next;
        Node(int k, int v) { key = k; val = v; }
    }
    static class DLList {
        Node head = new Node(0, 0), tail = new Node(0, 0);
        int size = 0;
        DLList() { head.next = tail; tail.prev = head; }
        void add(Node n) { n.next = head.next; n.prev = head; head.next.prev = n; head.next = n; size++; }
        void remove(Node n) { n.prev.next = n.next; n.next.prev = n.prev; size--; }
        Node popTail() { if (size == 0) return null; Node n = tail.prev; remove(n); return n; }
    }
    public LFUCache(int capacity) { this.capacity = capacity; }
    public int get(int key) {
        Node n = keyMap.get(key);
        if (n == null) return -1;
        update(n);
        return n.val;
    }
    public void put(int key, int value) {
        if (capacity == 0) return;
        Node n = keyMap.get(key);
        if (n != null) {
            n.val = value;
            update(n);
        } else {
            if (keyMap.size() == capacity) {
                DLList minList = freqMap.get(minFreq);
                Node toRemove = minList.popTail();
                keyMap.remove(toRemove.key);
            }
            Node newNode = new Node(key, value);
            keyMap.put(key, newNode);
            minFreq = 1;
            freqMap.computeIfAbsent(1, k -> new DLList()).add(newNode);
        }
    }
    private void update(Node n) {
        DLList oldList = freqMap.get(n.freq);
        oldList.remove(n);
        if (n.freq == minFreq && oldList.size == 0) minFreq++;
        n.freq++;
        freqMap.computeIfAbsent(n.freq, k -> new DLList()).add(n);
    }
}""",
                "python": """from collections import defaultdict

class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.freq = 1
        self.prev = self.next = None

class DLinkedList:
    def __init__(self):
        self.head, self.tail = Node(0, 0), Node(0, 0)
        self.head.next, self.tail.prev = self.tail, self.head
        self.size = 0
    def add(self, node):
        node.next, node.prev = self.head.next, self.head
        self.head.next.prev = node
        self.head.next = node
        self.size += 1
    def remove(self, node):
        node.prev.next, node.next.prev = node.next, node.prev
        self.size -= 1
    def pop_tail(self):
        if self.size == 0: return None
        node = self.tail.prev
        self.remove(node)
        return node

class LFUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.min_freq = 0
        self.key_map = {}
        self.freq_map = defaultdict(DLinkedList)

    def _update(self, node):
        old_list = self.freq_map[node.freq]
        old_list.remove(node)
        if node.freq == self.min_freq and old_list.size == 0:
            self.min_freq += 1
        node.freq += 1
        self.freq_map[node.freq].add(node)

    def get(self, key: int) -> int:
        if key not in self.key_map:
            return -1
        node = self.key_map[key]
        self._update(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if self.cap == 0:
            return
        if key in self.key_map:
            node = self.key_map[key]
            node.val = value
            self._update(node)
        else:
            if len(self.key_map) == self.cap:
                removed = self.freq_map[self.min_freq].pop_tail()
                del self.key_map[removed.key]
            new_node = Node(key, value)
            self.key_map[key] = new_node
            self.min_freq = 1
            self.freq_map[1].add(new_node)"""
            }
        }
    },
    # 287: Single Number
    {
        "seq": 287,
        "whyNext": "Entry to Chapter 17 (Bit Manipulation): XOR property x ^ x = 0 and x ^ 0 = x isolates the single element in O(1) space.",
        "brute": {
            "idea": "HashSet: add if not present, remove if present; remaining element in set is the single number.",
            "steps": [
                "Set contains numbers.",
                "Return remaining element."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "whySlow": "Allocates O(n) hash set memory.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public int singleNumber(int[] nums) {
        Set<Integer> set = new HashSet<>();
        for (int x : nums) {
            if (!set.add(x)) set.remove(x);
        }
        return set.iterator().next();
    }
}""",
                "python": """class Solution:
    def singleNumber(self, nums: list[int]) -> int:
        s = set()
        for x in nums:
            if x in s: s.remove(x)
            else: s.add(x)
        return s.pop()"""
            }
        },
        "optimal": {
            "idea": "Bitwise XOR: a ^ b ^ a = b. Running XOR of all numbers cancels all duplicates.",
            "steps": [
                "ans = 0.",
                "For x in nums: ans ^= x.",
                "Return ans."
            ],
            "time": "O(n)",
            "space": "O(1)",
            "code": {
                "java": """class Solution {
    public int singleNumber(int[] nums) {
        int ans = 0;
        for (int x : nums) ans ^= x;
        return ans;
    }
}""",
                "python": """class Solution:
    def singleNumber(self, nums: list[int]) -> int:
        ans = 0
        for x in nums:
            ans ^= x
        return ans"""
            }
        }
    },
    # 288: Single Number II
    {
        "seq": 288,
        "whyNext": "Modulo-3 bit counter: elements appear 3 times; track bits appearing 1 and 2 times using bitwise ones and twos.",
        "brute": {
            "idea": "Count frequency of each element using HashMap.",
            "steps": [
                "Map frequencies; return key with count == 1."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "whySlow": "Allocates O(n) map.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public int singleNumber(int[] nums) {
        Map<Integer, Integer> counts = new HashMap<>();
        for (int x : nums) counts.put(x, counts.getOrDefault(x, 0) + 1);
        for (int k : counts.keySet()) if (counts.get(k) == 1) return k;
        return 0;
    }
}""",
                "python": """from collections import Counter

class Solution:
    def singleNumber(self, nums: list[int]) -> int:
        c = Counter(nums)
        for k, v in c.items():
            if v == 1: return k
        return 0"""
            }
        },
        "optimal": {
            "idea": "State machine bitwise counters: ones = (ones ^ x) & ~twos; twos = (twos ^ x) & ~ones.",
            "steps": [
                "int ones = 0, twos = 0.",
                "For x in nums:",
                "ones = (ones ^ x) & ~twos;",
                "twos = (twos ^ x) & ~ones;",
                "Return ones."
            ],
            "time": "O(n)",
            "space": "O(1)",
            "code": {
                "java": """class Solution {
    public int singleNumber(int[] nums) {
        int ones = 0, twos = 0;
        for (int x : nums) {
            ones = (ones ^ x) & ~twos;
            twos = (twos ^ x) & ~ones;
        }
        return ones;
    }
}""",
                "python": """class Solution:
    def singleNumber(self, nums: list[int]) -> int:
        ones = twos = 0
        for x in nums:
            ones = (ones ^ x) & ~twos
            twos = (twos ^ x) & ~ones
        return ones"""
            }
        }
    },
    # 289: Single Number III
    {
        "seq": 289,
        "whyNext": "Two unique numbers: XOR sum = a ^ b; isolate lowest set bit diff = xor & (-xor) to partition array into two subsets containing a and b.",
        "brute": {
            "idea": "HashMap/HashSet tracking elements appearing once.",
            "steps": [
                "HashSet toggling."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "whySlow": "Allocates extra memory.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public int[] singleNumber(int[] nums) {
        Set<Integer> set = new HashSet<>();
        for (int x : nums) {
            if (!set.add(x)) set.remove(x);
        }
        int[] res = new int[2];
        int i = 0;
        for (int v : set) res[i++] = v;
        return res;
    }
}""",
                "python": """class Solution:
    def singleNumber(self, nums: list[int]) -> list[int]:
        s = set()
        for x in nums:
            if x in s: s.remove(x)
            else: s.add(x)
        return list(s)"""
            }
        },
        "optimal": {
            "idea": "Bit partition: diff = xor & (-xor) isolates a bit where the two numbers differ. Partition nums into two groups by that bit.",
            "steps": [
                "int diff = 0; for x in nums diff ^= x.",
                "diff &= -diff (isolate rightmost set bit).",
                "int[] res = new int[2];",
                "For x in nums: if (x & diff) == 0 res[0] ^= x; else res[1] ^= x.",
                "Return res."
            ],
            "time": "O(n)",
            "space": "O(1)",
            "code": {
                "java": """class Solution {
    public int[] singleNumber(int[] nums) {
        int diff = 0;
        for (int x : nums) diff ^= x;
        diff &= -diff;
        int[] res = new int[2];
        for (int x : nums) {
            if ((x & diff) == 0) {
                res[0] ^= x;
            } else {
                res[1] ^= x;
            }
        }
        return res;
    }
}""",
                "python": """class Solution:
    def singleNumber(self, nums: list[int]) -> list[int]:
        diff = 0
        for x in nums:
            diff ^= x
        diff &= -diff
        a = b = 0
        for x in nums:
            if x & diff:
                a ^= x
            else:
                b ^= x
        return [a, b]"""
            }
        }
    },
    # 290: Number of 1 Bits
    {
        "seq": 290,
        "whyNext": "Brian Kernighan's algorithm: n & (n - 1) flips the lowest set bit to 0; loops exactly set-bit count times.",
        "brute": {
            "idea": "Loop through all 32 bit positions checking (n >> i) & 1.",
            "steps": [
                "Test all 32 bits."
            ],
            "time": "O(32)",
            "space": "O(1)",
            "whySlow": "Always takes 32 iterations even if only one bit is set.",
            "code": {
                "java": """class Solution {
    public int hammingWeight(int n) {
        int count = 0;
        for (int i = 0; i < 32; i++) {
            if (((n >> i) & 1) == 1) count++;
        }
        return count;
    }
}""",
                "python": """class Solution:
    def hammingWeight(self, n: int) -> int:
        return bin(n).count('1')"""
            }
        },
        "optimal": {
            "idea": "Brian Kernighan: while n != 0: n &= n - 1, count++. Iterates only over set bits.",
            "steps": [
                "count = 0.",
                "While n != 0: n &= (n - 1); count++.",
                "Return count."
            ],
            "time": "O(k) where k is number of 1s",
            "space": "O(1)",
            "code": {
                "java": """class Solution {
    public int hammingWeight(int n) {
        int count = 0;
        while (n != 0) {
            n &= (n - 1);
            count++;
        }
        return count;
    }
}""",
                "python": """class Solution:
    def hammingWeight(self, n: int) -> int:
        count = 0
        while n:
            n &= n - 1
            count += 1
        return count"""
            }
        }
    },
    # 291: Counting Bits
    {
        "seq": 291,
        "whyNext": "Bit DP: ans[i] = ans[i >> 1] + (i & 1); builds on Number of 1 Bits in linear O(n) time.",
        "brute": {
            "idea": "For every number from 0 to n, call Integer.bitCount(i).",
            "steps": [
                "Call bitCount on each integer."
            ],
            "time": "O(n * 32)",
            "space": "O(1) auxiliary",
            "whySlow": "Calculates bit count independently for each number without reusing subproblems.",
            "code": {
                "java": """class Solution {
    public int[] countBits(int n) {
        int[] ans = new int[n + 1];
        for (int i = 0; i <= n; i++) ans[i] = Integer.bitCount(i);
        return ans;
    }
}""",
                "python": """class Solution:
    def countBits(self, n: int) -> list[int]:
        return [bin(i).count('1') for i in range(n + 1)]"""
            }
        },
        "optimal": {
            "idea": "1D DP: ans[i] = ans[i >> 1] + (i & 1). Shifting right removes LSB; add back (i & 1).",
            "steps": [
                "int[] ans = new int[n + 1];",
                "For i = 1..n: ans[i] = ans[i >> 1] + (i & 1).",
                "Return ans."
            ],
            "time": "O(n)",
            "space": "O(1) auxiliary",
            "code": {
                "java": """class Solution {
    public int[] countBits(int n) {
        int[] ans = new int[n + 1];
        for (int i = 1; i <= n; i++) {
            ans[i] = ans[i >> 1] + (i & 1);
        }
        return ans;
    }
}""",
                "python": """class Solution:
    def countBits(self, n: int) -> list[int]:
        ans = [0] * (n + 1)
        for i in range(1, n + 1):
            ans[i] = ans[i >> 1] + (i & 1)
        return ans"""
            }
        }
    },
    # 292: Power of Two
    {
        "seq": 292,
        "whyNext": "Bitmask trick: n > 0 && (n & (n - 1)) == 0 has exactly one 1 bit in binary representation.",
        "brute": {
            "idea": "Repeatedly divide n by 2 while n is even; check if final quotient is 1.",
            "steps": [
                "While n > 0 and n % 2 == 0: n /= 2.",
                "Return n == 1."
            ],
            "time": "O(log n)",
            "space": "O(1)",
            "whySlow": "Loop iterations when bitwise test is O(1).",
            "code": {
                "java": """class Solution {
    public boolean isPowerOfTwo(int n) {
        if (n <= 0) return false;
        while (n % 2 == 0) n /= 2;
        return n == 1;
    }
}""",
                "python": """class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        if n <= 0: return False
        while n % 2 == 0: n //= 2
        return n == 1"""
            }
        },
        "optimal": {
            "idea": "Single bit check: n > 0 && (n & (n - 1)) == 0 in O(1) time.",
            "steps": [
                "Return n > 0 && (n & (n - 1)) == 0."
            ],
            "time": "O(1)",
            "space": "O(1)",
            "code": {
                "java": """class Solution {
    public boolean isPowerOfTwo(int n) {
        return n > 0 && (n & (n - 1)) == 0;
    }
}""",
                "python": """class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        return n > 0 and (n & (n - 1)) == 0"""
            }
        }
    },
    # 293: Missing Number
    {
        "seq": 293,
        "whyNext": "Gauss summation or XOR cancellation: XOR indices 0..n and all nums[i]; cancel duplicates to find missing number.",
        "brute": {
            "idea": "Sort array; check if nums[i] != i.",
            "steps": [
                "Sort nums.",
                "Find first index where nums[i] != i."
            ],
            "time": "O(n log n)",
            "space": "O(1)",
            "whySlow": "Sorting is unnecessary when sum or XOR runs in O(n).",
            "code": {
                "java": """import java.util.*;
class Solution {
    public int missingNumber(int[] nums) {
        Arrays.sort(nums);
        for (int i = 0; i < nums.length; i++) {
            if (nums[i] != i) return i;
        }
        return nums.length;
    }
}""",
                "python": """class Solution:
    def missingNumber(self, nums: list[int]) -> int:
        nums.sort()
        for i, x in enumerate(nums):
            if i != x: return i
        return len(nums)"""
            }
        },
        "optimal": {
            "idea": "Gauss sum formula: expected = n * (n + 1) / 2; missing = expected - actual_sum.",
            "steps": [
                "n = nums.length; expected = n * (n + 1) / 2.",
                "Subtract all elements in nums from expected.",
                "Return result."
            ],
            "time": "O(n)",
            "space": "O(1)",
            "code": {
                "java": """class Solution {
    public int missingNumber(int[] nums) {
        int n = nums.length;
        int expected = n * (n + 1) / 2;
        int sum = 0;
        for (int x : nums) sum += x;
        return expected - sum;
    }
}""",
                "python": """class Solution:
    def missingNumber(self, nums: list[int]) -> int:
        n = len(nums)
        return n * (n + 1) // 2 - sum(nums)"""
            }
        }
    },
    # 294: Reverse Bits
    {
        "seq": 294,
        "whyNext": "Bit reversal: iterate 32 times; res = (res << 1) | (n & 1); n >>= 1.",
        "brute": {
            "idea": "Convert to 32-character binary string, reverse string, parse back as unsigned int.",
            "steps": [
                "Format binary string.",
                "Reverse string.",
                "Parse integer."
            ],
            "time": "O(32)",
            "space": "O(32)",
            "whySlow": "String allocations.",
            "code": {
                "java": """class Solution {
    public int reverseBits(int n) {
        int res = 0;
        for (int i = 0; i < 32; i++) {
            res = (res << 1) | (n & 1);
            n >>>= 1;
        }
        return res;
    }
}""",
                "python": """class Solution:
    def reverseBits(self, n: int) -> int:
        res = 0
        for _ in range(32):
            res = (res << 1) | (n & 1)
            n >>= 1
        return res"""
            }
        },
        "optimal": {
            "idea": "Bitwise shift: res = (res << 1) | (n & 1); n >>>= 1 over 32 iterations in O(1) space.",
            "steps": [
                "res = 0.",
                "For i = 0..31: res = (res << 1) | (n & 1); n >>>= 1.",
                "Return res."
            ],
            "time": "O(1) (fixed 32 loops)",
            "space": "O(1)",
            "code": {
                "java": """class Solution {
    public int reverseBits(int n) {
        int res = 0;
        for (int i = 0; i < 32; i++) {
            res = (res << 1) | (n & 1);
            n >>>= 1;
        }
        return res;
    }
}""",
                "python": """class Solution:
    def reverseBits(self, n: int) -> int:
        res = 0
        for _ in range(32):
            res = (res << 1) | (n & 1)
            n >>= 1
        return res"""
            }
        }
    },
    # 295: Sum of Two Integers
    {
        "seq": 295,
        "whyNext": "Full adder without + or -: sum without carry is a ^ b; carry is (a & b) << 1; loop until carry == 0.",
        "brute": {
            "idea": "Simulate bit-by-bit addition using bitwise carry and sum.",
            "steps": [
                "While carry b != 0: sum = a ^ b, carry = (a & b) << 1."
            ],
            "time": "O(32)",
            "space": "O(1)",
            "whySlow": "Standard bitwise adder is already optimal.",
            "code": {
                "java": """class Solution {
    public int getSum(int a, int b) {
        while (b != 0) {
            int carry = (a & b) << 1;
            a = a ^ b;
            b = carry;
        }
        return a;
    }
}""",
                "python": """class Solution:
    def getSum(self, a: int, b: int) -> int:
        mask = 0xFFFFFFFF
        while b & mask != 0:
            carry = (a & b) << 1
            a = a ^ b
            b = carry
        return (a & mask) if b > 0 else a"""
            }
        },
        "optimal": {
            "idea": "Hardware adder simulation: while b != 0: carry = (a & b) << 1, a = a ^ b, b = carry.",
            "steps": [
                "While b != 0:",
                "carry = (a & b) << 1.",
                "a = a ^ b.",
                "b = carry.",
                "Return a."
            ],
            "time": "O(1) (max 32 loops)",
            "space": "O(1)",
            "code": {
                "java": """class Solution {
    public int getSum(int a, int b) {
        while (b != 0) {
            int carry = (a & b) << 1;
            a = a ^ b;
            b = carry;
        }
        return a;
    }
}""",
                "python": """class Solution:
    def getSum(self, a: int, b: int) -> int:
        mask = 0xFFFFFFFF
        max_int = 0x7FFFFFFF
        while (b & mask) != 0:
            carry = (a & b) << 1
            a = (a ^ b) & mask
            b = carry & mask
        return a if a <= max_int else ~(a ^ mask)"""
            }
        }
    },
    # 296: Reverse Integer
    {
        "seq": 296,
        "whyNext": "32-bit signed integer overflow guard: check rev > Integer.MAX_VALUE / 10 before rev = rev * 10 + pop.",
        "brute": {
            "idea": "Convert to string, reverse, parse with Long to detect overflow.",
            "steps": [
                "String reversal.",
                "Check 32-bit bounds."
            ],
            "time": "O(log x)",
            "space": "O(log x)",
            "whySlow": "String allocations instead of mathematical arithmetic.",
            "code": {
                "java": """class Solution {
    public int reverse(int x) {
        long rev = 0;
        while (x != 0) {
            rev = rev * 10 + x % 10;
            x /= 10;
        }
        if (rev > Integer.MAX_VALUE || rev < Integer.MIN_VALUE) return 0;
        return (int) rev;
    }
}""",
                "python": """class Solution:
    def reverse(self, x: int) -> int:
        sign = -1 if x < 0 else 1
        x = abs(x)
        rev = int(str(x)[::-1]) * sign
        return rev if -2**31 <= rev <= 2**31 - 1 else 0"""
            }
        },
        "optimal": {
            "idea": "Mathematical pop and push with overflow check before multiplication: if rev > Integer.MAX_VALUE / 10 return 0.",
            "steps": [
                "rev = 0.",
                "While x != 0:",
                "pop = x % 10; x /= 10.",
                "If rev > Integer.MAX_VALUE / 10 || rev < Integer.MIN_VALUE / 10 return 0.",
                "rev = rev * 10 + pop.",
                "Return rev."
            ],
            "time": "O(log x)",
            "space": "O(1)",
            "code": {
                "java": """class Solution {
    public int reverse(int x) {
        int rev = 0;
        while (x != 0) {
            int pop = x % 10;
            x /= 10;
            if (rev > Integer.MAX_VALUE / 10 || (rev == Integer.MAX_VALUE / 10 && pop > 7)) return 0;
            if (rev < Integer.MIN_VALUE / 10 || (rev == Integer.MIN_VALUE / 10 && pop < -8)) return 0;
            rev = rev * 10 + pop;
        }
        return rev;
    }
}""",
                "python": """class Solution:
    def reverse(self, x: int) -> int:
        rev = 0
        sign = -1 if x < 0 else 1
        x = abs(x)
        while x:
            pop = x % 10
            x //= 10
            rev = rev * 10 + pop
        rev *= sign
        return rev if -2**31 <= rev <= 2**31 - 1 else 0"""
            }
        }
    },
    # 297: Palindrome Number
    {
        "seq": 297,
        "whyNext": "Builds on Reverse Integer: negative numbers cannot be palindromes; reverse only the second half of digits to avoid overflow entirely.",
        "brute": {
            "idea": "Convert integer to string and check if str == reverse(str).",
            "steps": [
                "s = String.valueOf(x).",
                "Two pointers check palindrome."
            ],
            "time": "O(log x)",
            "space": "O(log x)",
            "whySlow": "Allocates string.",
            "code": {
                "java": """class Solution {
    public boolean isPalindrome(int x) {
        if (x < 0) return false;
        String s = String.valueOf(x);
        int l = 0, r = s.length() - 1;
        while (l < r) {
            if (s.charAt(l++) != s.charAt(r--)) return false;
        }
        return true;
    }
}""",
                "python": """class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0: return False
        s = str(x)
        return s == s[::-1]"""
            }
        },
        "optimal": {
            "idea": "Reversing half of number: when x <= revertedNumber, half is reached. Check x == revertedNumber || x == revertedNumber / 10.",
            "steps": [
                "If x < 0 || (x % 10 == 0 && x != 0) return false.",
                "rev = 0.",
                "While x > rev: rev = rev * 10 + x % 10; x /= 10.",
                "Return x == rev || x == rev / 10."
            ],
            "time": "O(log x)",
            "space": "O(1)",
            "code": {
                "java": """class Solution {
    public boolean isPalindrome(int x) {
        if (x < 0 || (x % 10 == 0 && x != 0)) return false;
        int rev = 0;
        while (x > rev) {
            rev = rev * 10 + x % 10;
            x /= 10;
        }
        return x == rev || x == rev / 10;
    }
}""",
                "python": """class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0 or (x % 10 == 0 and x != 0):
            return False
        rev = 0
        while x > rev:
            rev = rev * 10 + x % 10
            x //= 10
        return x == rev or x == rev // 10"""
            }
        }
    },
    # 298: Happy Number
    {
        "seq": 298,
        "whyNext": "Cycle detection on digit transformations: Floyd's tortoise and hare detects loop in next_number sequence.",
        "brute": {
            "idea": "Keep a HashSet of visited numbers; loop until reaching 1 or revisiting a number.",
            "steps": [
                "HashSet tracks seen sums of squares.",
                "If sum == 1 return true; if seen return false."
            ],
            "time": "O(log n)",
            "space": "O(log n)",
            "whySlow": "Allocates set.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public boolean isHappy(int n) {
        Set<Integer> seen = new HashSet<>();
        while (n != 1 && !seen.contains(n)) {
            seen.add(n);
            n = getNext(n);
        }
        return n == 1;
    }
    private int getNext(int n) {
        int sum = 0;
        while (n > 0) {
            int d = n % 10;
            sum += d * d;
            n /= 10;
        }
        return sum;
    }
}""",
                "python": """class Solution:
    def isHappy(self, n: int) -> bool:
        seen = set()
        while n != 1 and n not in seen:
            seen.add(n)
            n = sum(int(d)**2 for d in str(n))
        return n == 1"""
            }
        },
        "optimal": {
            "idea": "Floyd's Cycle Finding (Tortoise and Hare): slow advances 1 step, fast advances 2 steps. If fast reaches 1 return true; if slow == fast cycle exists.",
            "steps": [
                "slow = n, fast = getNext(n).",
                "While fast != 1 && slow != fast: slow = getNext(slow), fast = getNext(getNext(fast)).",
                "Return fast == 1."
            ],
            "time": "O(log n)",
            "space": "O(1)",
            "code": {
                "java": """class Solution {
    public boolean isHappy(int n) {
        int slow = n, fast = getNext(n);
        while (fast != 1 && slow != fast) {
            slow = getNext(slow);
            fast = getNext(getNext(fast));
        }
        return fast == 1;
    }
    private int getNext(int n) {
        int total = 0;
        while (n > 0) {
            int d = n % 10;
            total += d * d;
            n /= 10;
        }
        return total;
    }
}""",
                "python": """class Solution:
    def isHappy(self, n: int) -> bool:
        def get_next(val):
            total = 0
            while val > 0:
                d = val % 10
                total += d * d
                val //= 10
            return total
        slow = n
        fast = get_next(n)
        while fast != 1 and slow != fast:
            slow = get_next(slow)
            fast = get_next(get_next(fast))
        return fast == 1"""
            }
        }
    },
    # 299: Count Primes
    {
        "seq": 299,
        "whyNext": "Sieve of Eratosthenes: mark multiples of primes starting from p*p in boolean array; counts primes < n in O(n log log n).",
        "brute": {
            "idea": "For every number 2..n-1, test trial division up to sqrt(i).",
            "steps": [
                "isPrime(x): loop 2..sqrt(x).",
                "Count primes."
            ],
            "time": "O(n * sqrt(n))",
            "space": "O(1)",
            "whySlow": "Trial division on all numbers is significantly slower than Sieve of Eratosthenes.",
            "code": {
                "java": """class Solution {
    public int countPrimes(int n) {
        int count = 0;
        for (int i = 2; i < n; i++) {
            if (isPrime(i)) count++;
        }
        return count;
    }
    private boolean isPrime(int x) {
        for (int i = 2; i * i <= x; i++) {
            if (x % i == 0) return false;
        }
        return true;
    }
}""",
                "python": """class Solution:
    def countPrimes(self, n: int) -> int:
        def is_prime(x):
            i = 2
            while i * i <= x:
                if x % i == 0: return False
                i += 1
            return True
        return sum(1 for i in range(2, n) if is_prime(i))"""
            }
        },
        "optimal": {
            "idea": "Sieve of Eratosthenes: boolean[] notPrime = new boolean[n]; for i = 2..sqrt(n), if !notPrime[i], mark all i*i, i*i + i, ... as true.",
            "steps": [
                "if n <= 2 return 0.",
                "boolean[] notPrime = new boolean[n]; int count = 0.",
                "For i = 2..sqrt(n): if !notPrime[i]: for j = i * i; j < n; j += i notPrime[j] = true.",
                "For i = 2..n-1: if !notPrime[i] count++.",
                "Return count."
            ],
            "time": "O(n log log n)",
            "space": "O(n)",
            "code": {
                "java": """class Solution {
    public int countPrimes(int n) {
        if (n <= 2) return 0;
        boolean[] notPrime = new boolean[n];
        for (int i = 2; i * i < n; i++) {
            if (!notPrime[i]) {
                for (int j = i * i; j < n; j += i) {
                    notPrime[j] = true;
                }
            }
        }
        int count = 0;
        for (int i = 2; i < n; i++) {
            if (!notPrime[i]) count++;
        }
        return count;
    }
}""",
                "python": """class Solution:
    def countPrimes(self, n: int) -> int:
        if n <= 2:
            return 0
        not_prime = [False] * n
        i = 2
        while i * i < n:
            if not not_prime[i]:
                for j in range(i * i, n, i):
                    not_prime[j] = True
            i += 1
        return sum(1 for x in range(2, n) if not not_prime[x])"""
            }
        }
    },
    # 300: Factorial Trailing Zeroes
    {
        "seq": 300,
        "whyNext": "Grand finale: Legendre's formula counts factors of 5 in n! (since 2s outnumber 5s): zeros = n/5 + n/25 + n/125 + ... in O(log_5 n).",
        "brute": {
            "idea": "Compute full factorial BigInteger and count trailing zeroes in string representation.",
            "steps": [
                "Compute n! using BigInteger.",
                "Count trailing '0' characters."
            ],
            "time": "O(n^2)",
            "space": "O(n)",
            "whySlow": "Factorial grows factorially large exceeding 10,000 digits.",
            "code": {
                "java": """import java.math.BigInteger;
class Solution {
    public int trailingZeroes(int n) {
        BigInteger fact = BigInteger.ONE;
        for (int i = 2; i <= n; i++) fact = fact.multiply(BigInteger.valueOf(i));
        int count = 0;
        while (fact.mod(BigInteger.TEN).equals(BigInteger.ZERO)) {
            count++;
            fact = fact.divide(BigInteger.TEN);
        }
        return count;
    }
}""",
                "python": """class Solution:
    def trailingZeroes(self, n: int) -> int:
        import math
        fact = math.factorial(n)
        s = str(fact)
        return len(s) - len(s.rstrip('0'))"""
            }
        },
        "optimal": {
            "idea": "Legendre's Formula: count prime factor 5s: count = n/5 + n/25 + n/125 + ... in O(log_5 n) time and O(1) space.",
            "steps": [
                "count = 0.",
                "While n >= 5: count += n / 5; n /= 5.",
                "Return count."
            ],
            "time": "O(log_5 n)",
            "space": "O(1)",
            "code": {
                "java": """class Solution {
    public int trailingZeroes(int n) {
        int count = 0;
        while (n >= 5) {
            count += n / 5;
            n /= 5;
        }
        return count;
    }
}""",
                "python": """class Solution:
    def trailingZeroes(self, n: int) -> int:
        count = 0
        while n >= 5:
            count += n // 5
            n //= 5
        return count"""
            }
        }
    }
]

with open('scripts/batches/batch_12.py', 'w', encoding='utf-8') as f:
    f.write("# Batch 12: Questions 276 to 300\n\n")
    f.write("def get_batch():\n")
    f.write("    return " + json.dumps(batch_12, indent=4) + "\n")

print("Wrote scripts/batches/batch_12.py with", len(batch_12), "questions.")


# Batch 12: Questions 276 to 300

def get_batch():
    return [
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
                "java": "class Solution {\n    public int maxProfit(int[] prices) {\n        int b1 = Integer.MIN_VALUE, s1 = 0;\n        int b2 = Integer.MIN_VALUE, s2 = 0;\n        for (int p : prices) {\n            b1 = Math.max(b1, -p);\n            s1 = Math.max(s1, b1 + p);\n            b2 = Math.max(b2, s1 - p);\n            s2 = Math.max(s2, b2 + p);\n        }\n        return s2;\n    }\n}",
                "python": "class Solution:\n    def maxProfit(self, prices: list[int]) -> int:\n        b1 = b2 = float('-inf')\n        s1 = s2 = 0\n        for p in prices:\n            b1 = max(b1, -p)\n            s1 = max(s1, b1 + p)\n            b2 = max(b2, s1 - p)\n            s2 = max(s2, b2 + p)\n        return s2"
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
                "java": "class Solution {\n    public int maxProfit(int[] prices) {\n        if (prices.length == 0) return 0;\n        int b1 = -prices[0], s1 = 0;\n        int b2 = -prices[0], s2 = 0;\n        for (int p : prices) {\n            b1 = Math.max(b1, -p);\n            s1 = Math.max(s1, b1 + p);\n            b2 = Math.max(b2, s1 - p);\n            s2 = Math.max(s2, b2 + p);\n        }\n        return s2;\n    }\n}",
                "python": "class Solution:\n    def maxProfit(self, prices: list[int]) -> int:\n        if not prices:\n            return 0\n        b1 = b2 = -prices[0]\n        s1 = s2 = 0\n        for p in prices:\n            b1 = max(b1, -p)\n            s1 = max(s1, b1 + p)\n            b2 = max(b2, s1 - p)\n            s2 = max(s2, b2 + p)\n        return s2"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public int maxProfit(int k, int[] prices) {\n        int n = prices.length;\n        if (n <= 1 || k == 0) return 0;\n        if (k >= n / 2) {\n            int p = 0;\n            for (int i = 1; i < n; i++) if (prices[i] > prices[i - 1]) p += prices[i] - prices[i - 1];\n            return p;\n        }\n        int[] buy = new int[k + 1];\n        int[] sell = new int[k + 1];\n        Arrays.fill(buy, -prices[0]);\n        for (int p : prices) {\n            for (int j = 1; j <= k; j++) {\n                buy[j] = Math.max(buy[j], sell[j - 1] - p);\n                sell[j] = Math.max(sell[j], buy[j] + p);\n            }\n        }\n        return sell[k];\n    }\n}",
                "python": "class Solution:\n    def maxProfit(self, k: int, prices: list[int]) -> int:\n        n = len(prices)\n        if n <= 1 or k == 0: return 0\n        if k >= n // 2:\n            return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, n))\n        buy = [-prices[0]] * (k + 1)\n        sell = [0] * (k + 1)\n        for p in prices:\n            for j in range(1, k + 1):\n                buy[j] = max(buy[j], sell[j - 1] - p)\n                sell[j] = max(sell[j], buy[j] + p)\n        return sell[k]"
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
                "java": "import java.util.*;\nclass Solution {\n    public int maxProfit(int k, int[] prices) {\n        int n = prices.length;\n        if (n <= 1 || k == 0) return 0;\n        if (k >= n / 2) {\n            int profit = 0;\n            for (int i = 1; i < n; i++) {\n                if (prices[i] > prices[i - 1]) profit += prices[i] - prices[i - 1];\n            }\n            return profit;\n        }\n        int[] buy = new int[k + 1];\n        int[] sell = new int[k + 1];\n        Arrays.fill(buy, -prices[0]);\n        for (int p : prices) {\n            for (int j = 1; j <= k; j++) {\n                buy[j] = Math.max(buy[j], sell[j - 1] - p);\n                sell[j] = Math.max(sell[j], buy[j] + p);\n            }\n        }\n        return sell[k];\n    }\n}",
                "python": "class Solution:\n    def maxProfit(self, k: int, prices: list[int]) -> int:\n        n = len(prices)\n        if n <= 1 or k == 0:\n            return 0\n        if k >= n // 2:\n            return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, n))\n        buy = [-prices[0]] * (k + 1)\n        sell = [0] * (k + 1)\n        for p in prices:\n            for j in range(1, k + 1):\n                buy[j] = max(buy[j], sell[j - 1] - p)\n                sell[j] = max(sell[j], buy[j] + p)\n        return sell[k]"
            }
        }
    },
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
                "java": "class Solution {\n    public String longestCommonPrefix(String[] strs) {\n        if (strs.length == 0) return \"\";\n        String prefix = strs[0];\n        for (int i = 1; i < strs.length; i++) {\n            while (strs[i].indexOf(prefix) != 0) {\n                prefix = prefix.substring(0, prefix.length() - 1);\n                if (prefix.isEmpty()) return \"\";\n            }\n        }\n        return prefix;\n    }\n}",
                "python": "class Solution:\n    def longestCommonPrefix(self, strs: list[str]) -> str:\n        if not strs: return \"\"\n        prefix = strs[0]\n        for s in strs[1:]:\n            while not s.startswith(prefix):\n                prefix = prefix[:-1]\n                if not prefix: return \"\"\n        return prefix"
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
                "java": "class Solution {\n    public String longestCommonPrefix(String[] strs) {\n        if (strs == null || strs.length == 0) return \"\";\n        for (int i = 0; i < strs[0].length(); i++) {\n            char c = strs[0].charAt(i);\n            for (int j = 1; j < strs.length; j++) {\n                if (i == strs[j].length() || strs[j].charAt(i) != c) {\n                    return strs[0].substring(0, i);\n                }\n            }\n        }\n        return strs[0];\n    }\n}",
                "python": "class Solution:\n    def longestCommonPrefix(self, strs: list[str]) -> str:\n        if not strs:\n            return \"\"\n        for i, c in enumerate(strs[0]):\n            for s in strs[1:]:\n                if i == len(s) or s[i] != c:\n                    return strs[0][:i]\n        return strs[0]"
            }
        }
    },
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
                "java": "import java.util.*;\npublic class Trie {\n    private Set<String> words = new HashSet<>();\n    public Trie() {}\n    public void insert(String word) {\n        words.add(word);\n    }\n    public boolean search(String word) {\n        return words.contains(word);\n    }\n    public boolean startsWith(String prefix) {\n        for (String w : words) {\n            if (w.startsWith(prefix)) return true;\n        }\n        return false;\n    }\n}",
                "python": "class Trie:\n    def __init__(self):\n        self.words = set()\n\n    def insert(self, word: str) -> None:\n        self.words.add(word)\n\n    def search(self, word: str) -> bool:\n        return word in self.words\n\n    def startsWith(self, prefix: str) -> bool:\n        return any(w.startswith(prefix) for w in self.words)"
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
                "java": "public class Trie {\n    private static class Node {\n        Node[] children = new Node[26];\n        boolean isWord = false;\n    }\n    private Node root = new Node();\n    public Trie() {}\n    public void insert(String word) {\n        Node cur = root;\n        for (char c : word.toCharArray()) {\n            int idx = c - 'a';\n            if (cur.children[idx] == null) cur.children[idx] = new Node();\n            cur = cur.children[idx];\n        }\n        cur.isWord = true;\n    }\n    public boolean search(String word) {\n        Node node = find(word);\n        return node != null && node.isWord;\n    }\n    public boolean startsWith(String prefix) {\n        return find(prefix) != null;\n    }\n    private Node find(String s) {\n        Node cur = root;\n        for (char c : s.toCharArray()) {\n            int idx = c - 'a';\n            if (cur.children[idx] == null) return null;\n            cur = cur.children[idx];\n        }\n        return cur;\n    }\n}",
                "python": "class Trie:\n    def __init__(self):\n        self.root = {}\n\n    def insert(self, word: str) -> None:\n        cur = self.root\n        for c in word:\n            if c not in cur:\n                cur[c] = {}\n            cur = cur[c]\n        cur['#'] = True\n\n    def search(self, word: str) -> bool:\n        cur = self.root\n        for c in word:\n            if c not in cur:\n                return False\n            cur = cur[c]\n        return '#' in cur\n\n    def startsWith(self, prefix: str) -> bool:\n        cur = self.root\n        for c in prefix:\n            if c not in cur:\n                return False\n            cur = cur[c]\n        return True"
            }
        }
    },
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
                "java": "import java.util.*;\npublic class WordDictionary {\n    private List<String> words = new ArrayList<>();\n    public WordDictionary() {}\n    public void addWord(String word) {\n        words.add(word);\n    }\n    public boolean search(String word) {\n        for (String w : words) {\n            if (match(w, word)) return true;\n        }\n        return false;\n    }\n    private boolean match(String s, String p) {\n        if (s.length() != p.length()) return false;\n        for (int i = 0; i < s.length(); i++) {\n            if (p.charAt(i) != '.' && p.charAt(i) != s.charAt(i)) return false;\n        }\n        return true;\n    }\n}",
                "python": "class WordDictionary:\n    def __init__(self):\n        self.words = []\n\n    def addWord(self, word: str) -> None:\n        self.words.append(word)\n\n    def search(self, word: str) -> bool:\n        n = len(word)\n        for w in self.words:\n            if len(w) == n and all(p == '.' or p == c for p, c in zip(word, w)):\n                return True\n        return False"
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
                "java": "public class WordDictionary {\n    private static class Node {\n        Node[] children = new Node[26];\n        boolean isWord = false;\n    }\n    private Node root = new Node();\n    public WordDictionary() {}\n    public void addWord(String word) {\n        Node cur = root;\n        for (char c : word.toCharArray()) {\n            int idx = c - 'a';\n            if (cur.children[idx] == null) cur.children[idx] = new Node();\n            cur = cur.children[idx];\n        }\n        cur.isWord = true;\n    }\n    public boolean search(String word) {\n        return search(root, word, 0);\n    }\n    private boolean search(Node node, String word, int idx) {\n        if (node == null) return false;\n        if (idx == word.length()) return node.isWord;\n        char c = word.charAt(idx);\n        if (c == '.') {\n            for (Node child : node.children) {\n                if (child != null && search(child, word, idx + 1)) return true;\n            }\n            return false;\n        } else {\n            return search(node.children[c - 'a'], word, idx + 1);\n        }\n    }\n}",
                "python": "class WordDictionary:\n    def __init__(self):\n        self.root = {}\n\n    def addWord(self, word: str) -> None:\n        cur = self.root\n        for c in word:\n            if c not in cur:\n                cur[c] = {}\n            cur = cur[c]\n        cur['#'] = True\n\n    def search(self, word: str) -> bool:\n        def dfs(node, idx):\n            if idx == len(word):\n                return '#' in node\n            c = word[idx]\n            if c == '.':\n                for k, child in node.items():\n                    if k != '#' and dfs(child, idx + 1):\n                        return True\n                return False\n            if c not in node:\n                return False\n            return dfs(node[c], idx + 1)\n        return dfs(self.root, 0)"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public String replaceWords(List<String> dictionary, String sentence) {\n        Set<String> set = new HashSet<>(dictionary);\n        String[] words = sentence.split(\" \");\n        for (int i = 0; i < words.length; i++) {\n            String word = words[i];\n            for (int len = 1; len <= word.length(); len++) {\n                String sub = word.substring(0, len);\n                if (set.contains(sub)) {\n                    words[i] = sub;\n                    break;\n                }\n            }\n        }\n        return String.join(\" \", words);\n    }\n}",
                "python": "class Solution:\n    def replaceWords(self, dictionary: list[str], sentence: list[str]) -> str:\n        roots = set(dictionary)\n        res = []\n        for word in sentence.split():\n            for i in range(1, len(word) + 1):\n                if word[:i] in roots:\n                    res.append(word[:i])\n                    break\n            else:\n                res.append(word)\n        return \" \".join(res)"
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
                "java": "import java.util.*;\nclass Solution {\n    private static class Node {\n        Node[] children = new Node[26];\n        boolean isWord = false;\n    }\n    public String replaceWords(List<String> dictionary, String sentence) {\n        Node root = new Node();\n        for (String d : dictionary) {\n            Node cur = root;\n            for (char c : d.toCharArray()) {\n                int idx = c - 'a';\n                if (cur.children[idx] == null) cur.children[idx] = new Node();\n                cur = cur.children[idx];\n            }\n            cur.isWord = true;\n        }\n        String[] words = sentence.split(\" \");\n        for (int i = 0; i < words.length; i++) {\n            words[i] = findRoot(root, words[i]);\n        }\n        return String.join(\" \", words);\n    }\n    private String findRoot(Node root, String word) {\n        Node cur = root;\n        StringBuilder sb = new StringBuilder();\n        for (char c : word.toCharArray()) {\n            int idx = c - 'a';\n            if (cur.children[idx] == null) return word;\n            sb.append(c);\n            cur = cur.children[idx];\n            if (cur.isWord) return sb.toString();\n        }\n        return word;\n    }\n}",
                "python": "class Solution:\n    def replaceWords(self, dictionary: list[str], sentence: str) -> str:\n        root = {}\n        for d in dictionary:\n            cur = root\n            for c in d:\n                if c not in cur: cur[c] = {}\n                cur = cur[c]\n            cur['#'] = True\n        def find_root(word):\n            cur = root\n            prefix = []\n            for c in word:\n                if c not in cur: return word\n                prefix.append(c)\n                cur = cur[c]\n                if '#' in cur: return \"\".join(prefix)\n            return word\n        return \" \".join(find_root(w) for w in sentence.split())"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public List<List<String>> suggestedProducts(String[] products, String searchWord) {\n        Arrays.sort(products);\n        List<List<String>> res = new ArrayList<>();\n        String cur = \"\";\n        for (char c : searchWord.toCharArray()) {\n            cur += c;\n            List<String> list = new ArrayList<>();\n            for (String p : products) {\n                if (p.startsWith(cur)) {\n                    list.add(p);\n                    if (list.size() == 3) break;\n                }\n            }\n            res.add(list);\n        }\n        return res;\n    }\n}",
                "python": "class Solution:\n    def suggestedProducts(self, products: list[str], searchWord: str) -> list[list[str]]:\n        products.sort()\n        res = []\n        cur = \"\"\n        for c in searchWord:\n            cur += c\n            res.append([p for p in products if p.startswith(cur)][:3])\n        return res"
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
                "java": "import java.util.*;\nclass Solution {\n    public List<List<String>> suggestedProducts(String[] products, String searchWord) {\n        Arrays.sort(products);\n        List<List<String>> res = new ArrayList<>();\n        int l = 0, r = products.length - 1;\n        for (int i = 0; i < searchWord.length(); i++) {\n            char c = searchWord.charAt(i);\n            while (l <= r && (products[l].length() <= i || products[l].charAt(i) != c)) l++;\n            while (l <= r && (products[r].length() <= i || products[r].charAt(i) != c)) r--;\n            List<String> list = new ArrayList<>();\n            for (int k = l; k <= Math.min(l + 2, r); k++) {\n                list.add(products[k]);\n            }\n            res.add(list);\n        }\n        return res;\n    }\n}",
                "python": "class Solution:\n    def suggestedProducts(self, products: list[str], searchWord: str) -> list[list[str]]:\n        products.sort()\n        res = []\n        l, r = 0, len(products) - 1\n        for i, c in enumerate(searchWord):\n            while l <= r and (len(products[l]) <= i or products[l][i] != c):\n                l += 1\n            while l <= r and (len(products[r]) <= i or products[r][i] != c):\n                r -= 1\n            res.append(products[l:min(l + 3, r + 1)])\n        return res"
            }
        }
    },
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
                "java": "import java.util.*;\npublic class MapSum {\n    private Map<String, Integer> map = new HashMap<>();\n    public MapSum() {}\n    public void insert(String key, int val) {\n        map.put(key, val);\n    }\n    public int sum(String prefix) {\n        int sum = 0;\n        for (String k : map.keySet()) {\n            if (k.startsWith(prefix)) sum += map.get(k);\n        }\n        return sum;\n    }\n}",
                "python": "class MapSum:\n    def __init__(self):\n        self.map = {}\n\n    def insert(self, key: str, val: int) -> None:\n        self.map[key] = val\n\n    def sum(self, prefix: str) -> int:\n        return sum(v for k, v in self.map.items() if k.startswith(prefix))"
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
                "java": "import java.util.*;\npublic class MapSum {\n    private static class Node {\n        Node[] children = new Node[26];\n        int score = 0;\n    }\n    private Map<String, Integer> map = new HashMap<>();\n    private Node root = new Node();\n    public MapSum() {}\n    public void insert(String key, int val) {\n        int delta = val - map.getOrDefault(key, 0);\n        map.put(key, val);\n        Node cur = root;\n        for (char c : key.toCharArray()) {\n            int idx = c - 'a';\n            if (cur.children[idx] == null) cur.children[idx] = new Node();\n            cur = cur.children[idx];\n            cur.score += delta;\n        }\n    }\n    public int sum(String prefix) {\n        Node cur = root;\n        for (char c : prefix.toCharArray()) {\n            int idx = c - 'a';\n            if (cur.children[idx] == null) return 0;\n            cur = cur.children[idx];\n        }\n        return cur.score;\n    }\n}",
                "python": "class MapSum:\n    def __init__(self):\n        self.map = {}\n        self.root = {}\n\n    def insert(self, key: str, val: int) -> None:\n        delta = val - self.map.get(key, 0)\n        self.map[key] = val\n        cur = self.root\n        for c in key:\n            if c not in cur:\n                cur[c] = {'score': 0}\n            cur = cur[c]\n            cur['score'] += delta\n\n    def sum(self, prefix: str) -> int:\n        cur = self.root\n        for c in prefix:\n            if c not in cur:\n                return 0\n            cur = cur[c]\n        return cur['score']"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public List<String> findWords(char[][] board, String[] words) {\n        List<String> res = new ArrayList<>();\n        Node root = buildTrie(words);\n        for (int i = 0; i < board.length; i++) {\n            for (int j = 0; j < board[0].length; j++) {\n                dfs(board, i, j, root, res);\n            }\n        }\n        return res;\n    }\n    private void dfs(char[][] board, int r, int c, Node p, List<String> res) {\n        char ch = board[r][c];\n        if (ch == '#' || p.children[ch - 'a'] == null) return;\n        p = p.children[ch - 'a'];\n        if (p.word != null) {\n            res.add(p.word);\n            p.word = null;\n        }\n        board[r][c] = '#';\n        if (r > 0) dfs(board, r - 1, c, p, res);\n        if (c > 0) dfs(board, r, c - 1, p, res);\n        if (r < board.length - 1) dfs(board, r + 1, c, p, res);\n        if (c < board[0].length - 1) dfs(board, r, c + 1, p, res);\n        board[r][c] = ch;\n    }\n    private static class Node {\n        Node[] children = new Node[26];\n        String word;\n    }\n    private Node buildTrie(String[] words) {\n        Node root = new Node();\n        for (String w : words) {\n            Node cur = root;\n            for (char c : w.toCharArray()) {\n                int idx = c - 'a';\n                if (cur.children[idx] == null) cur.children[idx] = new Node();\n                cur = cur.children[idx];\n            }\n            cur.word = w;\n        }\n        return root;\n    }\n}",
                "python": "class Solution:\n    def findWords(self, board: list[list[str]], words: list[str]) -> list[str]:\n        trie = {}\n        for word in words:\n            cur = trie\n            for c in word:\n                cur = cur.setdefault(c, {})\n            cur['$'] = word\n        m, n = len(board), len(board[0])\n        res = []\n        def dfs(r, c, parent):\n            char = board[r][c]\n            cur = parent[char]\n            if '$' in cur:\n                res.append(cur.pop('$'))\n            board[r][c] = '#'\n            for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):\n                nr, nc = r + dr, c + dc\n                if 0 <= nr < m and 0 <= nc < n and board[nr][nc] in cur:\n                    dfs(nr, nc, cur)\n            board[r][c] = char\n        for i in range(m):\n            for j in range(n):\n                if board[i][j] in trie:\n                    dfs(i, j, trie)\n        return res"
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
                "java": "import java.util.*;\nclass Solution {\n    private static class Node {\n        Node[] children = new Node[26];\n        String word = null;\n    }\n    public List<String> findWords(char[][] board, String[] words) {\n        Node root = new Node();\n        for (String w : words) {\n            Node cur = root;\n            for (char c : w.toCharArray()) {\n                int idx = c - 'a';\n                if (cur.children[idx] == null) cur.children[idx] = new Node();\n                cur = cur.children[idx];\n            }\n            cur.word = w;\n        }\n        List<String> res = new ArrayList<>();\n        int m = board.length, n = board[0].length;\n        for (int i = 0; i < m; i++) {\n            for (int j = 0; j < n; j++) {\n                if (root.children[board[i][j] - 'a'] != null) {\n                    dfs(board, i, j, root, res);\n                }\n            }\n        }\n        return res;\n    }\n    private void dfs(char[][] board, int r, int c, Node parent, List<String> res) {\n        char ch = board[r][c];\n        if (ch == '#' || parent.children[ch - 'a'] == null) return;\n        Node cur = parent.children[ch - 'a'];\n        if (cur.word != null) {\n            res.add(cur.word);\n            cur.word = null;\n        }\n        board[r][c] = '#';\n        if (r > 0) dfs(board, r - 1, c, cur, res);\n        if (c > 0) dfs(board, r, c - 1, cur, res);\n        if (r < board.length - 1) dfs(board, r + 1, c, cur, res);\n        if (c < board[0].length - 1) dfs(board, r, c + 1, cur, res);\n        board[r][c] = ch;\n    }\n}",
                "python": "class Solution:\n    def findWords(self, board: list[list[str]], words: list[str]) -> list[str]:\n        trie = {}\n        for w in words:\n            cur = trie\n            for c in w:\n                cur = cur.setdefault(c, {})\n            cur['#'] = w\n        m, n = len(board), len(board[0])\n        res = []\n        def dfs(r: int, c: int, parent: dict):\n            ch = board[r][c]\n            cur = parent[ch]\n            if '#' in cur:\n                res.append(cur.pop('#'))\n            board[r][c] = '$'\n            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n                nr, nc = r + dr, c + dc\n                if 0 <= nr < m and 0 <= nc < n and board[nr][nc] in cur:\n                    dfs(nr, nc, cur)\n            board[r][c] = ch\n        for i in range(m):\n            for j in range(n):\n                if board[i][j] in trie:\n                    dfs(i, j, trie)\n        return res"
            }
        }
    },
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
                "java": "class Solution {\n    public int findMaximumXOR(int[] nums) {\n        int max = 0, mask = 0;\n        for (int i = 31; i >= 0; i--) {\n            mask |= (1 << i);\n            java.util.Set<Integer> set = new java.util.HashSet<>();\n            for (int num : nums) set.add(num & mask);\n            int candidate = max | (1 << i);\n            for (int prefix : set) {\n                if (set.contains(prefix ^ candidate)) {\n                    max = candidate;\n                    break;\n                }\n            }\n        }\n        return max;\n    }\n}",
                "python": "class Solution:\n    def findMaximumXOR(self, nums: list[int]) -> int:\n        max_xor = 0\n        mask = 0\n        for i in range(31, -1, -1):\n            mask |= (1 << i)\n            prefixes = {num & mask for num in nums}\n            candidate = max_xor | (1 << i)\n            if any(candidate ^ p in prefixes for p in prefixes):\n                max_xor = candidate\n        return max_xor"
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
                "java": "class Solution {\n    private static class Node {\n        Node[] children = new Node[2];\n    }\n    public int findMaximumXOR(int[] nums) {\n        Node root = new Node();\n        for (int num : nums) {\n            Node cur = root;\n            for (int i = 31; i >= 0; i--) {\n                int bit = (num >> i) & 1;\n                if (cur.children[bit] == null) cur.children[bit] = new Node();\n                cur = cur.children[bit];\n            }\n        }\n        int maxXor = 0;\n        for (int num : nums) {\n            Node cur = root;\n            int curXor = 0;\n            for (int i = 31; i >= 0; i--) {\n                int bit = (num >> i) & 1;\n                int opposite = 1 - bit;\n                if (cur.children[opposite] != null) {\n                    curXor |= (1 << i);\n                    cur = cur.children[opposite];\n                } else {\n                    cur = cur.children[bit];\n                }\n            }\n            maxXor = Math.max(maxXor, curXor);\n        }\n        return maxXor;\n    }\n}",
                "python": "class Solution:\n    def findMaximumXOR(self, nums: list[int]) -> int:\n        max_xor = 0\n        mask = 0\n        for i in range(31, -1, -1):\n            mask |= (1 << i)\n            prefixes = {num & mask for num in nums}\n            candidate = max_xor | (1 << i)\n            if any(candidate ^ p in prefixes for p in prefixes):\n                max_xor = candidate\n        return max_xor"
            }
        }
    },
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
                "java": "import java.util.*;\npublic class LFUCache {\n    private int capacity, minFreq = 0;\n    private Map<Integer, Node> keyMap = new HashMap<>();\n    private Map<Integer, DLList> freqMap = new HashMap<>();\n    static class Node {\n        int key, val, freq = 1;\n        Node prev, next;\n        Node(int k, int v) { key = k; val = v; }\n    }\n    static class DLList {\n        Node head = new Node(0, 0), tail = new Node(0, 0);\n        int size = 0;\n        DLList() { head.next = tail; tail.prev = head; }\n        void add(Node n) { n.next = head.next; n.prev = head; head.next.prev = n; head.next = n; size++; }\n        void remove(Node n) { n.prev.next = n.next; n.next.prev = n.prev; size--; }\n        Node popTail() { if (size == 0) return null; Node n = tail.prev; remove(n); return n; }\n    }\n    public LFUCache(int capacity) { this.capacity = capacity; }\n    public int get(int key) {\n        Node n = keyMap.get(key);\n        if (n == null) return -1;\n        update(n);\n        return n.val;\n    }\n    public void put(int key, int value) {\n        if (capacity == 0) return;\n        Node n = keyMap.get(key);\n        if (n != null) {\n            n.val = value;\n            update(n);\n        } else {\n            if (keyMap.size() == capacity) {\n                DLList minList = freqMap.get(minFreq);\n                Node toRemove = minList.popTail();\n                keyMap.remove(toRemove.key);\n            }\n            Node newNode = new Node(key, value);\n            keyMap.put(key, newNode);\n            minFreq = 1;\n            freqMap.computeIfAbsent(1, k -> new DLList()).add(newNode);\n        }\n    }\n    private void update(Node n) {\n        DLList oldList = freqMap.get(n.freq);\n        oldList.remove(n);\n        if (n.freq == minFreq && oldList.size == 0) minFreq++;\n        n.freq++;\n        freqMap.computeIfAbsent(n.freq, k -> new DLList()).add(n);\n    }\n}",
                "python": "from collections import defaultdict\n\nclass Node:\n    def __init__(self, key, val):\n        self.key = key\n        self.val = val\n        self.freq = 1\n        self.prev = self.next = None\n\nclass DLinkedList:\n    def __init__(self):\n        self.head, self.tail = Node(0, 0), Node(0, 0)\n        self.head.next, self.tail.prev = self.tail, self.head\n        self.size = 0\n    def add(self, node):\n        node.next, node.prev = self.head.next, self.head\n        self.head.next.prev = node\n        self.head.next = node\n        self.size += 1\n    def remove(self, node):\n        node.prev.next, node.next.prev = node.next, node.prev\n        self.size -= 1\n    def pop_tail(self):\n        if self.size == 0: return None\n        node = self.tail.prev\n        self.remove(node)\n        return node\n\nclass LFUCache:\n    def __init__(self, capacity: int):\n        self.cap = capacity\n        self.min_freq = 0\n        self.key_map = {}\n        self.freq_map = defaultdict(DLinkedList)\n\n    def _update(self, node):\n        old_list = self.freq_map[node.freq]\n        old_list.remove(node)\n        if node.freq == self.min_freq and old_list.size == 0:\n            self.min_freq += 1\n        node.freq += 1\n        self.freq_map[node.freq].add(node)\n\n    def get(self, key: int) -> int:\n        if key not in self.key_map: return -1\n        node = self.key_map[key]\n        self._update(node)\n        return node.val\n\n    def put(self, key: int, value: int) -> None:\n        if self.cap == 0: return\n        if key in self.key_map:\n            node = self.key_map[key]\n            node.val = value\n            self._update(node)\n        else:\n            if len(self.key_map) == self.cap:\n                removed = self.freq_map[self.min_freq].pop_tail()\n                del self.key_map[removed.key]\n            new_node = Node(key, value)\n            self.key_map[key] = new_node\n            self.min_freq = 1\n            self.freq_map[1].add(new_node)"
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
                "java": "import java.util.*;\npublic class LFUCache {\n    private int capacity, minFreq = 0;\n    private Map<Integer, Node> keyMap = new HashMap<>();\n    private Map<Integer, DLList> freqMap = new HashMap<>();\n    static class Node {\n        int key, val, freq = 1;\n        Node prev, next;\n        Node(int k, int v) { key = k; val = v; }\n    }\n    static class DLList {\n        Node head = new Node(0, 0), tail = new Node(0, 0);\n        int size = 0;\n        DLList() { head.next = tail; tail.prev = head; }\n        void add(Node n) { n.next = head.next; n.prev = head; head.next.prev = n; head.next = n; size++; }\n        void remove(Node n) { n.prev.next = n.next; n.next.prev = n.prev; size--; }\n        Node popTail() { if (size == 0) return null; Node n = tail.prev; remove(n); return n; }\n    }\n    public LFUCache(int capacity) { this.capacity = capacity; }\n    public int get(int key) {\n        Node n = keyMap.get(key);\n        if (n == null) return -1;\n        update(n);\n        return n.val;\n    }\n    public void put(int key, int value) {\n        if (capacity == 0) return;\n        Node n = keyMap.get(key);\n        if (n != null) {\n            n.val = value;\n            update(n);\n        } else {\n            if (keyMap.size() == capacity) {\n                DLList minList = freqMap.get(minFreq);\n                Node toRemove = minList.popTail();\n                keyMap.remove(toRemove.key);\n            }\n            Node newNode = new Node(key, value);\n            keyMap.put(key, newNode);\n            minFreq = 1;\n            freqMap.computeIfAbsent(1, k -> new DLList()).add(newNode);\n        }\n    }\n    private void update(Node n) {\n        DLList oldList = freqMap.get(n.freq);\n        oldList.remove(n);\n        if (n.freq == minFreq && oldList.size == 0) minFreq++;\n        n.freq++;\n        freqMap.computeIfAbsent(n.freq, k -> new DLList()).add(n);\n    }\n}",
                "python": "from collections import defaultdict\n\nclass Node:\n    def __init__(self, key, val):\n        self.key = key\n        self.val = val\n        self.freq = 1\n        self.prev = self.next = None\n\nclass DLinkedList:\n    def __init__(self):\n        self.head, self.tail = Node(0, 0), Node(0, 0)\n        self.head.next, self.tail.prev = self.tail, self.head\n        self.size = 0\n    def add(self, node):\n        node.next, node.prev = self.head.next, self.head\n        self.head.next.prev = node\n        self.head.next = node\n        self.size += 1\n    def remove(self, node):\n        node.prev.next, node.next.prev = node.next, node.prev\n        self.size -= 1\n    def pop_tail(self):\n        if self.size == 0: return None\n        node = self.tail.prev\n        self.remove(node)\n        return node\n\nclass LFUCache:\n    def __init__(self, capacity: int):\n        self.cap = capacity\n        self.min_freq = 0\n        self.key_map = {}\n        self.freq_map = defaultdict(DLinkedList)\n\n    def _update(self, node):\n        old_list = self.freq_map[node.freq]\n        old_list.remove(node)\n        if node.freq == self.min_freq and old_list.size == 0:\n            self.min_freq += 1\n        node.freq += 1\n        self.freq_map[node.freq].add(node)\n\n    def get(self, key: int) -> int:\n        if key not in self.key_map:\n            return -1\n        node = self.key_map[key]\n        self._update(node)\n        return node.val\n\n    def put(self, key: int, value: int) -> None:\n        if self.cap == 0:\n            return\n        if key in self.key_map:\n            node = self.key_map[key]\n            node.val = value\n            self._update(node)\n        else:\n            if len(self.key_map) == self.cap:\n                removed = self.freq_map[self.min_freq].pop_tail()\n                del self.key_map[removed.key]\n            new_node = Node(key, value)\n            self.key_map[key] = new_node\n            self.min_freq = 1\n            self.freq_map[1].add(new_node)"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public int singleNumber(int[] nums) {\n        Set<Integer> set = new HashSet<>();\n        for (int x : nums) {\n            if (!set.add(x)) set.remove(x);\n        }\n        return set.iterator().next();\n    }\n}",
                "python": "class Solution:\n    def singleNumber(self, nums: list[int]) -> int:\n        s = set()\n        for x in nums:\n            if x in s: s.remove(x)\n            else: s.add(x)\n        return s.pop()"
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
                "java": "class Solution {\n    public int singleNumber(int[] nums) {\n        int ans = 0;\n        for (int x : nums) ans ^= x;\n        return ans;\n    }\n}",
                "python": "class Solution:\n    def singleNumber(self, nums: list[int]) -> int:\n        ans = 0\n        for x in nums:\n            ans ^= x\n        return ans"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public int singleNumber(int[] nums) {\n        Map<Integer, Integer> counts = new HashMap<>();\n        for (int x : nums) counts.put(x, counts.getOrDefault(x, 0) + 1);\n        for (int k : counts.keySet()) if (counts.get(k) == 1) return k;\n        return 0;\n    }\n}",
                "python": "from collections import Counter\n\nclass Solution:\n    def singleNumber(self, nums: list[int]) -> int:\n        c = Counter(nums)\n        for k, v in c.items():\n            if v == 1: return k\n        return 0"
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
                "java": "class Solution {\n    public int singleNumber(int[] nums) {\n        int ones = 0, twos = 0;\n        for (int x : nums) {\n            ones = (ones ^ x) & ~twos;\n            twos = (twos ^ x) & ~ones;\n        }\n        return ones;\n    }\n}",
                "python": "class Solution:\n    def singleNumber(self, nums: list[int]) -> int:\n        ones = twos = 0\n        for x in nums:\n            ones = (ones ^ x) & ~twos\n            twos = (twos ^ x) & ~ones\n        return ones"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public int[] singleNumber(int[] nums) {\n        Set<Integer> set = new HashSet<>();\n        for (int x : nums) {\n            if (!set.add(x)) set.remove(x);\n        }\n        int[] res = new int[2];\n        int i = 0;\n        for (int v : set) res[i++] = v;\n        return res;\n    }\n}",
                "python": "class Solution:\n    def singleNumber(self, nums: list[int]) -> list[int]:\n        s = set()\n        for x in nums:\n            if x in s: s.remove(x)\n            else: s.add(x)\n        return list(s)"
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
                "java": "class Solution {\n    public int[] singleNumber(int[] nums) {\n        int diff = 0;\n        for (int x : nums) diff ^= x;\n        diff &= -diff;\n        int[] res = new int[2];\n        for (int x : nums) {\n            if ((x & diff) == 0) {\n                res[0] ^= x;\n            } else {\n                res[1] ^= x;\n            }\n        }\n        return res;\n    }\n}",
                "python": "class Solution:\n    def singleNumber(self, nums: list[int]) -> list[int]:\n        diff = 0\n        for x in nums:\n            diff ^= x\n        diff &= -diff\n        a = b = 0\n        for x in nums:\n            if x & diff:\n                a ^= x\n            else:\n                b ^= x\n        return [a, b]"
            }
        }
    },
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
                "java": "class Solution {\n    public int hammingWeight(int n) {\n        int count = 0;\n        for (int i = 0; i < 32; i++) {\n            if (((n >> i) & 1) == 1) count++;\n        }\n        return count;\n    }\n}",
                "python": "class Solution:\n    def hammingWeight(self, n: int) -> int:\n        return bin(n).count('1')"
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
                "java": "class Solution {\n    public int hammingWeight(int n) {\n        int count = 0;\n        while (n != 0) {\n            n &= (n - 1);\n            count++;\n        }\n        return count;\n    }\n}",
                "python": "class Solution:\n    def hammingWeight(self, n: int) -> int:\n        count = 0\n        while n:\n            n &= n - 1\n            count += 1\n        return count"
            }
        }
    },
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
                "java": "class Solution {\n    public int[] countBits(int n) {\n        int[] ans = new int[n + 1];\n        for (int i = 0; i <= n; i++) ans[i] = Integer.bitCount(i);\n        return ans;\n    }\n}",
                "python": "class Solution:\n    def countBits(self, n: int) -> list[int]:\n        return [bin(i).count('1') for i in range(n + 1)]"
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
                "java": "class Solution {\n    public int[] countBits(int n) {\n        int[] ans = new int[n + 1];\n        for (int i = 1; i <= n; i++) {\n            ans[i] = ans[i >> 1] + (i & 1);\n        }\n        return ans;\n    }\n}",
                "python": "class Solution:\n    def countBits(self, n: int) -> list[int]:\n        ans = [0] * (n + 1)\n        for i in range(1, n + 1):\n            ans[i] = ans[i >> 1] + (i & 1)\n        return ans"
            }
        }
    },
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
                "java": "class Solution {\n    public boolean isPowerOfTwo(int n) {\n        if (n <= 0) return false;\n        while (n % 2 == 0) n /= 2;\n        return n == 1;\n    }\n}",
                "python": "class Solution:\n    def isPowerOfTwo(self, n: int) -> bool:\n        if n <= 0: return False\n        while n % 2 == 0: n //= 2\n        return n == 1"
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
                "java": "class Solution {\n    public boolean isPowerOfTwo(int n) {\n        return n > 0 && (n & (n - 1)) == 0;\n    }\n}",
                "python": "class Solution:\n    def isPowerOfTwo(self, n: int) -> bool:\n        return n > 0 and (n & (n - 1)) == 0"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public int missingNumber(int[] nums) {\n        Arrays.sort(nums);\n        for (int i = 0; i < nums.length; i++) {\n            if (nums[i] != i) return i;\n        }\n        return nums.length;\n    }\n}",
                "python": "class Solution:\n    def missingNumber(self, nums: list[int]) -> int:\n        nums.sort()\n        for i, x in enumerate(nums):\n            if i != x: return i\n        return len(nums)"
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
                "java": "class Solution {\n    public int missingNumber(int[] nums) {\n        int n = nums.length;\n        int expected = n * (n + 1) / 2;\n        int sum = 0;\n        for (int x : nums) sum += x;\n        return expected - sum;\n    }\n}",
                "python": "class Solution:\n    def missingNumber(self, nums: list[int]) -> int:\n        n = len(nums)\n        return n * (n + 1) // 2 - sum(nums)"
            }
        }
    },
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
                "java": "class Solution {\n    public int reverseBits(int n) {\n        int res = 0;\n        for (int i = 0; i < 32; i++) {\n            res = (res << 1) | (n & 1);\n            n >>>= 1;\n        }\n        return res;\n    }\n}",
                "python": "class Solution:\n    def reverseBits(self, n: int) -> int:\n        res = 0\n        for _ in range(32):\n            res = (res << 1) | (n & 1)\n            n >>= 1\n        return res"
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
                "java": "class Solution {\n    public int reverseBits(int n) {\n        int res = 0;\n        for (int i = 0; i < 32; i++) {\n            res = (res << 1) | (n & 1);\n            n >>>= 1;\n        }\n        return res;\n    }\n}",
                "python": "class Solution:\n    def reverseBits(self, n: int) -> int:\n        res = 0\n        for _ in range(32):\n            res = (res << 1) | (n & 1)\n            n >>= 1\n        return res"
            }
        }
    },
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
                "java": "class Solution {\n    public int getSum(int a, int b) {\n        while (b != 0) {\n            int carry = (a & b) << 1;\n            a = a ^ b;\n            b = carry;\n        }\n        return a;\n    }\n}",
                "python": "class Solution:\n    def getSum(self, a: int, b: int) -> int:\n        mask = 0xFFFFFFFF\n        while b & mask != 0:\n            carry = (a & b) << 1\n            a = a ^ b\n            b = carry\n        return (a & mask) if b > 0 else a"
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
                "java": "class Solution {\n    public int getSum(int a, int b) {\n        while (b != 0) {\n            int carry = (a & b) << 1;\n            a = a ^ b;\n            b = carry;\n        }\n        return a;\n    }\n}",
                "python": "class Solution:\n    def getSum(self, a: int, b: int) -> int:\n        mask = 0xFFFFFFFF\n        max_int = 0x7FFFFFFF\n        while (b & mask) != 0:\n            carry = (a & b) << 1\n            a = (a ^ b) & mask\n            b = carry & mask\n        return a if a <= max_int else ~(a ^ mask)"
            }
        }
    },
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
                "java": "class Solution {\n    public int reverse(int x) {\n        long rev = 0;\n        while (x != 0) {\n            rev = rev * 10 + x % 10;\n            x /= 10;\n        }\n        if (rev > Integer.MAX_VALUE || rev < Integer.MIN_VALUE) return 0;\n        return (int) rev;\n    }\n}",
                "python": "class Solution:\n    def reverse(self, x: int) -> int:\n        sign = -1 if x < 0 else 1\n        x = abs(x)\n        rev = int(str(x)[::-1]) * sign\n        return rev if -2**31 <= rev <= 2**31 - 1 else 0"
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
                "java": "class Solution {\n    public int reverse(int x) {\n        int rev = 0;\n        while (x != 0) {\n            int pop = x % 10;\n            x /= 10;\n            if (rev > Integer.MAX_VALUE / 10 || (rev == Integer.MAX_VALUE / 10 && pop > 7)) return 0;\n            if (rev < Integer.MIN_VALUE / 10 || (rev == Integer.MIN_VALUE / 10 && pop < -8)) return 0;\n            rev = rev * 10 + pop;\n        }\n        return rev;\n    }\n}",
                "python": "class Solution:\n    def reverse(self, x: int) -> int:\n        rev = 0\n        sign = -1 if x < 0 else 1\n        x = abs(x)\n        while x:\n            pop = x % 10\n            x //= 10\n            rev = rev * 10 + pop\n        rev *= sign\n        return rev if -2**31 <= rev <= 2**31 - 1 else 0"
            }
        }
    },
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
                "java": "class Solution {\n    public boolean isPalindrome(int x) {\n        if (x < 0) return false;\n        String s = String.valueOf(x);\n        int l = 0, r = s.length() - 1;\n        while (l < r) {\n            if (s.charAt(l++) != s.charAt(r--)) return false;\n        }\n        return true;\n    }\n}",
                "python": "class Solution:\n    def isPalindrome(self, x: int) -> bool:\n        if x < 0: return False\n        s = str(x)\n        return s == s[::-1]"
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
                "java": "class Solution {\n    public boolean isPalindrome(int x) {\n        if (x < 0 || (x % 10 == 0 && x != 0)) return false;\n        int rev = 0;\n        while (x > rev) {\n            rev = rev * 10 + x % 10;\n            x /= 10;\n        }\n        return x == rev || x == rev / 10;\n    }\n}",
                "python": "class Solution:\n    def isPalindrome(self, x: int) -> bool:\n        if x < 0 or (x % 10 == 0 and x != 0):\n            return False\n        rev = 0\n        while x > rev:\n            rev = rev * 10 + x % 10\n            x //= 10\n        return x == rev or x == rev // 10"
            }
        }
    },
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
                "java": "import java.util.*;\nclass Solution {\n    public boolean isHappy(int n) {\n        Set<Integer> seen = new HashSet<>();\n        while (n != 1 && !seen.contains(n)) {\n            seen.add(n);\n            n = getNext(n);\n        }\n        return n == 1;\n    }\n    private int getNext(int n) {\n        int sum = 0;\n        while (n > 0) {\n            int d = n % 10;\n            sum += d * d;\n            n /= 10;\n        }\n        return sum;\n    }\n}",
                "python": "class Solution:\n    def isHappy(self, n: int) -> bool:\n        seen = set()\n        while n != 1 and n not in seen:\n            seen.add(n)\n            n = sum(int(d)**2 for d in str(n))\n        return n == 1"
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
                "java": "class Solution {\n    public boolean isHappy(int n) {\n        int slow = n, fast = getNext(n);\n        while (fast != 1 && slow != fast) {\n            slow = getNext(slow);\n            fast = getNext(getNext(fast));\n        }\n        return fast == 1;\n    }\n    private int getNext(int n) {\n        int total = 0;\n        while (n > 0) {\n            int d = n % 10;\n            total += d * d;\n            n /= 10;\n        }\n        return total;\n    }\n}",
                "python": "class Solution:\n    def isHappy(self, n: int) -> bool:\n        def get_next(val):\n            total = 0\n            while val > 0:\n                d = val % 10\n                total += d * d\n                val //= 10\n            return total\n        slow = n\n        fast = get_next(n)\n        while fast != 1 and slow != fast:\n            slow = get_next(slow)\n            fast = get_next(get_next(fast))\n        return fast == 1"
            }
        }
    },
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
                "java": "class Solution {\n    public int countPrimes(int n) {\n        int count = 0;\n        for (int i = 2; i < n; i++) {\n            if (isPrime(i)) count++;\n        }\n        return count;\n    }\n    private boolean isPrime(int x) {\n        for (int i = 2; i * i <= x; i++) {\n            if (x % i == 0) return false;\n        }\n        return true;\n    }\n}",
                "python": "class Solution:\n    def countPrimes(self, n: int) -> int:\n        def is_prime(x):\n            i = 2\n            while i * i <= x:\n                if x % i == 0: return False\n                i += 1\n            return True\n        return sum(1 for i in range(2, n) if is_prime(i))"
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
                "java": "class Solution {\n    public int countPrimes(int n) {\n        if (n <= 2) return 0;\n        boolean[] notPrime = new boolean[n];\n        for (int i = 2; i * i < n; i++) {\n            if (!notPrime[i]) {\n                for (int j = i * i; j < n; j += i) {\n                    notPrime[j] = true;\n                }\n            }\n        }\n        int count = 0;\n        for (int i = 2; i < n; i++) {\n            if (!notPrime[i]) count++;\n        }\n        return count;\n    }\n}",
                "python": "class Solution:\n    def countPrimes(self, n: int) -> int:\n        if n <= 2:\n            return 0\n        not_prime = [False] * n\n        i = 2\n        while i * i < n:\n            if not not_prime[i]:\n                for j in range(i * i, n, i):\n                    not_prime[j] = True\n            i += 1\n        return sum(1 for x in range(2, n) if not not_prime[x])"
            }
        }
    },
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
                "java": "import java.math.BigInteger;\nclass Solution {\n    public int trailingZeroes(int n) {\n        BigInteger fact = BigInteger.ONE;\n        for (int i = 2; i <= n; i++) fact = fact.multiply(BigInteger.valueOf(i));\n        int count = 0;\n        while (fact.mod(BigInteger.TEN).equals(BigInteger.ZERO)) {\n            count++;\n            fact = fact.divide(BigInteger.TEN);\n        }\n        return count;\n    }\n}",
                "python": "class Solution:\n    def trailingZeroes(self, n: int) -> int:\n        import math\n        fact = math.factorial(n)\n        s = str(fact)\n        return len(s) - len(s.rstrip('0'))"
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
                "java": "class Solution {\n    public int trailingZeroes(int n) {\n        int count = 0;\n        while (n >= 5) {\n            count += n / 5;\n            n /= 5;\n        }\n        return count;\n    }\n}",
                "python": "class Solution:\n    def trailingZeroes(self, n: int) -> int:\n        count = 0\n        while n >= 5:\n            count += n // 5\n            n //= 5\n        return count"
            }
        }
    }
]

# Batch 7: Questions 151 to 175

def get_batch():
    return [
    {
        "seq": 151,
        "whyNext": "Builds on BST insertion: 3 cases when deleting a node (leaf, one child, two children replaced by inorder successor).",
        "brute": {
            "idea": "Perform inorder traversal into list, remove key, and rebuild balanced BST from remaining elements.",
            "steps": [
                "Inorder traversal collecting all values except key.",
                "Reconstruct balanced BST from sorted array."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "whySlow": "Allocates array and rebuilds whole tree instead of rewiring pointers at deletion site in O(h).",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public TreeNode deleteNode(TreeNode root, int key) {\n        List<Integer> list = new ArrayList<>();\n        inorder(root, key, list);\n        return build(list, 0, list.size() - 1);\n    }\n    private void inorder(TreeNode node, int key, List<Integer> list) {\n        if (node == null) return;\n        inorder(node.left, key, list);\n        if (node.val != key) list.add(node.val);\n        inorder(node.right, key, list);\n    }\n    private TreeNode build(List<Integer> list, int l, int r) {\n        if (l > r) return null;\n        int m = l + (r - l) / 2;\n        TreeNode node = new TreeNode(list.get(m));\n        node.left = build(list, l, m - 1);\n        node.right = build(list, m + 1, r);\n        return node;\n    }\n}",
                "python": "class Solution:\n    def deleteNode(self, root: TreeNode | None, key: int) -> TreeNode | None:\n        vals = []\n        def inorder(node):\n            if not node: return\n            inorder(node.left)\n            if node.val != key: vals.append(node.val)\n            inorder(node.right)\n        inorder(root)\n        def build(l, r):\n            if l > r: return None\n            m = (l + r) // 2\n            node = TreeNode(vals[m])\n            node.left = build(l, m - 1)\n            node.right = build(m + 1, r)\n            return node\n        return build(0, len(vals) - 1)"
            }
        },
        "optimal": {
            "idea": "Recursive BST deletion: search key; if node has 2 children, replace val with min of right subtree and delete successor.",
            "steps": [
                "If root == null return null.",
                "If key < root.val, root.left = deleteNode(root.left, key).",
                "Else if key > root.val, root.right = deleteNode(root.right, key).",
                "Else: if left is null return right; if right is null return left.",
                "Find min in right subtree, copy val to root.val, root.right = deleteNode(root.right, root.val)."
            ],
            "time": "O(h)",
            "space": "O(h)",
            "code": {
                "java": "class Solution {\n    public TreeNode deleteNode(TreeNode root, int key) {\n        if (root == null) return null;\n        if (key < root.val) {\n            root.left = deleteNode(root.left, key);\n        } else if (key > root.val) {\n            root.right = deleteNode(root.right, key);\n        } else {\n            if (root.left == null) return root.right;\n            if (root.right == null) return root.left;\n            TreeNode successor = root.right;\n            while (successor.left != null) successor = successor.left;\n            root.val = successor.val;\n            root.right = deleteNode(root.right, successor.val);\n        }\n        return root;\n    }\n}",
                "python": "class Solution:\n    def deleteNode(self, root: TreeNode | None, key: int) -> TreeNode | None:\n        if not root:\n            return None\n        if key < root.val:\n            root.left = self.deleteNode(root.left, key)\n        elif key > root.val:\n            root.right = self.deleteNode(root.right, key)\n        else:\n            if not root.left: return root.right\n            if not root.right: return root.left\n            succ = root.right\n            while succ.left:\n                succ = succ.left\n            root.val = succ.val\n            root.right = self.deleteNode(root.right, succ.val)\n        return root"
            }
        }
    },
    {
        "seq": 152,
        "whyNext": "Inorder traversal of BST yields sorted values in ascending order: kth visited node is kth smallest.",
        "brute": {
            "idea": "Full inorder traversal into an ArrayList, then return element at index k - 1.",
            "steps": [
                "Run recursive inorder traversal collecting all values.",
                "Return list.get(k - 1)."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "whySlow": "Stores all n elements in memory instead of stopping at the kth node.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int kthSmallest(TreeNode root, int k) {\n        List<Integer> list = new ArrayList<>();\n        inorder(root, list);\n        return list.get(k - 1);\n    }\n    private void inorder(TreeNode node, List<Integer> list) {\n        if (node == null) return;\n        inorder(node.left, list);\n        list.add(node.val);\n        inorder(node.right, list);\n    }\n}",
                "python": "class Solution:\n    def kthSmallest(self, root: TreeNode | None, k: int) -> int:\n        vals = []\n        def inorder(node):\n            if not node: return\n            inorder(node.left)\n            vals.append(node.val)\n            inorder(node.right)\n        inorder(root)\n        return vals[k - 1]"
            }
        },
        "optimal": {
            "idea": "Iterative inorder with stack: stop and return immediately as soon as k nodes have been popped.",
            "steps": [
                "Maintain explicit stack and cur pointer starting at root.",
                "Push all left descendants.",
                "Pop node, decrement k.",
                "If k == 0, return node.val.",
                "Move cur = node.right."
            ],
            "time": "O(h + k)",
            "space": "O(h)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int kthSmallest(TreeNode root, int k) {\n        Deque<TreeNode> stack = new ArrayDeque<>();\n        TreeNode cur = root;\n        while (cur != null || !stack.isEmpty()) {\n            while (cur != null) {\n                stack.push(cur);\n                cur = cur.left;\n            }\n            cur = stack.pop();\n            if (--k == 0) return cur.val;\n            cur = cur.right;\n        }\n        return -1;\n    }\n}",
                "python": "class Solution:\n    def kthSmallest(self, root: TreeNode | None, k: int) -> int:\n        stack = []\n        cur = root\n        while cur or stack:\n            while cur:\n                stack.append(cur)\n                cur = cur.left\n            cur = stack.pop()\n            k -= 1\n            if k == 0:\n                return cur.val\n            cur = cur.right\n        return -1"
            }
        }
    },
    {
        "seq": 153,
        "whyNext": "Builds on LCA of general tree: BST property allows choosing left or right child in O(1) without visiting both.",
        "brute": {
            "idea": "Use general binary tree LCA algorithm ignoring BST value comparisons.",
            "steps": [
                "Recurse left and right.",
                "Return root if left and right both non-null."
            ],
            "time": "O(n)",
            "space": "O(h)",
            "whySlow": "Visits both subtrees instead of pruning half the tree at each step using BST ordering.",
            "code": {
                "java": "class Solution {\n    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {\n        if (root == null || root == p || root == q) return root;\n        TreeNode left = lowestCommonAncestor(root.left, p, q);\n        TreeNode right = lowestCommonAncestor(root.right, p, q);\n        if (left != null && right != null) return root;\n        return left != null ? left : right;\n    }\n}",
                "python": "class Solution:\n    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:\n        if not root or root == p or root == q:\n            return root\n        left = self.lowestCommonAncestor(root.left, p, q)\n        right = self.lowestCommonAncestor(root.right, p, q)\n        if left and right: return root\n        return left if left else right"
            }
        },
        "optimal": {
            "idea": "Iterative BST walk: if both p and q < cur.val go left; if both > cur.val go right; otherwise cur is the split point (LCA).",
            "steps": [
                "While cur != null:",
                "If p.val < cur.val && q.val < cur.val: cur = cur.left.",
                "Else if p.val > cur.val && q.val > cur.val: cur = cur.right.",
                "Else: return cur (split point)."
            ],
            "time": "O(h)",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {\n        TreeNode cur = root;\n        while (cur != null) {\n            if (p.val < cur.val && q.val < cur.val) {\n                cur = cur.left;\n            } else if (p.val > cur.val && q.val > cur.val) {\n                cur = cur.right;\n            } else {\n                return cur;\n            }\n        }\n        return null;\n    }\n}",
                "python": "class Solution:\n    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:\n        cur = root\n        while cur:\n            if p.val < cur.val and q.val < cur.val:\n                cur = cur.left\n            elif p.val > cur.val and q.val > cur.val:\n                cur = cur.right\n            else:\n                return cur\n        return None"
            }
        }
    },
    {
        "seq": 154,
        "whyNext": "Divide and conquer BST construction: picking midpoint as root guarantees height-balanced subtrees (|h_L - h_R| <= 1).",
        "brute": {
            "idea": "Sequentially insert elements one-by-one from left to right into a BST using insertIntoBST.",
            "steps": [
                "Start with empty tree.",
                "For each number in sorted array, insert into BST."
            ],
            "time": "O(n^2)",
            "space": "O(n)",
            "whySlow": "Inserting sorted elements sequentially into standard BST results in a degenerate linked list of depth n.",
            "code": {
                "java": "class Solution {\n    public TreeNode sortedArrayToBST(int[] nums) {\n        return build(nums, 0, nums.length - 1);\n    }\n    private TreeNode build(int[] nums, int l, int r) {\n        if (l > r) return null;\n        int m = l + (r - l) / 2;\n        TreeNode node = new TreeNode(nums[m]);\n        node.left = build(nums, l, m - 1);\n        node.right = build(nums, m + 1, r);\n        return node;\n    }\n}",
                "python": "class Solution:\n    def sortedArrayToBST(self, nums: list[int]) -> TreeNode | None:\n        def build(l, r):\n            if l > r: return None\n            m = (l + r) // 2\n            node = TreeNode(nums[m])\n            node.left = build(l, m - 1)\n            node.right = build(m + 1, r)\n            return node\n        return build(0, len(nums) - 1)"
            }
        },
        "optimal": {
            "idea": "Binary search divide-and-conquer: mid = (l + r) / 2 is root, left subarray builds left subtree, right subarray builds right subtree.",
            "steps": [
                "Define helper build(nums, left, right).",
                "Base case: if left > right return null.",
                "mid = left + (right - left) / 2.",
                "root = new TreeNode(nums[mid]).",
                "root.left = build(nums, left, mid - 1); root.right = build(nums, mid + 1, right).",
                "Return root."
            ],
            "time": "O(n)",
            "space": "O(log n)",
            "code": {
                "java": "class Solution {\n    public TreeNode sortedArrayToBST(int[] nums) {\n        return build(nums, 0, nums.length - 1);\n    }\n    private TreeNode build(int[] nums, int left, int right) {\n        if (left > right) return null;\n        int mid = left + (right - left) / 2;\n        TreeNode root = new TreeNode(nums[mid]);\n        root.left = build(nums, left, mid - 1);\n        root.right = build(nums, mid + 1, right);\n        return root;\n    }\n}",
                "python": "class Solution:\n    def sortedArrayToBST(self, nums: list[int]) -> TreeNode | None:\n        def build(left: int, right: int) -> TreeNode | None:\n            if left > right:\n                return None\n            mid = (left + right) // 2\n            root = TreeNode(nums[mid])\n            root.left = build(left, mid - 1)\n            root.right = build(mid + 1, right)\n            return root\n        return build(0, len(nums) - 1)"
            }
        }
    },
    {
        "seq": 155,
        "whyNext": "Lazy evaluation of BST inorder traversal: controlled stack yields next() in O(1) amortized and O(h) space.",
        "brute": {
            "idea": "Flatten entire BST into a list during constructor; next() reads index pointer.",
            "steps": [
                "In constructor, run full inorder traversal into ArrayList.",
                "Maintain idx pointer; next() increments idx; hasNext() checks idx < size."
            ],
            "time": "O(n) constructor, O(1) calls",
            "space": "O(n)",
            "whySlow": "Eagerly traverses and stores all n elements in memory instead of lazy O(h) space.",
            "code": {
                "java": "import java.util.*;\npublic class BSTIterator {\n    private List<Integer> list = new ArrayList<>();\n    private int idx = 0;\n    public BSTIterator(TreeNode root) {\n        inorder(root);\n    }\n    private void inorder(TreeNode node) {\n        if (node == null) return;\n        inorder(node.left);\n        list.add(node.val);\n        inorder(node.right);\n    }\n    public int next() {\n        return list.get(idx++);\n    }\n    public boolean hasNext() {\n        return idx < list.size();\n    }\n}",
                "python": "class BSTIterator:\n    def __init__(self, root: TreeNode | None):\n        self.vals = []\n        self.idx = 0\n        def inorder(node):\n            if not node: return\n            inorder(node.left)\n            self.vals.append(node.val)\n            inorder(node.right)\n        inorder(root)\n\n    def next(self) -> int:\n        val = self.vals[self.idx]\n        self.idx += 1\n        return val\n\n    def hasNext(self) -> bool:\n        return self.idx < len(self.vals)"
            }
        },
        "optimal": {
            "idea": "Controlled stack simulation of inorder traversal: pushLeft on constructor and on right child in next().",
            "steps": [
                "Maintain stack of TreeNodes.",
                "Helper pushLeft(node): while node != null, stack.push(node), node = node.left.",
                "constructor: call pushLeft(root).",
                "next(): pop node, pushLeft(node.right), return node.val.",
                "hasNext(): return !stack.isEmpty()."
            ],
            "time": "O(1) amortized next, O(1) hasNext",
            "space": "O(h)",
            "code": {
                "java": "import java.util.*;\npublic class BSTIterator {\n    private Deque<TreeNode> stack = new ArrayDeque<>();\n    public BSTIterator(TreeNode root) {\n        pushLeft(root);\n    }\n    public int next() {\n        TreeNode node = stack.pop();\n        if (node.right != null) {\n            pushLeft(node.right);\n        }\n        return node.val;\n    }\n    public boolean hasNext() {\n        return !stack.isEmpty();\n    }\n    private void pushLeft(TreeNode node) {\n        while (node != null) {\n            stack.push(node);\n            node = node.left;\n        }\n    }\n}",
                "python": "class BSTIterator:\n    def __init__(self, root: TreeNode | None):\n        self.stack = []\n        self._push_left(root)\n\n    def _push_left(self, node: TreeNode | None):\n        while node:\n            self.stack.append(node)\n            node = node.left\n\n    def next(self) -> int:\n        node = self.stack.pop()\n        if node.right:\n            self._push_left(node.right)\n        return node.val\n\n    def hasNext(self) -> bool:\n        return len(self.stack) > 0"
            }
        }
    },
    {
        "seq": 156,
        "whyNext": "Two swapped nodes in BST create 1 or 2 inversions during inorder traversal; identify first and second swapped nodes.",
        "brute": {
            "idea": "Inorder traversal to collect all nodes into a list; sort values and reassign back to nodes.",
            "steps": [
                "Collect all nodes in inorder list.",
                "Extract values, sort them.",
                "Assign sorted values back to nodes in order."
            ],
            "time": "O(n log n)",
            "space": "O(n)",
            "whySlow": "Allocates lists and sorts values instead of finding the 2 inverted pointers directly in O(1) space.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public void recoverTree(TreeNode root) {\n        List<TreeNode> nodes = new ArrayList<>();\n        List<Integer> vals = new ArrayList<>();\n        inorder(root, nodes, vals);\n        Collections.sort(vals);\n        for (int i = 0; i < nodes.size(); i++) {\n            nodes.get(i).val = vals.get(i);\n        }\n    }\n    private void inorder(TreeNode node, List<TreeNode> nodes, List<Integer> vals) {\n        if (node == null) return;\n        inorder(node.left, nodes, vals);\n        nodes.add(node);\n        vals.add(node.val);\n        inorder(node.right, nodes, vals);\n    }\n}",
                "python": "class Solution:\n    def recoverTree(self, root: TreeNode | None) -> None:\n        nodes = []\n        vals = []\n        def inorder(node):\n            if not node: return\n            inorder(node.left)\n            nodes.append(node)\n            vals.append(node.val)\n            inorder(node.right)\n        inorder(root)\n        vals.sort()\n        for node, val in zip(nodes, vals):\n            node.val = val"
            }
        },
        "optimal": {
            "idea": "Inorder traversal tracking prev node: first anomaly is when prev.val > cur.val (record first = prev, second = cur); subsequent anomaly updates second = cur.",
            "steps": [
                "Track TreeNode first = null, second = null, prev = null.",
                "During inorder DFS: if prev != null && prev.val > cur.val:",
                "If first == null, first = prev; second = cur.",
                "After traversal, swap values: int temp = first.val; first.val = second.val; second.val = temp."
            ],
            "time": "O(n)",
            "space": "O(h)",
            "code": {
                "java": "class Solution {\n    private TreeNode first = null;\n    private TreeNode second = null;\n    private TreeNode prev = null;\n    public void recoverTree(TreeNode root) {\n        inorder(root);\n        int temp = first.val;\n        first.val = second.val;\n        second.val = temp;\n    }\n    private void inorder(TreeNode node) {\n        if (node == null) return;\n        inorder(node.left);\n        if (prev != null && prev.val > node.val) {\n            if (first == null) first = prev;\n            second = node;\n        }\n        prev = node;\n        inorder(node.right);\n    }\n}",
                "python": "class Solution:\n    def recoverTree(self, root: TreeNode | None) -> None:\n        first = second = prev = None\n        def inorder(node: TreeNode | None):\n            nonlocal first, second, prev\n            if not node:\n                return\n            inorder(node.left)\n            if prev and prev.val > node.val:\n                if not first:\n                    first = prev\n                second = node\n            prev = node\n            inorder(node.right)\n        inorder(root)\n        first.val, second.val = second.val, first.val"
            }
        }
    },
    {
        "seq": 157,
        "whyNext": "Entry to Chapter 10 (Heaps): min-heap of fixed capacity k maintains the k largest numbers; root is the kth largest.",
        "brute": {
            "idea": "Store all numbers in a list, append new val, sort descending, and return index k - 1.",
            "steps": [
                "Add new val to ArrayList.",
                "Sort list.",
                "Return element at k - 1."
            ],
            "time": "O(m * log m) per add",
            "space": "O(m)",
            "whySlow": "Sorting the growing stream on every addition wastes work.",
            "code": {
                "java": "import java.util.*;\npublic class KthLargest {\n    private List<Integer> list = new ArrayList<>();\n    private int k;\n    public KthLargest(int k, int[] nums) {\n        this.k = k;\n        for (int x : nums) list.add(x);\n    }\n    public int add(int val) {\n        list.add(val);\n        Collections.sort(list, Collections.reverseOrder());\n        return list.get(k - 1);\n    }\n}",
                "python": "class KthLargest:\n    def __init__(self, k: int, nums: list[int]):\n        self.k = k\n        self.nums = sorted(nums, reverse=True)\n\n    def add(self, val: int) -> int:\n        self.nums.append(val)\n        self.nums.sort(reverse=True)\n        return self.nums[self.k - 1]"
            }
        },
        "optimal": {
            "idea": "Min-heap of size k: add(val) pushes to heap; if heap.size() > k, pop min; peek() is the kth largest.",
            "steps": [
                "Maintain PriorityQueue<Integer> of size k.",
                "In add(val): heap.offer(val); if heap.size() > k heap.poll().",
                "Return heap.peek()."
            ],
            "time": "O(log k) per add",
            "space": "O(k)",
            "code": {
                "java": "import java.util.*;\npublic class KthLargest {\n    private PriorityQueue<Integer> minHeap = new PriorityQueue<>();\n    private int k;\n    public KthLargest(int k, int[] nums) {\n        this.k = k;\n        for (int x : nums) add(x);\n    }\n    public int add(int val) {\n        minHeap.offer(val);\n        if (minHeap.size() > k) {\n            minHeap.poll();\n        }\n        return minHeap.peek();\n    }\n}",
                "python": "import heapq\n\nclass KthLargest:\n    def __init__(self, k: int, nums: list[int]):\n        self.k = k\n        self.heap = []\n        for x in nums:\n            self.add(x)\n\n    def add(self, val: int) -> int:\n        heapq.heappush(self.heap, val)\n        if len(self.heap) > self.k:\n            heapq.heappop(self.heap)\n        return self.heap[0]"
            }
        }
    },
    {
        "seq": 158,
        "whyNext": "Builds on Min-Heap stream vs Quickselect: finding kth largest without full array sorting in O(n) average.",
        "brute": {
            "idea": "Sort entire array in ascending order and return element at index n - k.",
            "steps": [
                "Sort array using Arrays.sort().",
                "Return nums[nums.length - k]."
            ],
            "time": "O(n log n)",
            "space": "O(1)",
            "whySlow": "Sorts the entire array when only the k-th rank is requested.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int findKthLargest(int[] nums, int k) {\n        Arrays.sort(nums);\n        return nums[nums.length - k];\n    }\n}",
                "python": "class Solution:\n    def findKthLargest(self, nums: list[int], k: int) -> int:\n        nums.sort()\n        return nums[len(nums) - k]"
            }
        },
        "optimal": {
            "idea": "Quickselect with random pivot: partition around pivot; narrow search to the half containing target index n - k.",
            "steps": [
                "Target index target = nums.length - k.",
                "While left <= right: pick random pivot, partition nums into <= pivot and > pivot.",
                "If pivotIndex == target, return nums[pivotIndex].",
                "Else if pivotIndex < target, left = pivotIndex + 1; else right = pivotIndex - 1."
            ],
            "time": "O(n) average, O(n^2) worst case",
            "space": "O(1)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int findKthLargest(int[] nums, int k) {\n        int target = nums.length - k;\n        int l = 0, r = nums.length - 1;\n        Random rand = new Random();\n        while (l <= r) {\n            int pIdx = l + rand.nextInt(r - l + 1);\n            int newP = partition(nums, l, r, pIdx);\n            if (newP == target) return nums[newP];\n            else if (newP < target) l = newP + 1;\n            else r = newP - 1;\n        }\n        return nums[l];\n    }\n    private int partition(int[] nums, int l, int r, int pIdx) {\n        int pivot = nums[pIdx];\n        swap(nums, pIdx, r);\n        int store = l;\n        for (int i = l; i < r; i++) {\n            if (nums[i] < pivot) {\n                swap(nums, store++, i);\n            }\n        }\n        swap(nums, store, r);\n        return store;\n    }\n    private void swap(int[] nums, int i, int j) {\n        int temp = nums[i]; nums[i] = nums[j]; nums[j] = temp;\n    }\n}",
                "python": "import random\n\nclass Solution:\n    def findKthLargest(self, nums: list[int], k: int) -> int:\n        target = len(nums) - k\n        l, r = 0, len(nums) - 1\n        while l <= r:\n            p_idx = random.randint(l, r)\n            pivot = nums[p_idx]\n            nums[p_idx], nums[r] = nums[r], nums[p_idx]\n            store = l\n            for i in range(l, r):\n                if nums[i] < pivot:\n                    nums[store], nums[i] = nums[i], nums[store]\n                    store += 1\n            nums[store], nums[r] = nums[r], nums[store]\n            if store == target:\n                return nums[store]\n            elif store < target:\n                l = store + 1\n            else:\n                r = store - 1\n        return nums[l]"
            }
        }
    },
    {
        "seq": 159,
        "whyNext": "Max-heap simulation: repeatedly smash the two largest stones until at most 1 stone remains.",
        "brute": {
            "idea": "In each step, sort the list to extract the two largest elements, smash them, and insert the difference.",
            "steps": [
                "While list size > 1:",
                "Sort list ascending, pop last two elements y and x.",
                "If y > x, reinsert y - x.",
                "Return remaining element or 0."
            ],
            "time": "O(n^2 log n)",
            "space": "O(n)",
            "whySlow": "Sorting the entire list after every smash is unnecessarily quadratic.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int lastStoneWeight(int[] stones) {\n        List<Integer> list = new ArrayList<>();\n        for (int s : stones) list.add(s);\n        while (list.size() > 1) {\n            Collections.sort(list);\n            int y = list.remove(list.size() - 1);\n            int x = list.remove(list.size() - 1);\n            if (y > x) list.add(y - x);\n        }\n        return list.isEmpty() ? 0 : list.get(0);\n    }\n}",
                "python": "class Solution:\n    def lastStoneWeight(self, stones: list[int]) -> int:\n        while len(stones) > 1:\n            stones.sort()\n            y = stones.pop()\n            x = stones.pop()\n            if y > x:\n                stones.append(y - x)\n        return stones[0] if stones else 0"
            }
        },
        "optimal": {
            "idea": "Max-heap: poll two heaviest stones; if y > x, push y - x back. Return top or 0.",
            "steps": [
                "Insert all stones into max-heap (negated in Python, Collections.reverseOrder() in Java).",
                "While heap.size() > 1: y = poll(), x = poll(). If y > x offer(y - x).",
                "Return heap.isEmpty() ? 0 : heap.peek()."
            ],
            "time": "O(n log n)",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int lastStoneWeight(int[] stones) {\n        PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());\n        for (int s : stones) maxHeap.offer(s);\n        while (maxHeap.size() > 1) {\n            int y = maxHeap.poll();\n            int x = maxHeap.poll();\n            if (y > x) maxHeap.offer(y - x);\n        }\n        return maxHeap.isEmpty() ? 0 : maxHeap.peek();\n    }\n}",
                "python": "import heapq\n\nclass Solution:\n    def lastStoneWeight(self, stones: list[int]) -> int:\n        heap = [-s for s in stones]\n        heapq.heapify(heap)\n        while len(heap) > 1:\n            y = -heapq.heappop(heap)\n            x = -heapq.heappop(heap)\n            if y > x:\n                heapq.heappush(heap, -(y - x))\n        return -heap[0] if heap else 0"
            }
        }
    },
    {
        "seq": 160,
        "whyNext": "Max-heap of size k retains the k points with smallest Euclidean distance x^2 + y^2.",
        "brute": {
            "idea": "Sort all points by distance x^2 + y^2 and take first k points.",
            "steps": [
                "Sort points array with custom comparator: (x1^2 + y1^2) - (x2^2 + y2^2).",
                "Copy first k elements."
            ],
            "time": "O(n log n)",
            "space": "O(k)",
            "whySlow": "Sorts all n points when only k are needed.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int[][] kClosest(int[][] points, int k) {\n        Arrays.sort(points, (a, b) -> (a[0]*a[0] + a[1]*a[1]) - (b[0]*b[0] + b[1]*b[1]));\n        return Arrays.copyOfRange(points, 0, k);\n    }\n}",
                "python": "class Solution:\n    def kClosest(self, points: list[list[int]], k: int) -> list[list[int]]:\n        points.sort(key=lambda p: p[0]**2 + p[1]**2)\n        return points[:k]"
            }
        },
        "optimal": {
            "idea": "Max-heap of size k: evict largest distance when size exceeds k to retain k closest points in O(n log k).",
            "steps": [
                "Max-heap comparing distances (b[0]^2 + b[1]^2) - (a[0]^2 + a[1]^2).",
                "Iterate through points: push to heap; if heap.size() > k poll().",
                "Extract all k points from heap."
            ],
            "time": "O(n log k)",
            "space": "O(k)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int[][] kClosest(int[][] points, int k) {\n        PriorityQueue<int[]> maxHeap = new PriorityQueue<>((a, b) ->\n            (b[0] * b[0] + b[1] * b[1]) - (a[0] * a[0] + a[1] * a[1])\n        );\n        for (int[] p : points) {\n            maxHeap.offer(p);\n            if (maxHeap.size() > k) {\n                maxHeap.poll();\n            }\n        }\n        int[][] res = new int[k][2];\n        for (int i = 0; i < k; i++) {\n            res[i] = maxHeap.poll();\n        }\n        return res;\n    }\n}",
                "python": "import heapq\n\nclass Solution:\n    def kClosest(self, points: list[list[int]], k: int) -> list[list[int]]:\n        heap = []\n        for x, y in points:\n            dist = -(x * x + y * y)\n            if len(heap) < k:\n                heapq.heappush(heap, (dist, [x, y]))\n            else:\n                heapq.heappushpop(heap, (dist, [x, y]))\n        return [p for _, p in heap]"
            }
        }
    },
    {
        "seq": 161,
        "whyNext": "Builds on Top K Frequent Elements: tie-breaking with lexicographical order (higher count first; alphabetical for equal counts).",
        "brute": {
            "idea": "Count frequencies with HashMap; sort unique words with custom comparator and take top k.",
            "steps": [
                "Count frequencies in Map<String, Integer>.",
                "Sort keys: primary by frequency descending, secondary by word lexicographically.",
                "Return first k words."
            ],
            "time": "O(m log m) where m is unique words",
            "space": "O(m)",
            "whySlow": "Sorts all unique words instead of maintaining only k words in a priority queue.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<String> topKFrequent(String[] words, int k) {\n        Map<String, Integer> count = new HashMap<>();\n        for (String w : words) count.put(w, count.getOrDefault(w, 0) + 1);\n        List<String> list = new ArrayList<>(count.keySet());\n        list.sort((a, b) -> {\n            int fa = count.get(a), fb = count.get(b);\n            if (fa != fb) return fb - fa;\n            return a.compareTo(b);\n        });\n        return list.subList(0, k);\n    }\n}",
                "python": "from collections import Counter\n\nclass Solution:\n    def topKFrequent(self, words: list[str], k: int) -> list[str]:\n        count = Counter(words)\n        unique = list(count.keys())\n        unique.sort(key=lambda w: (-count[w], w))\n        return unique[:k]"
            }
        },
        "optimal": {
            "idea": "Min-heap of size k: min-heap evicts lowest frequency; for equal frequency evicts lexicographically larger word.",
            "steps": [
                "Count frequencies in HashMap.",
                "Min-heap with comparator: if freq differs, compare counts ascending; if equal, reverse lexicographical (b.compareTo(a)).",
                "Iterate unique words: push; if size > k, poll().",
                "Drain heap and reverse list."
            ],
            "time": "O(n log k)",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<String> topKFrequent(String[] words, int k) {\n        Map<String, Integer> counts = new HashMap<>();\n        for (String w : words) counts.put(w, counts.getOrDefault(w, 0) + 1);\n        PriorityQueue<String> minHeap = new PriorityQueue<>((a, b) -> {\n            int fa = counts.get(a), fb = counts.get(b);\n            if (fa != fb) return fa - fb;\n            return b.compareTo(a);\n        });\n        for (String w : counts.keySet()) {\n            minHeap.offer(w);\n            if (minHeap.size() > k) minHeap.poll();\n        }\n        List<String> res = new ArrayList<>();\n        while (!minHeap.isEmpty()) res.add(minHeap.poll());\n        Collections.reverse(res);\n        return res;\n    }\n}",
                "python": "import heapq\nfrom collections import Counter\n\nclass Solution:\n    def topKFrequent(self, words: list[str], k: int) -> list[str]:\n        counts = Counter(words)\n        class Item:\n            def __init__(self, word, count):\n                self.word = word\n                self.count = count\n            def __lt__(self, other):\n                if self.count != other.count:\n                    return self.count < other.count\n                return self.word > other.word\n        heap = []\n        for word, cnt in counts.items():\n            heapq.heappush(heap, Item(word, cnt))\n            if len(heap) > k:\n                heapq.heappop(heap)\n        res = []\n        while heap:\n            res.append(heapq.heappop(heap).word)\n        return res[::-1]"
            }
        }
    },
    {
        "seq": 162,
        "whyNext": "Bucket sort on character frequencies: group characters by frequency count 1..n to sort in O(n) linear time.",
        "brute": {
            "idea": "Count frequencies with map; sort characters using comparator and rebuild string.",
            "steps": [
                "Map frequencies of each character.",
                "Sort distinct characters by frequency descending.",
                "Replicate character freq times."
            ],
            "time": "O(n + k log k)",
            "space": "O(n)",
            "whySlow": "Sorting distinct characters takes extra comparison overhead compared to direct bucket indexing.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public String frequencySort(String s) {\n        Map<Character, Integer> counts = new HashMap<>();\n        for (char c : s.toCharArray()) counts.put(c, counts.getOrDefault(c, 0) + 1);\n        List<Character> list = new ArrayList<>(counts.keySet());\n        list.sort((a, b) -> counts.get(b) - counts.get(a));\n        StringBuilder sb = new StringBuilder();\n        for (char c : list) {\n            int cnt = counts.get(c);\n            for (int i = 0; i < cnt; i++) sb.append(c);\n        }\n        return sb.toString();\n    }\n}",
                "python": "from collections import Counter\n\nclass Solution:\n    def frequencySort(self, s: str) -> str:\n        count = Counter(s)\n        return \"\".join(c * cnt for c, cnt in count.most_common())"
            }
        },
        "optimal": {
            "idea": "Bucket Sort: create List<Character>[] buckets of size n + 1. Append characters backwards from index n down to 1.",
            "steps": [
                "Count frequencies of each character.",
                "Place each character into buckets[frequency].",
                "Iterate buckets from high to low frequency, appending char * freq."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public String frequencySort(String s) {\n        Map<Character, Integer> counts = new HashMap<>();\n        for (char c : s.toCharArray()) counts.put(c, counts.getOrDefault(c, 0) + 1);\n        List<Character>[] buckets = new List[s.length() + 1];\n        for (char c : counts.keySet()) {\n            int freq = counts.get(c);\n            if (buckets[freq] == null) buckets[freq] = new ArrayList<>();\n            buckets[freq].add(c);\n        }\n        StringBuilder sb = new StringBuilder();\n        for (int i = buckets.length - 1; i >= 1; i--) {\n            if (buckets[i] != null) {\n                for (char c : buckets[i]) {\n                    for (int j = 0; j < i; j++) sb.append(c);\n                }\n            }\n        }\n        return sb.toString();\n    }\n}",
                "python": "from collections import Counter\n\nclass Solution:\n    def frequencySort(self, s: str) -> str:\n        counts = Counter(s)\n        buckets = [[] for _ in range(len(s) + 1)]\n        for c, freq in counts.items():\n            buckets[freq].append(c)\n        res = []\n        for freq in range(len(s), 0, -1):\n            for c in buckets[freq]:\n                res.append(c * freq)\n        return \"\".join(res)"
            }
        }
    },
    {
        "seq": 163,
        "whyNext": "Greedy slot scheduling: the most frequent task creates (maxFreq - 1) frames of size (n + 1).",
        "brute": {
            "idea": "Simulate clock cycles using max-heap of ready tasks and a cooling cooldown queue.",
            "steps": [
                "Count frequencies in max-heap.",
                "At each second: pop most frequent task, execute it, push to cooling queue with readyTime = curTime + n.",
                "Check cooling queue and push ready tasks back into max-heap."
            ],
            "time": "O(total_time * log 26)",
            "space": "O(26)",
            "whySlow": "Simulates cycle-by-cycle up to total_time instead of computing answer mathematically in O(1).",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int leastInterval(char[] tasks, int n) {\n        int[] counts = new int[26];\n        for (char t : tasks) counts[t - 'A']++;\n        PriorityQueue<Integer> pq = new PriorityQueue<>(Collections.reverseOrder());\n        for (int c : counts) if (c > 0) pq.offer(c);\n        Queue<int[]> queue = new LinkedList<>();\n        int time = 0;\n        while (!pq.isEmpty() || !queue.isEmpty()) {\n            time++;\n            if (!pq.isEmpty()) {\n                int rem = pq.poll() - 1;\n                if (rem > 0) queue.offer(new int[]{rem, time + n});\n            }\n            if (!queue.isEmpty() && queue.peek()[1] == time) {\n                pq.offer(queue.poll()[0]);\n            }\n        }\n        return time;\n    }\n}",
                "python": "from collections import Counter, deque\nimport heapq\n\nclass Solution:\n    def leastInterval(self, tasks: list[str], n: int) -> int:\n        counts = Counter(tasks)\n        max_heap = [-cnt for cnt in counts.values()]\n        heapq.heapify(max_heap)\n        q = deque()\n        time = 0\n        while max_heap or q:\n            time += 1\n            if max_heap:\n                cnt = 1 + heapq.heappop(max_heap)\n                if cnt != 0:\n                    q.append((cnt, time + n))\n            if q and q[0][1] == time:\n                heapq.heappush(max_heap, q.popleft()[0])\n        return time"
            }
        },
        "optimal": {
            "idea": "Math formula: (maxCount - 1) * (n + 1) + maxCountTasks; answer is max(formula, tasks.length).",
            "steps": [
                "Find maximum task frequency maxCount.",
                "Count how many tasks share this maximum frequency (maxCountTasks).",
                "Answer is max(tasks.length, (maxCount - 1) * (n + 1) + maxCountTasks)."
            ],
            "time": "O(N)",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public int leastInterval(char[] tasks, int n) {\n        int[] counts = new int[26];\n        int maxCount = 0;\n        for (char t : tasks) {\n            counts[t - 'A']++;\n            maxCount = Math.max(maxCount, counts[t - 'A']);\n        }\n        int maxCountTasks = 0;\n        for (int c : counts) {\n            if (c == maxCount) maxCountTasks++;\n        }\n        int emptySlots = (maxCount - 1) * (n + 1) + maxCountTasks;\n        return Math.max(tasks.length, emptySlots);\n    }\n}",
                "python": "from collections import Counter\n\nclass Solution:\n    def leastInterval(self, tasks: list[str], n: int) -> int:\n        counts = Counter(tasks)\n        max_count = max(counts.values())\n        max_count_tasks = sum(1 for c in counts.values() if c == max_count)\n        return max(len(tasks), (max_count - 1) * (n + 1) + max_count_tasks)"
            }
        }
    },
    {
        "seq": 164,
        "whyNext": "Builds on Task Scheduler: no adjacent characters can be equal; place most frequent character at even indices first.",
        "brute": {
            "idea": "Max-heap greedily placing the most frequent available character that is not equal to previous character.",
            "steps": [
                "Max-heap of (char, count).",
                "Pop most frequent. If matches previous, pop second most frequent.",
                "Push back remaining counts."
            ],
            "time": "O(n log 26)",
            "space": "O(26)",
            "whySlow": "Heap pushes and pops per character instead of direct even/odd index placement in O(n).",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public String reorganizeString(String s) {\n        int[] counts = new int[26];\n        for (char c : s.toCharArray()) counts[c - 'a']++;\n        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> b[1] - a[1]);\n        for (int i = 0; i < 26; i++) {\n            if (counts[i] > 0) pq.offer(new int[]{i, counts[i]});\n        }\n        StringBuilder sb = new StringBuilder();\n        int[] prev = null;\n        while (!pq.isEmpty()) {\n            int[] cur = pq.poll();\n            sb.append((char) ('a' + cur[0]));\n            cur[1]--;\n            if (prev != null && prev[1] > 0) pq.offer(prev);\n            prev = cur;\n        }\n        return sb.length() == s.length() ? sb.toString() : \"\";\n    }\n}",
                "python": "import heapq\nfrom collections import Counter\n\nclass Solution:\n    def reorganizeString(self, s: str) -> str:\n        counts = Counter(s)\n        heap = [(-cnt, c) for c, cnt in counts.items()]\n        heapq.heapify(heap)\n        res = []\n        prev = None\n        while heap:\n            cnt, c = heapq.heappop(heap)\n            res.append(c)\n            if prev:\n                heapq.heappush(heap, prev)\n                prev = None\n            if -cnt > 1:\n                prev = (cnt + 1, c)\n        ans = \"\".join(res)\n        return ans if len(ans) == len(s) else \"\" "
            }
        },
        "optimal": {
            "idea": "Place characters at even indices 0, 2, 4... then odd indices 1, 3, 5... If maxCount > (n + 1)/2 return ''.",
            "steps": [
                "Find max count character. If maxCount > (n + 1) / 2 return empty string.",
                "Fill even indices with most frequent character.",
                "Fill remaining even then odd indices with other characters."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "code": {
                "java": "class Solution {\n    public String reorganizeString(String s) {\n        int[] counts = new int[26];\n        int maxCount = 0, letter = 0;\n        for (char c : s.toCharArray()) {\n            int code = c - 'a';\n            counts[code]++;\n            if (counts[code] > maxCount) {\n                maxCount = counts[code];\n                letter = code;\n            }\n        }\n        if (maxCount > (s.length() + 1) / 2) return \"\";\n        char[] res = new char[s.length()];\n        int idx = 0;\n        while (counts[letter] > 0) {\n            res[idx] = (char) ('a' + letter);\n            idx += 2;\n            counts[letter]--;\n        }\n        for (int i = 0; i < 26; i++) {\n            while (counts[i] > 0) {\n                if (idx >= res.length) idx = 1;\n                res[idx] = (char) ('a' + i);\n                idx += 2;\n                counts[i]--;\n            }\n        }\n        return new String(res);\n    }\n}",
                "python": "from collections import Counter\n\nclass Solution:\n    def reorganizeString(self, s: str) -> str:\n        counts = Counter(s)\n        max_c, max_cnt = counts.most_common(1)[0]\n        if max_cnt > (len(s) + 1) // 2:\n            return \"\"\n        res = [''] * len(s)\n        idx = 0\n        for _ in range(max_cnt):\n            res[idx] = max_c\n            idx += 2\n        del counts[max_c]\n        for c, cnt in counts.items():\n            for _ in range(cnt):\n                if idx >= len(s):\n                    idx = 1\n                res[idx] = c\n                idx += 2\n        return \"\".join(res)"
            }
        }
    },
    {
        "seq": 165,
        "whyNext": "Builds on Reorganize String: integer barcodes instead of characters; guaranteed always possible to arrange without adjacent duplicates.",
        "brute": {
            "idea": "Max-heap simulation picking most frequent barcode different from previous.",
            "steps": [
                "Max-heap of (freq, barcode).",
                "Pick most frequent not equal to last placed element.",
                "Insert back into heap."
            ],
            "time": "O(n log n)",
            "space": "O(n)",
            "whySlow": "Heap operations take logarithmic time per element compared to interleaved indexing.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int[] rearrangeBarcodes(int[] barcodes) {\n        Map<Integer, Integer> map = new HashMap<>();\n        for (int b : barcodes) map.put(b, map.getOrDefault(b, 0) + 1);\n        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> b[1] - a[1]);\n        for (int k : map.keySet()) pq.offer(new int[]{k, map.get(k)});\n        int[] res = new int[barcodes.length];\n        int idx = 0;\n        int[] prev = null;\n        while (!pq.isEmpty()) {\n            int[] cur = pq.poll();\n            res[idx++] = cur[0];\n            cur[1]--;\n            if (prev != null && prev[1] > 0) pq.offer(prev);\n            prev = cur;\n        }\n        return res;\n    }\n}",
                "python": "import heapq\nfrom collections import Counter\n\nclass Solution:\n    def rearrangeBarcodes(self, barcodes: list[int]) -> list[int]:\n        counts = Counter(barcodes)\n        heap = [(-cnt, b) for b, cnt in counts.items()]\n        heapq.heapify(heap)\n        res = []\n        prev = None\n        while heap:\n            cnt, b = heapq.heappop(heap)\n            res.append(b)\n            if prev:\n                heapq.heappush(heap, prev)\n                prev = None\n            if -cnt > 1:\n                prev = (cnt + 1, b)\n        return res"
            }
        },
        "optimal": {
            "idea": "Interleaved placement: sort barcodes by frequency descending, fill even indices 0, 2, 4... then odd indices 1, 3, 5...",
            "steps": [
                "Count barcode frequencies.",
                "Order barcodes by frequency descending.",
                "Place elements across even indices first, then wrap around to odd indices."
            ],
            "time": "O(n log unique)",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int[] rearrangeBarcodes(int[] barcodes) {\n        Map<Integer, Integer> counts = new HashMap<>();\n        for (int b : barcodes) counts.put(b, counts.getOrDefault(b, 0) + 1);\n        List<Integer> keys = new ArrayList<>(counts.keySet());\n        keys.sort((a, b) -> counts.get(b) - counts.get(a));\n        int[] res = new int[barcodes.length];\n        int idx = 0;\n        for (int k : keys) {\n            int freq = counts.get(k);\n            while (freq-- > 0) {\n                if (idx >= res.length) idx = 1;\n                res[idx] = k;\n                idx += 2;\n            }\n        }\n        return res;\n    }\n}",
                "python": "from collections import Counter\n\nclass Solution:\n    def rearrangeBarcodes(self, barcodes: list[int]) -> list[int]:\n        counts = Counter(barcodes)\n        sorted_items = counts.most_common()\n        res = [0] * len(barcodes)\n        idx = 0\n        for b, cnt in sorted_items:\n            for _ in range(cnt):\n                if idx >= len(barcodes):\n                    idx = 1\n                res[idx] = b\n                idx += 2\n        return res"
            }
        }
    },
    {
        "seq": 166,
        "whyNext": "Two-heap pattern: max-heap holds smaller half, min-heap holds larger half; sizes balanced within 1 element difference.",
        "brute": {
            "idea": "Store numbers in sorted list via binary insertion; median is middle element(s).",
            "steps": [
                "addNum(num): insert using binary search (bisect.insort in Python).",
                "findMedian(): middle element if odd, average of two middle elements if even."
            ],
            "time": "O(n) per addNum",
            "space": "O(n)",
            "whySlow": "Array shifting on insertion takes linear time per number.",
            "code": {
                "java": "import java.util.*;\npublic class MedianFinder {\n    private List<Integer> list = new ArrayList<>();\n    public MedianFinder() {}\n    public void addNum(int num) {\n        int idx = Collections.binarySearch(list, num);\n        if (idx < 0) idx = -(idx + 1);\n        list.add(idx, num);\n    }\n    public double findMedian() {\n        int n = list.size();\n        if (n % 2 == 1) return list.get(n / 2);\n        return (list.get(n / 2 - 1) + list.get(n / 2)) / 2.0;\n    }\n}",
                "python": "import bisect\n\nclass MedianFinder:\n    def __init__(self):\n        self.nums = []\n\n    def addNum(self, num: int) -> None:\n        bisect.insort(self.nums, num)\n\n    def findMedian(self) -> float:\n        n = len(self.nums)\n        if n % 2 == 1:\n            return float(self.nums[n // 2])\n        return (self.nums[n // 2 - 1] + self.nums[n // 2]) / 2.0"
            }
        },
        "optimal": {
            "idea": "Dual-heap (small max-heap, large min-heap): keep max_heap.size == min_heap.size or max_heap.size == min_heap.size + 1.",
            "steps": [
                "Push num to maxHeap; pop maxHeap top and push to minHeap.",
                "If minHeap.size() > maxHeap.size(), balance back by moving minHeap top to maxHeap.",
                "findMedian: if maxHeap.size() > minHeap.size() return maxHeap.peek(); else return (maxHeap.peek() + minHeap.peek()) / 2.0."
            ],
            "time": "O(log n) addNum, O(1) findMedian",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\npublic class MedianFinder {\n    private PriorityQueue<Integer> small = new PriorityQueue<>(Collections.reverseOrder());\n    private PriorityQueue<Integer> large = new PriorityQueue<>();\n    public MedianFinder() {}\n    public void addNum(int num) {\n        small.offer(num);\n        large.offer(small.poll());\n        if (large.size() > small.size()) {\n            small.offer(large.poll());\n        }\n    }\n    public double findMedian() {\n        if (small.size() > large.size()) {\n            return small.peek();\n        }\n        return (small.peek() + large.peek()) / 2.0;\n    }\n}",
                "python": "import heapq\n\nclass MedianFinder:\n    def __init__(self):\n        self.small = []  # max-heap (negated)\n        self.large = []  # min-heap\n\n    def addNum(self, num: int) -> None:\n        heapq.heappush(self.small, -num)\n        heapq.heappush(self.large, -heapq.heappop(self.small))\n        if len(self.large) > len(self.small):\n            heapq.heappush(self.small, -heapq.heappop(self.large))\n\n    def findMedian(self) -> float:\n        if len(self.small) > len(self.large):\n            return float(-self.small[0])\n        return (-self.small[0] + self.large[0]) / 2.0"
            }
        }
    },
    {
        "seq": 167,
        "whyNext": "Matrix sorted row-wise and column-wise: binary search on value range [matrix[0][0], matrix[n-1][n-1]] with O(n) staircase counting.",
        "brute": {
            "idea": "Flatten matrix into 1D array, sort, and return element at index k - 1.",
            "steps": [
                "Flatten all n * n elements into array.",
                "Sort array.",
                "Return element at k - 1."
            ],
            "time": "O(n^2 log(n^2))",
            "space": "O(n^2)",
            "whySlow": "Flattens and sorts all elements ignoring the sorted row and column properties.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int kthSmallest(int[][] matrix, int k) {\n        int n = matrix.length;\n        int[] arr = new int[n * n];\n        int idx = 0;\n        for (int[] row : matrix) {\n            for (int v : row) arr[idx++] = v;\n        }\n        Arrays.sort(arr);\n        return arr[k - 1];\n    }\n}",
                "python": "class Solution:\n    def kthSmallest(self, matrix: list[list[int]], k: int) -> int:\n        arr = [v for row in matrix for v in row]\n        arr.sort()\n        return arr[k - 1]"
            }
        },
        "optimal": {
            "idea": "Binary search on answer range [min, max]: for mid, count elements <= mid in O(n) via staircase walk from bottom-left.",
            "steps": [
                "low = matrix[0][0], high = matrix[n-1][n-1].",
                "While low < high: mid = low + (high - low) / 2.",
                "countLessEqual(mid): start at row = n-1, col = 0; if val <= mid count += row + 1, col++; else row--.",
                "If count < k: low = mid + 1; else high = mid.",
                "Return low."
            ],
            "time": "O(n * log(max - min))",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public int kthSmallest(int[][] matrix, int k) {\n        int n = matrix.length;\n        int low = matrix[0][0], high = matrix[n - 1][n - 1];\n        while (low < high) {\n            int mid = low + (high - low) / 2;\n            if (countLessEqual(matrix, mid) < k) {\n                low = mid + 1;\n            } else {\n                high = mid;\n            }\n        }\n        return low;\n    }\n    private int countLessEqual(int[][] matrix, int target) {\n        int n = matrix.length;\n        int count = 0;\n        int r = n - 1, c = 0;\n        while (r >= 0 && c < n) {\n            if (matrix[r][c] <= target) {\n                count += (r + 1);\n                c++;\n            } else {\n                r--;\n            }\n        }\n        return count;\n    }\n}",
                "python": "class Solution:\n    def kthSmallest(self, matrix: list[list[int]], k: int) -> int:\n        n = len(matrix)\n        low, high = matrix[0][0], matrix[n - 1][n - 1]\n        def count_le(mid):\n            count = 0\n            r, c = n - 1, 0\n            while r >= 0 and c < n:\n                if matrix[r][c] <= mid:\n                    count += r + 1\n                    c += 1\n                else:\n                    r -= 1\n            return count\n        while low < high:\n            mid = (low + high) // 2\n            if count_le(mid) < k:\n                low = mid + 1\n            else:\n                high = mid\n        return low"
            }
        }
    },
    {
        "seq": 168,
        "whyNext": "Multi-way merge with Min-Heap: push initial pairs (nums1[i], nums2[0]); after popping (i, j), push (i, j + 1).",
        "brute": {
            "idea": "Generate all pairs nums1[i] + nums2[j], sort by sum, return first k pairs.",
            "steps": [
                "Generate all len(nums1) * len(nums2) pairs.",
                "Sort by sum ascending.",
                "Return first k."
            ],
            "time": "O(m * n * log(m * n))",
            "space": "O(m * n)",
            "whySlow": "Generates all m * n pairs when k is typically much smaller than m * n.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<List<Integer>> kSmallestPairs(int[] nums1, int[] nums2, int k) {\n        List<List<Integer>> all = new ArrayList<>();\n        for (int a : nums1) {\n            for (int b : nums2) {\n                all.add(Arrays.asList(a, b));\n            }\n        }\n        all.sort(Comparator.comparingInt(p -> p.get(0) + p.get(1)));\n        return all.subList(0, Math.min(k, all.size()));\n    }\n}",
                "python": "class Solution:\n    def kSmallestPairs(self, nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:\n        pairs = [[a, b] for a in nums1 for b in nums2]\n        pairs.sort(key=lambda p: p[0] + p[1])\n        return pairs[:k]"
            }
        },
        "optimal": {
            "idea": "Min-heap storing (sum, i, j): initialize with (nums1[i] + nums2[0], i, 0) for i in 0..min(k, len(nums1)); advance j -> j + 1.",
            "steps": [
                "Heap stores (nums1[i] + nums2[j], i, j).",
                "Push (nums1[i] + nums2[0], i, 0) for i from 0 to min(k, nums1.length) - 1.",
                "Loop up to k times: poll pair (i, j), add [nums1[i], nums2[j]] to res.",
                "If j + 1 < nums2.length, push (nums1[i] + nums2[j + 1], i, j + 1)."
            ],
            "time": "O(k log k)",
            "space": "O(k)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public List<List<Integer>> kSmallestPairs(int[] nums1, int[] nums2, int k) {\n        List<List<Integer>> res = new ArrayList<>();\n        if (nums1.length == 0 || nums2.length == 0 || k == 0) return res;\n        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[0]));\n        for (int i = 0; i < Math.min(k, nums1.length); i++) {\n            pq.offer(new int[]{nums1[i] + nums2[0], i, 0});\n        }\n        while (k-- > 0 && !pq.isEmpty()) {\n            int[] cur = pq.poll();\n            int i = cur[1], j = cur[2];\n            res.add(Arrays.asList(nums1[i], nums2[j]));\n            if (j + 1 < nums2.length) {\n                pq.offer(new int[]{nums1[i] + nums2[j + 1], i, j + 1});\n            }\n        }\n        return res;\n    }\n}",
                "python": "import heapq\n\nclass Solution:\n    def kSmallestPairs(self, nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:\n        if not nums1 or not nums2 or k == 0:\n            return []\n        heap = []\n        for i in range(min(k, len(nums1))):\n            heapq.heappush(heap, (nums1[i] + nums2[0], i, 0))\n        res = []\n        while heap and len(res) < k:\n            _, i, j = heapq.heappop(heap)\n            res.append([nums1[i], nums2[j]])\n            if j + 1 < len(nums2):\n                heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))\n        return res"
            }
        }
    },
    {
        "seq": 169,
        "whyNext": "Object-oriented design combining HashMaps (user followers, user tweet chains) with Min/Max-Heap k-way merge for news feed.",
        "brute": {
            "idea": "Store all posted tweets globally with timestamps; filter top 10 tweets posted by user or followees.",
            "steps": [
                "Append every tweet to global list.",
                "getNewsFeed: iterate global list backwards and filter matching user or followees."
            ],
            "time": "O(total_tweets) per getNewsFeed",
            "space": "O(total_tweets)",
            "whySlow": "Scans every tweet in the system linearly on every news feed query.",
            "code": {
                "java": "import java.util.*;\npublic class Twitter {\n    private List<int[]> allTweets = new ArrayList<>();\n    private Map<Integer, Set<Integer>> follows = new HashMap<>();\n    public Twitter() {}\n    public void postTweet(int userId, int tweetId) {\n        allTweets.add(new int[]{userId, tweetId});\n    }\n    public List<Integer> getNewsFeed(int userId) {\n        Set<Integer> validUsers = new HashSet<>(follows.getOrDefault(userId, new HashSet<>()));\n        validUsers.add(userId);\n        List<Integer> feed = new ArrayList<>();\n        for (int i = allTweets.size() - 1; i >= 0 && feed.size() < 10; i--) {\n            int[] t = allTweets.get(i);\n            if (validUsers.contains(t[0])) feed.add(t[1]);\n        }\n        return feed;\n    }\n    public void follow(int followerId, int followeeId) {\n        follows.computeIfAbsent(followerId, k -> new HashSet<>()).add(followeeId);\n    }\n    public void unfollow(int followerId, int followeeId) {\n        if (follows.containsKey(followerId)) follows.get(followerId).remove(followeeId);\n    }\n}",
                "python": "from collections import defaultdict\n\nclass Twitter:\n    def __init__(self):\n        self.tweets = []\n        self.follows = defaultdict(set)\n\n    def postTweet(self, userId: int, tweetId: int) -> None:\n        self.tweets.append((userId, tweetId))\n\n    def getNewsFeed(self, userId: int) -> list[int]:\n        valid = self.follows[userId] | {userId}\n        feed = []\n        for u, t in reversed(self.tweets):\n            if u in valid:\n                feed.append(t)\n                if len(feed) == 10:\n                    break\n        return feed\n\n    def follow(self, followerId: int, followeeId: int) -> None:\n        self.follows[followerId].add(followeeId)\n\n    def unfollow(self, followerId: int, followeeId: int) -> None:\n        self.follows[followerId].discard(followeeId)"
            }
        },
        "optimal": {
            "idea": "Per-user linked list of tweets + k-way merge (max-heap) of size 10 across followed users.",
            "steps": [
                "Global timestamp counter increments on each tweet.",
                "User has head Tweet node (tweetId, time, next).",
                "getNewsFeed: gather head of user and all followees into max-heap sorted by timestamp.",
                "Extract up to 10 latest tweets, advancing next pointers into heap."
            ],
            "time": "O(1) post/follow/unfollow, O(F log F) getNewsFeed",
            "space": "O(users + tweets)",
            "code": {
                "java": "import java.util.*;\npublic class Twitter {\n    private static int timestamp = 0;\n    private static class Tweet {\n        int id;\n        int time;\n        Tweet next;\n        Tweet(int id, int time) { this.id = id; this.time = time; }\n    }\n    private Map<Integer, Set<Integer>> follows = new HashMap<>();\n    private Map<Integer, Tweet> tweets = new HashMap<>();\n    public Twitter() {}\n    public void postTweet(int userId, int tweetId) {\n        Tweet t = new Tweet(tweetId, ++timestamp);\n        t.next = tweets.get(userId);\n        tweets.put(userId, t);\n    }\n    public List<Integer> getNewsFeed(int userId) {\n        Set<Integer> users = new HashSet<>(follows.getOrDefault(userId, new HashSet<>()));\n        users.add(userId);\n        PriorityQueue<Tweet> maxHeap = new PriorityQueue<>((a, b) -> b.time - a.time);\n        for (int u : users) {\n            Tweet t = tweets.get(u);\n            if (t != null) maxHeap.offer(t);\n        }\n        List<Integer> feed = new ArrayList<>();\n        while (!maxHeap.isEmpty() && feed.size() < 10) {\n            Tweet t = maxHeap.poll();\n            feed.add(t.id);\n            if (t.next != null) maxHeap.offer(t.next);\n        }\n        return feed;\n    }\n    public void follow(int followerId, int followeeId) {\n        follows.computeIfAbsent(followerId, k -> new HashSet<>()).add(followeeId);\n    }\n    public void unfollow(int followerId, int followeeId) {\n        if (follows.containsKey(followerId)) follows.get(followerId).remove(followeeId);\n    }\n}",
                "python": "import heapq\nfrom collections import defaultdict\n\nclass Twitter:\n    def __init__(self):\n        self.time = 0\n        self.tweets = defaultdict(list)\n        self.follows = defaultdict(set)\n\n    def postTweet(self, userId: int, tweetId: int) -> None:\n        self.time += 1\n        self.tweets[userId].append((self.time, tweetId))\n\n    def getNewsFeed(self, userId: int) -> list[int]:\n        users = self.follows[userId] | {userId}\n        heap = []\n        for u in users:\n            if self.tweets[u]:\n                idx = len(self.tweets[u]) - 1\n                t, tid = self.tweets[u][idx]\n                heapq.heappush(heap, (-t, tid, u, idx))\n        feed = []\n        while heap and len(feed) < 10:\n            neg_t, tid, u, idx = heapq.heappop(heap)\n            feed.append(tid)\n            if idx > 0:\n                nxt_t, nxt_tid = self.tweets[u][idx - 1]\n                heapq.heappush(heap, (-nxt_t, nxt_tid, u, idx - 1))\n        return feed\n\n    def follow(self, followerId: int, followeeId: int) -> None:\n        self.follows[followerId].add(followeeId)\n\n    def unfollow(self, followerId: int, followeeId: int) -> None:\n        self.follows[followerId].discard(followeeId)"
            }
        }
    },
    {
        "seq": 170,
        "whyNext": "Two-heap greedy strategy: sort projects by capital; push newly affordable projects into profit max-heap, greedily picking highest profit.",
        "brute": {
            "idea": "For each of the k rounds, scan all remaining projects to find the affordable project with maximum profit.",
            "steps": [
                "Track boolean used[] array.",
                "For round 1..k: find index i with used[i] == false, capital[i] <= w, maximizing profits[i].",
                "If no project affordable, break.",
                "w += profits[bestIndex], used[bestIndex] = true."
            ],
            "time": "O(k * n)",
            "space": "O(n)",
            "whySlow": "Scans all n projects k times in O(k * n).",
            "code": {
                "java": "class Solution {\n    public int findMaximizedCapital(int k, int w, int[] profits, int[] capital) {\n        int n = profits.length;\n        boolean[] used = new boolean[n];\n        for (int round = 0; round < k; round++) {\n            int bestIdx = -1;\n            for (int i = 0; i < n; i++) {\n                if (!used[i] && capital[i] <= w) {\n                    if (bestIdx == -1 || profits[i] > profits[bestIdx]) {\n                        bestIdx = i;\n                    }\n                }\n            }\n            if (bestIdx == -1) break;\n            used[bestIdx] = true;\n            w += profits[bestIdx];\n        }\n        return w;\n    }\n}",
                "python": "class Solution:\n    def findMaximizedCapital(self, k: int, w: int, profits: list[int], capital: list[int]) -> int:\n        n = len(profits)\n        used = [False] * n\n        for _ in range(k):\n            best = -1\n            for i in range(n):\n                if not used[i] and capital[i] <= w:\n                    if best == -1 or profits[i] > profits[best]:\n                        best = i\n            if best == -1: break\n            used[best] = True\n            w += profits[best]\n        return w"
            }
        },
        "optimal": {
            "idea": "Sort projects by capital; min-heap / pointer adds newly affordable projects into profit max-heap; greedily pick max profit.",
            "steps": [
                "Pair up projects (capital[i], profits[i]) and sort ascending by capital.",
                "Maintain maxHeap for profits of affordable projects.",
                "For k iterations: while pointer < n and projects[ptr].capital <= w, maxHeap.offer(projects[ptr].profit).",
                "If maxHeap is empty, break.",
                "w += maxHeap.poll()."
            ],
            "time": "O(n log n + k log n)",
            "space": "O(n)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int findMaximizedCapital(int k, int w, int[] profits, int[] capital) {\n        int n = profits.length;\n        int[][] projects = new int[n][2];\n        for (int i = 0; i < n; i++) {\n            projects[i][0] = capital[i];\n            projects[i][1] = profits[i];\n        }\n        Arrays.sort(projects, Comparator.comparingInt(a -> a[0]));\n        PriorityQueue<Integer> maxProfitHeap = new PriorityQueue<>(Collections.reverseOrder());\n        int ptr = 0;\n        for (int i = 0; i < k; i++) {\n            while (ptr < n && projects[ptr][0] <= w) {\n                maxProfitHeap.offer(projects[ptr][1]);\n                ptr++;\n            }\n            if (maxProfitHeap.isEmpty()) break;\n            w += maxProfitHeap.poll();\n        }\n        return w;\n    }\n}",
                "python": "import heapq\n\nclass Solution:\n    def findMaximizedCapital(self, k: int, w: int, profits: list[int], capital: list[int]) -> int:\n        projects = sorted(zip(capital, profits), key=lambda x: x[0])\n        n = len(projects)\n        max_profit_heap = []\n        ptr = 0\n        for _ in range(k):\n            while ptr < n and projects[ptr][0] <= w:\n                heapq.heappush(max_profit_heap, -projects[ptr][1])\n                ptr += 1\n            if not max_profit_heap:\n                break\n            w += -heapq.heappop(max_profit_heap)\n        return w"
            }
        }
    },
    {
        "seq": 171,
        "whyNext": "Entry to Chapter 11 (Greedy Algorithms): sort both greed factors and cookie sizes; satisfy least greedy child first.",
        "brute": {
            "idea": "For every child, iterate through all remaining cookies to find the smallest valid cookie.",
            "steps": [
                "Iterate through children.",
                "Search smallest unused cookie s[j] >= g[i].",
                "Mark cookie used."
            ],
            "time": "O(n * m)",
            "space": "O(m)",
            "whySlow": "Quadratic search across cookie array without sorting.",
            "code": {
                "java": "class Solution {\n    public int findContentChildren(int[] g, int[] s) {\n        boolean[] used = new boolean[s.length];\n        int content = 0;\n        for (int child : g) {\n            int bestIdx = -1;\n            for (int j = 0; j < s.length; j++) {\n                if (!used[j] && s[j] >= child) {\n                    if (bestIdx == -1 || s[j] < s[bestIdx]) {\n                        bestIdx = j;\n                    }\n                }\n            }\n            if (bestIdx != -1) {\n                used[bestIdx] = true;\n                content++;\n            }\n        }\n        return content;\n    }\n}",
                "python": "class Solution:\n    def findContentChildren(self, g: list[int], s: list[int]) -> int:\n        used = [False] * len(s)\n        ans = 0\n        for child in g:\n            best = -1\n            for j in range(len(s)):\n                if not used[j] and s[j] >= child:\n                    if best == -1 or s[j] < s[best]:\n                        best = j\n            if best != -1:\n                used[best] = True\n                ans += 1\n        return ans"
            }
        },
        "optimal": {
            "idea": "Sort both arrays: two pointers i and j. If s[j] >= g[i], satisfy child i++; always advance cookie j++.",
            "steps": [
                "Arrays.sort(g) and Arrays.sort(s).",
                "i = 0, j = 0.",
                "While i < g.length and j < s.length:",
                "If s[j] >= g[i], i++.",
                "j++.",
                "Return i."
            ],
            "time": "O(n log n + m log m)",
            "space": "O(1)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int findContentChildren(int[] g, int[] s) {\n        Arrays.sort(g);\n        Arrays.sort(s);\n        int i = 0, j = 0;\n        while (i < g.length && j < s.length) {\n            if (s[j] >= g[i]) {\n                i++;\n            }\n            j++;\n        }\n        return i;\n    }\n}",
                "python": "class Solution:\n    def findContentChildren(self, g: list[int], s: list[int]) -> int:\n        g.sort()\n        s.sort()\n        i = j = 0\n        while i < len(g) and j < len(s):\n            if s[j] >= g[i]:\n                i += 1\n            j += 1\n        return i"
            }
        }
    },
    {
        "seq": 172,
        "whyNext": "Greedy choice: for $20 bill, prefer giving change as $10 + $5 over three $5 bills (preserves flexible $5 bills).",
        "brute": {
            "idea": "Recursively explore change combinations for each transaction; backtrack if cannot make change.",
            "steps": [
                "Track list of available bills.",
                "For each customer, find subset of bills summing to bill - 5.",
                "Return true if all customers can be served."
            ],
            "time": "O(2^n)",
            "space": "O(n)",
            "whySlow": "Backtracking is unnecessary because greedy choice ($10 + $5 first) is strictly optimal.",
            "code": {
                "java": "class Solution {\n    public boolean lemonadeChange(int[] bills) {\n        int five = 0, ten = 0;\n        for (int b : bills) {\n            if (b == 5) five++;\n            else if (b == 10) {\n                if (five == 0) return false;\n                five--; ten++;\n            } else {\n                if (ten > 0 && five > 0) {\n                    ten--; five--;\n                } else if (five >= 3) {\n                    five -= 3;\n                } else {\n                    return false;\n                }\n            }\n        }\n        return true;\n    }\n}",
                "python": "class Solution:\n    def lemonadeChange(self, bills: list[int]) -> bool:\n        five = ten = 0\n        for b in bills:\n            if b == 5:\n                five += 1\n            elif b == 10:\n                if not five: return False\n                five -= 1\n                ten += 1\n            else:\n                if ten and five:\n                    ten -= 1\n                    five -= 1\n                elif five >= 3:\n                    five -= 3\n                else:\n                    return False\n        return True"
            }
        },
        "optimal": {
            "idea": "Track five and ten bill counts: for $5 increment five; for $10 give $5; for $20 prioritize $10 + $5, else three $5.",
            "steps": [
                "five = 0, ten = 0.",
                "For bill in bills:",
                "If bill == 5: five++.",
                "Else if bill == 10: if five == 0 return false; five--; ten++.",
                "Else: if ten > 0 && five > 0 { ten--; five--; } else if five >= 3 { five -= 3; } else return false.",
                "Return true."
            ],
            "time": "O(n)",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public boolean lemonadeChange(int[] bills) {\n        int five = 0, ten = 0;\n        for (int bill : bills) {\n            if (bill == 5) {\n                five++;\n            } else if (bill == 10) {\n                if (five == 0) return false;\n                five--;\n                ten++;\n            } else {\n                if (ten > 0 && five > 0) {\n                    ten--;\n                    five--;\n                } else if (five >= 3) {\n                    five -= 3;\n                } else {\n                    return false;\n                }\n            }\n        }\n        return true;\n    }\n}",
                "python": "class Solution:\n    def lemonadeChange(self, bills: list[int]) -> bool:\n        five = ten = 0\n        for bill in bills:\n            if bill == 5:\n                five += 1\n            elif bill == 10:\n                if five == 0:\n                    return False\n                five -= 1\n                ten += 1\n            else:\n                if ten > 0 and five > 0:\n                    ten -= 1\n                    five -= 1\n                elif five >= 3:\n                    five -= 3\n                else:\n                    return False\n        return True"
            }
        }
    },
    {
        "seq": 173,
        "whyNext": "Pair adjacent sorted numbers to minimize the wasted difference between min(a, b) pairs; sum even indices.",
        "brute": {
            "idea": "Generate all possible pairings of 2n numbers into n pairs and take maximum sum of min(a, b).",
            "steps": [
                "Recursively pair numbers.",
                "Sum mins of pairs.",
                "Take maximum across all pairings."
            ],
            "time": "O((2n)!)",
            "space": "O(n)",
            "whySlow": "Exponential factorial pairings when sorted order is provably optimal.",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int arrayPairSum(int[] nums) {\n        Arrays.sort(nums);\n        int sum = 0;\n        for (int i = 0; i < nums.length; i += 2) {\n            sum += nums[i];\n        }\n        return sum;\n    }\n}",
                "python": "class Solution:\n    def arrayPairSum(self, nums: list[int]) -> int:\n        nums.sort()\n        return sum(nums[::2])"
            }
        },
        "optimal": {
            "idea": "Sort array: pairing nums[2i] with nums[2i+1] minimizes sacrificed value; sum elements at even indices.",
            "steps": [
                "Sort nums in ascending order.",
                "Sum elements at even indices: i = 0, 2, 4...",
                "Return sum."
            ],
            "time": "O(n log n)",
            "space": "O(1)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int arrayPairSum(int[] nums) {\n        Arrays.sort(nums);\n        int sum = 0;\n        for (int i = 0; i < nums.length; i += 2) {\n            sum += nums[i];\n        }\n        return sum;\n    }\n}",
                "python": "class Solution:\n    def arrayPairSum(self, nums: list[int]) -> int:\n        nums.sort()\n        return sum(nums[i] for i in range(0, len(nums), 2))"
            }
        }
    },
    {
        "seq": 174,
        "whyNext": "Triangle inequality a + b > c: sort descending; first triplet satisfying nums[i] < nums[i-1] + nums[i-2] gives max perimeter.",
        "brute": {
            "idea": "Check all triplets (i, j, k) for valid triangle condition a + b > c and find maximum perimeter.",
            "steps": [
                "Three nested loops over all triplets.",
                "Check if valid triangle.",
                "Track maximum perimeter."
            ],
            "time": "O(n^3)",
            "space": "O(1)",
            "whySlow": "Examines all O(n^3) triplets.",
            "code": {
                "java": "class Solution {\n    public int largestPerimeter(int[] nums) {\n        int maxP = 0;\n        int n = nums.length;\n        for (int i = 0; i < n; i++) {\n            for (int j = i + 1; j < n; j++) {\n                for (int k = j + 1; k < n; k++) {\n                    int a = nums[i], b = nums[j], c = nums[k];\n                    if (a + b > c && a + c > b && b + c > a) {\n                        maxP = Math.max(maxP, a + b + c);\n                    }\n                }\n            }\n        }\n        return maxP;\n    }\n}",
                "python": "class Solution:\n    def largestPerimeter(self, nums: list[int]) -> int:\n        max_p = 0\n        n = len(nums)\n        for i in range(n):\n            for j in range(i + 1, n):\n                for k in range(j + 1, n):\n                    a, b, c = nums[i], nums[j], nums[k]\n                    if a + b > c and a + c > b and b + c > a:\n                        max_p = max(max_p, a + b + c)\n        return max_p"
            }
        },
        "optimal": {
            "idea": "Sort ascending: iterate from largest element downwards; first i where nums[i-2] + nums[i-1] > nums[i] is largest perimeter.",
            "steps": [
                "Arrays.sort(nums).",
                "Loop i from nums.length - 1 down to 2:",
                "If nums[i - 2] + nums[i - 1] > nums[i], return nums[i - 2] + nums[i - 1] + nums[i].",
                "Return 0."
            ],
            "time": "O(n log n)",
            "space": "O(1)",
            "code": {
                "java": "import java.util.*;\nclass Solution {\n    public int largestPerimeter(int[] nums) {\n        Arrays.sort(nums);\n        for (int i = nums.length - 1; i >= 2; i--) {\n            if (nums[i - 2] + nums[i - 1] > nums[i]) {\n                return nums[i - 2] + nums[i - 1] + nums[i];\n            }\n        }\n        return 0;\n    }\n}",
                "python": "class Solution:\n    def largestPerimeter(self, nums: list[int]) -> int:\n        nums.sort()\n        for i in range(len(nums) - 1, 1, -1):\n            if nums[i - 2] + nums[i - 1] > nums[i]:\n                return nums[i - 2] + nums[i - 1] + nums[i]\n        return 0"
            }
        }
    },
    {
        "seq": 175,
        "whyNext": "Greedy slope accumulation: capture every positive day-over-day price jump prices[i] - prices[i - 1].",
        "brute": {
            "idea": "Recursively decide on each day whether to buy, sell, or do nothing.",
            "steps": [
                "dfs(day, hasStock): return max profit reachable.",
                "Explore all buy and sell choices."
            ],
            "time": "O(2^n)",
            "space": "O(n)",
            "whySlow": "Exponential recursive branching when greedy accumulation of positive differences captures optimal total.",
            "code": {
                "java": "class Solution {\n    public int maxProfit(int[] prices) {\n        return dfs(prices, 0, 0);\n    }\n    private int dfs(int[] prices, int day, int holding) {\n        if (day == prices.length) return 0;\n        int doNothing = dfs(prices, day + 1, holding);\n        int action = 0;\n        if (holding == 1) {\n            action = prices[day] + dfs(prices, day + 1, 0);\n        } else {\n            action = -prices[day] + dfs(prices, day + 1, 1);\n        }\n        return Math.max(doNothing, action);\n    }\n}",
                "python": "class Solution:\n    def maxProfit(self, prices: list[int]) -> int:\n        def dfs(day, holding):\n            if day == len(prices): return 0\n            do_nothing = dfs(day + 1, holding)\n            if holding:\n                action = prices[day] + dfs(day + 1, 0)\n            else:\n                action = -prices[day] + dfs(day + 1, 1)\n            return max(do_nothing, action)\n        return dfs(0, 0)"
            }
        },
        "optimal": {
            "idea": "Greedy: whenever prices[i] > prices[i - 1], accumulate prices[i] - prices[i - 1] into total profit.",
            "steps": [
                "profit = 0.",
                "For i from 1 to prices.length - 1:",
                "If prices[i] > prices[i - 1], profit += prices[i] - prices[i - 1].",
                "Return profit."
            ],
            "time": "O(n)",
            "space": "O(1)",
            "code": {
                "java": "class Solution {\n    public int maxProfit(int[] prices) {\n        int profit = 0;\n        for (int i = 1; i < prices.length; i++) {\n            if (prices[i] > prices[i - 1]) {\n                profit += prices[i] - prices[i - 1];\n            }\n        }\n        return profit;\n    }\n}",
                "python": "class Solution:\n    def maxProfit(self, prices: list[int]) -> int:\n        return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, len(prices)))"
            }
        }
    }
]

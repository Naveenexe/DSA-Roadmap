# scripts/gen_batch_07.py
import json

batch_7 = [
    # 151: Delete Node in a BST
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
                "java": """import java.util.*;
class Solution {
    public TreeNode deleteNode(TreeNode root, int key) {
        List<Integer> list = new ArrayList<>();
        inorder(root, key, list);
        return build(list, 0, list.size() - 1);
    }
    private void inorder(TreeNode node, int key, List<Integer> list) {
        if (node == null) return;
        inorder(node.left, key, list);
        if (node.val != key) list.add(node.val);
        inorder(node.right, key, list);
    }
    private TreeNode build(List<Integer> list, int l, int r) {
        if (l > r) return null;
        int m = l + (r - l) / 2;
        TreeNode node = new TreeNode(list.get(m));
        node.left = build(list, l, m - 1);
        node.right = build(list, m + 1, r);
        return node;
    }
}""",
                "python": """class Solution:
    def deleteNode(self, root: TreeNode | None, key: int) -> TreeNode | None:
        vals = []
        def inorder(node):
            if not node: return
            inorder(node.left)
            if node.val != key: vals.append(node.val)
            inorder(node.right)
        inorder(root)
        def build(l, r):
            if l > r: return None
            m = (l + r) // 2
            node = TreeNode(vals[m])
            node.left = build(l, m - 1)
            node.right = build(m + 1, r)
            return node
        return build(0, len(vals) - 1)"""
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
                "java": """class Solution {
    public TreeNode deleteNode(TreeNode root, int key) {
        if (root == null) return null;
        if (key < root.val) {
            root.left = deleteNode(root.left, key);
        } else if (key > root.val) {
            root.right = deleteNode(root.right, key);
        } else {
            if (root.left == null) return root.right;
            if (root.right == null) return root.left;
            TreeNode successor = root.right;
            while (successor.left != null) successor = successor.left;
            root.val = successor.val;
            root.right = deleteNode(root.right, successor.val);
        }
        return root;
    }
}""",
                "python": """class Solution:
    def deleteNode(self, root: TreeNode | None, key: int) -> TreeNode | None:
        if not root:
            return None
        if key < root.val:
            root.left = self.deleteNode(root.left, key)
        elif key > root.val:
            root.right = self.deleteNode(root.right, key)
        else:
            if not root.left: return root.right
            if not root.right: return root.left
            succ = root.right
            while succ.left:
                succ = succ.left
            root.val = succ.val
            root.right = self.deleteNode(root.right, succ.val)
        return root"""
            }
        }
    },
    # 152: Kth Smallest Element in a BST
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
                "java": """import java.util.*;
class Solution {
    public int kthSmallest(TreeNode root, int k) {
        List<Integer> list = new ArrayList<>();
        inorder(root, list);
        return list.get(k - 1);
    }
    private void inorder(TreeNode node, List<Integer> list) {
        if (node == null) return;
        inorder(node.left, list);
        list.add(node.val);
        inorder(node.right, list);
    }
}""",
                "python": """class Solution:
    def kthSmallest(self, root: TreeNode | None, k: int) -> int:
        vals = []
        def inorder(node):
            if not node: return
            inorder(node.left)
            vals.append(node.val)
            inorder(node.right)
        inorder(root)
        return vals[k - 1]"""
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
                "java": """import java.util.*;
class Solution {
    public int kthSmallest(TreeNode root, int k) {
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode cur = root;
        while (cur != null || !stack.isEmpty()) {
            while (cur != null) {
                stack.push(cur);
                cur = cur.left;
            }
            cur = stack.pop();
            if (--k == 0) return cur.val;
            cur = cur.right;
        }
        return -1;
    }
}""",
                "python": """class Solution:
    def kthSmallest(self, root: TreeNode | None, k: int) -> int:
        stack = []
        cur = root
        while cur or stack:
            while cur:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            k -= 1
            if k == 0:
                return cur.val
            cur = cur.right
        return -1"""
            }
        }
    },
    # 153: Lowest Common Ancestor of a Binary Search Tree
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
                "java": """class Solution {
    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        if (root == null || root == p || root == q) return root;
        TreeNode left = lowestCommonAncestor(root.left, p, q);
        TreeNode right = lowestCommonAncestor(root.right, p, q);
        if (left != null && right != null) return root;
        return left != null ? left : right;
    }
}""",
                "python": """class Solution:
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        if not root or root == p or root == q:
            return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left and right: return root
        return left if left else right"""
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
                "java": """class Solution {
    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        TreeNode cur = root;
        while (cur != null) {
            if (p.val < cur.val && q.val < cur.val) {
                cur = cur.left;
            } else if (p.val > cur.val && q.val > cur.val) {
                cur = cur.right;
            } else {
                return cur;
            }
        }
        return null;
    }
}""",
                "python": """class Solution:
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        cur = root
        while cur:
            if p.val < cur.val and q.val < cur.val:
                cur = cur.left
            elif p.val > cur.val and q.val > cur.val:
                cur = cur.right
            else:
                return cur
        return None"""
            }
        }
    },
    # 154: Convert Sorted Array to Binary Search Tree
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
                "java": """class Solution {
    public TreeNode sortedArrayToBST(int[] nums) {
        return build(nums, 0, nums.length - 1);
    }
    private TreeNode build(int[] nums, int l, int r) {
        if (l > r) return null;
        int m = l + (r - l) / 2;
        TreeNode node = new TreeNode(nums[m]);
        node.left = build(nums, l, m - 1);
        node.right = build(nums, m + 1, r);
        return node;
    }
}""",
                "python": """class Solution:
    def sortedArrayToBST(self, nums: list[int]) -> TreeNode | None:
        def build(l, r):
            if l > r: return None
            m = (l + r) // 2
            node = TreeNode(nums[m])
            node.left = build(l, m - 1)
            node.right = build(m + 1, r)
            return node
        return build(0, len(nums) - 1)"""
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
                "java": """class Solution {
    public TreeNode sortedArrayToBST(int[] nums) {
        return build(nums, 0, nums.length - 1);
    }
    private TreeNode build(int[] nums, int left, int right) {
        if (left > right) return null;
        int mid = left + (right - left) / 2;
        TreeNode root = new TreeNode(nums[mid]);
        root.left = build(nums, left, mid - 1);
        root.right = build(nums, mid + 1, right);
        return root;
    }
}""",
                "python": """class Solution:
    def sortedArrayToBST(self, nums: list[int]) -> TreeNode | None:
        def build(left: int, right: int) -> TreeNode | None:
            if left > right:
                return None
            mid = (left + right) // 2
            root = TreeNode(nums[mid])
            root.left = build(left, mid - 1)
            root.right = build(mid + 1, right)
            return root
        return build(0, len(nums) - 1)"""
            }
        }
    },
    # 155: Binary Search Tree Iterator
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
                "java": """import java.util.*;
public class BSTIterator {
    private List<Integer> list = new ArrayList<>();
    private int idx = 0;
    public BSTIterator(TreeNode root) {
        inorder(root);
    }
    private void inorder(TreeNode node) {
        if (node == null) return;
        inorder(node.left);
        list.add(node.val);
        inorder(node.right);
    }
    public int next() {
        return list.get(idx++);
    }
    public boolean hasNext() {
        return idx < list.size();
    }
}""",
                "python": """class BSTIterator:
    def __init__(self, root: TreeNode | None):
        self.vals = []
        self.idx = 0
        def inorder(node):
            if not node: return
            inorder(node.left)
            self.vals.append(node.val)
            inorder(node.right)
        inorder(root)

    def next(self) -> int:
        val = self.vals[self.idx]
        self.idx += 1
        return val

    def hasNext(self) -> bool:
        return self.idx < len(self.vals)"""
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
                "java": """import java.util.*;
public class BSTIterator {
    private Deque<TreeNode> stack = new ArrayDeque<>();
    public BSTIterator(TreeNode root) {
        pushLeft(root);
    }
    public int next() {
        TreeNode node = stack.pop();
        if (node.right != null) {
            pushLeft(node.right);
        }
        return node.val;
    }
    public boolean hasNext() {
        return !stack.isEmpty();
    }
    private void pushLeft(TreeNode node) {
        while (node != null) {
            stack.push(node);
            node = node.left;
        }
    }
}""",
                "python": """class BSTIterator:
    def __init__(self, root: TreeNode | None):
        self.stack = []
        self._push_left(root)

    def _push_left(self, node: TreeNode | None):
        while node:
            self.stack.append(node)
            node = node.left

    def next(self) -> int:
        node = self.stack.pop()
        if node.right:
            self._push_left(node.right)
        return node.val

    def hasNext(self) -> bool:
        return len(self.stack) > 0"""
            }
        }
    },
    # 156: Recover Binary Search Tree
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
                "java": """import java.util.*;
class Solution {
    public void recoverTree(TreeNode root) {
        List<TreeNode> nodes = new ArrayList<>();
        List<Integer> vals = new ArrayList<>();
        inorder(root, nodes, vals);
        Collections.sort(vals);
        for (int i = 0; i < nodes.size(); i++) {
            nodes.get(i).val = vals.get(i);
        }
    }
    private void inorder(TreeNode node, List<TreeNode> nodes, List<Integer> vals) {
        if (node == null) return;
        inorder(node.left, nodes, vals);
        nodes.add(node);
        vals.add(node.val);
        inorder(node.right, nodes, vals);
    }
}""",
                "python": """class Solution:
    def recoverTree(self, root: TreeNode | None) -> None:
        nodes = []
        vals = []
        def inorder(node):
            if not node: return
            inorder(node.left)
            nodes.append(node)
            vals.append(node.val)
            inorder(node.right)
        inorder(root)
        vals.sort()
        for node, val in zip(nodes, vals):
            node.val = val"""
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
                "java": """class Solution {
    private TreeNode first = null;
    private TreeNode second = null;
    private TreeNode prev = null;
    public void recoverTree(TreeNode root) {
        inorder(root);
        int temp = first.val;
        first.val = second.val;
        second.val = temp;
    }
    private void inorder(TreeNode node) {
        if (node == null) return;
        inorder(node.left);
        if (prev != null && prev.val > node.val) {
            if (first == null) first = prev;
            second = node;
        }
        prev = node;
        inorder(node.right);
    }
}""",
                "python": """class Solution:
    def recoverTree(self, root: TreeNode | None) -> None:
        first = second = prev = None
        def inorder(node: TreeNode | None):
            nonlocal first, second, prev
            if not node:
                return
            inorder(node.left)
            if prev and prev.val > node.val:
                if not first:
                    first = prev
                second = node
            prev = node
            inorder(node.right)
        inorder(root)
        first.val, second.val = second.val, first.val"""
            }
        }
    },
    # 157: Kth Largest Element in a Stream
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
                "java": """import java.util.*;
public class KthLargest {
    private List<Integer> list = new ArrayList<>();
    private int k;
    public KthLargest(int k, int[] nums) {
        this.k = k;
        for (int x : nums) list.add(x);
    }
    public int add(int val) {
        list.add(val);
        Collections.sort(list, Collections.reverseOrder());
        return list.get(k - 1);
    }
}""",
                "python": """class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.nums = sorted(nums, reverse=True)

    def add(self, val: int) -> int:
        self.nums.append(val)
        self.nums.sort(reverse=True)
        return self.nums[self.k - 1]"""
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
                "java": """import java.util.*;
public class KthLargest {
    private PriorityQueue<Integer> minHeap = new PriorityQueue<>();
    private int k;
    public KthLargest(int k, int[] nums) {
        this.k = k;
        for (int x : nums) add(x);
    }
    public int add(int val) {
        minHeap.offer(val);
        if (minHeap.size() > k) {
            minHeap.poll();
        }
        return minHeap.peek();
    }
}""",
                "python": """import heapq

class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.heap = []
        for x in nums:
            self.add(x)

    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]"""
            }
        }
    },
    # 158: Kth Largest Element in an Array
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
                "java": """import java.util.*;
class Solution {
    public int findKthLargest(int[] nums, int k) {
        Arrays.sort(nums);
        return nums[nums.length - k];
    }
}""",
                "python": """class Solution:
    def findKthLargest(self, nums: list[int], k: int) -> int:
        nums.sort()
        return nums[len(nums) - k]"""
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
                "java": """import java.util.*;
class Solution {
    public int findKthLargest(int[] nums, int k) {
        int target = nums.length - k;
        int l = 0, r = nums.length - 1;
        Random rand = new Random();
        while (l <= r) {
            int pIdx = l + rand.nextInt(r - l + 1);
            int newP = partition(nums, l, r, pIdx);
            if (newP == target) return nums[newP];
            else if (newP < target) l = newP + 1;
            else r = newP - 1;
        }
        return nums[l];
    }
    private int partition(int[] nums, int l, int r, int pIdx) {
        int pivot = nums[pIdx];
        swap(nums, pIdx, r);
        int store = l;
        for (int i = l; i < r; i++) {
            if (nums[i] < pivot) {
                swap(nums, store++, i);
            }
        }
        swap(nums, store, r);
        return store;
    }
    private void swap(int[] nums, int i, int j) {
        int temp = nums[i]; nums[i] = nums[j]; nums[j] = temp;
    }
}""",
                "python": """import random

class Solution:
    def findKthLargest(self, nums: list[int], k: int) -> int:
        target = len(nums) - k
        l, r = 0, len(nums) - 1
        while l <= r:
            p_idx = random.randint(l, r)
            pivot = nums[p_idx]
            nums[p_idx], nums[r] = nums[r], nums[p_idx]
            store = l
            for i in range(l, r):
                if nums[i] < pivot:
                    nums[store], nums[i] = nums[i], nums[store]
                    store += 1
            nums[store], nums[r] = nums[r], nums[store]
            if store == target:
                return nums[store]
            elif store < target:
                l = store + 1
            else:
                r = store - 1
        return nums[l]"""
            }
        }
    },
    # 159: Last Stone Weight
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
                "java": """import java.util.*;
class Solution {
    public int lastStoneWeight(int[] stones) {
        List<Integer> list = new ArrayList<>();
        for (int s : stones) list.add(s);
        while (list.size() > 1) {
            Collections.sort(list);
            int y = list.remove(list.size() - 1);
            int x = list.remove(list.size() - 1);
            if (y > x) list.add(y - x);
        }
        return list.isEmpty() ? 0 : list.get(0);
    }
}""",
                "python": """class Solution:
    def lastStoneWeight(self, stones: list[int]) -> int:
        while len(stones) > 1:
            stones.sort()
            y = stones.pop()
            x = stones.pop()
            if y > x:
                stones.append(y - x)
        return stones[0] if stones else 0"""
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
                "java": """import java.util.*;
class Solution {
    public int lastStoneWeight(int[] stones) {
        PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
        for (int s : stones) maxHeap.offer(s);
        while (maxHeap.size() > 1) {
            int y = maxHeap.poll();
            int x = maxHeap.poll();
            if (y > x) maxHeap.offer(y - x);
        }
        return maxHeap.isEmpty() ? 0 : maxHeap.peek();
    }
}""",
                "python": """import heapq

class Solution:
    def lastStoneWeight(self, stones: list[int]) -> int:
        heap = [-s for s in stones]
        heapq.heapify(heap)
        while len(heap) > 1:
            y = -heapq.heappop(heap)
            x = -heapq.heappop(heap)
            if y > x:
                heapq.heappush(heap, -(y - x))
        return -heap[0] if heap else 0"""
            }
        }
    },
    # 160: K Closest Points to Origin
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
                "java": """import java.util.*;
class Solution {
    public int[][] kClosest(int[][] points, int k) {
        Arrays.sort(points, (a, b) -> (a[0]*a[0] + a[1]*a[1]) - (b[0]*b[0] + b[1]*b[1]));
        return Arrays.copyOfRange(points, 0, k);
    }
}""",
                "python": """class Solution:
    def kClosest(self, points: list[list[int]], k: int) -> list[list[int]]:
        points.sort(key=lambda p: p[0]**2 + p[1]**2)
        return points[:k]"""
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
                "java": """import java.util.*;
class Solution {
    public int[][] kClosest(int[][] points, int k) {
        PriorityQueue<int[]> maxHeap = new PriorityQueue<>((a, b) ->
            (b[0] * b[0] + b[1] * b[1]) - (a[0] * a[0] + a[1] * a[1])
        );
        for (int[] p : points) {
            maxHeap.offer(p);
            if (maxHeap.size() > k) {
                maxHeap.poll();
            }
        }
        int[][] res = new int[k][2];
        for (int i = 0; i < k; i++) {
            res[i] = maxHeap.poll();
        }
        return res;
    }
}""",
                "python": """import heapq

class Solution:
    def kClosest(self, points: list[list[int]], k: int) -> list[list[int]]:
        heap = []
        for x, y in points:
            dist = -(x * x + y * y)
            if len(heap) < k:
                heapq.heappush(heap, (dist, [x, y]))
            else:
                heapq.heappushpop(heap, (dist, [x, y]))
        return [p for _, p in heap]"""
            }
        }
    },
    # 161: Top K Frequent Words
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
                "java": """import java.util.*;
class Solution {
    public List<String> topKFrequent(String[] words, int k) {
        Map<String, Integer> count = new HashMap<>();
        for (String w : words) count.put(w, count.getOrDefault(w, 0) + 1);
        List<String> list = new ArrayList<>(count.keySet());
        list.sort((a, b) -> {
            int fa = count.get(a), fb = count.get(b);
            if (fa != fb) return fb - fa;
            return a.compareTo(b);
        });
        return list.subList(0, k);
    }
}""",
                "python": """from collections import Counter

class Solution:
    def topKFrequent(self, words: list[str], k: int) -> list[str]:
        count = Counter(words)
        unique = list(count.keys())
        unique.sort(key=lambda w: (-count[w], w))
        return unique[:k]"""
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
                "java": """import java.util.*;
class Solution {
    public List<String> topKFrequent(String[] words, int k) {
        Map<String, Integer> counts = new HashMap<>();
        for (String w : words) counts.put(w, counts.getOrDefault(w, 0) + 1);
        PriorityQueue<String> minHeap = new PriorityQueue<>((a, b) -> {
            int fa = counts.get(a), fb = counts.get(b);
            if (fa != fb) return fa - fb;
            return b.compareTo(a);
        });
        for (String w : counts.keySet()) {
            minHeap.offer(w);
            if (minHeap.size() > k) minHeap.poll();
        }
        List<String> res = new ArrayList<>();
        while (!minHeap.isEmpty()) res.add(minHeap.poll());
        Collections.reverse(res);
        return res;
    }
}""",
                "python": """import heapq
from collections import Counter

class Solution:
    def topKFrequent(self, words: list[str], k: int) -> list[str]:
        counts = Counter(words)
        class Item:
            def __init__(self, word, count):
                self.word = word
                self.count = count
            def __lt__(self, other):
                if self.count != other.count:
                    return self.count < other.count
                return self.word > other.word
        heap = []
        for word, cnt in counts.items():
            heapq.heappush(heap, Item(word, cnt))
            if len(heap) > k:
                heapq.heappop(heap)
        res = []
        while heap:
            res.append(heapq.heappop(heap).word)
        return res[::-1]"""
            }
        }
    },
    # 162: Sort Characters By Frequency
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
                "java": """import java.util.*;
class Solution {
    public String frequencySort(String s) {
        Map<Character, Integer> counts = new HashMap<>();
        for (char c : s.toCharArray()) counts.put(c, counts.getOrDefault(c, 0) + 1);
        List<Character> list = new ArrayList<>(counts.keySet());
        list.sort((a, b) -> counts.get(b) - counts.get(a));
        StringBuilder sb = new StringBuilder();
        for (char c : list) {
            int cnt = counts.get(c);
            for (int i = 0; i < cnt; i++) sb.append(c);
        }
        return sb.toString();
    }
}""",
                "python": """from collections import Counter

class Solution:
    def frequencySort(self, s: str) -> str:
        count = Counter(s)
        return "".join(c * cnt for c, cnt in count.most_common())"""
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
                "java": """import java.util.*;
class Solution {
    public String frequencySort(String s) {
        Map<Character, Integer> counts = new HashMap<>();
        for (char c : s.toCharArray()) counts.put(c, counts.getOrDefault(c, 0) + 1);
        List<Character>[] buckets = new List[s.length() + 1];
        for (char c : counts.keySet()) {
            int freq = counts.get(c);
            if (buckets[freq] == null) buckets[freq] = new ArrayList<>();
            buckets[freq].add(c);
        }
        StringBuilder sb = new StringBuilder();
        for (int i = buckets.length - 1; i >= 1; i--) {
            if (buckets[i] != null) {
                for (char c : buckets[i]) {
                    for (int j = 0; j < i; j++) sb.append(c);
                }
            }
        }
        return sb.toString();
    }
}""",
                "python": """from collections import Counter

class Solution:
    def frequencySort(self, s: str) -> str:
        counts = Counter(s)
        buckets = [[] for _ in range(len(s) + 1)]
        for c, freq in counts.items():
            buckets[freq].append(c)
        res = []
        for freq in range(len(s), 0, -1):
            for c in buckets[freq]:
                res.append(c * freq)
        return "".join(res)"""
            }
        }
    },
    # 163: Task Scheduler
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
                "java": """import java.util.*;
class Solution {
    public int leastInterval(char[] tasks, int n) {
        int[] counts = new int[26];
        for (char t : tasks) counts[t - 'A']++;
        PriorityQueue<Integer> pq = new PriorityQueue<>(Collections.reverseOrder());
        for (int c : counts) if (c > 0) pq.offer(c);
        Queue<int[]> queue = new LinkedList<>();
        int time = 0;
        while (!pq.isEmpty() || !queue.isEmpty()) {
            time++;
            if (!pq.isEmpty()) {
                int rem = pq.poll() - 1;
                if (rem > 0) queue.offer(new int[]{rem, time + n});
            }
            if (!queue.isEmpty() && queue.peek()[1] == time) {
                pq.offer(queue.poll()[0]);
            }
        }
        return time;
    }
}""",
                "python": """from collections import Counter, deque
import heapq

class Solution:
    def leastInterval(self, tasks: list[str], n: int) -> int:
        counts = Counter(tasks)
        max_heap = [-cnt for cnt in counts.values()]
        heapq.heapify(max_heap)
        q = deque()
        time = 0
        while max_heap or q:
            time += 1
            if max_heap:
                cnt = 1 + heapq.heappop(max_heap)
                if cnt != 0:
                    q.append((cnt, time + n))
            if q and q[0][1] == time:
                heapq.heappush(max_heap, q.popleft()[0])
        return time"""
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
                "java": """class Solution {
    public int leastInterval(char[] tasks, int n) {
        int[] counts = new int[26];
        int maxCount = 0;
        for (char t : tasks) {
            counts[t - 'A']++;
            maxCount = Math.max(maxCount, counts[t - 'A']);
        }
        int maxCountTasks = 0;
        for (int c : counts) {
            if (c == maxCount) maxCountTasks++;
        }
        int emptySlots = (maxCount - 1) * (n + 1) + maxCountTasks;
        return Math.max(tasks.length, emptySlots);
    }
}""",
                "python": """from collections import Counter

class Solution:
    def leastInterval(self, tasks: list[str], n: int) -> int:
        counts = Counter(tasks)
        max_count = max(counts.values())
        max_count_tasks = sum(1 for c in counts.values() if c == max_count)
        return max(len(tasks), (max_count - 1) * (n + 1) + max_count_tasks)"""
            }
        }
    },
    # 164: Reorganize String
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
                "java": """import java.util.*;
class Solution {
    public String reorganizeString(String s) {
        int[] counts = new int[26];
        for (char c : s.toCharArray()) counts[c - 'a']++;
        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> b[1] - a[1]);
        for (int i = 0; i < 26; i++) {
            if (counts[i] > 0) pq.offer(new int[]{i, counts[i]});
        }
        StringBuilder sb = new StringBuilder();
        int[] prev = null;
        while (!pq.isEmpty()) {
            int[] cur = pq.poll();
            sb.append((char) ('a' + cur[0]));
            cur[1]--;
            if (prev != null && prev[1] > 0) pq.offer(prev);
            prev = cur;
        }
        return sb.length() == s.length() ? sb.toString() : "";
    }
}""",
                "python": """import heapq
from collections import Counter

class Solution:
    def reorganizeString(self, s: str) -> str:
        counts = Counter(s)
        heap = [(-cnt, c) for c, cnt in counts.items()]
        heapq.heapify(heap)
        res = []
        prev = None
        while heap:
            cnt, c = heapq.heappop(heap)
            res.append(c)
            if prev:
                heapq.heappush(heap, prev)
                prev = None
            if -cnt > 1:
                prev = (cnt + 1, c)
        ans = "".join(res)
        return ans if len(ans) == len(s) else "" """
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
                "java": """class Solution {
    public String reorganizeString(String s) {
        int[] counts = new int[26];
        int maxCount = 0, letter = 0;
        for (char c : s.toCharArray()) {
            int code = c - 'a';
            counts[code]++;
            if (counts[code] > maxCount) {
                maxCount = counts[code];
                letter = code;
            }
        }
        if (maxCount > (s.length() + 1) / 2) return "";
        char[] res = new char[s.length()];
        int idx = 0;
        while (counts[letter] > 0) {
            res[idx] = (char) ('a' + letter);
            idx += 2;
            counts[letter]--;
        }
        for (int i = 0; i < 26; i++) {
            while (counts[i] > 0) {
                if (idx >= res.length) idx = 1;
                res[idx] = (char) ('a' + i);
                idx += 2;
                counts[i]--;
            }
        }
        return new String(res);
    }
}""",
                "python": """from collections import Counter

class Solution:
    def reorganizeString(self, s: str) -> str:
        counts = Counter(s)
        max_c, max_cnt = counts.most_common(1)[0]
        if max_cnt > (len(s) + 1) // 2:
            return ""
        res = [''] * len(s)
        idx = 0
        for _ in range(max_cnt):
            res[idx] = max_c
            idx += 2
        del counts[max_c]
        for c, cnt in counts.items():
            for _ in range(cnt):
                if idx >= len(s):
                    idx = 1
                res[idx] = c
                idx += 2
        return "".join(res)"""
            }
        }
    },
    # 165: Distant Barcodes
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
                "java": """import java.util.*;
class Solution {
    public int[] rearrangeBarcodes(int[] barcodes) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int b : barcodes) map.put(b, map.getOrDefault(b, 0) + 1);
        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> b[1] - a[1]);
        for (int k : map.keySet()) pq.offer(new int[]{k, map.get(k)});
        int[] res = new int[barcodes.length];
        int idx = 0;
        int[] prev = null;
        while (!pq.isEmpty()) {
            int[] cur = pq.poll();
            res[idx++] = cur[0];
            cur[1]--;
            if (prev != null && prev[1] > 0) pq.offer(prev);
            prev = cur;
        }
        return res;
    }
}""",
                "python": """import heapq
from collections import Counter

class Solution:
    def rearrangeBarcodes(self, barcodes: list[int]) -> list[int]:
        counts = Counter(barcodes)
        heap = [(-cnt, b) for b, cnt in counts.items()]
        heapq.heapify(heap)
        res = []
        prev = None
        while heap:
            cnt, b = heapq.heappop(heap)
            res.append(b)
            if prev:
                heapq.heappush(heap, prev)
                prev = None
            if -cnt > 1:
                prev = (cnt + 1, b)
        return res"""
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
                "java": """import java.util.*;
class Solution {
    public int[] rearrangeBarcodes(int[] barcodes) {
        Map<Integer, Integer> counts = new HashMap<>();
        for (int b : barcodes) counts.put(b, counts.getOrDefault(b, 0) + 1);
        List<Integer> keys = new ArrayList<>(counts.keySet());
        keys.sort((a, b) -> counts.get(b) - counts.get(a));
        int[] res = new int[barcodes.length];
        int idx = 0;
        for (int k : keys) {
            int freq = counts.get(k);
            while (freq-- > 0) {
                if (idx >= res.length) idx = 1;
                res[idx] = k;
                idx += 2;
            }
        }
        return res;
    }
}""",
                "python": """from collections import Counter

class Solution:
    def rearrangeBarcodes(self, barcodes: list[int]) -> list[int]:
        counts = Counter(barcodes)
        sorted_items = counts.most_common()
        res = [0] * len(barcodes)
        idx = 0
        for b, cnt in sorted_items:
            for _ in range(cnt):
                if idx >= len(barcodes):
                    idx = 1
                res[idx] = b
                idx += 2
        return res"""
            }
        }
    },
    # 166: Find Median from Data Stream
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
                "java": """import java.util.*;
public class MedianFinder {
    private List<Integer> list = new ArrayList<>();
    public MedianFinder() {}
    public void addNum(int num) {
        int idx = Collections.binarySearch(list, num);
        if (idx < 0) idx = -(idx + 1);
        list.add(idx, num);
    }
    public double findMedian() {
        int n = list.size();
        if (n % 2 == 1) return list.get(n / 2);
        return (list.get(n / 2 - 1) + list.get(n / 2)) / 2.0;
    }
}""",
                "python": """import bisect

class MedianFinder:
    def __init__(self):
        self.nums = []

    def addNum(self, num: int) -> None:
        bisect.insort(self.nums, num)

    def findMedian(self) -> float:
        n = len(self.nums)
        if n % 2 == 1:
            return float(self.nums[n // 2])
        return (self.nums[n // 2 - 1] + self.nums[n // 2]) / 2.0"""
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
                "java": """import java.util.*;
public class MedianFinder {
    private PriorityQueue<Integer> small = new PriorityQueue<>(Collections.reverseOrder());
    private PriorityQueue<Integer> large = new PriorityQueue<>();
    public MedianFinder() {}
    public void addNum(int num) {
        small.offer(num);
        large.offer(small.poll());
        if (large.size() > small.size()) {
            small.offer(large.poll());
        }
    }
    public double findMedian() {
        if (small.size() > large.size()) {
            return small.peek();
        }
        return (small.peek() + large.peek()) / 2.0;
    }
}""",
                "python": """import heapq

class MedianFinder:
    def __init__(self):
        self.small = []  # max-heap (negated)
        self.large = []  # min-heap

    def addNum(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0"""
            }
        }
    },
    # 167: Kth Smallest Element in a Sorted Matrix
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
                "java": """import java.util.*;
class Solution {
    public int kthSmallest(int[][] matrix, int k) {
        int n = matrix.length;
        int[] arr = new int[n * n];
        int idx = 0;
        for (int[] row : matrix) {
            for (int v : row) arr[idx++] = v;
        }
        Arrays.sort(arr);
        return arr[k - 1];
    }
}""",
                "python": """class Solution:
    def kthSmallest(self, matrix: list[list[int]], k: int) -> int:
        arr = [v for row in matrix for v in row]
        arr.sort()
        return arr[k - 1]"""
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
                "java": """class Solution {
    public int kthSmallest(int[][] matrix, int k) {
        int n = matrix.length;
        int low = matrix[0][0], high = matrix[n - 1][n - 1];
        while (low < high) {
            int mid = low + (high - low) / 2;
            if (countLessEqual(matrix, mid) < k) {
                low = mid + 1;
            } else {
                high = mid;
            }
        }
        return low;
    }
    private int countLessEqual(int[][] matrix, int target) {
        int n = matrix.length;
        int count = 0;
        int r = n - 1, c = 0;
        while (r >= 0 && c < n) {
            if (matrix[r][c] <= target) {
                count += (r + 1);
                c++;
            } else {
                r--;
            }
        }
        return count;
    }
}""",
                "python": """class Solution:
    def kthSmallest(self, matrix: list[list[int]], k: int) -> int:
        n = len(matrix)
        low, high = matrix[0][0], matrix[n - 1][n - 1]
        def count_le(mid):
            count = 0
            r, c = n - 1, 0
            while r >= 0 and c < n:
                if matrix[r][c] <= mid:
                    count += r + 1
                    c += 1
                else:
                    r -= 1
            return count
        while low < high:
            mid = (low + high) // 2
            if count_le(mid) < k:
                low = mid + 1
            else:
                high = mid
        return low"""
            }
        }
    },
    # 168: Find K Pairs with Smallest Sums
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
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> kSmallestPairs(int[] nums1, int[] nums2, int k) {
        List<List<Integer>> all = new ArrayList<>();
        for (int a : nums1) {
            for (int b : nums2) {
                all.add(Arrays.asList(a, b));
            }
        }
        all.sort(Comparator.comparingInt(p -> p.get(0) + p.get(1)));
        return all.subList(0, Math.min(k, all.size()));
    }
}""",
                "python": """class Solution:
    def kSmallestPairs(self, nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:
        pairs = [[a, b] for a in nums1 for b in nums2]
        pairs.sort(key=lambda p: p[0] + p[1])
        return pairs[:k]"""
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
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> kSmallestPairs(int[] nums1, int[] nums2, int k) {
        List<List<Integer>> res = new ArrayList<>();
        if (nums1.length == 0 || nums2.length == 0 || k == 0) return res;
        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[0]));
        for (int i = 0; i < Math.min(k, nums1.length); i++) {
            pq.offer(new int[]{nums1[i] + nums2[0], i, 0});
        }
        while (k-- > 0 && !pq.isEmpty()) {
            int[] cur = pq.poll();
            int i = cur[1], j = cur[2];
            res.add(Arrays.asList(nums1[i], nums2[j]));
            if (j + 1 < nums2.length) {
                pq.offer(new int[]{nums1[i] + nums2[j + 1], i, j + 1});
            }
        }
        return res;
    }
}""",
                "python": """import heapq

class Solution:
    def kSmallestPairs(self, nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:
        if not nums1 or not nums2 or k == 0:
            return []
        heap = []
        for i in range(min(k, len(nums1))):
            heapq.heappush(heap, (nums1[i] + nums2[0], i, 0))
        res = []
        while heap and len(res) < k:
            _, i, j = heapq.heappop(heap)
            res.append([nums1[i], nums2[j]])
            if j + 1 < len(nums2):
                heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))
        return res"""
            }
        }
    },
    # 169: Design Twitter
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
                "java": """import java.util.*;
public class Twitter {
    private List<int[]> allTweets = new ArrayList<>();
    private Map<Integer, Set<Integer>> follows = new HashMap<>();
    public Twitter() {}
    public void postTweet(int userId, int tweetId) {
        allTweets.add(new int[]{userId, tweetId});
    }
    public List<Integer> getNewsFeed(int userId) {
        Set<Integer> validUsers = new HashSet<>(follows.getOrDefault(userId, new HashSet<>()));
        validUsers.add(userId);
        List<Integer> feed = new ArrayList<>();
        for (int i = allTweets.size() - 1; i >= 0 && feed.size() < 10; i--) {
            int[] t = allTweets.get(i);
            if (validUsers.contains(t[0])) feed.add(t[1]);
        }
        return feed;
    }
    public void follow(int followerId, int followeeId) {
        follows.computeIfAbsent(followerId, k -> new HashSet<>()).add(followeeId);
    }
    public void unfollow(int followerId, int followeeId) {
        if (follows.containsKey(followerId)) follows.get(followerId).remove(followeeId);
    }
}""",
                "python": """from collections import defaultdict

class Twitter:
    def __init__(self):
        self.tweets = []
        self.follows = defaultdict(set)

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.tweets.append((userId, tweetId))

    def getNewsFeed(self, userId: int) -> list[int]:
        valid = self.follows[userId] | {userId}
        feed = []
        for u, t in reversed(self.tweets):
            if u in valid:
                feed.append(t)
                if len(feed) == 10:
                    break
        return feed

    def follow(self, followerId: int, followeeId: int) -> None:
        self.follows[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.follows[followerId].discard(followeeId)"""
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
                "java": """import java.util.*;
public class Twitter {
    private static int timestamp = 0;
    private static class Tweet {
        int id;
        int time;
        Tweet next;
        Tweet(int id, int time) { this.id = id; this.time = time; }
    }
    private Map<Integer, Set<Integer>> follows = new HashMap<>();
    private Map<Integer, Tweet> tweets = new HashMap<>();
    public Twitter() {}
    public void postTweet(int userId, int tweetId) {
        Tweet t = new Tweet(tweetId, ++timestamp);
        t.next = tweets.get(userId);
        tweets.put(userId, t);
    }
    public List<Integer> getNewsFeed(int userId) {
        Set<Integer> users = new HashSet<>(follows.getOrDefault(userId, new HashSet<>()));
        users.add(userId);
        PriorityQueue<Tweet> maxHeap = new PriorityQueue<>((a, b) -> b.time - a.time);
        for (int u : users) {
            Tweet t = tweets.get(u);
            if (t != null) maxHeap.offer(t);
        }
        List<Integer> feed = new ArrayList<>();
        while (!maxHeap.isEmpty() && feed.size() < 10) {
            Tweet t = maxHeap.poll();
            feed.add(t.id);
            if (t.next != null) maxHeap.offer(t.next);
        }
        return feed;
    }
    public void follow(int followerId, int followeeId) {
        follows.computeIfAbsent(followerId, k -> new HashSet<>()).add(followeeId);
    }
    public void unfollow(int followerId, int followeeId) {
        if (follows.containsKey(followerId)) follows.get(followerId).remove(followeeId);
    }
}""",
                "python": """import heapq
from collections import defaultdict

class Twitter:
    def __init__(self):
        self.time = 0
        self.tweets = defaultdict(list)
        self.follows = defaultdict(set)

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.time += 1
        self.tweets[userId].append((self.time, tweetId))

    def getNewsFeed(self, userId: int) -> list[int]:
        users = self.follows[userId] | {userId}
        heap = []
        for u in users:
            if self.tweets[u]:
                idx = len(self.tweets[u]) - 1
                t, tid = self.tweets[u][idx]
                heapq.heappush(heap, (-t, tid, u, idx))
        feed = []
        while heap and len(feed) < 10:
            neg_t, tid, u, idx = heapq.heappop(heap)
            feed.append(tid)
            if idx > 0:
                nxt_t, nxt_tid = self.tweets[u][idx - 1]
                heapq.heappush(heap, (-nxt_t, nxt_tid, u, idx - 1))
        return feed

    def follow(self, followerId: int, followeeId: int) -> None:
        self.follows[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.follows[followerId].discard(followeeId)"""
            }
        }
    },
    # 170: IPO
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
                "java": """class Solution {
    public int findMaximizedCapital(int k, int w, int[] profits, int[] capital) {
        int n = profits.length;
        boolean[] used = new boolean[n];
        for (int round = 0; round < k; round++) {
            int bestIdx = -1;
            for (int i = 0; i < n; i++) {
                if (!used[i] && capital[i] <= w) {
                    if (bestIdx == -1 || profits[i] > profits[bestIdx]) {
                        bestIdx = i;
                    }
                }
            }
            if (bestIdx == -1) break;
            used[bestIdx] = true;
            w += profits[bestIdx];
        }
        return w;
    }
}""",
                "python": """class Solution:
    def findMaximizedCapital(self, k: int, w: int, profits: list[int], capital: list[int]) -> int:
        n = len(profits)
        used = [False] * n
        for _ in range(k):
            best = -1
            for i in range(n):
                if not used[i] and capital[i] <= w:
                    if best == -1 or profits[i] > profits[best]:
                        best = i
            if best == -1: break
            used[best] = True
            w += profits[best]
        return w"""
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
                "java": """import java.util.*;
class Solution {
    public int findMaximizedCapital(int k, int w, int[] profits, int[] capital) {
        int n = profits.length;
        int[][] projects = new int[n][2];
        for (int i = 0; i < n; i++) {
            projects[i][0] = capital[i];
            projects[i][1] = profits[i];
        }
        Arrays.sort(projects, Comparator.comparingInt(a -> a[0]));
        PriorityQueue<Integer> maxProfitHeap = new PriorityQueue<>(Collections.reverseOrder());
        int ptr = 0;
        for (int i = 0; i < k; i++) {
            while (ptr < n && projects[ptr][0] <= w) {
                maxProfitHeap.offer(projects[ptr][1]);
                ptr++;
            }
            if (maxProfitHeap.isEmpty()) break;
            w += maxProfitHeap.poll();
        }
        return w;
    }
}""",
                "python": """import heapq

class Solution:
    def findMaximizedCapital(self, k: int, w: int, profits: list[int], capital: list[int]) -> int:
        projects = sorted(zip(capital, profits), key=lambda x: x[0])
        n = len(projects)
        max_profit_heap = []
        ptr = 0
        for _ in range(k):
            while ptr < n and projects[ptr][0] <= w:
                heapq.heappush(max_profit_heap, -projects[ptr][1])
                ptr += 1
            if not max_profit_heap:
                break
            w += -heapq.heappop(max_profit_heap)
        return w"""
            }
        }
    },
    # 171: Assign Cookies
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
                "java": """class Solution {
    public int findContentChildren(int[] g, int[] s) {
        boolean[] used = new boolean[s.length];
        int content = 0;
        for (int child : g) {
            int bestIdx = -1;
            for (int j = 0; j < s.length; j++) {
                if (!used[j] && s[j] >= child) {
                    if (bestIdx == -1 || s[j] < s[bestIdx]) {
                        bestIdx = j;
                    }
                }
            }
            if (bestIdx != -1) {
                used[bestIdx] = true;
                content++;
            }
        }
        return content;
    }
}""",
                "python": """class Solution:
    def findContentChildren(self, g: list[int], s: list[int]) -> int:
        used = [False] * len(s)
        ans = 0
        for child in g:
            best = -1
            for j in range(len(s)):
                if not used[j] and s[j] >= child:
                    if best == -1 or s[j] < s[best]:
                        best = j
            if best != -1:
                used[best] = True
                ans += 1
        return ans"""
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
                "java": """import java.util.*;
class Solution {
    public int findContentChildren(int[] g, int[] s) {
        Arrays.sort(g);
        Arrays.sort(s);
        int i = 0, j = 0;
        while (i < g.length && j < s.length) {
            if (s[j] >= g[i]) {
                i++;
            }
            j++;
        }
        return i;
    }
}""",
                "python": """class Solution:
    def findContentChildren(self, g: list[int], s: list[int]) -> int:
        g.sort()
        s.sort()
        i = j = 0
        while i < len(g) and j < len(s):
            if s[j] >= g[i]:
                i += 1
            j += 1
        return i"""
            }
        }
    },
    # 172: Lemonade Change
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
                "java": """class Solution {
    public boolean lemonadeChange(int[] bills) {
        int five = 0, ten = 0;
        for (int b : bills) {
            if (b == 5) five++;
            else if (b == 10) {
                if (five == 0) return false;
                five--; ten++;
            } else {
                if (ten > 0 && five > 0) {
                    ten--; five--;
                } else if (five >= 3) {
                    five -= 3;
                } else {
                    return false;
                }
            }
        }
        return true;
    }
}""",
                "python": """class Solution:
    def lemonadeChange(self, bills: list[int]) -> bool:
        five = ten = 0
        for b in bills:
            if b == 5:
                five += 1
            elif b == 10:
                if not five: return False
                five -= 1
                ten += 1
            else:
                if ten and five:
                    ten -= 1
                    five -= 1
                elif five >= 3:
                    five -= 3
                else:
                    return False
        return True"""
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
                "java": """class Solution {
    public boolean lemonadeChange(int[] bills) {
        int five = 0, ten = 0;
        for (int bill : bills) {
            if (bill == 5) {
                five++;
            } else if (bill == 10) {
                if (five == 0) return false;
                five--;
                ten++;
            } else {
                if (ten > 0 && five > 0) {
                    ten--;
                    five--;
                } else if (five >= 3) {
                    five -= 3;
                } else {
                    return false;
                }
            }
        }
        return true;
    }
}""",
                "python": """class Solution:
    def lemonadeChange(self, bills: list[int]) -> bool:
        five = ten = 0
        for bill in bills:
            if bill == 5:
                five += 1
            elif bill == 10:
                if five == 0:
                    return False
                five -= 1
                ten += 1
            else:
                if ten > 0 and five > 0:
                    ten -= 1
                    five -= 1
                elif five >= 3:
                    five -= 3
                else:
                    return False
        return True"""
            }
        }
    },
    # 173: Array Partition
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
                "java": """import java.util.*;
class Solution {
    public int arrayPairSum(int[] nums) {
        Arrays.sort(nums);
        int sum = 0;
        for (int i = 0; i < nums.length; i += 2) {
            sum += nums[i];
        }
        return sum;
    }
}""",
                "python": """class Solution:
    def arrayPairSum(self, nums: list[int]) -> int:
        nums.sort()
        return sum(nums[::2])"""
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
                "java": """import java.util.*;
class Solution {
    public int arrayPairSum(int[] nums) {
        Arrays.sort(nums);
        int sum = 0;
        for (int i = 0; i < nums.length; i += 2) {
            sum += nums[i];
        }
        return sum;
    }
}""",
                "python": """class Solution:
    def arrayPairSum(self, nums: list[int]) -> int:
        nums.sort()
        return sum(nums[i] for i in range(0, len(nums), 2))"""
            }
        }
    },
    # 174: Largest Perimeter Triangle
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
                "java": """class Solution {
    public int largestPerimeter(int[] nums) {
        int maxP = 0;
        int n = nums.length;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                for (int k = j + 1; k < n; k++) {
                    int a = nums[i], b = nums[j], c = nums[k];
                    if (a + b > c && a + c > b && b + c > a) {
                        maxP = Math.max(maxP, a + b + c);
                    }
                }
            }
        }
        return maxP;
    }
}""",
                "python": """class Solution:
    def largestPerimeter(self, nums: list[int]) -> int:
        max_p = 0
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    a, b, c = nums[i], nums[j], nums[k]
                    if a + b > c and a + c > b and b + c > a:
                        max_p = max(max_p, a + b + c)
        return max_p"""
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
                "java": """import java.util.*;
class Solution {
    public int largestPerimeter(int[] nums) {
        Arrays.sort(nums);
        for (int i = nums.length - 1; i >= 2; i--) {
            if (nums[i - 2] + nums[i - 1] > nums[i]) {
                return nums[i - 2] + nums[i - 1] + nums[i];
            }
        }
        return 0;
    }
}""",
                "python": """class Solution:
    def largestPerimeter(self, nums: list[int]) -> int:
        nums.sort()
        for i in range(len(nums) - 1, 1, -1):
            if nums[i - 2] + nums[i - 1] > nums[i]:
                return nums[i - 2] + nums[i - 1] + nums[i]
        return 0"""
            }
        }
    },
    # 175: Best Time to Buy and Sell Stock II
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
                "java": """class Solution {
    public int maxProfit(int[] prices) {
        return dfs(prices, 0, 0);
    }
    private int dfs(int[] prices, int day, int holding) {
        if (day == prices.length) return 0;
        int doNothing = dfs(prices, day + 1, holding);
        int action = 0;
        if (holding == 1) {
            action = prices[day] + dfs(prices, day + 1, 0);
        } else {
            action = -prices[day] + dfs(prices, day + 1, 1);
        }
        return Math.max(doNothing, action);
    }
}""",
                "python": """class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        def dfs(day, holding):
            if day == len(prices): return 0
            do_nothing = dfs(day + 1, holding)
            if holding:
                action = prices[day] + dfs(day + 1, 0)
            else:
                action = -prices[day] + dfs(day + 1, 1)
            return max(do_nothing, action)
        return dfs(0, 0)"""
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
                "java": """class Solution {
    public int maxProfit(int[] prices) {
        int profit = 0;
        for (int i = 1; i < prices.length; i++) {
            if (prices[i] > prices[i - 1]) {
                profit += prices[i] - prices[i - 1];
            }
        }
        return profit;
    }
}""",
                "python": """class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, len(prices)))"""
            }
        }
    }
]

with open('scripts/batches/batch_07.py', 'w', encoding='utf-8') as f:
    f.write("# Batch 7: Questions 151 to 175\n\n")
    f.write("def get_batch():\n")
    f.write("    return " + json.dumps(batch_7, indent=4) + "\n")

print("Wrote scripts/batches/batch_07.py with", len(batch_7), "questions.")


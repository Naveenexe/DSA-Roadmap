# scripts/gen_batch_06.py
import json

batch_6 = [
    # 126: Balanced Binary Tree
    {
        "seq": 126,
        "whyNext": "Builds on Maximum Depth: checks whether difference between heights of left and right subtrees is at most 1 at every node.",
        "brute": {
            "idea": "For every node, calculate height(node.left) and height(node.right) and verify diff <= 1.",
            "steps": [
                "Recursively compute depth of left and right children.",
                "Check |depth(left) - depth(right)| <= 1.",
                "Recurse for left and right children."
            ],
            "time": "O(n^2)",
            "space": "O(h)",
            "whySlow": "Recalculates depths of subtrees repeatedly at every ancestor node.",
            "code": {
                "java": """class Solution {
    public boolean isBalanced(TreeNode root) {
        if (root == null) return true;
        int leftH = depth(root.left);
        int rightH = depth(root.right);
        if (Math.abs(leftH - rightH) > 1) return false;
        return isBalanced(root.left) && isBalanced(root.right);
    }
    private int depth(TreeNode node) {
        if (node == null) return 0;
        return 1 + Math.max(depth(node.left), depth(node.right));
    }
}""",
                "python": """class Solution:
    def isBalanced(self, root: TreeNode | None) -> bool:
        if not root:
            return True
        def depth(node):
            if not node: return 0
            return 1 + max(depth(node.left), depth(node.right))
        if abs(depth(root.left) - depth(root.right)) > 1:
            return False
        return self.isBalanced(root.left) and self.isBalanced(root.right)"""
            }
        },
        "optimal": {
            "idea": "Bottom-up DFS: return height if balanced, or -1 immediately when unbalanced to short-circuit in O(n).",
            "steps": [
                "Define checkHeight(node): returns height or -1 if unbalanced.",
                "If node == null return 0.",
                "Recursively get left = checkHeight(node.left); if left == -1 return -1.",
                "Get right = checkHeight(node.right); if right == -1 return -1.",
                "If |left - right| > 1 return -1; else return 1 + max(left, right)."
            ],
            "time": "O(n)",
            "space": "O(h)",
            "code": {
                "java": """class Solution {
    public boolean isBalanced(TreeNode root) {
        return checkHeight(root) != -1;
    }
    private int checkHeight(TreeNode node) {
        if (node == null) return 0;
        int left = checkHeight(node.left);
        if (left == -1) return -1;
        int right = checkHeight(node.right);
        if (right == -1) return -1;
        if (Math.abs(left - right) > 1) return -1;
        return 1 + Math.max(left, right);
    }
}""",
                "python": """class Solution:
    def isBalanced(self, root: TreeNode | None) -> bool:
        def check(node: TreeNode | None) -> int:
            if not node:
                return 0
            left = check(node.left)
            if left == -1: return -1
            right = check(node.right)
            if right == -1: return -1
            if abs(left - right) > 1: return -1
            return 1 + max(left, right)
        return check(root) != -1"""
            }
        }
    },
    # 127: Diameter of Binary Tree
    {
        "seq": 127,
        "whyNext": "Builds on height calculation: diameter at node is left_depth + right_depth; track global maximum during post-order traversal.",
        "brute": {
            "idea": "For every node in the tree, calculate maxDepth(left) + maxDepth(right) and return the overall max.",
            "steps": [
                "Traverse every node in the tree.",
                "At each node, call depth(node.left) + depth(node.right).",
                "Take maximum across all nodes."
            ],
            "time": "O(n^2)",
            "space": "O(h)",
            "whySlow": "Depth is recomputed independently for all descendants, leading to quadratic running time.",
            "code": {
                "java": """class Solution {
    public int diameterOfBinaryTree(TreeNode root) {
        if (root == null) return 0;
        int throughRoot = depth(root.left) + depth(root.right);
        int leftD = diameterOfBinaryTree(root.left);
        int rightD = diameterOfBinaryTree(root.right);
        return Math.max(throughRoot, Math.max(leftD, rightD));
    }
    private int depth(TreeNode node) {
        if (node == null) return 0;
        return 1 + Math.max(depth(node.left), depth(node.right));
    }
}""",
                "python": """class Solution:
    def diameterOfBinaryTree(self, root: TreeNode | None) -> int:
        if not root:
            return 0
        def depth(node):
            if not node: return 0
            return 1 + max(depth(node.left), depth(node.right))
        cur = depth(root.left) + depth(root.right)
        return max(cur, self.diameterOfBinaryTree(root.left), self.diameterOfBinaryTree(root.right))"""
            }
        },
        "optimal": {
            "idea": "Post-order DFS updating global diameter while returning 1 + max(left, right) height upwards.",
            "steps": [
                "Initialize maxDiameter = 0.",
                "In dfs(node): if node == null return 0.",
                "Recursively compute left = dfs(node.left), right = dfs(node.right).",
                "Update maxDiameter = max(maxDiameter, left + right).",
                "Return 1 + max(left, right)."
            ],
            "time": "O(n)",
            "space": "O(h)",
            "code": {
                "java": """class Solution {
    private int maxDiameter = 0;
    public int diameterOfBinaryTree(TreeNode root) {
        dfs(root);
        return maxDiameter;
    }
    private int dfs(TreeNode node) {
        if (node == null) return 0;
        int left = dfs(node.left);
        int right = dfs(node.right);
        maxDiameter = Math.max(maxDiameter, left + right);
        return 1 + Math.max(left, right);
    }
}""",
                "python": """class Solution:
    def diameterOfBinaryTree(self, root: TreeNode | None) -> int:
        max_d = 0
        def dfs(node: TreeNode | None) -> int:
            nonlocal max_d
            if not node:
                return 0
            left = dfs(node.left)
            right = dfs(node.right)
            max_d = max(max_d, left + right)
            return 1 + max(left, right)
        dfs(root)
        return max_d"""
            }
        }
    },
    # 128: Subtree of Another Tree
    {
        "seq": 128,
        "whyNext": "Builds on Same Tree: checks if tree contains a subtree identical to subRoot at any node.",
        "brute": {
            "idea": "Serialize both trees with unique null markers and check if subRoot serialized string is substring of root string.",
            "steps": [
                "Serialize root and subRoot into comma-delimited strings with delimiters (e.g. ^val$).",
                "Perform substring search."
            ],
            "time": "O(m * n)",
            "space": "O(m + n)",
            "whySlow": "String serialization and search requires large string allocations and delimiter care.",
            "code": {
                "java": """class Solution {
    public boolean isSubtree(TreeNode root, TreeNode subRoot) {
        StringBuilder sb1 = new StringBuilder();
        StringBuilder sb2 = new StringBuilder();
        serialize(root, sb1);
        serialize(subRoot, sb2);
        return sb1.toString().contains(sb2.toString());
    }
    private void serialize(TreeNode node, StringBuilder sb) {
        if (node == null) {
            sb.append(",#");
            return;
        }
        sb.append(",").append(node.val);
        serialize(node.left, sb);
        serialize(node.right, sb);
    }
}""",
                "python": """class Solution:
    def isSubtree(self, root: TreeNode | None, subRoot: TreeNode | None) -> bool:
        def serialize(node: TreeNode | None) -> str:
            if not node:
                return ",#"
            return f",{node.val}" + serialize(node.left) + serialize(node.right)
        return serialize(subRoot) in serialize(root)"""
            }
        },
        "optimal": {
            "idea": "Recursive tree traversal: at each node check isSameTree(node, subRoot); if not, recurse on left and right subtrees.",
            "steps": [
                "If root == null return false.",
                "If isSameTree(root, subRoot) return true.",
                "Return isSubtree(root.left, subRoot) || isSubtree(root.right, subRoot)."
            ],
            "time": "O(m * n)",
            "space": "O(h)",
            "code": {
                "java": """class Solution {
    public boolean isSubtree(TreeNode root, TreeNode subRoot) {
        if (root == null) return false;
        if (isSame(root, subRoot)) return true;
        return isSubtree(root.left, subRoot) || isSubtree(root.right, subRoot);
    }
    private boolean isSame(TreeNode s, TreeNode t) {
        if (s == null && t == null) return true;
        if (s == null || t == null || s.val != t.val) return false;
        return isSame(s.left, t.left) && isSame(s.right, t.right);
    }
}""",
                "python": """class Solution:
    def isSubtree(self, root: TreeNode | None, subRoot: TreeNode | None) -> bool:
        if not root:
            return False
        def is_same(s: TreeNode | None, t: TreeNode | None) -> bool:
            if not s and not t: return True
            if not s or not t or s.val != t.val: return False
            return is_same(s.left, t.left) and is_same(s.right, t.right)
        if is_same(root, subRoot):
            return True
        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)"""
            }
        }
    },
    # 129: Path Sum
    {
        "seq": 129,
        "whyNext": "Root-to-leaf path tracking: subtract node.val along path; verify targetSum == 0 at leaf nodes.",
        "brute": {
            "idea": "Collect all root-to-leaf path sums into a list and check if targetSum is present.",
            "steps": [
                "Traverse all root-to-leaf paths, accumulating path sum.",
                "At leaves, record total sum.",
                "Check if targetSum is in accumulated sums."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "whySlow": "Stores all path sums in auxiliary collections instead of short-circuiting.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public boolean hasPathSum(TreeNode root, int targetSum) {
        List<Integer> sums = new ArrayList<>();
        collectSums(root, 0, sums);
        return sums.contains(targetSum);
    }
    private void collectSums(TreeNode node, int cur, List<Integer> sums) {
        if (node == null) return;
        cur += node.val;
        if (node.left == null && node.right == null) {
            sums.add(cur);
            return;
        }
        collectSums(node.left, cur, sums);
        collectSums(node.right, cur, sums);
    }
}""",
                "python": """class Solution:
    def hasPathSum(self, root: TreeNode | None, targetSum: int) -> bool:
        sums = []
        def dfs(node, cur):
            if not node: return
            cur += node.val
            if not node.left and not node.right:
                sums.append(cur)
                return
            dfs(node.left, cur)
            dfs(node.right, cur)
        dfs(root, 0)
        return targetSum in sums"""
            }
        },
        "optimal": {
            "idea": "Short-circuit recursive DFS: decrement targetSum by node.val. At leaf, return targetSum == node.val.",
            "steps": [
                "If root == null return false.",
                "If root.left == null and root.right == null, return targetSum == root.val.",
                "Return hasPathSum(root.left, targetSum - root.val) || hasPathSum(root.right, targetSum - root.val)."
            ],
            "time": "O(n)",
            "space": "O(h)",
            "code": {
                "java": """class Solution {
    public boolean hasPathSum(TreeNode root, int targetSum) {
        if (root == null) return false;
        if (root.left == null && root.right == null) {
            return targetSum == root.val;
        }
        return hasPathSum(root.left, targetSum - root.val) ||
               hasPathSum(root.right, targetSum - root.val);
    }
}""",
                "python": """class Solution:
    def hasPathSum(self, root: TreeNode | None, targetSum: int) -> bool:
        if not root:
            return False
        if not root.left and not root.right:
            return targetSum == root.val
        rem = targetSum - root.val
        return self.hasPathSum(root.left, rem) or self.hasPathSum(root.right, rem)"""
            }
        }
    },
    # 130: Path Sum II
    {
        "seq": 130,
        "whyNext": "Builds on Path Sum: must record the complete path of node values for every path equaling targetSum.",
        "brute": {
            "idea": "Generate all root-to-leaf paths as lists of integers; filter those that sum to targetSum.",
            "steps": [
                "Recursively collect all root-to-leaf paths.",
                "Sum each path and filter paths matching targetSum."
            ],
            "time": "O(n * h)",
            "space": "O(n * h)",
            "whySlow": "Copies lists at each recursive branching point even when sum diverges.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> pathSum(TreeNode root, int targetSum) {
        List<List<Integer>> allPaths = new ArrayList<>();
        getAllPaths(root, new ArrayList<>(), allPaths);
        List<List<Integer>> res = new ArrayList<>();
        for (List<Integer> path : allPaths) {
            int s = 0;
            for (int v : path) s += v;
            if (s == targetSum) res.add(path);
        }
        return res;
    }
    private void getAllPaths(TreeNode node, List<Integer> cur, List<List<Integer>> all) {
        if (node == null) return;
        cur.add(node.val);
        if (node.left == null && node.right == null) {
            all.add(new ArrayList<>(cur));
        } else {
            getAllPaths(node.left, new ArrayList<>(cur), all);
            getAllPaths(node.right, new ArrayList<>(cur), all);
        }
    }
}""",
                "python": """class Solution:
    def pathSum(self, root: TreeNode | None, targetSum: int) -> list[list[int]]:
        all_paths = []
        def dfs(node, path):
            if not node: return
            new_path = path + [node.val]
            if not node.left and not node.right:
                all_paths.append(new_path)
            else:
                dfs(node.left, new_path)
                dfs(node.right, new_path)
        dfs(root, [])
        return [p for p in all_paths if sum(p) == targetSum]"""
            }
        },
        "optimal": {
            "idea": "Backtracking with single path list: push node.val, recurse, save copy at leaf if target == node.val, then pop.",
            "steps": [
                "Maintain a single mutable path list.",
                "At each node, append node.val.",
                "If leaf and targetSum == node.val, append copy of path to result.",
                "Recurse left and right with targetSum - node.val.",
                "Pop node.val to backtrack."
            ],
            "time": "O(n)",
            "space": "O(h)",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> pathSum(TreeNode root, int targetSum) {
        List<List<Integer>> res = new ArrayList<>();
        List<Integer> path = new ArrayList<>();
        dfs(root, targetSum, path, res);
        return res;
    }
    private void dfs(TreeNode node, int rem, List<Integer> path, List<List<Integer>> res) {
        if (node == null) return;
        path.add(node.val);
        if (node.left == null && node.right == null && rem == node.val) {
            res.add(new ArrayList<>(path));
        } else {
            dfs(node.left, rem - node.val, path, res);
            dfs(node.right, rem - node.val, path, res);
        }
        path.remove(path.size() - 1);
    }
}""",
                "python": """class Solution:
    def pathSum(self, root: TreeNode | None, targetSum: int) -> list[list[int]]:
        res = []
        path = []
        def dfs(node: TreeNode | None, rem: int):
            if not node:
                return
            path.append(node.val)
            if not node.left and not node.right and rem == node.val:
                res.append(list(path))
            else:
                dfs(node.left, rem - node.val)
                dfs(node.right, rem - node.val)
            path.pop()
        dfs(root, targetSum)
        return res"""
            }
        }
    },
    # 131: Binary Tree Paths
    {
        "seq": 131,
        "whyNext": "Builds on root-to-leaf paths: formats paths into arrow strings 'val->val->val'.",
        "brute": {
            "idea": "Recursively concatenate strings with '->' at each recursive step.",
            "steps": [
                "At each node, create a new string appending '->' and node.val.",
                "If leaf, add string to result list."
            ],
            "time": "O(n * h)",
            "space": "O(n * h)",
            "whySlow": "String immutability creates numerous intermediate string objects on each recursive step.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<String> binaryTreePaths(TreeNode root) {
        List<String> res = new ArrayList<>();
        if (root != null) dfs(root, "", res);
        return res;
    }
    private void dfs(TreeNode node, String path, List<String> res) {
        path += node.val;
        if (node.left == null && node.right == null) {
            res.add(path);
            return;
        }
        if (node.left != null) dfs(node.left, path + "->", res);
        if (node.right != null) dfs(node.right, path + "->", res);
    }
}""",
                "python": """class Solution:
    def binaryTreePaths(self, root: TreeNode | None) -> list[str]:
        res = []
        def dfs(node: TreeNode | None, path: str):
            if not node: return
            path += str(node.val)
            if not node.left and not node.right:
                res.append(path)
                return
            if node.left: dfs(node.left, path + "->")
            if node.right: dfs(node.right, path + "->")
        if root: dfs(root, "")
        return res"""
            }
        },
        "optimal": {
            "idea": "Backtracking with StringBuilder: record length, append node.val, backtrack by resetting length.",
            "steps": [
                "Use a single StringBuilder.",
                "Save len = sb.length(); append node.val.",
                "If leaf, add sb.toString() to res.",
                "Else if children exist, append '->' and recurse on left and right.",
                "Reset sb.setLength(len) to backtrack cleanly."
            ],
            "time": "O(n)",
            "space": "O(h)",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<String> binaryTreePaths(TreeNode root) {
        List<String> res = new ArrayList<>();
        if (root == null) return res;
        dfs(root, new StringBuilder(), res);
        return res;
    }
    private void dfs(TreeNode node, StringBuilder sb, List<String> res) {
        int len = sb.length();
        sb.append(node.val);
        if (node.left == null && node.right == null) {
            res.add(sb.toString());
        } else {
            sb.append("->");
            if (node.left != null) dfs(node.left, sb, res);
            if (node.right != null) dfs(node.right, sb, res);
        }
        sb.setLength(len);
    }
}""",
                "python": """class Solution:
    def binaryTreePaths(self, root: TreeNode | None) -> list[str]:
        res = []
        path = []
        def dfs(node: TreeNode | None):
            if not node:
                return
            path.append(str(node.val))
            if not node.left and not node.right:
                res.append("->".join(path))
            else:
                dfs(node.left)
                dfs(node.right)
            path.pop()
        dfs(root)
        return res"""
            }
        }
    },
    # 132: Path Sum III
    {
        "seq": 132,
        "whyNext": "Path does not need to start at root or end at leaf: prefix sum hash map technique applied to tree DFS.",
        "brute": {
            "idea": "For every node in the tree, run Path Sum starting from that node as the root.",
            "steps": [
                "At each node, call countFromNode(node, targetSum).",
                "Recurse pathSum on node.left and node.right."
            ],
            "time": "O(n^2)",
            "space": "O(h)",
            "whySlow": "Paths are re-traversed repeatedly from every ancestor node.",
            "code": {
                "java": """class Solution {
    public int pathSum(TreeNode root, int targetSum) {
        if (root == null) return 0;
        return countFrom(root, targetSum) + pathSum(root.left, targetSum) + pathSum(root.right, targetSum);
    }
    private int countFrom(TreeNode node, long rem) {
        if (node == null) return 0;
        int count = (rem == node.val) ? 1 : 0;
        count += countFrom(node.left, rem - node.val);
        count += countFrom(node.right, rem - node.val);
        return count;
    }
}""",
                "python": """class Solution:
    def pathSum(self, root: TreeNode | None, targetSum: int) -> int:
        if not root:
            return 0
        def count_from(node, rem):
            if not node: return 0
            cnt = 1 if rem == node.val else 0
            return cnt + count_from(node.left, rem - node.val) + count_from(node.right, rem - node.val)
        return count_from(root, targetSum) + self.pathSum(root.left, targetSum) + self.pathSum(root.right, targetSum)"""
            }
        },
        "optimal": {
            "idea": "Prefix sum hash map with backtracking: count paths ending at current node with prefixSum = curSum - targetSum in O(1).",
            "steps": [
                "Maintain HashMap<Long, Integer> prefixCount initialized with map.put(0L, 1).",
                "At current node, curSum += node.val.",
                "totalPaths += prefixCount.getOrDefault(curSum - targetSum, 0).",
                "Put curSum into map, recurse left and right.",
                "Backtrack: decrement prefixCount for curSum before returning."
            ],
            "time": "O(n)",
            "space": "O(h)",
            "code": {
                "java": """import java.util.*;
class Solution {
    private int total = 0;
    public int pathSum(TreeNode root, int targetSum) {
        Map<Long, Integer> prefixMap = new HashMap<>();
        prefixMap.put(0L, 1);
        dfs(root, 0L, targetSum, prefixMap);
        return total;
    }
    private void dfs(TreeNode node, long curSum, int target, Map<Long, Integer> map) {
        if (node == null) return;
        curSum += node.val;
        total += map.getOrDefault(curSum - target, 0);
        map.put(curSum, map.getOrDefault(curSum, 0) + 1);
        dfs(node.left, curSum, target, map);
        dfs(node.right, curSum, target, map);
        map.put(curSum, map.get(curSum) - 1);
    }
}""",
                "python": """from collections import defaultdict

class Solution:
    def pathSum(self, root: TreeNode | None, targetSum: int) -> int:
        total = 0
        prefix_map = defaultdict(int)
        prefix_map[0] = 1
        def dfs(node: TreeNode | None, cur_sum: int):
            nonlocal total
            if not node:
                return
            cur_sum += node.val
            total += prefix_map[cur_sum - targetSum]
            prefix_map[cur_sum] += 1
            dfs(node.left, cur_sum)
            dfs(node.right, cur_sum)
            prefix_map[cur_sum] -= 1
        dfs(root, 0)
        return total"""
            }
        }
    },
    # 133: Count Good Nodes in Binary Tree
    {
        "seq": 133,
        "whyNext": "Path maximum tracking: node is good if node.val >= max value seen along path from root.",
        "brute": {
            "idea": "For every node, trace the path back to the root to verify whether node.val is the maximum.",
            "steps": [
                "Store parent pointers for all nodes using a hash map.",
                "For each node, traverse backwards to root; if any ancestor > node.val, it is not good.",
                "Count good nodes."
            ],
            "time": "O(n * h)",
            "space": "O(n)",
            "whySlow": "Tracing back to root repeatedly costs O(h) per node.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public int goodNodes(TreeNode root) {
        List<TreeNode> all = new ArrayList<>();
        Map<TreeNode, TreeNode> parent = new HashMap<>();
        collect(root, null, all, parent);
        int good = 0;
        for (TreeNode node : all) {
            boolean isGood = true;
            TreeNode cur = parent.get(node);
            while (cur != null) {
                if (cur.val > node.val) {
                    isGood = false;
                    break;
                }
                cur = parent.get(cur);
            }
            if (isGood) good++;
        }
        return good;
    }
    private void collect(TreeNode node, TreeNode par, List<TreeNode> all, Map<TreeNode, TreeNode> p) {
        if (node == null) return;
        all.add(node);
        p.put(node, par);
        collect(node.left, node, all, p);
        collect(node.right, node, all, p);
    }
}""",
                "python": """class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        parent = {}
        all_nodes = []
        def collect(node, p):
            if not node: return
            all_nodes.append(node)
            parent[node] = p
            collect(node.left, node)
            collect(node.right, node)
        collect(root, None)
        ans = 0
        for node in all_nodes:
            cur = parent[node]
            good = True
            while cur:
                if cur.val > node.val:
                    good = False
                    break
                cur = parent[cur]
            if good: ans += 1
        return ans"""
            }
        },
        "optimal": {
            "idea": "Pass running maximum down the DFS recursion tree: if node.val >= maxVal, increment count and update maxVal.",
            "steps": [
                "In dfs(node, maxVal): if node == null return 0.",
                "good = (node.val >= maxVal) ? 1 : 0.",
                "newMax = Math.max(maxVal, node.val).",
                "Return good + dfs(node.left, newMax) + dfs(node.right, newMax)."
            ],
            "time": "O(n)",
            "space": "O(h)",
            "code": {
                "java": """class Solution {
    public int goodNodes(TreeNode root) {
        return dfs(root, root.val);
    }
    private int dfs(TreeNode node, int maxVal) {
        if (node == null) return 0;
        int count = 0;
        if (node.val >= maxVal) {
            count = 1;
            maxVal = node.val;
        }
        return count + dfs(node.left, maxVal) + dfs(node.right, maxVal);
    }
}""",
                "python": """class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        def dfs(node: TreeNode | None, max_val: int) -> int:
            if not node:
                return 0
            count = 1 if node.val >= max_val else 0
            new_max = max(max_val, node.val)
            return count + dfs(node.left, new_max) + dfs(node.right, new_max)
        return dfs(root, root.val)"""
            }
        }
    },
    # 134: Binary Tree Maximum Path Sum
    {
        "seq": 134,
        "whyNext": "Builds on Diameter: max path sum can turn at any node (left_gain + val + right_gain); ignore negative subtree sums with max(0, gain).",
        "brute": {
            "idea": "For every node, consider it as the highest point of the path: compute max downward path from left child + node.val + right child.",
            "steps": [
                "For every node, calculate max path starting down left and max path starting down right.",
                "Sum them with node.val and update overall maximum.",
                "Recurse for all nodes in the tree."
            ],
            "time": "O(n^2)",
            "space": "O(h)",
            "whySlow": "Repeatedly computes downward subtree maximums at every ancestor.",
            "code": {
                "java": """class Solution {
    public int maxPathSum(TreeNode root) {
        if (root == null) return Integer.MIN_VALUE;
        int leftGain = Math.max(0, maxGain(root.left));
        int rightGain = Math.max(0, maxGain(root.right));
        int cur = root.val + leftGain + rightGain;
        return Math.max(cur, Math.max(maxPathSum(root.left), maxPathSum(root.right)));
    }
    private int maxGain(TreeNode node) {
        if (node == null) return 0;
        return node.val + Math.max(0, Math.max(maxGain(node.left), maxGain(node.right)));
    }
}""",
                "python": """class Solution:
    def maxPathSum(self, root: TreeNode | None) -> int:
        if not root:
            return float('-inf')
        def max_gain(node):
            if not node: return 0
            return node.val + max(0, max(max_gain(node.left), max_gain(node.right)))
        cur = root.val + max(0, max_gain(root.left)) + max(0, max_gain(root.right))
        return max(cur, self.maxPathSum(root.left), self.maxPathSum(root.right))"""
            }
        },
        "optimal": {
            "idea": "Post-order DFS: each node returns max single branch contribution (node.val + max(0, max(left, right))) while updating global max with left + right + node.val.",
            "steps": [
                "Initialize maxSum = Integer.MIN_VALUE.",
                "In dfs(node): if node == null return 0.",
                "leftGain = Math.max(0, dfs(node.left)).",
                "rightGain = Math.max(0, dfs(node.right)).",
                "maxSum = Math.max(maxSum, node.val + leftGain + rightGain).",
                "Return node.val + Math.max(leftGain, rightGain)."
            ],
            "time": "O(n)",
            "space": "O(h)",
            "code": {
                "java": """class Solution {
    private int maxSum = Integer.MIN_VALUE;
    public int maxPathSum(TreeNode root) {
        dfs(root);
        return maxSum;
    }
    private int dfs(TreeNode node) {
        if (node == null) return 0;
        int left = Math.max(0, dfs(node.left));
        int right = Math.max(0, dfs(node.right));
        maxSum = Math.max(maxSum, node.val + left + right);
        return node.val + Math.max(left, right);
    }
}""",
                "python": """class Solution:
    def maxPathSum(self, root: TreeNode | None) -> int:
        max_sum = float('-inf')
        def dfs(node: TreeNode | None) -> int:
            nonlocal max_sum
            if not node:
                return 0
            left = max(0, dfs(node.left))
            right = max(0, dfs(node.right))
            max_sum = max(max_sum, node.val + left + right)
            return node.val + max(left, right)
        dfs(root)
        return max_sum"""
            }
        }
    },
    # 135: Binary Tree Level Order Traversal
    {
        "seq": 135,
        "whyNext": "Canonical BFS queue traversal: process nodes level-by-level using queue snapshot size.",
        "brute": {
            "idea": "Perform DFS passing level index; append node values into a 2D array indexed by level.",
            "steps": [
                "Recursively visit nodes passing current level.",
                "If result.size() == level, append a new list.",
                "Add node.val to result.get(level)."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "whySlow": "Recursive call stack overhead instead of standard BFS queue.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> res = new ArrayList<>();
        dfs(root, 0, res);
        return res;
    }
    private void dfs(TreeNode node, int level, List<List<Integer>> res) {
        if (node == null) return;
        if (level == res.size()) res.add(new ArrayList<>());
        res.get(level).add(node.val);
        dfs(node.left, level + 1, res);
        dfs(node.right, level + 1, res);
    }
}""",
                "python": """class Solution:
    def levelOrder(self, root: TreeNode | None) -> list[list[int]]:
        res = []
        def dfs(node: TreeNode | None, level: int):
            if not node: return
            if level == len(res):
                res.append([])
            res[level].append(node.val)
            dfs(node.left, level + 1)
            dfs(node.right, level + 1)
        dfs(root, 0)
        return res"""
            }
        },
        "optimal": {
            "idea": "Iterative BFS with Queue: at each level, read queue.size(), process exactly that many nodes, and push their children.",
            "steps": [
                "If root == null return empty list.",
                "Push root into Queue.",
                "While queue is not empty: size = queue.size(), create level list.",
                "Poll size nodes, add vals to level, enqueue non-null left and right.",
                "Add level to res."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> res = new ArrayList<>();
        if (root == null) return res;
        Queue<TreeNode> q = new LinkedList<>();
        q.offer(root);
        while (!q.isEmpty()) {
            int size = q.size();
            List<Integer> level = new ArrayList<>(size);
            for (int i = 0; i < size; i++) {
                TreeNode node = q.poll();
                level.add(node.val);
                if (node.left != null) q.offer(node.left);
                if (node.right != null) q.offer(node.right);
            }
            res.add(level);
        }
        return res;
    }
}""",
                "python": """from collections import deque

class Solution:
    def levelOrder(self, root: TreeNode | None) -> list[list[int]]:
        if not root:
            return []
        res = []
        q = deque([root])
        while q:
            level = []
            for _ in range(len(q)):
                node = q.popleft()
                level.append(node.val)
                if node.left: q.append(node.left)
                if node.right: q.append(node.right)
            res.append(level)
        return res"""
            }
        }
    },
    # 136: Binary Tree Right Side View
    {
        "seq": 136,
        "whyNext": "Builds on Level Order: pick the last element of every level or use reverse preorder (root -> right -> left) DFS.",
        "brute": {
            "idea": "Run full level order traversal BFS, take the last element of each level array.",
            "steps": [
                "Execute BFS level order traversal.",
                "Extract last item from each level list."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "whySlow": "Stores all node values across all levels in memory just to inspect the rightmost one.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<Integer> rightSideView(TreeNode root) {
        List<Integer> res = new ArrayList<>();
        if (root == null) return res;
        Queue<TreeNode> q = new LinkedList<>();
        q.offer(root);
        while (!q.isEmpty()) {
            int size = q.size();
            int lastVal = 0;
            for (int i = 0; i < size; i++) {
                TreeNode node = q.poll();
                lastVal = node.val;
                if (node.left != null) q.offer(node.left);
                if (node.right != null) q.offer(node.right);
            }
            res.add(lastVal);
        }
        return res;
    }
}""",
                "python": """from collections import deque

class Solution:
    def rightSideView(self, root: TreeNode | None) -> list[int]:
        if not root: return []
        res = []
        q = deque([root])
        while q:
            val = 0
            for _ in range(len(q)):
                node = q.popleft()
                val = node.val
                if node.left: q.append(node.left)
                if node.right: q.append(node.right)
            res.append(val)
        return res"""
            }
        },
        "optimal": {
            "idea": "DFS visiting Right child before Left child: first node visited at each depth level is the rightmost node.",
            "steps": [
                "In dfs(node, depth): if node == null return.",
                "If depth == res.size(), add node.val to res (first time reaching this level from the right).",
                "Recurse right child: dfs(node.right, depth + 1).",
                "Recurse left child: dfs(node.left, depth + 1)."
            ],
            "time": "O(n)",
            "space": "O(h)",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<Integer> rightSideView(TreeNode root) {
        List<Integer> res = new ArrayList<>();
        dfs(root, 0, res);
        return res;
    }
    private void dfs(TreeNode node, int depth, List<Integer> res) {
        if (node == null) return;
        if (depth == res.size()) {
            res.add(node.val);
        }
        dfs(node.right, depth + 1, res);
        dfs(node.left, depth + 1, res);
    }
}""",
                "python": """class Solution:
    def rightSideView(self, root: TreeNode | None) -> list[int]:
        res = []
        def dfs(node: TreeNode | None, depth: int):
            if not node:
                return
            if depth == len(res):
                res.append(node.val)
            dfs(node.right, depth + 1)
            dfs(node.left, depth + 1)
        dfs(root, 0)
        return res"""
            }
        }
    },
    # 137: Binary Tree Zigzag Level Order Traversal
    {
        "seq": 137,
        "whyNext": "Builds on Level Order: alternate direction between left-to-right and right-to-left at each level.",
        "brute": {
            "idea": "Collect normal level order traversal; reverse odd-indexed level lists with Collections.reverse.",
            "steps": [
                "Perform normal level order BFS.",
                "For every level at odd index, reverse the list.",
                "Return result."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "whySlow": "Reversing list elements takes an extra traversal pass per level.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> zigzagLevelOrder(TreeNode root) {
        List<List<Integer>> res = new ArrayList<>();
        if (root == null) return res;
        Queue<TreeNode> q = new LinkedList<>();
        q.offer(root);
        boolean leftToRight = true;
        while (!q.isEmpty()) {
            int size = q.size();
            List<Integer> level = new ArrayList<>(size);
            for (int i = 0; i < size; i++) {
                TreeNode node = q.poll();
                level.add(node.val);
                if (node.left != null) q.offer(node.left);
                if (node.right != null) q.offer(node.right);
            }
            if (!leftToRight) Collections.reverse(level);
            res.add(level);
            leftToRight = !leftToRight;
        }
        return res;
    }
}""",
                "python": """from collections import deque

class Solution:
    def zigzagLevelOrder(self, root: TreeNode | None) -> list[list[int]]:
        if not root: return []
        res = []
        q = deque([root])
        left_to_right = True
        while q:
            level = []
            for _ in range(len(q)):
                node = q.popleft()
                level.append(node.val)
                if node.left: q.append(node.left)
                if node.right: q.append(node.right)
            if not left_to_right:
                level.reverse()
            res.append(level)
            left_to_right = not left_to_right
        return res"""
            }
        },
        "optimal": {
            "idea": "Use LinkedList / deque for each level: add to tail if left-to-right, add to head if right-to-left.",
            "steps": [
                "BFS with queue.",
                "Maintain boolean leftToRight = true.",
                "For each node in current level, if leftToRight append to tail, else prepend to head (addFirst).",
                "Toggle leftToRight flag after each level."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<List<Integer>> zigzagLevelOrder(TreeNode root) {
        List<List<Integer>> res = new ArrayList<>();
        if (root == null) return res;
        Queue<TreeNode> q = new LinkedList<>();
        q.offer(root);
        boolean leftToRight = true;
        while (!q.isEmpty()) {
            int size = q.size();
            LinkedList<Integer> level = new LinkedList<>();
            for (int i = 0; i < size; i++) {
                TreeNode node = q.poll();
                if (leftToRight) level.addLast(node.val);
                else level.addFirst(node.val);
                if (node.left != null) q.offer(node.left);
                if (node.right != null) q.offer(node.right);
            }
            res.add(level);
            leftToRight = !leftToRight;
        }
        return res;
    }
}""",
                "python": """from collections import deque

class Solution:
    def zigzagLevelOrder(self, root: TreeNode | None) -> list[list[int]]:
        if not root:
            return []
        res = []
        q = deque([root])
        left_to_right = True
        while q:
            level = deque()
            for _ in range(len(q)):
                node = q.popleft()
                if left_to_right:
                    level.append(node.val)
                else:
                    level.appendleft(node.val)
                if node.left: q.append(node.left)
                if node.right: q.append(node.right)
            res.append(list(level))
            left_to_right = not left_to_right
        return res"""
            }
        }
    },
    # 138: Binary Tree Inorder Traversal
    {
        "seq": 138,
        "whyNext": "LNR traversal: standard recursive vs iterative with explicit stack vs Morris traversal in O(1) space.",
        "brute": {
            "idea": "Simple recursion: visit left child, record node.val, visit right child.",
            "steps": [
                "If root == null return.",
                "Recurse left child.",
                "Add root.val to result list.",
                "Recurse right child."
            ],
            "time": "O(n)",
            "space": "O(h)",
            "whySlow": "Uses O(h) recursion stack frames.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<Integer> inorderTraversal(TreeNode root) {
        List<Integer> res = new ArrayList<>();
        dfs(root, res);
        return res;
    }
    private void dfs(TreeNode node, List<Integer> res) {
        if (node == null) return;
        dfs(node.left, res);
        res.add(node.val);
        dfs(node.right, res);
    }
}""",
                "python": """class Solution:
    def inorderTraversal(self, root: TreeNode | None) -> list[int]:
        res = []
        def dfs(node):
            if not node: return
            dfs(node.left)
            res.append(node.val)
            dfs(node.right)
        dfs(root)
        return res"""
            }
        },
        "optimal": {
            "idea": "Iterative stack traversal: push all left children to stack, pop to visit, then move to right child.",
            "steps": [
                "Initialize empty stack and cur = root.",
                "While cur != null or stack is not empty:",
                "While cur != null: stack.push(cur), cur = cur.left.",
                "cur = stack.pop(), res.add(cur.val), cur = cur.right."
            ],
            "time": "O(n)",
            "space": "O(h)",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<Integer> inorderTraversal(TreeNode root) {
        List<Integer> res = new ArrayList<>();
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode cur = root;
        while (cur != null || !stack.isEmpty()) {
            while (cur != null) {
                stack.push(cur);
                cur = cur.left;
            }
            cur = stack.pop();
            res.add(cur.val);
            cur = cur.right;
        }
        return res;
    }
}""",
                "python": """class Solution:
    def inorderTraversal(self, root: TreeNode | None) -> list[int]:
        res = []
        stack = []
        cur = root
        while cur or stack:
            while cur:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            res.append(cur.val)
            cur = cur.right
        return res"""
            }
        }
    },
    # 139: Binary Tree Preorder Traversal
    {
        "seq": 139,
        "whyNext": "NLR traversal: visit node immediately upon arrival, push right then left child to stack for iterative processing.",
        "brute": {
            "idea": "Standard recursive preorder traversal: visit node, then left child, then right child.",
            "steps": [
                "If root == null return.",
                "Add root.val to result list.",
                "dfs(node.left), dfs(node.right)."
            ],
            "time": "O(n)",
            "space": "O(h)",
            "whySlow": "Uses call stack instead of explicit iterative control.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<Integer> preorderTraversal(TreeNode root) {
        List<Integer> res = new ArrayList<>();
        dfs(root, res);
        return res;
    }
    private void dfs(TreeNode node, List<Integer> res) {
        if (node == null) return;
        res.add(node.val);
        dfs(node.left, res);
        dfs(node.right, res);
    }
}""",
                "python": """class Solution:
    def preorderTraversal(self, root: TreeNode | None) -> list[int]:
        res = []
        def dfs(node):
            if not node: return
            res.append(node.val)
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return res"""
            }
        },
        "optimal": {
            "idea": "Iterative stack: push root. While stack not empty: pop node, record val, push right child then left child.",
            "steps": [
                "If root == null return empty list.",
                "Stack with root.",
                "Pop node, add node.val to res.",
                "If node.right != null, push node.right.",
                "If node.left != null, push node.left."
            ],
            "time": "O(n)",
            "space": "O(h)",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<Integer> preorderTraversal(TreeNode root) {
        List<Integer> res = new ArrayList<>();
        if (root == null) return res;
        Deque<TreeNode> stack = new ArrayDeque<>();
        stack.push(root);
        while (!stack.isEmpty()) {
            TreeNode node = stack.pop();
            res.add(node.val);
            if (node.right != null) stack.push(node.right);
            if (node.left != null) stack.push(node.left);
        }
        return res;
    }
}""",
                "python": """class Solution:
    def preorderTraversal(self, root: TreeNode | None) -> list[int]:
        if not root:
            return []
        res = []
        stack = [root]
        while stack:
            node = stack.pop()
            res.append(node.val)
            if node.right: stack.append(node.right)
            if node.left: stack.append(node.left)
        return res"""
            }
        }
    },
    # 140: Construct Binary Tree from Preorder and Inorder Traversal
    {
        "seq": 140,
        "whyNext": "Combines Preorder and Inorder: preorder[0] is root; finding root in inorder splits left and right subtrees.",
        "brute": {
            "idea": "Linear scan inorder array to find root index; recursively build left and right subtrees using array slices.",
            "steps": [
                "Root val is preorder[0].",
                "Linear search root in inorder array to find index k.",
                "Slice preorder and inorder into left and right sub-arrays and recurse."
            ],
            "time": "O(n^2)",
            "space": "O(n^2)",
            "whySlow": "Linear scan for index and copying sub-arrays takes O(n) per node.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public TreeNode buildTree(int[] preorder, int[] inorder) {
        if (preorder.length == 0) return null;
        int rootVal = preorder[0];
        TreeNode root = new TreeNode(rootVal);
        int mid = 0;
        while (inorder[mid] != rootVal) mid++;
        root.left = buildTree(
            Arrays.copyOfRange(preorder, 1, 1 + mid),
            Arrays.copyOfRange(inorder, 0, mid)
        );
        root.right = buildTree(
            Arrays.copyOfRange(preorder, 1 + mid, preorder.length),
            Arrays.copyOfRange(inorder, mid + 1, inorder.length)
        );
        return root;
    }
}""",
                "python": """class Solution:
    def buildTree(self, preorder: list[int], inorder: list[int]) -> TreeNode | None:
        if not preorder or not inorder:
            return None
        val = preorder[0]
        root = TreeNode(val)
        mid = inorder.index(val)
        root.left = self.buildTree(preorder[1:mid+1], inorder[:mid])
        root.right = self.buildTree(preorder[mid+1:], inorder[mid+1:])
        return root"""
            }
        },
        "optimal": {
            "idea": "HashMap for O(1) inorder index lookups + index pointers avoids all array slicing.",
            "steps": [
                "Store (value -> index) mapping of inorder array in a HashMap.",
                "Maintain preIdx = 0 pointer.",
                "Define helper build(inStart, inEnd): if inStart > inEnd return null.",
                "rootVal = preorder[preIdx++], root = new TreeNode(rootVal), mid = map.get(rootVal).",
                "root.left = build(inStart, mid - 1); root.right = build(mid + 1, inEnd); return root."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "code": {
                "java": """import java.util.*;
class Solution {
    private int preIdx = 0;
    private Map<Integer, Integer> inMap = new HashMap<>();
    public TreeNode buildTree(int[] preorder, int[] inorder) {
        for (int i = 0; i < inorder.length; i++) {
            inMap.put(inorder[i], i);
        }
        return build(preorder, 0, inorder.length - 1);
    }
    private TreeNode build(int[] preorder, int inStart, int inEnd) {
        if (inStart > inEnd) return null;
        int rootVal = preorder[preIdx++];
        TreeNode root = new TreeNode(rootVal);
        int mid = inMap.get(rootVal);
        root.left = build(preorder, inStart, mid - 1);
        root.right = build(preorder, mid + 1, inEnd);
        return root;
    }
}""",
                "python": """class Solution:
    def buildTree(self, preorder: list[int], inorder: list[int]) -> TreeNode | None:
        in_map = {v: i for i, v in enumerate(inorder)}
        pre_idx = 0
        def build(in_start: int, in_end: int) -> TreeNode | None:
            nonlocal pre_idx
            if in_start > in_end:
                return None
            val = preorder[pre_idx]
            pre_idx += 1
            root = TreeNode(val)
            mid = in_map[val]
            root.left = build(in_start, mid - 1)
            root.right = build(mid + 1, in_end)
            return root
        return build(0, len(inorder) - 1)"""
            }
        }
    },
    # 141: Lowest Common Ancestor of a Binary Tree
    {
        "seq": 141,
        "whyNext": "LCA divide and conquer: if left and right subtrees both report finding targets, current node is their LCA.",
        "brute": {
            "idea": "Find root-to-p path and root-to-q path as node lists, then compare to find the last common node.",
            "steps": [
                "Find path from root to p.",
                "Find path from root to q.",
                "Walk both paths simultaneously; return last node they share."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "whySlow": "Stores entire paths in lists instead of short-circuiting in single recursive pass.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        List<TreeNode> pathP = new ArrayList<>();
        List<TreeNode> pathQ = new ArrayList<>();
        findPath(root, p, pathP);
        findPath(root, q, pathQ);
        TreeNode lca = null;
        int minLen = Math.min(pathP.size(), pathQ.size());
        for (int i = 0; i < minLen; i++) {
            if (pathP.get(i) == pathQ.get(i)) lca = pathP.get(i);
            else break;
        }
        return lca;
    }
    private boolean findPath(TreeNode node, TreeNode target, List<TreeNode> path) {
        if (node == null) return false;
        path.add(node);
        if (node == target) return true;
        if (findPath(node.left, target, path) || findPath(node.right, target, path)) return true;
        path.remove(path.size() - 1);
        return false;
    }
}""",
                "python": """class Solution:
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        def find_path(node, target, path):
            if not node: return False
            path.append(node)
            if node == target: return True
            if find_path(node.left, target, path) or find_path(node.right, target, path):
                return True
            path.pop()
            return False
        p_path, q_path = [], []
        find_path(root, p, p_path)
        find_path(root, q, q_path)
        lca = root
        for a, b in zip(p_path, q_path):
            if a == b: lca = a
            else: break
        return lca"""
            }
        },
        "optimal": {
            "idea": "Single-pass DFS: if root is null, p, or q, return root. Recurse left and right: if both non-null, root is LCA.",
            "steps": [
                "If root == null || root == p || root == q, return root.",
                "left = lowestCommonAncestor(root.left, p, q).",
                "right = lowestCommonAncestor(root.right, p, q).",
                "If left != null && right != null, return root.",
                "Return left != null ? left : right."
            ],
            "time": "O(n)",
            "space": "O(h)",
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
        if left and right:
            return root
        return left if left else right"""
            }
        }
    },
    # 142: Flatten Binary Tree to Linked List
    {
        "seq": 142,
        "whyNext": "Tree restructuring: rearrange pointers so right child forms preorder linked list and left child is null.",
        "brute": {
            "idea": "Perform preorder traversal into a list of nodes, then rewire node.right = list[i+1] and node.left = null.",
            "steps": [
                "Traverse tree preorder into a list.",
                "Loop through list rewiring pointers."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "whySlow": "Requires O(n) auxiliary memory to hold all tree nodes.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public void flatten(TreeNode root) {
        if (root == null) return;
        List<TreeNode> list = new ArrayList<>();
        preorder(root, list);
        for (int i = 0; i < list.size() - 1; i++) {
            list.get(i).left = null;
            list.get(i).right = list.get(i + 1);
        }
        list.get(list.size() - 1).left = null;
        list.get(list.size() - 1).right = null;
    }
    private void preorder(TreeNode node, List<TreeNode> list) {
        if (node == null) return;
        list.add(node);
        preorder(node.left, list);
        preorder(node.right, list);
    }
}""",
                "python": """class Solution:
    def flatten(self, root: TreeNode | None) -> None:
        if not root: return
        nodes = []
        def preorder(node):
            if not node: return
            nodes.append(node)
            preorder(node.left)
            preorder(node.right)
        preorder(root)
        for i in range(len(nodes) - 1):
            nodes[i].left = None
            nodes[i].right = nodes[i + 1]
        nodes[-1].left = None
        nodes[-1].right = None"""
            }
        },
        "optimal": {
            "idea": "Morris-style pointer rewiring in O(1) space: at cur with left child, find rightmost node of cur.left and connect to cur.right.",
            "steps": [
                "While cur != null:",
                "If cur.left != null: find rightmost node of cur.left.",
                "Attach cur.right to rightmost.right, set cur.right = cur.left, cur.left = null.",
                "Advance cur = cur.right."
            ],
            "time": "O(n)",
            "space": "O(1)",
            "code": {
                "java": """class Solution {
    public void flatten(TreeNode root) {
        TreeNode cur = root;
        while (cur != null) {
            if (cur.left != null) {
                TreeNode rightmost = cur.left;
                while (rightmost.right != null) {
                    rightmost = rightmost.right;
                }
                rightmost.right = cur.right;
                cur.right = cur.left;
                cur.left = null;
            }
            cur = cur.right;
        }
    }
}""",
                "python": """class Solution:
    def flatten(self, root: TreeNode | None) -> None:
        cur = root
        while cur:
            if cur.left:
                rightmost = cur.left
                while rightmost.right:
                    rightmost = rightmost.right
                rightmost.right = cur.right
                cur.right = cur.left
                cur.left = None
            cur = cur.right"""
            }
        }
    },
    # 143: Serialize and Deserialize Binary Tree
    {
        "seq": 143,
        "whyNext": "Full tree serialization and reconstruction: encode tree into string representation and parse back.",
        "brute": {
            "idea": "Level-order serialization with null markers; reconstruct using queue by levels.",
            "steps": [
                "BFS level order: serialize every node value or 'null'.",
                "Deserialize: split by delimiter, use queue to attach children."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "whySlow": "Stores null placeholders for all leaf children in BFS queue.",
            "code": {
                "java": """import java.util.*;
public class Codec {
    public String serialize(TreeNode root) {
        if (root == null) return "";
        StringBuilder sb = new StringBuilder();
        Queue<TreeNode> q = new LinkedList<>();
        q.offer(root);
        while (!q.isEmpty()) {
            TreeNode node = q.poll();
            if (node == null) {
                sb.append("null,");
            } else {
                sb.append(node.val).append(",");
                q.offer(node.left);
                q.offer(node.right);
            }
        }
        return sb.toString();
    }

    public TreeNode deserialize(String data) {
        if (data.isEmpty()) return null;
        String[] vals = data.split(",");
        TreeNode root = new TreeNode(Integer.parseInt(vals[0]));
        Queue<TreeNode> q = new LinkedList<>();
        q.offer(root);
        int i = 1;
        while (!q.isEmpty() && i < vals.length) {
            TreeNode parent = q.poll();
            if (!vals[i].equals("null")) {
                parent.left = new TreeNode(Integer.parseInt(vals[i]));
                q.offer(parent.left);
            }
            i++;
            if (i < vals.length && !vals[i].equals("null")) {
                parent.right = new TreeNode(Integer.parseInt(vals[i]));
                q.offer(parent.right);
            }
            i++;
        }
        return root;
    }
}""",
                "python": """from collections import deque

class Codec:
    def serialize(self, root):
        if not root: return ""
        q = deque([root])
        res = []
        while q:
            node = q.popleft()
            if node:
                res.append(str(node.val))
                q.append(node.left)
                q.append(node.right)
            else:
                res.append("null")
        return ",".join(res)

    def deserialize(self, data):
        if not data: return None
        vals = data.split(",")
        root = TreeNode(int(vals[0]))
        q = deque([root])
        i = 1
        while q and i < len(vals):
            node = q.popleft()
            if vals[i] != "null":
                node.left = TreeNode(int(vals[i]))
                q.append(node.left)
            i += 1
            if i < len(vals) and vals[i] != "null":
                node.right = TreeNode(int(vals[i]))
                q.append(node.right)
            i += 1
        return root"""
            }
        },
        "optimal": {
            "idea": "Preorder DFS with '#' for null: serialize root->left->right; deserialize recursively consuming queue or iterator.",
            "steps": [
                "serialize: if node == null append '#,'; else append node.val + ',' and recurse left then right.",
                "deserialize: split data by ',', place tokens in a Queue, and recursively build nodes.",
                "In helper: poll token; if token is '#', return null; else make TreeNode and recurse left then right."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "code": {
                "java": """import java.util.*;
public class Codec {
    public String serialize(TreeNode root) {
        StringBuilder sb = new StringBuilder();
        buildString(root, sb);
        return sb.toString();
    }
    private void buildString(TreeNode node, StringBuilder sb) {
        if (node == null) {
            sb.append("#,");
        } else {
            sb.append(node.val).append(",");
            buildString(node.left, sb);
            buildString(node.right, sb);
        }
    }

    public TreeNode deserialize(String data) {
        Queue<String> nodes = new LinkedList<>(Arrays.asList(data.split(",")));
        return buildTree(nodes);
    }
    private TreeNode buildTree(Queue<String> nodes) {
        String val = nodes.poll();
        if (val == null || val.equals("#")) return null;
        TreeNode node = new TreeNode(Integer.parseInt(val));
        node.left = buildTree(nodes);
        node.right = buildTree(nodes);
        return node;
    }
}""",
                "python": """class Codec:
    def serialize(self, root):
        res = []
        def dfs(node):
            if not node:
                res.append("#")
                return
            res.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return ",".join(res)

    def deserialize(self, data):
        tokens = iter(data.split(","))
        def build():
            val = next(tokens)
            if val == "#":
                return None
            node = TreeNode(int(val))
            node.left = build()
            node.right = build()
            return node
        return build()"""
            }
        }
    },
    # 144: All Nodes Distance K in Binary Tree
    {
        "seq": 144,
        "whyNext": "Converts binary tree to undirected graph: traverse parents and children with BFS up to distance k.",
        "brute": {
            "idea": "Convert entire tree into an adjacency list graph, then run standard BFS from target node.",
            "steps": [
                "Build graph (Map<Integer, List<Integer>>) using DFS on tree.",
                "Run BFS from target.val up to k steps, tracking visited nodes.",
                "Return nodes at layer k."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "whySlow": "Allocates an entirely new adjacency list structure for all nodes.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<Integer> distanceK(TreeNode root, TreeNode target, int k) {
        Map<Integer, List<Integer>> graph = new HashMap<>();
        buildGraph(root, null, graph);
        List<Integer> res = new ArrayList<>();
        Set<Integer> visited = new HashSet<>();
        Queue<Integer> q = new LinkedList<>();
        q.offer(target.val);
        visited.add(target.val);
        int dist = 0;
        while (!q.isEmpty()) {
            if (dist == k) {
                res.addAll(q);
                return res;
            }
            int size = q.size();
            for (int i = 0; i < size; i++) {
                int cur = q.poll();
                for (int neighbor : graph.getOrDefault(cur, Collections.emptyList())) {
                    if (visited.add(neighbor)) {
                        q.offer(neighbor);
                    }
                }
            }
            dist++;
        }
        return res;
    }
    private void buildGraph(TreeNode node, TreeNode par, Map<Integer, List<Integer>> g) {
        if (node == null) return;
        g.putIfAbsent(node.val, new ArrayList<>());
        if (par != null) {
            g.get(node.val).add(par.val);
            g.get(par.val).add(node.val);
        }
        buildGraph(node.left, node, g);
        buildGraph(node.right, node, g);
    }
}""",
                "python": """from collections import deque, defaultdict

class Solution:
    def distanceK(self, root: TreeNode, target: TreeNode, k: int) -> list[int]:
        graph = defaultdict(list)
        def build(node, parent):
            if not node: return
            if parent:
                graph[node.val].append(parent.val)
                graph[parent.val].append(node.val)
            build(node.left, node)
            build(node.right, node)
        build(root, None)
        q = deque([target.val])
        visited = {target.val}
        dist = 0
        while q:
            if dist == k: return list(q)
            for _ in range(len(q)):
                cur = q.popleft()
                for nxt in graph[cur]:
                    if nxt not in visited:
                        visited.add(nxt)
                        q.append(nxt)
            dist += 1
        return []"""
            }
        },
        "optimal": {
            "idea": "Parent map + BFS: store parent pointers in Map<TreeNode, TreeNode>, then launch BFS from target node.",
            "steps": [
                "Map each TreeNode to its parent using DFS.",
                "Queue with target node and visited Set with target.",
                "Run BFS: expand to left, right, and parent.",
                "Stop at step k and return nodes in queue."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "code": {
                "java": """import java.util.*;
class Solution {
    public List<Integer> distanceK(TreeNode root, TreeNode target, int k) {
        Map<TreeNode, TreeNode> parentMap = new HashMap<>();
        populateParents(root, null, parentMap);
        Queue<TreeNode> q = new LinkedList<>();
        Set<TreeNode> visited = new HashSet<>();
        q.offer(target);
        visited.add(target);
        int dist = 0;
        while (!q.isEmpty()) {
            if (dist == k) {
                List<Integer> res = new ArrayList<>();
                for (TreeNode n : q) res.add(n.val);
                return res;
            }
            int size = q.size();
            for (int i = 0; i < size; i++) {
                TreeNode node = q.poll();
                if (node.left != null && visited.add(node.left)) q.offer(node.left);
                if (node.right != null && visited.add(node.right)) q.offer(node.right);
                TreeNode p = parentMap.get(node);
                if (p != null && visited.add(p)) q.offer(p);
            }
            dist++;
        }
        return Collections.emptyList();
    }
    private void populateParents(TreeNode node, TreeNode parent, Map<TreeNode, TreeNode> map) {
        if (node == null) return;
        if (parent != null) map.put(node, parent);
        populateParents(node.left, node, map);
        populateParents(node.right, node, map);
    }
}""",
                "python": """from collections import deque

class Solution:
    def distanceK(self, root: TreeNode, target: TreeNode, k: int) -> list[int]:
        parents = {}
        def map_parents(node, par):
            if not node: return
            if par: parents[node] = par
            map_parents(node.left, node)
            map_parents(node.right, node)
        map_parents(root, None)
        q = deque([target])
        visited = {target}
        dist = 0
        while q:
            if dist == k:
                return [n.val for n in q]
            for _ in range(len(q)):
                node = q.popleft()
                for neighbor in (node.left, node.right, parents.get(node)):
                    if neighbor and neighbor not in visited:
                        visited.add(neighbor)
                        q.append(neighbor)
            dist += 1
        return []"""
            }
        }
    },
    # 145: Maximum Width of Binary Tree
    {
        "seq": 145,
        "whyNext": "Binary heap indexing: assign 1-based index (left = 2*i, right = 2*i + 1); normalize indices per level to avoid overflow.",
        "brute": {
            "idea": "Full BFS queue storing nulls for missing nodes; measure width between first and last non-null node on each level.",
            "steps": [
                "Enqueue nulls for missing branches.",
                "For each level, find distance between first and last non-null node."
            ],
            "time": "O(2^h)",
            "space": "O(2^h)",
            "whySlow": "Generates exponential number of null placeholder nodes, leading to memory limit exceeded.",
            "code": {
                "java": """import java.util.*;
class Solution {
    public int widthOfBinaryTree(TreeNode root) {
        if (root == null) return 0;
        List<Integer> firstIndex = new ArrayList<>();
        return dfs(root, 0, 1, firstIndex);
    }
    private int dfs(TreeNode node, int level, int index, List<Integer> firstIndex) {
        if (node == null) return 0;
        if (level == firstIndex.size()) firstIndex.add(index);
        int cur = index - firstIndex.get(level) + 1;
        int left = dfs(node.left, level + 1, 2 * index, firstIndex);
        int right = dfs(node.right, level + 1, 2 * index + 1, firstIndex);
        return Math.max(cur, Math.max(left, right));
    }
}""",
                "python": """class Solution:
    def widthOfBinaryTree(self, root: TreeNode | None) -> int:
        if not root: return 0
        first_idx = []
        def dfs(node, level, idx):
            if not node: return 0
            if level == len(first_idx):
                first_idx.append(idx)
            cur = idx - first_idx[level] + 1
            left = dfs(node.left, level + 1, 2 * idx)
            right = dfs(node.right, level + 1, 2 * idx + 1)
            return max(cur, left, right)
        return dfs(root, 0, 1)"""
            }
        },
        "optimal": {
            "idea": "BFS level order with normalized index pairs (node, index): width = last_index - first_index + 1.",
            "steps": [
                "Queue storing pairs (TreeNode, long index).",
                "At each level, offset = q.peek().index to keep numbers small and prevent 64-bit integer overflow.",
                "First index is q.peek().index - offset; track last index.",
                "Push children with 2 * (index - offset) and 2 * (index - offset) + 1.",
                "Update maxWidth = max(maxWidth, last - first + 1)."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "code": {
                "java": """import java.util.*;
class Solution {
    public int widthOfBinaryTree(TreeNode root) {
        if (root == null) return 0;
        Queue<Pair> q = new LinkedList<>();
        q.offer(new Pair(root, 0L));
        int maxWidth = 0;
        while (!q.isEmpty()) {
            int size = q.size();
            long offset = q.peek().index;
            long first = 0, last = 0;
            for (int i = 0; i < size; i++) {
                Pair p = q.poll();
                long curIdx = p.index - offset;
                if (i == 0) first = curIdx;
                if (i == size - 1) last = curIdx;
                if (p.node.left != null) q.offer(new Pair(p.node.left, 2 * curIdx + 1));
                if (p.node.right != null) q.offer(new Pair(p.node.right, 2 * curIdx + 2));
            }
            maxWidth = Math.max(maxWidth, (int)(last - first + 1));
        }
        return maxWidth;
    }
    static class Pair {
        TreeNode node;
        long index;
        Pair(TreeNode n, long i) { node = n; index = i; }
    }
}""",
                "python": """from collections import deque

class Solution:
    def widthOfBinaryTree(self, root: TreeNode | None) -> int:
        if not root:
            return 0
        q = deque([(root, 0)])
        max_width = 0
        while q:
            size = len(q)
            offset = q[0][1]
            first = last = 0
            for i in range(size):
                node, idx = q.popleft()
                cur = idx - offset
                if i == 0: first = cur
                if i == size - 1: last = cur
                if node.left: q.append((node.left, 2 * cur + 1))
                if node.right: q.append((node.right, 2 * cur + 2))
            max_width = max(max_width, last - first + 1)
        return max_width"""
            }
        }
    },
    # 146: Count Complete Tree Nodes
    {
        "seq": 146,
        "whyNext": "Exploits complete binary tree structure: if left depth equals right depth, left subtree is full (2^h - 1) in O(log^2 n).",
        "brute": {
            "idea": "Standard recursive DFS counting every node 1 + count(left) + count(right).",
            "steps": [
                "If root == null return 0.",
                "Return 1 + countNodes(root.left) + countNodes(root.right)."
            ],
            "time": "O(n)",
            "space": "O(h)",
            "whySlow": "Visits every node linearly without exploiting the complete tree geometry.",
            "code": {
                "java": """class Solution {
    public int countNodes(TreeNode root) {
        if (root == null) return 0;
        return 1 + countNodes(root.left) + countNodes(root.right);
    }
}""",
                "python": """class Solution:
    def countNodes(self, root: TreeNode | None) -> int:
        if not root:
            return 0
        return 1 + self.countNodes(root.left) + self.countNodes(root.right)"""
            }
        },
        "optimal": {
            "idea": "Binary search on complete tree: compare left depth and right depth. If equal, left subtree is full 2^h; else right subtree is full 2^(h-1).",
            "steps": [
                "Find leftmost depth leftH and rightmost depth rightH.",
                "If leftH == rightH, node count is (1 << leftH) - 1.",
                "Otherwise, return 1 + countNodes(root.left) + countNodes(root.right)."
            ],
            "time": "O(log^2 n)",
            "space": "O(log n)",
            "code": {
                "java": """class Solution {
    public int countNodes(TreeNode root) {
        if (root == null) return 0;
        int leftH = getLeftHeight(root);
        int rightH = getRightHeight(root);
        if (leftH == rightH) {
            return (1 << leftH) - 1;
        }
        return 1 + countNodes(root.left) + countNodes(root.right);
    }
    private int getLeftHeight(TreeNode node) {
        int h = 0;
        while (node != null) { h++; node = node.left; }
        return h;
    }
    private int getRightHeight(TreeNode node) {
        int h = 0;
        while (node != null) { h++; node = node.right; }
        return h;
    }
}""",
                "python": """class Solution:
    def countNodes(self, root: TreeNode | None) -> int:
        if not root:
            return 0
        def left_h(node):
            h = 0
            while node:
                h += 1
                node = node.left
            return h
        def right_h(node):
            h = 0
            while node:
                h += 1
                node = node.right
            return h
        lh = left_h(root)
        rh = right_h(root)
        if lh == rh:
            return (1 << lh) - 1
        return 1 + self.countNodes(root.left) + self.countNodes(root.right)"""
            }
        }
    },
    # 147: House Robber III
    {
        "seq": 147,
        "whyNext": "Tree DP: each node returns pair [rob_node, skip_node]; rob_node includes children skip, skip_node takes max of each child.",
        "brute": {
            "idea": "Recursion: either rob root + grandchildren, or rob left child + right child.",
            "steps": [
                "If root == null return 0.",
                "Calculate robRoot = root.val + grandchildren sums.",
                "Calculate skipRoot = rob(root.left) + rob(root.right).",
                "Return max(robRoot, skipRoot)."
            ],
            "time": "O(2^n)",
            "space": "O(h)",
            "whySlow": "Recomputes values of grandchildren and children redundantly across branches.",
            "code": {
                "java": """class Solution {
    public int rob(TreeNode root) {
        if (root == null) return 0;
        int robRoot = root.val;
        if (root.left != null) {
            robRoot += rob(root.left.left) + rob(root.left.right);
        }
        if (root.right != null) {
            robRoot += rob(root.right.left) + rob(root.right.right);
        }
        int skipRoot = rob(root.left) + rob(root.right);
        return Math.max(robRoot, skipRoot);
    }
}""",
                "python": """class Solution:
    def rob(self, root: TreeNode | None) -> int:
        if not root:
            return 0
        rob_root = root.val
        if root.left:
            rob_root += self.rob(root.left.left) + self.rob(root.left.right)
        if root.right:
            rob_root += self.rob(root.right.left) + self.rob(root.right.right)
        skip_root = self.rob(root.left) + self.rob(root.right)
        return max(rob_root, skip_root)"""
            }
        },
        "optimal": {
            "idea": "Post-order Tree DP returning int[2] = {rob_node, not_rob_node} in a single pass.",
            "steps": [
                "In dfs(node): returns int[]{robThis, skipThis}.",
                "If node == null return {0, 0}.",
                "left = dfs(node.left), right = dfs(node.right).",
                "robThis = node.val + left[1] + right[1].",
                "skipThis = max(left[0], left[1]) + max(right[0], right[1]).",
                "Return {robThis, skipThis}."
            ],
            "time": "O(n)",
            "space": "O(h)",
            "code": {
                "java": """class Solution {
    public int rob(TreeNode root) {
        int[] res = dfs(root);
        return Math.max(res[0], res[1]);
    }
    private int[] dfs(TreeNode node) {
        if (node == null) return new int[]{0, 0};
        int[] left = dfs(node.left);
        int[] right = dfs(node.right);
        int robThis = node.val + left[1] + right[1];
        int skipThis = Math.max(left[0], left[1]) + Math.max(right[0], right[1]);
        return new int[]{robThis, skipThis};
    }
}""",
                "python": """class Solution:
    def rob(self, root: TreeNode | None) -> int:
        def dfs(node: TreeNode | None) -> tuple[int, int]:
            if not node:
                return (0, 0)
            l_rob, l_skip = dfs(node.left)
            r_rob, r_skip = dfs(node.right)
            rob_this = node.val + l_skip + r_skip
            skip_this = max(l_rob, l_skip) + max(r_rob, r_skip)
            return (rob_this, skip_this)
        return max(dfs(root))"""
            }
        }
    },
    # 148: Search in a Binary Search Tree
    {
        "seq": 148,
        "whyNext": "Entry to Chapter 9 (Binary Search Tree): BST invariant left < root < right enables binary search in tree.",
        "brute": {
            "idea": "Blind tree traversal searching both children ignoring the BST ordering property.",
            "steps": [
                "Check if root == null or root.val == val.",
                "Recurse left child; if found return.",
                "Recurse right child."
            ],
            "time": "O(n)",
            "space": "O(h)",
            "whySlow": "Searches both branches instead of using BST property to prune one branch.",
            "code": {
                "java": """class Solution {
    public TreeNode searchBST(TreeNode root, int val) {
        if (root == null || root.val == val) return root;
        TreeNode left = searchBST(root.left, val);
        if (left != null) return left;
        return searchBST(root.right, val);
    }
}""",
                "python": """class Solution:
    def searchBST(self, root: TreeNode | None, val: int) -> TreeNode | None:
        if not root or root.val == val:
            return root
        left = self.searchBST(root.left, val)
        return left if left else self.searchBST(root.right, val)"""
            }
        },
        "optimal": {
            "idea": "Iterative BST search: if val < cur.val go left, if val > cur.val go right; achieves O(1) extra space.",
            "steps": [
                "While cur != null and cur.val != val:",
                "cur = (val < cur.val) ? cur.left : cur.right.",
                "Return cur."
            ],
            "time": "O(h)",
            "space": "O(1)",
            "code": {
                "java": """class Solution {
    public TreeNode searchBST(TreeNode root, int val) {
        TreeNode cur = root;
        while (cur != null && cur.val != val) {
            cur = (val < cur.val) ? cur.left : cur.right;
        }
        return cur;
    }
}""",
                "python": """class Solution:
    def searchBST(self, root: TreeNode | None, val: int) -> TreeNode | None:
        cur = root
        while cur and cur.val != val:
            cur = cur.left if val < cur.val else cur.right
        return cur"""
            }
        }
    },
    # 149: Validate Binary Search Tree
    {
        "seq": 149,
        "whyNext": "BST property validation: every node must satisfy minVal < node.val < maxVal across its entire ancestor chain.",
        "brute": {
            "idea": "For every node, check that max of left subtree < node.val and min of right subtree > node.val.",
            "steps": [
                "Find maxValue in left subtree and minValue in right subtree.",
                "Verify leftMax < node.val < rightMin.",
                "Recurse for children."
            ],
            "time": "O(n^2)",
            "space": "O(h)",
            "whySlow": "Recalculates subtree minimums and maximums repeatedly at each level.",
            "code": {
                "java": """class Solution {
    public boolean isValidBST(TreeNode root) {
        if (root == null) return true;
        if (root.left != null && maxValue(root.left) >= root.val) return false;
        if (root.right != null && minValue(root.right) <= root.val) return false;
        return isValidBST(root.left) && isValidBST(root.right);
    }
    private long maxValue(TreeNode node) {
        if (node == null) return Long.MIN_VALUE;
        return Math.max(node.val, Math.max(maxValue(node.left), maxValue(node.right)));
    }
    private long minValue(TreeNode node) {
        if (node == null) return Long.MAX_VALUE;
        return Math.min(node.val, Math.min(minValue(node.left), minValue(node.right)));
    }
}""",
                "python": """class Solution:
    def isValidBST(self, root: TreeNode | None) -> bool:
        if not root: return True
        def max_val(node):
            if not node: return float('-inf')
            return max(node.val, max_val(node.left), max_val(node.right))
        def min_val(node):
            if not node: return float('inf')
            return min(node.val, min_val(node.left), min_val(node.right))
        if root.left and max_val(root.left) >= root.val: return False
        if root.right and min_val(root.right) <= root.val: return False
        return self.isValidBST(root.left) and self.isValidBST(root.right)"""
            }
        },
        "optimal": {
            "idea": "Top-down recursion passing valid range (lower, upper); every node must satisfy lower < node.val < upper.",
            "steps": [
                "Helper validate(node, Long min, Long max).",
                "If node == null return true.",
                "If node.val <= min || node.val >= max return false.",
                "Return validate(node.left, min, node.val) && validate(node.right, node.val, max)."
            ],
            "time": "O(n)",
            "space": "O(h)",
            "code": {
                "java": """class Solution {
    public boolean isValidBST(TreeNode root) {
        return validate(root, null, null);
    }
    private boolean validate(TreeNode node, Integer min, Integer max) {
        if (node == null) return true;
        if (min != null && node.val <= min) return false;
        if (max != null && node.val >= max) return false;
        return validate(node.left, min, node.val) && validate(node.right, node.val, max);
    }
}""",
                "python": """class Solution:
    def isValidBST(self, root: TreeNode | None) -> bool:
        def validate(node: TreeNode | None, low: float, high: float) -> bool:
            if not node:
                return True
            if not (low < node.val < high):
                return False
            return validate(node.left, low, node.val) and validate(node.right, node.val, high)
        return validate(root, float('-inf'), float('inf'))"""
            }
        }
    },
    # 150: Insert into a Binary Search Tree
    {
        "seq": 150,
        "whyNext": "BST insertion: traverse until finding null position maintaining BST invariant, attach new TreeNode(val).",
        "brute": {
            "idea": "Collect all nodes into a sorted list, insert val into list, and rebuild balanced BST.",
            "steps": [
                "Inorder traversal to get sorted list.",
                "Insert val in sorted order.",
                "Reconstruct BST from sorted list."
            ],
            "time": "O(n)",
            "space": "O(n)",
            "whySlow": "Allocates array and completely rebuilds tree instead of inserting at a leaf in O(h).",
            "code": {
                "java": """import java.util.*;
class Solution {
    public TreeNode insertIntoBST(TreeNode root, int val) {
        List<Integer> list = new ArrayList<>();
        inorder(root, list);
        int pos = 0;
        while (pos < list.size() && list.get(pos) < val) pos++;
        list.add(pos, val);
        return build(list, 0, list.size() - 1);
    }
    private void inorder(TreeNode node, List<Integer> list) {
        if (node == null) return;
        inorder(node.left, list);
        list.add(node.val);
        inorder(node.right, list);
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
    def insertIntoBST(self, root: TreeNode | None, val: int) -> TreeNode | None:
        vals = []
        def inorder(node):
            if not node: return
            inorder(node.left)
            vals.append(node.val)
            inorder(node.right)
        inorder(root)
        import bisect
        bisect.insort(vals, val)
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
            "idea": "Iterative BST insertion: navigate down tree comparing val with cur.val; attach new leaf when target child is null.",
            "steps": [
                "If root == null return new TreeNode(val).",
                "cur = root.",
                "While true: if val < cur.val: if cur.left == null { cur.left = new TreeNode(val); break; } else cur = cur.left.",
                "Else: if cur.right == null { cur.right = new TreeNode(val); break; } else cur = cur.right.",
                "Return root."
            ],
            "time": "O(h)",
            "space": "O(1)",
            "code": {
                "java": """class Solution {
    public TreeNode insertIntoBST(TreeNode root, int val) {
        if (root == null) return new TreeNode(val);
        TreeNode cur = root;
        while (true) {
            if (val < cur.val) {
                if (cur.left == null) {
                    cur.left = new TreeNode(val);
                    break;
                }
                cur = cur.left;
            } else {
                if (cur.right == null) {
                    cur.right = new TreeNode(val);
                    break;
                }
                cur = cur.right;
            }
        }
        return root;
    }
}""",
                "python": """class Solution:
    def insertIntoBST(self, root: TreeNode | None, val: int) -> TreeNode | None:
        if not root:
            return TreeNode(val)
        cur = root
        while True:
            if val < cur.val:
                if not cur.left:
                    cur.left = TreeNode(val)
                    break
                cur = cur.left
            else:
                if not cur.right:
                    cur.right = TreeNode(val)
                    break
                cur = cur.right
        return root"""
            }
        }
    }
]

with open('scripts/batches/batch_06.py', 'w', encoding='utf-8') as f:
    f.write("# Batch 6: Questions 126 to 150\n\n")
    f.write("def get_batch():\n")
    f.write("    return " + json.dumps(batch_6, indent=4) + "\n")

print("Wrote scripts/batches/batch_06.py with", len(batch_6), "questions.")


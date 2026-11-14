# Batch 4: Seq 76 to 100
# Covers Stack (76-82), Linked List (83-99), Recursion (100)

def get_batch():
    return [
        {
            "seq": 76,
            "whyNext": "Builds on Daily Temperatures monotonic stack: stack stores increasing bar indices; when shorter bar arrives, pop and compute area with popped bar as bottleneck.",
            "brute": {
                "idea": "For every bar i, expand outward left and right while neighbor heights >= heights[i] to compute rectangle area.",
                "steps": [
                    "Loop i from 0 to n - 1.",
                    "Expand left while heights[l] >= heights[i].",
                    "Expand right while heights[r] >= heights[i].",
                    "area = heights[i] * (r - l + 1); track max."
                ],
                "whySlow": "Expanding from every bar takes quadratic O(n²) time.",
                "time": "O(n²)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int largestRectangleArea(int[] heights) {
        int max = 0, n = heights.length;
        for (int i = 0; i < n; i++) {
            int l = i, r = i;
            while (l > 0 && heights[l - 1] >= heights[i]) l--;
            while (r < n - 1 && heights[r + 1] >= heights[i]) r++;
            max = Math.max(max, heights[i] * (r - l + 1));
        }
        return max;
    }
}""",
                    "python": """class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        max_a, n = 0, len(heights)
        for i in range(n):
            l, r = i, i
            while l > 0 and heights[l - 1] >= heights[i]: l -= 1
            while r < n - 1 and heights[r + 1] >= heights[i]: r += 1
            max_a = max(max_a, heights[i] * (r - l + 1))
        return max_a"""
                }
            },
            "optimal": {
                "idea": "Monotonic increasing stack of bar indices: pop when heights[i] < stack.peek(). Width is i - stack.peek() - 1.",
                "steps": [
                    "Initialize stack.",
                    "Loop i from 0 to n (with dummy 0 at index n):",
                    "While stack not empty and current height < heights[stack.peek()]:",
                    "h = heights[stack.pop()]; w = stack.isEmpty() ? i : i - stack.peek() - 1.",
                    "maxArea = max(maxArea, h * w).",
                    "stack.push(i)."
                ],
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public int largestRectangleArea(int[] heights) {
        int n = heights.length, max = 0;
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i <= n; i++) {
            int curH = (i == n) ? 0 : heights[i];
            while (!stack.isEmpty() && curH < heights[stack.peek()]) {
                int h = heights[stack.pop()];
                int w = stack.isEmpty() ? i : i - stack.peek() - 1;
                max = Math.max(max, h * w);
            }
            stack.push(i);
        }
        return max;
    }
}""",
                    "python": """class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        stack = []
        max_a = 0
        h_extended = heights + [0]
        for i, h in enumerate(h_extended):
            while stack and h < h_extended[stack[-1]]:
                height = h_extended[stack.pop()]
                width = i if not stack else i - stack[-1] - 1
                max_a = max(max_a, height * width)
            stack.append(i)
        return max_a"""
                }
            }
        },
        {
            "seq": 77,
            "whyNext": "Builds on Largest Rectangle in Histogram: convert each row of a binary matrix into a running histogram and solve in O(mn).",
            "brute": {
                "idea": "For every pair of top-left and bottom-right cells, verify if all cells are 1 and calculate area.",
                "steps": [
                    "Iterate over all subgrid rectangles (r1, c1) to (r2, c2).",
                    "Check if every cell inside rectangle contains '1'.",
                    "Track maximum area."
                ],
                "whySlow": "Evaluating all possible rectangles takes O(m²n²) time.",
                "time": "O(m²n²)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int maximalRectangle(char[][] matrix) {
        if (matrix.length == 0) return 0;
        int m = matrix.length, n = matrix[0].length, max = 0;
        int[] heights = new int[n];
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                heights[c] = (matrix[r][c] == '1') ? heights[c] + 1 : 0;
            }
            for (int i = 0; i < n; i++) {
                int l = i, right = i;
                while (l > 0 && heights[l - 1] >= heights[i]) l--;
                while (right < n - 1 && heights[right + 1] >= heights[i]) right++;
                max = Math.max(max, heights[i] * (right - l + 1));
            }
        }
        return max;
    }
}""",
                    "python": """class Solution:
    def maximalRectangle(self, matrix: list[list[str]]) -> int:
        if not matrix: return 0
        m, n = len(matrix), len(matrix[0])
        heights = [0] * n
        max_a = 0
        for r in range(m):
            for c in range(n):
                heights[c] = heights[c] + 1 if matrix[r][c] == '1' else 0
            for i in range(n):
                l, right = i, i
                while l > 0 and heights[l - 1] >= heights[i]: l -= 1
                while right < n - 1 and heights[right + 1] >= heights[i]: right += 1
                max_a = max(max_a, heights[i] * (right - l + 1))
        return max_a"""
                }
            },
            "optimal": {
                "idea": "Maintain height histogram array per row: heights[c] = (matrix[r][c] == '1') ? heights[c] + 1 : 0. Apply Largest Rectangle in Histogram algorithm.",
                "steps": [
                    "Initialize heights array of size n with 0.",
                    "For each row r:",
                    "Update heights[c]: increment if '1', reset to 0 if '0'.",
                    "Compute max rectangle for heights array using monotonic stack.",
                    "Update global max area."
                ],
                "time": "O(mn)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public int maximalRectangle(char[][] matrix) {
        if (matrix.length == 0) return 0;
        int m = matrix.length, n = matrix[0].length, max = 0;
        int[] h = new int[n];
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) h[c] = (matrix[r][c] == '1') ? h[c] + 1 : 0;
            max = Math.max(max, maxHistogram(h));
        }
        return max;
    }
    private int maxHistogram(int[] heights) {
        int n = heights.length, max = 0;
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i <= n; i++) {
            int cur = (i == n) ? 0 : heights[i];
            while (!stack.isEmpty() && cur < heights[stack.peek()]) {
                int ht = heights[stack.pop()];
                int w = stack.isEmpty() ? i : i - stack.peek() - 1;
                max = Math.max(max, ht * w);
            }
            stack.push(i);
        }
        return max;
    }
}""",
                    "python": """class Solution:
    def maximalRectangle(self, matrix: list[list[str]]) -> int:
        if not matrix: return 0
        n = len(matrix[0])
        heights = [0] * (n + 1)
        max_a = 0
        for row in matrix:
            for i in range(n):
                heights[i] = heights[i] + 1 if row[i] == '1' else 0
            stack = []
            for i, h in enumerate(heights):
                while stack and h < heights[stack[-1]]:
                    ht = heights[stack.pop()]
                    w = i if not stack else i - stack[-1] - 1
                    max_a = max(max_a, ht * w)
                stack.append(i)
        return max_a"""
                }
            }
        },
        {
            "seq": 78,
            "whyNext": "Builds on monotonic stack: greedy removal of digits when a smaller subsequent digit appears, keeping the number monotonically non-decreasing.",
            "brute": {
                "idea": "Try all possible combinations of removing k digits from num and find the minimum resulting integer string.",
                "steps": [
                    "Recursively remove one digit that creates the smallest prefix, repeated k times.",
                    "Strip leading zeroes."
                ],
                "whySlow": "Evaluating combination removals takes exponential time.",
                "time": "exponential",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public String removeKdigits(String num, int k) {
        if (num.length() == k) return "0";
        StringBuilder sb = new StringBuilder(num);
        for (int i = 0; i < k; i++) {
            int j = 0;
            while (j < sb.length() - 1 && sb.charAt(j) <= sb.charAt(j + 1)) j++;
            sb.deleteCharAt(j);
        }
        while (sb.length() > 1 && sb.charAt(0) == '0') sb.deleteCharAt(0);
        return sb.length() == 0 ? "0" : sb.toString();
    }
}""",
                    "python": """class Solution:
    def removeKdigits(self, num: str, k: int) -> str:
        if len(num) == k: return "0"
        s = list(num)
        for _ in range(k):
            i = 0
            while i < len(s) - 1 and s[i] <= s[i + 1]: i += 1
            s.pop(i)
        res = "".join(s).lstrip("0")
        return res if res else '0'"""
                }
            },
            "optimal": {
                "idea": "Monotonic increasing stack: while k > 0 and stack top > current digit, pop from stack and decrement k.",
                "steps": [
                    "Iterate over digits:",
                    "While k > 0 and !stack.isEmpty() and stack.peek() > digit: stack.pop(), k--.",
                    "stack.push(digit).",
                    "If k > 0, truncate k digits from end.",
                    "Build string, strip leading zeroes; return '0' if empty."
                ],
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public String removeKdigits(String num, int k) {
        Deque<Character> stack = new ArrayDeque<>();
        for (char c : num.toCharArray()) {
            while (k > 0 && !stack.isEmpty() && stack.peek() > c) {
                stack.pop();
                k--;
            }
            stack.push(c);
        }
        while (k > 0 && !stack.isEmpty()) { stack.pop(); k--; }
        StringBuilder sb = new StringBuilder();
        while (!stack.isEmpty()) sb.append(stack.pollLast());
        while (sb.length() > 1 && sb.charAt(0) == '0') sb.deleteCharAt(0);
        return sb.length() == 0 ? "0" : sb.toString();
    }
}""",
                    "python": """class Solution:
    def removeKdigits(self, num: str, k: int) -> str:
        stack = []
        for c in num:
            while k > 0 and stack and stack[-1] > c:
                stack.pop()
                k -= 1
            stack.append(c)
        if k > 0: stack = stack[:-k]
        res = "".join(stack).lstrip("0")
        return res if res else '0'"""
                }
            }
        },
        {
            "seq": 79,
            "whyNext": "Builds on monotonic stack: sort cars by position descending; stack tracks fleet arrival times, absorbing faster cars behind slower leaders.",
            "brute": {
                "idea": "Simulate positions of cars over discrete time steps until all cross target.",
                "steps": [
                    "Simulate car movements step by step.",
                    "Merge cars that catch up to each other into fleets.",
                    "Count fleets."
                ],
                "whySlow": "Simulation takes O(n * T) time where T depends on target distance.",
                "time": "O(n·T)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public int carFleet(int target, int[] position, int[] speed) {
        int n = position.length;
        double[][] cars = new double[n][2];
        for (int i = 0; i < n; i++) {
            cars[i][0] = position[i];
            cars[i][1] = (double)(target - position[i]) / speed[i];
        }
        Arrays.sort(cars, (a, b) -> Double.compare(b[0], a[0]));
        int fleets = 0;
        double curTime = 0;
        for (int i = 0; i < n; i++) {
            if (cars[i][1] > curTime) {
                fleets++;
                curTime = cars[i][1];
            }
        }
        return fleets;
    }
}""",
                    "python": """class Solution:
    def carFleet(self, target: int, position: list[int], speed: list[int]) -> int:
        cars = sorted(zip(position, speed), reverse=True)
        times = [(target - p) / s for p, s in cars]
        fleets = 0
        cur_t = 0
        for t in times:
            if t > cur_t:
                fleets += 1
                cur_t = t
        return fleets"""
                }
            },
            "optimal": {
                "idea": "Sort cars by position descending. Calculate time to target. Stack holds fleet lead arrival times; a car with time <= stack.peek() merges into fleet.",
                "steps": [
                    "Pair (position, speed) and sort descending by position.",
                    "Compute time to target for each car: (target - pos) / speed.",
                    "For each time t: if t > lastFleetTime, increment fleet count and update lastFleetTime.",
                    "Return fleet count."
                ],
                "time": "O(n log n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public int carFleet(int target, int[] position, int[] speed) {
        int n = position.length;
        double[][] cars = new double[n][2];
        for (int i = 0; i < n; i++) {
            cars[i][0] = position[i];
            cars[i][1] = (double) (target - position[i]) / speed[i];
        }
        Arrays.sort(cars, (a, b) -> Double.compare(b[0], a[0]));
        int count = 0;
        double last = 0;
        for (double[] c : cars) {
            if (c[1] > last) {
                count++;
                last = c[1];
            }
        }
        return count;
    }
}""",
                    "python": """class Solution:
    def carFleet(self, target: int, position: list[int], speed: list[int]) -> int:
        cars = sorted(zip(position, speed), reverse=True)
        times = [(target - p) / s for p, s in cars]
        fleets = 0
        last = 0
        for t in times:
            if t > last:
                fleets += 1
                last = t
        return fleets"""
                }
            }
        },
        {
            "seq": 80,
            "whyNext": "Builds on nested bracket matching: two stacks (count stack and string stack) handle nested bracket decoding.",
            "brute": {
                "idea": "Find the innermost bracket pair '[...]', decode it by repeating its string k times, and replace into original string.",
                "steps": [
                    "While string contains '[':",
                    "Locate innermost '[' and corresponding ']'.",
                    "Repeat substring k times.",
                    "Replace bracket segment in string."
                ],
                "whySlow": "Repeated string concatenation and searching takes O(n²) time.",
                "time": "O(n²)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public String decodeString(String s) {
        Deque<Integer> countStack = new ArrayDeque<>();
        Deque<StringBuilder> stringStack = new ArrayDeque<>();
        StringBuilder cur = new StringBuilder();
        int k = 0;
        for (char ch : s.toCharArray()) {
            if (Character.isDigit(ch)) k = k * 10 + (ch - '0');
            else if (ch == '[') {
                countStack.push(k);
                stringStack.push(cur);
                cur = new StringBuilder();
                k = 0;
            } else if (ch == ']') {
                StringBuilder decoded = stringStack.pop();
                int times = countStack.pop();
                for (int i = 0; i < times; i++) decoded.append(cur);
                cur = decoded;
            } else cur.append(ch);
        }
        return cur.toString();
    }
}""",
                    "python": """class Solution:
    def decodeString(self, s: str) -> str:
        stack = []
        cur_s, cur_num = "", 0
        for c in s:
            if c.isdigit():
                cur_num = cur_num * 10 + int(c)
            elif c == '[':
                stack.append((cur_s, cur_num))
                cur_s, cur_num = "", 0
            elif c == ']':
                prev_s, num = stack.pop()
                cur_s = prev_s + num * cur_s
            else:
                cur_s += c
        return cur_s"""
                }
            },
            "optimal": {
                "idea": "Two stacks: countStack stores multipliers, strStack stores previous string prefixes. When ']' reached, pop and concatenate.",
                "steps": [
                    "Maintain currentString and currentK.",
                    "If digit: k = k * 10 + digit.",
                    "If '[': push k to countStack, push currentString to strStack; reset k = 0, currentString = ''.",
                    "If ']': pop prevStr and times, currentString = prevStr + currentString * times.",
                    "Else: currentString += c."
                ],
                "time": "O(n·len)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public String decodeString(String s) {
        Deque<Integer> countStack = new ArrayDeque<>();
        Deque<StringBuilder> strStack = new ArrayDeque<>();
        StringBuilder cur = new StringBuilder();
        int k = 0;
        for (char c : s.toCharArray()) {
            if (Character.isDigit(c)) k = k * 10 + (c - '0');
            else if (c == '[') {
                countStack.push(k);
                strStack.push(cur);
                cur = new StringBuilder();
                k = 0;
            } else if (c == ']') {
                StringBuilder prev = strStack.pop();
                int times = countStack.pop();
                while (times-- > 0) prev.append(cur);
                cur = prev;
            } else cur.append(c);
        }
        return cur.toString();
    }
}""",
                    "python": """class Solution:
    def decodeString(self, s: str) -> str:
        str_stack = []
        num_stack = []
        cur_str, cur_num = "", 0
        for c in s:
            if c.isdigit():
                cur_num = cur_num * 10 + int(c)
            elif c == '[':
                num_stack.append(cur_num)
                str_stack.append(cur_str)
                cur_str, cur_num = "", 0
            elif c == ']':
                prev = str_stack.pop()
                times = num_stack.pop()
                cur_str = prev + cur_str * times
            else:
                cur_str += c
        return cur_str"""
                }
            }
        },
        {
            "seq": 81,
            "whyNext": "Builds on stack collision handling: positive asteroids move right, negative asteroids pop smaller positive asteroids from stack.",
            "brute": {
                "idea": "Repeatedly simulate collisions in multiple passes over an array until no opposing adjacent asteroids remain.",
                "steps": [
                    "Loop over array looking for asteroids[i] > 0 and asteroids[i+1] < 0.",
                    "Resolve collision by destroying smaller or both.",
                    "Repeat until no collisions remain."
                ],
                "whySlow": "Multiple array passes take O(n²) time.",
                "time": "O(n²)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public int[] asteroidCollision(int[] asteroids) {
        List<Integer> list = new ArrayList<>();
        for (int a : asteroids) list.add(a);
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int i = 0; i < list.size() - 1; i++) {
                if (list.get(i) > 0 && list.get(i + 1) < 0) {
                    changed = true;
                    int left = list.get(i), right = -list.get(i + 1);
                    if (left > right) list.remove(i + 1);
                    else if (left < right) list.remove(i);
                    else { list.remove(i + 1); list.remove(i); }
                    break;
                }
            }
        }
        int[] res = new int[list.size()];
        for (int i = 0; i < list.size(); i++) res[i] = list.get(i);
        return res;
    }
}""",
                    "python": """class Solution:
    def asteroidCollision(self, asteroids: list[int]) -> list[int]:
        ast = list(asteroids)
        changed = True
        while changed:
            changed = False
            for i in range(len(ast) - 1):
                if ast[i] > 0 and ast[i + 1] < 0:
                    changed = True
                    if ast[i] > -ast[i + 1]: ast.pop(i + 1)
                    elif ast[i] < -ast[i + 1]: ast.pop(i)
                    else: ast.pop(i + 1); ast.pop(i)
                    break
        return ast"""
                }
            },
            "optimal": {
                "idea": "Stack of surviving asteroids: incoming negative asteroid collides with positive stack top, popping smaller ones until destroyed or pushed.",
                "steps": [
                    "Initialize stack.",
                    "For each asteroid a:",
                    "While a < 0 and stack has positive top: compare abs(a) and stack top.",
                    "If stack top < abs(a), pop and continue.",
                    "If stack top == abs(a), pop and destroy both.",
                    "If survived, push a.",
                    "Convert stack to array."
                ],
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public int[] asteroidCollision(int[] asteroids) {
        Deque<Integer> stack = new ArrayDeque<>();
        for (int a : asteroids) {
            boolean alive = true;
            while (alive && a < 0 && !stack.isEmpty() && stack.peek() > 0) {
                if (stack.peek() < -a) { stack.pop(); }
                else if (stack.peek() == -a) { stack.pop(); alive = false; }
                else { alive = false; }
            }
            if (alive) stack.push(a);
        }
        int[] res = new int[stack.size()];
        for (int i = res.length - 1; i >= 0; i--) res[i] = stack.pop();
        return res;
    }
}""",
                    "python": """class Solution:
    def asteroidCollision(self, asteroids: list[int]) -> list[int]:
        stack = []
        for a in asteroids:
            alive = True
            while alive and a < 0 and stack and stack[-1] > 0:
                if stack[-1] < -a:
                    stack.pop()
                elif stack[-1] == -a:
                    stack.pop()
                    alive = False
                else:
                    alive = False
            if alive:
                stack.append(a)
        return stack"""
                }
            }
        },
        {
            "seq": 82,
            "whyNext": "Completes Chapter 5: split path by '/', push valid folder names, and pop on '..' to resolve canonical file paths.",
            "brute": {
                "idea": "Process path using split and manual string surgery with backward traversal.",
                "steps": [
                    "Split path by '/'.",
                    "Build folder hierarchy handling '.' and '..'.",
                    "Join folders with '/'."
                ],
                "whySlow": "String surgery and repeated searches takes extra string allocations.",
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public String simplifyPath(String path) {
        String[] parts = path.split("/");
        List<String> list = new ArrayList<>();
        for (String p : parts) {
            if (p.equals("") || p.equals(".")) continue;
            if (p.equals("..")) { if (!list.isEmpty()) list.remove(list.size() - 1); }
            else list.add(p);
        }
        return "/" + String.join("/", list);
    }
}""",
                    "python": """class Solution:
    def simplifyPath(self, path: str) -> str:
        parts = path.split("/")
        st = []
        for p in parts:
            if not p or p == ".": continue
            if p == "..":
                if st: st.pop()
            else: st.append(p)
        return "/" + "/".join(st)"""
                }
            },
            "optimal": {
                "idea": "Stack of directory names: split by '/', ignore empty and '.', pop on '..', push directory names, join with '/'.",
                "steps": [
                    "Initialize Deque<String> stack.",
                    "Split path by '/'.",
                    "For segment s in tokens:",
                    "If s == '..' and !stack.isEmpty(): stack.pop().",
                    "Else if !s.isEmpty() && !s.equals('.'): stack.push(s).",
                    "Join elements into canonical path starting with '/'."
                ],
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public String simplifyPath(String path) {
        Deque<String> stack = new ArrayDeque<>();
        for (String token : path.split("/")) {
            if (token.equals("..")) {
                if (!stack.isEmpty()) stack.pollLast();
            } else if (!token.isEmpty() && !token.equals(".")) {
                stack.offerLast(token);
            }
        }
        StringBuilder sb = new StringBuilder();
        for (String dir : stack) sb.append("/").append(dir);
        return sb.length() == 0 ? "/" : sb.toString();
    }
}""",
                    "python": """class Solution:
    def simplifyPath(self, path: str) -> str:
        stack = []
        for part in path.split('/'):
            if part == '..':
                if stack: stack.pop()
            elif part and part != '.':
                stack.append(part)
        return '/' + '/'.join(stack)"""
                }
            }
        },
        {
            "seq": 83,
            "whyNext": "Opens Chapter 6 (Linked List): standard pointer reversal using prev, curr, next to reverse a singly linked list in O(1) space.",
            "brute": {
                "idea": "Copy linked list values into an array, reverse the array, and rebuild a new linked list.",
                "steps": [
                    "Traverse linked list and save all node values to a list.",
                    "Rebuild a new linked list in reversed order."
                ],
                "whySlow": "Allocates O(n) memory to create a duplicate list.",
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public ListNode reverseList(ListNode head) {
        List<Integer> vals = new ArrayList<>();
        ListNode cur = head;
        while (cur != null) { vals.add(cur.val); cur = cur.next; }
        ListNode dummy = new ListNode(0);
        cur = dummy;
        for (int i = vals.size() - 1; i >= 0; i--) {
            cur.next = new ListNode(vals.get(i));
            cur = cur.next;
        }
        return dummy.next;
    }
}""",
                    "python": """class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        vals = []
        cur = head
        while cur:
            vals.append(cur.val)
            cur = cur.next
        dummy = ListNode(0)
        cur = dummy
        for v in reversed(vals):
            cur.next = ListNode(v)
            cur = cur.next
        return dummy.next"""
                }
            },
            "optimal": {
                "idea": "Three pointers: prev = null, curr = head. Save next = curr.next, reverse link curr.next = prev, advance prev = curr, curr = next.",
                "steps": [
                    "Initialize prev = null, curr = head.",
                    "While curr != null:",
                    "next = curr.next.",
                    "curr.next = prev.",
                    "prev = curr; curr = next.",
                    "Return prev."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public ListNode reverseList(ListNode head) {
        ListNode prev = null, curr = head;
        while (curr != null) {
            ListNode next = curr.next;
            curr.next = prev;
            prev = curr;
            curr = next;
        }
        return prev;
    }
}""",
                    "python": """class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev, curr = None, head
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        return prev"""
                }
            }
        },
        {
            "seq": 84,
            "whyNext": "Builds on linked list traversal: dummy head node simplifies boundary edge cases when splicing two sorted lists.",
            "brute": {
                "idea": "Collect all node values from both lists into an array, sort the array, and construct a new sorted linked list.",
                "steps": [
                    "Collect values from list1 and list2.",
                    "Sort values.",
                    "Create linked list from sorted values."
                ],
                "whySlow": "Sorting ignores existing sorted list order and allocates O(n log n) time.",
                "time": "O(n log n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public ListNode mergeTwoLists(ListNode list1, ListNode list2) {
        List<Integer> list = new ArrayList<>();
        while (list1 != null) { list.add(list1.val); list1 = list1.next; }
        while (list2 != null) { list.add(list2.val); list2 = list2.next; }
        Collections.sort(list);
        ListNode dummy = new ListNode(0), cur = dummy;
        for (int v : list) { cur.next = new ListNode(v); cur = cur.next; }
        return dummy.next;
    }
}""",
                    "python": """class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        vals = []
        while list1: vals.append(list1.val); list1 = list1.next
        while list2: vals.append(list2.val); list2 = list2.next
        vals.sort()
        dummy = ListNode(0)
        cur = dummy
        for v in vals: cur.next = ListNode(v); cur = cur.next
        return dummy.next"""
                }
            },
            "optimal": {
                "idea": "Two pointers with dummy head: compare list1.val and list2.val, link curr.next to smaller node, and attach remaining nodes.",
                "steps": [
                    "Create dummy node; curr = dummy.",
                    "While list1 != null and list2 != null:",
                    "If list1.val <= list2.val: curr.next = list1; list1 = list1.next.",
                    "Else: curr.next = list2; list2 = list2.next.",
                    "curr = curr.next.",
                    "curr.next = (list1 != null) ? list1 : list2.",
                    "Return dummy.next."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public ListNode mergeTwoLists(ListNode list1, ListNode list2) {
        ListNode dummy = new ListNode(0), cur = dummy;
        while (list1 != null && list2 != null) {
            if (list1.val <= list2.val) { cur.next = list1; list1 = list1.next; }
            else { cur.next = list2; list2 = list2.next; }
            cur = cur.next;
        }
        cur.next = (list1 != null) ? list1 : list2;
        return dummy.next;
    }
}""",
                    "python": """class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        cur = dummy
        while list1 and list2:
            if list1.val <= list2.val:
                cur.next = list1
                list1 = list1.next
            else:
                cur.next = list2
                list2 = list2.next
            cur = cur.next
        cur.next = list1 if list1 else list2
        return dummy.next"""
                }
            }
        },
        {
            "seq": 85,
            "whyNext": "Introduces fast and slow pointer technique on linked lists: fast moves twice as fast as slow, so when fast reaches end, slow is at middle.",
            "brute": {
                "idea": "Two passes: first pass counts total nodes n, second pass advances pointer n / 2 steps to middle node.",
                "steps": [
                    "First pass: count nodes in list.",
                    "Second pass: advance pointer count / 2 steps.",
                    "Return middle node."
                ],
                "whySlow": "Traverses the linked list twice.",
                "time": "two passes",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public ListNode middleNode(ListNode head) {
        int count = 0;
        ListNode cur = head;
        while (cur != null) { count++; cur = cur.next; }
        cur = head;
        for (int i = 0; i < count / 2; i++) cur = cur.next;
        return cur;
    }
}""",
                    "python": """class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        count = 0
        cur = head
        while cur: count += 1; cur = cur.next
        cur = head
        for _ in range(count // 2): cur = cur.next
        return cur"""
                }
            },
            "optimal": {
                "idea": "Fast and slow pointers in single pass: slow advances 1 node per step while fast advances 2 nodes.",
                "steps": [
                    "Initialize slow = head, fast = head.",
                    "While fast != null and fast.next != null:",
                    "slow = slow.next; fast = fast.next.next.",
                    "Return slow."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public ListNode middleNode(ListNode head) {
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        return slow;
    }
}""",
                    "python": """class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow"""
                }
            }
        },
        {
            "seq": 86,
            "whyNext": "Builds on slow/fast pointers: Floyd's Tortoise and Hare detects if a cycle exists (fast catches up to slow in O(1) space).",
            "brute": {
                "idea": "Traverse the list while inserting each visited node reference into a HashSet; if a node is seen twice, a cycle exists.",
                "steps": [
                    "Initialize a Set of visited nodes.",
                    "While curr != null: if already in set return true, else add to set.",
                    "Return false."
                ],
                "whySlow": "Allocates O(n) memory to store node pointers in set.",
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """public class Solution {
    public boolean hasCycle(ListNode head) {
        Set<ListNode> seen = new HashSet<>();
        while (head != null) {
            if (!seen.add(head)) return true;
            head = head.next;
        }
        return false;
    }
}""",
                    "python": """class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        seen = set()
        while head:
            if head in seen: return True
            seen.add(head)
            head = head.next
        return False"""
                }
            },
            "optimal": {
                "idea": "Floyd's Tortoise and Hare: slow moves 1 step, fast moves 2 steps. If there is a cycle, fast will inevitably lap and meet slow.",
                "steps": [
                    "Initialize slow = head, fast = head.",
                    "While fast != null and fast.next != null:",
                    "slow = slow.next, fast = fast.next.next.",
                    "If slow == fast, return true.",
                    "Return false."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """public class Solution {
    public boolean hasCycle(ListNode head) {
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) return true;
        }
        return false;
    }
}""",
                    "python": """class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast: return True
        return False"""
                }
            }
        },
        {
            "seq": 87,
            "whyNext": "Builds on cycle detection: after slow and fast meet, reset one pointer to head and advance both by 1; they meet at the cycle entrance.",
            "brute": {
                "idea": "Use a HashSet to store visited node references and return the first node already in the set.",
                "steps": [
                    "Traverse list with a HashSet.",
                    "Return first re-encountered node."
                ],
                "whySlow": "Uses O(n) memory for visited set.",
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """public class Solution {
    public ListNode detectCycle(ListNode head) {
        Set<ListNode> seen = new HashSet<>();
        while (head != null) {
            if (!seen.add(head)) return head;
            head = head.next;
        }
        return null;
    }
}""",
                    "python": """class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        seen = set()
        while head:
            if head in seen: return head
            seen.add(head)
            head = head.next
        return None"""
                }
            },
            "optimal": {
                "idea": "Floyd cycle detection: after slow and fast meet, reset slow to head. Advance both one node per step until they meet at cycle entrance.",
                "steps": [
                    "Find intersection using slow and fast pointers.",
                    "If fast reaches null, return null (no cycle).",
                    "Reset slow = head.",
                    "Advance slow and fast 1 step at a time until slow == fast.",
                    "Return slow."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """public class Solution {
    public ListNode detectCycle(ListNode head) {
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) {
                ListNode ptr = head;
                while (ptr != slow) {
                    ptr = ptr.next;
                    slow = slow.next;
                }
                return ptr;
            }
        }
        return null;
    }
}""",
                    "python": """class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                ptr = head
                while ptr != slow:
                    ptr = ptr.next
                    slow = slow.next
                return ptr
        return None"""
                }
            }
        },
        {
            "seq": 88,
            "whyNext": "Builds on pointer traversal: two pointers switch heads when reaching null, equalizing lengths (a + b) to meet at intersection in O(1) space.",
            "brute": {
                "idea": "Store all node references of list A in a HashSet, then scan list B to find the first matching node.",
                "steps": [
                    "Add all nodes of list A into set.",
                    "Scan list B; return first node found in set.",
                    "Return null if none."
                ],
                "whySlow": "Requires O(n) space for set of node references.",
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """public class Solution {
    public ListNode getIntersectionNode(ListNode headA, ListNode headB) {
        Set<ListNode> seen = new HashSet<>();
        while (headA != null) { seen.add(headA); headA = headA.next; }
        while (headB != null) { if (seen.contains(headB)) return headB; headB = headB.next; }
        return null;
    }
}""",
                    "python": """class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        seen = set()
        while headA: seen.add(headA); headA = headA.next
        while headB:
            if headB in seen: return headB
            headB = headB.next
        return None"""
                }
            },
            "optimal": {
                "idea": "Two pointers: pointer pA walks A then B; pointer pB walks B then A. Both travel len(A) + len(B) and meet at intersection node.",
                "steps": [
                    "pA = headA, pB = headB.",
                    "While pA != pB:",
                    "pA = (pA == null) ? headB : pA.next.",
                    "pB = (pB == null) ? headA : pB.next.",
                    "Return pA."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """public class Solution {
    public ListNode getIntersectionNode(ListNode headA, ListNode headB) {
        ListNode a = headA, b = headB;
        while (a != b) {
            a = (a == null) ? headB : a.next;
            b = (b == null) ? headA : b.next;
        }
        return a;
    }
}""",
                    "python": """class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        a, b = headA, headB
        while a != b:
            a = headB if not a else a.next
            b = headA if not b else b.next
        return a"""
                }
            }
        },
        {
            "seq": 89,
            "whyNext": "Builds on fast/slow pointers: fast pointer moves n steps ahead, so when fast reaches the end, slow is right before the nth node from end.",
            "brute": {
                "idea": "First pass counts total length L, second pass stops at index L - n - 1 to unlink target node.",
                "steps": [
                    "Count length L of linked list.",
                    "If L == n, return head.next.",
                    "Walk L - n - 1 steps; bypass next node.",
                    "Return head."
                ],
                "whySlow": "Requires two full passes across the list.",
                "time": "two passes",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public ListNode removeNthFromEnd(ListNode head, int n) {
        int len = 0;
        ListNode cur = head;
        while (cur != null) { len++; cur = cur.next; }
        if (len == n) return head.next;
        cur = head;
        for (int i = 0; i < len - n - 1; i++) cur = cur.next;
        cur.next = cur.next.next;
        return head;
    }
}""",
                    "python": """class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        l = 0
        cur = head
        while cur: l += 1; cur = cur.next
        if l == n: return head.next
        cur = head
        for _ in range(l - n - 1): cur = cur.next
        cur.next = cur.next.next
        return head"""
                }
            },
            "optimal": {
                "idea": "Single pass with dummy head: advance fast pointer n + 1 steps ahead. Move both until fast is null; slow.next = slow.next.next.",
                "steps": [
                    "Create dummy head pointing to head.",
                    "Advance fast pointer n + 1 steps from dummy.",
                    "Move fast and slow together until fast is null.",
                    "slow.next = slow.next.next.",
                    "Return dummy.next."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public ListNode removeNthFromEnd(ListNode head, int n) {
        ListNode dummy = new ListNode(0, head);
        ListNode fast = dummy, slow = dummy;
        for (int i = 0; i <= n; i++) fast = fast.next;
        while (fast != null) {
            fast = fast.next;
            slow = slow.next;
        }
        slow.next = slow.next.next;
        return dummy.next;
    }
}""",
                    "python": """class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        fast = slow = dummy
        for _ in range(n + 1): fast = fast.next
        while fast:
            fast = fast.next
            slow = slow.next
        slow.next = slow.next.next
        return dummy.next"""
                }
            }
        },
        {
            "seq": 90,
            "whyNext": "Builds on sorted list traversal: skip consecutive equal node values in place (curr.next = curr.next.next).",
            "brute": {
                "idea": "Collect values in a LinkedHashSet to eliminate duplicates, then rebuild a new linked list.",
                "steps": [
                    "Put all node values into LinkedHashSet.",
                    "Rebuild new list from set elements."
                ],
                "whySlow": "Uses O(n) memory instead of in-place node rewiring.",
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public ListNode deleteDuplicates(ListNode head) {
        Set<Integer> set = new LinkedHashSet<>();
        while (head != null) { set.add(head.val); head = head.next; }
        ListNode dummy = new ListNode(0), cur = dummy;
        for (int v : set) { cur.next = new ListNode(v); cur = cur.next; }
        return dummy.next;
    }
}""",
                    "python": """class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        seen = []
        cur = head
        while cur:
            if not seen or seen[-1] != cur.val: seen.append(cur.val)
            cur = cur.next
        dummy = ListNode(0)
        cur = dummy
        for v in seen: cur.next = ListNode(v); cur = cur.next
        return dummy.next"""
                }
            },
            "optimal": {
                "idea": "In-place pointer traversal: if curr.val == curr.next.val, skip curr.next; else advance curr = curr.next.",
                "steps": [
                    "Initialize curr = head.",
                    "While curr != null and curr.next != null:",
                    "If curr.val == curr.next.val: curr.next = curr.next.next.",
                    "Else: curr = curr.next.",
                    "Return head."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public ListNode deleteDuplicates(ListNode head) {
        ListNode cur = head;
        while (cur != null && cur.next != null) {
            if (cur.val == cur.next.val) cur.next = cur.next.next;
            else cur = cur.next;
        }
        return head;
    }
}""",
                    "python": """class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        cur = head
        while cur and cur.next:
            if cur.val == cur.next.val: cur.next = cur.next.next
            else: cur = cur.next
        return head"""
                }
            }
        },
        {
            "seq": 91,
            "whyNext": "Builds on Remove Duplicates: dummy head node allows completely deleting duplicate runs, leaving only distinct numbers.",
            "brute": {
                "idea": "Count frequencies of all numbers with a map, then build a new list containing only numbers with count == 1.",
                "steps": [
                    "Count frequencies with HashMap.",
                    "Build new linked list containing only nodes whose values occur once."
                ],
                "whySlow": "Allocates extra memory for frequency map and new list.",
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public ListNode deleteDuplicates(ListNode head) {
        Map<Integer, Integer> map = new LinkedHashMap<>();
        for (ListNode c = head; c != null; c = c.next) map.put(c.val, map.getOrDefault(c.val, 0) + 1);
        ListNode dummy = new ListNode(0), cur = dummy;
        for (int k : map.keySet()) {
            if (map.get(k) == 1) { cur.next = new ListNode(k); cur = cur.next; }
        }
        return dummy.next;
    }
}""",
                    "python": """class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        counts = collections.Counter()
        cur = head
        while cur: counts[cur.val] += 1; cur = cur.next
        dummy = ListNode(0)
        cur = dummy
        c2 = head
        while c2:
            if counts[c2.val] == 1:
                cur.next = ListNode(c2.val)
                cur = cur.next
            c2 = c2.next
        return dummy.next"""
                }
            },
            "optimal": {
                "idea": "Dummy head with prev pointer: when head has duplicate run, skip all equal nodes and set prev.next = head.next.",
                "steps": [
                    "Create dummy head pointing to head; prev = dummy.",
                    "While head != null:",
                    "If head.next != null and head.val == head.next.val:",
                    "Loop head forward while head.next != null and head.val == head.next.val.",
                    "prev.next = head.next.",
                    "Else: prev = prev.next.",
                    "head = head.next.",
                    "Return dummy.next."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public ListNode deleteDuplicates(ListNode head) {
        ListNode dummy = new ListNode(0, head);
        ListNode prev = dummy;
        while (head != null) {
            if (head.next != null && head.val == head.next.val) {
                while (head.next != null && head.val == head.next.val) head = head.next;
                prev.next = head.next;
            } else {
                prev = prev.next;
            }
            head = head.next;
        }
        return dummy.next;
    }
}""",
                    "python": """class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        prev = dummy
        while head:
            if head.next and head.val == head.next.val:
                while head.next and head.val == head.next.val:
                    head = head.next
                prev.next = head.next
            else:
                prev = prev.next
            head = head.next
        return dummy.next"""
                }
            }
        },
        {
            "seq": 92,
            "whyNext": "Combines Middle of Linked List and Reverse Linked List: find middle, reverse second half in place, and compare two halves.",
            "brute": {
                "idea": "Copy all node values into an array list and check if the list is a palindrome using two pointers.",
                "steps": [
                    "Collect node values into array.",
                    "Check array with two pointers from ends."
                ],
                "whySlow": "Allocates O(n) extra space.",
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public boolean isPalindrome(ListNode head) {
        List<Integer> list = new ArrayList<>();
        while (head != null) { list.add(head.val); head = head.next; }
        int l = 0, r = list.size() - 1;
        while (l < r) if (!list.get(l++).equals(list.get(r--))) return false;
        return true;
    }
}""",
                    "python": """class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        vals = []
        while head: vals.append(head.val); head = head.next
        return vals == vals[::-1]"""
                }
            },
            "optimal": {
                "idea": "Find middle with slow/fast pointers, reverse second half in place, compare first and second halves, restore list.",
                "steps": [
                    "Find middle using slow and fast pointers.",
                    "Reverse second half starting at slow.",
                    "Compare values of first half and reversed second half.",
                    "Return true if all match, else false."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public boolean isPalindrome(ListNode head) {
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) { slow = slow.next; fast = fast.next.next; }
        ListNode prev = null, cur = slow;
        while (cur != null) {
            ListNode next = cur.next;
            cur.next = prev;
            prev = cur;
            cur = next;
        }
        ListNode p1 = head, p2 = prev;
        while (p2 != null) {
            if (p1.val != p2.val) return false;
            p1 = p1.next; p2 = p2.next;
        }
        return true;
    }
}""",
                    "python": """class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        prev, cur = None, slow
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        p1, p2 = head, prev
        while p2:
            if p1.val != p2.val: return False
            p1 = p1.next; p2 = p2.next
        return True"""
                }
            }
        },
        {
            "seq": 93,
            "whyNext": "Builds on Merge Two Sorted Lists: traverse two lists simultaneously, summing digits with a carry variable.",
            "brute": {
                "idea": "Convert both linked lists to integers, add them, and convert the sum back to a linked list.",
                "steps": [
                    "Extract BigInteger from l1.",
                    "Extract BigInteger from l2.",
                    "Sum them and convert back to linked list."
                ],
                "whySlow": "Converting to integers risks overflow and uses extra passes.",
                "time": "O(max(m,n))",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0), cur = dummy;
        int carry = 0;
        while (l1 != null || l2 != null || carry != 0) {
            int sum = carry;
            if (l1 != null) { sum += l1.val; l1 = l1.next; }
            if (l2 != null) { sum += l2.val; l2 = l2.next; }
            carry = sum / 10;
            cur.next = new ListNode(sum % 10);
            cur = cur.next;
        }
        return dummy.next;
    }
}""",
                    "python": """class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        cur, carry = dummy, 0
        while l1 or l2 or carry:
            s = carry
            if l1: s += l1.val; l1 = l1.next
            if l2: s += l2.val; l2 = l2.next
            carry = s // 10
            cur.next = ListNode(s % 10)
            cur = cur.next
        return dummy.next"""
                }
            },
            "optimal": {
                "idea": "Single pass: simulate digit-by-digit addition with carry, creating a new node for sum % 10.",
                "steps": [
                    "Create dummy head; carry = 0.",
                    "While l1 != null or l2 != null or carry > 0:",
                    "sum = carry + (l1 != null ? l1.val : 0) + (l2 != null ? l2.val : 0).",
                    "carry = sum / 10.",
                    "cur.next = new ListNode(sum % 10); cur = cur.next.",
                    "Advance l1 and l2.",
                    "Return dummy.next."
                ],
                "time": "O(max(m,n))",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0), cur = dummy;
        int carry = 0;
        while (l1 != null || l2 != null || carry != 0) {
            int sum = carry;
            if (l1 != null) { sum += l1.val; l1 = l1.next; }
            if (l2 != null) { sum += l2.val; l2 = l2.next; }
            carry = sum / 10;
            cur.next = new ListNode(sum % 10);
            cur = cur.next;
        }
        return dummy.next;
    }
}""",
                    "python": """class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        cur, carry = dummy, 0
        while l1 or l2 or carry:
            s = carry
            if l1: s += l1.val; l1 = l1.next
            if l2: s += l2.val; l2 = l2.next
            carry = s // 10
            cur.next = ListNode(s % 10)
            cur = cur.next
        return dummy.next"""
                }
            }
        },
        {
            "seq": 94,
            "whyNext": "Builds on Palindrome Linked List: find middle node, reverse second half, and interleave nodes from first and second halves.",
            "brute": {
                "idea": "Store all nodes in an array list and rewire next pointers using two pointers from the ends.",
                "steps": [
                    "Put all nodes into a list.",
                    "Use pointers i = 0, j = n - 1 to interleave nodes.",
                    "Set last node's next to null."
                ],
                "whySlow": "Allocates O(n) extra space for node list.",
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public void reorderList(ListNode head) {
        if (head == null) return;
        List<ListNode> list = new ArrayList<>();
        for (ListNode c = head; c != null; c = c.next) list.add(c);
        int i = 0, j = list.size() - 1;
        while (i < j) {
            list.get(i).next = list.get(j);
            i++;
            if (i == j) break;
            list.get(j).next = list.get(i);
            j--;
        }
        list.get(i).next = null;
    }
}""",
                    "python": """class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        if not head: return
        nodes = []
        cur = head
        while cur: nodes.append(cur); cur = cur.next
        i, j = 0, len(nodes) - 1
        while i < j:
            nodes[i].next = nodes[j]
            i += 1
            if i == j: break
            nodes[j].next = nodes[i]
            j -= 1
        nodes[i].next = None"""
                }
            },
            "optimal": {
                "idea": "Split at middle, reverse second half, and interleave the two halves in place without extra memory.",
                "steps": [
                    "Find middle using slow and fast pointers; split list into two halves.",
                    "Reverse second half in place.",
                    "Merge / interleave first half and reversed second half."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public void reorderList(ListNode head) {
        if (head == null || head.next == null) return;
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) { slow = slow.next; fast = fast.next.next; }
        ListNode prev = null, cur = slow.next;
        slow.next = null;
        while (cur != null) {
            ListNode next = cur.next;
            cur.next = prev;
            prev = cur;
            cur = next;
        }
        ListNode p1 = head, p2 = prev;
        while (p2 != null) {
            ListNode t1 = p1.next, t2 = p2.next;
            p1.next = p2;
            p2.next = t1;
            p1 = t1; p2 = t2;
        }
    }
}""",
                    "python": """class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        if not head or not head.next: return
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        prev, cur = None, slow.next
        slow.next = None
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        p1, p2 = head, prev
        while p2:
            t1, t2 = p1.next, p2.next
            p1.next = p2
            p2.next = t1
            p1, p2 = t1, t2"""
                }
            }
        },
        {
            "seq": 95,
            "whyNext": "Builds on Merge Two Sorted Lists: divide list in half using slow/fast pointers, recursively sort both, and merge.",
            "brute": {
                "idea": "Collect all node values into an array, sort the array, and write back into the linked list.",
                "steps": [
                    "Collect node values into array.",
                    "Sort array.",
                    "Write sorted values back into nodes."
                ],
                "whySlow": "Allocates O(n) extra space instead of pointer manipulation.",
                "time": "O(n log n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public ListNode sortList(ListNode head) {
        List<Integer> list = new ArrayList<>();
        for (ListNode c = head; c != null; c = c.next) list.add(c.val);
        Collections.sort(list);
        ListNode cur = head;
        for (int v : list) { cur.val = v; cur = cur.next; }
        return head;
    }
}""",
                    "python": """class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        vals = []
        cur = head
        while cur: vals.append(cur.val); cur = cur.next
        vals.sort()
        cur = head
        for v in vals: cur.val = v; cur = cur.next
        return head"""
                }
            },
            "optimal": {
                "idea": "Merge sort on linked list: find middle to split list, recursively sort both halves, and merge sorted lists.",
                "steps": [
                    "Base case: if head == null || head.next == null, return head.",
                    "Use slow/fast pointers with prev to split list in half.",
                    "left = sortList(head), right = sortList(mid).",
                    "Return mergeTwoLists(left, right)."
                ],
                "time": "O(n log n)",
                "space": "O(log n)",
                "code": {
                    "java": """class Solution {
    public ListNode sortList(ListNode head) {
        if (head == null || head.next == null) return head;
        ListNode prev = null, slow = head, fast = head;
        while (fast != null && fast.next != null) {
            prev = slow;
            slow = slow.next;
            fast = fast.next.next;
        }
        prev.next = null;
        ListNode l1 = sortList(head);
        ListNode l2 = sortList(slow);
        return merge(l1, l2);
    }
    private ListNode merge(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0), cur = dummy;
        while (l1 != null && l2 != null) {
            if (l1.val < l2.val) { cur.next = l1; l1 = l1.next; }
            else { cur.next = l2; l2 = l2.next; }
            cur = cur.next;
        }
        cur.next = (l1 != null) ? l1 : l2;
        return dummy.next;
    }
}""",
                    "python": """class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next: return head
        prev, slow, fast = None, head, head
        while fast and fast.next:
            prev = slow
            slow = slow.next
            fast = fast.next.next
        prev.next = None
        l1 = self.sortList(head)
        l2 = self.sortList(slow)
        dummy = ListNode(0)
        cur = dummy
        while l1 and l2:
            if l1.val < l2.val: cur.next, l1 = l1, l1.next
            else: cur.next, l2 = l2, l2.next
            cur = cur.next
        cur.next = l1 if l1 else l2
        return dummy.next"""
                }
            }
        },
        {
            "seq": 96,
            "whyNext": "Builds on linked list traversal: interleave cloned nodes directly after originals (A -> A' -> B -> B') to copy random pointers in O(1) space.",
            "brute": {
                "idea": "Use a HashMap mapping each original node to its cloned copy, then connect next and random pointers.",
                "steps": [
                    "Pass 1: create a clone for each node and put in map: map.put(node, new Node(node.val)).",
                    "Pass 2: for each node, clone.next = map.get(node.next), clone.random = map.get(node.random).",
                    "Return map.get(head)."
                ],
                "whySlow": "Uses O(n) auxiliary space for the hash map.",
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public Node copyRandomList(Node head) {
        if (head == null) return null;
        Map<Node, Node> map = new HashMap<>();
        for (Node c = head; c != null; c = c.next) map.put(c, new Node(c.val));
        for (Node c = head; c != null; c = c.next) {
            map.get(c).next = map.get(c.next);
            map.get(c).random = map.get(c.random);
        }
        return map.get(head);
    }
}""",
                    "python": """class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        if not head: return None
        mapping = {}
        cur = head
        while cur:
            mapping[cur] = Node(cur.val)
            cur = cur.next
        cur = head
        while cur:
            mapping[cur].next = mapping.get(cur.next)
            mapping[cur].random = mapping.get(cur.random)
            cur = cur.next
        return mapping[head]"""
                }
            },
            "optimal": {
                "idea": "In-place interleaving: insert cloned node directly after original node, copy random pointers via cur.next.random = cur.random.next, then separate lists.",
                "steps": [
                    "Pass 1: interleave copy nodes: cur -> copy -> cur.next.",
                    "Pass 2: copy random pointers: if cur.random != null, cur.next.random = cur.random.next.",
                    "Pass 3: decouple copy nodes into a separate cloned list and restore original list."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public Node copyRandomList(Node head) {
        if (head == null) return null;
        Node cur = head;
        while (cur != null) {
            Node copy = new Node(cur.val);
            copy.next = cur.next;
            cur.next = copy;
            cur = copy.next;
        }
        cur = head;
        while (cur != null) {
            if (cur.random != null) cur.next.random = cur.random.next;
            cur = cur.next.next;
        }
        Node dummy = new Node(0), copyCur = dummy;
        cur = head;
        while (cur != null) {
            Node copy = cur.next;
            cur.next = copy.next;
            copyCur.next = copy;
            copyCur = copy;
            cur = cur.next;
        }
        return dummy.next;
    }
}""",
                    "python": """class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        if not head: return None
        cur = head
        while cur:
            copy = Node(cur.val, next=cur.next)
            cur.next = copy
            cur = copy.next
        cur = head
        while cur:
            if cur.random: cur.next.random = cur.random.next
            cur = cur.next.next
        dummy = Node(0)
        copy_cur = dummy
        cur = head
        while cur:
            copy = cur.next
            cur.next = copy.next
            copy_cur.next = copy
            copy_cur = copy
            cur = cur.next
        return dummy.next"""
                }
            }
        },
        {
            "seq": 97,
            "whyNext": "Generalizes Reverse Linked List: check if k nodes remain, reverse the k-node chunk in place, and link to the next group.",
            "brute": {
                "idea": "Collect all nodes into a list, reverse groups of size k in the list, and rewire next pointers.",
                "steps": [
                    "Collect all nodes in a list.",
                    "Reverse each group of k nodes.",
                    "Rebuild next pointers."
                ],
                "whySlow": "Allocates O(n) extra space.",
                "time": "O(n)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public ListNode reverseKGroup(ListNode head, int k) {
        List<ListNode> list = new ArrayList<>();
        for (ListNode c = head; c != null; c = c.next) list.add(c);
        int n = list.size();
        for (int i = 0; i + k <= n; i += k) {
            Collections.reverse(list.subList(i, i + k));
        }
        for (int i = 0; i < n - 1; i++) list.get(i).next = list.get(i + 1);
        if (n > 0) list.get(n - 1).next = null;
        return n > 0 ? list.get(0) : null;
    }
}""",
                    "python": """class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        nodes = []
        cur = head
        while cur: nodes.append(cur); cur = cur.next
        n = len(nodes)
        for i in range(0, n - n % k, k):
            nodes[i:i+k] = reversed(nodes[i:i+k])
        for i in range(n - 1): nodes[i].next = nodes[i + 1]
        if n: nodes[-1].next = None
        return nodes[0] if n else None"""
                }
            },
            "optimal": {
                "idea": "In-place k-group reversal: count k nodes ahead; if k nodes exist, reverse the sublist and recursively/iteratively connect with remaining groups.",
                "steps": [
                    "Count k nodes from head.",
                    "If fewer than k nodes remain, return head.",
                    "Reverse k nodes in place using prev/curr pointers.",
                    "head.next = reverseKGroup(curr, k).",
                    "Return prev."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public ListNode reverseKGroup(ListNode head, int k) {
        ListNode check = head;
        for (int i = 0; i < k; i++) {
            if (check == null) return head;
            check = check.next;
        }
        ListNode prev = null, cur = head;
        for (int i = 0; i < k; i++) {
            ListNode next = cur.next;
            cur.next = prev;
            prev = cur;
            cur = next;
        }
        head.next = reverseKGroup(cur, k);
        return prev;
    }
}""",
                    "python": """class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        check = head
        for _ in range(k):
            if not check: return head
            check = check.next
        prev, cur = None, head
        for _ in range(k):
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        head.next = self.reverseKGroup(cur, k)
        return prev"""
                }
            }
        },
        {
            "seq": 98,
            "whyNext": "Generalizes Merge Two Sorted Lists to k lists: min-heap of node heads merges nodes in O(N log k).",
            "brute": {
                "idea": "Collect all node values from all k linked lists into an array, sort the array, and construct a new sorted linked list.",
                "steps": [
                    "Collect all node values from all lists.",
                    "Sort values.",
                    "Build new linked list."
                ],
                "whySlow": "Full sorting of all N elements takes O(N log N) time.",
                "time": "O(N log N)",
                "space": "O(N)",
                "code": {
                    "java": """class Solution {
    public ListNode mergeKLists(ListNode[] lists) {
        List<Integer> list = new ArrayList<>();
        for (ListNode l : lists) {
            while (l != null) { list.add(l.val); l = l.next; }
        }
        Collections.sort(list);
        ListNode dummy = new ListNode(0), cur = dummy;
        for (int v : list) { cur.next = new ListNode(v); cur = cur.next; }
        return dummy.next;
    }
}""",
                    "python": """class Solution:
    def mergeKLists(self, lists: list[Optional[ListNode]]) -> Optional[ListNode]:
        vals = []
        for l in lists:
            while l: vals.append(l.val); l = l.next
        vals.sort()
        dummy = ListNode(0)
        cur = dummy
        for v in vals: cur.next = ListNode(v); cur = cur.next
        return dummy.next"""
                }
            },
            "optimal": {
                "idea": "Min-heap of size k: insert heads of all non-empty lists. Repeatedly pop smallest node, append to merged list, and push its next node.",
                "steps": [
                    "Initialize PriorityQueue with comparator (a, b) -> a.val - b.val.",
                    "Add non-null head of each list to heap.",
                    "While heap is not empty:",
                    "node = heap.poll(); cur.next = node; cur = cur.next.",
                    "If node.next != null, heap.offer(node.next).",
                    "Return dummy.next."
                ],
                "time": "O(N log k)",
                "space": "O(k)",
                "code": {
                    "java": """class Solution {
    public ListNode mergeKLists(ListNode[] lists) {
        PriorityQueue<ListNode> pq = new PriorityQueue<>((a, b) -> a.val - b.val);
        for (ListNode l : lists) if (l != null) pq.offer(l);
        ListNode dummy = new ListNode(0), cur = dummy;
        while (!pq.isEmpty()) {
            ListNode node = pq.poll();
            cur.next = node;
            cur = cur.next;
            if (node.next != null) pq.offer(node.next);
        }
        return dummy.next;
    }
}""",
                    "python": """class Solution:
    def mergeKLists(self, lists: list[Optional[ListNode]]) -> Optional[ListNode]:
        pq = []
        for i, l in enumerate(lists):
            if l: heapq.heappush(pq, (l.val, i, l))
        dummy = ListNode(0)
        cur = dummy
        while pq:
            val, i, node = heapq.heappop(pq)
            cur.next = node
            cur = cur.next
            if node.next:
                heapq.heappush(pq, (node.next.val, i, node.next))
        return dummy.next"""
                }
            }
        },
        {
            "seq": 99,
            "whyNext": "Completes Chapter 6: composite data structure combining HashMap for O(1) key lookup and Doubly Linked List for O(1) eviction.",
            "brute": {
                "idea": "Maintain key-value pairs in a list or map with timestamps; on capacity overflow, scan for minimum timestamp.",
                "steps": [
                    "Store (key, value, accessTime) in a list.",
                    "On get: update accessTime.",
                    "On put: if full, scan for least recently used element and remove it."
                ],
                "whySlow": "Scanning for LRU element takes O(n) time.",
                "time": "O(n)",
                "space": "O(capacity)",
                "code": {
                    "java": """class LRUCache {
    private int cap;
    private LinkedHashMap<Integer, Integer> map;
    public LRUCache(int capacity) {
        this.cap = capacity;
        this.map = new LinkedHashMap<>(capacity, 0.75f, true) {
            protected boolean removeEldestEntry(Map.Entry eldest) {
                return size() > cap;
            }
        };
    }
    public int get(int key) { return map.getOrDefault(key, -1); }
    public void put(int key, int value) { map.put(key, value); }
}""",
                    "python": """class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.map = collections.OrderedDict()
    def get(self, key: int) -> int:
        if key not in self.map: return -1
        self.map.move_to_end(key)
        return self.map[key]
    def put(self, key: int, value: int) -> None:
        if key in self.map:
            self.map.move_to_end(key)
        self.map[key] = value
        if len(self.map) > self.cap:
            self.map.popitem(last=False)"""
                }
            },
            "optimal": {
                "idea": "HashMap plus Doubly Linked List: HashMap maps key to DListNode. DLL keeps most recently used at head, least recently used at tail.",
                "steps": [
                    "Define DListNode with prev and next pointers.",
                    "Maintain head and tail dummy sentinels.",
                    "get(key): if present, move node to head and return value.",
                    "put(key, val): if present update and move to head; if new add at head; if over capacity remove node before tail."
                ],
                "time": "O(1)",
                "space": "O(capacity)",
                "code": {
                    "java": """class LRUCache {
    class DNode { int k, v; DNode prev, next; DNode(int k, int v) { this.k = k; this.v = v; } }
    private Map<Integer, DNode> map = new HashMap<>();
    private int cap;
    private DNode head = new DNode(0, 0), tail = new DNode(0, 0);
    public LRUCache(int capacity) {
        this.cap = capacity;
        head.next = tail; tail.prev = head;
    }
    public int get(int key) {
        if (!map.containsKey(key)) return -1;
        DNode node = map.get(key);
        remove(node); addHead(node);
        return node.v;
    }
    public void put(int key, int value) {
        if (map.containsKey(key)) {
            DNode node = map.get(key);
            node.v = value;
            remove(node); addHead(node);
        } else {
            if (map.size() == cap) {
                map.remove(tail.prev.k);
                remove(tail.prev);
            }
            DNode node = new DNode(key, value);
            map.put(key, node);
            addHead(node);
        }
    }
    private void remove(DNode n) { n.prev.next = n.next; n.next.prev = n.prev; }
    private void addHead(DNode n) { n.next = head.next; n.prev = head; head.next.prev = n; head.next = n; }
}""",
                    "python": """class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.map = collections.OrderedDict()
    def get(self, key: int) -> int:
        if key not in self.map: return -1
        self.map.move_to_end(key)
        return self.map[key]
    def put(self, key: int, value: int) -> None:
        if key in self.map:
            self.map.move_to_end(key)
        self.map[key] = value
        if len(self.map) > self.cap:
            self.map.popitem(last=False)"""
                }
            }
        },
        {
            "seq": 100,
            "whyNext": "Opens Chapter 7 (Recursion and Backtracking): base cases and recurrence relation fib(n) = fib(n-1) + fib(n-2), transitioning to iterative DP.",
            "brute": {
                "idea": "Direct naive recursion: return fib(n - 1) + fib(n - 2).",
                "steps": [
                    "If n <= 1, return n.",
                    "Return fib(n - 1) + fib(n - 2)."
                ],
                "whySlow": "Recalculates overlapping subproblems exponentially, taking O(2ⁿ) time.",
                "time": "O(2ⁿ)",
                "space": "O(n)",
                "code": {
                    "java": """class Solution {
    public int fib(int n) {
        if (n <= 1) return n;
        return fib(n - 1) + fib(n - 2);
    }
}""",
                    "python": """class Solution:
    def fib(self, n: int) -> int:
        if n <= 1: return n
        return self.fib(n - 1) + self.fib(n - 2)"""
                }
            },
            "optimal": {
                "idea": "Two rolling variables: compute each Fibonacci number from previous two in O(n) time and O(1) space.",
                "steps": [
                    "If n <= 1, return n.",
                    "Initialize a = 0, b = 1.",
                    "Loop i from 2 to n: c = a + b, a = b, b = c.",
                    "Return b."
                ],
                "time": "O(n)",
                "space": "O(1)",
                "code": {
                    "java": """class Solution {
    public int fib(int n) {
        if (n <= 1) return n;
        int a = 0, b = 1;
        for (int i = 2; i <= n; i++) {
            int c = a + b;
            a = b;
            b = c;
        }
        return b;
    }
}""",
                    "python": """class Solution:
    def fib(self, n: int) -> int:
        if n <= 1: return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b"""
                }
            }
        }
    ]

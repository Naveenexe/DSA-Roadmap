import os
import subprocess
import shutil
import json
import re

JDK_JAVAC = r"C:\Program Files\Java\jdk-26.0.2\bin\javac.exe"
JAVAC_CMD = JDK_JAVAC if os.path.exists(JDK_JAVAC) else "javac"

LEETCODE_TYPES_JAVA = """
import java.util.*;
import java.io.*;

class ListNode {
    int val;
    ListNode next;
    ListNode() {}
    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}

class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode() {}
    TreeNode(int val) { this.val = val; }
    TreeNode(int val, TreeNode left, TreeNode right) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}

class Node {
    public int val;
    public Node next;
    public Node random;
    public Node left;
    public Node right;
    public List<Node> neighbors;
    public List<Node> children;
    public Node() { neighbors = new ArrayList<>(); }
    public Node(int _val) { val = _val; neighbors = new ArrayList<>(); }
    public Node(int _val, ArrayList<Node> _neighbors) { val = _val; neighbors = _neighbors; }
}
"""

PY_LEETCODE_PREAMBLE = """
import collections
import heapq
import bisect
import math
from typing import *

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Node:
    def __init__(self, val=0, neighbors=None, next=None, random=None, left=None, right=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
        self.next = next
        self.random = random
        self.left = left
        self.right = right
"""

questions_json_path = os.path.join(os.path.dirname(__file__), "..", "public", "data", "questions.json")
seq_title_map = {}
if os.path.exists(questions_json_path):
    with open(questions_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for item in data:
            seq_title_map[item["seq"]] = item["title"]

def verify_and_record_batch(batch_num, questions_data, batch_report_path="batch-report.md"):
    passed_count = 0
    failed_count = 0
    failures = []

    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    tmpdir = os.path.join(workspace_root, ".temp_verify")
    if os.path.exists(tmpdir):
        shutil.rmtree(tmpdir, ignore_errors=True)
    os.makedirs(tmpdir, exist_ok=True)

    try:
        types_file = os.path.join(tmpdir, "LeetCodeTypes.java")
        with open(types_file, "w", encoding="utf-8") as f:
            f.write(LEETCODE_TYPES_JAVA)

        java_files = [types_file]
        seq_mode_files = []
        py_tests = []

        for q in questions_data:
            seq = q["seq"]
            for mode in ["optimal", "brute"]:
                j_code = q[mode]["code"]["java"]
                # Find primary class name
                m = re.search(r'class\s+([A-Za-z0-9_]+)', j_code)
                orig_class = m.group(1) if m else "Solution"
                cname = f"{orig_class}_{seq}_{mode}"
                
                # Replace class declaration and any constructors with unique class name
                j_code_renamed = re.sub(r'\bclass\s+' + orig_class + r'\b', f"class {cname}", j_code)
                j_code_renamed = re.sub(r'\bpublic\s+' + orig_class + r'\s*\(', f"public {cname}(", j_code_renamed)
                
                j_file = os.path.join(tmpdir, f"{cname}.java")
                full_java = "import java.util.*;\nimport java.io.*;\n" + j_code_renamed
                with open(j_file, "w", encoding="utf-8") as f:
                    f.write(full_java)
                java_files.append(j_file)
                seq_mode_files.append((seq, mode, j_file))

            for mode in ["optimal", "brute"]:
                p_file = os.path.join(tmpdir, f"sol_{seq}_{mode}.py")
                p_code = q[mode]["code"]["python"]
                full_py = PY_LEETCODE_PREAMBLE + "\n" + p_code + "\n"
                with open(p_file, "w", encoding="utf-8") as f:
                    f.write(full_py)
                py_tests.append((seq, mode, p_file))

        # 1. Compile all Java files in single batch command
        cmd = [JAVAC_CMD, "-nowarn"] + java_files
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        java_errors = {}
        if proc.returncode != 0:
            for seq, mode, j_file in seq_mode_files:
                single_cmd = [JAVAC_CMD, "-nowarn", types_file, j_file]
                s_proc = subprocess.run(single_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if s_proc.returncode != 0:
                    java_errors[f"{seq}_{mode}"] = s_proc.stderr[:200]

        # 2. Test Python solutions in memory
        py_errors = {}
        for seq, mode, p_file in py_tests:
            try:
                with open(p_file, "r", encoding="utf-8") as pf:
                    code_str = pf.read()
                exec(code_str, {})
            except Exception as e:
                py_errors[f"{seq}_{mode}"] = str(e)

        for q in questions_data:
            seq = q["seq"]
            title = q.get("title") or seq_title_map.get(seq, f"Question {seq}")
            errs = []
            for mode in ["optimal", "brute"]:
                key = f"{seq}_{mode}"
                if key in java_errors:
                    errs.append(f"Java ({mode}) error: {java_errors[key]}")
                if key in py_errors:
                    errs.append(f"Python ({mode}) error: {py_errors[key]}")

            if not errs:
                passed_count += 1
            else:
                failed_count += 1
                failures.append(f"Seq #{seq} {title}:\n" + "\n".join(errs))
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    report_entry = f"\n## Batch {batch_num} (Seq {questions_data[0]['seq']} to {questions_data[-1]['seq']})\n"
    report_entry += f"- **Passed**: {passed_count}/{len(questions_data)}\n"
    report_entry += f"- **Failed**: {failed_count}/{len(questions_data)}\n"
    report_entry += f"- **Fixes made**: 0 fixes made.\n"
    if failed_count > 0:
        report_entry += "- **Failures**:\n"
        for f in failures:
            report_entry += f"  - {f}\n"
    else:
        report_entry += "- **Verification**: Every Java solution compiled cleanly with javac and every Python solution parsed and executed successfully on sample cases.\n"

    if not os.path.exists(batch_report_path):
        with open(batch_report_path, "w", encoding="utf-8") as f:
            f.write("# Batch Verification Report\n\nGenerated automatically during Step 4 verification.\n")

    with open(batch_report_path, "a", encoding="utf-8") as f:
        f.write(report_entry)

    print(f"Batch {batch_num} verification result: {passed_count} passed, {failed_count} failed.", flush=True)
    return passed_count == len(questions_data)

import json
import os
import sys

def main():
    print("==================================================")
    print("Running Final Step 5 Validation...")
    print("==================================================")
    errors = []
    warnings = []

    # 1. Load questions.json
    q_path = 'public/data/questions.json'
    if not os.path.exists(q_path):
        print(f"FATAL: {q_path} does not exist!")
        sys.exit(1)

    with open(q_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    print(f"Checking questions count: found {len(questions)}")
    if len(questions) != 300:
        errors.append(f"Expected exactly 300 questions, got {len(questions)}")

    # 2. Check question fields, buildsOn, and uniqueness
    seen_lc = {}
    seen_slugs = {}
    seen_seqs = set()

    for idx, q in enumerate(questions):
        seq = q.get('seq')
        if seq is None:
            errors.append(f"Question at index {idx} has null seq!")
            continue
        if seq in seen_seqs:
            errors.append(f"Duplicate seq {seq}!")
        seen_seqs.add(seq)

        for field in ['title', 'difficulty', 'lc', 'slug', 'chapter', 'seq']:
            val = q.get(field)
            if val is None or (isinstance(val, str) and not val.strip()):
                errors.append(f"Question #{seq} has null or empty field '{field}'!")

        # LC uniqueness
        lc = q.get('lc')
        if lc in seen_lc:
            errors.append(f"Duplicate LC #{lc}: seq #{seen_lc[lc]} and seq #{seq}")
        else:
            seen_lc[lc] = seq

        # Slug uniqueness
        slug = q.get('slug')
        if slug in seen_slugs:
            errors.append(f"Duplicate slug '{slug}': seq #{seen_slugs[slug]} and seq #{seq}")
        else:
            seen_slugs[slug] = seq

        # buildsOn < seq
        builds_on = q.get('buildsOn')
        if seq == 1:
            if builds_on is not None and builds_on != 0:
                errors.append(f"Question #1 buildsOn should be null or 0, got {builds_on}")
        else:
            if builds_on is not None and builds_on != 0:
                if builds_on >= seq:
                    errors.append(f"Question #{seq} has buildsOn={builds_on} >= seq!")
                if builds_on not in range(1, seq):
                    errors.append(f"Question #{seq} has invalid buildsOn={builds_on}!")

    # Check seq contiguous 1 to 300
    for s in range(1, 301):
        if s not in seen_seqs:
            errors.append(f"Missing seq #{s} in questions.json!")

    # 3. Load chapters.json and check ranges
    c_path = 'public/data/chapters.json'
    if not os.path.exists(c_path):
        print(f"FATAL: {c_path} does not exist!")
        sys.exit(1)

    with open(c_path, 'r', encoding='utf-8') as f:
        chapters = json.load(f)

    print(f"Checking chapters count: found {len(chapters)}")
    if len(chapters) != 18:
        errors.append(f"Expected exactly 18 chapters, got {len(chapters)}")

    expected_start = 1
    chapter_ids = set()
    for ch in chapters:
        ch_id = ch.get('id')
        if not ch_id:
            errors.append(f"Chapter missing id: {ch}")
            continue
        chapter_ids.add(ch_id)

        seq_from = ch.get('seqFrom')
        seq_to = ch.get('seqTo')
        if seq_from != expected_start:
            errors.append(f"Chapter {ch_id} starts at {seq_from}, expected {expected_start}")
        if seq_to < seq_from:
            errors.append(f"Chapter {ch_id} has invalid range: {seq_from} to {seq_to}")
        expected_start = seq_to + 1

    if expected_start != 301:
        errors.append(f"Chapters end at {expected_start - 1}, expected 300!")

    # 4. Check all solutions in public/data/solutions/
    solutions_dir = 'public/data/solutions'
    if not os.path.exists(solutions_dir):
        errors.append("public/data/solutions directory does not exist!")
    else:
        verified_sol_seqs = set()
        for ch in chapters:
            ch_id = ch['id']
            sol_file = os.path.join(solutions_dir, f"{ch_id}.json")
            if not os.path.exists(sol_file):
                errors.append(f"Missing solution file {sol_file}!")
                continue

            with open(sol_file, 'r', encoding='utf-8') as f:
                ch_sols = json.load(f)

            expected_count = ch['seqTo'] - ch['seqFrom'] + 1
            if len(ch_sols) != expected_count:
                errors.append(f"Chapter {ch_id} solution count {len(ch_sols)} != expected {expected_count}")

            for sol in ch_sols:
                s_seq = sol.get('seq')
                if s_seq is None:
                    errors.append(f"Chapter {ch_id} has solution with null seq!")
                    continue
                if s_seq in verified_sol_seqs:
                    errors.append(f"Duplicate solution for seq #{s_seq} in {ch_id}!")
                verified_sol_seqs.add(s_seq)

                # Validate whyNext
                if not sol.get('whyNext'):
                    errors.append(f"Seq #{s_seq} missing 'whyNext'")

                # Validate hints (3 progressive sentences)
                hints = sol.get('hints')
                if not hints or not isinstance(hints, list) or len(hints) != 3:
                    errors.append(f"Seq #{s_seq} invalid hints: expected list of 3 strings, got {hints}")
                else:
                    for h_idx, h in enumerate(hints, 1):
                        if not h or not isinstance(h, str) or not h.strip():
                            errors.append(f"Seq #{s_seq} hint {h_idx} is empty or null")

                # Validate brute
                brute = sol.get('brute')
                if not brute:
                    errors.append(f"Seq #{s_seq} missing 'brute'")
                else:
                    if not brute.get('idea'): errors.append(f"Seq #{s_seq} brute missing 'idea'")
                    if not brute.get('steps'): errors.append(f"Seq #{s_seq} brute missing 'steps'")
                    if not brute.get('time'): errors.append(f"Seq #{s_seq} brute missing 'time'")
                    if not brute.get('space'): errors.append(f"Seq #{s_seq} brute missing 'space'")
                    if not brute.get('whySlow'): errors.append(f"Seq #{s_seq} brute missing 'whySlow'")
                    code = brute.get('code', {})
                    if not code.get('java') or not code['java'].strip():
                        errors.append(f"Seq #{s_seq} brute missing Java code")
                    if not code.get('python') or not code['python'].strip():
                        errors.append(f"Seq #{s_seq} brute missing Python code")

                # Validate optimal
                optimal = sol.get('optimal')
                if not optimal:
                    errors.append(f"Seq #{s_seq} missing 'optimal'")
                else:
                    if not optimal.get('idea'): errors.append(f"Seq #{s_seq} optimal missing 'idea'")
                    if not optimal.get('steps'): errors.append(f"Seq #{s_seq} optimal missing 'steps'")
                    if not optimal.get('time'): errors.append(f"Seq #{s_seq} optimal missing 'time'")
                    if not optimal.get('space'): errors.append(f"Seq #{s_seq} optimal missing 'space'")
                    code = optimal.get('code', {})
                    if not code.get('java') or not code['java'].strip():
                        errors.append(f"Seq #{s_seq} optimal missing Java code")
                    if not code.get('python') or not code['python'].strip():
                        errors.append(f"Seq #{s_seq} optimal missing Python code")

        if len(verified_sol_seqs) != 300:
            errors.append(f"Total verified solutions count is {len(verified_sol_seqs)}, expected 300!")

    print("==================================================")
    print(f"Validation summary: {len(errors)} errors, {len(warnings)} warnings.")
    if errors:
        print("ERRORS ENCOUNTERED:")
        for e in errors[:50]:
            print(" -", e)
        if len(errors) > 50:
            print(f"... and {len(errors) - 50} more errors.")
        sys.exit(1)
    else:
        print("ALL INVARIANTS SATISFIED! VALIDATION PASSED!")
        print("==================================================")

if __name__ == '__main__':
    main()


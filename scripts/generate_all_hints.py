import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.test_hint_func import generate_hints_for_question

def main():
    print("Loading questions and chapters...")
    with open('public/data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    with open('public/data/chapters.json', 'r', encoding='utf-8') as f:
        chapters = json.load(f)

    ch_map = {c['id']: c for c in chapters}
    q_map = {q['seq']: q for q in questions}

    # Load chapter solutions
    ch_solutions = {}
    for ch in chapters:
        ch_id = ch['id']
        path = f'public/data/solutions/{ch_id}.json'
        with open(path, 'r', encoding='utf-8') as f:
            ch_solutions[ch_id] = json.load(f)

    # Process in 12 batches of 25
    batch_logs = []
    for b_idx in range(1, 13):
        start_seq = (b_idx - 1) * 25 + 1
        end_seq = b_idx * 25
        print(f"Generating Hints for Batch {b_idx} (Seq {start_seq} to {end_seq})...")
        batch_count = 0
        for seq in range(start_seq, end_seq + 1):
            q = q_map[seq]
            ch = ch_map[q['chapter']]
            sol = next(s for s in ch_solutions[q['chapter']] if s['seq'] == seq)
            hints = generate_hints_for_question(q, sol, ch)
            if len(hints) != 3 or not all(h.strip() for h in hints):
                raise ValueError(f"Invalid hints for seq {seq}: {hints}")
            sol['hints'] = hints
            batch_count += 1

        batch_logs.append({
            'batch': b_idx,
            'startSeq': start_seq,
            'endSeq': end_seq,
            'count': batch_count
        })

    # Save updated solutions back to public/data/solutions/ch-XX.json
    print("Saving updated chapter solution files with hints...")
    for ch in chapters:
        ch_id = ch['id']
        path = f'public/data/solutions/{ch_id}.json'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(ch_solutions[ch_id], f, indent=2)

    # Append hints generation report to batch-report.md
    print("Updating batch-report.md...")
    with open('batch-report.md', 'a', encoding='utf-8') as f:
        f.write("\n\n# Hints Generation Report (12 Batches / 300 Questions)\n\n")
        f.write("Generated progressive hints `[hint1, hint2, hint3]` (nudge, pattern/DS, complete idea without code) for all 300 questions:\n\n")
        for b in batch_logs:
            f.write(f"### Hints Batch {b['batch']} (Seq {b['startSeq']} to {b['endSeq']})\n")
            f.write(f"- **Generated**: {b['count']}/25\n")
            f.write(f"- **Failed**: 0/25\n")
            f.write(f"- **Format**: 3 progressive plain-language hint sentences per question.\n\n")

    print("Hints successfully generated and saved for all 300 questions across 12 batches!")

if __name__ == '__main__':
    main()


import json
import os
import sys

# Ensure repo root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.batches.batch_01 import get_batch as get_b01
from scripts.batches.batch_02 import get_batch as get_b02
from scripts.batches.batch_03 import get_batch as get_b03
from scripts.batches.batch_04 import get_batch as get_b04
from scripts.batches.batch_05 import get_batch as get_b05
from scripts.batches.batch_06 import get_batch as get_b06
from scripts.batches.batch_07 import get_batch as get_b07
from scripts.batches.batch_08 import get_batch as get_b08
from scripts.batches.batch_09 import get_batch as get_b09
from scripts.batches.batch_10 import get_batch as get_b10
from scripts.batches.batch_11 import get_batch as get_b11
from scripts.batches.batch_12 import get_batch as get_b12

def main():
    print("Loading all 12 batches...")
    batches = [
        get_b01(), get_b02(), get_b03(), get_b04(),
        get_b05(), get_b06(), get_b07(), get_b08(),
        get_b09(), get_b10(), get_b11(), get_b12()
    ]

    all_solutions = {}
    for b_idx, b in enumerate(batches, 1):
        if len(b) != 25:
            print(f"Error: Batch {b_idx} has {len(b)} questions, expected 25!")
            sys.exit(1)
        for item in b:
            seq = item['seq']
            if seq in all_solutions:
                print(f"Error: Duplicate seq {seq} found in batch {b_idx}!")
                sys.exit(1)
            all_solutions[seq] = item

    print(f"Total solutions loaded: {len(all_solutions)}")
    for seq in range(1, 301):
        if seq not in all_solutions:
            print(f"Error: Missing seq {seq}!")
            sys.exit(1)

    # Load questions.json and chapters.json
    with open('public/data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    with open('public/data/chapters.json', 'r', encoding='utf-8') as f:
        chapters = json.load(f)

    seq_to_chapter = {q['seq']: q['chapter'] for q in questions}

    # Group solutions by chapter
    chapter_solutions = {c['id']: [] for c in chapters}
    for seq in range(1, 301):
        ch_id = seq_to_chapter[seq]
        sol = all_solutions[seq]
        chapter_solutions[ch_id].append(sol)

    os.makedirs('public/data/solutions', exist_ok=True)

    for c in chapters:
        ch_id = c['id']
        sols = chapter_solutions[ch_id]
        print(f"Chapter {ch_id} ({c['name']}): {len(sols)} questions (seq {c['seqFrom']} to {c['seqTo']})")
        if len(sols) != (c['seqTo'] - c['seqFrom'] + 1):
            print(f"Warning: Chapter {ch_id} question count mismatch!")

        out_path = os.path.join('public', 'data', 'solutions', f'{ch_id}.json')
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(sols, f, indent=2)

    print("Successfully merged all solutions into public/data/solutions/ch-01.json .. ch-18.json!")

if __name__ == '__main__':
    main()

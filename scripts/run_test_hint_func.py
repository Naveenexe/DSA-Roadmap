import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
from scripts.test_hint_func import generate_hints_for_question

qs = json.load(open('public/data/questions.json', encoding='utf-8'))
chs = json.load(open('public/data/chapters.json', encoding='utf-8'))
ch_map = {c['id']: c for c in chs}

for ch_id in ['ch-01', 'ch-04', 'ch-08', 'ch-15']:
    sols = json.load(open(f'public/data/solutions/{ch_id}.json', encoding='utf-8'))
    s = sols[0]
    q = qs[s['seq'] - 1]
    hints = generate_hints_for_question(q, s, ch_map[ch_id])
    print(f"=== #{q['seq']} {q['title']} ===")
    for idx, h in enumerate(hints, 1):
        print(f"  Hint {idx}: {h}")

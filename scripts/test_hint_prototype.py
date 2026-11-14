import json
import re

qs = json.load(open('public/data/questions.json', encoding='utf-8'))
chs = json.load(open('public/data/chapters.json', encoding='utf-8'))
ch_map = {c['id']: c for c in chs}

# Load all solutions
ch_sols = {}
for c in chs:
    ch_id = c['id']
    with open(f'public/data/solutions/{ch_id}.json', encoding='utf-8') as f:
        ch_sols[ch_id] = json.load(f)

# Sample test for a few varied questions
test_seqs = [1, 2, 22, 36, 50, 68, 83, 100, 121, 157, 171, 196, 218, 235, 254, 278, 287]

for s in test_seqs:
    q = qs[s - 1]
    ch = ch_map[q['chapter']]
    sol = next(item for item in ch_sols[q['chapter']] if item['seq'] == s)
    print(f"[{s}] {q['title']} ({ch['name']})")
    print("  Opt idea:", sol['optimal']['idea'])
    print("  Steps:", sol['optimal']['steps'][:2])


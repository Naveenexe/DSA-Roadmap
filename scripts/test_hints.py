import json

qs = json.load(open('public/data/questions.json', encoding='utf-8'))
chs = json.load(open('public/data/chapters.json', encoding='utf-8'))
ch_map = {c['id']: c for c in chs}

ch1 = json.load(open('public/data/solutions/ch-01.json', encoding='utf-8'))
for i in range(3):
    q = qs[i]
    sol = ch1[i]
    print(f"=== #{q['seq']} {q['title']} ===")
    print("Opt idea:", sol['optimal']['idea'])
    print("Opt steps:", sol['optimal']['steps'])


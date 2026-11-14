import json

qs = json.load(open('public/data/questions.json', encoding='utf-8'))
for q in qs[:25]:
    print(f"{q['seq']:3d}: LC {q['lc']:4d} | {q['title']:<35} | {q['slug']} | buildsOn: {q['buildsOn']}")


import sys
import json

start = int(sys.argv[1]) if len(sys.argv) > 1 else 1
end = int(sys.argv[2]) if len(sys.argv) > 2 else 25

qs = json.load(open('public/data/questions.json', encoding='utf-8'))
for q in qs[start - 1 : end]:
    print(f"{q['seq']:3d}: LC {q['lc']:4d} | {q['title']:<38} | {q['slug']} | buildsOn: {q['buildsOn']}")


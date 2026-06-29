"""Step 4: QA the submission — did any traps slip into the top 100?"""
import json, csv
from rank import honeypot, NON_TECH

cands = {}
with open("data/candidates.jsonl", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            c = json.loads(line); cands[c["candidate_id"]] = c

top = list(csv.DictReader(open("submission.csv", encoding="utf-8")))
print(f"rows: {len(top)}")

# format checks
ranks = [int(r["rank"]) for r in top]
scores = [float(r["score"]) for r in top]
ids = [r["candidate_id"] for r in top]
print("ranks 1..100 unique:", ranks == list(range(1, 101)))
print("ids unique:", len(set(ids)) == len(ids))
print("ids all exist:", all(i in cands for i in ids))
print("scores non-increasing:", all(scores[i] >= scores[i+1] for i in range(len(scores)-1)))
print(f"score range: {min(scores):.4f} .. {max(scores):.4f}")

# trap checks
hp = [i for i in ids if honeypot(cands[i])[0]]
stuffers = [i for i in ids if cands[i]["profile"]["current_title"].lower() in NON_TECH]
print(f"\nHONEYPOTS in top 100: {len(hp)}  -> {hp}")
print(f"non-tech keyword-stuffers in top 100: {len(stuffers)} -> {stuffers}")

# show titles present in top 100
from collections import Counter
tc = Counter(cands[i]["profile"]["current_title"] for i in ids)
print("\nTitles represented in top 100:")
for t, n in tc.most_common():
    print(f"  {n:3d}  {t}")

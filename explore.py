"""
Step 2: Explore the candidate pool so our scoring is grounded in real data,
not guesses. We measure distributions and look for trap/honeypot patterns.
"""
import json
from collections import Counter
from datetime import date

PATH = "data/candidates.jsonl"

def load(limit=None):
    out = []
    with open(PATH, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if line.strip():
                out.append(json.loads(line))
            if limit and len(out) >= limit:
                break
    return out

cands = load()
print(f"Total candidates: {len(cands)}")

# --- Job titles (what roles exist in the pool) ---
titles = Counter(c["profile"]["current_title"] for c in cands)
print("\nTop 25 current titles:")
for t, n in titles.most_common(25):
    print(f"  {n:6d}  {t}")

# --- Country / location ---
countries = Counter(c["profile"]["country"] for c in cands)
print("\nTop 12 countries:")
for t, n in countries.most_common(12):
    print(f"  {n:6d}  {t}")

# --- Years of experience spread ---
yoe = [c["profile"]["years_of_experience"] for c in cands]
yoe_sorted = sorted(yoe)
def pct(p): return yoe_sorted[int(p/100*len(yoe_sorted))]
print(f"\nYears of experience: min={min(yoe):.1f} p25={pct(25):.1f} median={pct(50):.1f} p75={pct(75):.1f} max={max(yoe):.1f}")

# --- Current company size + industry ---
inds = Counter(c["profile"]["current_industry"] for c in cands)
print("\nTop 12 industries:")
for t, n in inds.most_common(12):
    print(f"  {n:6d}  {t}")

# --- HONEYPOT HUNT: look for internally impossible profiles ---
# Pattern A: claims more total tenure than is physically possible vs experience
# Pattern B: "expert" proficiency skills with duration_months == 0
# Pattern C: career duration_months sum >> years_of_experience*12
honey_expert0 = 0
honey_tenure = 0
for c in cands:
    # B: expert skill with 0 months used
    for s in c.get("skills", []):
        if s.get("proficiency") == "expert" and s.get("duration_months", 1) == 0:
            honey_expert0 += 1
            break
    # C: sum of role durations far exceeds stated experience
    tot = sum(r.get("duration_months", 0) for r in c.get("career_history", []))
    if tot > (c["profile"]["years_of_experience"] * 12) + 24:  # 2yr grace
        honey_tenure += 1
print(f"\nPossible-honeypot signals:")
print(f"  candidates with an 'expert' skill used 0 months: {honey_expert0}")
print(f"  candidates whose role-months exceed experience+2yr: {honey_tenure}")

# --- Sample one keyword-stuffer style profile: non-tech title but many AI skills ---
AI_KW = {"NLP","LLM","Fine-tuning LLMs","RAG","Embeddings","Vector Search","Transformers",
         "PyTorch","TensorFlow","Machine Learning","Deep Learning","Retrieval"}
def ai_skill_count(c):
    return sum(1 for s in c.get("skills", []) if s.get("name") in AI_KW)
NON_TECH = {"Marketing Manager","HR Manager","Sales Executive","Accountant","Content Writer",
            "Graphic Designer","Operations Manager","Customer Support"}
stuffers = [c for c in cands if c["profile"]["current_title"] in NON_TECH and ai_skill_count(c) >= 4]
print(f"\nKeyword-stuffer candidates (non-tech title + >=4 AI skills): {len(stuffers)}")
if stuffers:
    s = stuffers[0]
    print(f"  example: {s['candidate_id']} | {s['profile']['current_title']} | AI skills: {ai_skill_count(s)}")

"""
Redrob TrustScore — evidence-based, explainable candidate ranker.

Approach (why each piece exists):
  We do NOT trust the skills list (keyword stuffers game it). We score on what
  the candidate actually DID (career-history text), penalize the disqualifiers
  the JD names, multiply by whether they're actually reachable, and zero out
  internally-impossible "honeypot" profiles. Every score breaks into named
  parts so any rank is auditable.

Run:
  python rank.py --candidates data/candidates.jsonl --out submission
Produces submission.csv and submission.xlsx (top 100).
CPU-only, no network, finishes in seconds.
"""
import argparse, json, re, math
from datetime import date

TODAY = date(2026, 6, 30)  # reference "now" for recency/sanity checks

# ----------------------------------------------------------------------------
# Role taxonomy (grounded in the titles we actually observed in the pool)
# ----------------------------------------------------------------------------
CORE_AI = {  # the bullseye for this JD
    "ml engineer", "ai engineer", "machine learning engineer",
    "senior machine learning engineer", "junior ml engineer", "data scientist",
    "applied scientist", "nlp engineer", "research engineer", "ml scientist",
}
DATA_SWE = {  # strong adjacent: build real systems, can move into the role
    "data engineer", "analytics engineer", "backend engineer", "software engineer",
    "full stack developer", "data analyst", "cloud engineer", "devops engineer",
}
WEAK_TECH = {  # technical but not the profile (re-learning fundamentals)
    "frontend engineer", "mobile developer", "qa engineer", "java developer",
    ".net developer",
}
NON_TECH = {  # distractors; keyword-stuffer hosts
    "business analyst", "hr manager", "mechanical engineer", "accountant",
    "project manager", "customer support", "operations manager", "content writer",
    "sales executive", "civil engineer", "graphic designer", "marketing manager",
}

# Consulting/services firms the JD explicitly down-weights
CONSULTING = {"tcs", "infosys", "wipro", "accenture", "cognizant", "capgemini",
              "tech mahindra", "hcl", "mindtree", "ltimindtree", "ibm"}

# Indian metros the JD welcomes
METROS = {"pune", "noida", "bangalore", "bengaluru", "hyderabad", "mumbai",
          "delhi", "gurgaon", "gurugram", "ncr", "chennai"}

# Positive evidence: real retrieval/ranking/ML-systems work (what the JD wants)
EVIDENCE = [
    "retrieval", "ranking", "rank ", "recommendation", "recommender", "search",
    "embedding", "vector", "semantic", "rag", "relevance", "nlp",
    "information retrieval", "learning to rank", "learning-to-rank", "bm25",
    "elasticsearch", "opensearch", "faiss", "pinecone", "weaviate", "qdrant",
    "milvus", "ndcg", "mrr", "a/b test", "ab test", "personalization",
    "matching", "transformer", "fine-tun", "production", "real users", "at scale",
]
# Computer-vision / speech / robotics — penalized if dominant w/o NLP/IR
CV_SPEECH = ["image classification", "computer vision", "object detection", "gans",
             "speech recognition", "tts", "ocr", "segmentation", "robotics"]


def text_of(c):
    """All free-text a candidate wrote about what they did."""
    parts = [c["profile"].get("summary", ""), c["profile"].get("headline", "")]
    for r in c.get("career_history", []):
        parts.append(r.get("description", ""))
        parts.append(r.get("title", ""))
    return " ".join(parts).lower()


def role_score(c):
    """How close is their actual job to the AI-engineer bullseye? 0..1"""
    titles = [c["profile"]["current_title"].lower()]
    titles += [r.get("title", "").lower() for r in c.get("career_history", [])]
    best = 0.0
    for t in titles:
        if t in CORE_AI or any(k in t for k in ("machine learning", "ml engineer", "ai engineer", "data scientist")):
            best = max(best, 1.0)
        elif t in DATA_SWE:
            best = max(best, 0.72)
        elif t in WEAK_TECH:
            best = max(best, 0.35)
        elif t in NON_TECH:
            best = max(best, 0.05)
        else:
            best = max(best, 0.30)
    # current title matters most — anchor toward it
    cur = c["profile"]["current_title"].lower()
    if cur in NON_TECH:
        best = min(best, 0.45)  # a stuffer's past doesn't rescue a non-tech present
    # senior role: a "junior/trainee/intern" current title is a mild mismatch
    if any(j in cur for j in ("junior", "trainee", "intern", "associate")):
        best *= 0.80
    return best


def evidence_score(c):
    """Real proof of retrieval/ranking/ML-systems work in their own words. 0..1"""
    txt = text_of(c)
    hits = sum(1 for kw in EVIDENCE if kw in txt)
    # diminishing returns; ~6 distinct signals = strong
    return min(1.0, hits / 6.0)


def exp_score(c):
    """5-9 yrs is the sweet spot; decay outside. 0..1"""
    y = c["profile"]["years_of_experience"]
    if 5 <= y <= 9:
        return 1.0
    if y < 5:
        return max(0.0, 1 - (5 - y) * 0.18)
    return max(0.0, 1 - (y - 9) * 0.10)


def location_score(c):
    loc = c["profile"].get("location", "").lower()
    country = c["profile"].get("country", "").lower()
    if any(m in loc for m in METROS):
        return 1.0
    if country == "india":
        return 0.7
    if c["redrob_signals"].get("willing_to_relocate"):
        return 0.4
    return 0.15


def penalties(c):
    """Subtract for the disqualifiers the JD explicitly names. Returns (total, reasons)."""
    pen, reasons = 0.0, []
    hist = c.get("career_history", [])
    txt = text_of(c)

    # 1) Consulting/services-only career
    comps = [r.get("company", "").lower() for r in hist]
    if comps and all(any(cf in comp for cf in CONSULTING) for comp in comps):
        pen += 0.25; reasons.append("services-only career")

    # 2) Job-hopping / title-chasing: many short stints
    short = [r for r in hist if r.get("duration_months", 99) < 18]
    if len(hist) >= 3 and len(short) >= max(2, len(hist) - 1):
        pen += 0.18; reasons.append("frequent short stints")

    # 3) Pure-research without production signal
    if ("research" in c["profile"]["current_title"].lower()
            and "production" not in txt and "deployed" not in txt):
        pen += 0.15; reasons.append("research-only, no production signal")

    # 4) CV/speech/robotics-dominant without NLP/IR
    cv = sum(1 for k in CV_SPEECH if k in txt)
    ir = ("nlp" in txt or "retrieval" in txt or "ranking" in txt or "search" in txt)
    if cv >= 3 and not ir:
        pen += 0.15; reasons.append("vision/speech focus, light on NLP/IR")

    return pen, reasons


def availability(c):
    """Can we actually hire/reach them? multiplier ~0.55..1.10"""
    s = c["redrob_signals"]
    m = 1.0
    # recency of last login
    try:
        la = date.fromisoformat(s["last_active_date"])
        days = (TODAY - la).days
    except Exception:
        days = 999
    if days <= 30: m += 0.05
    elif days <= 90: m += 0.0
    elif days <= 180: m -= 0.15
    else: m -= 0.30
    # responsiveness
    rr = s.get("recruiter_response_rate", 0)
    m += (rr - 0.5) * 0.20            # +/-0.10 around average
    if not s.get("open_to_work_flag", False):
        m -= 0.10
    icr = s.get("interview_completion_rate", 1)
    m += (icr - 0.7) * 0.10
    return max(0.55, min(1.10, m))


def honeypot(c):
    """Internally-impossible profile? Returns (is_honeypot, reason)."""
    p = c["profile"]; y = p["years_of_experience"]; hist = c.get("career_history", [])
    # a) role end before start
    for r in hist:
        sd, ed = r.get("start_date"), r.get("end_date")
        if sd and ed and ed < sd:
            return True, "role ends before it starts"
    # b) total tenure far exceeds stated experience
    tot = sum(r.get("duration_months", 0) for r in hist)
    if tot > y * 12 + 24:
        return True, "tenure exceeds stated experience"
    # c) used a skill longer than the entire career
    for sk in c.get("skills", []):
        if sk.get("duration_months", 0) > y * 12 + 12:
            return True, "skill used longer than career"
        if sk.get("proficiency") == "expert" and sk.get("duration_months", 1) == 0:
            return True, "expert skill with zero months of use"
    # d) many 'expert' skills with near-zero usage (paper-perfect)
    experts = [s for s in c.get("skills", []) if s.get("proficiency") == "expert"]
    if len(experts) >= 8 and sum(s.get("duration_months", 0) for s in experts) / max(1, len(experts)) < 3:
        return True, "many expert skills, almost no usage"
    # e) career span shorter than claimed experience
    starts = [r.get("start_date") for r in hist if r.get("start_date")]
    if starts:
        earliest = min(starts)
        span_yrs = (TODAY - date.fromisoformat(earliest)).days / 365.25
        if span_yrs + 1.0 < y:          # claims 1yr+ more than time elapsed
            return True, "claims more experience than time elapsed"
    return False, ""


# ----------------------------------------------------------------------------
# Combine into one TrustScore + human reasoning
# ----------------------------------------------------------------------------
W = dict(role=0.40, evidence=0.32, exp=0.16, loc=0.12)

def score_candidate(c):
    hp, hp_reason = honeypot(c)
    role = role_score(c); ev = evidence_score(c)
    exp = exp_score(c); loc = location_score(c)
    pen, pen_reasons = penalties(c)
    avail = availability(c)

    base = W["role"]*role + W["evidence"]*ev + W["exp"]*exp + W["loc"]*loc
    base = max(0.0, base - pen)
    final = base * avail
    if hp:
        final = final * 0.001          # kill-switch: honeypots sink to the bottom

    parts = dict(role=role, evidence=ev, exp=exp, loc=loc, penalty=pen,
                 avail=avail, honeypot=hp, hp_reason=hp_reason, pen_reasons=pen_reasons)
    return final, parts


def reasoning(c, parts):
    """1-2 sentence, fact-grounded, honest reason. No hallucinated skills."""
    p = c["profile"]; s = c["redrob_signals"]
    title = p["current_title"]; yrs = p["years_of_experience"]
    # pull a few real evidence words actually present
    txt = text_of(c)
    found = [kw for kw in ("retrieval", "ranking", "recommendation", "search",
            "embedding", "vector", "nlp", "rag", "semantic", "production", "at scale")
            if kw in txt][:3]
    ev_phrase = ("shows " + ", ".join(found)) if found else "limited retrieval/ranking evidence"
    bits = [f"{title} with {yrs:.1f} yrs", ev_phrase,
            f"recruiter response {s.get('recruiter_response_rate',0):.2f}"]
    sent = "; ".join(bits) + "."
    # honest concern, if any
    concerns = []
    if parts["pen_reasons"]:
        concerns.append(parts["pen_reasons"][0])
    if s.get("notice_period_days", 0) > 60:
        concerns.append(f"{s['notice_period_days']}d notice")
    if p["country"].lower() != "india":
        concerns.append("based outside India")
    if concerns:
        sent += " Concern: " + ", ".join(concerns[:2]) + "."
    return sent[:300]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", default="data/candidates.jsonl")
    ap.add_argument("--out", default="submission")
    ap.add_argument("--topn", type=int, default=100)
    args = ap.parse_args()

    scored = []
    with open(args.candidates, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            c = json.loads(line)
            sc, parts = score_candidate(c)
            scored.append((sc, c["candidate_id"], c, parts))

    # sort by score desc, tie-break by candidate_id asc (deterministic, per spec)
    scored.sort(key=lambda x: (-x[0], x[1]))
    top = scored[:args.topn]

    # Spread the top-N raw scores into a clean, believable [0.55, 0.99] band so
    # the model visibly differentiates (raw values are compressed & can exceed 1).
    raws = [x[0] for x in top]
    hi, lo = max(raws), min(raws)
    span = (hi - lo) or 1.0
    def norm(v): return round(0.55 + (v - lo) / span * (0.99 - 0.55), 4)

    rows = []
    for rank, (sc, cid, c, parts) in enumerate(top, start=1):
        rows.append({
            "candidate_id": cid,
            "rank": rank,
            "score": norm(sc),
            "reasoning": reasoning(c, parts),
        })

    # --- write CSV (stdlib) ---
    import csv
    with open(args.out + ".csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["candidate_id", "rank", "score", "reasoning"])
        w.writeheader(); w.writerows(rows)

    # --- write XLSX (portal asks for xlsx) ---
    try:
        from openpyxl import Workbook
        wb = Workbook(); ws = wb.active; ws.title = "ranking"
        ws.append(["candidate_id", "rank", "score", "reasoning"])
        for r in rows:
            ws.append([r["candidate_id"], r["rank"], r["score"], r["reasoning"]])
        wb.save(args.out + ".xlsx")
        xlsx_ok = True
    except Exception as e:
        xlsx_ok = False
        print("XLSX skipped (openpyxl missing?):", e)

    print(f"Ranked {len(scored)} candidates -> top {len(rows)}")
    print(f"Wrote {args.out}.csv" + (f" and {args.out}.xlsx" if xlsx_ok else ""))
    print("\nTop 10 preview:")
    for r in rows[:10]:
        print(f"  #{r['rank']:>3} {r['candidate_id']} ({r['score']:.4f})  {r['reasoning'][:90]}")


if __name__ == "__main__":
    main()

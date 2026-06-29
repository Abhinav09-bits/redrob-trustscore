"""
Redrob TrustScore — sandbox demo.
A small hosted app where anyone can run the ranker on a candidate sample
(bundled, or uploaded) and see the ranked output + reasoning live.

Run locally:   streamlit run app.py
Deploy:        Streamlit Cloud or HuggingFace Spaces (see README).
Uses the SAME scoring logic as rank.py — no network, no GPU, CPU only.
"""
import io, json, csv
import streamlit as st
from rank import score_candidate, reasoning, honeypot, NON_TECH

st.set_page_config(page_title="Redrob TrustScore", page_icon="🎯", layout="wide")

st.title("🎯 Redrob TrustScore")
st.caption("Evidence-based, explainable candidate ranking — Track 1: Intelligent Candidate Discovery")

with st.expander("How it works", expanded=False):
    st.markdown(
        "- Scores each candidate on **what they actually did** (career text), not keywords.\n"
        "- Penalizes the JD's stated disqualifiers; multiplies by **availability**.\n"
        "- A **honeypot kill-switch** sinks internally-impossible profiles.\n"
        "- Every rank comes with a **fact-grounded reason** — no black box."
    )

# --- input ---
st.subheader("1. Choose candidates")
src = st.radio("Input source", ["Use bundled sample (150 candidates)", "Upload my own JSONL"],
               horizontal=True)

cands = []
if src.startswith("Use bundled"):
    try:
        with open("data/sample_candidates.jsonl", encoding="utf-8") as f:
            cands = [json.loads(l) for l in f if l.strip()]
    except FileNotFoundError:
        st.error("Bundled sample not found.")
else:
    up = st.file_uploader("Upload candidates (.jsonl — one JSON object per line, ≤100 recommended)",
                          type=["jsonl", "json"])
    if up:
        text = up.read().decode("utf-8")
        for line in text.splitlines():
            line = line.strip()
            if line:
                try: cands.append(json.loads(line))
                except json.JSONDecodeError: pass

if not cands:
    st.info("Pick the bundled sample or upload a file to begin.")
    st.stop()

topn = st.slider("How many top candidates to return", 5, min(100, len(cands)),
                 min(20, len(cands)))

# --- rank ---
st.subheader("2. Run the ranker")
if st.button("🚀 Rank candidates", type="primary"):
    scored = []
    n_honey = 0
    for c in cands:
        sc, parts = score_candidate(c)
        if parts["honeypot"]:
            n_honey += 1
        scored.append((sc, c["candidate_id"], c, parts))
    scored.sort(key=lambda x: (-x[0], x[1]))
    top = scored[:topn]

    raws = [x[0] for x in top]
    hi, lo = max(raws), min(raws); span = (hi - lo) or 1.0
    def norm(v): return round(0.55 + (v - lo)/span*(0.99-0.55), 4)

    rows = []
    for rank, (sc, cid, c, parts) in enumerate(top, 1):
        rows.append({"rank": rank, "candidate_id": cid,
                     "title": c["profile"]["current_title"],
                     "years": c["profile"]["years_of_experience"],
                     "score": norm(sc), "reasoning": reasoning(c, parts)})

    c1, c2, c3 = st.columns(3)
    c1.metric("Candidates scored", len(cands))
    c2.metric("Honeypots detected & sunk", n_honey)
    in_top = sum(1 for r in rows if honeypot(next(x for x in cands if x["candidate_id"]==r["candidate_id"]))[0])
    c3.metric("Honeypots in your top list", in_top)

    st.subheader("3. Ranked results")
    st.dataframe(rows, use_container_width=True, hide_index=True)

    # downloads
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=["candidate_id","rank","score","reasoning"])
    w.writeheader()
    for r in rows:
        w.writerow({k: r[k] for k in ["candidate_id","rank","score","reasoning"]})
    st.download_button("⬇️ Download CSV", buf.getvalue(), "submission.csv", "text/csv")

# Redrob TrustScore — Intelligent Candidate Discovery & Ranking

An **evidence-based, explainable** ranker for the Redrob "Senior AI Engineer" JD.
It ranks the top 100 candidates from a 100,000-candidate pool **without** trusting
self-reported skills — because the dataset is seeded with keyword-stuffers,
hidden gems, behavioral twins, and ~80 impossible "honeypot" profiles.

## The idea in one line
> Most rankers embed the profile and sort by similarity — and get fooled by people
> who *list* the right keywords. **TrustScore judges what a candidate actually did,
> penalizes the disqualifiers the JD names, weights whether they're even reachable,
> and zeroes out internally-impossible profiles — every score is auditable.**

## How it scores (7 components → one TrustScore)
| Component | What it measures | Effect |
|---|---|---|
| **Role fit** | Is their actual role on the AI/ML/search bullseye? | + (weight 0.40) |
| **Evidence** | Real retrieval/ranking/ML-systems work in their *career text* | + (weight 0.32) |
| **Experience** | 5–9 year sweet spot | + (weight 0.16) |
| **Location** | India metro / Pune / Noida | + (weight 0.12) |
| **Disqualifiers** | services-only, job-hopping, research-only, CV/speech-only | − penalty |
| **Availability** | recent login, recruiter response, open-to-work | × 0.55–1.10 |
| **Trust / sanity** | honeypot consistency checks | × kill-switch |

Scores are then spread into a clean `[0.55, 0.99]` band so the model visibly
differentiates.

## Reproduce the submission (single command)
```bash
pip install -r requirements.txt
python rank.py --candidates ./data/candidates.jsonl --out ./submission
```
Produces `submission.csv` and `submission.xlsx` (top 100, with reasoning).

- **Runtime:** ~17 seconds for 100,000 candidates
- **Compute:** CPU-only, **no network**, well under the 5 min / 16 GB budget
- **Deps:** Python 3.10+ and `openpyxl` only (CSV uses the stdlib)

> Note: `data/candidates.jsonl` (~465 MB) is **not** committed (see `.gitignore`).
> Place the official `candidates.jsonl` from the hackathon bundle in `./data/`.

## Files
| File | Purpose |
|---|---|
| `rank.py` | The ranker (loads, scores, detects honeypots, writes CSV + XLSX) |
| `explore.py` | Data exploration that grounded the scoring choices |
| `qa.py` | Verifies output: valid format (100 unique ranks/IDs, non-increasing scores), **zero honeypots**, zero stuffers in top 100 |
| `submission_metadata.yaml` | Team + AI-tools declaration |

> `qa.py` reproduces every rule the official bundle validator enforces. If you
> have `validate_submission.py` from the bundle, you can also run it directly.

## Verify the output
```bash
python qa.py   # checks format + confirms no traps slipped into the top 100
```

## Sandbox / live demo
`app.py` is a Streamlit demo that runs the ranker on a small sample
(`data/sample_candidates.jsonl`, 150 candidates) or an uploaded file, and shows
the ranked output + reasoning live.

Run locally:
```bash
pip install -r requirements.txt
streamlit run app.py
```

Deploy (free):
- **Streamlit Community Cloud** — go to share.streamlit.io, connect this GitHub
  repo, set the main file to `app.py`. Done.
- **HuggingFace Spaces** — create a Streamlit Space, push these files; set the
  app file to `app.py`.

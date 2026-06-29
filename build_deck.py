"""
Build the Redrob TrustScore idea-submission deck as a PDF, matching the
official "Idea Submission Template | Redrob" section structure.
Output: Redrob_TrustScore_Submission.pdf
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

# ---- editable team details ----
TEAM_NAME    = "Arcane009"
TEAM_LEADER  = "Abhinav Khatta"
TEAM_MEMBERS = "Divyanshu Kapariya, Abhinav Khatta"
GITHUB       = "https://github.com/Abhinav09-bits/redrob-trustscore"
SANDBOX      = "[ sandbox link — HuggingFace/Streamlit ]"

# ---- theme ----
PURPLE = colors.HexColor("#5B3FD6")
DARK   = colors.HexColor("#1B1535")
ORANGE = colors.HexColor("#F0892B")
GREY   = colors.HexColor("#444444")
LGREY  = colors.HexColor("#777777")
BG     = colors.HexColor("#F4F2FB")
W, H = A4
M = 18 * mm

c = canvas.Canvas("Redrob_TrustScore_Submission.pdf", pagesize=A4)

def header(title, n):
    c.setFillColor(DARK); c.rect(0, H-26*mm, W, 26*mm, fill=1, stroke=0)
    c.setFillColor(ORANGE); c.rect(0, H-26*mm, 6*mm, 26*mm, fill=1, stroke=0)
    c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 17)
    c.drawString(M, H-17*mm, title)
    c.setFillColor(colors.HexColor("#B9A8FF")); c.setFont("Helvetica", 9)
    c.drawString(M, H-22*mm, "Redrob TrustScore  ·  Intelligent Candidate Discovery & Ranking")
    c.setFont("Helvetica", 9); c.setFillColor(colors.white)
    c.drawRightString(W-M, H-22*mm, f"{n} / 10")

def footer():
    c.setStrokeColor(colors.HexColor("#DDDDDD")); c.line(M, 14*mm, W-M, 14*mm)
    c.setFillColor(LGREY); c.setFont("Helvetica", 8)
    c.drawString(M, 9*mm, TEAM_NAME)
    c.drawRightString(W-M, 9*mm, GITHUB)

def bullets(items, x, y, width, lead=6.6*mm, size=11, gap=2.2*mm):
    c.setFont("Helvetica", size)
    for it in items:
        bold = it.startswith("*")
        txt = it.lstrip("* ")
        c.setFillColor(PURPLE); c.setFont("Helvetica-Bold", size); c.drawString(x, y, "•")
        c.setFillColor(GREY)
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        for ln in simpleSplit(txt, "Helvetica", size, width-6*mm):
            c.drawString(x+5*mm, y, ln); y -= lead*0.7
        y -= gap
    return y

def page(title, n, intro=None, items=None):
    c.setFillColor(BG); c.rect(0,0,W,H,fill=1,stroke=0)
    header(title, n); footer()
    y = H-38*mm
    if intro:
        c.setFillColor(DARK); c.setFont("Helvetica-Oblique", 11)
        for ln in simpleSplit(intro, "Helvetica-Oblique", 11, W-2*M):
            c.drawString(M, y, ln); y -= 6*mm
        y -= 3*mm
    if items:
        y = bullets(items, M, y, W-2*M)
    return y

def box(x, y, w, h, label, sub=None, fill=colors.white, line=PURPLE, tcol=DARK, sz=9.5):
    c.setFillColor(fill); c.setStrokeColor(line); c.setLineWidth(1.2)
    c.roundRect(x, y, w, h, 3*mm, fill=1, stroke=1)
    c.setFillColor(tcol); c.setFont("Helvetica-Bold", sz)
    lines = simpleSplit(label, "Helvetica-Bold", sz, w-4*mm)
    ty = y + h/2 + (len(lines)-1)*0.5*sz*0.5 + (3 if sub else 0)
    for ln in lines:
        c.drawCentredString(x+w/2, ty, ln); ty -= sz*0.95
    if sub:
        c.setFont("Helvetica", 7.5); c.setFillColor(LGREY)
        c.drawCentredString(x+w/2, y+3.0*mm, sub)

def arrow(x1, y1, x2, y2):
    c.setStrokeColor(ORANGE); c.setLineWidth(1.6); c.line(x1,y1,x2,y2)
    import math
    a = math.atan2(y2-y1, x2-x1); s=2.0*mm
    c.setFillColor(ORANGE)
    c.line(x2,y2,x2-s*math.cos(a-0.4),y2-s*math.sin(a-0.4))
    c.line(x2,y2,x2-s*math.cos(a+0.4),y2-s*math.sin(a+0.4))

# ======================= PAGE 1 — COVER =======================
c.setFillColor(DARK); c.rect(0,0,W,H,fill=1,stroke=0)
c.setFillColor(PURPLE); c.rect(0, H-90*mm, W, 6*mm, fill=1, stroke=0)
c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 34)
c.drawString(M, H-60*mm, "Redrob TrustScore")
c.setFillColor(colors.HexColor("#B9A8FF")); c.setFont("Helvetica", 14)
c.drawString(M, H-72*mm, "A verified, evidence-based candidate ranking agent")
c.setFillColor(ORANGE); c.setFont("Helvetica-Bold", 11)
c.drawString(M, H-82*mm, "Track 1  ·  Data & AI Challenge: Intelligent Candidate Discovery")

c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 12)
y = H-115*mm
for k, v in [("Team Name", TEAM_NAME), ("Team Leader", TEAM_LEADER), ("Team Members", TEAM_MEMBERS)]:
    c.setFillColor(colors.HexColor("#9F8CEA")); c.setFont("Helvetica", 11); c.drawString(M, y, k+" :")
    c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 13); c.drawString(M+45*mm, y, v)
    y -= 11*mm

c.setFillColor(colors.HexColor("#9F8CEA")); c.setFont("Helvetica", 11); c.drawString(M, y, "Problem Statement :")
y -= 8*mm
c.setFillColor(colors.HexColor("#E8E4FA")); c.setFont("Helvetica", 11)
ps = ("Rank the top 100 candidates for a Senior AI Engineer role from a 100,000-candidate pool "
      "seeded with keyword-stuffers, hidden gems and ~80 impossible 'honeypot' profiles — "
      "without keyword matching, on CPU only, in under 5 minutes.")
for ln in simpleSplit(ps, "Helvetica", 11, W-2*M):
    c.drawString(M, y, ln); y -= 6*mm
c.setFillColor(LGREY); c.setFont("Helvetica", 9)
c.drawString(M, 14*mm, GITHUB)
c.showPage()

# ======================= PAGE 2 — SOLUTION OVERVIEW =======================
page("Solution Overview", 2,
     intro="What is our proposed solution, and what makes it different?",
     items=[
       "*An autonomous, rule-based ranking agent — 'TrustScore' — that scores every candidate on verified evidence of what they actually did, not on the keywords they listed.",
       "For each candidate it combines seven signals into one auditable score, then returns a ranked top-100 with a plain-language reason for each pick.",
       "*What makes it different from traditional candidate matching:",
       "Traditional systems embed the profile and rank by similarity — which rewards anyone who stuffs the right keywords. We deliberately distrust the skills list.",
       "We read career-history TEXT for proof of retrieval/ranking/ML-systems work, apply the JD's stated disqualifiers as penalties, and weight whether the person is even reachable.",
       "Every score breaks into named parts, so a recruiter can see and challenge exactly why a candidate ranks where they do — no black box.",
       "It runs in ~17 seconds for 100K candidates on a CPU with no network — production-realistic, not a benchmark toy.",
     ])
c.showPage()

# ======================= PAGE 3 — JD UNDERSTANDING =======================
page("JD Understanding & Candidate Evaluation", 3,
     intro="Key requirements extracted from the JD, and the signals that decide fit.",
     items=[
       "*Key requirements pulled from the JD:",
       "Real production experience in embeddings/retrieval, vector search, ranking and evaluation (NDCG/MRR) — at PRODUCT companies, not pure research or services.",
       "5–9 years experience; strong Python; based in / open to Indian metros (Pune, Noida).",
       "Explicit disqualifiers: title-chasers, consulting-only careers, research-only, CV/speech-only without NLP/IR.",
       "*Signals that matter most (fit beyond keyword matching):",
       "Evidence in career descriptions — 'built a learning-to-rank model', 'RAG in production' — outweighs any skills tag.",
       "Actual job title and company type (product vs services) vs. a polished-but-fake skills list.",
       "Behavioral availability: recent login, recruiter response rate, open-to-work — a perfect-on-paper ghost is not hireable.",
       "Profile internal consistency — impossible timelines flag fakes/honeypots.",
     ])
c.showPage()

# ======================= PAGE 4 — RANKING METHODOLOGY =======================
y = page("Ranking Methodology", 4,
     intro="How candidates are retrieved, scored, and combined into a final rank.")
rows = [
  ("Role fit", "Is the actual role on the AI/ML/search bullseye?", "weight 0.40"),
  ("Evidence", "Retrieval/ranking/ML work found in career TEXT", "weight 0.32"),
  ("Experience", "5–9 year sweet spot, decaying outside", "weight 0.16"),
  ("Location", "India metro / Pune / Noida", "weight 0.12"),
  ("Disqualifiers", "services-only, job-hopping, research-only, CV-only", "− penalty"),
  ("Availability", "recent login, response rate, open-to-work", "× 0.55–1.10"),
  ("Trust / sanity", "honeypot consistency checks", "× kill-switch"),
]
ry = y - 2*mm
c.setFont("Helvetica-Bold", 10)
for name, desc, eff in rows:
    c.setFillColor(PURPLE); c.setFont("Helvetica-Bold", 10); c.drawString(M, ry, name)
    c.setFillColor(GREY); c.setFont("Helvetica", 10); c.drawString(M+38*mm, ry, desc)
    c.setFillColor(ORANGE); c.setFont("Helvetica-Bold", 9); c.drawRightString(W-M, ry, eff)
    ry -= 7.5*mm
c.setFillColor(DARK); c.setFont("Helvetica-Bold", 10.5)
c.drawString(M, ry-2*mm, "score = (0.40·role + 0.32·evidence + 0.16·exp + 0.12·loc − penalties) × availability")
c.drawString(M, ry-9*mm, "honeypots are multiplied by 0.001 → they sink below the top 100.")
c.setFillColor(GREY); c.setFont("Helvetica", 10)
c.drawString(M, ry-18*mm, "Heuristic / rule-based (no GPU, no LLM at runtime). Ties broken deterministically by candidate_id.")
c.drawString(M, ry-24*mm, "Final scores are spread into a clean [0.55, 0.99] band so the model visibly differentiates.")
c.showPage()

# ======================= PAGE 5 — EXPLAINABILITY & VALIDATION =======================
page("Explainability & Data Validation", 5,
     intro="How decisions are explained, and how we keep them honest.",
     items=[
       "*Every ranking decision is explained from real data:",
       "Each candidate gets a 1–2 sentence reason built only from fields in their profile — title, years, evidence words actually present, recruiter response rate.",
       "Honest concerns are surfaced too (e.g. '120d notice', 'based outside India') so reasoning matches the rank.",
       "*Preventing hallucination / unsupported justifications:",
       "Reasoning is generated by templating REAL field values — it cannot invent skills or employers the candidate doesn't have.",
       "Because the score itself is a transparent sum of named components, any claim is traceable to a number.",
       "*Handling inconsistent, low-quality, or suspicious profiles:",
       "A honeypot kill-switch flags internally-impossible profiles (tenure > experience, expert skill used 0 months, skill used longer than the career, claims more experience than time elapsed) and pushes them out of the top 100.",
       "QA verified: 0 honeypots and 0 keyword-stuffers in our top 100.",
     ])
c.showPage()

# ======================= PAGE 6 — END-TO-END WORKFLOW =======================
page("End-to-End Workflow", 6,
     intro="From JD input to ranked candidate output.")
bw, bh, gap = 33*mm, 16*mm, 6*mm
x0 = M; yA = H-95*mm
steps1 = [("candidates\n.jsonl (100K)", "input"), ("Extract\nevidence text", "career history"),
          ("Score 7\nsignals", "role+evidence+…"), ("Penalties +\navailability", "JD disqualifiers")]
xs=[]
x=x0
for lbl,sub in steps1:
    box(x,yA,bw,bh,lbl.replace("\n"," "),sub); xs.append(x); x+=bw+gap
for i in range(len(xs)-1):
    arrow(xs[i]+bw, yA+bh/2, xs[i+1], yA+bh/2)
# second row
yB = yA-30*mm
steps2 = [("Honeypot\nkill-switch","sink fakes"), ("Sort &\ntake top 100","rank 1..100"),
          ("Generate\nreasoning","fact-grounded"), ("Output\nCSV + XLSX","submission")]
xs2=[]; x=x0
for lbl,sub in steps2:
    box(x,yB,bw,bh,lbl.replace("\n"," "),sub, fill=colors.HexColor("#EFEAFD")); xs2.append(x); x+=bw+gap
for i in range(len(xs2)-1):
    arrow(xs2[i]+bw, yB+bh/2, xs2[i+1], yB+bh/2)
# connector from row1 end to row2 start
arrow(xs[-1]+bw/2, yA, xs2[0]+bw/2, yB+bh)
c.setFillColor(GREY); c.setFont("Helvetica", 10)
c.drawString(M, yB-12*mm, "Single command:  python rank.py --candidates ./data/candidates.jsonl --out ./submission")
c.drawString(M, yB-19*mm, "End-to-end runtime: ~17 seconds on CPU, no network.")
c.showPage()

# ======================= PAGE 7 — SYSTEM ARCHITECTURE =======================
page("System Architecture", 7,
     intro="Layered, dependency-light, reproducible.")
lw = W-2*M
layers = [
  ("INPUT LAYER", "candidates.jsonl (100K profiles)  +  Job Description requirements", colors.HexColor("#E8E4FA")),
  ("FEATURE / EVIDENCE EXTRACTION", "career-history text · titles · skills · redrob behavioral signals", colors.HexColor("#DCD3FA")),
  ("SCORING ENGINE (rule-based)", "role · evidence · experience · location · penalties · availability · honeypot", colors.HexColor("#CDBFF8")),
  ("RANKER", "deterministic sort → top 100 → fact-grounded reasoning", colors.HexColor("#BBAAF4")),
  ("OUTPUT + QA", "submission.csv / submission.xlsx   ·   qa.py validates format & traps", colors.HexColor("#EFEAFD")),
]
ly = H-58*mm; lh=18*mm; first=True
for name, sub, col in layers:
    if not first:
        arrow(M+lw/2, ly+lh+6*mm, M+lw/2, ly+lh+1.5*mm)  # connector in the gap above
    c.setFillColor(col); c.setStrokeColor(PURPLE); c.setLineWidth(1)
    c.roundRect(M, ly, lw, lh, 2*mm, fill=1, stroke=1)
    c.setFillColor(DARK); c.setFont("Helvetica-Bold", 11); c.drawString(M+5*mm, ly+lh-7*mm, name)
    c.setFillColor(GREY); c.setFont("Helvetica", 9.5); c.drawString(M+5*mm, ly+4*mm, sub)
    ly -= lh+7*mm; first=False
c.setFillColor(GREY); c.setFont("Helvetica", 9.5)
c.drawString(M, ly+2*mm, "CPU-only · no GPU · no network · pure Python + openpyxl · ~17s / 100K · <16GB RAM.")
c.showPage()

# ======================= PAGE 8 — RESULTS & PERFORMANCE =======================
y = page("Results & Performance", 8,
     intro="Evidence the ranking is high-quality and within compute limits.")
stats = [("100,000", "candidates ranked"), ("~17 s", "runtime on CPU"),
         ("0", "honeypots in top 100"), ("0", "keyword-stuffers in top 100")]
sx = M; sw=(W-2*M-3*5*mm)/4
for val, lbl in stats:
    c.setFillColor(colors.white); c.setStrokeColor(PURPLE); c.setLineWidth(1.2)
    c.roundRect(sx, y-26*mm, sw, 24*mm, 3*mm, fill=1, stroke=1)
    c.setFillColor(PURPLE); c.setFont("Helvetica-Bold", 19); c.drawCentredString(sx+sw/2, y-13*mm, val)
    c.setFillColor(GREY); c.setFont("Helvetica", 8)
    for i,ln in enumerate(simpleSplit(lbl,"Helvetica",8,sw-3*mm)):
        c.drawCentredString(sx+sw/2, y-19*mm-i*3.5*mm, ln)
    sx += sw+5*mm
yy = y-34*mm
bullets([
  "*Top-100 is 100% relevant roles: ML/AI/NLP/Search/Recommendation engineers — no distractor titles.",
  "Manual spot-checks confirm reasoning matches each real profile (no hallucination).",
  "Compute constraints met with large margin: 17s vs 5-min budget, CPU-only, zero network calls, <16GB RAM.",
  "Format validated: exactly 100 unique ranks & IDs, all IDs exist, scores non-increasing.",
], M, yy, W-2*M)
c.showPage()

# ======================= PAGE 9 — TECHNOLOGIES USED =======================
page("Technologies Used", 9,
     intro="Chosen for speed, reproducibility, and zero runtime dependencies.",
     items=[
       "*Python 3 (standard library) — JSON parsing, scoring, CSV output. No heavy ML stack needed; keeps runtime in seconds and fully reproducible.",
       "openpyxl — to also emit the XLSX output the portal requests.",
       "Pure rule-based scoring — deliberately NO LLM / GPU at runtime, so it meets the 5-min CPU, no-network constraint and scales to a 200K production pool.",
       "Git / GitHub — versioned, reproducible repo with a single reproduce command.",
       "Why this stack: the challenge rewards latency-quality tradeoffs and reproducibility. A transparent heuristic beats a black-box embedding model here — it's faster, explainable, and immune to keyword-stuffer traps.",
       "AI tools (Claude) were used for code review and drafting — declared honestly; no candidate data sent to any LLM, no LLM in the ranking path.",
     ])
c.showPage()

# ======================= PAGE 10 — SUBMISSION ASSETS =======================
page("Submission Assets", 10,
     intro="Everything needed to reproduce and verify our submission.",
     items=[
       "*GitHub repository: " + GITHUB,
       "Reproduce command:  python rank.py --candidates ./data/candidates.jsonl --out ./submission",
       "Ranked output: submission.xlsx (and submission.csv) — top 100 with reasoning.",
       "QA script: qa.py — verifies valid format and zero traps in the top 100.",
       "Sandbox / demo link: " + SANDBOX,
       "Metadata: submission_metadata.yaml (team, compute env, honest AI-tools declaration).",
     ])
c.showPage()
c.save()
print("Wrote Redrob_TrustScore_Submission.pdf")

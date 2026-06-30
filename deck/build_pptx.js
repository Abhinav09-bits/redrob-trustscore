// Redrob TrustScore — idea-submission deck (PPTX), matching the official template.
const pptxgen = require("pptxgenjs");
const p = new pptxgen();
p.layout = "LAYOUT_WIDE";            // 13.33 x 7.5
p.author = "Team Arcane009";
p.title  = "Redrob TrustScore";

// ---- palette (Redrob: deep indigo + violet, warm amber accent) ----
const INK   = "1B1535";   // near-black indigo (text + dark bg)
const VIOLET= "6D4AE0";   // primary
const LILAC = "B9A8FF";   // light accent on dark
const AMBER = "F0892B";   // sharp accent (sparingly)
const BG    = "F5F3FC";   // light content bg
const CARD  = "FFFFFF";
const MUT   = "6A6680";    // muted text
const TINT  = "EEE9FB";    // card tint

const TEAM = "Arcane009";
const GH = "github.com/Abhinav09-bits/redrob-trustscore";
const SB = "redrob-trustscore-gba7ntzmq5cwxtkp6ghgkn.streamlit.app";
const W = 13.33, H = 7.5, MX = 0.62;
const shadow = () => ({ type:"outer", color:"000000", blur:7, offset:3, angle:90, opacity:0.10 });

function footer(s, n){
  s.addText([{text:TEAM,options:{bold:true,color:VIOLET}},{text:"  ·  Redrob TrustScore",options:{color:MUT}}],
    {x:MX,y:H-0.42,w:7,h:0.3,fontSize:9,fontFace:"Calibri",align:"left",margin:0});
  s.addText(`${n} / 11`,{x:W-MX-1.2,y:H-0.42,w:1.2,h:0.3,fontSize:9,color:MUT,align:"right",fontFace:"Calibri",margin:0});
}
function head(s, kicker, title){
  s.background={color:BG};
  s.addText(kicker.toUpperCase(),{x:MX,y:0.5,w:W-2*MX,h:0.3,fontSize:12,bold:true,color:VIOLET,charSpacing:2,fontFace:"Calibri",margin:0});
  s.addText(title,{x:MX,y:0.78,w:W-2*MX,h:0.7,fontSize:30,bold:true,color:INK,fontFace:"Calibri",margin:0});
}
function card(s,x,y,w,h,fill){ s.addShape(p.shapes.ROUNDED_RECTANGLE,{x,y,w,h,rectRadius:0.07,fill:{color:fill||CARD},line:{color:"E4DEF5",width:1},shadow:shadow()}); }
function arrowR(s,x,y,w){ s.addShape(p.shapes.LINE,{x,y,w,h:0,line:{color:AMBER,width:2.25,endArrowType:"triangle"}}); }
function arrowL(s,x,y,w){ s.addShape(p.shapes.LINE,{x,y,w,h:0,line:{color:AMBER,width:2.25,beginArrowType:"triangle"}}); }
function arrowD(s,x,y,h){ s.addShape(p.shapes.LINE,{x,y,w:0,h,line:{color:AMBER,width:2.25,endArrowType:"triangle"}}); }

// ============ SLIDE 1 — TITLE ============
let s = p.addSlide(); s.background={color:INK};
s.addShape(p.shapes.OVAL,{x:10.4,y:-2.0,w:5.6,h:5.6,fill:{color:"2A2150"},line:{type:"none"}});
s.addShape(p.shapes.OVAL,{x:11.6,y:3.9,w:4.2,h:4.2,fill:{color:"241C46"},line:{type:"none"}});
s.addText("TRACK 1  ·  DATA & AI CHALLENGE",{x:MX,y:1.5,w:9,h:0.3,fontSize:13,bold:true,color:AMBER,charSpacing:2,fontFace:"Calibri",margin:0});
s.addText("Redrob TrustScore",{x:MX,y:1.95,w:11,h:1.1,fontSize:54,bold:true,color:"FFFFFF",fontFace:"Calibri",margin:0});
s.addText("A verified, evidence-based candidate ranking agent",{x:MX,y:3.05,w:11,h:0.5,fontSize:20,color:LILAC,italic:true,fontFace:"Calibri",margin:0});
// info row
const meta=[["Team",TEAM],["Team Leader","Abhinav Khatta"],["Members","Divyanshu Kapariya · Abhinav Khatta"]];
let yy=4.1;
meta.forEach(([k,v])=>{ s.addText([{text:k+"   ",options:{color:LILAC}},{text:v,options:{bold:true,color:"FFFFFF"}}],
  {x:MX,y:yy,w:11,h:0.34,fontSize:14,fontFace:"Calibri",margin:0}); yy+=0.42; });
s.addText("Rank the top 100 of 100,000 candidates for a Senior AI Engineer role — without keyword matching, dodging ~80 honeypots, on CPU in under 5 minutes.",
  {x:MX,y:5.7,w:11.4,h:0.8,fontSize:13,color:"D9D2F5",fontFace:"Calibri",margin:0});
s.addText(GH,{x:MX,y:H-0.5,w:8,h:0.3,fontSize:10,color:MUT,fontFace:"Calibri",margin:0});

// ============ SLIDE 2 — SOLUTION OVERVIEW (comparison) ============
s=p.addSlide(); head(s,"02 · Solution Overview","An autonomous, explainable ranking agent");
s.addText("For each candidate, TrustScore combines seven signals into one auditable score, then returns a ranked top-100 with a plain-language reason for each pick.",
  {x:MX,y:1.55,w:W-2*MX,h:0.5,fontSize:14,color:MUT,italic:true,fontFace:"Calibri",margin:0});
const colW=(W-2*MX-0.5)/2;
// left: traditional
card(s,MX,2.25,colW,4.1,CARD);
s.addText("Traditional matching",{x:MX+0.3,y:2.5,w:colW-0.6,h:0.4,fontSize:18,bold:true,color:"B23A48",fontFace:"Calibri",margin:0});
s.addText([
 {text:"Embeds the profile, ranks by similarity",options:{bullet:true,breakLine:true}},
 {text:"Rewards anyone who stuffs the right keywords",options:{bullet:true,breakLine:true}},
 {text:"Walks into honeypots / impossible profiles",options:{bullet:true,breakLine:true}},
 {text:"Black box — “the model thought they’re similar”",options:{bullet:true}},
],{x:MX+0.3,y:3.05,w:colW-0.6,h:3.1,fontSize:14,color:INK,fontFace:"Calibri",paraSpaceAfter:10,margin:0});
// right: trustscore
card(s,MX+colW+0.5,2.25,colW,4.1,TINT);
s.addText("Redrob TrustScore",{x:MX+colW+0.8,y:2.5,w:colW-0.6,h:0.4,fontSize:18,bold:true,color:VIOLET,fontFace:"Calibri",margin:0});
s.addText([
 {text:"Reads real career evidence — what they actually did",options:{bullet:true,breakLine:true}},
 {text:"Penalizes the JD’s stated disqualifiers",options:{bullet:true,breakLine:true}},
 {text:"Honeypot kill-switch sinks impossible profiles",options:{bullet:true,breakLine:true}},
 {text:"Weights whether the person is even reachable",options:{bullet:true,breakLine:true}},
 {text:"Every score is auditable — no black box",options:{bullet:true}},
],{x:MX+colW+0.8,y:3.05,w:colW-0.6,h:3.1,fontSize:14,color:INK,fontFace:"Calibri",paraSpaceAfter:9,margin:0});
footer(s,2);

// ============ SLIDE 3 — JD UNDERSTANDING ============
s=p.addSlide(); head(s,"03 · JD Understanding & Candidate Evaluation","What the role needs — and the signals that decide fit");
card(s,MX,1.75,colW,4.6,CARD);
s.addText("Requirements extracted from the JD",{x:MX+0.3,y:2.0,w:colW-0.6,h:0.4,fontSize:17,bold:true,color:VIOLET,fontFace:"Calibri",margin:0});
s.addText([
 {text:"Production retrieval / embeddings, vector search, ranking & evaluation (NDCG, MRR)",options:{bullet:true,breakLine:true}},
 {text:"At product companies — not pure research or services",options:{bullet:true,breakLine:true}},
 {text:"5–9 years; strong Python; Indian metros (Pune, Noida)",options:{bullet:true,breakLine:true}},
 {text:"Disqualifiers: title-chasers, consulting-only, research-only, CV/speech-only",options:{bullet:true}},
],{x:MX+0.3,y:2.55,w:colW-0.6,h:3.6,fontSize:14,color:INK,fontFace:"Calibri",paraSpaceAfter:11,margin:0});
card(s,MX+colW+0.5,1.75,colW,4.6,TINT);
s.addText("Signals that decide fit (beyond keywords)",{x:MX+colW+0.8,y:2.0,w:colW-0.6,h:0.4,fontSize:17,bold:true,color:VIOLET,fontFace:"Calibri",margin:0});
s.addText([
 {text:"Evidence in career text — “built a learning-to-rank model”, “RAG in production”",options:{bullet:true,breakLine:true}},
 {text:"Real job title + company type vs. a polished-but-fake skills list",options:{bullet:true,breakLine:true}},
 {text:"Behavioral availability: recent login, response rate, open-to-work",options:{bullet:true,breakLine:true}},
 {text:"Internal consistency — impossible timelines flag fakes",options:{bullet:true}},
],{x:MX+colW+0.8,y:2.55,w:colW-0.6,h:3.6,fontSize:14,color:INK,fontFace:"Calibri",paraSpaceAfter:11,margin:0});
footer(s,3);

// ============ SLIDE 4 — RANKING METHODOLOGY ============
s=p.addSlide(); head(s,"04 · Ranking Methodology","Seven signals combined into one TrustScore");
const sig=[
 ["Role fit","Is the actual role on the AI/ML/search bullseye?","weight 0.40"],
 ["Evidence","Retrieval / ranking / ML work found in career text","weight 0.32"],
 ["Experience","5–9 year sweet spot, decaying outside","weight 0.16"],
 ["Location","India metro / Pune / Noida","weight 0.12"],
 ["Disqualifiers","services-only, job-hopping, research-only, CV-only","− penalty"],
 ["Availability","recent login, response rate, open-to-work","× 0.55–1.10"],
 ["Trust / sanity","honeypot consistency checks","× kill-switch"],
];
let ry=1.7, rh=0.5;
sig.forEach((r,i)=>{
  if(i%2===0) s.addShape(p.shapes.RECTANGLE,{x:MX,y:ry,w:W-2*MX,h:rh,fill:{color:TINT},line:{type:"none"}});
  s.addText(r[0],{x:MX+0.2,y:ry,w:3.0,h:rh,fontSize:14,bold:true,color:VIOLET,valign:"middle",fontFace:"Calibri",margin:0});
  s.addText(r[1],{x:MX+3.3,y:ry,w:7.0,h:rh,fontSize:13,color:INK,valign:"middle",fontFace:"Calibri",margin:0});
  s.addText(r[2],{x:W-MX-2.3,y:ry,w:2.1,h:rh,fontSize:12,bold:true,color:AMBER,align:"right",valign:"middle",fontFace:"Calibri",margin:0});
  ry+=rh;
});
card(s,MX,ry+0.12,W-2*MX,1.0,INK);
s.addText([
 {text:"score = (0.40·role + 0.32·evidence + 0.16·exp + 0.12·loc − penalties) × availability",options:{breakLine:true,bold:true,color:"FFFFFF"}},
 {text:"honeypots × 0.001 → they sink below the top 100   ·   rule-based, no GPU / no LLM at runtime   ·   ties broken by candidate_id",options:{color:LILAC,fontSize:11}},
],{x:MX+0.3,y:ry+0.2,w:W-2*MX-0.6,h:0.85,fontSize:14,fontFace:"Calibri",valign:"middle",margin:0});
footer(s,4);

// ============ SLIDE 5 — EXPLAINABILITY & VALIDATION ============
s=p.addSlide(); head(s,"05 · Explainability & Data Validation","Decisions explained — and kept honest");
const c3w=(W-2*MX-1.0)/3;
const cards3=[
 ["Explained from real data","Each pick gets a 1–2 sentence reason built from the candidate’s own fields — title, years, evidence words present, response rate. Honest concerns (notice period, location) are surfaced too."],
 ["No hallucination","Reasoning is templated from REAL field values, so it cannot invent skills or employers. The score is a transparent sum of named parts — every claim traces to a number."],
 ["Suspicious / impossible profiles","A honeypot kill-switch flags impossible profiles (tenure > experience, expert skill used 0 months, skill used longer than the career) and pushes them out of the top 100."],
];
cards3.forEach(([t,b],i)=>{
  const x=MX+i*(c3w+0.5);
  card(s,x,1.9,c3w,3.4,i===2?TINT:CARD);
  s.addShape(p.shapes.OVAL,{x:x+0.3,y:2.15,w:0.5,h:0.5,fill:{color:VIOLET},line:{type:"none"}});
  s.addText(String(i+1),{x:x+0.3,y:2.15,w:0.5,h:0.5,fontSize:16,bold:true,color:"FFFFFF",align:"center",valign:"middle",fontFace:"Calibri",margin:0});
  s.addText(t,{x:x+0.3,y:2.8,w:c3w-0.6,h:0.7,fontSize:15,bold:true,color:INK,fontFace:"Calibri",margin:0});
  s.addText(b,{x:x+0.3,y:3.5,w:c3w-0.6,h:1.7,fontSize:12.5,color:MUT,fontFace:"Calibri",margin:0});
});
card(s,MX,5.55,W-2*MX,0.75,INK);
s.addText([{text:"QA verified:  ",options:{bold:true,color:AMBER}},{text:"0 honeypots and 0 keyword-stuffers in our top 100.",options:{color:"FFFFFF"}}],
  {x:MX+0.3,y:5.55,w:W-2*MX-0.6,h:0.75,fontSize:15,valign:"middle",fontFace:"Calibri",margin:0});
footer(s,5);

// ============ SLIDE 6 — END-TO-END WORKFLOW ============
s=p.addSlide(); head(s,"06 · End-to-End Workflow","From JD input to ranked output");
const steps=[
 ["candidates.jsonl","100K profiles"],["Extract evidence","career-history text"],
 ["Score 7 signals","role + evidence + …"],["Penalties + availability","JD disqualifiers"],
 ["Honeypot kill-switch","sink fakes"],["Sort & take top 100","rank 1..100"],
 ["Generate reasoning","fact-grounded"],["Output XLSX / CSV","submission"],
];
const bw=2.7,bh=1.15,gap=(W-2*MX-4*bw)/3;
const yA=2.1, yB=4.0;
function placeBox(idx,x,y,tint){
  card(s,x,y,bw,bh,tint?TINT:CARD);
  s.addText(steps[idx][0],{x:x+0.12,y:y+0.18,w:bw-0.24,h:0.5,fontSize:13.5,bold:true,color:INK,align:"center",fontFace:"Calibri",margin:0});
  s.addText(steps[idx][1],{x:x+0.12,y:y+0.66,w:bw-0.24,h:0.35,fontSize:11,color:MUT,align:"center",fontFace:"Calibri",margin:0});
}
let cols=[]; for(let i=0;i<4;i++) cols.push(MX+i*(bw+gap));
// row A: steps 0..3 left-to-right
for(let i=0;i<4;i++) placeBox(i,cols[i],yA,false);
for(let i=0;i<3;i++) arrowR(s,cols[i]+bw+0.05,yA+bh/2,gap-0.1);
// down connector at the right column into the start of row B
arrowD(s,cols[3]+bw/2,yA+bh+0.03,yB-(yA+bh)-0.06);
// row B: steps 4..7 serpentine (right-to-left), arrows point left
for(let i=0;i<4;i++) placeBox(4+(3-i),cols[i],yB,true);
for(let i=0;i<3;i++) arrowL(s,cols[i]+bw+0.05,yB+bh/2,gap-0.1);
s.addText("Single command:   python rank.py --candidates ./data/candidates.jsonl --out ./submission",
  {x:MX,y:5.5,w:W-2*MX,h:0.35,fontSize:13,bold:true,color:VIOLET,fontFace:"Consolas",margin:0});
s.addText("End-to-end runtime ~17 seconds on CPU, no network.",
  {x:MX,y:5.85,w:W-2*MX,h:0.35,fontSize:12,color:MUT,italic:true,fontFace:"Calibri",margin:0});
footer(s,6);

// ============ SLIDE 7 — SYSTEM ARCHITECTURE ============
s=p.addSlide(); head(s,"07 · System Architecture","Layered, dependency-light, reproducible");
const layers=[
 ["INPUT LAYER","candidates.jsonl (100K profiles)  +  Job Description requirements"],
 ["FEATURE / EVIDENCE EXTRACTION","career-history text · titles · skills · redrob behavioral signals"],
 ["SCORING ENGINE  (rule-based)","role · evidence · experience · location · penalties · availability · honeypot"],
 ["RANKER","deterministic sort  →  top 100  →  fact-grounded reasoning"],
 ["OUTPUT  +  QA","submission.xlsx / .csv   ·   qa.py validates format & traps"],
];
let ly=1.75; const lh=0.82, lgap=0.18;
layers.forEach((L,i)=>{
  const tint = i===2 ? VIOLET : (i%2? TINT: CARD);
  const txtc = i===2 ? "FFFFFF" : INK;
  const subc = i===2 ? LILAC : MUT;
  card(s,MX,ly,W-2*MX,lh, i===2?VIOLET:(i%2?TINT:CARD));
  s.addText(L[0],{x:MX+0.35,y:ly+0.1,w:W-2*MX-0.7,h:0.35,fontSize:14,bold:true,color:txtc,fontFace:"Calibri",margin:0});
  s.addText(L[1],{x:MX+0.35,y:ly+0.44,w:W-2*MX-0.7,h:0.3,fontSize:11.5,color:subc,fontFace:"Calibri",margin:0});
  if(i<layers.length-1) arrowD(s,W/2,ly+lh+0.01,lgap-0.02);
  ly+=lh+lgap;
});
s.addText("CPU-only · no GPU · no network · pure Python + openpyxl · ~17s / 100K · < 16 GB RAM",
  {x:MX,y:ly+0.05,w:W-2*MX,h:0.35,fontSize:12,italic:true,color:MUT,align:"center",fontFace:"Calibri",margin:0});
footer(s,7);

// ============ SLIDE 8 — RESULTS & PERFORMANCE ============
s=p.addSlide(); head(s,"08 · Results & Performance","High-quality ranking, well within compute limits");
const stats=[["100,000","candidates ranked"],["~17 s","runtime on CPU"],["0","honeypots in top 100"],["0","keyword-stuffers in top 100"]];
const sw=(W-2*MX-3*0.5)/4;
stats.forEach(([v,l],i)=>{
  const x=MX+i*(sw+0.5);
  card(s,x,1.9,sw,1.9,CARD);
  s.addText(v,{x:x+0.1,y:2.15,w:sw-0.2,h:0.8,fontSize:40,bold:true,color:VIOLET,align:"center",fontFace:"Calibri",margin:0});
  s.addText(l,{x:x+0.15,y:3.05,w:sw-0.3,h:0.6,fontSize:12,color:MUT,align:"center",fontFace:"Calibri",margin:0});
});
s.addText([
 {text:"Top-100 is 100% relevant roles — ML / AI / NLP / Search / Recommendation engineers, no distractor titles",options:{bullet:true,breakLine:true}},
 {text:"Manual spot-checks confirm every reason matches the real profile (no hallucination)",options:{bullet:true,breakLine:true}},
 {text:"Constraints met with huge margin: 17 s vs 5-min budget, CPU-only, zero network calls, < 16 GB RAM",options:{bullet:true,breakLine:true}},
 {text:"Format validated: exactly 100 unique ranks & IDs, all IDs exist, scores non-increasing",options:{bullet:true}},
],{x:MX,y:4.2,w:W-2*MX,h:2.4,fontSize:14.5,color:INK,fontFace:"Calibri",paraSpaceAfter:12,margin:0});
footer(s,8);

// ============ SLIDE 9 — TECHNOLOGIES USED ============
s=p.addSlide(); head(s,"09 · Technologies Used","Chosen for speed, reproducibility, zero runtime deps");
const tech=[
 ["Python 3 (stdlib)","JSON parsing, scoring, CSV output — runtime in seconds, fully reproducible"],
 ["openpyxl","emits the XLSX output the portal requests"],
 ["Rule-based scoring","deliberately NO LLM / GPU at runtime → meets 5-min CPU, no-network budget; scales to 200K"],
 ["Git / GitHub","versioned, reproducible repo with a single reproduce command"],
 ["Streamlit","hosted sandbox demo for live verification on a small sample"],
];
let ty=1.85; const trh=0.84;
tech.forEach(([t,d],i)=>{
  card(s,MX,ty,W-2*MX,trh, i%2?TINT:CARD);
  s.addShape(p.shapes.OVAL,{x:MX+0.25,y:ty+0.22,w:0.4,h:0.4,fill:{color:VIOLET},line:{type:"none"}});
  s.addText(t,{x:MX+0.9,y:ty+0.12,w:3.7,h:0.6,fontSize:15,bold:true,color:VIOLET,valign:"middle",fontFace:"Calibri",margin:0});
  s.addText(d,{x:MX+4.7,y:ty+0.12,w:W-2*MX-5.0,h:0.6,fontSize:13,color:INK,valign:"middle",fontFace:"Calibri",margin:0});
  ty+=trh+0.12;
});
s.addText("AI tools (Claude) used for code review & drafting — declared honestly; no candidate data sent to any LLM, no LLM in the ranking path.",
  {x:MX,y:ty+0.02,w:W-2*MX,h:0.4,fontSize:11.5,italic:true,color:MUT,fontFace:"Calibri",margin:0});
footer(s,9);

// ============ SLIDE 10 — SUBMISSION ASSETS ============
s=p.addSlide(); head(s,"10 · Submission Assets","Everything to reproduce and verify");
const assets=[
 ["GitHub repository",GH],
 ["Live sandbox demo",SB],
 ["Reproduce command","python rank.py --candidates ./data/candidates.jsonl --out ./submission"],
 ["Ranked output","submission.xlsx (+ submission.csv) — top 100 with reasoning"],
 ["QA script","qa.py — verifies valid format and zero traps in the top 100"],
 ["Metadata","submission_metadata.yaml — team, compute env, honest AI-tools declaration"],
];
const aw=(W-2*MX-0.5)/2;
assets.forEach(([t,d],i)=>{
  const x=MX+(i%2)*(aw+0.5), y=1.9+Math.floor(i/2)*1.45;
  card(s,x,y,aw,1.25,CARD);
  s.addText(t,{x:x+0.3,y:y+0.18,w:aw-0.6,h:0.4,fontSize:15,bold:true,color:VIOLET,fontFace:"Calibri",margin:0});
  s.addText(d,{x:x+0.3,y:y+0.6,w:aw-0.6,h:0.55,fontSize:12,color:INK,fontFace:"Calibri",margin:0});
});
footer(s,10);

// ============ SLIDE 11 — CLOSING ============
s=p.addSlide(); s.background={color:INK};
s.addShape(p.shapes.OVAL,{x:-1.8,y:4.0,w:5.2,h:5.2,fill:{color:"241C46"},line:{type:"none"}});
s.addShape(p.shapes.OVAL,{x:10.8,y:-1.8,w:4.6,h:4.6,fill:{color:"2A2150"},line:{type:"none"}});
s.addText("Thank you",{x:MX,y:2.4,w:11,h:1.0,fontSize:46,bold:true,color:"FFFFFF",fontFace:"Calibri",margin:0});
s.addText("Redrob TrustScore — judging candidates on verified evidence, explainably.",
  {x:MX,y:3.5,w:11.5,h:0.5,fontSize:18,color:LILAC,italic:true,fontFace:"Calibri",margin:0});
s.addText([{text:"Team Arcane009",options:{bold:true,color:"FFFFFF",breakLine:true}},
 {text:GH,options:{color:LILAC,fontSize:13,breakLine:true}},
 {text:SB,options:{color:LILAC,fontSize:13}}],
 {x:MX,y:4.4,w:11,h:1.2,fontSize:16,fontFace:"Calibri",margin:0,paraSpaceAfter:4});

p.writeFile({fileName:"Redrob_TrustScore_Submission.pptx"}).then(f=>console.log("wrote",f));

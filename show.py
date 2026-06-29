"""Look up one candidate's real profile to verify the reasoning isn't made up.
Usage:  python show.py CAND_0064326
"""
import json, sys

cid = sys.argv[1] if len(sys.argv) > 1 else "CAND_0064326"
with open("data/candidates.jsonl", encoding="utf-8") as f:
    for line in f:
        if cid in line:
            c = json.loads(line)
            if c["candidate_id"] == cid:
                break
    else:
        print("not found"); sys.exit()

p = c["profile"]; s = c["redrob_signals"]
print(f"=== {cid} ===")
print(f"Title   : {p['current_title']}  ({p['years_of_experience']} yrs)")
print(f"Location: {p['location']}, {p['country']}")
print(f"Headline: {p['headline']}")
print(f"\nSummary : {p['summary']}\n")
print("Career history:")
for r in c["career_history"]:
    print(f"  - {r['title']} @ {r['company']} ({r['start_date']}..{r['end_date']}, {r['duration_months']}mo)")
    print(f"      {r['description'][:240]}...")
print("\nKey signals:")
print(f"  recruiter_response_rate : {s['recruiter_response_rate']}")
print(f"  last_active_date        : {s['last_active_date']}")
print(f"  open_to_work_flag       : {s['open_to_work_flag']}")
print(f"  notice_period_days      : {s['notice_period_days']}")
print(f"  interview_completion    : {s['interview_completion_rate']}")

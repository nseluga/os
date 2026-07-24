---
name: Pitcher Injury Risk
status: on-hold
priority: medium
last_active: 2026-06-27
next_step: "Refine the GitHub repo using baseball-research tooling to make it more presentable for viewers"
repo: ~/Pitcher-Injury-Risk
github: https://github.com/nseluga/Pitcher-Injury-Risk
summary: "MLB pitcher health modeling platform — injury probability, severity, time-to-injury, and composite Injury Risk+ score."
tags: [ml, baseball]
---

## Where it stands

On hold. Models pitcher injury probability, severity, and time-to-injury (survival models) into a composite Injury Risk+ score, with a Streamlit dashboard. Honest finding: AUC ~0.57 — a genuine information ceiling, framed as a domain result. Notebooks, models, and reports are committed; last run 2026-06-27. Next work is presentation polish, not new modeling.

## Run / verify

    cd ~/Pitcher-Injury-Risk && ./run_project.sh    # autonomous notebook loop (fix → critique → improve → dashboard)
    # env: requirements.txt / environment.yml

## Key files

- **claude_instructions.md** — project conventions.
- **audit.md** (in this os folder) — prior code audit.
- `src/`, `notebooks/`, `models/`, `reports/`, `dashboard/` in the repo.

Related: [[projects/batting-average-ability/README|batting-average-ability]] · [[projects/hitter-embedding/README|hitter-embedding]]

---
name: review-infra-config
description: Agent review of infrastructure/config code catches critical blockers that fail at runtime
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4f4de8d8-3f48-4411-a6e2-1511de5d2898
---

**Rule:** Have a fresh agent adversarially review infrastructure-as-code and deploy scripts before real deployment, even if the code looks complete.

**Why:** The BCNS infra grilling session produced bootstrap.sh, deploy workflows, systemd unit, and backup scripts that looked solid to inline review. An independent agent audit caught 2 blockers (no reverse proxy/TLS termination = nothing listens on 443; pg_dump v16 client refuses Supabase Postgres 17) and 5+ NITs (Cloudflare IP fetch failure silently swallowed, release pruning deletes the running app after rollback, sshd config overrideable by cloud-init, sudoers files unvalidated, etc.). All would have failed on first droplet provision. The 10-minute review cost was tiny vs weeks debugging those issues in production.

**How to apply:** When writing ops/infrastructure scripts, treat a review pass as mandatory before real deployment — especially when the first run is unrehearsable (real droplet, prod database). Use an Explore or general-purpose agent to find path mismatches, cross-file inconsistencies, race conditions, and failure modes that inline review misses. The review is most valuable on configs that interact with the real system (bash scripts, CI workflows, systemd units, nginx vhosts) because typos and logic errors don't surface until they run.

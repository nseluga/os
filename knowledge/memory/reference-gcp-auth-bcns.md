---
name: reference-gcp-auth-bcns
description: GCP under bcn-services.com blocks service-account keys and Sheets/Drive ADC scopes — use impersonation; Places API (New) takes OAuth so needs no API key
metadata: 
  node_type: memory
  type: reference
  originSessionId: 08984a96-e34c-4893-98db-d5ac18570eb4
  modified: 2026-07-30T16:05:17.752Z
---

Two Google defaults block the obvious auth paths on the `bcn-services.com` org,
and neither error message names the fix.

**Service account keys are blocked.** `iam.managed.disableServiceAccountKeyCreation`
is enforced org-wide by Secure by Default. Overriding it needs
`roles/orgpolicy.policyAdmin` at the *org* (Project Owner is not enough — the
console greys out "Manage policy").

**gcloud's default OAuth client cannot request Sheets/Drive scopes.**
`gcloud auth application-default login --scopes=...spreadsheets,...drive` fails
with "This app is blocked". Plain `application-default login` works fine.

**The way through is service account impersonation** — no key file exists at all:

```sh
gcloud auth application-default login          # no --scopes
gcloud auth application-default set-quota-project <project>
gcloud services enable iamcredentials.googleapis.com --project=<project>
gcloud iam service-accounts add-iam-policy-binding <sa>@<project>.iam.gserviceaccount.com \
  --member="user:<you>@bcn-services.com" --role="roles/iam.serviceAccountTokenCreator"
```

Then in Python, `impersonated_credentials.Credentials(...)` with the Sheets/Drive
scopes as `target_scopes` — the blocked scopes are legal on the *impersonated*
token, just not on gcloud's shared client. IAM bindings take 1–2 min to
propagate; a 403 on `iam.serviceAccounts.getAccessToken` right after granting is
expected, so retry before debugging.

Sharing the sheet with the service account's email is separate from all GCP
permissions and is the most common failure: correct credentials still 403.

**Places API (New) accepts OAuth bearer tokens**, so it needs no API key —
skip the key, the restrictions, and the rotation entirely.

If gcloud CLI itself has no active account (only ADC), `export
CLOUDSDK_AUTH_ACCESS_TOKEN=$(gcloud auth application-default print-access-token)`
makes `gcloud` commands work without a second login.

**Related:** [[reference-bcns-ci-setup]], [[feedback-hosting-work-profile-only]]

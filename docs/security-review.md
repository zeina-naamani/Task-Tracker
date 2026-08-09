# Module 5 Security Review

## 1. Security review summary

This document records a read-only security review of the Task Tracker repository. Codex performed the initial source audit, after which the project author manually reviewed selected findings and performed runtime checks where noted.

Findings were graded as **Valid**, **Noise**, or **False Positive**. The review also reconciled the original AI findings with eight observations independently identified by the author during the subsequent manual review.

No application fixes were made as part of this review.

## 2. Final security findings

| ID | Final classification | Severity | Evidence | Rationale | Recommended action |
|---|---|---|---|---|---|
| SEC-01 | Valid | Medium | `app/models.py:57-65`; `app/main.py:260-274`; `app/storage.py:139-145`; manual Swagger test | Explicit JSON `"status": null` was runtime-confirmed to return HTTP 500. `TaskUpdate.status` accepts `None`, transition validation is skipped for `None`, and explicitly supplied update fields reach storage before response validation. Persistent stored corruption is statically supported but was not runtime-confirmed with a follow-up GET or list request. | Reject explicit null for update fields that cannot validly be null, and add regression tests confirming that invalid requests return 422 without mutating stored data. |
| SEC-02 | Valid | Low in the current trusted/local course context; potentially Medium if remotely exposed | `app/models.py:29-37`; `app/main.py:70-117`; `app/storage.py:7,60-97`; `frontend/index.html:413-477`; manual browser/API testing | Description, assignee, search length, task count, and list/search work have no visible server-side bounds. Manual testing confirmed that long Description, Assignee, and Search values are accepted. Denial of service or resource exhaustion was not reproduced; the finding is an availability/resource risk. | Define reasonable server-side text limits. Consider pagination, request-size controls, and other resource limits only if scale or remote exposure enters project scope. |
| SEC-03 | Valid / documented course-scope limitation | N/A | `README.md:157-161`; `AGENTS.md:79-83`; `docs/midcourse/mini-adr.md:83-91`; `app/main.py:65-314` | The API factually has no authentication or user-level authorization. Repository documentation explicitly excludes authentication and authorization from the accepted course scope, so their absence is not an in-scope implementation defect. Under the instructor's grading definition, the limitation is nevertheless Valid because it would become security-relevant outside the learning/local context. | Do not add authentication or authorization to this course project. Reassess the requirement only if the application becomes public, production-hosted, sensitive, multi-user, or ownership-aware. |
| SEC-04 | Valid | Low | `app/main.py:29-35`; `frontend/index.html:494`; `README.md:65,161`; local configuration review | `allow_origins=["*"]` and `allow_headers=["*"]` permit arbitrary browser origins to attempt interaction with the local API while it is running. `allow_credentials=False` reduces risk but does not eliminate it because the API is unauthenticated. The hardcoded `http://localhost:8000` URL is an intentional local-development assumption, not a current defect. Unrelated-origin access was not independently demonstrated at runtime. | If a minimal hardening change is approved, restrict CORS to explicitly required local frontend origins. Use environment-specific HTTPS origins only if remote deployment enters scope. |
| SEC-05 | Noise | N/A | `requirements.txt`; `Dockerfile:6-25`; `.github/workflows/ci.yml:11-27`; `README.md:123,161` | Missing dependency hashes, immutable action/image references, and dependency scanning are technically valid supply-chain and build-hardening observations. They are outside the current local course scope, and no vulnerable dependency, compromised action, or exploited supply-chain path was confirmed. | No current change. Reassess dependency scanning and immutable build provenance if production or deployment requirements are introduced. |

## 3. AI versus manual reconciliation

For this review:

- **Agreement** means Codex identified a finding and the author subsequently confirmed the same finding through manual/runtime review or testing.
- **AI-only** means Codex identified a finding, but the security behavior was not fully confirmed through manual/runtime testing.
- **You-only** means the author independently identified an observation during the manual review that followed the initial Codex SEC-01 through SEC-05 audit.

Under these operational definitions, Agreement represents later confirmation, not independent discovery before exposure to the AI result.

### Reconciliation summary

- **Agreement: 2**
  - SEC-01
  - SEC-02
- **AI-only valid findings: 2**
  - SEC-03
  - SEC-04
- **Noise from the AI audit: 1**
  - SEC-05
- **You-only observations: 8**
  - One documentation/verification defect: Observation 5A
  - Seven design/business-rule suggestions

SEC-01 and SEC-02 were originally discovered by Codex and subsequently confirmed through manual/runtime testing. They are classified as Agreement under this document's operational definition, while their original discovery source remains Codex.

SEC-03 and SEC-04 remain AI-only Valid findings. SEC-03 was verified as a documented scope limitation rather than through runtime demonstration of an authentication exploit. SEC-04's local configuration was confirmed, but unrelated-origin browser access was not independently demonstrated.

## 4. Manual review observations

These observations originated independently from the author's manual review after the initial Codex security audit. Except for Observation 5A, they are design or business-rule proposals and are not security vulnerabilities in the current requirements.

### M-01 — Completed Late

**Classification:** New historical business/audit concept derived from the existing overdue logic.

The current implementation intentionally treats a task as overdue only while its due date is past and its status is not `Done` (`app/storage.py:10-13`; `docs/midcourse/user-stories.md:35-44`). The existing calculation is not defective.

A future Completed Late concept would require completion timing and history semantics. Because `Done -> InProgress` is intentionally allowed, a reliable implementation would need to define first versus latest completion and preserve the due date that applied at completion.

This observation is useful for completion-history and accountability analysis. It is You-only because the manual review examined historical meaning after completion, while the initial AI audit focused on current security behavior.

### M-02 — Require assignee before progression

**Classification:** New business/accountability rule; not an existing defect.

Assignee is intentionally nullable (`app/models.py:36,64`), and status-transition validation checks only status pairs (`app/business_rules.py:5-38`). No accepted requirement requires assignment before progression.

The proposed rule would improve ownership accountability but is outside the current transition requirements. It is You-only because the manual review evaluated workflow responsibility rather than an AI-identified security failure.

### M-03 — Controlled assignee values

**Classification:** New data-integrity/accountability design suggestion.

Assignee is currently free text in both the model and frontend (`app/models.py:36`; `frontend/index.html:476-477`). A predefined local list could improve consistency, but authentication, accounts, roles, and member management remain outside scope.

This matters if assignee-based reporting or accountability is later required. It is You-only because the manual review identified semantic consistency concerns distinct from SEC-02's input-length risk.

### M-04 — Restrict title editing after progression

**Classification:** New business/data-integrity/audit rule; not an existing defect.

`TaskUpdate` permits title changes, and storage applies valid partial updates without status-dependent title restrictions (`app/models.py:57-65`; `app/storage.py:117-145`). No accepted requirement prohibits renaming after work starts.

The suggestion would preserve the identity of work after progression but introduces a new policy. It is You-only because the manual review considered historical and audit meaning not covered by the initial AI security findings.

### M-05 — Frontend Delete verification mismatch

**Classification:** Documentation/verification error.

Git history established that:

- Backend DELETE was present in commit `56c9cb8`.
- No committed version of `frontend/index.html` contained a Delete control, DELETE request, `deleteTask` function, or equivalent implementation.
- Commit `d9cd4f6` introduced the unsupported claim that “Delete Task” was manually browser-verified.
- No later commit removed frontend Delete functionality because it never existed in committed frontend history.

The history is consistent with deletion being performed through Swagger/API using the task ID. This is not a frontend regression and is not supported as a missing required frontend implementation.

This matters to evidence integrity rather than application security. It is You-only because the manual review identified the browser-verification mismatch independently; later Git analysis confirmed it.

### M-06 — Abort/Cancel

**Classification:** New business/audit design suggestion.

Replacing permanent deletion of progressed tasks with Abort or Cancel would require new task-state and history semantics. It is not an existing requirement or defect.

Current DELETE behavior permanently removes a task regardless of status. Abort/Cancel would preserve lifecycle meaning but requires new state semantics, so it remains a You-only manual workflow and audit suggestion.

### M-07 — Mandatory reason or note

**Classification:** New audit/accountability/UI suggestion.

Requiring a reason and confirmation for Delete or Abort would require new request, model, storage, and frontend behavior. No existing requirement mandates it.

The suggestion is useful where destructive or lifecycle-ending actions require explanation, but the project has no audit-history requirement. It is You-only because the manual review considered human accountability around those actions.

### M-08 — Earliest accepted due-date boundary

**Classification:** New validation/business-rule suggestion.

The current model accepts syntactically valid dates without a lower boundary (`app/models.py:37,65`). Existing tests intentionally support already-overdue tasks (`tests/test_tasks.py:84-108`).

A future rule could define a sensible or configurable historical lower boundary, but it should preserve legitimate past and overdue dates rather than requiring every due date to be today or later.

This could reduce accidental data-entry errors, but the correct boundary requires a product decision about historical records. It is You-only because the manual review assessed semantic date plausibility beyond the initial AI validation findings.

## 5. Categories with no issue found

- **Enum validation:** Status and priority use explicit enums, and invalid query or body values are tested.
- **Extra-field rejection:** `TaskCreate` and `TaskUpdate` use `extra="forbid"`.
- **Frontend output escaping:** Task values inserted through `innerHTML` pass through `escapeHtml()` (`frontend/index.html:561-567,637-644`).
- **Backend traceback exposure:** No explicit debug configuration or traceback serialization was visible.
- **Broad backend exception suppression:** No broad backend exception handler was found.
- **Repository secrets:** No exposed secret was found in inspected configuration. `.env` matched `.env.example`, contained only local configuration entries, and is excluded by `.gitignore` and `.dockerignore`.
- **Container privilege:** The Docker runtime creates and uses a non-root `app` user (`Dockerfile:27-34`).

## 6. Audit assumptions and limits

### Files inspected

- `AGENTS.md`
- `README.md`
- `app/main.py`
- `app/models.py`
- `app/storage.py`
- `app/business_rules.py`
- `tests/conftest.py`
- `tests/test_tasks.py`
- `tests/verify_a.py`
- `frontend/index.html`
- `requirements.txt`
- `pytest.ini`
- `Dockerfile`
- `.dockerignore`
- `.gitignore`
- `.github/workflows/ci.yml`
- `.env` and `.env.example` through redacted metadata
- Relevant files under `docs/midcourse/` and `docs/decisions/`
- Git history for the frontend Delete verification investigation

### Limits

- The audit was static and read-only except for manual runtime checks already performed for SEC-01 and SEC-02 and the local configuration review related to SEC-04.
- No penetration test was performed.
- No current CVE or dependency-advisory scan was performed.
- No production infrastructure review was performed.
- Reverse proxy behavior, firewall rules, TLS termination, hosting configuration, production secrets, and external secret management were not visible.
- No compose file or `pyproject.toml` was present.
- SEC-01's HTTP 500 response is runtime-confirmed. Persistent stored corruption is supported by the static update sequence but was not runtime-confirmed through a follow-up GET or list request.

## 7. Top-3 security backlog

| Priority | Finding | Why it matters | Evidence | Recommended action | Current-scope handling |
|---:|---|---|---|---|---|
| 1 | SEC-01 — Explicit null PATCH causes HTTP 500 | Runtime-confirmed HTTP 500 on a reachable PATCH request; the potential stored-state impact was not runtime-confirmed. | Runtime-confirmed HTTP 500; `app/models.py:57-65`; `app/main.py:260-274`; `app/storage.py:139-145` | Reject explicit null for update fields that cannot validly be null. Add regression tests proving invalid updates return 422 and do not mutate storage. | Highest-priority candidate for one specifically approved minimal `app/` fix. No fix is included in this review. |
| 2 | SEC-02 — Unbounded text and collection/search behavior | Long values are accepted while storage, listing, and search have no visible resource bounds. Impact could grow if remotely exposed. | Manual acceptance tests; `app/models.py:29-37`; `app/storage.py:7,60-97`; `frontend/index.html:413-477` | Define reasonable server-side text limits. Consider pagination or request/resource controls only if scale enters scope. | Document the lower trusted-local risk and avoid expanding this into database or deployment work. |
| 3 | SEC-04 — Wildcard CORS | Arbitrary browser origins can attempt interaction with the unauthenticated local API while it is running. | `app/main.py:29-35`; documented frontend origin in `README.md:65` | Restrict origins to explicitly required local frontend origins if a minimal hardening change is approved. | Low priority. The localhost HTTP URL itself remains an accepted local-development assumption. |

SEC-03 is Valid under the instructor's definition because the documented absence of authentication and authorization would matter outside the learning context. It remains outside this actionable Top-3 because it is not an in-scope implementation defect, repository guidance explicitly prohibits adding authentication, and no current remediation should be performed.

## 8. Smallest next actions

| Finding | Smallest next action | Action type | Why this is sufficient now |
|---|---|---|---|
| SEC-01 | In a separately approved task, reject explicit null for `TaskUpdate.status` and add one focused regression test expecting 422 without mutation. | Optional minimal fix | Directly addresses the runtime-confirmed HTTP 500 without restructuring PATCH or storage. |
| SEC-02 | Record a backlog item to decide reasonable maximum lengths for Description, Assignee, and Search. | Backlog | The risk is valid, but denial of service was not reproduced and exact limits require a product decision. |
| SEC-03 | Keep a concise note that authentication is intentionally excluded and must be reassessed before public, production, or multi-user use. | Documentation note | Captures the Valid scope limitation without introducing an out-of-scope feature. |
| SEC-04 | In a separately approved task, replace wildcard origins with the explicitly required local frontend origin or origins. | Optional minimal fix | Addresses only the wildcard-CORS issue while preserving the accepted local-development setup. |

## 9. Final counts

- **Valid security findings:** 4
- **Noise findings:** 1
- **False Positives:** 0
- **Agreement findings:** 2
- **AI-only valid findings:** 2
- **You-only documentation/evidence findings:** 1
- **You-only design/business-rule suggestions:** 7

SEC-01, SEC-02, SEC-03, and SEC-04 are Valid under the instructor's grading definition. The actionable Top-3 remains SEC-01, SEC-02, and SEC-04 because SEC-03 is a documented course-scope limitation with no permitted current remediation. SEC-05 remains Noise. Observation 5A is a documentation/evidence defect, while the other seven You-only observations remain separate design or business-rule suggestions and should not be presented as security vulnerabilities.

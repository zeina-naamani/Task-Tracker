# Final AI Review and Ownership Evidence

## AGENTS.md guardrails

`AGENTS.md` documents the repository-specific Python/FastAPI/Pydantic stack, the `uvicorn` run command, and the `pytest -v` test command. Its Module 5 guidance requires read-only inspection first, docs-first work, one bounded task per thread, and explicit approval before a specific minimal change to `app/`; it also prohibits unrelated changes. The project guardrails exclude authentication, databases, deployment work, and major UI changes without approval, thereby protecting both the backend scope and `frontend/`. Its security and governance rules require repository evidence, preservation of existing changes and behavior, relevant verification after changes, exact failure reporting, protection of sensitive values, and no staging, committing, or pushing without approval.

## AI code review mini-log

The review target was the uncommitted CR-1 diff in `app/models.py` and `tests/test_tasks.py`.

| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
| ---------- | ----------------------------- | ------ | ------------------------ |
| CR1-R1: The description-null persistence test started with `description == ""`, so its GET assertion could not prove that PATCH changed and persisted the value. | Useful | Starting and ending with the same value could let an implementation that ignored the update pass. | Corrected the test to start with `"Original description"`, PATCH `{"description": null}`, and require `""` in both the PATCH response and subsequent GET. The focused test passed (`1 passed in 0.12s`), and the full suite passed (`49 passed in 0.49s`). |
| CR1-R2: The description validator correctly normalizes explicit null to `""` while preserving omitted-field PATCH behavior. | Useful | It verified that descriptions remain non-null strings and that omission does not become an update. | Accepted as-is; no additional change was required. |
| CR1-R3: The shared status/priority validator rejects explicit null at the request boundary while preserving enum and status-transition behavior. | Useful | It confirmed that the correction is minimal and does not interfere with the established business rules. | Accepted as-is; no additional change was required. |

### CR-1 bug-fix justification

CR-1 was a small correctness and data-integrity defect reproduced during the Final AI review. The Final Project permits a small, justified bug or security correction in `app/`, so the production change was limited to request validation and normalization in `TaskUpdate`: description null is normalized to `""`, while status and priority null are rejected. Regression tests in `tests/test_tasks.py` verify all intended field semantics, including intentionally nullable assignee and due date. No product feature was added, and `frontend/` was not changed.

## AI security mini-review

| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
| ------- | ------------- | ------------------------------------- | ------ | ----------- |
| SR-3: PATCH explicit-null handling previously allowed invalid `None` values for non-null task fields to reach storage and later fail response validation. | `app/models.py`; `app/storage.py`; focused regressions in `tests/test_tasks.py` | Valid | This was reproduced as a real data-integrity/correctness defect, not merely suggested hardening. | Fixed minimally at the request-model boundary and protected by regression tests. Current full suite: `49 passed`. |
| SR-1: Wildcard CORS allows unrelated browser origins to interact with the reachable unauthenticated API. | `app/main.py` | Valid | A bounded preflight returned status 200, `Access-Control-Allow-Origin: *`, methods `GET, POST, PATCH, DELETE, OPTIONS`, and no credentials header. This is a real but low-risk local exposure; the app is an intentionally local learning project and credentials are disabled. | Document and accept for the current scope. Do not add authentication, which is explicitly out of scope. |
| SR-6: Docker base images and GitHub Actions use mutable tags rather than immutable digests or commit SHAs. | `Dockerfile`; `.github/workflows/ci.yml` | Noise | Immutable references are legitimate production supply-chain hardening, but no compromised component or production delivery path exists here. Applying the recommendation would be disproportionate to this course scope. | No change. |

## Manual security check

I manually checked the corrected behavior through the running FastAPI Swagger UI using synthetic task data:

- PATCH `{"description": null}` returned HTTP 200, changed the response description to `""`, and left the other task fields unchanged.
- PATCH `{"status": null}` returned HTTP 422 with a validation message that the field must not be null. A subsequent GET returned HTTP 200 with `"status": "ToDo"`, confirming no mutation.
- PATCH `{"priority": null}` returned HTTP 422 with the same null-validation meaning. A subsequent GET returned HTTP 200 with the previous `"priority": "Medium"`, confirming no mutation.

This human-performed check independently verified the corrected data-integrity boundary through the public API rather than relying only on AI review comments or automated tests.

## One AI output I rejected or corrected

The original AI review grouped `description: null`, `status: null`, and `priority: null` together as values that should be rejected. I did not accept that recommendation blindly and requested repository-grounded verification because description is intentionally optional/empty in this Task Tracker. Inspection established that empty descriptions are represented as `""`, the frontend clears description with `""`, stored and returned descriptions remain strings, assignee and due date are genuinely nullable, and status and priority must remain non-null.

I therefore made the final semantic decision: description null normalizes to `""`; status, priority, and title null return 422; assignee null is accepted; and due-date null clears the date. Correcting the AI's initial recommendation before implementation is evidence of human review and ownership.

## Three AI usage rules

1. **Never paste:** I will not paste credentials, tokens, `.env` values, real personal or customer data, production-sensitive logs, or other secrets into an AI tool.
2. **Always verify:** I will inspect the actual repository and diff, run relevant tests or commands, and check AI claims against current code or runtime behavior before accepting them.
3. **Record AI contributions by:** I will note significant prompts and reviews, grade findings instead of accepting them automatically, and record corrections or rejections together with the evidence behind my final decision.

## Ownership statement

I reviewed the relevant diffs and repository evidence and made the final decision about PATCH null semantics instead of blindly accepting the AI's first recommendation. I verified the completed behavior through automated tests and a separate manual Swagger check. I understand the CR-1 changes, why the request-model boundary was corrected, and how the regression tests protect the intended behavior. I am comfortable submitting this repository as my own work.

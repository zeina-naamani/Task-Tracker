# Verified Interaction Note — Module 4

**Source reviewed by AI:** `app/main.py`, `app/models.py` (via Claude Code, prompted with read-only, cite-or-flag constraints)
**Claims manually verified by author:** #6 and #10, by directly reading `app/business_rules.py`

| # | Claim (as flagged by AI) | Manual verification | Result |
|---|---|---|---|
| 6 | `update_task()` calls `validate_status_transition(existing.status, payload.status)`; AI could not confirm the resulting status code/exception behavior without reading `business_rules.py`. | Read `app/business_rules.py::validate_status_transition` (lines 12–39). | **Confirmed.** On an invalid transition, it raises `HTTPException(status_code=422, detail=...)`, with the detail message listing allowed transitions (e.g. `"Invalid status transition from ToDo to Done. Allowed transitions: [...]"`). A same-status call (`current == new`) returns silently (no-op, no exception). |
| 10 | The specific allowed/disallowed status transitions were not visible in `main.py`/`models.py` alone. | Read `VALID_TRANSITIONS` in `app/business_rules.py` (lines 5–9). | **Confirmed.** Allowed transitions are exactly: `ToDo → InProgress`, `InProgress → Done`, `Done → InProgress`. Any other transition (e.g. `ToDo → Done`) is rejected with 422. |

**Why this matters:** the AI correctly declined to guess at the transition rules or error status code from `main.py` alone (since `validate_status_transition` is only imported there, not defined) and flagged both as `[VERIFY]` instead of asserting them. Manual verification against `business_rules.py` confirmed the AI's caution was warranted — the rule set and status code were accurate but not derivable from the files it was restricted to, so the flags were an appropriate use of `[VERIFY]` rather than an unnecessary hedge.

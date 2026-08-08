# Technical Decision Note — Documentation Verification Approach

**Project:** Task Tracker (Module 4)
**Branch:** `module-4`
**Status:** Final
**Date:** 2026-08-08

---

## 1. Context

As part of the current project work, we added Google-style docstrings to the route handlers and public functions, a multi-stage `Dockerfile` and `.dockerignore`, a GitHub Actions CI workflow, a rewritten `README.md`, and a `CLAUDE.md` project-guidance file — a substantial amount of new documentation surface area added in a short period.

AI assistance was used to generate the docstrings, the README, and two rounds of review against that documentation: a focused AI-assisted review of the branch diff against `main` (referred to here as the review), followed by a triage of the review's comments into Useful, Noise, Wrong, or Needs manual check when evidence was insufficient (referred to here as the triage). Generated documentation and generated review comments share the same risk: both are claims about the code, and both can be wrong without looking wrong. Two concrete instances of this surfaced on this branch:

- A **docstring audit** (comparing every changed docstring against the actual function bodies) found that four route docstrings' example `Response` bodies showed `created_at`/`updated_at` timestamps ending in `+00:00`, while live `TaskResponse` JSON actually ends in `Z` (Pydantic v2's default UTC serialization). `/health`'s own docstring example was correct as-is — it's a plain `dict` built with `datetime.now(timezone.utc).isoformat()`, a different code path from the Pydantic-serialized `TaskResponse` routes. After verifying the actual runtime responses, the four affected docstring examples were corrected to match the observed UTC serialization, for example from `2026-08-05T12:00:00+00:00` to `2026-08-05T12:00:00Z`. The `/health` example remained unchanged because its `+00:00` format was already correct.
- The review of the branch diff against `main` produced three findings. One — `CLAUDE.md` claiming `pytest`/`httpx` were "not pinned anywhere in the repo" when `requirements.txt` already pinned both — was verified against `requirements.txt` and against the specific commit where the claim first became false, confirmed as a real, currently-false claim, and fixed. The other two — CI not building/testing the `Dockerfile`, and an apparent tension between `CLAUDE.md`'s "Do not add deployment steps" rule and the presence of Docker/CI — were checked against `.github/workflows/ci.yml`, the `Dockerfile`, and `README.md`, and classified as **Noise**: both were technically valid observations, but neither identified a defect requiring action within the project's current scope, and acting on them would have introduced unnecessary changes beyond what this work required.

CLAUDE.md's own stated boundaries are unchanged by any of this work: no authentication, no database, no deployment steps, no production hardening. The Dockerfile builds a local/manual container (non-root user, `HEALTHCHECK` against `/health`, no `--reload`) and is not wired to any registry push, hosting target, or deployment pipeline. The CI workflow runs `pytest -v` only — checkout, Python 3.11 setup, `pip install -r requirements.txt`, then tests — with no Docker build step and no deploy step of any kind. A fresh `docker build` + `docker run`, using the exact commands documented in `README.md`, confirmed the container reports `(healthy)` and `GET /health` returns `200`; only the container created for this check was stopped/removed, and no other containers or processes were touched.

## 2. Decision

**Documentation claims about this codebase — whether AI-generated or human-written — are only trusted after being checked against one of four evidence tiers, and the tier used is recorded alongside the claim:**

1. **Code inspection** — reading the actual implementation and validation rules in files such as `app/business_rules.py` and `app/models.py`, in order to verify behavior from the implementation rather than infer it from documentation.
2. **Automated test evidence** — using the existing `pytest -v` suite to confirm claims such as HTTP status codes (`201`, `204`, `422`, `404`) and application behavior through actual test assertions, rather than assuming the expected behavior without checking the tests.
3. **OpenAPI/Swagger evidence** — using the generated OpenAPI schema or Swagger UI to verify the API's generated response structure, required and optional fields, and serialized output as they are actually exposed through the API.
4. **Live runtime verification** — running the application or container and making real requests when static evidence is insufficient or runtime behavior needs confirmation. For example, a fresh Docker build and run confirmed that the container reached a `healthy` state and that `GET /health` returned HTTP `200`.

No AI-produced documentation edit or AI-produced review finding is applied to a project file automatically. Each of the three AI-assisted code review findings was independently checked against repository evidence before deciding whether to fix it or leave it unchanged. Findings are not treated as correct by default just because an AI produced them, and they are not treated as requiring action just because they are technically true.

## 3. Alternatives Considered

- **Trust AI-generated docstrings/README content without verification.** Rejected: this is exactly what produced the `+00:00`/`Z` mismatch — the AI's own example JSON was self-consistent and plausible-looking, but wrong, and would not have been caught without comparing it to actual serialized output.
- **Verify documentation once at generation time, then treat it as permanently correct.** Rejected: the `CLAUDE.md` pytest/httpx claim was accurate when first written, and became false only after a later, unrelated commit pinned those packages in `requirements.txt`. Documentation drifts as code changes; a one-time check doesn't catch that.
- **Treat every AI code-review finding as an automatic action item.** Rejected: two of the three AI-assisted code review findings were technically valid observations but did not identify defects requiring action within the project's current scope; acting on them would have introduced unnecessary out-of-scope changes (e.g., a Docker-build CI step, or rewording a project rule) not requested or needed for this work.
- **Rely solely on static code reading for every claim.** Rejected: some behavior is better confirmed by executing automated tests rather than only reading the implementation. For example, the test suite confirmed expected HTTP status codes and application behavior.

## 4. Trade-offs

**Time VS Accuracy:**
Verification, inspection, and testing take additional time and effort, but they help ensure that AI-generated documentation is accurate and actually matches the code and runtime behavior.

**Scope VS Possible Improvements:**
Classifying and ignoring Noise findings helps keep Module 4 focused on its required scope and avoids unnecessary changes, although some technically valid improvements may be left for future consideration.

**Manual Effort VS Stronger Verification:**
Manually checking API behavior through Swagger takes additional effort, but it provides independent confirmation of actual responses, status codes, and behavior instead of relying only on AI-generated claims or verification that could be inaccurate.

## 5. Consequences

- `app/main.py`'s `list_tasks`, `get_task`, `create_task`, and `update_task` docstrings now show `Z`-suffixed timestamps matching verified `TaskResponse` runtime output; `health_check`'s docstring (a different, non-Pydantic-serialized code path) is unchanged and remains correct.
- `CLAUDE.md` now correctly states that `pytest` and `httpx` are pinned in `requirements.txt`.
- CI does not build or exercise the `Dockerfile`, and `CLAUDE.md`'s "Do not add deployment steps" rule has no adjacent clarification of what "deployment" excludes (Section 9 of `README.md` already states this correctly; `CLAUDE.md` does not). Both are confirmed current facts, left as-is for this module — see Open Questions.
- `TaskResponse.assignee` was verified as intentionally nullable: a task does not need an assigned person, and when `assignee` is `null`, the frontend displays `"Unassigned"` instead of treating it as an error.
- `pytest -v` (44/44) was run during the verification work and after the documentation-only fixes to confirm the test suite still passed.
- No claim in this note or in the reviewed documentation asserts authentication, a database, deployment, or production hardening exist in this project — none of this work added any of these, and CLAUDE.md's do-not rules explicitly exclude them.

## 6. Open Questions

**CI and Docker:**
Should CI on GitHub also automatically test that the Docker image builds successfully, or are the current automated tests enough for Module 4?

**Deployment Documentation:**
Should `CLAUDE.md` also clarify that local Docker usage and CI testing are not considered deployment, or is the explanation already provided in `README.md` enough?

**Python Version:**
Since the course requires Python 3.11 and CI/Docker already use it, should my local development environment also use Python 3.11, or can it continue using Python 3.13.7?

**requirements.txt Encoding:**
Since UTF-16 has not caused problems for me directly but has required special handling by some AI-assisted tools, should `requirements.txt` be converted to UTF-8 for broader tool compatibility, or remain as UTF-16 since the project currently works correctly?

**Task Assignment:**
Should an unassigned task be allowed to move from `ToDo` to `InProgress` or `Done`, or should an assignee be required before the task can move forward?

**Task Due Date:**
Should a task be allowed to move from `ToDo` to `InProgress` or `Done` without a due date, or should a due date be required before the task can progress?

**Personal Reflection:**
I would do this differently by refining the handbook prompts myself first before using GPT and then sending them to Claude Code. During this work, I saw that the prompts needed some adjustments and additional constraints to better match my project's code and requirements, so refining them earlier would have made the process more direct and saved time.

---

*This technical note was reviewed and refined from its initial draft using code inspection, automated tests, OpenAPI/Swagger evidence, and runtime verification to ensure that its claims match the current project.*

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Task Tracker is a learning project (AI Assisted Coding course) built as a Kanban-style task manager: a FastAPI + Pydantic REST backend with in-memory storage, and a single-file vanilla HTML/CSS/JS frontend. There is no database — all task data lives in a module-level dict and is lost on restart.

## Commands

```powershell
# Activate the virtual environment (Windows)
.\.venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install -r requirements.txt

# Run the backend (reload enabled)
python -m uvicorn app.main:app --reload --port 8000

# Run the full test suite
python -m pytest tests/ -v

# Run a single test file / test
python -m pytest tests/test_tasks.py -v
python -m pytest tests/test_tasks.py::test_patch_invalid_transition_todo_to_done_returns_422 -v
```

There is no separate lint/format command configured in this repo.

The backend serves Swagger UI at `/docs` and a health check at `/health`. The frontend (`frontend/index.html`) is a static file opened directly or via VS Code's Live Server — it must be opened with the backend already running, since it calls the API over CORS at a hardcoded `BASE_URL` (`http://localhost:8000` in `frontend/index.html`).

`pytest.ini` sets `pythonpath = .`, so tests import `app` as a top-level package without any src-layout tricks.

Note: `requirements.txt` is UTF-16 encoded; reading it with tools that assume UTF-8 will show garbled/spaced-out characters.

## Architecture

The backend is intentionally small and layered by responsibility rather than by feature:

- `app/models.py` — Pydantic schemas and enums. `TaskCreate` / `TaskUpdate` are input models (`extra="forbid"`, so unknown fields 422); `TaskResponse` is the output model. `TaskStatus` (`ToDo` / `InProgress` / `Done`) and `TaskPriority` (`Low` / `Medium` / `High`) are string enums whose values are the wire format. Title validation (non-blank, ≤200 chars) lives in a shared `_validate_title` helper used by both `TaskCreate` and `TaskUpdate` validators.
- `app/storage.py` — the entire persistence layer: an in-memory `dict[str, dict]` keyed by UUID string, plus CRUD functions (`add_task`, `get_all_tasks`, `get_task_by_id`, `update_task`, `delete_task`) and a `_reset()` used by tests. `overdue` is **never stored** — `_compute_overdue()` derives it on every read from `due_date` + current `status` (a task is overdue only if `due_date < today()` and status is not `Done`). `get_all_tasks` also does the search/filter work (case-insensitive substring match across title/description/assignee, plus optional status/priority equality filters) — this logic lives in storage, not in the route handlers.
- `app/business_rules.py` — status-transition validation as a standalone function (`validate_status_transition`), independent of storage. Valid transitions are an explicit allow-list: `ToDo→InProgress`, `InProgress→Done`, `Done→InProgress`. Same-status "transitions" are always allowed (no-op). Anything else raises HTTP 422 with the allowed transitions listed in the error detail.
- `app/main.py` — FastAPI route handlers only; no business logic. The `PATCH /tasks/{id}` handler is the one place that composes two layers: it loads the existing task, calls `validate_status_transition` only when `status` is present in the payload, and only then calls `storage.update_task`. `app/api/`, `app/schemas/`, and `app/services/` are empty placeholder packages (no code yet) — don't assume routes/schemas live there.

Because `overdue` is computed rather than persisted, any change to due-date or status semantics should be made in `_compute_overdue()` in `storage.py`, not by adding a stored field — this was a deliberate decision (see `docs/mid-course-Project/mini-adr.md`), not an oversight.

Filtering/search is a backend-only concern by design (also an explicit ADR decision) — do not move search/filter logic into the frontend. The frontend's only client-side filter is "overdue," since it can reuse the `overdue` flag already present in each task response.

## Tests

`tests/conftest.py` provides:
- `client` — a `TestClient(app)` fixture.
- `created_task` — creates a default task via the API and returns its JSON body.
- an autouse `_reset_storage` fixture that clears in-memory storage before and after every test — tests never need to manage storage state manually.

`tests/test_tasks.py` is the real suite (pytest, parametrized where useful, one behavior per test, named `test_<action>_<condition>_<expected_result>`). `tests/verify_a.py` is a standalone manual verification script (not pytest-based — run with `python tests/verify_a.py`), used for ad hoc validation of `app/models.py` behavior during development.

## Documentation

`docs/mid-course-Project/` contains the course deliverables for this project phase: `user-stories.md`, `mini-adr.md` (architecture decisions and rejected AI alternatives — read this before changing overdue or search/filter behavior), `verification.md`, `reflection.md`, and `prompt-log.md`. These are course artifacts, not living engineering docs — update them only if asked to.

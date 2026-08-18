# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Project overview

Task Tracker is a learning project (AI Assisted Coding course) built as a Kanban-style task manager: a FastAPI + Pydantic REST backend with in-memory storage, and a single-file vanilla HTML/CSS/JS frontend. There is no database — all task data lives in a module-level dict and is lost on restart.

## Tech stack

- Python 3.11 or later; Docker and CI use Python 3.11, while the current local `.venv` was created with Python 3.13.7.
- FastAPI 0.115.6
- Pydantic v2 (2.10.3)
- Uvicorn 0.32.1
- pytest 9.1.1 — used by the automated test suite and pinned in `requirements.txt`.
- httpx 0.28.1 — used by FastAPI's `TestClient` in the test suite and pinned in `requirements.txt`.
- Vanilla JavaScript frontend present: `frontend/index.html` (single file, no framework, no build step)

Note: `requirements.txt` is UTF-16 encoded; reading it with tools that assume UTF-8 will show garbled/spaced-out characters.

## Run command

```
uvicorn app.main:app --reload --port 8000
```

## Test command

```
pytest -v
```

## Architecture

**Backend** (`app/`):
- `app/main.py` — route handlers; validation/transition rules live in `business_rules.py`, not here, but the `PATCH /tasks/{task_id}` handler does compose the fetch-then-validate-then-update sequence itself (conditionally fetches the existing task and calls `validate_status_transition` only when `status` is present in the payload). Endpoints: `GET /health`, `GET /tasks`, `GET /tasks/{task_id}`, `POST /tasks`, `PATCH /tasks/{task_id}`, `DELETE /tasks/{task_id}`.
- `app/models.py` — Pydantic schemas and enums. `TaskCreate`/`TaskUpdate` are input models (`extra="forbid"`, so unknown fields 422); `TaskResponse` is the output model. `TaskStatus` (`ToDo`/`InProgress`/`Done`) and `TaskPriority` (`Low`/`Medium`/`High`) are string enums. Title validation (non-blank, ≤200 chars) lives in a shared `_validate_title` helper.
- `app/storage.py` — in-memory `dict[str, dict]` keyed by UUID string, plus CRUD functions (`add_task`, `get_all_tasks`, `get_task_by_id`, `update_task`, `delete_task`) and a `_reset()` used by tests. Search/filter logic for `GET /tasks` (case-insensitive substring match on title/description/assignee, plus optional status/priority equality filters) lives here, not in the route handler.
- `app/business_rules.py` — `validate_status_transition()`, the sole location of status-transition rules, independent of storage.
- `app/api/`, `app/schemas/`, `app/services/` — empty placeholder packages (each contains only an `__init__.py`, verified); don't assume routes/schemas live there.

**Frontend**:
- `frontend/index.html` — single-file HTML/CSS/JS Kanban board (To Do / In Progress / Done columns, drag-and-drop). Calls the API via a hardcoded `BASE_URL = 'http://localhost:8000'`, so the backend must already be running.

**Tests** (`tests/`):
- `tests/conftest.py` — `client` (`TestClient(app)`), `created_task` fixture (creates a default task via the API), and an autouse `_reset_storage` fixture that clears in-memory storage before/after every test.
- `tests/test_tasks.py` — main pytest suite.
- `tests/verify_a.py` — standalone manual script (print-based `expect_ok`/`expect_fail` helpers, no `pytest` import, no `test_*` functions), not part of the pytest suite; ad hoc validation of `app/models.py` behavior, run directly with `python tests/verify_a.py`.

**Where task rules live**: status-transition validation is entirely in `app/business_rules.py`; the "overdue" rule is entirely in `app/storage.py` (`_compute_overdue`), computed on every read and never persisted.

## Business rules

Task status values (`app/models.py::TaskStatus`, verified): `ToDo`, `InProgress`, `Done`.

Status transitions (`app/business_rules.py::validate_status_transition`, verified):
- A same-status "transition" (`current == new`) is always allowed (no-op).
- Allowed transitions: `ToDo → InProgress`, `InProgress → Done`, `Done → InProgress`.
- Any other transition raises HTTP 422, with the allowed transitions listed in the error detail.

Overdue rule (`app/storage.py::_compute_overdue`, verified):
- Never stored — recomputed on every read from `due_date` and `status`.
- A task is overdue if `due_date < date.today()` **and** `status != Done`. A task with no `due_date` is never overdue.

## UI states and CORS notes

CORS (`app/main.py`, verified):
- `allow_origins=["*"]`
- `allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"]`
- `allow_headers=["*"]`
- `allow_credentials=False`

UI states (`frontend/index.html`, verified):
- **Loading**: `renderLoadingState()` renders "Loading tasks..." while the initial fetch is in flight.
- **Error**: `.error-message`, `.form-error`, and `#modal-error` elements surface API/network failures — e.g. a failed drag-and-drop status update shows "Failed to update task: ..." and reverts the card; a network failure shows "Network error. Task status reverted."
- **Drag-and-drop**: `.task-card.dragging` / `.column.drag-over` classes track drag state for moving tasks between Kanban columns.
- **Overdue filter**: client-side filter (`activeTaskFilter === 'overdue'`) that reuses the `overdue` flag already present in each task response — the only client-side filter, per the project's backend-filtering design decision.

## Do-not rules

- Do not add authentication.
- Do not add a database.
- Do not add deployment steps.
- Do not make major UI changes without asking first.

## Module 5 guardrails

Module 5 focuses on grading and governing AI-assisted coding work, not building new application features.

- Work docs-first: edit files under `docs/` only unless the user explicitly approves another path.
- Begin with read-only inspection by default.
- Use one bounded task per Codex thread.
- Do not modify `app/` unless the user explicitly approves one specific minimal fix.
- Do not make unrelated changes outside the approved task.
- Before editing, identify the files inspected and the files, if any, that will change.

## Security and governance

- Do not paste, expose, log, or commit secrets, credentials, tokens, or sensitive environment values.
- Do not run destructive commands or destructive Git operations.
- Base repository claims on files actually inspected and cite those files.
- Do not invent findings, commands, behavior, or business rules.
- If evidence is unavailable, ambiguous, or not visible in the repository, state that clearly and mark the claim as `not confirmed` instead of guessing.
- Preserve existing user changes and do not overwrite repository guidance without inspecting it first.
- Preserve existing working behavior and run the relevant verification or tests after changes; report failures exactly as observed.
- Do not stage, commit, or push unless the user explicitly approves those Git actions.

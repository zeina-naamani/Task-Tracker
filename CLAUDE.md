# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Task Tracker is a learning project (AI Assisted Coding course) built as a Kanban-style task manager: a FastAPI + Pydantic REST backend with in-memory storage, and a single-file vanilla HTML/CSS/JS frontend. There is no database — all task data lives in a module-level dict and is lost on restart.

## Tech stack

- Python 3.13 (verified via `.venv/pyvenv.cfg`: `version = 3.13.7`; `README.md` also specifies `py -3.13` for venv creation)
- FastAPI 0.115.6
- Pydantic v2 (2.10.3)
- Uvicorn 0.32.1
- pytest — used by the test suite (`pytest.ini`, `tests/`) but **not** listed in `requirements.txt`; installed separately in this environment (pytest 9.1.1 found via `pip show`). [VERIFY] whether an intentional/pinned version is expected
- httpx — required transitively by FastAPI's `TestClient` (used in `tests/conftest.py`); **not** listed in `requirements.txt`; installed separately in this environment (httpx 0.28.1 found via `pip show`). [VERIFY] whether an intentional/pinned version is expected
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
- `app/main.py` — FastAPI route handlers only; no business logic lives here. Endpoints: `GET /health`, `GET /tasks`, `GET /tasks/{task_id}`, `POST /tasks`, `PATCH /tasks/{task_id}`, `DELETE /tasks/{task_id}`.
- `app/models.py` — Pydantic schemas and enums. `TaskCreate`/`TaskUpdate` are input models (`extra="forbid"`, so unknown fields 422); `TaskResponse` is the output model. `TaskStatus` (`ToDo`/`InProgress`/`Done`) and `TaskPriority` (`Low`/`Medium`/`High`) are string enums. Title validation (non-blank, ≤200 chars) lives in a shared `_validate_title` helper.
- `app/storage.py` — in-memory `dict[str, dict]` keyed by UUID string, plus CRUD functions (`add_task`, `get_all_tasks`, `get_task_by_id`, `update_task`, `delete_task`) and a `_reset()` used by tests. Search/filter logic for `GET /tasks` (case-insensitive substring match on title/description/assignee, plus optional status/priority equality filters) lives here, not in the route handler.
- `app/business_rules.py` — `validate_status_transition()`, the sole location of status-transition rules, independent of storage.
- `app/api/`, `app/schemas/`, `app/services/` — [VERIFY] not re-inspected in this pass; not read to confirm current contents.

**Frontend**:
- `frontend/index.html` — single-file HTML/CSS/JS Kanban board (To Do / In Progress / Done columns, drag-and-drop). Calls the API via a hardcoded `BASE_URL = 'http://localhost:8000'`, so the backend must already be running.

**Tests** (`tests/`):
- `tests/conftest.py` — `client` (`TestClient(app)`), `created_task` fixture (creates a default task via the API), and an autouse `_reset_storage` fixture that clears in-memory storage before/after every test.
- `tests/test_tasks.py` — main pytest suite.
- `tests/verify_a.py` — [VERIFY] not re-inspected in this pass; prior version of this file described it as a standalone manual script, not part of the pytest suite.

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

# Task Tracker Architecture

## 1. What the app does

Task Tracker is a course-project Kanban application whose frontend supports creating, viewing, editing, filtering, and moving tasks. Task deletion is available through the backend API but is not exposed as a frontend UI action. The vanilla HTML/CSS/JavaScript board displays tasks in To Do, In Progress, and Done columns and communicates with a FastAPI backend that validates requests and keeps tasks in memory.

## 2. Data model

The central entity is `Task`.

| Field | Important behavior |
|---|---|
| `id` | Server-generated UUID string |
| `title` | Required, trimmed, nonblank, maximum 200 characters |
| `description` | Optional text; defaults to an empty string |
| `status` | `ToDo`, `InProgress`, or `Done` |
| `priority` | `Low`, `Medium`, or `High` |
| `assignee` | Optional string |
| `due_date` | Optional date |
| `overdue` | Computed on reads; true when the due date is past and status is not Done |
| `created_at`, `updated_at` | Server-generated UTC datetimes |

`TaskCreate` defines creation input, `TaskUpdate` supports partial updates, and `TaskResponse` defines API output. Unknown input fields are forbidden.

## 3. Request flow

When a user creates a task:

1. `submitTask()` in `frontend/index.html` reads and trims the form values, rejects a blank title, and builds a JSON payload.
2. The browser sends `POST http://localhost:8000/tasks`.
3. FastAPI validates the body as `TaskCreate`.
4. `create_task()` in `app/main.py` passes the validated model to `storage.add_task()`.
5. Storage generates a UUID and UTC timestamps, saves the task in the module-level `_tasks` dictionary, and constructs a `TaskResponse`.
6. The API returns HTTP 201 with the created task.
7. The frontend closes the modal and calls `fetchTasks()` to reload and render the board.

## 4. Key files

- `AGENTS.md` — Repository architecture, business rules, commands, and Module 5 guardrails.
- `README.md` — Setup, run/test instructions, structure, and current limitations.
- `app/main.py` — FastAPI application, CORS configuration, and task CRUD route handlers.
- `app/models.py` — Pydantic task input/output models, enums, and title validation.
- `app/storage.py` — In-memory CRUD, search/filter behavior, timestamps, and overdue calculation.
- `app/business_rules.py` — Allowed and rejected task-status transitions.
- `frontend/index.html` — Entire Kanban UI, task modal, API calls, rendering, filters, and drag-and-drop.
- `tests/conftest.py` — API client, task fixture, and automatic storage reset.
- `tests/test_tasks.py` — Automated API behavior and validation tests.

## 5. Conventions

- Validation is performed primarily by Pydantic models; invalid bodies and unknown fields return HTTP 422.
- Status transitions are centralized in `app/business_rules.py`; same-status updates are allowed.
- Storage is a module-level `dict[str, dict]`; there is no database, and all tasks disappear on restart.
- Missing tasks return HTTP 404; successful deletion returns HTTP 204 without a body.
- The backend computes `overdue` on each read rather than storing it.
- The frontend uses a hardcoded `BASE_URL` of `http://localhost:8000` and must be served separately.
- The frontend checks `response.ok`, displays validation or modal errors, and escapes task values before inserting them into generated HTML.
- Tests use pytest and FastAPI `TestClient`; storage is cleared before and after each test.

## 6. Not visible or assumptions

- No authentication, database, or production deployment behavior exists in the inspected repository.
- Production scaling, durable persistence, multi-process synchronization, and user-specific authorization are not defined.
- The intended hosting environment beyond local course use is **not confirmed**.
- Any architecture outside the inspected repository, such as external services or an undisclosed production system, is **not confirmed**.

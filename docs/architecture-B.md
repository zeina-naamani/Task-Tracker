# Task Tracker Architecture — Strategy B

## What the app does

Task Tracker is a learning-oriented Kanban task manager with To Do, In Progress, and Done columns. Its single-file vanilla HTML/CSS/JavaScript frontend supports creating, viewing, editing, searching, filtering, and moving tasks through a FastAPI REST backend; the backend API also supports deletion, although deletion is not exposed as a frontend UI action. All data is held in memory and is lost when the backend restarts.

## Data model

The application has one primary entity, `Task`, represented by Pydantic request and response models. Important fields include a UUID string identifier, title, description, status (`ToDo`, `InProgress`, or `Done`), priority (`Low`, `Medium`, or `High`), assignee, optional due date, and a computed `overdue` flag. Task creation and update use separate input models, while `TaskResponse` defines API output.

## Request flow

When a user creates a task, the frontend sends a request to `POST /tasks` at the hardcoded backend URL `http://localhost:8000`. FastAPI parses and validates the request using `TaskCreate`, including rejecting unknown fields and invalid or blank titles. The route passes the validated payload to the storage layer, which generates a UUID, stores the task in the module-level dictionary, computes its `overdue` value for the response, and returns a `TaskResponse` with HTTP 201.

## Key files

- `app/main.py` — Configures FastAPI and CORS, exposes health and task CRUD routes, and coordinates status-transition validation during updates.
- `app/models.py` — Defines task status and priority enums and the strict Pydantic create, update, and response schemas.
- `app/storage.py` — Implements in-memory CRUD, searching, filtering, response construction, and overdue calculation.
- `app/business_rules.py` — Defines and enforces allowed task status transitions independently of storage.
- `frontend/index.html` — Contains the complete Kanban frontend, API integration, forms, filters, UI states, and drag-and-drop behavior.
- `tests/conftest.py` — Supplies the API test client, a reusable created-task fixture, and per-test storage reset.
- `tests/test_tasks.py` — Verifies CRUD, validation, due dates, overdue behavior, transitions, searching, and filtering.
- `README.md` — Documents setup, execution, testing, architecture, project structure, and current limitations.

## Conventions

Input schemas forbid unknown fields, and titles are stripped, required to be non-blank, and limited to 200 characters. Status-transition rules are centralized in `app/business_rules.py`; same-status updates and `ToDo → InProgress`, `InProgress → Done`, and `Done → InProgress` are allowed, while invalid transitions return HTTP 422. Missing tasks return HTTP 404. Storage is a module-level dictionary with no database, and `overdue` is recomputed on reads rather than persisted. Search is case-insensitive across title, description, and assignee, while status and priority use equality filters. The frontend calls the REST API through a hardcoded base URL, and permissive local-development CORS allows the supported CRUD methods without credentials.

## Not visible or assumptions

Authentication, database persistence, and deployment are explicitly outside the current architecture. The supplied context does not confirm production hosting, multi-user concurrency behavior, persistent recovery, or behavior across multiple backend worker processes. No assumptions are made about those areas.

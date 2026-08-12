# Task Tracker Architecture — Strategy C

## What the app does

Task Tracker is a REST API for creating, listing, searching, filtering, retrieving, partially updating, and deleting tasks. It also exposes a health endpoint and returns a computed overdue indicator with task responses.

## Data model

The primary entity is `Task`.

- Core fields: `id`, `title`, `description`, `status`, `priority`, `assignee`, and `due_date`.
- Metadata: `created_at` and `updated_at`.
- Computed field: `overdue`, true when the due date is before today and status is not `Done`.
- Status values: `ToDo`, `InProgress`, `Done`.
- Priority values: `Low`, `Medium`, `High`.
- Creation defaults: empty description, `ToDo` status, `Medium` priority, and null assignee/due date.

## Request flow

When a client sends `POST /tasks`, FastAPI receives a `TaskCreate` payload. The model forbids unknown fields, trims the title, and rejects blank or over-200-character titles. The route passes the validated payload to `storage.add_task()`, which generates a UUID, assigns UTC creation and update timestamps, stores a dictionary in the module-level `_tasks` collection, computes `overdue`, and returns a `TaskResponse` with HTTP 201.

## Key files

- `app/main.py` — defines the FastAPI application, CORS configuration, and health/task routes.
- `app/models.py` — defines task input/output models, enums, defaults, and title validation.
- `app/storage.py` — implements in-memory CRUD, filtering, response construction, and overdue calculation.
- `app/business_rules.py` — imported by `app/main.py` for status-transition validation; its implementation is **not visible from the files I read**.
- Remaining key files are **not visible from the files I read**.

## Conventions

- Validation: Pydantic models forbid extra fields; task titles are stripped and must be nonblank and at most 200 characters. Update payloads contain optional fields, and only explicitly supplied fields are merged.
- Storage: tasks reside in a module-level dictionary keyed by UUID strings. Persistence beyond process memory is **not visible from the files I read**.
- Error handling: task lookup, update, and deletion routes explicitly raise HTTP 404 when an ID is absent. Status updates invoke a separate transition validator; its rules are **not visible from the files I read**.
- Querying: list filters are combined, with case-insensitive search across title, description, and assignee plus exact status and priority filters.
- Frontend/backend interaction: CORS permits all origins and allows `GET`, `POST`, `PATCH`, `DELETE`, and `OPTIONS`. The frontend implementation and how it calls the API are **not visible from the files I read**.

## Not visible or assumptions

Authentication, frontend structure and behavior, tests, deployment, database integration, process topology, production configuration, observability, and the exact status-transition rules are **not visible from the files I read**. No behavior for these areas is assumed.

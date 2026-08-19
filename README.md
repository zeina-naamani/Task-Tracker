# Task Tracker (Module 4)

A Kanban-style task management application built as part of the AI Assisted Coding course, using **Python**, **FastAPI**, **Pydantic**, and a vanilla **HTML/CSS/JavaScript** frontend.

## 1. Project overview

The backend is built with FastAPI and uses **in-memory storage only** — all task data lives in a module-level dict and is lost on restart (see [Project conventions and current limitations](#9-project-conventions-and-current-limitations)). The frontend is a single-file Kanban board (`frontend/index.html`, no framework, no build step) that communicates with the backend through a hardcoded `BASE_URL`.

Core features:

- Create, view, update, and delete tasks
- Kanban board (To Do, In Progress, Done) with drag-and-drop status updates
- Due dates with backend-computed overdue detection
- Backend search (title/description/assignee) and status/priority filtering
- Business-rule validation for task status transitions
- Loading and error states in the UI

### Final Project submission

- **Branch reviewed:** `final-project`
- **What this submission demonstrates:** The existing Task Tracker remains runnable within its intended course scope. CI runs the pytest suite on every push and pull request, and the Docker image builds and runs with `/health` returning HTTP `200`. AI review, security-review, and ownership evidence is recorded under `docs/`.
- **Commands:** Follow [Run the app locally](#4-run-the-app-locally), [Run tests](#5-run-tests), and [Run with Docker](#6-run-with-docker) for the exact repository commands.
- **Evidence:** [Final Project release evidence](docs/release-evidence.md), [Final AI review and ownership evidence](docs/final-ai-review.md), and [AI Playbook](docs/ai-playbook.md).

AI assisted with bounded code and diff review, CI/Docker/documentation review, security review, and debugging. I verified the work through repository inspection, diff review, automated tests, Docker/runtime evidence, and a manual Swagger check. I corrected one initial AI recommendation: after verifying the repository's field semantics, I decided that `description: null` should normalize to `""`, while null status and priority should be rejected.

## 2. Prerequisites

- **Python 3.11 or later** — matches the version used by Docker and CI (see [Run with Docker](#6-run-with-docker) and [CI workflow summary](#7-ci-workflow-summary)).
- **Git**, to clone the repository.
- **Docker** — only required if you want to run the app in a container (see [Run with Docker](#6-run-with-docker)). No minimum version is pinned in this repo.
- **VS Code with the Live Server extension** (or another static file server) — used to serve `frontend/index.html` (see [Run the app locally](#4-run-the-app-locally)).

## 3. Local setup

Run from the repository root:

```bash
git clone <repository-url>
cd Task-Tracker
```

Create and activate a virtual environment (Windows / PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Project dependencies are listed in `requirements.txt`. Install them using the command above.

## 4. Run the app locally

The application consists of two parts: a FastAPI backend and a frontend served by a local static file server.

With the virtual environment from [Local setup](#3-local-setup) activated, start the backend from the repository root:

```bash
uvicorn app.main:app --reload --port 8000
```

The backend is available at:

- Swagger UI: http://127.0.0.1:8000/docs
- Health endpoint: http://127.0.0.1:8000/health
- OpenAPI spec: http://127.0.0.1:8000/openapi.json

**Frontend:** once the backend is running, open `frontend/index.html` using the VS Code Live Server extension (or another static file server). The frontend is served at http://localhost:8080 and communicates with the FastAPI backend at http://localhost:8000 through the configured `BASE_URL`. The backend must already be running before you open the frontend.

## 5. Run tests

With the virtual environment activated, run from the repository root:

```bash
pytest -v
```

`pytest.ini` sets `pythonpath = .`, so `pytest -v` discovers and runs `tests/test_tasks.py` directly from the repo root — no `python -m` prefix or explicit `tests/` path is needed.

`tests/verify_a.py` is a standalone manual script (not part of the pytest suite) and is run separately if needed:

```bash
python tests/verify_a.py
```

## 6. Run with Docker

**Note:** If the backend is already running locally, stop it (`Ctrl+C`) before starting the Docker container, as both use port **8000**.

Build the image from the repository root:

```bash
docker build -t task-tracker:dev .
```

Run the container:

```bash
docker run --rm -d -p 8000:8000 --name tt-dev task-tracker:dev
```

Verify it's healthy:

```bash
curl http://localhost:8000/health
```

Stop it when done:

```bash
docker stop tt-dev
```

The `Dockerfile` is a multi-stage build (`python:3.11-slim`) that installs dependencies in a builder stage, copies only the installed packages and `app/` into the runtime stage, runs as a non-root user (`app`), and includes a `HEALTHCHECK` that polls `GET /health` using only the Python standard library. The container's `CMD` does **not** use `--reload`.

Local development requires Python 3.11 or later; Docker and the CI workflow are configured with Python 3.11.

## 7. CI workflow summary

Defined in `.github/workflows/ci.yml`:

- **Triggers:** every `push` and `pull_request` (no branch filter).
- **Runner:** `ubuntu-latest`.
- **Steps:** checkout (`actions/checkout@v4`) → set up Python 3.11 (`actions/setup-python@v5`) → `python -m pip install --upgrade pip` → `pip install -r requirements.txt` → `pytest -v`.
- No `continue-on-error`, no `|| true`, no `--exit-zero`, and no piping that could hide a test failure — a failing test fails the workflow.
- No deployment steps.

## 8. Project structure

```text
app/
├── main.py            # Route handlers (health, tasks CRUD)
├── models.py          # Pydantic schemas: TaskCreate, TaskUpdate, TaskResponse, enums
├── storage.py         # In-memory storage, CRUD functions, search/filter, overdue calculation
├── business_rules.py  # validate_status_transition() — the sole location of transition rules
├── api/               # Reserved for future API modules
├── schemas/           # Reserved for future schemas
└── services/          # Reserved for future business services

frontend/
└── index.html         # Single-file Kanban board (HTML/CSS/JS, no build step)

tests/
├── conftest.py    # Shared pytest fixtures and test setup
├── test_tasks.py  # Automated API tests using pytest
└── verify_a.py    # Manual verification script

docs/
├── decisions/  # Technical decision notes
├── midcourse/  # Mid-course project deliverables (user stories, mini ADR, etc.)
└── module4/    # Module 4 deliverables (prompt log, CI/Docker verification notes)

Dockerfile
.dockerignore
.github/workflows/ci.yml
requirements.txt
pytest.ini
```

## 9. Project conventions and current limitations

- **No database.** Storage is a module-level `dict[str, dict]` in `app/storage.py`; all data is lost on restart.
- **No authentication.**
- **No deployment.** CI (`ci.yml`) runs tests only; the Docker image is for local/manual container runs, not a deployment target.
- **Status transitions are centralized** in `app/business_rules.py::validate_status_transition`: `ToDo → InProgress`, `InProgress → Done`, `Done → InProgress` are allowed; a same-status transition is always a no-op; any other transition returns `422`.
- **Overdue is never stored.** It's recomputed on every read in `app/storage.py` from `due_date` and `status` — a task with no `due_date` is never overdue.
- **`app/api/`, `app/schemas/`, and `app/services/` are reserved for future API modules, schemas, and business services** (each currently contains only an `__init__.py`) — don't assume routes or schemas live there yet.
- Input models (`TaskCreate`, `TaskUpdate`) use `extra="forbid"`, so unknown fields in a request body return `422`.

## 10. Related documentation

- [Personal AI Coding Playbook](docs/ai-playbook.md) — personal rules, review habits, course evidence, and tool choices for AI-assisted coding work.

Technical decision notes are documented under `docs/decisions/`:

- [Technical_Notes.md](docs/decisions/Technical_Notes.md) — technical decision note on the documentation-verification approach, including verification evidence, trade-offs, consequences, and open questions.

The mid-course technical note is the mini ADR at [`docs/midcourse/mini-adr.md`](docs/midcourse/mini-adr.md), documenting implementation decisions for the mid-course project's due-date/overdue and search/filter features.

Module 4 deliverables are documented under `docs/module4/`:

- [`ci-green-red-green-verification.md`](docs/module4/ci-green-red-green-verification.md) — evidence log for the CI green→red→green verification.
- [`verified-interaction.md`](docs/module4/verified-interaction.md) — verified-interaction note on status-transition business rules.

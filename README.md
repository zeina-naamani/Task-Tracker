# Task Tracker

A Task Tracker web application built as part of the AI Assisted Coding course using **Python**, **FastAPI**, **Pydantic**, **HTML**, **CSS**, and **JavaScript**.

The project provides a Kanban-style task management interface with a FastAPI REST API backend and a simple frontend. Tasks can be created, viewed, updated, deleted, searched, filtered, and moved between workflow stages using drag and drop.

## Features

- Create, view, update, and delete tasks
- Kanban board (To Do, In Progress, Done)
- Drag and drop status updates
- Due date support
- Overdue badge
- Backend overdue calculation
- Backend search
- Backend status filtering
- Backend priority filtering
- Frontend overdue filtering
- Combined search and filtering
- Loading and error states
- Business rule validation for task status transitions

## Technologies

- Python
- FastAPI
- Pydantic
- HTML
- CSS
- JavaScript
- Pytest

## Project Structure

```text
app/
frontend/
tests/
docs/
```

## Running the Project

### 1. Clone the repository

```bash
git clone <repository-url>
cd Task-Tracker
```

### 2. Create and activate the virtual environment (Windows)

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the backend

```bash
python -m uvicorn app.main:app --reload --port 8000
```

The backend will be available at:

- Swagger UI: http://127.0.0.1:8000/docs
- Health Endpoint: http://127.0.0.1:8000/health
- OpenAPI Specification: http://127.0.0.1:8000/openapi.json

### 5. Run the frontend

With the backend running:

1. Open the `frontend` folder in Visual Studio Code.
2. Open `frontend/index.html`.
3. Right-click the file and select **Open with Live Server**.

> **Note:** The backend must be running before opening the frontend, otherwise the frontend will not be able to communicate with the API.

## Running Tests

Activate the virtual environment if it is not already active:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run the test suite:

```bash
python -m pytest tests/ -v
```

## Documentation

Project documentation for the mid-course project is available in the `docs/midcourse/` directory:

- User Stories
- Mini ADR
- Prompt Log
- Verification
- Reflection

## Submission

The mid-course project work is available on the **mid-course-project** branch.

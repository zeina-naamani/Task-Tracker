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

```
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

### 2. Create and activate a virtual environment

Windows:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install dependencies
pip install -r requirements.txt

### 4. Run the backend
uvicorn app.main:app --reload --port 8000

### 5. Run the frontend

Open `frontend/index.html` using VS Code Live Server.

## Running Tests
python -m pytest tests/ -v

## API Documentation

After starting the backend:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Documentation

Project documentation is available in the `docs/` directory:

- User Stories
- Mini ADR
- Prompt Log
- Verification
- Reflection
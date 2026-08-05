"""
Task Tracker API

FastAPI backend with in-memory storage, CRUD endpoints,
business-rule validation, and CORS support for the frontend.
"""

from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app import storage
from app.business_rules import validate_status_transition
from app.models import (
    TaskCreate,
    TaskPriority,
    TaskResponse,
    TaskStatus,
    TaskUpdate,
)

app = FastAPI(
    title="Task Tracker API",
    description="A learning project REST API for tracking tasks.",
    version="0.1.0",
)

# Allow the frontend to communicate with the FastAPI backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local development
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=False,
)


@app.get("/health", tags=["Health"])
def health_check() -> dict:
    """Return the current API health status and UTC timestamp.

    Returns:
        dict: A mapping with ``status`` (always ``"ok"``) and
        ``timestamp`` (current UTC time in ISO 8601 format).

    Example:
        GET /health

    Status:
        200 OK

    Response:
        {
            "status": "ok",
            "timestamp": "2026-08-05T12:00:00+00:00"
        }
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get(
    "/tasks",
    response_model=list[TaskResponse],
    tags=["tasks"],
)
def list_tasks(
    search: str | None = None,
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
) -> list[TaskResponse]:
    """Retrieve tasks, optionally filtered by search term, status, and priority.

    Args:
        search: Case-insensitive substring matched against a task's
            title, description, or assignee. Blank or omitted values
            apply no search filter.
        status: If provided, only tasks with this exact status are
            returned.
        priority: If provided, only tasks with this exact priority are
            returned.

    Returns:
        list[TaskResponse]: Tasks matching all provided filters
        (combined with AND), each including the computed ``overdue``
        flag.

    Example:
        GET /tasks?search=bug&status=ToDo&priority=High

    Status:
        200 OK

    Response:
        [
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "title": "Fix login bug",
                "description": "",
                "status": "ToDo",
                "priority": "High",
                "assignee": null,
                "due_date": null,
                "overdue": false,
                "created_at": "2026-08-05T12:00:00+00:00",
                "updated_at": "2026-08-05T12:00:00+00:00"
            }
        ]
    """
    return storage.get_all_tasks(
        search=search,
        status=status,
        priority=priority,
    )


@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    tags=["tasks"],
)
def get_task(task_id: str) -> TaskResponse:
    """Retrieve a single task by its unique identifier.

    Args:
        task_id: The UUID string identifying the task.

    Returns:
        TaskResponse: The matching task, including the computed
        ``overdue`` flag.

    Raises:
        HTTPException: 404 if no task with ``task_id`` exists.

    Example:
        GET /tasks/{task_id}

    Status:
        200 OK

    Response:
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "title": "Fix login bug",
            "description": "",
            "status": "ToDo",
            "priority": "High",
            "assignee": null,
            "due_date": null,
            "overdue": false,
            "created_at": "2026-08-05T12:00:00+00:00",
            "updated_at": "2026-08-05T12:00:00+00:00"
        }
    """
    task = storage.get_task_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    return task


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["tasks"],
)
def create_task(payload: TaskCreate) -> TaskResponse:
    """Create a new task.

    Args:
        payload: Fields for the new task. ``status`` defaults to
            ``ToDo`` and ``priority`` defaults to ``Medium`` when
            omitted (see ``TaskCreate``).

    Returns:
        TaskResponse: The newly created task, with a generated ``id``
        and ``created_at``/``updated_at`` timestamps.

    Example:
        POST /tasks

    Status:
        201 Created

    Response:
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "title": "Fix login bug",
            "description": "",
            "status": "ToDo",
            "priority": "Medium",
            "assignee": null,
            "due_date": null,
            "overdue": false,
            "created_at": "2026-08-05T12:00:00+00:00",
            "updated_at": "2026-08-05T12:00:00+00:00"
        }
    """
    return storage.add_task(payload)


@app.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    tags=["tasks"],
)
def update_task(
    task_id: str,
    payload: TaskUpdate,
) -> TaskResponse:
    """Update an existing task with the fields provided.

    Only fields explicitly present in ``payload`` are changed; fields
    omitted from ``payload`` remain unchanged. If ``payload.status``
    is provided, the transition from the task's current status is
    validated before the update is applied. A same-status transition
    is always allowed as a no-op (see ``validate_status_transition``).

    Args:
        task_id: The UUID string identifying the task to update.
        payload: The fields to update. Unset fields are ignored.

    Returns:
        TaskResponse: The updated task.

    Raises:
        HTTPException: 404 if no task with ``task_id`` exists.
        HTTPException: 422 if ``payload.status`` is present and the
            transition from the task's current status is not allowed
            (see ``validate_status_transition``).

    Example:
        PATCH /tasks/{task_id}

    Status:
        200 OK

    Response:
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "title": "Fix login bug",
            "description": "",
            "status": "InProgress",
            "priority": "High",
            "assignee": null,
            "due_date": null,
            "overdue": false,
            "created_at": "2026-08-05T12:00:00+00:00",
            "updated_at": "2026-08-05T12:05:00+00:00"
        }
    """
    if payload.status is not None:
        existing = storage.get_task_by_id(task_id)

        if existing is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found",
            )

        validate_status_transition(
            existing.status,
            payload.status,
        )

    task = storage.update_task(task_id, payload)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    return task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["tasks"],
)
def delete_task(task_id: str) -> None:
    """Delete an existing task by its ID.

    Args:
        task_id: The UUID string identifying the task to delete.

    Returns:
        None

    Raises:
        HTTPException: 404 if no task with ``task_id`` exists.

    Example:
        DELETE /tasks/{task_id}

    Status:
        204 No Content
    """
    deleted = storage.delete_task(task_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
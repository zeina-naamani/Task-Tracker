from datetime import date, datetime, timezone
from typing import Optional
from uuid import uuid4

from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate

_tasks: dict[str, dict] = {}


def _compute_overdue(task_status: TaskStatus, due_date: Optional[date]) -> bool:
    if due_date is None or task_status == TaskStatus.DONE:
        return False
    return due_date < date.today()


def _build_task_response(task_data: dict) -> TaskResponse:
    return TaskResponse(
        id=task_data["id"],
        title=task_data["title"],
        description=task_data["description"],
        status=task_data["status"],
        priority=task_data["priority"],
        assignee=task_data["assignee"],
        due_date=task_data.get("due_date"),
        overdue=_compute_overdue(task_data["status"], task_data.get("due_date")),
        created_at=task_data["created_at"],
        updated_at=task_data["updated_at"],
    )


def add_task(payload: TaskCreate) -> TaskResponse:
    """Create and store a new task.

    Generates a new UUID and sets ``created_at``/``updated_at`` to the
    current UTC time.

    Args:
        payload: Validated task creation data.

    Returns:
        TaskResponse: The newly stored task, including the computed
        ``overdue`` flag.
    """
    now = datetime.now(timezone.utc)
    task_data = {
        "id": str(uuid4()),
        "title": payload.title,
        "description": payload.description or "",
        "status": payload.status,
        "priority": payload.priority,
        "assignee": payload.assignee,
        "due_date": payload.due_date,
        "created_at": now,
        "updated_at": now,
    }
    _tasks[task_data["id"]] = task_data
    return _build_task_response(task_data)


def get_all_tasks(
    search: Optional[str] = None,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
) -> list[TaskResponse]:
    """Retrieve all stored tasks, optionally filtered.

    Args:
        search: Case-insensitive substring matched against title,
            description, or assignee. Blank or ``None`` applies no
            filter.
        status: If provided, only tasks with this exact status are
            included.
        priority: If provided, only tasks with this exact priority are
            included.

    Returns:
        list[TaskResponse]: Tasks matching all provided filters
        (combined with AND), each including the computed ``overdue``
        flag.
    """
    tasks = list(_tasks.values())

    search_term = (search or "").strip().lower()
    if search_term:
        tasks = [
            task
            for task in tasks
            if search_term in (task["title"] or "").lower()
            or search_term in (task["description"] or "").lower()
            or search_term in (task["assignee"] or "").lower()
        ]

    if status is not None:
        tasks = [task for task in tasks if task["status"] == status]
    if priority is not None:
        tasks = [task for task in tasks if task["priority"] == priority]
    return [_build_task_response(task) for task in tasks]


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    """Retrieve a single stored task by its ID.

    Args:
        task_id: The UUID string identifying the task.

    Returns:
        Optional[TaskResponse]: The matching task, including the
        computed ``overdue`` flag, or ``None`` if no task with
        ``task_id`` exists.
    """
    task_data = _tasks.get(task_id)
    if task_data is None:
        return None
    return _build_task_response(task_data)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    """Update a stored task, merging only the fields set on payload.

    Fields omitted from ``payload`` remain unchanged. This function
    does not perform status-transition validation — that is the
    caller's responsibility.

    Args:
        task_id: The UUID string identifying the task to update.
        payload: The fields to update. Unset fields are ignored.

    Returns:
        Optional[TaskResponse]: ``None`` if no task with ``task_id``
        exists. If ``payload`` has no fields set, the existing task
        is returned unchanged and ``updated_at`` is left untouched.
        Otherwise, the merged task is returned with ``updated_at``
        refreshed to the current UTC time.
    """
    task_data = _tasks.get(task_id)
    if task_data is None:
        return None

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return _build_task_response(task_data)

    updated_data = {**task_data, **updates, "updated_at": datetime.now(timezone.utc)}
    _tasks[task_id] = updated_data
    return _build_task_response(updated_data)


def delete_task(task_id: str) -> bool:
    """Delete a stored task by its ID.

    Args:
        task_id: The UUID string identifying the task to delete.

    Returns:
        bool: ``True`` if a task was found and deleted, ``False`` if
        no task with ``task_id`` exists.
    """
    if task_id not in _tasks:
        return False
    del _tasks[task_id]
    return True


def _reset() -> None:
    _tasks.clear()

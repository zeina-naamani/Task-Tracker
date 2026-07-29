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
    task_data = _tasks.get(task_id)
    if task_data is None:
        return None
    return _build_task_response(task_data)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
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
    if task_id not in _tasks:
        return False
    del _tasks[task_id]
    return True


def _reset() -> None:
    _tasks.clear()

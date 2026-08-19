from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


def _validate_title(value: str) -> str:
    stripped = value.strip()
    if not stripped:
        raise ValueError("title must not be blank")
    if len(stripped) > 200:
        raise ValueError("title must be at most 200 characters")
    return stripped


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    description: Optional[str] = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    due_date: Optional[date] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        """Validate and normalize the task title.

        Args:
            value: The raw title string.

        Returns:
            str: The stripped title.

        Raises:
            ValueError: If the stripped title is blank or exceeds 200
                characters (see ``_validate_title``).
        """
        return _validate_title(value)


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    due_date: Optional[date] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: Optional[str]) -> Optional[str]:
        """Validate and normalize an updated task title.

        Runs only when ``title`` is explicitly present in the input
        payload (Pydantic skips this validator for an omitted
        ``title`` field, since it keeps its ``None`` default
        unvalidated; verified via ``TaskUpdate()`` not raising).

        Args:
            value: The raw title string, or ``None`` if explicitly
                set to null in the payload.

        Returns:
            str: The stripped title.

        Raises:
            ValueError: If ``value`` is ``None`` (title must not be
                explicitly null), or if the stripped title is blank
                or exceeds 200 characters (see ``_validate_title``).
        """
        if value is None:
            raise ValueError("title must not be null")
        return _validate_title(value)

    @field_validator("description")
    @classmethod
    def normalize_description(cls, value: Optional[str]) -> str:
        return value or ""

    @field_validator("status", "priority")
    @classmethod
    def reject_null_required_fields(
        cls,
        value: Optional[TaskStatus | TaskPriority],
    ) -> TaskStatus | TaskPriority:
        if value is None:
            raise ValueError("field must not be null")
        return value


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str]
    due_date: Optional[date] = None
    overdue: bool = False
    created_at: datetime
    updated_at: datetime

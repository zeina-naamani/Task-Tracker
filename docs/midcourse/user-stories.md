# User Stories

This document describes the two features implemented for the Mid-Course Project. Each feature includes user stories, acceptance criteria, and one AI assumption that was reviewed and corrected during development.

---

# Feature 1 – Due Dates and Overdue Detection

## US-1 – Create a task with an optional due date

**As a team member,** I want to optionally assign a due date when creating a task so that deadlines can be tracked.

### Acceptance Criteria

- A task can be created with or without a due date.
- A valid due date is accepted by the backend.
- Invalid due date values are rejected with a validation error.
- The due date is displayed on the task card when present.

---

## US-2 – Update or remove a due date

**As a team member,** I want to update or remove a task's due date so that deadlines remain accurate.

### Acceptance Criteria

- An existing due date can be changed.
- An existing due date can be removed.
- The updated value is displayed after the task is saved.
- Invalid due date updates are rejected by the backend.

---

## US-3 – View overdue tasks

**As a team member,** I want overdue tasks to be clearly identified so that I can quickly recognise work requiring attention.

### Acceptance Criteria

- A task is marked as overdue when its due date has passed and its status is not **Done**.
- Tasks with the status **Done** are never marked as overdue.
- Overdue tasks display an overdue badge on the task card.
- The overdue value is recalculated whenever tasks are retrieved.

---

## US-4 – Filter overdue tasks

**As a team member,** I want to filter the board to display only overdue tasks so that I can focus on urgent work.

### Acceptance Criteria

- Selecting **Overdue Only** displays only overdue tasks.
- Selecting **All Tasks** restores the complete board.
- Empty status columns remain visible while the overdue filter is active.
- The overdue filter works with the task data returned by the backend.

---

## AI Assumption Corrected for Feature 1

### Initial AI Assumption

The AI initially suggested storing an `overdue` field as part of each task's saved data.

### Correction

The `overdue` value is derived information and should not be stored. The final implementation calculates it in the backend whenever a task response is created, based on:

- the task's due date,
- the current date,
- and the task's status.

This avoids storing a value that could become outdated and keeps the stored task data consistent.

---

# Feature 2 – Search and Combined Filters

## US-1 – Search tasks

**As a team member,** I want to search tasks by keyword so that I can quickly locate specific work items.

### Acceptance Criteria

- Search matches the task title.
- Search matches the task description.
- Search matches the task assignee.
- Search is case-insensitive.
- Search results update immediately as the user types.
- No matching tasks return HTTP 200 with an empty list.

---

## US-2 – Filter tasks by status

**As a team member,** I want to filter tasks by status so that I can focus on a particular stage of work.

### Acceptance Criteria

- Tasks can be filtered by **ToDo**, **InProgress**, or **Done**.
- Selecting **All Statuses** removes the status filter.
- Invalid status values are rejected with HTTP 422.
- Only tasks matching the selected status are returned.

---

## US-3 – Filter tasks by priority

**As a team member,** I want to filter tasks by priority so that I can focus on the most relevant work.

### Acceptance Criteria

- Tasks can be filtered by **Low**, **Medium**, or **High** priority.
- Selecting **All Priorities** removes the priority filter.
- Invalid priority values are rejected with HTTP 422.
- Only tasks matching the selected priority are returned.

---

## US-4 – Combine search and filters

**As a team member,** I want to combine search, status, and priority filters so that I can narrow the task list efficiently.

### Acceptance Criteria

- Search, status, and priority can be used together.
- The frontend sends only active filters as query parameters.
- The backend applies all provided filters to the same request.
- The **Clear Filters** button resets the search, status, and priority filters.
- Active filters are visually highlighted.
- Empty results return HTTP 200 with an empty list.
- The overdue filter can still be applied to the results displayed on the board.

---

## AI Assumption Corrected for Feature 2

### Initial AI Assumption

The AI initially suggested implementing search entirely in the frontend.

### Correction

The final implementation extends `GET /tasks` so that searching and filtering are performed by the backend. The frontend sends optional query parameters for:

- `search`,
- `status`,
- and `priority`.

The backend then returns only the matching tasks. The overdue filter remains frontend-side because it uses the derived `overdue` value already included in each task response.
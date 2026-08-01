## 1 – Add the `due_date` Field to the Backend


### Prompt

1 – Add the due\_date field to the backend

I am implementing Feature 1 (Due Dates + Overdue Filter) for my existing FastAPI Task Tracker.

Current project:



* Backend: Python/FastAPI

* Storage: In-memory

* Existing task fields:



&#x20; * id

&#x20; * title

&#x20; * description

&#x20; * status

&#x20; * priority

&#x20; * assignee

* Existing CRUD endpoints and tests are working.

* Existing status-transition business rules must remain unchanged.



Task:

Add support for an optional due\_date field to the backend data model.



Requirements:



* Add an optional due\_date field to the appropriate Pydantic models.

* Use the appropriate Python date type for validation.

* Existing tasks without a due date must continue to work.

* Existing CRUD endpoints should continue to function without breaking backward compatibility.

* Existing validation rules for title, status, and priority must remain unchanged.

* Do not implement overdue logic yet.

* Do not modify the frontend.

* Do not change storage behavior beyond storing the new optional field.



Constraints:



* Make only the minimum required backend changes.

* Do not rewrite entire files.

* Explain each file that needs to be modified before generating code.

* After generating the code, explain how I should verify that this step works before moving to the next implementation step.



### AI Response Summary



The AI inspected the backend models and identified the Pydantic task models that needed to support the new field. It proposed adding `due_date` as an optional Python `date` value so FastAPI and Pydantic could validate dates in the standard `YYYY-MM-DD` format.



The response kept the change limited to the backend data model and existing task flow. It preserved compatibility with tasks that did not contain a due date and did not introduce overdue calculations or frontend changes. It also provided verification steps for creating, retrieving, updating, and clearing a task’s due date while confirming that the existing tests and status-transition rules still worked.



### What I Accepted



* I accepted adding `due_date` as an optional field to the appropriate task models.

* I accepted using Python’s `date` type for automatic validation.

* I accepted allowing tasks to be created without a due date.

* I accepted storing `null` when no due date was provided.

* I accepted preserving all existing CRUD behaviour and validation rules.

* I accepted keeping overdue logic out of this implementation step.

* I accepted making only small, focused backend changes.



### What I Edited



* I reviewed the generated model changes before applying them.

* I ensured that `due_date` was included consistently in task creation, partial updates, and task responses.

* I confirmed that clearing a due date with `due_date: null` worked correctly.

* I adjusted the implementation where needed to match the existing project structure and coding style.

* I ran the backend test suite after the change and confirmed that the existing functionality remained intact.



### What I Rejected



* I rejected adding overdue calculations during this step because they were planned for a later implementation stage.

* I rejected any frontend changes because this step was limited to the backend.

* I rejected unrelated refactoring or rewriting complete files.

* I rejected introducing a database or changing the existing in-memory storage architecture.

* I rejected changes to the existing status-transition business rules.



\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_





2 – Frontend: Add Due Date Support


## Prompt


### 2 – Frontend: Add Due Date Support


This includes:



* Add a date picker to the Create/Edit modal.

* Send `due_date` to the backend.

* Display the due date on task cards.

* Allow editing and clearing the due date.



### Prompt:



I am continuing Feature 1 (Due Dates + Overdue Filter) for my existing FastAPI Task Tracker.



Current state:



* Backend supports an optional due\_date field using the YYYY-MM-DD format.

* Tasks can be created, updated, and cleared with due\_date: null.

* All 22 backend tests pass.

* Frontend is vanilla HTML, CSS, and JavaScript in frontend/index.html.

* The frontend already has New Task and Edit Task modal flows.

* Existing Kanban rendering, priority sorting, drag-and-drop, validation, and error handling must remain unchanged.



Task:



Add basic due-date support to the frontend.



Requirements:



1. Add an optional date input to the existing New/Edit Task modal.

2. When creating a task, include due\_date in the request:



&#x20;  * Send the selected YYYY-MM-DD value when provided.

&#x20;  * Send null when the field is empty.

3. When editing a task, prefill the date input with the task’s existing due\_date.

4. Allow the user to change or clear the due date while editing.

5. Display the due date on a task card only when one exists.

6. Cards without a due date must not show an empty placeholder.



Constraints:



* Modify only frontend/index.html.

* Inspect the existing modal, submit handler, edit flow, and card-rendering sections before changing them.

* Make small, focused edits only.

* Do not rewrite the entire file.

* Do not add overdue logic, overdue styling, or an overdue filter yet.

* Do not modify the backend.

* Preserve all existing frontend behavior.



Before editing:



* Explain which specific sections or functions need changes.



Verification:



* Explain how to manually verify:



&#x20; 1. Create a task with a due date.

&#x20; 2. Create a task without a due date.

&#x20; 3. Edit a task and change its due date.

&#x20; 4. Edit a task and clear its due date.

&#x20; 5. Confirm existing drag-and-drop and modal behavior still work.



---



# AI Response Summary



The AI first inspected the existing frontend implementation before suggesting any code changes. It identified the modal form, form submission handler, edit task workflow, and task card rendering as the only sections requiring modification. Rather than rewriting the file, it proposed making small, isolated changes that integrated seamlessly with the existing codebase.



The implementation added an optional date picker to the Create and Edit Task modal, submitted the selected `due_date` to the backend in `YYYY-MM-DD` format (or `null` when empty), prefilled the existing value during editing, and displayed the due date on task cards only when one was present. The AI also provided manual verification steps to ensure the new functionality worked correctly while confirming that drag-and-drop, validation, sorting, and modal behavior remained unchanged.



---



# What I Accepted



* Added an optional date picker to the existing Create/Edit Task modal.

* Sent the selected `due_date` to the backend in `YYYY-MM-DD` format.

* Sent `null` when the due date field was left empty.

* Prefilled the due date when editing an existing task.

* Allowed users to modify or remove an existing due date.

* Displayed the due date on task cards only when a due date existed.

* Preserved all existing Kanban functionality, including drag-and-drop, priority sorting, validation, loading state, and error handling.

* Followed the requirement of making only small, focused frontend changes.



---



# What I Edited



* Corrected the original prompt during development from `DD-MM-YYYY` to `YYYY-MM-DD` so it matched the backend implementation.

* Reviewed the generated frontend changes before applying them.

* Ensured the new date input integrated with the existing modal instead of creating a separate workflow.

* Verified that cards without a due date displayed no placeholder or empty label.

* Confirmed that existing frontend behavior remained unchanged after implementation.



---



# What I Rejected



* Implementing overdue calculations in JavaScript.

* Adding overdue styling or an overdue filter during this step.

* Modifying backend code, since backend support had already been completed.

* Rewriting large portions of `frontend/index.html`.

* Refactoring unrelated frontend code that was outside the scope of this implementation step.



\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_



# 3 — Backend Overdue Logic First



## Prompt



I am continuing Feature 1 (Due Dates + Overdue Filter) for my existing FastAPI Task Tracker.



Current state:



* Backend supports an optional due\_date field using Python’s date type.

* Tasks can be created, updated, and cleared with due\_date.

* All 22 backend tests pass.

* Frontend can already create, edit, clear, and display due dates.

* Existing CRUD behavior and status-transition rules must remain unchanged.



Task:



Add backend support for determining whether a task is overdue.



Overdue rule:



* A task is overdue only when:



&#x20; * it has a due\_date,

&#x20; * the due\_date is earlier than the current calendar date,

&#x20; * and the task status is not Done.

* A task due today is not overdue.

* Done tasks must never be overdue.



Requirements:



1. Add a boolean overdue field to the task response model.

2. The backend must calculate overdue instead of storing it.

3. Include overdue in task responses for create, list, and update operations.

4. Keep due\_date stored as YYYY-MM-DD.

5. Add focused backend tests for:



&#x20;  * past-due ToDo task returns overdue: true,

&#x20;  * past-due InProgress task returns overdue: true,

&#x20;  * past-due Done task returns overdue: false,

&#x20;  * task due today returns overdue: false,

&#x20;  * future task returns overdue: false,

&#x20;  * task without due_date returns overdue: false.



Constraints:



* Do not modify the frontend yet.

* Do not store overdue in the in-memory task dictionary.

* Do not change existing status-transition rules.

* Do not introduce databases, background jobs, notifications, or other out-of-scope features.

* Make only the minimum required backend changes.

* Do not rewrite entire files.

* Reuse the existing project style and test fixtures.



Before editing:



* Inspect the current models, storage, and route handlers.

* Explain which files and functions need changes.

* Explain how overdue will be calculated without being stored.



Verification:



* Run the relevant backend tests.

* Report the final number of passing tests.

* Explain any production-code change separately before applying it.



---



# AI Response Summary



The AI inspected the current response model, storage structure, and route handlers before recommending any changes. It proposed adding an `overdue` boolean to the response model while keeping the stored task dictionary unchanged.



The overdue value was calculated dynamically whenever a task response was created. The calculation checked whether the task had a due date, whether that date was earlier than the current calendar date, and whether the task status was not `Done`. This ensured that tasks due today were not considered overdue and completed tasks never appeared as overdue.



The AI also proposed focused backend tests for each overdue scenario and preserved the existing CRUD endpoints, validation rules, and status-transition business logic.



# What I Accepted



* Added an `overdue` boolean field to the task response model.

* Calculated overdue dynamically instead of storing it.

* Used the current calendar date when evaluating overdue status.

* Treated a task as overdue only when its due date was in the past and its status was not `Done`.

* Ensured tasks due today were not overdue.

* Ensured completed tasks were never overdue.

* Included `overdue` in create, list, and update responses.

* Added focused backend tests covering past, present, future, completed, and missing due-date cases.

* Preserved the existing CRUD behavior and status-transition rules.



# What I Edited



* Reviewed the proposed production-code changes before applying them.

* Ensured the overdue calculation was centralized in the response-building flow rather than repeated across endpoints.

* Verified that the raw in-memory task dictionary contained only stored fields and did not contain `overdue`.

* Checked that every endpoint rebuilt the response so the overdue value remained current.

* Removed or avoided duplicate overdue tests when similar test cases were generated more than once.

* Confirmed that existing tests continued to pass after adding the new overdue tests.



# What I Rejected



* Storing the `overdue` value in the in-memory task dictionary.

* Calculating overdue in the frontend.

* Adding background jobs to update overdue values.

* Introducing a database, notifications, or scheduling features.

* Changing the existing status-transition rules.

* Rewriting entire backend files or refactoring unrelated code.

* Applying production-code changes before reviewing the explanation and proposed implementation.



\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\__



# 4 — Frontend: Display the Overdue Indicator



## Prompt

I am continuing Feature 1 (Due Dates + Overdue Filter) for my existing Task Tracker.



Current state:



* The backend now returns a derived boolean field named `overdue` on every task response.

* The frontend already supports creating, editing, clearing, and displaying due dates.

* No overdue indicator exists yet.



Task:

Display the overdue status returned by the backend.



Requirements:



1. Inspect the current task-card rendering before making changes.

2. If `task.overdue` is true, display a small red "Overdue" pill on the task card.

3. Place the overdue pill next to the existing Due Date pill.

4. Do not calculate overdue in JavaScript.

5. Use only the value returned by the backend (`task.overdue`).

6. If `task.overdue` is false, show nothing.

7. Keep the existing Due Date pill unchanged.

8. Add only the minimal CSS needed to style the overdue pill.

9. Keep the existing Kanban layout unchanged.



Constraints:



* Modify only frontend/index.html.

* Do not modify the backend.

* Do not change drag-and-drop, sorting, modal behavior, filtering, or validation.

* Make the smallest possible change.

* Do not rewrite unrelated code.



Before editing:



* Explain which CSS block and which task-card rendering section will change.



Verification:

Explain how to manually verify:



1. A past-due ToDo task displays the Overdue pill.

2. A past-due InProgress task displays the Overdue pill.

3. A past-due Done task does not display the Overdue pill.

4. A future task does not display the Overdue pill.

5. A task without a due date does not display the Overdue pill.



## AI Response Summary



The AI inspected the existing task-card rendering logic and identified the section responsible for displaying due-date information. It proposed adding a small conditional UI element that would render only when `task.overdue` was `true`.



The implementation reused the `overdue` value already calculated by the backend and did not duplicate the overdue business rule in JavaScript. It also added only the minimum CSS required for a red “Overdue” pill and preserved the existing Due Date pill and Kanban layout.



## What I Accepted



* Displayed a red “Overdue” pill when `task.overdue` was `true`.

* Placed the overdue indicator next to the existing Due Date pill.

* Used only the backend-provided `task.overdue` value.

* Displayed nothing when `task.overdue` was `false`.

* Kept the existing Due Date pill unchanged.

* Added only minimal CSS for the new indicator.

* Preserved the existing Kanban layout and frontend behaviour.

* Verified the indicator using past-due, completed, future, and undated tasks.


## What I Edited


* Reviewed the existing task-card rendering section before applying the generated change.

* Adjusted the generated markup where necessary so the new pill matched the structure and style of the existing Due Date pill.

* Confirmed that the indicator was conditional and did not leave an empty placeholder.

* Ensured that no overdue calculation was added to the frontend.

* Kept the modification limited to `frontend/index.html`.



## What I Rejected



* Calculating overdue in JavaScript.

* Recreating the backend overdue business rule in the frontend.

* Modifying the backend.

* Changing drag-and-drop, sorting, modal behavior, filtering, or validation.

* Rewriting unrelated card-rendering or CSS code.

* Adding the overdue filter during this step.



\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\__



# 5 — Overdue Filter



## Prompt



I am continuing Feature 1 (Due Dates + Overdue Filter) for my existing Task Tracker.



Current state:



* The backend already computes and returns a derived boolean field named `overdue`.

* The frontend already displays:



&#x20; * Due Date

&#x20; * Overdue pill

* Drag-and-drop now correctly updates the local task object using the full backend response.

* Existing Kanban behavior, sorting, validation, loading, empty state, error state, and modal flows all work correctly.



Task:

Add an Overdue filter to the frontend.



Requirements:



1. Add a simple filter control above the Kanban board.

2. Filter options:



&#x20;  * All Tasks (default)

&#x20;  * Overdue Only

3. When "All Tasks" is selected:



&#x20;  * Display all tasks exactly as before.

4. When "Overdue Only" is selected:



&#x20;  * Display only tasks where `task.overdue === true`.

5. Do not calculate overdue in JavaScript.

6. Use only the backend-provided `task.overdue` field.

7. Filtering should happen only in the frontend.

8. Do not call the backend again when changing the filter.

9. Keep task counts accurate for the tasks currently being displayed.

10. Empty columns should still be visible even when no overdue tasks exist.



Constraints:



* Modify only frontend/index.html.

* Do not modify the backend.

* Do not change drag-and-drop behavior.

* Do not change sorting.

* Do not change modal behavior.

* Do not change validation.

* Make the smallest possible change.

* Reuse the existing renderBoard() flow where appropriate.

* Do not rewrite unrelated code.



Before editing:

Explain:



* where the filter state will be stored,

* how renderBoard() will use it,

* which HTML section will be updated.



Verification:

Explain how to manually verify:



1. Default view shows every task.

2. Switching to "Overdue Only" displays only overdue tasks.

3. Tasks that become non-overdue immediately disappear from the filtered view after drag-and-drop to Done.

4. Switching back to "All Tasks" restores every task.

5. Empty columns remain visible.

6. No additional backend requests are made when changing the filter.



## AI Response Summary



The AI proposed adding a small filter control above the Kanban board and storing the selected filter in frontend state. The existing rendering flow would then use the current filter value to determine which tasks should be displayed.



For “All Tasks,” the board would render the complete task list. For “Overdue Only,” it would render only tasks where `task.overdue === true`. The filtering would remain entirely client-side and would not send another request to the backend when the user changed the filter.



The AI also preserved accurate visible task counts, kept empty Kanban columns displayed, and ensured that tasks which became non-overdue after being moved to `Done` disappeared immediately from the filtered view.



## What I Accepted



* Added an Overdue filter above the Kanban board.

* Added the options “All Tasks” and “Overdue Only.”

* Used “All Tasks” as the default selection.

* Stored the selected filter in frontend state.

* Filtered tasks using only the backend-provided `task.overdue` field.

* Kept overdue filtering entirely in the frontend.

* Reused the existing board-rendering flow.

* Kept visible task counts accurate.

* Preserved empty columns even when no overdue tasks existed.

* Avoided additional backend requests when switching the filter.

* Updated the filtered board immediately after drag-and-drop changes.



## What I Edited



* Reviewed how `renderBoard()` obtained and displayed tasks before applying the generated change.

* Integrated the filter into the existing rendering flow instead of creating a separate board-rendering function.

* Ensured that the displayed counts were calculated from the filtered task list rather than the full task list.

* Confirmed that moving an overdue task to `Done` updated the local task object using the full backend response.

* Ensured the filtered view refreshed immediately after task changes.

* Preserved the existing loading, error, sorting, modal, and empty-state behaviours.



## What I Rejected



* Calling the backend again whenever the Overdue filter changed.

* Calculating overdue in JavaScript.

* Storing a separate frontend overdue value.

* Hiding empty Kanban columns.

* Changing drag-and-drop, sorting, modal behaviour, or validation.

* Modifying the backend.

* Refactoring unrelated frontend code.

* Rewriting the entire rendering system.



\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\__





# Feature 2 – 1: Backend Assessment for Task Search and Combined Filters



## Prompt:

Inspect the current FastAPI backend before making any changes.



Feature requirements:



* Search tasks by title, description, or assignee.

* Search must be case-insensitive.

* Search must work together with the existing overdue filter.

* The original task data must remain unchanged.

* No unnecessary API requests.



Tasks:



1. Inspect the current GET /tasks endpoint, models, and storage.

2. Decide whether this feature requires backend changes or can remain frontend-only.

3. Explain your reasoning based on the current architecture and project scope.

4. Identify any backend risks or limitations.

5. Do not modify any files yet.



## AI Response Summary



The AI inspected the existing `GET /tasks` endpoint, task models, and in-memory storage before suggesting any implementation changes. It evaluated whether search and combined filtering should be performed entirely in the frontend or supported by the backend.



The AI concluded that search by title, description, and assignee should be added to the backend through optional query parameters. This would keep filtering logic centralized, allow the API to return only matching tasks, and make the feature easier to test independently.



It also recommended keeping the existing Overdue filter on the frontend because the backend already returned the derived `overdue` value. This produced a mixed approach: search, status, and priority filtering would be handled by the backend, while overdue filtering would remain client-side.



## What I Accepted



* Inspected the current backend before making any changes.

* Reviewed the `GET /tasks` endpoint, models, and in-memory storage.

* Chose backend-supported search instead of frontend-only search.

* Kept the original stored task data unchanged.

* Preserved `overdue` as a derived response field.

* Kept the existing Overdue filter as a frontend filter.

* Limited the proposed backend change to the task-list endpoint.

* Identified null assignee handling and combined filters as important edge cases.

* Required the backend search to be case-insensitive.

* Avoided implementation changes until the assessment was reviewed.



## What I Edited



* Clarified that backend search would later work with Status and Priority filters, not only the Overdue filter.

* Confirmed that the frontend Overdue filter would be applied after receiving the backend response.

* Limited the backend scope to optional query parameters on `GET /tasks`.

* Reviewed the proposed architecture before moving to the implementation prompt.

* Ensured that no files were modified during this assessment step.



## What I Rejected



* Implementing the complete feature before inspecting the existing backend.

* Keeping all search and filtering logic entirely in the frontend.

* Modifying the original task records during search or filtering.

* Adding unnecessary API requests for the frontend-only Overdue filter.

* Changing POST, PATCH, or DELETE endpoints.

* Introducing pagination, a database, authentication, or unrelated refactoring.

* Applying code changes before reviewing the assessment and implementation plan.



\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\__



# Feature 2 – Backend Step 2: Extend `GET /tasks` for Search and Combined Status + Priority Filters



Adding Priority and status dropdowns:

Proper Prompt:

Feature 2 – Backend Step 1: Extend GET /tasks for search and combined Status + Priority filters.

Inspect the current backend first before making any changes.



Files to inspect:



* app/main.py

* app/storage.py

* app/models.py

* existing backend tests



Requirements (follow exactly):



* Extend GET /tasks to support optional query parameters:



&#x20; * search

&#x20; * status

&#x20; * priority

* Search must be case-insensitive.

* Search must match title, description, and assignee.

* Handle null assignee safely.

* Status and Priority filters must each work independently.

* Search, Status, and Priority must all work together in the same request (combined filtering).

* Keep the stored task data unchanged.

* Continue computing the overdue field in the response only.

* Reuse the existing Status and Priority enums.

* Preserve all existing endpoint behaviour.

* Do not modify POST, PATCH, DELETE, models, or unrelated code.

* Do not modify the frontend yet.

* Do not add pagination, sorting, databases, authentication, or refactoring.



Testing requirements:



* Search by title.

* Search by description.

* Search by assignee.

* Case-insensitive search.

* Filter by status.

* Filter by priority.

* Combined status + priority.

* Combined search + status.

* Combined search + priority.

* Combined search + status + priority.

* No matches returns HTTP 200 with an empty list.

* Invalid status returns HTTP 422.

* Invalid priority returns HTTP 422.

* Existing backend tests must continue to pass.



Before making any changes, explain:



1. What the backend currently supports.

2. Exactly which files need to change.

3. How the combined filtering logic will work.

4. Any edge cases or risks.

&#x20;  Do not apply any changes until after showing the explanation and proposed diff.



## AI Response Summary



The AI inspected the current backend structure and focused on the existing `GET /tasks` route, the task storage layer, the task models, and the current test suite. It determined that the feature could be implemented by extending the list endpoint with three optional query parameters: `search`, `status`, and `priority`.



The proposed filtering process applied each active condition to the task list without changing the stored task data. Search was made case-insensitive and checked the task title, description, and assignee, while safely handling tasks whose assignee was `null`. Status and Priority reused the existing enums, which allowed FastAPI to return validation errors automatically for invalid values.



The AI also proposed focused tests for every individual filter, several combined-filter cases, empty results, invalid enum values, and regression coverage for the existing backend functionality. No frontend or unrelated endpoint changes were included.



## What I Accepted



* Extended only `GET /tasks` with optional `search`, `status`, and `priority` query parameters.

* Used case-insensitive matching for search.

* Searched across title, description, and assignee.

* Handled a missing or `null` assignee safely.

* Allowed Status and Priority filters to work independently.

* Allowed Search, Status, and Priority to work together using combined filtering.

* Reused the existing Status and Priority enums.

* Kept the stored task data unchanged.

* Continued calculating `overdue` only when building task responses.

* Preserved the existing behaviour of POST, PATCH, and DELETE.

* Added focused tests for individual and combined filters.

* Accepted HTTP 200 with an empty list when no tasks matched.

* Accepted HTTP 422 for invalid Status or Priority values.

* Reviewed the proposed explanation and diff before applying changes.



## What I Edited



* Reviewed the order and placement of the filtering logic so it remained clear and consistent with the existing route handler.

* Ensured optional query parameters were ignored when they were not provided.

* Confirmed that search did not fail when `assignee` was `null`.

* Kept the response-building flow responsible for adding the derived `overdue` field.

* Avoided changing the Pydantic models because the existing enums and response models already supported the required behaviour.

* Reviewed the generated tests and removed or avoided unnecessary duplication.

* Confirmed that existing backend tests still passed together with the newly added filter tests.



## What I Rejected



* Implementing the filters in POST, PATCH, or DELETE.

* Modifying task models unnecessarily.

* Mutating or replacing the original in-memory task records during filtering.

* Calculating or storing `overdue` as part of the filter logic.

* Modifying the frontend during this backend step.

* Adding pagination or new sorting behaviour.

* Introducing a database or authentication.

* Refactoring unrelated backend code.

* Applying generated changes before first reviewing the explanation and proposed diff.



\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\__





# Feature 2 – 3 Frontend Combined Filter Implementation



## Proper Prompt



Context:

The backend has already been updated and tested.



GET /tasks now supports the following optional query parameters:



* search

* status

* priority



The backend implementation is complete and must not be modified.



Task:

Update only the frontend (index.html) to use the backend filtering.



Requirements:



1. Add a Status dropdown to the filter bar.

&#x20;  Options:



* All Statuses (default)

* ToDo

* InProgress

* Done



2. Add a Priority dropdown to the filter bar.

&#x20;  Options:



* All Priorities (default)

* Low

* Medium

* High



3. Modify fetchTasks() so it sends only the selected query parameters to:

&#x20;  GET /tasks



Examples:



* /tasks

* /tasks?search=alice

* /tasks?status=InProgress

* /tasks?priority=High

* /tasks?search=alice&status=InProgress&priority=High



Do not send parameters whose value is "All" or empty.



4. Keep the existing Overdue filter exactly as a client-side filter after the backend response is received.



5. Add a 300 ms debounce to the Search textbox so the backend is not called on every keystroke.



6. Preserve all existing functionality:



* Kanban board

* Drag and drop

* Modal create/edit

* Overdue badge

* Priority sorting

* Loading state

* Error state

* Empty columns



Constraints:



* Do NOT modify the backend.

* Do NOT refactor unrelated code.

* Make the smallest possible changes.

* Reuse existing variables and functions whenever reasonable.

* Keep the code readable and consistent with the current project.



Before applying:

Show the proposed diff and explain every change.

Do not apply anything until I review it.



## AI Response Summary



The AI inspected the existing frontend filter bar, `fetchTasks()` function, board-rendering flow, and event handlers before proposing changes. It recommended adding Status and Priority dropdowns and constructing the `GET /tasks` request dynamically so that only active search and filter values were sent to the backend.



The backend response would then be stored in the existing task list, while the Overdue filter would continue to operate locally using the backend-provided `task.overdue` field. This preserved the separation between backend search, Status and Priority filtering, and frontend-only overdue filtering.



The initial AI proposal included a 300 ms debounce for the Search input. During later testing and refinement, this was removed so search requests were sent immediately as the user typed. The rest of the existing Kanban, modal, sorting, loading, error, and drag-and-drop behaviour remained unchanged.



## What I Accepted



* Added a Status dropdown with:



&#x20; * All Statuses

&#x20; * ToDo

&#x20; * InProgress

&#x20; * Done

* Added a Priority dropdown with:



&#x20; * All Priorities

&#x20; * Low

&#x20; * Medium

&#x20; * High



* Updated `fetchTasks()` to send optional `search`, `status`, and `priority` query parameters.

* Sent only parameters with active values.

* Did not send empty values or options representing “All.”

* Kept the Overdue filter as a frontend-only filter after receiving backend results.

* Reused the existing task list and board-rendering flow.

* Preserved the Kanban board, drag-and-drop, modal flows, overdue badge, priority sorting, loading state, error state, and empty columns.

* Reviewed the proposed diff before applying the generated frontend changes.

* Kept all implementation changes inside `frontend/index.html`.



## What I Edited



* Removed the 300 ms debounce from the Search input during later refinement.

* Changed search to execute immediately while the user typed.

* Ensured every search input change called the backend with the currently selected Status and Priority values.

* Reused the existing filtering and rendering helpers instead of introducing a separate rendering system.

* Ensured the Overdue filter was applied only after the backend response was received.

* Confirmed that query parameters were encoded and combined correctly.

* Updated the current board view after creating, editing, deleting, or moving a task.

* Verified that filtered empty columns remained visible.

* Kept the implementation consistent with the final project behaviour rather than the original debounce requirement.



## What I Rejected



* The final use of a 300 ms debounce.

* Delaying search results after the user typed.

* Sending query parameters whose values were empty or represented “All.”

* Moving the existing Overdue filter to the backend.

* Modifying the backend after it had already been completed and tested.

* Refactoring unrelated frontend code.

* Rewriting the existing Kanban rendering flow.

* Adding pagination, advanced search, authentication, or database features.

* Applying the generated changes before reviewing the proposed diff and explanation.



\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\__




# Weak Prompt → Proper Prompt Examples

## Example 1 – Backend Assessment → Backend Implementation (Feature 2)


### Weak Prompt


**Feature 2 – 1: Backend assessment for task search and combined filters.**



Inspect the current FastAPI backend before making any changes.



Feature requirements:



* Search tasks by title, description, or assignee.

* Search must be case-insensitive.

* Search must work together with the existing overdue filter.

* The original task data must remain unchanged.

* No unnecessary API requests.



Tasks:



1. Inspect the current GET /tasks endpoint, models, and storage.

2. Decide whether this feature requires backend changes or can remain frontend-only.

3. Explain your reasoning based on the current architecture and project scope.

4. Identify any backend risks or limitations.

5. Do not modify any files yet.


### Why it was weak



Although this prompt encouraged architectural thinking, it did not define how the feature should be implemented. It focused on assessing the current backend rather than providing concrete implementation requirements. It also did not specify which endpoint should be modified, what parameters should be added, how combined filtering should behave, or how the feature should be tested.


### Proper Prompt



**Feature 2 – Backend: Extend GET /tasks for search and combined Status + Priority filters.**



*(Insert your full proper prompt exactly as written.)*



### Why it was stronger



* Identified the exact endpoint to modify (`GET /tasks`).

* Specified the files to inspect before implementation.

* Clearly defined the required query parameters.

* Specified case-insensitive search behaviour.

* Required support for combined search, Status, and Priority filtering.

* Reused the existing enums and response model.

* Included comprehensive testing requirements.

* Added implementation constraints to prevent unnecessary changes.

* Required reviewing the explanation and proposed diff before applying code changes.



### Reflection



Initially, I believed this feature might remain entirely on the frontend. After reviewing the existing architecture, I realised that backend filtering would produce a cleaner API, simplify the frontend, and support combined filtering more effectively. Refining the prompt resulted in a more precise implementation plan and reduced unnecessary iterations.



---



# Example 2 – Missing Status and Priority Filters



### Initial Prompt



The initial implementation focused primarily on **search** functionality. At that stage, the prompt did not explicitly require backend support for **Status** and **Priority** filtering.



### Why it was incomplete



Although the search functionality was clearly described, the prompt overlooked two important filtering requirements that the final feature needed:



* Status filtering

* Priority filtering



Without these requirements, the backend implementation would not fully support the combined filtering expected by the frontend.



### Refined (Proper) Prompt



The prompt was revised to explicitly require:



* Optional `search`, `status`, and `priority` query parameters.

* Independent Status and Priority filters.

* Combined Search + Status + Priority filtering.

* Additional backend validation and test cases.

* Preservation of the existing API behaviour.



### Why it was stronger



The refined prompt fully described the required backend behaviour instead of focusing only on search. It ensured that all filter combinations were supported, aligned the backend with the frontend requirements, and added explicit testing expectations. This reduced ambiguity and produced a more complete implementation.



### Reflection



While reviewing the feature, I realised that implementing search alone would not satisfy the intended user experience because users also needed to filter tasks by Status and Priority. Updating the prompt before implementation ensured that all filtering behaviour was designed together rather than being added incrementally later.



-----------------------------------------------------------------------------------------------------------------------------------------------------------------------



Overall Project Verification



Each implementation step documented in this prompt log followed the same workflow: inspect, implement, review, functional testing, regression testing, and refinement. Before proceeding to the next step, the generated code was reviewed to ensure it met the project requirements while remaining within the defined project scope.



-----------------------------------------------------------------------------------------------------------------------------------------------------------------------










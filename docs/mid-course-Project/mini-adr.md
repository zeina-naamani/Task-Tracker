\# Mini Architecture Decision Record (ADR)



\## Title



Implementation Decisions for the Mid-Course Project Features



\## Status



Accepted



\## Context



The Mid-Course Project required extending the existing FastAPI Task Tracker application by implementing two new features while preserving the project's simple architecture and existing design.



The implemented features were:



\- Due Dates and Overdue Detection

\- Search and Combined Filters



Throughout development, AI suggested multiple implementation approaches. Each suggestion was reviewed before deciding whether it aligned with the project requirements and learning objectives.



\---



\# Decision 1 – Due Dates and Overdue Detection



\## Decision



An optional `due\_date` field was added to the task model. The backend calculates the `overdue` value whenever task data is returned instead of storing it as part of the task.



\## Why This Decision Was Made



The overdue status depends on:



\- the current date,

\- the task's due date,

\- and the task's status.



Calculating the value dynamically keeps the stored task data simple and prevents outdated or inconsistent information.



\## AI Alternative Considered



The AI initially suggested storing an `overdue` field inside every task.



\## Why It Was Rejected



A stored value could become outdated whenever the date changes or a task's status changes. Calculating it in the backend guarantees that the value is always accurate without requiring additional update logic.



\---



\# Decision 2 – Search and Combined Filters



\## Decision



Searching and filtering were implemented by extending the existing `GET /tasks` endpoint with optional query parameters for search, status, and priority.



The frontend sends only the active filter values, while the backend performs the filtering and returns the matching tasks.



\## Why This Decision Was Made



Keeping the filtering logic in the backend provides a single source of truth, avoids duplicating business logic in the frontend, and allows multiple filters to be combined consistently through a single API request.



\## AI Alternative Considered



The AI initially suggested implementing search entirely in the frontend after retrieving all tasks.



\## Why It Was Rejected



Frontend searching would require downloading all tasks before filtering and would duplicate logic that belongs in the API. Performing the filtering in the backend results in a cleaner and more maintainable design.



\---



**# AI Suggestions Rejected as Too Complex or Out of Scope**



During development, AI suggested several additional ideas that were intentionally not implemented because they exceeded the scope of the Mid-Course Project or conflicted with previous project decisions.



\### Feature-specific suggestions



\- Storing the `overdue` value instead of calculating it dynamically.

\- Calculating the overdue status in the frontend instead of the backend.

\- Implementing searching entirely in the frontend.

\- Keeping a debounce delay for search requests instead of updating results immediately while typing.



\### Project-level suggestions



\- Using a database instead of the project's in-memory storage.

\- Adding authentication and authorization.

\- Implementing advanced search features such as fuzzy or full-text search.

\- Adding pagination for large task lists.

\- Implementing real-time updates using WebSockets or notifications.



These ideas could improve a production application, but they were intentionally excluded to keep the project focused on the required learning objectives, maintain a simple architecture, and remain within the defined project scope.


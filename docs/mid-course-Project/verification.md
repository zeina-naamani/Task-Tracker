**# Verification**



**## 1. Baseline Check**



Before implementing Feature 1 (Due Dates and Overdue Support) and Feature 2 (Search and Combined Filtering), the application was verified to establish a stable baseline. This ensured that all subsequent changes could be measured against a known working version of the project.



\### Existing Functionality



The baseline application included:



\- Task CRUD operations (Create, Read, Update, Delete)

\- Kanban board with three status columns

\- Drag-and-drop task movement

\- Business rule validation for task status transitions

\- Modal dialog for creating and editing tasks

\- Priority sorting within each column

\- Loading state while retrieving tasks

\- Error state when the backend was unavailable

\- Empty-column rendering

\- In-memory task storage

\- REST API implemented using FastAPI



\### Existing Backend Tests



Prior to implementing the new features, the existing backend test suite was executed to confirm that the application was in a working state.



Verification included:



\- Existing API endpoint tests

\- Business rule validation tests

\- Model validation tests

\- CRUD operation tests



\*\*Result:\*\* Existing backend tests passed successfully before feature implementation.



\### Initial Behaviour



At the start of implementation:



\- Tasks did not support due dates.

\- Overdue indicators did not exist.

\- Search functionality was unavailable.

\- Status and Priority filtering were unavailable.

\- The frontend always retrieved the complete task list.



This baseline established a reference point for regression testing after each implementation step.



\---



**# 2. Backend Test Results**



Backend verification was performed throughout development using the existing FastAPI test suite together with newly added tests for implemented features.



\## Existing Test Suite



The existing automated backend tests were executed before implementing each major feature to confirm that previously completed functionality remained stable.



Areas covered included:



\- CRUD endpoints

\- Model validation

\- Business rules

\- Response validation

\- Error handling



\## New Tests



Additional backend tests were introduced where appropriate to verify new functionality, including:



\- Due date support

\- Overdue calculation

\- Search functionality

\- Status filtering

\- Priority filtering

\- Combined filtering behaviour



\## Regression Testing



After completing each implementation step, regression testing was performed to ensure that previously implemented behaviour continued to function correctly.



Regression verification included:



\- Existing endpoints

\- Existing validation rules

\- Existing frontend interactions

\- Business rule enforcement



\## Overall Backend Verification



Backend verification confirmed that:



\- Existing functionality remained operational.

\- Newly implemented features behaved as expected.

\- Existing API behaviour was preserved.

\- Validation continued to operate correctly.



\*\*Pytest Result:\*\* All backend tests passed successfully.

======================================= 42 passed in 0.66s ======================================= 



\---



**# 3. Swagger API Verification**



Swagger UI (OpenAPI) was used throughout development to manually verify backend behaviour before frontend integration.



The following API operations were verified.



| Verification Item | Status |

|-------------------|--------|

| GET /tasks | ✔ Verified |

| POST /tasks | ✔ Verified |

| PATCH /tasks/{id} | ✔ Verified |

| DELETE /tasks/{id} | ✔ Verified |

| Search query parameter | ✔ Verified |

| Status query parameter | ✔ Verified |

| Priority query parameter | ✔ Verified |

| Combined query parameters | ✔ Verified |

| Response models | ✔ Verified |

| HTTP status codes | ✔ Verified |

| Validation errors | ✔ Verified |



*Verification included:*



\- Correct request parameters

\- Correct response structure

\- Correct response values

\- Validation of optional query parameters

\- Invalid enum handling

\- Empty result responses

\- Existing endpoint behaviour remained unchanged



\---



**# 4. Manual Browser Verification**



The frontend application was manually tested after each implementation step.



| Feature | Verified |

|----------|----------|

| Kanban Board Rendering | ✔ |

| Create Task | ✔ |

| Edit Task | ✔ |

| Delete Task | ✔ |

| Drag and Drop | ✔ |

| Due Date Display | ✔ |

| Overdue Badge | ✔ |

| Search | ✔ |

| Status Filter | ✔ |

| Priority Filter | ✔ |

| Combined Filters | ✔ |

| Loading State | ✔ |

| Error State | ✔ |

| Empty Columns | ✔ |

| Priority Sorting | ✔ |



Manual verification confirmed that the frontend continued to behave correctly after integrating each new feature.



Regression testing was also performed after every completed implementation step to verify that existing functionality remained unaffected.



\---



**# 5. Browser Developer Tools Verification**



Browser Developer Tools were used throughout implementation to inspect frontend behaviour and communication with the backend.



Verification included:



\### Network Tab



\- Verified HTTP requests were sent correctly.

\- Verified only active query parameters were included.

\- Verified query strings matched selected filters.

\- Verified backend responses.

\- Verified HTTP status codes.



\### Console



\- Checked for JavaScript runtime errors.

\- Confirmed no unexpected console errors during normal application usage.



\### Frontend Behaviour



Developer Tools were used to confirm:



\- Search requests were generated correctly.

\- Status and Priority filters produced the expected requests.

\- Combined filters generated the expected query string.

\- Overdue filtering continued to operate on the frontend after receiving backend responses.



\---



**# 6. Behaviour Contract Verification**



\## Before Refactor



Before implementing the new features, the behaviour contract included:



\- Three Kanban columns with task counts

\- Priority sorting

\- Loading state

\- Empty-column rendering

\- Error state

\- Valid drag-and-drop updates

\- Invalid drag operations reverted correctly

\- Modal create/edit workflow



\## After Refactor



After implementing Feature 1 and Feature 2, the behaviour contract was re-verified.



The following behaviours were confirmed to remain unchanged:



\- Kanban board rendering

\- Drag-and-drop functionality

\- Modal create/edit workflow

\- Priority sorting

\- Loading state

\- Error state

\- Empty-column rendering

\- Existing business rules



***Additional behavior successfully verified included:***



\- Due date support (backend and frontend)

\- Overdue badge and frontend overdue filtering

\- Backend search

\- Frontend search functionality

\- Backend Status filtering

\- Frontend Status filter integration

\- Backend Priority filtering

\- Frontend Priority filter integration

\- Combined backend filtering

\- Combined frontend filter integration



Regression testing confirmed that introducing the new functionality did not negatively impact previously implemented behaviour.



\------------------------------------------------------



**# 7. Break Testing**



Break testing (negative and edge-case testing) was performed throughout development to verify that the application remained stable when functionality was intentionally disrupted. After each test, the original implementation was restored and the expected behaviour was re-verified.



\---



**## Break Test 1 – Frontend Overdue Filter Logic**



**\*\*Objective\*\***



Verify that the application remains stable when the frontend overdue filter intentionally returns no matching tasks.



**\*\*Steps\*\***



1\. Temporarily modified the frontend overdue filter logic:

&#x20;  

&#x20;  return tasks.filter((task) => false);

&#x20;  

2\. Reloaded the application.

3\. Selected \*\*Filter → Overdue Only\*\*.

4\. Observed the application behaviour.

5\. Restored the original implementation:

&#x20;  

&#x20;  return tasks.filter((task) => task.overdue === true);

&#x20;  

6\. Re-tested the \*\*Overdue Only\*\* filter.



**\*\*Expected Result\*\***



\- The application should not crash.

\- All three Kanban columns should remain visible.

\- No task cards should be displayed while the modified filter is active.

\- After restoring the original implementation, overdue tasks should display correctly.



**\*\*Actual Result\*\***



* The application remained stable throughout the test. 
* All three Kanban columns remained visible, no task cards were displayed while the modified filter was active, and restoring the original implementation immediately restored the expected overdue filtering behaviour.



\*\*Status\*\*



\*\*PASS\*\*



\---



**## Break Test 2 – Frontend Search Logic:**



**\*\*Objective\*\***



Verify that the application behaves safely when the frontend search condition intentionally returns no matching tasks.



**\*\*Steps\*\***



1\. Temporarily modified the frontend search logic:

&#x20;  return false;

2\. Reloaded the application.

3\. Performed a search.

4\. Observed the application behaviour.

5\. Restored the original search implementation:

&#x20;  title.includes(query) ||

&#x20;  description.includes(query) ||

&#x20;  assignee.includes(query)

6\. Re-tested the search functionality.



**\*\*Expected Result\*\***



\- No task cards should be displayed.

\- All three Kanban columns should remain visible.

\- All column counters should become zero.

\- The application should not crash or display runtime errors.

\- Restoring the original implementation should immediately restore normal search functionality.



**\*\*Actual Result\*\***



* The application behaved as expected. 
* No task cards were displayed, all three Kanban columns remained visible, all counters became zero, no runtime errors occurred, and restoring the original implementation immediately restored normal search functionality.



\*\*Status\*\*



\*\*PASS\*\*



\---



**## Break Test 3 – Backend Status Filter Request**



\*\*Objective\*\*



Verify that the frontend correctly sends the selected Status filter to the backend by constructing the expected API request.



\*\*Steps\*\*



1\. Temporarily modified the frontend request-building logic to prevent the Status query parameter from being added:

&#x20;  if (false \&\& activeStatusFilter !== 'all')

2\. Selected a Status filter in the application.

3\. Observed the generated request using the browser Developer Tools (Network tab).

4\. Restored the original implementation.

5\. Re-tested the Status filter.



\*\*Expected Result\*\*



\- The generated request should not contain the Status query parameter while the modified code is active.

\- The generated request should not include the Status query parameter, and the browser Network tab should confirm that the parameter is absent from the request.

\- After restoring the original implementation, the request should again include the selected Status value (for example, `GET /tasks?status=InProgress`).



\*\*Actual Result\*\*



* The modified implementation generated requests without the Status query parameter (`GET /tasks`). 
* Developer Tools confirmed the regression by showing the missing parameter. 
* After restoring the original implementation, requests correctly included the selected Status parameter (for example, `GET /tasks?status=InProgress`), confirming that the frontend correctly constructed backend requests.



\*\*Status\*\*



\*\*PASS\*\*



\------------------------------------------------------------------------------------------------------------------------------------------------------------



**# 8. Overall Verification Summary**



Each implementation step followed the same structured workflow:



\- Inspect

\- Implement

\- Review

\- Functional Testing

\- Regression Testing

\- Refinement



Before proceeding to the next step, the generated code was reviewed to ensure it met the project requirements while remaining within the defined project scope.



Verification activities included:



\- Automated backend testing using the existing pytest suite.

\- Manual API verification using Swagger/OpenAPI.

\- Functional testing of frontend features.

\- Regression testing after every completed implementation step.

\- Browser Developer Tools inspection of requests, responses, query parameters, and console output.

\- Break testing using invalid and edge-case scenarios.



The verification process confirmed that the implemented features behaved as expected while preserving existing functionality. 

Throughout development, issues identified during testing were resolved before continuing to the next implementation step, resulting in a stable and fully integrated final implementation.










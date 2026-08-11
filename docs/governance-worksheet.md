# Module 5 Governance Worksheet

## 1. What I Shared with AI

| # | Item shared | Risk | Reason | Safer future version | Ambiguity to resolve |
|---:|---|---|---|---|---|
| 1 | Task Tracker requirements and scope | Low | Course-project requirements contained no evidenced secrets, PII, or proprietary logic. | Share a concise requirements summary without unrelated institutional details. | None material. |
| 2 | User stories, acceptance criteria, and business rules | Low | Ordinary business rules for a course Task Tracker. | Share only the acceptance criteria relevant to the current task. | None material. |
| 3 | Backend source and implementation | Medium | Complete source exposes implementation details if the repository is private. | Share only the relevant route, model, or storage excerpt. | Whether the repository was public and authorized for sharing. |
| 4 | Frontend source and implementation | Medium | The complete frontend exposes more implementation detail than most questions require. | Share only the relevant HTML or JavaScript function. | Whether the repository was public and authorized for sharing. |
| 5 | Automated tests and behavior | Medium | Tests reveal expected behavior, edge cases, and internal assumptions. | Share only the relevant test, fixture, and sanitized result. | Whether the tests were already public. |
| 6 | Repository structure and development configuration | Medium | Complete structure and configuration reveal internal development context. | Provide a reduced file tree and only relevant dependencies or commands. | Whether the repository material was public. |
| 7 | Architecture and design documentation | Medium | ADRs and technical notes can expose non-public reasoning and rejected alternatives. | Summarize the relevant decision, constraints, and outcome. | Whether the documentation was public or course-internal. |
| 8 | Prompts and AI-assisted development records | Medium | Prompt logs can expose development history, mistakes, and unrelated contextual information. | Share only the necessary sanitized prompt excerpt. | Whether the records contained additional personal or institutional details. |
| 9 | Terminal output and development logs | Medium | Logs may expose local paths, usernames, IDs, and environment details. | Share only relevant lines after removing paths, identifiers, and environment values. | Whether every shared log was fully sanitized. |
| 10 | Screenshots of the running Task Tracker | Medium | Although task data was synthetic, some screenshots exposed local paths, terminal details, or development-environment information. | Crop screenshots and remove or obscure local paths, terminal details, and unrelated screen content. | None; exposure of local development details is established. |
| 11 | Swagger/API request and response evidence | Low | Requests used synthetic task data, random assignee names, and local Task Tracker IDs. | Continue using synthetic values and omit local IDs when unnecessary. | None; the data is confirmed synthetic and local. |
| 12 | Security-review source/configuration context | Medium | Security and configuration details expose a potentially private security posture and system assumptions. | Share only relevant configuration lines and state the local course scope. | Whether the repository was public. |
| 13 | Manual security/governance observations | Low | These were course-project design suggestions and a documentation defect, not sensitive operational information. | Share categorized observations without unrelated context. | None material. |
| 14 | Git/repository history evidence | Medium | History can reveal authors, development chronology, mistakes, and abandoned approaches. | Share only relevant hashes, paths, and summarized conclusions. | Whether the repository history was public. |
| 15 | Docker and CI configuration | Medium | Build and workflow details can expose repository identifiers and operational assumptions. | Share only relevant steps with repository and account identifiers removed. | Whether the configuration was public. |
| 16 | Course/project documentation | Medium | Complete documentation may contain non-public course context and verification history. | Share only the necessary section after removing local and institutional details. | Whether the documentation was public or authorized for redistribution. |

### Important business-rule context

- `ToDo → InProgress`: allowed
- `InProgress → Done`: allowed
- `Done → InProgress`: allowed
- Same-status updates: allowed as no-ops
- `ToDo → Done`: rejected
- `InProgress → ToDo`: rejected
- `Done → ToDo`: rejected

### Git-history clarification

Git history was reviewed after AI-generated documentation incorrectly claimed that a frontend “Delete Task” feature existed and had been manually browser-verified. The history confirmed that Delete existed only in the backend/API and was tested through Swagger using the task ID; no frontend Delete functionality had ever been implemented.

### Final totals

- Low: 4
- Medium: 12
- High: 0

No High-risk sharing was evidenced. The main lesson is to minimize context, sanitize logs and screenshots, and confirm whether repository material is public/private and authorized before sharing complete source or internal documentation.

## 2. Medium-item governance-habit prioritization

| Priority | Item | Current risk | Habit to change | Why change this habit first | Concrete future practice |
|---:|---|---|---|---|---|
| 1 | Terminal output and logs | Medium | Sanitize logs | Logs commonly expose paths, usernames, IDs, environment details, or accidental secrets. | Share only relevant lines and remove local identifiers, headers, paths, and environment values. |
| 2 | Screenshots | Medium | Crop and sanitize screenshots | Images can unintentionally expose terminal details, paths, notifications, and unrelated screen content. | Crop tightly, use synthetic data, and inspect the entire visible image before sharing. |
| 3 | AI-development records | Medium | Minimize prompt context | Prompt records can combine code, decisions, mistakes, and personal or institutional context. | Share only the necessary prompt excerpt after removing unrelated history and identifiers. |
| 4 | Backend source | Medium | Share minimal code excerpts | This reduces implementation disclosure while preserving necessary technical context. | Provide only the relevant function, model, and smallest required dependencies. |
| 5 | Frontend source | Medium | Share minimal code excerpts | Complete frontend files reveal more implementation detail than most questions require. | Extract only the relevant HTML, JavaScript, and surrounding context. |
| 6 | Security-review context | Medium | Limit configuration exposure | Combined security details can reveal system assumptions and weaknesses. | Share only the relevant sanitized configuration lines. |
| 7 | Git history | Medium | Remove identities and unrelated history | Repository history may disclose authors, mistakes, chronology, and abandoned work. | Provide only relevant commit hashes, paths, and conclusions. |
| 8 | Docker and CI configuration | Medium | Sanitize operational configuration | Workflow files may expose repository identifiers and operational assumptions. | Share relevant stages or steps with account and repository identifiers replaced. |
| 9 | Architecture documentation | Medium | Summarize decisions | Complete ADRs may reveal unnecessary internal reasoning and alternatives. | Share the relevant decision, constraints, and outcome. |
| 10 | Tests and test behavior | Medium | Share focused tests | Full test suites reveal extensive behavior and edge cases. | Share only the relevant test, fixture, and sanitized output. |
| 11 | Course/project documentation | Medium | Extract relevant sections | Complete documents may expose unrelated course and verification context. | Paste only the necessary section after removing local details. |
| 12 | Repository structure and configuration | Medium | Reduce structural disclosure | Full trees and environment information are rarely necessary for a bounded question. | Provide a trimmed file tree and only relevant dependencies or commands. |

### Top three habits

1. Sanitize terminal output and logs.
2. Crop and inspect screenshots before sharing.
3. Share only the minimum code, prompt, and contextual information necessary.

## 3. What I Received from AI

To be completed in the next Part 5.3 step.

# Part 5.3B — AI-Generated Code Ownership Trace

## Selected AI-generated code block

The selected block is `submitTask()` from `frontend/index.html`.

This block was selected because it contains meaningful frontend/API behavior, including form handling, validation, payload construction, POST and PATCH requests, HTTP error handling, and UI refresh behavior.

```javascript
      async function submitTask() {
        clearModalErrors();

        const title = document.getElementById('task-title').value.trim();
        const description = document.getElementById('task-description').value.trim();
        const status = document.getElementById('task-status').value;
        const priority = document.getElementById('task-priority').value;
        const assignee = document.getElementById('task-assignee').value.trim();
        const dueDate = document.getElementById('task-due-date').value;

        // Validation
        if (!title) {
          showFieldError('title', 'Title is required');
          return;
        }

        const payload = {
          title: title,
          description: description === '' ? '' : description, // null not included here
          status: status,
          priority: priority,
          assignee: assignee === '' ? null : assignee,
          due_date: dueDate === '' ? null : dueDate
        };

        try {
          let response;
          if (modalState.mode === 'create') {
            response = await fetch(`${BASE_URL}/tasks`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(payload)
            });
          } else if (modalState.mode === 'edit') {
            response = await fetch(`${BASE_URL}/tasks/${modalState.taskId}`, {
              method: 'PATCH',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(payload)
            });
          }

          if (!response.ok) {
            if (response.status === 422) {
              const errorData = await response.json().catch(() => ({}));
              if (errorData.detail && Array.isArray(errorData.detail)) {
                // FastAPI validation error format: array of errors
                errorData.detail.forEach(err => {
                  if (err.loc && err.loc[1]) {
                    const field = err.loc[1];
                    showFieldError(field, err.msg);
                  } else {
                    showModalError(err.msg || 'Validation error');
                  }
                });
              } else if (errorData.detail) {
                showModalError(errorData.detail);
              } else {
                showModalError('Server validation failed');
              }
              return;
            } else {
              const errorData = await response.json().catch(() => ({}));
              showModalError(errorData.detail || `Server error: ${response.status}`);
              return;
            }
          }

          // Success: close modal and refresh board
          closeModal();
          await fetchTasks();
        } catch (error) {
          console.error('Request error:', error);
          showModalError('Network error. Please try again.');
        }
      }
```

## Line-by-line ownership trace

| Line(s) | What it does | Why it is there | What could break | Do I own this yet? |
|---|---|---|---|---|
| 987 | Declares the asynchronous `submitTask()` function. `async` permits the function to use `await` and means it returns a Promise. | Submitting and refreshing tasks involve operations that finish later. | Removing `async` would make the `await` expressions invalid JavaScript. | Understood: `async` is required because this function uses `await`. |
| 988 | Calls `clearModalErrors()` to remove messages left by a previous submission attempt. | Old errors, such as “Title is required,” should not remain after the user corrects the form and tries again. | Without it, stale validation messages could remain visible even when they are no longer accurate. | Needs surrounding-helper verification: the purpose is understood, but the exact elements cleared depend on `clearModalErrors()`. |
| 990–995 | Reads title, description, status, priority, assignee, and due date from the form. Text inputs are trimmed. | These values are needed to validate the form and construct the API payload. Trimming prevents surrounding spaces and makes a whitespace-only title empty. | Missing or renamed element IDs would make `getElementById()` return `null`, causing `.value` to fail. | Understood, with the assumption that all referenced control IDs exist. |
| 997–1001 | Checks for a blank title, displays a title-field error, and exits with `return`. | The title is required, and the request must stop when it is missing. | Without `return`, the code would display the error but still submit the invalid form. | Understood: the error is shown and `return` prevents submission. |
| 1003–1010 | Builds a payload containing title, description, status, priority, assignee, and due date. | The form values must be collected into an object matching the API’s expected fields. | Incorrect property names or types could produce validation errors. During editing, sending every field can replace stored values that the user did not intend to change. | Understood, subject to verifying the payload fields against the backend request models. |
| 1004 | Places the value from the `title` variable into the payload property named `title`. | The backend expects a `title` field. | Changing the property name would break the API contract. | Understood: the left side is the property name and the right side is the variable value. |
| 1005 | Keeps an empty description as `''`; otherwise it uses the entered description. The current source comment notes that `null` is not included here. | The code represents “no description” as an empty string rather than `null`. | Changing it to `null` could fail if the backend does not accept a nullable description. The conditional is otherwise redundant because both outcomes preserve the description string. | Understood, with backend nullability still requiring model verification. |
| 1006–1007 | Adds the selected status and priority to the payload. | Both values are required for task creation and are also included during editing. | Values that do not match the backend enums could return HTTP 422. Sending status during PATCH can also invoke transition validation. | Understood, assuming the form options match the backend enum values. |
| 1008–1009 | Converts blank assignee and due-date values to `null`; otherwise it sends their current values. | The code represents an absent optional value as JSON `null` instead of an empty string. | This would fail if the backend did not allow either field to be nullable. | Understood: `condition ? null : value` means “send null if empty; otherwise send the value.” |
| 1012–1013 | Starts the `try` block and declares a shared `response` variable. | Create and edit requests use different branches but share the same response-handling code. | If neither mode assigns `response`, line 1028 would try to read `.ok` from `undefined`. | Needs verification that `modalState.mode` can only be `create` or `edit`. |
| 1014–1019 | In create mode, sends a POST request to `${BASE_URL}/tasks` with a JSON body. | POST `/tasks` is the API operation used to create a task. | An incorrect URL, method, header, or payload would prevent creation or cause an HTTP error. | Understood, assuming `BASE_URL` and the backend route are configured as expected. |
| 1017–1018 | Declares that the request body is JSON and serializes the JavaScript payload using `JSON.stringify(payload)`. | A plain JavaScript object must be converted into JSON text before it is sent in the request body. | Without serialization or the correct content type, the backend might not parse the body correctly. | Understood: `JSON.stringify()` converts the JavaScript object into JSON request text. |
| 1020–1025 | In edit mode, sends a PATCH request to the URL containing `modalState.taskId`. | PATCH updates the task identified by the task ID. | A missing or incorrect ID could return 404 or target the wrong task. | Understood, assuming the task ID is correctly stored when the edit modal opens. |
| 1021–1024 | Sends the complete current form payload in the PATCH request, not only the field that changed. | The edit form supplies all displayed task values to one shared payload. | Unchanged, stale, or default form values could replace saved values even if the user intended to change only one field. | Understood: changing only the title still sends description, status, priority, assignee, and due date. |
| 1028 | Checks `response.ok` to determine whether the HTTP response status is successful. | `fetch()` does not reject merely because the server returns HTTP 422 or 500; those are completed HTTP responses and must be checked explicitly. | Without this check, HTTP error responses would continue through the success path. It also fails if `response` was never assigned. | Understood: HTTP error responses and rejected requests are different cases. |
| 1029–1030 | Detects HTTP 422 and attempts to parse the response body as JSON. If JSON parsing fails, it uses `{}`. | FastAPI uses 422 for validation failures, and parsing the body may provide useful error details. The fallback prevents a parsing failure from replacing the original handling path. | Without the fallback, an empty or invalid JSON body would throw and reach the outer catch. | Understood: `errorData` becomes `{}` when the body cannot be parsed, while the HTTP status remains 422. |
| 1031–1040 | Checks for FastAPI’s array-style validation details and processes each error. | A request can contain multiple field-validation errors. | A different response structure or nested location may not map correctly to a frontend field. | Needs verification against the actual FastAPI error shapes and field-name mapping. |
| 1034–1036 | Uses `err.loc[1]` as the field name and displays `err.msg` beside that field. | FastAPI body errors commonly use locations such as `['body', 'title']`. | Nested errors, query errors, or API names such as `due_date` may not map to the expected frontend control. | Needs verification that `showFieldError()` supports every possible backend field name. |
| 1037–1039 | Displays a modal-level validation message when an error cannot be mapped to a field. | Non-field or unexpectedly structured validation errors still need visible feedback. | Without this fallback, some validation errors could be invisible to the user. | Understood. |
| 1041–1045 | Handles a non-array `detail` value or displays “Server validation failed” when no detail exists. | Business-rule errors may use a single detail message rather than an array. | Unexpected detail types might display poorly; without the fallback, the user might receive no explanation. | Understood, with the possible detail types still requiring verification. |
| 1046 | Exits after handling the 422 response. | The modal must remain open so the user can correct the form. | Without this `return`, the code would continue to the success path and close the modal. | Understood. |
| 1047–1051 | Handles other unsuccessful HTTP responses by parsing their JSON and displaying either `detail` or a status-based fallback. | Errors such as 404 and 500 are not ordinary field-validation failures. | Without the return, an unsuccessful response would be treated as success. Displaying raw server detail could also be inappropriate if it exposed internal information. | Understood, with server error-detail exposure requiring verification. |
| 1054–1056 | After a successful response, closes the modal and waits for `fetchTasks()` to refresh the board. | The saved task should appear in the current board state. | Without refreshing, the board could remain stale. If refreshing fails after saving, the outer catch may display a network-error message even though the save succeeded. | Understood, with `fetchTasks()` failure behavior requiring surrounding-code verification. |
| 1057–1060 | Handles rejected Promises and other exceptions thrown inside the `try`, logs the technical error, and displays a general network message. | The user needs feedback when the request or another awaited/thrown operation fails. | Removing it could leave failures unhandled. The message can be inaccurate because the catch can also receive programming errors or a failed board refresh. | Understood: an unreachable backend is one example, but network failure is not the only possible cause. |

## Three critical ownership checks

### Check 1 — PATCH sends the complete payload

**Question:**  
If the user changes only the title, which other fields will this PATCH request still send and potentially overwrite?

**My answer:**  
“Even if I change only the title, the PATCH request still sends all the form fields with their current values, including description, status, priority, assignee, and due date. Empty assignee and due-date fields are sent as `null`. Therefore, this PATCH sends the full form payload rather than only the field that changed.”

### Check 2 — HTTP errors versus catch(error)

**Question:**  
Why does an HTTP 422 or 500 response not automatically enter the outer `catch` block?

**My answer:**  
“JavaScript does not go to `catch(error)` for HTTP 422 or 500 because the backend was reached and returned a response, even though it was an error response. `catch(error)` is used when the request itself fails, such as when the backend/Uvicorn cannot be reached.”

**Technical clarification:**  
The outer catch can also receive other exceptions or rejected Promises thrown inside the `try`; an unreachable backend is a clear example, not the only possible cause.

### Check 3 — JSON parsing fallback

**Question:**  
What value does `errorData` receive when the server’s 422 response body is empty or not valid JSON?

**My answer:**  
“If the 422 response body is empty or cannot be read as valid JSON, `errorData` becomes an empty object `{}`, so there are no error details/descriptions available from `errorData`. The HTTP status is still 422.”

## Ownership conclusion

This exercise demonstrates ownership of the selected AI-generated block by explaining its full-payload PATCH behavior, the difference between HTTP error responses and rejected or thrown failures, FastAPI validation-error handling, and the JSON parsing fallback. Some assumptions about surrounding helpers, field mapping, modal state, and refresh behavior remain identified for verification rather than being claimed as independently verified.

# Part 5.3C — Personal AI Usage Rules

## 1. Personal AI Usage Rules

| Rule category | Draft rule | Evidence from my notes | What is still vague? | Revised rule |
|---|---|---|---|---|
| What I will never paste | I will never paste complete or unsanitized project material when a smaller sanitized excerpt is sufficient. | Complete backend/frontend files expose unnecessary details. Logs may expose paths, usernames, IDs, and environment details. Screenshots exposed local development information. Prompt logs and Git history may contain unrelated context or identities. Repository visibility and sharing authorization must be checked. | “Project material” is broad, and the notes do not establish a category that must never be shared under every circumstance. | I will never paste unreviewed logs, screenshots, prompt records, or Git history. Before sharing, I will remove local paths, usernames, IDs, environment details, author identities, and unrelated context. I will share only the relevant code or documentation excerpt after confirming that the repository material is authorized for sharing. |
| What I will always verify before accepting | I will verify AI claims against the repository before accepting them. | AI documentation incorrectly claimed that frontend Delete was browser-verified; code and Git history disproved it. The ownership trace also identified assumptions requiring checks of helper functions, field mapping, modal state, `fetch()` behavior, and refresh behavior. | “Verify against the repository” does not specify what evidence must be checked or what happens when verification is incomplete. | Before accepting an AI claim or generated block, I will check the relevant source code, tests, Git history, or documented library behavior. I will confirm the claimed behavior and identify any assumptions. If the required evidence is unavailable, I will mark the claim as needing verification instead of recording it as fact. |
| How I will record AI contributions | I will document AI-generated work and the checks I performed. | The worksheet records the selected AI-generated block, source file, line-by-line trace, assumptions requiring verification, ownership questions, student answers, technical clarification, and correction of an inaccurate AI claim. Git evidence is limited to relevant hashes, paths, and conclusions. | The notes do not establish one mandatory storage location or a format that must be used for every future contribution. Missing - add course evidence for a fixed location. | For each AI contribution I keep, I will record the affected file or code block, the AI’s contribution, the evidence I used to verify it, assumptions that still need verification, and any correction or rejected claim. I will distinguish my own answer from later technical clarification and include only sanitized, relevant Git evidence. The required storage location is: Missing - add course evidence. |

## 2. Future-scenario rule test

This optional follow-up tests whether each revised rule produces a clear decision in a future scenario supported by the governance worksheet.

| Rule category | Future scenario | Decision from rule | Clear yes/no? | Reason |
|---|---|---|---|---|
| What I will never paste | I am about to paste terminal output containing a local path, username, task ID, and unrelated log lines without sanitizing it. | No—do not paste it. Remove the identifiers and unrelated lines first. | Yes | The rule explicitly prohibits sharing unreviewed logs and lists the details that must be removed. |
| What I will always verify | AI claims that a frontend feature was implemented and browser-verified, but I have not checked the source code, tests, documentation, or Git history. | No—do not accept the claim yet. Check the available repository evidence or mark it as needing verification. | Yes | The rule defines both the required verification and what to do when evidence is unavailable. |
| How I will record AI contributions | I keep an AI-generated code block but record only the final code, without its source location, verification evidence, remaining assumptions, or corrected AI claims. | No—the record is incomplete. Add the affected file/block, contribution, evidence, assumptions, and corrections. | Mostly yes | The required record contents are clear. However, the rule still cannot determine where the record must be stored because that remains “Missing - add course evidence”. |

## 3. Short conclusion

- Rule 1 gives a clear decision about unsanitized sharing.
- Rule 2 gives a clear decision about accepting unverified AI claims.
- Rule 3 clearly defines what information must be recorded, but the required storage location remains unsupported by the current worksheet evidence.
- Do not invent a storage location. Preserve “Missing - add course evidence” until supporting course evidence is provided.

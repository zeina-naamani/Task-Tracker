# Comments on Tasks — Repo-Grounded Feature Plan

## 1. Data Model

The comment schemas will live in `app/models.py`, beside `TaskCreate`, `TaskUpdate`, and `TaskResponse`. This follows the current flat structure: Pydantic request and response models are kept in that file, while the reserved `app/schemas/` package remains unused ([app/models.py](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/app/models.py:29), [AGENTS.md](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/AGENTS.md:35)).

This feature will not move routes, models, or storage into the empty reserved packages. Any such reorganization requires a separate architecture decision.

### `CommentCreate`

The request model will accept:

| Field | Type | Validation |
|---|---|---|
| `author` | string | Required; trim surrounding whitespace; reject whitespace-only values; require 1–100 characters after trimming |
| `body` | string | Required; trim surrounding whitespace; reject whitespace-only values; require 1–2,000 characters after trimming |

Follow the existing input-model convention by using `extra="forbid"`. Unknown request fields will return HTTP 422, consistent with `TaskCreate` and `TaskUpdate` ([app/models.py](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/app/models.py:29)).

The client will not provide:

- `id`
- `task_id`
- `created_at`

If supplied in the request body, these fields will be rejected rather than accepted or trusted.

### `CommentResponse`

The response model will contain:

| Field | Type | Source |
|---|---|---|
| `id` | string | Server-generated UUID |
| `task_id` | string | Copied from the task ID in the route |
| `author` | string | Trimmed and validated request value |
| `body` | string | Trimmed and validated request value |
| `created_at` | datetime | Server-generated timezone-aware UTC datetime |

The existing storage layer generates IDs with `str(uuid4())` and timestamps with `datetime.now(timezone.utc)`. Comments will follow those conventions ([app/storage.py](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/app/storage.py:31)).

UTC remains the stored and server-returned reference time. Browser-local conversion applies only when displaying the timestamp.

### `CommentListResponse`

The list route will use a lightweight paginated response:

| Field | Type | Meaning |
|---|---|---|
| `items` | list of `CommentResponse` | The current page of comments |
| `offset` | integer | Number of ordered comments skipped |
| `limit` | integer | Maximum comments requested for this page |
| `has_more` | boolean | Whether another page exists after the returned page |

This envelope lets the single-file frontend determine whether to display a **Load more** control without requesting every comment at once.

### Storage shape

Comments will use a separate module-level collection in `app/storage.py`.

Planned shape:

- Key: comment UUID string.
- Value: comment data containing `id`, `task_id`, `author`, `body`, and `created_at`.
- `task_id` is an application-level task reference.

The repository has no database or foreign-key enforcement. Its persistence mechanism is a module-level dictionary whose contents are lost on restart ([app/storage.py](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/app/storage.py:7), [README.md](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/README.md:157)).

The storage layer will need operations to:

- create a comment for an existing task;
- list comments belonging to one task;
- sort comments by `created_at` ascending;
- use `id` as a deterministic tie-breaker;
- apply `offset` and `limit` after sorting;
- determine whether more comments remain;
- remove all comments associated with a deleted task;
- clear comments through the test-reset mechanism.

Comments will not be embedded in task dictionaries or `TaskResponse`.

### Duplicate-request records

Use a small in-memory idempotency-key collection for backend duplicate prevention.

For each accepted comment-creation request, record:

- task ID;
- idempotency key;
- normalized author;
- normalized body;
- created comment ID.

This is internal request-deduplication metadata, not part of `CommentResponse`.

The mapping will:

- exist only in memory;
- be cleared by `storage._reset()`;
- be cleared for a task when that task is deleted;
- disappear on backend restart, like all other application data.

This remains proportional to the repository and introduces no database, external cache, distributed lock, authentication, or infrastructure service.

Authentication remains outside scope, so `author` stays validated free text ([AGENTS.md](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/AGENTS.md:79)).

## 2. API Routes

The initial feature supports only:

- creating comments;
- listing comments for a task.

It does not include:

- retrieving one comment independently;
- editing comments;
- deleting individual comments.

Routes will be declared directly in `app/main.py`, following the existing flat route structure ([app/main.py](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/app/main.py:65)).

### Create a comment

**Method and path:** `POST /tasks/{task_id}/comments`

**Required header:** `Idempotency-Key`

The frontend will generate one UUID-shaped idempotency key for each intended comment submission. Retries or repeated submission attempts for that same intended comment will reuse the key.

**Request body:**

| Field | Required | Rules |
|---|---:|---|
| `author` | Yes | Trim before validation; reject whitespace-only values; 1–100 characters after trimming |
| `body` | Yes | Trim before validation; reject whitespace-only values; 1–2,000 characters after trimming |

**New request processing:**

1. Confirm that `task_id` identifies an existing task.
2. Validate and normalize `author` and `body`.
3. Validate that the idempotency header is present and usable.
4. Check whether the task and key combination was previously accepted.
5. Generate a string UUID for the new comment.
6. Generate `created_at` as a timezone-aware UTC datetime.
7. Store the comment and its idempotency record.
8. Return the created comment.

**Success responses:**

- `201 Created` when a new comment is created.
- `200 OK` when the same task, idempotency key, and normalized payload are replayed; return the previously created comment without creating another record.

**Conflict response:**

- `409 Conflict` when the same task and idempotency key are reused with a different normalized author or body.

**Other error cases:**

- `404 Not Found` when the task does not exist.
- `422 Unprocessable Content` when:
  - `author` or `body` is missing;
  - either value is blank after trimming;
  - `author` exceeds 100 characters;
  - `body` exceeds 2,000 characters;
  - an unknown body field is included;
  - the client supplies `id`, `task_id`, or `created_at`;
  - the required idempotency key is missing or invalid.

The task-not-found response will follow the current wording: `Task with id {task_id} not found` ([app/main.py](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/app/main.py:158)).

Frontend button guarding remains useful for user experience, but backend idempotency is the data-integrity control. The backend must not depend only on the button being disabled.

### List comments for a task

**Method and path:** `GET /tasks/{task_id}/comments`

**Query parameters:**

| Parameter | Default | Validation | Meaning |
|---|---:|---|---|
| `offset` | `0` | Integer, minimum `0` | Number of ordered comments to skip |
| `limit` | `20` | Integer, minimum `1`, maximum `100` | Maximum comments returned |

These values keep pagination simple and suitable for an in-memory learning project.

**Processing:**

1. Confirm that the task exists.
2. Retrieve comments matching `task_id`.
3. Sort by `created_at` ascending.
4. Use `id` as a deterministic secondary key.
5. Apply `offset` and `limit`.
6. Determine `has_more`.

**Success response:**

- Status: `200 OK`
- Body: `CommentListResponse`
- An existing task with no comments returns:
  - an empty `items` list;
  - `has_more: false`;
  - the validated offset and limit.

**Error cases:**

- `404 Not Found` when the task does not exist.
- `422 Unprocessable Content` when:
  - `offset` is negative;
  - `limit` is below 1;
  - `limit` exceeds 100;
  - either parameter cannot be parsed as an integer.

Checking task existence ensures that a missing task is not treated as an existing task with no comments.

### Task deletion behavior

When `DELETE /tasks/{task_id}` succeeds:

- remove the task;
- remove all comments belonging to it;
- remove its idempotency-key records.

This is the approved lifecycle rule.

The operation should behave as one logical storage action so the API cannot report successful task deletion while leaving inaccessible comment or request-deduplication records.

The existing response remains:

- `204 No Content` on success;
- `404 Not Found` when the task does not exist.

These current outcomes are visible in [app/main.py](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/app/main.py:285).

## 3. Tests

The existing automated tests use `pytest`, FastAPI’s `TestClient`, direct HTTP requests, descriptive test names, and status/JSON assertions ([tests/conftest.py](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/tests/conftest.py:8), [tests/test_tasks.py](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/tests/test_tasks.py:6)).

Create `tests/test_comments.py` and reuse the existing `client` and `created_task` fixtures.

Update `storage._reset()` to clear:

- tasks;
- comments;
- idempotency-key records.

The autouse fixture already invokes this reset around each test ([tests/conftest.py](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/tests/conftest.py:8), [app/storage.py](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/app/storage.py:164)).

### Happy path

- `test_create_comment_for_existing_task_returns_201_with_full_body`
- `test_create_comment_trims_author_and_body`
- `test_list_comments_for_existing_task_returns_paginated_response`
- `test_list_comments_for_task_with_no_comments_returns_empty_items`
- `test_list_comments_returns_only_comments_for_requested_task`
- `test_list_comments_returns_comments_oldest_first`
- `test_list_comments_uses_id_as_tie_breaker_when_timestamps_match`

Creation assertions should verify:

- UUID-string ID;
- route task ID;
- normalized author and body;
- timezone-aware UTC `created_at`.

### Validation

- `test_create_comment_missing_author_returns_422`
- `test_create_comment_blank_author_returns_422`
- `test_create_comment_whitespace_only_author_returns_422`
- `test_create_comment_author_at_100_characters_returns_201`
- `test_create_comment_author_over_100_characters_returns_422`
- `test_create_comment_missing_body_returns_422`
- `test_create_comment_blank_body_returns_422`
- `test_create_comment_whitespace_only_body_returns_422`
- `test_create_comment_body_at_2000_characters_returns_201`
- `test_create_comment_body_over_2000_characters_returns_422`
- `test_create_comment_unknown_field_returns_422`
- `test_create_comment_client_supplied_id_returns_422`
- `test_create_comment_client_supplied_task_id_returns_422`
- `test_create_comment_client_supplied_created_at_returns_422`
- `test_create_comment_missing_idempotency_key_returns_422`
- `test_list_comments_negative_offset_returns_422`
- `test_list_comments_zero_limit_returns_422`
- `test_list_comments_limit_over_100_returns_422`
- `test_list_comments_non_integer_pagination_returns_422`

Length boundaries must be measured after trimming.

### Pagination

- `test_list_comments_uses_default_offset_zero_and_limit_twenty`
- `test_list_comments_respects_custom_offset_and_limit`
- `test_list_comments_has_more_true_when_additional_comments_exist`
- `test_list_comments_has_more_false_on_final_page`
- `test_list_comments_pages_do_not_repeat_comments`
- `test_list_comments_pages_preserve_oldest_first_order`
- `test_list_comments_offset_past_end_returns_empty_items`

### Duplicate prevention

- `test_create_comment_replayed_with_same_key_and_payload_returns_existing_comment`
- `test_create_comment_replayed_with_same_key_does_not_increase_comment_count`
- `test_create_comment_same_key_with_different_payload_returns_409`
- `test_create_comment_same_payload_with_different_keys_creates_distinct_comments`
- `test_delete_task_removes_comment_idempotency_records`
- `test_storage_reset_clears_comment_idempotency_records`

These tests distinguish accidental request replay from an intentional second comment with the same text.

### Edge cases and integrity

- `test_create_comment_for_missing_task_returns_404_with_detail`
- `test_list_comments_for_missing_task_returns_404_with_detail`
- `test_failed_comment_creation_does_not_store_comment`
- `test_delete_task_removes_its_comments`
- `test_delete_one_task_does_not_remove_other_task_comments`
- `test_storage_reset_clears_comments_between_tests`
- `test_existing_task_endpoints_keep_original_response_shape`
- `test_task_list_response_does_not_include_comments_or_comment_count`
- `test_get_task_response_does_not_include_comments_or_comment_count`

### Frontend manual verification

No automated browser-test framework is visible in the inspected repository. Manually verify:

- the separate Comments modal;
- loading and empty states;
- initial page size;
- Load more behavior;
- oldest-first ordering across pages;
- trimmed input;
- validation errors;
- replay behavior after an uncertain request;
- browser-local timestamp conversion;
- the friendly timestamp display;
- task-board responses remaining unchanged.

Frontend automation would require a separately approved testing decision.

## 4. Frontend Changes

All frontend changes will remain in `frontend/index.html`, which contains the project’s HTML, CSS, and JavaScript without a framework or build step ([README.md](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/README.md:126), [frontend/index.html](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/frontend/index.html:493)).

### Separate Comments modal

Use a separate Comments modal rather than adding comments inside the Edit Task modal.

This isolates:

- selected task state;
- loaded comment pages;
- pagination state;
- comment-form state;
- comment errors;
- idempotency-key state.

It avoids adding more responsibilities to the existing create/edit `modalState`, `openModal()`, `closeModal()`, and `submitTask()` flow ([frontend/index.html](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/frontend/index.html:913)).

### Task-card control

Add a **Comments** button beside the existing Edit button in each task card. Cards are generated in `renderBoard()` and already contain the task ID needed to open the correct comment view ([frontend/index.html](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/frontend/index.html:612)).

### Comments modal contents

The modal will show:

- selected task title;
- loading state;
- empty state;
- load-error state;
- comments ordered oldest first;
- author, body, and displayed timestamp for each comment;
- required author input;
- required body textarea;
- length guidance;
- field and modal errors;
- submit control;
- **Load more** control when `has_more` is true;
- close or cancel control.

### Paginated loading

When the modal opens:

1. Clear comments from the previously selected task.
2. Set `offset` to `0`.
3. Request the first page using `limit=20`.
4. Render returned comments oldest first.
5. Store the next offset as the current offset plus the number of returned items.
6. Show Load more only when `has_more` is true.

When Load more is selected:

1. Request the next page with the stored offset.
2. Append the returned comments without clearing the existing list.
3. Preserve oldest-first order.
4. Update the offset and `has_more`.
5. Prevent concurrent page-load requests.

Comments will be loaded only when the Comments modal is open. The initial board request remains unchanged:

- no comments embedded in `TaskResponse`;
- no comment count;
- no comment requests for every card;
- no change to `fetchTasks()` response shape.

### Comment creation and duplicate protection

For each intended submission, the frontend will:

1. Trim author and body.
2. Validate required values and post-trimming lengths.
3. Generate one idempotency key.
4. Send that key in the `Idempotency-Key` header.
5. Reuse the same key if the same submission must be retried because its outcome is uncertain.
6. Disable or guard the submit control while a request is active.
7. Treat both new creation and a successful replay as success.
8. Generate a new key only for a new intended comment.
9. Preserve entered values on failure.
10. Clear the body and refresh or update the comment list after success.

Frontend guarding improves the user experience, but backend idempotency provides the required integrity protection.

The exact JavaScript syntax and state-variable names remain implementation details and are intentionally not specified in this plan.

### Validation and errors

The modal will:

- show field-level 422 errors where possible;
- show 404, 409, and other errors at modal level;
- explain an idempotency conflict without silently creating another comment;
- retain entered values when submission fails.

### Safe rendering

Render author and body as text or escape them before inserting them into generated markup.

The existing task renderer already uses `escapeHtml()` for task-controlled content, so comments should follow that convention ([frontend/index.html](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/frontend/index.html:561), [frontend/index.html](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/frontend/index.html:637)).

### Timestamp display

The backend-generated `created_at` remains UTC.

For display only, the frontend will:

1. Parse the returned UTC timestamp.
2. Convert it to the browser’s local timezone.
3. Render it in a friendly human-readable format such as `11 Aug 2026, 11:30 PM`.

The displayed value represents the browser’s local timezone. It must not be described as the user’s country time because browser timezone settings and physical location are not necessarily the same.

## 5. Migration Notes

No database migration will be created.

The repository:

- uses in-memory dictionaries;
- loses data on restart;
- explicitly excludes adding a database.

This is supported by [app/storage.py](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/app/storage.py:7), [README.md](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/README.md:157), and [AGENTS.md](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/AGENTS.md:79).

Required runtime data-shape changes:

- Add a separate comments dictionary.
- Add a small idempotency-key dictionary.
- Leave existing task dictionaries unchanged.
- Leave `TaskResponse` unchanged.
- Treat existing tasks as having no comments.
- Clear tasks, comments, and idempotency records in `storage._reset()`.
- Remove a task’s comments and idempotency records when the task is deleted.
- Continue accepting that all runtime data disappears when the backend restarts.

No historical task conversion is required because comments are stored separately.

The CORS configuration already permits:

- GET and POST methods;
- all request headers.

Therefore, the paginated GET route, comment POST route, and `Idempotency-Key` header fit the current local configuration without adding another allowed method or header ([app/main.py](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/app/main.py:29)).

The idempotency guarantee lasts only for the lifetime of the current backend process. That limitation is consistent with the rest of the in-memory application and must be documented rather than represented as durable protection across restarts.

## 6. Open Questions

No unresolved product decision remains for the initial comments feature.

The following are implementation-verification items, not reopened product questions:

- Confirm that repeated requests using the same idempotency key are handled correctly when they arrive close together.
- Confirm that the chosen in-memory update sequence does not create two comments before the key record is visible.
- Confirm that the frontend reuses a key only for retries of the same normalized submission.
- Confirm that pagination does not skip or repeat comments during ordinary sequential use.
- Confirm timestamp formatting in the browsers used for course verification.

These checks do not introduce additional infrastructure or expand the approved scope.

# Files read

- [AGENTS.md](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/AGENTS.md)
- [README.md](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/README.md)
- [app/models.py](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/app/models.py)
- [app/main.py](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/app/main.py)
- [app/storage.py](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/app/storage.py)
- [tests/conftest.py](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/tests/conftest.py)
- [tests/test_tasks.py](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/tests/test_tasks.py)
- [frontend/index.html](D:/AI%20Assisted%20Coding%20Course/Task-Tracker/frontend/index.html)

# Remaining assumptions to verify

No unresolved product assumptions remain for the planned initial scope.

Implementation must still verify:

- correct handling of near-simultaneous requests with one idempotency key;
- correct reuse and reset of frontend idempotency keys;
- stable pagination without repeated or skipped comments during sequential loading;
- browser support and output for the chosen local-time formatting;
- the documented limitation that in-memory idempotency records do not survive backend restarts.

# Human decisions incorporated

1. **Frontend design:** Use a separate Comments modal.
2. **Initial scope:** Support comment creation and task-comment listing only.
3. **Task deletion:** Delete all comments belonging to a deleted task.
4. **Whitespace:** Trim author and body, reject whitespace-only values, and apply length limits after trimming.
5. **Ordering:** Return and display comments oldest first using `created_at` ascending and `id` as a deterministic tie-breaker.
6. **Task responses:** Keep existing task responses and board-fetch payload unchanged; load comments separately.
7. **Module placement:** Keep the flat backend structure in `app/models.py`, `app/main.py`, and `app/storage.py`.
8. **Pagination:** Use lightweight offset/limit loading with a paginated response and Load more behavior.
9. **Duplicate prevention:** Use backend idempotency keys in addition to frontend submit guarding.
10. **Timezone display:** Keep server timestamps in UTC and convert them to browser-local time only for display.
11. **Timestamp format:** Display a friendly value such as `11 Aug 2026, 11:30 PM`.

# Revision summary

## 1. Previous open questions resolved

The following questions are now resolved:

- pagination and expected comment-volume handling;
- stronger duplicate-submission protection;
- UTC versus browser-local display;
- friendly timestamp presentation.

They are now initial feature requirements rather than assumptions.

## 2. Genuinely unresolved questions

No unresolved product question remains for the initial plan.

Only bounded implementation-verification details remain, principally:

- near-simultaneous idempotent request handling;
- frontend key lifecycle;
- sequential pagination correctness;
- browser formatting verification.

## 3. Ready to save?

**Yes.** The plan is ready to save as `docs/decisions/comments-feature-plan.md`.

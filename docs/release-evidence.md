# Final Project Release Evidence

This document records baseline verification performed on the `final-project` branch before Final Project release and documentation changes.

## Baseline Summary

| Check | Result | Evidence |
| --- | --- | --- |
| Backend startup | Pass | Uvicorn started successfully and application startup completed. |
| `GET /health` | Pass | HTTP `200` with the observed response body recorded below. |
| Automated tests | Pass | 44/44 passed; 0 failed; 0 skipped. |
| Frontend serving | Pass | `http://localhost:8080/` returned HTTP `200`. |
| Manual Kanban rendering | Pass | Student manually confirmed the board and all three columns rendered correctly. |
| Create flow | Pass | Student manually created `Testing_Task` and confirmed it appeared. |
| Edit flow | Pass | Student manually edited the task and confirmed the updated card appeared. |

## Backend Verification

Command:

```bash
uvicorn app.main:app --reload --port 8000
```

Uvicorn started successfully on `http://127.0.0.1:8000`, and application startup completed successfully.

`GET /health` returned:

- HTTP status: `200`
- Body: `{"status":"ok","timestamp":"2026-08-17T10:04:31.783805+00:00"}`

The timestamp above is the response observed during this verification run; it is not a fixed expected value.

## Automated Test Verification

Command:

```bash
pytest -v
```

- Total tests: **44**
- Passed: **44**
- Failed: **0**
- Skipped: **0**
- Observed execution time: **0.51 seconds**

The execution time is the observed result of this baseline run, not a guaranteed or expected runtime.

## Frontend Serving Verification

Codex served the unchanged frontend with:

```bash
python -m http.server 8080 --directory frontend
```

Codex verified that `http://localhost:8080/` returned HTTP `200` and that the delivered frontend source contained the existing Kanban UI and create/edit handlers. Codex could not directly perform rendered browser interaction because browser control was unavailable in its environment.

### Student Manual UI Verification

The student manually verified that:

- The Task Tracker loaded correctly in the browser.
- The three Kanban columns appeared: To Do, In Progress, and Done.
- `+ New Task` worked.
- A temporary task named `Testing_Task` was created and appeared on the board.
- The task's existing Edit flow opened.
- The task was edited and saved successfully.
- The updated card appeared correctly.

Supporting backend responses observed during the manual check:

- `GET /tasks` → `200 OK`
- `OPTIONS /tasks` → `200 OK`
- `POST /tasks` → `201 Created`
- `PATCH /tasks/{id}` → `200 OK`
- Subsequent `GET /tasks` → `200 OK`

## Baseline Conclusion

The baseline verification passed: backend startup, `/health`, automated tests (44/44), frontend serving, manual Kanban rendering, task creation, and task editing all passed.

This is baseline evidence captured before later Final Project changes. Later final verification results should be recorded separately rather than replacing or being presented as these baseline results.

## CI Evidence

### CI Configuration Verification by Codex

Codex inspected `.github/workflows/ci.yml`, `requirements.txt`, and `pytest.ini` and confirmed:

- CI triggers on `push` and `pull_request`.
- CI explicitly uses Python `3.11`.
- Dependencies are installed before testing with `pip install -r requirements.txt`.
- CI runs `pytest -v` without a test-path restriction, so the full suite runs.
- A nonzero pytest exit code fails the CI job.

Dangerous-shortcut check:

| Check | Result |
| --- | --- |
| `continue-on-error` | Not Present |
| `\|\| true` | Not Present |
| Skipped or commented-out pytest | Not Present |
| Other test-failure bypasses | Not Present |
| Missing dependency installation | Not Present |
| Vague or unpinned Python setup | Not Present |

Configuration judgment: `CI ready — no changes needed`.

### Student Manual GitHub Actions Verification

Codex could not access the live GitHub Actions run. The student manually opened GitHub Actions and verified the current Final Project run:

- Workflow/run: `docs: add final project baseline evidence`
- Branch: `final-project`
- Commit: `aaa67de` (`aaa67de1b701cb6647c069401d38d95d0e8f259f`)
- Result: **Successful / green**
- Duration shown by GitHub: **19 seconds**

No run URL was provided or recorded.

### Historical Module 4 Fail-and-Recovery Evidence

Separately from the current Final Project run, the student verified this GitHub Actions sequence on the `module-4` branch:

1. `Add GitHub Actions CI workflow` → successful / green.
2. `Deliberately break test for CI verification` → failed / red.
3. `Restore passing test - from 201 back to 200` → successful / green.
4. Later Module 4 CI runs continued to pass.

This demonstrates that the workflow failed when a test was deliberately broken and returned to green after the test was restored. This historical sequence is not the current Final Project CI run.

### CI Conclusion

CI verification passes based on configuration inspection, the absence of dangerous failure-bypass shortcuts, the current successful `final-project` GitHub Actions run verified by the student, and historical fail-and-recovery evidence showing that failing tests can fail CI.


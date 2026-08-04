## CI Verification — Green → Red → Green

### 1. Baseline (green)
- Commit: f518b7c — "Add GitHub Actions CI workflow"
- Date: 2026-08-02 23:40:18 +0300
- Files changed: .github/workflows/ci.yml (new), requirements.txt (pytest + httpx added)
- GitHub Actions run URL: https://github.com/zeina-naamani/Task-Tracker/actions/runs/30766159871
- Result: PASS
- Test count: 44 passed

### 2. Intentional break (red)
- Commit: dd0badb — "Deliberately break test for CI verification"
- Date: 2026-08-02 23:48:41 +0300
- Change: tests/test_tasks.py::test_patch_existing_task_with_valid_due_date_returns_200_and_updates_due_date
  assert response.status_code == 200  →  assert response.status_code == 201
- GitHub Actions run URL: https://github.com/zeina-naamani/Task-Tracker/actions/runs/30766460682
- Result: FAIL
- Failing test: test_patch_existing_task_with_valid_due_date_returns_200_and_updates_due_date

### 3. Restore (green)
- Commit: 1a8696c — "Restore passing test - from 201 back to 200"
- Date: 2026-08-02 23:52:57 +0300
- Change: reverted assert response.status_code == 201 → == 200
- GitHub Actions run URL: https://github.com/zeina-naamani/Task-Tracker/actions/runs/30766621624
- Result: PASS
- Test count: 44 passed

### Conclusion
The CI workflow correctly transitions from PASS → FAIL → PASS in direct response to
a genuine test assertion change, with no failure-masking mechanisms involved
(confirmed line-by-line in Entry 12 of the Module 4 prompt log). This demonstrates
the workflow accurately reports test outcomes rather than always reporting green.

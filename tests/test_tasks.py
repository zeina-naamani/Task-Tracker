from datetime import date, timedelta

import pytest


def test_create_task_valid_returns_201_with_full_body(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Write tests",
            "description": "Module 2 coverage",
            "status": "ToDo",
            "priority": "High",
            "assignee": "alice",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Write tests"
    assert body["description"] == "Module 2 coverage"
    assert body["status"] == "ToDo"
    assert body["priority"] == "High"
    assert body["assignee"] == "alice"
    assert isinstance(body["id"], str)
    assert body["id"]
    assert body["created_at"]
    assert body["updated_at"]


def test_create_task_with_due_date_returns_201_and_stores_due_date(client):
    response = client.post(
        "/tasks",
        json={"title": "Due date task", "due_date": "2026-08-15"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["due_date"] == "2026-08-15"


def test_patch_existing_task_with_valid_due_date_returns_200_and_updates_due_date(
    client,
    created_task,
):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"due_date": "2026-08-15"},
    )

    assert response.status_code == 200
    assert response.json()["due_date"] == "2026-08-15"


def test_patch_existing_task_with_null_due_date_clears_due_date(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Clear due date", "due_date": "2026-08-15"},
    )
    task_id = create_response.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={"due_date": None})

    assert response.status_code == 200
    assert response.json()["due_date"] is None


def test_create_task_with_invalid_due_date_returns_422(client):
    response = client.post(
        "/tasks",
        json={"title": "Bad due date", "due_date": "not-a-date"},
    )

    assert response.status_code == 422


def test_create_task_without_due_date_returns_due_date_null(client):
    response = client.post("/tasks", json={"title": "No due date"})

    assert response.status_code == 201
    assert response.json()["due_date"] is None


@pytest.mark.parametrize(
    ("status", "due_date", "expected_overdue"),
    [
        ("ToDo", (date.today() - timedelta(days=1)).isoformat(), True),
        ("InProgress", (date.today() - timedelta(days=1)).isoformat(), True),
        ("Done", (date.today() - timedelta(days=1)).isoformat(), False),
        ("ToDo", date.today().isoformat(), False),
        ("ToDo", (date.today() + timedelta(days=1)).isoformat(), False),
        ("ToDo", None, False),
    ],
)
def test_create_task_returns_overdue_flag_based_on_due_date_and_status(
    client,
    status,
    due_date,
    expected_overdue,
):
    payload = {"title": "Overdue task", "status": status}
    if due_date is not None:
        payload["due_date"] = due_date

    response = client.post("/tasks", json=payload)

    assert response.status_code == 201
    assert response.json()["overdue"] is expected_overdue


def test_list_and_get_task_return_overdue_flag(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Past task",
            "due_date": (date.today() - timedelta(days=1)).isoformat(),
        },
    )
    task_id = create_response.json()["id"]

    list_response = client.get("/tasks")
    get_response = client.get(f"/tasks/{task_id}")

    assert list_response.status_code == 200
    assert list_response.json()[0]["overdue"] is True
    assert get_response.status_code == 200
    assert get_response.json()["overdue"] is True


def test_create_task_missing_title_returns_422(client):
    response = client.post("/tasks", json={})

    assert response.status_code == 422


def test_create_task_blank_title_returns_422(client):
    response = client.post("/tasks", json={"title": "   "})

    assert response.status_code == 422


def test_create_task_invalid_priority_returns_422(client):
    response = client.post("/tasks", json={"title": "Valid title", "priority": "Whatever"})

    assert response.status_code == 422


def test_create_task_unknown_field_returns_422(client):
    response = client.post("/tasks", json={"title": "Valid title", "unknown": "field"})

    assert response.status_code == 422


def test_list_tasks_empty_returns_200_and_empty_list(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(client):
    client.post("/tasks", json={"title": "Open task", "status": "ToDo"})

    response = client.get("/tasks", params={"status": "Done"})

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_priority_returns_only_matches(client):
    client.post("/tasks", json={"title": "Low task", "priority": "Low"})
    client.post("/tasks", json={"title": "High task", "priority": "High"})
    client.post("/tasks", json={"title": "Another high task", "priority": "High"})

    response = client.get("/tasks", params={"priority": "High"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert all(task["priority"] == "High" for task in body)


def test_get_task_by_id_returns_task(client, created_task):
    response = client.get(f"/tasks/{created_task['id']}")

    assert response.status_code == 200
    assert response.json() == created_task


def test_get_task_by_id_not_found_returns_404_with_detail(client):
    missing_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/tasks/{missing_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == f"Task with id {missing_id} not found"


def test_patch_partial_update_keeps_other_fields(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"title": "updated title"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "updated title"
    assert body["description"] == created_task["description"]
    assert body["status"] == created_task["status"]
    assert body["priority"] == created_task["priority"]
    assert body["assignee"] == created_task["assignee"]
    assert body["id"] == created_task["id"]
    assert body["created_at"] == created_task["created_at"]
    assert body["updated_at"] != created_task["updated_at"]


def test_patch_not_found_returns_404(client):
    missing_id = "00000000-0000-0000-0000-000000000000"
    response = client.patch(f"/tasks/{missing_id}", json={"title": "nope"})

    assert response.status_code == 404
    assert response.json()["detail"] == f"Task with id {missing_id} not found"


def test_patch_valid_transition_todo_to_inprogress_returns_200(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "InProgress"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"


def test_patch_invalid_transition_todo_to_done_returns_422(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "Done"},
    )

    assert response.status_code == 422
    assert "Invalid status transition from ToDo to Done" in response.json()["detail"]


def test_patch_same_status_returns_200(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "ToDo"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "ToDo"


def test_delete_existing_returns_204_no_body(client, created_task):
    response = client.delete(f"/tasks/{created_task['id']}")

    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_returns_404(client):
    missing_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f"/tasks/{missing_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == f"Task with id {missing_id} not found"


def test_list_tasks_search_by_title_returns_only_matches(client):
    client.post("/tasks", json={"title": "Fix login bug"})
    client.post("/tasks", json={"title": "Write docs"})

    response = client.get("/tasks", params={"search": "login"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["title"] == "Fix login bug"


def test_list_tasks_search_by_description_returns_only_matches(client):
    client.post("/tasks", json={"title": "Task A", "description": "Refactor endpoint docs"})
    client.post("/tasks", json={"title": "Task B", "description": "Update UI styles"})

    response = client.get("/tasks", params={"search": "endpoint"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["title"] == "Task A"


def test_list_tasks_search_by_assignee_returns_only_matches(client):
    client.post("/tasks", json={"title": "Task A", "assignee": "Alice"})
    client.post("/tasks", json={"title": "Task B", "assignee": "Bob"})

    response = client.get("/tasks", params={"search": "alice"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["assignee"] == "Alice"


def test_list_tasks_search_is_case_insensitive(client):
    client.post("/tasks", json={"title": "Fix Login Bug", "assignee": "Alice"})

    response = client.get("/tasks", params={"search": "LOGIN"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["title"] == "Fix Login Bug"


def test_list_tasks_search_handles_null_assignee_safely(client):
    client.post("/tasks", json={"title": "Unassigned task"})
    client.post("/tasks", json={"title": "Assigned task", "assignee": "Alice"})

    response = client.get("/tasks", params={"search": "alice"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["title"] == "Assigned task"
    assert body[0]["assignee"] == "Alice"


def test_list_tasks_filter_by_status_returns_only_matches(client):
    client.post("/tasks", json={"title": "Open task", "status": "ToDo"})
    client.post("/tasks", json={"title": "Done task", "status": "Done"})

    response = client.get("/tasks", params={"status": "ToDo"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["status"] == "ToDo"


def test_list_tasks_combined_status_and_priority_returns_only_matches(client):
    client.post(
        "/tasks",
        json={"title": "Match", "status": "InProgress", "priority": "High"},
    )
    client.post(
        "/tasks",
        json={"title": "Wrong status", "status": "Done", "priority": "High"},
    )
    client.post(
        "/tasks",
        json={"title": "Wrong priority", "status": "InProgress", "priority": "Low"},
    )

    response = client.get("/tasks", params={"status": "InProgress", "priority": "High"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["title"] == "Match"


def test_list_tasks_combined_search_and_status_returns_only_matches(client):
    client.post(
        "/tasks",
        json={"title": "API cleanup", "status": "InProgress", "assignee": "Alice"},
    )
    client.post(
        "/tasks",
        json={"title": "API cleanup", "status": "Done", "assignee": "Alice"},
    )

    response = client.get(
        "/tasks",
        params={"search": "alice", "status": "InProgress"},
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["status"] == "InProgress"


def test_list_tasks_combined_search_and_priority_returns_only_matches(client):
    client.post(
        "/tasks",
        json={"title": "API cleanup", "priority": "High", "assignee": "Alice"},
    )
    client.post(
        "/tasks",
        json={"title": "API cleanup", "priority": "Low", "assignee": "Alice"},
    )

    response = client.get(
        "/tasks",
        params={"search": "alice", "priority": "High"},
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["priority"] == "High"


def test_list_tasks_combined_search_status_and_priority_returns_only_matches(client):
    client.post(
        "/tasks",
        json={
            "title": "API cleanup",
            "description": "Refactor endpoint docs",
            "assignee": "Alice",
            "status": "InProgress",
            "priority": "High",
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "API cleanup",
            "description": "Refactor endpoint docs",
            "assignee": "Bob",
            "status": "InProgress",
            "priority": "High",
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "API cleanup",
            "description": "Refactor endpoint docs",
            "assignee": "Alice",
            "status": "Done",
            "priority": "High",
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "API cleanup",
            "description": "Refactor endpoint docs",
            "assignee": "Alice",
            "status": "InProgress",
            "priority": "Low",
        },
    )

    response = client.get(
        "/tasks",
        params={
            "search": "alice",
            "status": "InProgress",
            "priority": "High",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["title"] == "API cleanup"
    assert body[0]["status"] == "InProgress"
    assert body[0]["priority"] == "High"
    assert body[0]["assignee"] == "Alice"


def test_list_tasks_search_no_match_returns_200_and_empty_list(client):
    client.post("/tasks", json={"title": "Existing task"})

    response = client.get("/tasks", params={"search": "missing"})

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_invalid_status_query_returns_422(client):
    response = client.get("/tasks", params={"status": "BadStatus"})

    assert response.status_code == 422


def test_list_tasks_invalid_priority_query_returns_422(client):
    response = client.get("/tasks", params={"priority": "BadPriority"})

    assert response.status_code == 422

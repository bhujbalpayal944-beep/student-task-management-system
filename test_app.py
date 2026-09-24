
from app import app, tasks


def test_home_page():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_add_task():
    client = app.test_client()

    response = client.post(
        "/add-task",
        data={
            "task": "Test Assignment",
            "subject": "Testing",
            "deadline": "2026-10-01",
            "priority": "High"
        }
    )

    assert response.status_code == 302
    assert tasks[-1]["task"] == "Test Assignment"


def test_tasks_api():
    client = app.test_client()

    response = client.get("/api/tasks")

    assert response.status_code == 200

    data = response.get_json()

    assert isinstance(data, dict)
    assert "total_tasks" in data
    assert "tasks" in data
    assert data["total_tasks"] == len(data["tasks"])
    assert isinstance(data["tasks"], list)


def test_complete_task():
    client = app.test_client()

    tasks.append(
        {
            "id": 999,
            "task": "Completion Test",
            "subject": "Testing",
            "deadline": "2026-10-05",
            "priority": "Medium",
            "status": "Pending"
        }
    )

    response = client.post("/complete-task/999")

    assert response.status_code == 302
    assert tasks[-1]["status"] == "Completed"

    tasks.pop()


def test_statistics():
    client = app.test_client()

    response = client.get("/statistics")

    assert response.status_code == 200

    data = response.get_json()

    assert "total_tasks" in data
    assert "completed_tasks" in data
    assert "pending_tasks" in data
    assert "high_priority_tasks" in data

    assert data["total_tasks"] == len(tasks)


def test_task_filter():
    client = app.test_client()

    tasks.append(
        {
            "id": 1000,
            "task": "Filter Pending Test",
            "subject": "Testing",
            "deadline": "2026-10-10",
            "priority": "High",
            "status": "Pending"
        }
    )

    response = client.get("/?status=Pending")

    assert response.status_code == 200
    assert b"Filter Pending Test" in response.data

    tasks.pop()
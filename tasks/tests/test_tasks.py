# Verified (Week 3): Part of a 30-test suite covering authentication, CRUD operations, scoping, and validation.
# TODO (Week 3): A full login→create→read→update→delete sequential integration test is still missing.
import pytest

from tasks.models import Task

# ──────────────────────────────────────────────
# AUTHENTICATION GUARD TESTS
# ──────────────────────────────────────────────


@pytest.mark.django_db
class TestAuthenticationRequired:
    """Unauthenticated users must be blocked from all task endpoints."""

    def test_list_tasks_unauthenticated(self, api_client):
        """GET /api/tasks/ without token returns 401."""
        response = api_client.get("/api/tasks/")
        assert response.status_code == 401

    def test_create_task_unauthenticated(self, api_client):
        """POST /api/tasks/ without token returns 401."""
        response = api_client.post(
            "/api/tasks/",
            {"title": "Sneak in"},
            format="json",
        )
        assert response.status_code == 401

    def test_retrieve_task_unauthenticated(self, api_client, sample_task):
        """GET /api/tasks/<id>/ without token returns 401."""
        response = api_client.get(f"/api/tasks/{sample_task.id}/")
        assert response.status_code == 401

    def test_update_task_unauthenticated(self, api_client, sample_task):
        """PUT /api/tasks/<id>/ without token returns 401."""
        response = api_client.put(
            f"/api/tasks/{sample_task.id}/",
            {"title": "Hacked"},
            format="json",
        )
        assert response.status_code == 401

    def test_delete_task_unauthenticated(self, api_client, sample_task):
        """DELETE /api/tasks/<id>/ without token returns 401."""
        response = api_client.delete(f"/api/tasks/{sample_task.id}/")
        assert response.status_code == 401


# ──────────────────────────────────────────────
# CRUD TESTS
# ──────────────────────────────────────────────


@pytest.mark.django_db
class TestTaskCRUD:
    """Full CRUD for authenticated users."""

    def test_create_task_success(self, auth_client):
        """POST /api/tasks/ with valid data returns 201 and the task."""
        payload = {
            "title": "Write report",
            "description": "Annual report for Q4",
            "status": "pending",
            "priority": "high",
        }
        response = auth_client.post("/api/tasks/", payload, format="json")
        assert response.status_code == 201
        assert response.data["title"] == "Write report"
        assert response.data["priority"] == "high"

    def test_create_task_missing_title(self, auth_client):
        """POST without title returns 400."""
        response = auth_client.post(
            "/api/tasks/",
            {"description": "No title here"},
            format="json",
        )
        assert response.status_code == 400
        assert "title" in response.data  # error message mentions the field

    def test_create_task_title_too_long(self, auth_client):
        """POST with title > 200 chars returns 400."""
        long_title = "A" * 201
        response = auth_client.post(
            "/api/tasks/",
            {"title": long_title},
            format="json",
        )
        assert response.status_code == 400

    def test_list_tasks_returns_only_own(self, auth_client, sample_task):
        """GET /api/tasks/ returns the authenticated user's tasks."""
        response = auth_client.get("/api/tasks/")
        assert response.status_code == 200
        # sample_task belongs to user_one (same as auth_client)
        assert len(response.data) >= 1
        titles = [t["title"] for t in response.data]
        assert "Buy groceries" in titles

    def test_retrieve_task_success(self, auth_client, sample_task):
        """GET /api/tasks/<id>/ returns correct task data."""
        response = auth_client.get(f"/api/tasks/{sample_task.id}/")
        assert response.status_code == 200
        assert response.data["title"] == "Buy groceries"

    def test_update_task_full(self, auth_client, sample_task):
        """PUT /api/tasks/<id>/ replaces the task data."""
        payload = {
            "title": "Buy groceries and cook",
            "description": "Updated list",
            "status": "in_progress",
            "priority": "high",
        }
        response = auth_client.put(
            f"/api/tasks/{sample_task.id}/",
            payload,
            format="json",
        )
        assert response.status_code == 200
        assert response.data["status"] == "in_progress"
        assert response.data["title"] == "Buy groceries and cook"

    def test_update_task_partial(self, auth_client, sample_task):
        """PATCH /api/tasks/<id>/ updates only the provided fields."""
        response = auth_client.patch(
            f"/api/tasks/{sample_task.id}/",
            {"status": "completed"},
            format="json",
        )
        assert response.status_code == 200
        assert response.data["status"] == "completed"
        # Title should remain unchanged
        assert response.data["title"] == "Buy groceries"

    def test_delete_task_success(self, auth_client, sample_task):
        """DELETE /api/tasks/<id>/ removes the task and returns 204."""
        response = auth_client.delete(f"/api/tasks/{sample_task.id}/")
        assert response.status_code == 204
        # Confirm it's gone from the database
        assert not Task.objects.filter(id=sample_task.id).exists()

    def test_retrieve_nonexistent_task(self, auth_client):
        """GET /api/tasks/99999/ returns 404."""
        response = auth_client.get("/api/tasks/99999/")
        assert response.status_code == 404


# ──────────────────────────────────────────────
# PER-USER SCOPING TESTS
# ──────────────────────────────────────────────


@pytest.mark.django_db
class TestPerUserScoping:
    """
    The most critical security tests.
    User A must never see, edit, or delete User B's tasks.
    """

    def test_users_see_only_their_own_tasks(
        self, auth_client, auth_client_two, user_one, user_two, db
    ):
        """Each user's task list contains only their own tasks."""
        # Create a task for user_one
        Task.objects.create(
            user=user_one, title="Imad's task", status="pending", priority="medium"
        )
        # Create a task for user_two
        Task.objects.create(
            user=user_two, title="Ali's task", status="pending", priority="medium"
        )

        response_one = auth_client.get("/api/tasks/")
        response_two = auth_client_two.get("/api/tasks/")

        titles_one = [t["title"] for t in response_one.data]
        titles_two = [t["title"] for t in response_two.data]

        assert "Imad's task" in titles_one
        assert "Ali's task" not in titles_one  # user_one must NOT see user_two's task

        assert "Ali's task" in titles_two
        assert "Imad's task" not in titles_two  # user_two must NOT see user_one's task

    def test_user_cannot_retrieve_other_users_task(self, auth_client_two, sample_task):
        """
        user_two tries to GET user_one's task by ID.
        Should return 404 (not 403) because the task doesn't
        exist in user_two's queryset — it's as if it doesn't exist.
        """
        response = auth_client_two.get(f"/api/tasks/{sample_task.id}/")
        assert response.status_code == 404

    def test_user_cannot_update_other_users_task(self, auth_client_two, sample_task):
        """user_two tries to PUT user_one's task. Returns 404."""
        response = auth_client_two.put(
            f"/api/tasks/{sample_task.id}/",
            {"title": "Stolen", "status": "completed", "priority": "low"},
            format="json",
        )
        assert response.status_code == 404

    def test_user_cannot_delete_other_users_task(self, auth_client_two, sample_task):
        """user_two tries to DELETE user_one's task. Returns 404."""
        response = auth_client_two.delete(f"/api/tasks/{sample_task.id}/")
        assert response.status_code == 404
        # Confirm user_one's task is still intact
        assert Task.objects.filter(id=sample_task.id).exists()


# ──────────────────────────────────────────────
# VALIDATION TESTS
# ──────────────────────────────────────────────


@pytest.mark.django_db
class TestTaskValidation:
    """Tests for serializer-level validation rules."""

    def test_invalid_status_value(self, auth_client):
        """Submitting a status not in the choices list returns 400."""
        response = auth_client.post(
            "/api/tasks/",
            {"title": "Test task", "status": "flying"},
            format="json",
        )
        assert response.status_code == 400
        assert "status" in response.data

    def test_invalid_priority_value(self, auth_client):
        """Submitting a priority not in the choices list returns 400."""
        response = auth_client.post(
            "/api/tasks/",
            {"title": "Test task", "priority": "extreme"},
            format="json",
        )
        assert response.status_code == 400
        assert "priority" in response.data

    def test_blank_title_rejected(self, auth_client):
        """An empty string title returns 400."""
        response = auth_client.post(
            "/api/tasks/",
            {"title": ""},
            format="json",
        )
        assert response.status_code == 400
        assert "title" in response.data

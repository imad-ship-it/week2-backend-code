# Authentication endpoints tests
import pytest

# ──────────────────────────────────────────────
# REGISTRATION TESTS
# ──────────────────────────────────────────────


@pytest.mark.django_db
class TestRegistration:
    """Tests for the /api/register/ endpoint."""

    def test_register_success(self, api_client):
        """A new user can register with valid credentials."""
        payload = {
            "username": "newuser",
            "email": "new@test.com",
            "password": "securepass999",
            "password2": "securepass999",
        }
        response = api_client.post("/api/register/", payload, format="json")
        assert response.status_code == 201
        assert response.data["user"]["username"] == "newuser"

    def test_register_duplicate_username(self, api_client, user_one):
        """Registering with an existing username returns 400."""
        payload = {
            "username": "imad",  # user_one already has this username
            "email": "other@test.com",
            "password": "securepass999",
        }
        response = api_client.post("/api/register/", payload, format="json")
        assert response.status_code == 400

    def test_register_missing_password(self, api_client):
        """Registering without a password returns 400."""
        payload = {"username": "ghost"}
        response = api_client.post("/api/register/", payload, format="json")
        assert response.status_code == 400

    def test_register_missing_username(self, api_client):
        """Registering without a username returns 400."""
        payload = {"password": "somepass123"}
        response = api_client.post("/api/register/", payload, format="json")
        assert response.status_code == 400


# ──────────────────────────────────────────────
# LOGIN / TOKEN TESTS
# ──────────────────────────────────────────────


@pytest.mark.django_db
class TestLogin:
    """Tests for the /api/token/ (JWT obtain) endpoint."""

    def test_login_success_returns_tokens(self, api_client, user_one):
        """Valid credentials return access and refresh tokens."""
        payload = {"username": "imad", "password": "strongpass123"}
        response = api_client.post("/api/token/", payload, format="json")
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_wrong_password(self, api_client, user_one):
        """Wrong password returns 401."""
        payload = {"username": "imad", "password": "wrongpassword"}
        response = api_client.post("/api/token/", payload, format="json")
        assert response.status_code == 401

    def test_login_nonexistent_user(self, api_client):
        """Non-existent user returns 401."""
        payload = {"username": "nobody", "password": "pass"}
        response = api_client.post("/api/token/", payload, format="json")
        assert response.status_code == 401


# ──────────────────────────────────────────────
# TOKEN REFRESH TESTS
# ──────────────────────────────────────────────


@pytest.mark.django_db
class TestTokenRefresh:
    """Tests for the /api/token/refresh/ endpoint."""

    def test_refresh_returns_new_access_token(self, api_client, user_one):
        """A valid refresh token returns a new access token."""
        # Step 1: log in to get tokens
        login = api_client.post(
            "/api/token/",
            {"username": "imad", "password": "strongpass123"},
            format="json",
        )
        refresh_token = login.data["refresh"]

        # Step 2: use refresh token to get new access token
        response = api_client.post(
            "/api/token/refresh/",
            {"refresh": refresh_token},
            format="json",
        )
        assert response.status_code == 200
        assert "access" in response.data

    def test_refresh_with_invalid_token(self, api_client):
        """An invalid refresh token returns 401."""
        response = api_client.post(
            "/api/token/refresh/",
            {"refresh": "this.is.not.valid"},
            format="json",
        )
        assert response.status_code == 401

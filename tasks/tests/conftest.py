# Pytest configuration and fixtures
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from tasks.models import Task


@pytest.fixture
def api_client():
    """A bare APIClient with no authentication."""
    return APIClient()


@pytest.fixture
def user_one(db):
    """First test user."""
    return User.objects.create_user(
        username="imad", email="imad@test.com", password="strongpass123"
    )


@pytest.fixture
def user_two(db):
    """Second test user — used for scoping tests."""
    return User.objects.create_user(
        username="ali", email="ali@test.com", password="strongpass456"
    )


@pytest.fixture
def auth_client(db, user_one):
    """
    An APIClient already authenticated as user_one.
    We get a real JWT token from the login endpoint,
    exactly like a real user would.
    """
    client = APIClient()
    response = client.post(
        "/api/token/",
        {"username": "imad", "password": "strongpass123"},
        format="json",
    )
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


@pytest.fixture
def auth_client_two(db, user_two):
    """An APIClient authenticated as user_two."""
    client = APIClient()
    response = client.post(
        "/api/token/",
        {"username": "ali", "password": "strongpass456"},
        format="json",
    )
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


@pytest.fixture
def sample_task(db, user_one):
    """A Task owned by user_one, ready to use in tests."""
    return Task.objects.create(
        user=user_one,
        title="Buy groceries",
        description="Milk, eggs, bread",
        status="pending",
        priority="medium",
    )

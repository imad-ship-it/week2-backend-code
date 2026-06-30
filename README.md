
# Week 2 — Django REST Framework Task Manager API

A fully featured REST API built with Django and Django REST Framework during Week 2 of my AI-focused internship at Arbisoft. The API supports task management with JWT authentication, per-user data scoping, filtering, and a comprehensive pytest test suite.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.14 | Language |
| Django 6.0.6 | Web framework |
| Django REST Framework | API layer |
| djangorestframework-simplejwt | JWT authentication |
| django-filter | Filtering, search, ordering |
| pytest + pytest-django | Testing |
| Ruff | Linting and formatting |
| pre-commit | Git hook automation |

---

## Features

- Full CRUD for tasks via RESTful endpoints
- JWT authentication (register, login, token refresh)
- Per-user task scoping — users can only access their own tasks
- Filtering by status and priority
- Search by title and description
- Ordering by due date, priority, created date
- 30 automated tests covering auth, CRUD, scoping, and validation
- Clean codebase verified by Ruff linter and formatter

---

## Project Structure

```
taskmanager/
├── accounts/          # Registration, login, JWT endpoints
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── tasks/             # Task model, ViewSet, serializer, tests
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── tests/
│       ├── conftest.py
│       ├── test_auth.py
│       └── test_tasks.py
├── taskmanager/       # Project settings and root URLs
│   ├── settings.py
│   └── urls.py
├── ruff.toml          # Linter and formatter config
├── .pre-commit-config.yaml
├── pytest.ini
└── requirements.txt
```

---

## API Endpoints

### Auth

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/accounts/register/` | Register a new user |
| POST | `/api/accounts/login/` | Login and receive JWT tokens |
| POST | `/api/accounts/token/refresh/` | Refresh access token |

### Tasks (all require JWT token)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/tasks/` | List all tasks for authenticated user |
| POST | `/api/tasks/` | Create a new task |
| GET | `/api/tasks/{id}/` | Retrieve a specific task |
| PUT | `/api/tasks/{id}/` | Full update of a task |
| PATCH | `/api/tasks/{id}/` | Partial update of a task |
| DELETE | `/api/tasks/{id}/` | Delete a task |

### Filtering

```
GET /api/tasks/?status=pending
GET /api/tasks/?priority=high
GET /api/tasks/?search=report
GET /api/tasks/?ordering=-due_date
GET /api/tasks/?status=pending&priority=high&ordering=due_date
```

---

## Task Model

| Field | Type | Details |
|---|---|---|
| user | ForeignKey | Linked to auth user, CASCADE delete |
| title | CharField | Max 200 characters, required |
| description | TextField | Optional |
| due_date | DateField | Optional |
| status | CharField | pending / in_progress / completed |
| priority | CharField | low / medium / high |
| created_at | DateTimeField | Auto set on create |
| updated_at | DateTimeField | Auto set on update |

---

## Setup and Installation

```bash
# Clone the repo
git clone https://github.com/imad-ship-it/week2-backend-django
cd week2-backend-django

# Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate  # Git Bash on Windows
# or
venv\Scripts\activate         # PowerShell on Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start the server
python manage.py runserver
```

---

## Running Tests

```bash
# Run full test suite
pytest tasks/tests/ -v

# Run with coverage report
pytest tasks/tests/ -v --cov=tasks --cov-report=term-missing
```

---

## Code Quality

```bash
# Lint and auto-fix
ruff check . --fix

# Format
ruff format .

# Run all pre-commit hooks
pre-commit run --all-files
```

---

## Week 1 Reference

The React frontend built in Week 1 is available at:
[github.com/imad-ship-it/task-manager](https://github.com/imad-ship-it/task-manager)



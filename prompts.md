# AI Interaction Log — Week 2 (Django Backend)

This log documents all AI tool usage during Week 2 of the Arbisoft internship, as required by my mentor. Each entry includes the day, the tool used, the purpose, and a summary of what was produced or fixed.

---

## Day 1 — Django Setup

**Tool:** Claude (Sonnet)
**Purpose:** Learn Django project structure, build the Task model, serializer, ViewSet, and URL routing from scratch.
**Summary:** Claude explained the MTV pattern, the difference between Django and DRF, and walked through creating the Task model with all required fields. Code was written step by step with concept explanations before each piece.

---

## Day 2 — Full CRUD

**Tool:** Claude (Sonnet)
**Purpose:** Implement and understand all 5 CRUD operations, correct HTTP status codes, and Postman testing.
**Summary:** Claude explained the mapping between HTTP methods and CRUD operations, the difference between PUT and PATCH, and how DRF serializer validation triggers 400 responses. All endpoints were manually tested in Postman.

---

## Day 3 — ORM, Filtering, Admin

**Tool:** Claude (Sonnet)
**Purpose:** Add status/priority/user fields to the Task model, implement django-filter, search, and ordering.
**Summary:** Claude explained the Django ORM as a translation layer over SQL, walked through filterset_fields vs search_fields vs ordering_fields, and explained model choices for data validation. Admin panel registration and superuser creation were also covered.

---

## Day 4 — JWT Authentication

**Tool:** Claude (Sonnet)
**Purpose:** Implement JWT authentication, register/login endpoints, and per-user task scoping.
**Summary:** Claude explained JWT token structure (header/payload/signature), access vs refresh tokens, and stateless authentication. Built register and login endpoints, protected task endpoints with IsAuthenticated, and implemented per-user scoping via get_queryset() and perform_create().

---

## Day 5 — Testing with pytest

**Tool:** Claude (Sonnet)
**Purpose:** Write a full pytest test suite covering authentication, CRUD, per-user scoping, and validation.
**Summary:** Claude explained the difference between unit/integration/e2e tests, pytest fixtures, the db marker, and APIClient. Generated conftest.py with reusable fixtures and two test files covering 30 test cases total.

**Debugging note:** Initial test run produced 9 failures and 16 errors, all caused by URL mismatches — the tests assumed `/api/token/` and `/api/register/`, but the actual project routes were `/api/accounts/login/` and `/api/accounts/register/` (defined in a separate accounts app). I used Antigravity's internal agent to diagnose the URL routing issue and fix a related runserver crash (an incorrect import in `taskmanager/urls.py` — `RegisterView` was being imported from the wrong app). I then reviewed every change with Claude to confirm correctness, verified the test payload fix (`password2` field requirement), and ran the full suite myself to confirm all 30 tests passed before committing.

---

## Day 6 — Linting and Code Quality

**Tool:** Claude (Sonnet)
**Purpose:** Verify and run linting/formatting tooling across the codebase.
**Summary:** Discovered I had already configured Ruff (linter + formatter) and pre-commit hooks in an earlier session. Claude explained the difference between a linter and a formatter, the meaning of each Ruff rule set (E, W, F, I, B, SIM), and how pre-commit compares to Husky from Week 1. Ran `ruff check --fix`, `ruff format`, and `pre-commit run --all-files` — all checks passed with zero issues.

---

## Day 7 — Documentation and Delivery

**Tool:** Claude (Sonnet)
**Purpose:** Write concept notes outline, professional README, and prepare final deliverables.
**Summary:** Claude provided a topic list (not written content) for all 6 daily concept note files in the week2-concepts repo, which I wrote in my own words. Claude generated the README.md for this repo and a comprehensive PDF study guide summarizing the full week's architecture and request lifecycle for personal reference.

---

## General Notes

- All code explanations were requested step-by-step with concepts explained before implementation, per my own learning preference.
- Conventional commit format (feat/fix/test/docs/chore) was used throughout the week, as required.
- This log will be updated in future weeks as the project continues.

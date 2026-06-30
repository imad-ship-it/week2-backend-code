from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated  # ← NEW

from .filters import TaskFilter
from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    # Verified (Week 3): JWT authentication is enforced here (referenced by TestAuthenticationRequired in test_tasks.py)
    permission_classes = [IsAuthenticated]  # ← NEW

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = TaskFilter
    search_fields = ["title", "description"]
    ordering_fields = ["due_date", "priority", "created_at", "status"]
    ordering = ["-created_at"]

    # TODO (Week 3): Current scoping is object-level only; a role-based permission class is still needed
    def get_queryset(self):  # ← NEW
        # Only return tasks belonging to the logged-in user                     # ← NEW
        return Task.objects.filter(user=self.request.user)  # ← NEW

    def perform_create(self, serializer):  # ← NEW
        # Automatically assign the logged-in user when creating a task          # ← NEW
        serializer.save(user=self.request.user)  # ← NEW

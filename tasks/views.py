from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .filters import TaskFilter
from .models import Task
from .permissions import IsOwnerOrAdmin
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    # Verified (Week 3): JWT authentication and custom permissions are enforced here
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = TaskFilter
    search_fields = ["title", "description"]
    ordering_fields = ["due_date", "priority", "created_at", "status"]
    ordering = ["-created_at"]

    def get_queryset(self):
        # Admin-role users get all tasks, standard-role users get only their own
        user_role = getattr(
            getattr(self.request.user, "profile", None), "role", "standard"
        )
        if user_role == "admin":
            return Task.objects.all()
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the logged-in user when creating a task
        serializer.save(user=self.request.user)

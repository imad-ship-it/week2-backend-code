import django_filters

from .models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr="exact")
    priority = django_filters.CharFilter(lookup_expr="exact")
    due_date = django_filters.DateFilter(lookup_expr="exact")
    due_date_before = django_filters.DateFilter(
        field_name="due_date", lookup_expr="lte"
    )
    due_date_after = django_filters.DateFilter(field_name="due_date", lookup_expr="gte")

    class Meta:
        model = Task
        fields = ["status", "priority", "due_date"]

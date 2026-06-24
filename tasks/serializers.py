from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "due_date",
            "completed",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Title must be at least 3 characters long"
            )
        return value.strip()

    def validate_due_date(self, value):
        from datetime import date

        if value and value < date.today():
            raise serializers.ValidationError("Due date cannot be in the past")
        return value

    def validate(self, data):
        # Only enforce title requirement on create, not on partial update (PATCH)
        if not self.instance and ("title" not in data or not data["title"]):
            raise serializers.ValidationError({"title": "Title is required"})
        return data

from datetime import date

from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # ← NEW

    class Meta:
        model = Task
        fields = [
            "id",
            "user",  # ← NEW
            "title",
            "description",
            "due_date",
            "status",
            "priority",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]  # ← UPDATED

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Title must be at least 3 characters long"
            )
        return value.strip()

    def validate_due_date(self, value):
        if value and value < date.today():
            raise serializers.ValidationError("Due date cannot be in the past")
        return value

    def validate(self, data):
        # Only enforce title requirement on create, not on partial update (PATCH)
        if not self.instance and ("title" not in data or not data["title"]):
            raise serializers.ValidationError({"title": "Title is required"})
        return data

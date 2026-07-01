from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("standard", "Standard"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="standard")

    def __str__(self):
        return f"{self.user.username}'s Profile ({self.role})"

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        BIOMEDICAL_OFFICER = 'BIOMEDICAL_OFFICER', 'Biomedical Officer'
        WARD_STAFF = 'WARD_STAFF', 'Ward Staff'

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.WARD_STAFF,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
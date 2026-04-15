from django.contrib.auth.models import AbstractUser
from django.db import models


class MedicalUser(AbstractUser):
    class Role(models.TextChoices):
        PATIENT = 'patient', 'Patient'
        DOCTOR = 'doctor', 'Doctor'
        ADMIN = 'admin', 'Admin'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.PATIENT)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self) -> str:
        return f'{self.get_full_name() or self.username} ({self.role})'

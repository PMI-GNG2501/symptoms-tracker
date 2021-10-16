from django.db import models

from medication.models import Medication
from users.models import User


class Reminder(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    time = models.TimeField()
    notes = models.TextField(blank=True)
    medication = models.ManyToManyField(Medication)
    scheduler_id = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

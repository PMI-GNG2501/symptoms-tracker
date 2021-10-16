from django.db import models

from medication.models import Medication
from users.models import User


class Symptoms(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    datetime = models.DateTimeField()
    message = models.TextField()
    medication = models.ManyToManyField(Medication, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

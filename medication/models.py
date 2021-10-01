from django.db import models
from users.models import User


class Medication(models.Model):
    name = models.TextField()
    notes = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

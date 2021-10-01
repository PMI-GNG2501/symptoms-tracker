from django.db import models

from medication.models import Medication
from users.models import User


class Symptoms(models.Model):
    datetime = models.DateTimeField()
    message = models.TextField()
    medication = models.ManyToManyField(Medication)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

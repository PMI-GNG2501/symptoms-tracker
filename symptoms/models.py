from django.db import models
from users.models import User


class Symptoms(models.Model):
    datetime = models.DateTimeField()
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

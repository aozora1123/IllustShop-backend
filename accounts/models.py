from django.db import models
from django.contrib.auth.models import AbstractUser

class Account(AbstractUser):
    point = models.PositiveIntegerField(default=100)

    def get_point(self):
        return self.point
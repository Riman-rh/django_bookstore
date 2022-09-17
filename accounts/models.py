from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    address = models.CharField(null=True, blank=True, max_length=225)
    phone = models.CharField(null=True, blank=True, max_length=25)

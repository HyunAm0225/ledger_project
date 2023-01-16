from django.contrib.auth.models import AbstractUser
from django.db import models

from base.models import BaseModel


class User(BaseModel, AbstractUser):
    email = models.EmailField("email address", unique=True, max_length=255)
    password = models.CharField("password", max_length=128)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = "사용자"

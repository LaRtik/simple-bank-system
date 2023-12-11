from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    telegram_id = models.BigIntegerField()
    confirmed = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["first_name", "last_name", "telegram_id"]
    




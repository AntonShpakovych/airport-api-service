from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser

from account.managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

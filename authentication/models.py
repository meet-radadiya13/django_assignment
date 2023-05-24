from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phone_field import PhoneField

from .managers import CustomUserManager


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("Username"), default="user", max_length=20)
    firstname = models.CharField(max_length=20, null=True, blank=True)
    lastname = models.CharField(max_length=20, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    contact_no = PhoneField(blank=True, null=True)
    email = models.EmailField(_("Email Address"), unique=True)
    is_active = models.BooleanField(verbose_name="active", default=True)
    is_superuser = models.BooleanField(verbose_name="superuser", default=False)
    is_staff = models.BooleanField(verbose_name="staff", default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to="profiles/", default="profiles/default.png")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

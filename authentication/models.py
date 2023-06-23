from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phone_field import PhoneField

from .managers import CustomUserManager


# Create your models here.
class CommonModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Company(CommonModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    contact_number = PhoneField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    subscription_end_date = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return str(self.name)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _("Username"), default="user", max_length=20, unique=True
    )
    firstname = models.CharField(max_length=20, null=True, blank=True)
    lastname = models.CharField(max_length=20, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    contact_no = PhoneField(blank=True, null=True)
    email = models.EmailField(_("Email Address"), unique=True)
    is_active = models.BooleanField(verbose_name="active", default=True)
    is_superuser = models.BooleanField(verbose_name="superuser", default=False)
    is_staff = models.BooleanField(verbose_name="staff", default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    image = models.ImageField(
        upload_to="profiles/", default="profiles/default.png"
    )
    company = models.ForeignKey(
        Company, blank=True, null=True, on_delete=models.SET_NULL
    )
    is_owner = models.BooleanField(default=False)
    has_changed_password = models.BooleanField(default=False)
    stripe_customer_id = models.CharField(
        max_length=255, null=True, blank=True
    )
    stripe_subscription_id = models.CharField(
        max_length=255, null=True,
        blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class PaymentHistory(CommonModel):
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    status = models.CharField(max_length=10, null=True, blank=True)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    transaction_made_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True
        )

    def __str__(self):
        return str(self.company)

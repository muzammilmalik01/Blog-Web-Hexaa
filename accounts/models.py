from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    A custom user model for the blogging site.

    Inherits from the AbstractUser model provided by Django.
    Adds additional fields for email, user type, staff status, and superuser status.
    Overrides the USERNAME_FIELD and REQUIRED_FIELDS attributes for authentication.
    """

    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False) # Editor
    is_superuser = models.BooleanField(default=False) # Super Admin
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password','is_staff','is_superuser','username']

    def __str__(self):
        return self.email
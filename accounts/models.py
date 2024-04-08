from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
import stripe


class CustomUser(AbstractUser):
    """
    A custom user model for the blogging site.

    Inherits from the AbstractUser model provided by Django.
    Adds additional fields for email, user type, staff status, and superuser status.
    Overrides the USERNAME_FIELD and REQUIRED_FIELDS attributes for authentication.
    """

    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)  # Editor
    is_superuser = models.BooleanField(default=False)  # Super Admin
    USERNAME_FIELD = "email"
    picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "password",
        "is_staff",
        "is_superuser",
        "username",
    ]

    def __str__(self):
        return self.email


class PremiumUser(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, null=True, blank=True)
    stripe_subscription_id = models.CharField(max_length=50, null=True, blank=True)
    has_active_subscription = models.BooleanField(default=False)

    def has_active_subscription(self):
        """
        This method checks if the user has active subscription or not.
        """
        customer = stripe.Customer.retrieve(
            self.stripe_customer_id, expand=["subscriptions"]
        )

        for subscription in customer.subscriptions.data:
            if subscription.status == "active":
                return True

        return False

    def __str__(self):
        return self.user.email

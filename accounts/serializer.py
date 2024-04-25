from rest_framework import serializers

# from djoser.serializers import UserCreateSerializer
from .models import CustomUser, PremiumUser

# from django.contrib.auth import get_user_model


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Simple Serializer class for the CustomUser model.
    """

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "picture",
            "email",
            "password",
            "username",
            "first_name",
            "last_name",
            "is_staff",
            "is_superuser",
            "address",
            "phone",
        )


class PremiumUserSerializer(serializers.ModelSerializer):
    """
    Serializer Class for Premium Users.
    """

    class Meta:
        model = PremiumUser
        fields = "__all__"

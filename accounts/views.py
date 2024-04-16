from django.shortcuts import render
from .models import CustomUser
from .serializer import CustomUserSerializer
from rest_framework import generics
from django.contrib.auth.hashers import make_password
from rest_framework.pagination import PageNumberPagination
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response


class AllAccountsListAPI(generics.ListAPIView):
    """
    Lists all the accounts in the database.
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = PageNumberPagination


class CreateAccountAPI(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def perform_create(self, serializer):
        # ! PASSWORD can be retrieved / sniffed from the POST request from Client Side !
        """
        Overriding perform_create()

        Pops out the password from validated_data, hashes and saves the password.

        validated_data (Serializer's Instance - Dictionary)

        # * Password is hashed and saved to the DATABASE *
        """
        password = serializer.validated_data.pop("password")  # popping password.
        hashed_password = make_password(password)  # hashing password.
        serializer.save(password=hashed_password)  # saving to the DB.


class DetailAccountAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def perform_update(self, serializer):
        # ! PASSWORD can be retrieved / sniffed from the POST request from Client Side !
        """
        Overriding perform_create()

        Pops out the password from validated_data, hashes and saves the password.

        validated_data (Serializer's Instance - Dictionary)

        # * Password is hashed and saved to the DATABASE *
        """
        password = serializer.validated_data.pop("password")  # popping password.
        hashed_password = make_password(password)  # hashing password.
        serializer.save(password=hashed_password)  # saving to the DB.


class DetailAccountByEmail(generics.RetrieveAPIView):
    queryset = CustomUser.objects.filter(is_staff=True)
    serializer_class = CustomUserSerializer

    def get_object(self):
        queryset = self.get_queryset()
        email = self.kwargs.get("email")
        try:
            obj = queryset.get(email=email)
        except ObjectDoesNotExist:
            raise Http404("User not found")
        return obj

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        return Response(
            {
                "user_id": user.id,
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
            },
            status=status.HTTP_200_OK,
        )

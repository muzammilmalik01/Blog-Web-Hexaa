from django.shortcuts import render
from .models import CustomUser
from .serializer import CustomUserSerializer
from rest_framework import generics
from django.contrib.auth.hashers import make_password


class AllAccountsListAPI(generics.ListAPIView):
    """
    Lists all the accounts in the database.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

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
        password = serializer.validated_data.pop('password') # popping password.
        hashed_password = make_password(password) # hashing password.
        serializer.save(password=hashed_password) # saving to the DB.

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
        password = serializer.validated_data.pop('password') # popping password.
        hashed_password = make_password(password) # hashing password.
        serializer.save(password=hashed_password) # saving to the DB.
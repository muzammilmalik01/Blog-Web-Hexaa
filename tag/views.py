from django.shortcuts import render
from .models import Tag
from .serializer import TagSerializer
from rest_framework import generics
from .permissions import TagsPermissions

class ListCreateAPI(generics.ListCreateAPIView):
    permission_classes = [TagsPermissions]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None

class DetailAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [TagsPermissions]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None

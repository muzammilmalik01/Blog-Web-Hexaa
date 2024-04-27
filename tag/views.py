from django.shortcuts import render
from .models import Tag
from .serializer import TagSerializer
from rest_framework import generics
from .permissions import TagsPermissions
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class ListCreateAPI(generics.ListCreateAPIView):
    permission_classes = [TagsPermissions]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None

    # * Redis Mem-cache Demo Implementation
    @method_decorator(cache_page(60 * 15))  # cache for 15 minutes
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class DetailAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [TagsPermissions]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None

    # * Redis Mem-cache Demo Implementation
    @method_decorator(cache_page(60 * 15))  # cache for 15 minutes
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

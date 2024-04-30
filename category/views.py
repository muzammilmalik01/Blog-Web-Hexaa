from rest_framework import generics
from .models import Category
from .serializer import CategorySerializer
from .permissions import CategoryPermissions
from django.core.cache import cache
from rest_framework.response import Response


class CategoryCreate(generics.ListCreateAPIView):
    permission_classes = [CategoryPermissions]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        """
        Overriding GET method to return Cached Data if exists, else create cache.
        """
        data = cache.get("post_categories_list")
        # If the categories list is not in the cache, generate it and store it in the cache
        if data is None:
            response = super().get(request, *args, **kwargs)
            data = response.data
            cache.set("post_categories_list", data, 60 * 3)  # Cache for 3 minutes
        return Response(data)

    def post(self, request, *args, **kwargs):
        """
        Overriding POST method to delete the cache when a new object is added.
        Keeps the cache updated.
        """
        response = super().post(request, *args, **kwargs)
        cache.delete("post_categories_list")  # Clear the cache for this view
        return response


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [CategoryPermissions]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        """
        Overriding GET method to returned Cached detailed view if exists, else create one
        """
        pk = kwargs["pk"]
        cache_key = f"post_category_{pk}"
        data = cache.get(cache_key)

        if data is None:
            response = super().get(request, *args, **kwargs)
            data = response.data
            cache.set(cache_key, data, 60 * 3)
        return Response(data)

    def put(self, request, *args, **kwargs):
        """
        Overiding PUT method to delete the cache when an object is updated.
        Deletes existing post_categories_list cache_key if exists.
        """
        response = super().put(request, *args, **kwargs)
        pk = kwargs["pk"]
        cache_key = f"post_category_{pk}"
        cache.delete(cache_key)
        cache_key = "post_categories_list"
        cache.delete(cache_key)
        return response

    def delete(self, request, *args, **kwargs):
        """
        Overiding DELETE method to delete the cache when an object is deleted.
        Deletes existing post_categories_list cache_key if exists.
        """
        pk = kwargs["pk"]
        cache_key = f"post_category_{pk}"
        cache.delete(cache_key)
        cache_key = "post_categories_list"
        cache.delete(cache_key)
        return super().delete(request, *args, **kwargs)

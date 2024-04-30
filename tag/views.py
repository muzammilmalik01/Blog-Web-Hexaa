from .models import Tag
from .serializer import TagSerializer
from rest_framework import generics
from .permissions import TagsPermissions
from django.core.cache import cache
from rest_framework.response import Response


class ListCreateAPI(generics.ListCreateAPIView):
    permission_classes = [TagsPermissions]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        """
        Overriding GET method to return Cached Data if exists, else create cache.
        """
        data = cache.get("post_tags_list")
        # If the tags list is not in the cache, generate it and store it in the cache
        if data is None:
            response = super().get(request, *args, **kwargs)
            data = response.data
            cache.set("post_tags_list", data, 60 * 3)  # Cache for 3 minutes
        return Response(data)

    def post(self, request, *args, **kwargs):
        """
        Overriding POST method to delete the cache when a new object is added.
        Keeps the cache updated.
        """
        response = super().post(request, *args, **kwargs)
        cache.delete("post_tags_list")  # Clear the cache for this view
        return response


class DetailAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [TagsPermissions]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        """
        Overriding GET method to returned Cached detailed view if exists, else create one
        """
        pk = kwargs["pk"]
        cache_key = f"post_tag_{pk}"
        data = cache.get(cache_key)

        if data is None:
            response = super().get(request, *args, **kwargs)
            data = response.data
            cache.set(cache_key, data, 60 * 3)
        return Response(data)

    def put(self, request, *args, **kwargs):
        """
        Overiding PUT method to delete the cache when an object is updated.
        Deletes existing post_tags_list cache_key if exists.
        """
        response = super().put(request, *args, **kwargs)
        pk = kwargs["pk"]
        cache_key = f"post_tag_{pk}"
        cache.delete(cache_key)
        cache_key = "post_tags_list"
        cache.delete(cache_key)
        return response

    def delete(self, request, *args, **kwargs):
        """
        Overiding DELETE method to delete the cache when an object is deleted.
        Deletes existing post_tags_list cache_key if exists.
        """
        pk = kwargs["pk"]
        cache_key = f"post_tag_{pk}"
        cache.delete(cache_key)
        cache_key = "post_tags_list"
        cache.delete(cache_key)
        return super().delete(request, *args, **kwargs)

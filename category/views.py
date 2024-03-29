from rest_framework import generics
from .models import Category
from .serializer import CategorySerializer
from .permissions import CategoryPermissions

class CategoryCreate(generics.ListCreateAPIView):
    permission_classes = [CategoryPermissions]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None

    

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [CategoryPermissions]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None
from django.shortcuts import render
from .models import Product_Category, Color, Product, Image, Attribute
from .serializers import (
    Product_CategorySerializer,
    ColorSerializer,
    ProductSerializer,
    AttributeSerializer,
    ImageSerializer,
)
from rest_framework import generics


# Product Category Views #
class Product_CategoryListCreateAPI(generics.ListCreateAPIView):
    """
    List and Create view using Generics.

    GET list of all Product Categories
    POST new Product Categories
    """

    serializer_class = Product_CategorySerializer
    queryset = Product_Category.objects.all()
    pagination_class = None


class Product_CategoryUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update, Delete view using Generics.

    GET, PUT, PATCH, DELETE Product Category using PK.
    """

    serializer_class = Product_CategorySerializer
    queryset = Product_Category.objects.all()


# Color Views #
class ColorListCreateAPI(generics.ListCreateAPIView):
    """
    List and Create view using Generics.

    GET list of all Colors
    POST new Color
    """

    serializer_class = ColorSerializer
    queryset = Color.objects.all()
    pagination_class = None


class ColorUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update, Delete view using Generics.

    GET, PUT, PATCH, DELETE Product Color using PK.
    """

    serializer_class = ColorSerializer
    queryset = Color.objects.all()


# Product Views #
# TODO: Add Retrieve, Update, Delete Product View using Slug
class ProductListCreateAPI(generics.ListCreateAPIView):
    """
    TODO: Add Product Slug on save()

    List and Create view using Generics.

    GET list of all Products
    POST new Products
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = None


class ProductUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update, Delete view using Generics.

    GET, PUT, PATCH, DELETE Product using PK.
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.all()


# Images Views #
# TODO: Added view which gets images based on Product's Slug / PK
class ImageListCreateAPI(generics.ListCreateAPIView):
    """
    List and Create view using Generics.

    GET list of all Images
    POST new Images
    """

    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    pagination_class = None


class ImageUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update, Delete view using Generics.

    GET, PUT, PATCH, DELETE Image using PK.
    """

    serializer_class = ImageSerializer
    queryset = Image.objects.all()


# Attribute Views
class AttributeListCreateAPI(generics.ListCreateAPIView):
    """
    TODO: Prevent addition of Multiple Same Attributes
    TODO: GET Attributes using Post Slug

    List and Create view using Generics.

    GET list of all Attributes / Stock
    POST new Attributes / Stock
    """

    serializer_class = AttributeSerializer
    queryset = Attribute.objects.all()
    pagination_class = None


class AttributeUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update, Delete view using Generics.

    GET, PUT, PATCH, DELETE Attributes / Stock using PK.
    """

    serializer_class = AttributeSerializer
    queryset = Attribute.objects.all()

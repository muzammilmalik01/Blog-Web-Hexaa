from rest_framework import serializers
from .models import Product_Category, Color, Product, Attribute, Image


class Product_CategorySerializer(serializers.Serializer):
    class Meta:
        model = Product_Category
        fields = "__all__"


class ColorSerializer(serializers.Serializer):
    class Meta:
        model = Color
        field = "__all__"


class ProductSerializer(serializers.Serializer):
    class Meta:
        model = Product
        field = "__all__"


class AttributeSerializer(serializers.Serializer):
    class Meta:
        model = Attribute
        field = "__all__"


class ImageSerializer(serializers.Serializer):
    class Meta:
        model = Image
        field = "__all__"

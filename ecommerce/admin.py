from django.contrib import admin
from .models import Product_Category, Product, Attribute, Color, Image, Order, OrderItem

# Register your models here.

admin.site.register(Product_Category)
admin.site.register(Product)
admin.site.register(Attribute)
admin.site.register(Color)
admin.site.register(Image)
admin.site.register(Order)
admin.site.register(OrderItem)

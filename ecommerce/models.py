from django.db import models
from accounts.models import CustomUser


class Product_Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    category = models.ForeignKey(Product_Category, on_delete=models.PROTECT)
    description = models.CharField(max_length=1000, null=True)
    details = models.CharField(max_length=2000, null=False)
    color = models.ForeignKey(Color, on_delete=models.PROTECT)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self) -> str:
        return self.name


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_images/", null=False)
    # TODO: Image Location Changed -> Test Apis


class Attribute(models.Model):
    ATTRIBUTE_CHOICES = [
        ("Size", "Size"),
        ("Phone Model", "Phone Model"),
        ("Material", "Material"),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, choices=ATTRIBUTE_CHOICES)
    attribute_value = models.CharField(max_length=255)
    stock_quantity = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.product} - {self.name} ({self.attribute_value})"


# TODO: Tentative Models, might alter. Testing is needs.
class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    complete = models.BooleanField(default=False)
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Dispatched", "Dispatched"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]
    status = models.CharField(default="Pending", max_length=255, choices=STATUS_CHOICES)

    def __str__(self) -> str:
        return f"Order {self.id} by Customer {self.customer}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=False)

    def subtotal(self):
        return self.product.product.price * self.quantity

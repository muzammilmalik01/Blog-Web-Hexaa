from django.db import models


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
    slug = models.SlugField(unique=True)

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
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, choices=ATTRIBUTE_CHOICES)
    attribute_value = models.CharField(max_length=255)
    stock_quantity = models.PositiveIntegerField(default=0)

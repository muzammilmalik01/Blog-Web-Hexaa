from django.shortcuts import render
from .models import Product_Category, Color, Product, Image, Attribute, Order, OrderItem
from .serializers import (
    Product_CategorySerializer,
    ColorSerializer,
    ProductSerializer,
    AttributeSerializer,
    ImageSerializer,
    OrderItemSerializer,
    OrderSerializer,
)
from rest_framework import generics
from django.utils.text import slugify
import uuid
from django.shortcuts import get_object_or_404
from django.http import Http404
from .permissions import OrderPermission, ProductPermissions

# * How to populate Products:

# * 1. Add Product Category
# * 2. Add Color
# * 3. Add Products
# * 4. Add Images
# * 5. Add Attributes (Size or Model, Available Stock)

# ! Permission are commented out (disabled)


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
    # permission_classes = [ProductPermissions]


class Product_CategoryUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update, Delete view using Generics.

    GET, PUT, PATCH, DELETE Product Category using PK.
    """

    serializer_class = Product_CategorySerializer
    queryset = Product_Category.objects.all()
    # permission_classes = [ProductPermissions]


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
    # permission_classes = [ProductPermissions]


class ColorUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update, Delete view using Generics.

    GET, PUT, PATCH, DELETE Product Color using PK.
    """

    serializer_class = ColorSerializer
    queryset = Color.objects.all()
    # permission_classes = [ProductPermissions]


# Product Views #
class ProductListCreateAPI(generics.ListCreateAPIView):
    """

    List and Create view using Generics.

    GET list of all Products
    POST new Products
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = None
    # permission_classes = [ProductPermissions]

    def perform_create(self, serializer):
        product_name = serializer.validated_data.get("name")
        slug = slugify(product_name)
        unique_id = str(uuid.uuid4())[:8]  # generates a unique ID

        if Product.objects.filter(slug=slug).exists():
            slug = f"{slug}-{unique_id}"

        serializer.save(slug=slug)


class ProductUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update, Delete view using Generics.

    GET, PUT, PATCH, DELETE Product using PK.
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    # permission_classes = [ProductPermissions]


class ProductUpdateDeletebySlug(generics.RetrieveAPIView):
    """
    Retrieve, Update, Delete view using Generics.

    GET, PUT, PATCH, DELETE Product using slug.
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    # permission_classes = [ProductPermissions]

    def get_object(self):
        slug = self.kwargs.get("slug")
        return get_object_or_404(Product, slug=slug)


# Images Views #
class ImageListCreateAPI(generics.ListCreateAPIView):
    """
    List and Create view using Generics.

    GET list of all Images
    POST new Images
    """

    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    pagination_class = None
    # permission_classes = [ProductPermissions]


class ImageListAPIbyProduct(generics.ListAPIView):
    """
    List view using Generics.

    GET list of all Images of a Product using Product ID
    POST new Images
    """

    serializer_class = ImageSerializer
    pagination_class = None
    # permission_classes = [ProductPermissions]

    def get_queryset(self):
        product_id = self.kwargs.get("product_id", None)
        if product_id is not None:
            if not Product.objects.filter(id=product_id).exists():
                raise Http404("Product not found.")
            return Image.objects.filter(product_id=product_id)
        raise Http404("Product ID not provided.")


class ImageUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update, Delete view using Generics.

    GET, PUT, PATCH, DELETE Image using PK.
    """

    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    # permission_classes = [ProductPermissions]


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
    # permission_classes = [ProductPermissions]


class AttributeUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update, Delete view using Generics.

    GET, PUT, PATCH, DELETE Attributes / Stock using PK.
    """

    serializer_class = AttributeSerializer
    queryset = Attribute.objects.all()
    # permission_classes = [ProductPermissions]


# * Basic workflow how the order placing will work on Front-End:

# * 1. User selects different products, adds to cart and clicks place order.
# * 2. Order is created with user ID and it would return Order NO (Order ID)
# * 3. Returned order ID will be used to POST Order Items one by one
# * 4. When all order items will be POSTED, Order will be PATCHED (complete -> True). This will make sure all the Order Item were Posted and Window was not closed.
# * 5. Return the user with necesarry details after the order is successfully placed.
# * 6. For payment, when all the Order Items are successfully posted, take the user to Payment Window.
# ! Payment Model or workflow not implemented - Stripe is integrated.

# * In detail POST Item:
# * 1. When POST request is received, check if the Product Quantity >= Order Item Quantity
# * 2. If Product Quantity >= Order Item Quantity, subtract the Product Quantity, set Order Total amount by += Order Item Subtotal, return 204


class OrderListCreateAPI(generics.ListCreateAPIView):
    """
    List and Create view using Generics.

    GET list of all Orders
    POST new Orders
    """

    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    pagination_class = None
    # permission_classes = [OrderPermission]


class OrderUpdateDeleteAPI(generics.RetrieveUpdateDestroyAPIView):
    # TODO: Make same view but get the object via Customer username / ID
    """
    List and Create view using Generics.

    GET, PUT, PATCH Order by PK
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    pagination_class = None
    # permission_classes = [OrderPermission]


# TODO: Have to make specialized views for Order Items according to React
class OrderItemListAPI(generics.ListAPIView):
    """
    List view using Generics.

    GET list of all Orders Items
    """

    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
    pagination_class = None
    # permission_classes = [OrderPermission]


class OrderItemCreateAPI(generics.CreateAPIView):
    """
    Create view using Generics.

    POST new Orders Items

    * Uses Customer Order Item Serializer to properly place an order *
    ! Thorough testing is required !
    """

    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
    pagination_class = None
    # permission_classes = [OrderPermission]


class OrderItemUpdateDeleteAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    RetrieveUpdateDelete view using Generics.

    GET, PUT, PATCH, DELETE Orders Items by ID
    """

    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
    pagination_class = None
    # permission_classes = [OrderPermission]

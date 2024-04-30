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
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
import stripe
from django.conf import settings
from django.core.cache import cache

stripe.api_key = settings.STRIPE_SECRET_KEY

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

    def get(self, request, *args, **kwargs):
        """
        Overriding GET method to return Cached Data if exists, else create cache.
        """
        data = cache.get("product_category_list")
        if data is None:
            response = super().get(request, *args, **kwargs)
            data = response
            cache.set("product_category_list", data, 60 * 10)  # cache for 10 minutes
        return Response(data)

    def post(self, request, *args, **kwargs):
        """
        Overriding POST method to delete cached data, keeps the data updated.
        """
        response = super().post(request, *args, **kwargs)
        cache.delete("product_category_list")
        return response


class Product_CategoryUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update, Delete view using Generics.

    GET, PUT, PATCH, DELETE Product Category using PK.
    """

    serializer_class = Product_CategorySerializer
    queryset = Product_Category.objects.all()
    # permission_classes = [ProductPermissions]

    def put(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        cache_key = f"product_category_{pk}"
        cache.delete(cache_key)
        cache_key = "product_category_list"
        cache.delete(cache_key)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        cache_key = f"product_category_{pk}"
        cache.delete(cache_key)
        cache_key = "product_category_list"
        cache.delete(cache_key)
        return super().put(request, *args, **kwargs)


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

    def get(self, request, *args, **kwargs):
        """
        Overriding GET method to return Cached List of objects if exists, else create one
        """
        data = cache.get("products_list")

        if data is None:
            response = super().get(request, *args, **kwargs)
            data = response.data
            cache.set("products_list", data, 60 * 10)
        return Response(data)

    def perform_create(self, serializer):
        """
        Overriding perform_create() to handle slug and delete cache to keep the data updated.
        """
        product_name = serializer.validated_data.get("name")
        slug = slugify(product_name)
        unique_id = str(uuid.uuid4())[:8]

        if Product.objects.filter(slug=slug).exists():
            slug = f"{slug}-{unique_id}"

        serializer.save(slug=slug)
        cache.delete("products_list")


class ProductUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update, Delete view using Generics.

    GET, PUT, PATCH, DELETE Product using PK.
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    # permission_classes = [ProductPermissions]

    def put(self, request, *args, **kwargs):
        """
        Overiding PUT method to delete cache.
        """
        product_id = kwargs["pk"]
        product = Product.objects.get(id=product_id)
        print(f"Product: {product}")
        product_slug = product.slug
        cache.delete(f"product_{product_slug}")
        cache.delete(f"products_list")
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Overiding DELETE method to delete cache.
        """
        product_id = kwargs["pk"]
        product = Product.objects.get(id=product_id)
        product_slug = product.slug
        cache.delete(f"product_{product_slug}")
        cache.delete(f"products_list")
        return super().put(request, *args, **kwargs)


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
        cache_key = f"product_{slug}"
        product = cache.get(cache_key)

        if product is None:
            try:
                product = Product.objects.get(slug=slug)
                cache.set(cache_key, product)
            except Product.DoesNotExist:
                raise Http404("Product does not exist")
        return product


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
# * 7. When the Order has been successfully placed, a new payment will be created
# * 8.

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


@api_view(["POST"])
def create_payment_intent(request):
    """
    Create a payment intent for a given order.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing the client secret of the payment intent.

    Raises:
        Exception: If there is an error creating the payment intent.

    """
    total_amount = request.data.get("total_amount")
    order_id = request.data.get("order_id")
    order = Order.objects.get(id=order_id)
    customer_name = f"{order.customer.first_name} {order.customer.last_name}"
    customer_email = order.customer.email

    try:
        # check if user with this email already exists at Stripe
        existing_customer = stripe.Customer.list(email=customer_email, limit=1).data
        if existing_customer and len(existing_customer) > 0:
            # Customer already exists, return the existing customer ID
            customer_id = existing_customer[0].id
        else:
            # New Customer -> Create a new customer at Stripe
            new_customer = stripe.Customer.create(
                email=customer_email,
                name=customer_name,
                description="Customer Created by Django Backend",
            )
            customer_id = new_customer.id
        # Create new PaymentIntent at Stripe
        intent = stripe.PaymentIntent.create(
            amount=total_amount,
            currency="usd",
            customer=customer_id,
            metadata={
                "customer_name": customer_name,  # Customer's name as metadata
                "customer_email": customer_email,  # Customer's email as metadata
                "order_id": order_id,
            },
        )
        order.payment_intent = intent.client_secret
        order.save()  # Save PaymentIntent in Order
        return JsonResponse(
            {"client_secret": intent.client_secret}
        )  # returning Payment Intent
    except Exception as e:
        return Response({"error": str(e)}, status=400)

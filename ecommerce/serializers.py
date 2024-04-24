from rest_framework import serializers
from .models import Product_Category, Color, Product, Attribute, Image, Order, OrderItem


class Product_CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Category
        fields = "__all__"


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "quantity"]

    try:

        def create(self, validated_data):
            """
            Create a new order item.

            Args:
                validated_data (dict): Validated data containing the order item details.

            Returns:
                OrderItem: The created order item.

            Raises:
                serializers.ValidationError: If the product is out of stock or the requested quantity is greater than the available stock.
            """
            attribute_id = validated_data.get(
                "product"
            )  # Product ID is actually Attribute, take a look at the models.
            requested_quantity = validated_data.get("quantity")  # Customer Quantity
            order_id = validated_data.get("order")  # Order of the Customer
            attribute = Attribute.objects.get(
                id=attribute_id.id
            )  # Attribute Object for Stock Quantity
            product = Product.objects.get(
                id=attribute.product.id
            )  # Product Object for Price

            if attribute.stock_quantity >= requested_quantity:
                order = Order.objects.get(id=order_id.id)  # Get Order by id
                attribute.stock_quantity -= (
                    requested_quantity  # Subtract the requested quantity from Stock
                )
                attribute.save()  # save the attribute
                order.total_amount += (
                    product.price
                ) * requested_quantity  # Calculate the total amount
                order.save()  # Save the order

                order_item = OrderItem.objects.create(
                    **validated_data
                )  # Save the Order Item

                return order_item
            elif attribute.stock_quantity < requested_quantity:
                raise serializers.ValidationError(
                    "Product is out of stock or requested quantity is greater than available stock."
                )

    except Exception as e:
        raise serializers.ValidationError(str(e))

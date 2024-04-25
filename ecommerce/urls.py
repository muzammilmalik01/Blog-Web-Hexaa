from django.urls import path
from . import views

urlpatterns = [
    # Product Category URLs
    path(
        "product-category/",
        views.Product_CategoryListCreateAPI.as_view(),
        name="create-list-product-category",
    ),
    path(
        "product-category-detail/<int:pk>/",
        views.Product_CategoryUpdateDelete.as_view(),
        name="update-delete-product-category",
    ),
    # Color URLs
    path(
        "color/",
        views.ColorListCreateAPI.as_view(),
        name="create-list-color",
    ),
    path(
        "color-detail/<int:pk>/",
        views.ColorUpdateDelete.as_view(),
        name="update-delete-color",
    ),
    # Product URLs
    path(
        "products/",
        views.ProductListCreateAPI.as_view(),
        name="create-list-products",
    ),
    path(
        "products-detail/<int:pk>/",
        views.ProductUpdateDelete.as_view(),
        name="update-delete-products",
    ),
    path(
        "products-detail/<str:slug>/",
        views.ProductUpdateDeletebySlug.as_view(),
        name="update-delete-products-slug",
    ),
    # Attribute URLs
    path(
        "attribute/",
        views.AttributeListCreateAPI.as_view(),
        name="create-list-attribute",
    ),
    path(
        "attribute-detail/<int:pk>/",
        views.AttributeUpdateDelete.as_view(),
        name="update-delete-attribute",
    ),
    # Images URLs
    path(
        "product-image/",
        views.ImageListCreateAPI.as_view(),
        name="create-list-image",
    ),
    path(
        "product-images/<int:product_id>/",
        views.ImageListAPIbyProduct.as_view(),
        name="create-list-image-by-product-id",
    ),
    path(
        "product-image-detail/<int:pk>/",
        views.ImageUpdateDelete.as_view(),
        name="update-delete-image",
    ),
    # Order URLs
    path(
        "order/",
        views.OrderListCreateAPI.as_view(),
        name="create-list-order",
    ),
    path(
        "order-detail/<int:pk>",
        views.OrderUpdateDeleteAPI.as_view(),
        name="update-delete-order",
    ),
    # Order Item URLs
    path(
        "order-items/",
        views.OrderItemListAPI.as_view(),
        name="list-order",
    ),
    path(
        "order-items-create/",
        views.OrderItemCreateAPI.as_view(),
        name="create-order",
    ),
    path(
        "order-item-detail/<int:pk>",
        views.OrderItemUpdateDeleteAPI.as_view(),
        name="update-delete-order",
    ),
]

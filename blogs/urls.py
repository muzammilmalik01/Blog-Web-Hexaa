from django.contrib import admin
from rest_framework import permissions
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from posts.views import CreateSubscriptionView
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="Blogging Project APIs",
        default_version="v1",
        description="API documentation for Blogging Web Project",
        terms_of_service="https://youtu.be/dQw4w9WgXcQ?si=Oa678F4uH4XV4k_7",  # HEHE :)
        contact=openapi.Contact(email="muzamil.py@proton.me"),
        license=openapi.License(name="All NASA Licenses"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("accounts.urls")),  # Accounts APIs
    path("categories/", include("category.urls")),  # Categories APIs
    path("tags/", include("tag.urls")),  # Tags APIs
    path("posts/", include("posts.urls")),  # Posts APIs
    path("newsletter/", include("newsletter.urls")),  # Newsletter APIs
    path(
        "premium/", CreateSubscriptionView.as_view(), name="create-premium-account"
    ),  # Get Premium Post Subscription
    # Simple-JWT APIs
    path("api/token/", TokenObtainPairView.as_view(), name="obtain-token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh-token"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="verify-token"),
    # Swagger APIs
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # DJoser APIs
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

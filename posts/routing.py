from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, re_path
from .consumers import NotificationConsumer

websocket_urlpatterns = [
    re_path(r"ws/notifications/$", NotificationConsumer.as_asgi()),
]

"""
This module defines the routing configuration for WebSocket connections in the Django project.

The `websocket_urlpatterns` list contains the URL patterns for WebSocket connections.
In this case, there is a single URL pattern defined using the `re_path` function.
The pattern matches the path "ws/notifications/" and associates it with the `NotificationConsumer` consumer.

Note: This module is used by the Channels framework to handle WebSocket connections.
"""

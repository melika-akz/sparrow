from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Standard HTTP handling (Django views)
    "websocket": AuthMiddlewareStack(  # WebSocket handling
        URLRouter([
            re_path(r'ws/some_channel/$', consumers.ChatConsumer.as_asgi()),  # Your WebSocket consumer
        ])
    ),
})


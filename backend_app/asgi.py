# Using uvicorn

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.auth import AuthMiddlewareStack
from .consumers import StrategyConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/strategies/<str:strategy_id>/", StrategyConsumer.as_asgi()),
        ])
    ),
})
app = application
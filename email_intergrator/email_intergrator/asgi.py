import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path

from message.consumers import ProgressConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'email_intergrator.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    path('ws/progress/', ProgressConsumer.as_asgi()),
                ]
            )
        )
    ),
})

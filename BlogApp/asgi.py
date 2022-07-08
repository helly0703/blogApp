import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BlogApp.settings')
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application



# django_asgi_app = get_asgi_application()

import chat.routing
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    "https": get_asgi_application(),
    "websocket":AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
        )
    ),
})

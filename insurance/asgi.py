import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import notifications.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insurance.settings')
websocket_urlpatterns = []
websocket_urlpatterns += notifications.routing.websocket_urlpatterns

application = ProtocolTypeRouter({
  'http': get_asgi_application(),
  'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})

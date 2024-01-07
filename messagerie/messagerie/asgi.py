
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import os
from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "messagerie.settings")

asgi_application = get_asgi_application()

import chat.routing 
application = ProtocolTypeRouter({
"http": asgi_application,
"websocket": 
    AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(chat.routing.websocket_urlpatterns) 
                ),
            )
})
import os

import django
from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
import example.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tic_tac_toe.settings')
django.setup()

application = ProtocolTypeRouter({
  "http": AsgiHandler(),
  "websocket": AuthMiddlewareStack(
    URLRouter(
      example.routing.websocket_urlpatterns
    )
  ),
  ## IMPORTANT::Just HTTP for now. (We can add other protocols later.)
})
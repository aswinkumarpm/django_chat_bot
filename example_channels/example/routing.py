from django.conf.urls import url
from example.consumers import TicTacToeConsumer, ChatConsumer, NewChatConsumer
from channels import routing
from django.conf.urls import url

websocket_urlpatterns = [
    url(r'^ws/play/(?P<room_code>\w+)/$', TicTacToeConsumer.as_asgi()),
    url(r'^ws/chat/$', ChatConsumer.as_asgi()),
    url(r'^ws/new_chat/$', NewChatConsumer.as_asgi()),

]
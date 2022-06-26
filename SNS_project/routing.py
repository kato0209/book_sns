from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from SNS_App.views import *
from SNS_App.consumer import *

websocket_urlpatterns = [
    path('ws/<str:room_name>', ChatConsumer.as_asgi()),
]
application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
from django.urls import path
from .consumer import *

websocket_urlpatterns = [
    path('ws/api/pong/', PongConsumer.as_asgi()),
]

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/ac/', consumers.MyAsyncConsumer.as_asgi()),  # WebSocket URL
]

from django.urls import path

from .views import RoomView
from .views.direct import DirectView
from .views.message import MessageView

urlpatterns = [
    path('rooms/', RoomView.as_view(), name='create_room'),
    path('rooms/<int:room_id>/', RoomView.as_view(), name='update_room'),
    path('rooms/<int:room_id>/messages', MessageView.as_view(), name='messages'),
    path('directs/', DirectView.as_view(), name='create_direct'),
    path('directs/<int:room_id>/', DirectView.as_view(), name='update_direct'),
]


from django.urls import path

from .views import RoomView, DirectView, DirectDetailView, MessageView

urlpatterns = [
    path('rooms/', RoomView.as_view(), name='create_room'),
    path('rooms/<int:room_id>/', RoomView.as_view(), name='update_room'),
    path('rooms/<int:room_id>/messages', MessageView.as_view(), name='messages'),
    path('directs/', DirectView.as_view(), name='create_direct'),
    path('directs/<int:room_id>/', DirectDetailView.as_view(), name='update_direct'),
]


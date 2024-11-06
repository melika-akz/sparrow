from django.urls import path

from .views import RoomView

urlpatterns = [
    path('rooms/', RoomView.as_view(), name='create_room'),
    path('rooms/<int:room_id>/', RoomView.as_view(), name='update_room'),
]


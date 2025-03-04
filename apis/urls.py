from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import RoomView, DirectView, DirectDetailView, MessageView, RoomDetailView, MessageDetailView, \
    MessageSeenView

router = DefaultRouter()

urlpatterns = [
    path('rooms/', RoomView.as_view(), name='create_room'),
    path('rooms/<int:room_id>/', RoomDetailView.as_view(), name='update_room'),
    path('directs/', DirectView.as_view(), name='create_direct'),
    path('directs/<int:room_id>/', DirectDetailView.as_view(), name='update_direct'),
    path('rooms/<int:room_id>/messages/', MessageView.as_view(), name='message'),
    path('rooms/<int:room_id>/messages/<int:message_id>/', MessageDetailView.as_view(), name='message-detail'),
    path('messages/<int:message_id>/', MessageSeenView.as_view(), name='message-seen'),
]

urlpatterns += router.urls


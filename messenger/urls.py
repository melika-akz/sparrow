from django.urls import path
from rest_framework.routers import DefaultRouter

from .views.member_room import MemberRoomView
from .views.room import RoomView, RoomDetailView
from .views.message import MessageView, MessageDetailView, MessageSeenView
from .views.direct import DirectView, DirectDetailView
from .views import UnreadCountView

router = DefaultRouter()

urlpatterns = [
    path('rooms/', RoomView.as_view(), name='create_room'),
    path('rooms/<int:room_id>/', RoomDetailView.as_view(), name='update_room'),
    path('directs/', DirectView.as_view(), name='create_direct'),
    path('directs/<int:room_id>/', DirectDetailView.as_view(), name='update_direct'),
    path('rooms/<int:room_id>/messages/', MessageView.as_view(), name='message'),
    path('rooms/<int:room_id>/messages/<int:message_id>/', MessageDetailView.as_view(), name='message-detail'),
    path('rooms/unread-counts/', UnreadCountView.as_view(), name='unread-counts'),
    path('messages/<int:message_id>/', MessageSeenView.as_view(), name='message-seen'),
    path('member/rooms/', MemberRoomView.as_view(), name='member-rooms'),
]

urlpatterns += router.urls


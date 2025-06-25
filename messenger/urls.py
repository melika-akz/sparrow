from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UnreadCountView, DirectView, DirectDetailView, MessageView, MessageDetailView, MessageSeenView, \
    RoomView, RoomDetailView, MemberRoomView, MessageCountView, RoomMemberJoinView, RoomMemberLeaveView, \
    RoomMemberAddView, RoomMemberRemoveView

router = DefaultRouter()

urlpatterns = [
    path('rooms/', RoomView.as_view(), name='create_room'),
    path('rooms/<int:room_id>/', RoomDetailView.as_view(), name='update_room'),
    path('directs/', DirectView.as_view(), name='create_direct'),
    path('directs/<int:room_id>/', DirectDetailView.as_view(), name='update_direct'),
    path('rooms/<int:room_id>/messages/', MessageView.as_view(), name='message'),
    path('rooms/<int:room_id>/messages/counts/', MessageCountView.as_view(), name='message'),
    path('rooms/<int:room_id>/messages/<int:message_id>/', MessageDetailView.as_view(), name='message-detail'),
    path('rooms/unread-counts/', UnreadCountView.as_view(), name='unread-counts'),
    path('messages/<int:message_id>/', MessageSeenView.as_view(), name='message-seen'),
    path('member/rooms/', MemberRoomView.as_view(), name='member-rooms'),
    path('rooms/<int:room_id>/members/join/', RoomMemberJoinView.as_view(), name='room-members-join'),
    path('rooms/<int:room_id>/members/leave/', RoomMemberLeaveView.as_view(), name='room-members-leave'),
    path('rooms/<int:room_id>/members/add/', RoomMemberAddView.as_view(), name='room-members-add'),
    path('rooms/<int:room_id>/members/remove/', RoomMemberRemoveView.as_view(), name='room-members-remove'),
]

urlpatterns += router.urls


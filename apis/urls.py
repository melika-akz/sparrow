from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RoomViewSet
from .views.member import MemberViewSet


router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'members', MemberViewSet)
# router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
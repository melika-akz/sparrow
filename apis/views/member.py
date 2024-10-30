from rest_framework import viewsets, status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from authorize.models import User
from ..serializers import MemberSerializer


class MemberViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = MemberSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed("POST", detail="User creation is not allowed.")


from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from authorize.models import User
from ..serializers import MemberSerializer


class MemberViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            return Response(self.get_serializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        return super().partial_update(request, *args, **kwargs)


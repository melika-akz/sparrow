from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .entities import UserRepository
from .models import User
from .serializers import DRFTokenSerializer, UserSerializer


class TokenController(TokenObtainPairView):
    serializer_class = DRFTokenSerializer


class MemberView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method in ['PUT']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"id": user.id, "title": user.title, "email": user.email},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, member_id):
        member = UserRepository.get_by_id(member_id)
        serializer = UserSerializer(member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

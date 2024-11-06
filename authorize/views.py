from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .entities import MemberRepository
from .models import Member
from .serializers import DRFTokenSerializer, MemberSerializer


class TokenController(TokenObtainPairView):
    serializer_class = DRFTokenSerializer


class MemberView(APIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def get_permissions(self):
        if self.request.method in ['PUT']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def post(self, request):
        serializer = MemberSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"id": user.id, "title": user.title, "email": user.email},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, member_id):
        member = UserRepository.get_by_id(member_id)
        serializer = MemberSerializer(member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        objects = Member.objects.all()
        serializer = MemberSerializer(objects, many=True)
        return Response(serializer.data)


class MemberDetailView(APIView):
    def get(self, request, member_id):
        member = UserRepository.get_by_id(member_id)
        serializer = MemberSerializer(member)
        return Response(serializer.data)


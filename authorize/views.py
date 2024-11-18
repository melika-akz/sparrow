from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Q

from .entities import MemberRepository
from .models import Member
from .serializers import DRFTokenSerializer, MemberSerializer


class TokenController(TokenObtainPairView):
    serializer_class = DRFTokenSerializer


class MemberView(APIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def post(self, request):
        serializer = MemberSerializer(data=request.data)

        if serializer.is_valid():
            member = serializer.save()
            return Response(
                {"id": member.id, "title": member.title, "email": member.email},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        search_query = request.query_params.get('search', None)
        first_name = request.query_params.get('first_name', None)
        last_name = request.query_params.get('last_name', None)
        email = request.query_params.get('email', None)

        filter_conditions = Q()
        if search_query:
            filter_conditions |= Q(first_name__icontains=search_query)
            filter_conditions |= Q(last_name__icontains=search_query)
            filter_conditions |= Q(email__icontains=search_query)

        if first_name:
            filter_conditions &= Q(first_name__icontains=first_name)

        if last_name:
            filter_conditions &= Q(last_name__icontains=last_name)

        if email:
            filter_conditions &= Q(email__icontains=email)

        members = Member.objects.filter(filter_conditions)

        page_size = request.query_params.get('page_size', 10)
        page = request.query_params.get('page', 1)
        start = (int(page) - 1) * int(page_size)
        end = start + int(page_size)
        paginated_members = members[start:end]

        serializer = MemberSerializer(paginated_members, many=True)
        return Response({"count": members.count(), "results": serializer.data}, status=status.HTTP_200_OK)


class MemberDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, member_id):
        member = MemberRepository.get_by_id(member_id)
        serializer = MemberSerializer(member)
        return Response(serializer.data)


    def put(self, request, member_id):
        member = MemberRepository.get_by_id(member_id)
        serializer = MemberSerializer(member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


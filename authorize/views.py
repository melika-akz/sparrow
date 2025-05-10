from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Q
from rest_framework import status
from django.contrib.auth.models import User
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework_simplejwt.tokens import RefreshToken  # If using JWT

from .entities import MemberRepository
from .models import Member
from .paginations import MemberPagination
from .serializers import DRFTokenSerializer, MemberSerializer


class TokenController(TokenObtainPairView):
    serializer_class = DRFTokenSerializer


class MemberView(APIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    pagination_class = MemberPagination


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

        paginator = self.pagination_class()
        paginated_members = paginator.paginate_queryset(members, request)
        serializer = MemberSerializer(paginated_members, many=True)

        return paginator.get_paginated_response(serializer.data)


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


import random
import string
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class GoogleLoginView(APIView):
    queryset = Member.objects.all()

    def post(self, request):
        # ایجاد یک state تصادفی و ذخیره آن در session
        state = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        request.session['oauth_state'] = state  # ذخیره state در session

        # آدرس بازگشتی و پارامترهای لازم
        redirect_uri = "http://localhost:8000/auth/google/callback/"
        client_id = settings.GOOGLE_CLIENT_ID
        scope = "openid email profile"
        response_type = "code"

        # ساخت URL درخواست گوگل برای ورود
        url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type={response_type}&scope={scope}&state={state}"

        # هدایت کاربر به صفحه احراز هویت گوگل
        return Response({"redirect_url": url})
    

import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class GoogleCallbackView(APIView):
    queryset = Member.objects.all()


    def get(self, request):
        # دریافت کد و state از درخواست
        code = request.GET.get('code')
        state = request.GET.get('state')

        if not code or not state:
            return Response({'error': 'Missing code or state'}, status=status.HTTP_400_BAD_REQUEST)

        # مقایسه state دریافتی با مقداری که در session ذخیره کردیم
        stored_state = request.session.get('oauth_state')
        print(state, stored_state)
        if state != stored_state:
            return Response({'error': 'State mismatch'}, status=status.HTTP_400_BAD_REQUEST)

        # ارسال درخواست برای دریافت توکن با استفاده از کد دریافتی
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": "http://localhost:8000/auth/google/callback/",
            "grant_type": "authorization_code",
        }
        token_resp = requests.post(token_url, data=data)
        if token_resp.status_code != 200:
            return Response({'error': 'Failed to get token', 'details': token_resp.json()}, status=status.HTTP_400_BAD_REQUEST)

        # دریافت اطلاعات کاربر با استفاده از توکن
        token_data = token_resp.json()
        access_token = token_data.get("access_token")

        userinfo_url = "https://openidconnect.googleapis.com/v1/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        userinfo_resp = requests.get(userinfo_url, headers=headers)
        if userinfo_resp.status_code != 200:
            return Response({'error': 'Failed to get userinfo', 'details': userinfo_resp.json()}, status=status.HTTP_400_BAD_REQUEST)

        # اطلاعات کاربر دریافت شده
        userinfo = userinfo_resp.json()

        # اینجا می‌توانید کاربر را بسازید یا لاگین کنید
        # مثلاً: user, created = User.objects.get_or_create(email=userinfo['email'], defaults={'name': userinfo['name']})

        # بازگشت اطلاعات کاربر و توکن‌ها
        return Response({
            "user": userinfo,
            "tokens": token_data
        })


from rest_framework_simplejwt.serializers import AuthUser, TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token
from rest_framework import serializers
from .models import User


class DRFTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        token = super().get_token(user)
        token['email'] = user.email
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'title', 'email']  # Include any other fields you need


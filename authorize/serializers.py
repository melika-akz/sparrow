from rest_framework import serializers
from rest_framework_simplejwt.serializers import AuthUser, TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

from .models import Member


class DRFTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        token = super().get_token(user)
        token['email'] = user.email
        return token



class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'title', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        member = Member.objects.create(**validated_data, password=password)
        member.set_password(password)
        member.save()
        return member

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance.title = validated_data.get('title', instance.title)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_system = validated_data.get('is_system', instance.is_system)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class MemberDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    is_staff = serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = [
            'id',
            'title',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'date_joined',
            'modified_at',
            'is_admin',
            'is_staff',
            'is_system',
        ]
        read_only_fields = [
            'id',
            'date_joined',
            'modified_at',
            'is_admin',
            'is_staff',
            'is_system',
        ]

    def get_full_name(self, obj):
        return obj.full_name()

    def get_is_staff(self, obj):
        return obj.is_staff

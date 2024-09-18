from rest_framework import serializers
from authorize.models import User


class MemberSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)  # Optional for updates

    class Meta:
        model = User
        fields = ['id', 'title', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data, password=password)
        return user

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

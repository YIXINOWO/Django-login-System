from rest_framework import serializers
from .models import UserInfo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['id', 'username', 'email', 'age', 'created_at']
        read_only_fields = ['created_at']

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['username', 'password', 'email', 'age']
        extra_kwargs = {'password': {'write_only': True}} 
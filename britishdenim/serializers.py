from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=200, required=True)
    password = serializers.CharField(write_only=True, max_length=200, required=True, style={'input_type': 'password'})
    

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email']
        read_only_fields = ['id', 'first_name', 'last_name', 'email']


class LogoutSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = []

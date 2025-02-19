from django.contrib.auth.models import User
from rest_framework import serializers


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class SigninSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

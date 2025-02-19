from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from user.serializer import SignupSerializer, SigninSerializer


class UserViewSet(viewsets.ViewSet):
    def signup(self, request):
        """user signup

        """
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # check whether user is existed
            if User.objects.filter(email=email).exists():
                data = {'error': 'email existed'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            # create user
            user = User.objects.create_user(username=email, email=email, password=password)
            data = {
                'id': user.id,
                'email': user.email
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def signin(self, request):
        """user signin

        """
        serializer = SigninSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(username=email, email=email, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                data = {
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token),
                }
                return Response(data, status=status.HTTP_200_OK)
            data = {'data': 'email or password error'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def me(self, request):
        """profile

        """
        user = request.user
        if user.is_authenticated:
            data = {
                'id': user.id,
                'email': user.email
            }
            return Response(data, status=status.HTTP_200_OK)
        data = {'data': 'please signup or signin first.'}
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)

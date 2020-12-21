from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from identity import serializers as sz 

class UserCreationView(viewsets.ModelViewSet):

    permission_classes = (AllowAny,)
    http_method_names = ['post']
    queryset = User.objects.all()
    serializer_class = sz.UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if User.objects.filter(email=serializer.data.get('email')).exists():
            return Response(data={'response': {}, 'message': 'Email already registered', 'error_type': 201, 'status': False},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User(first_name=serializer.data.get('first_name'),
                    last_name=serializer.data.get('last_name'),
                    email=serializer.data.get('email'),
                    username=serializer.data.get('email'),
                    is_active=True)
        user.set_password(serializer.data.get('password'))
        user.save()
        token = Token.objects.create(user=user)

        return Response(data={'token': token.key,
                              'message': 'Thank you for registering stack app',
                              },
                        status=status.HTTP_200_OK)

class UserLoginView(viewsets.ModelViewSet):
   
    permission_classes = (AllowAny,)
    http_method_names = ['post']
    queryset = User.objects.all()
    serializer_class = sz.UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            return Response(data={"message": "Invalid email or password"},
                            status=status.HTTP_400_BAD_REQUEST)
       

        user = serializer.validated_data['user']
        old_token = Token.objects.filter(user=user)
        if old_token.exists():
            old_token[0].delete()
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key,
                         "message": "Login Successfully",
                         },
                        status=status.HTTP_200_OK)


class LogoutView():
	pass



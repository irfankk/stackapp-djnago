from django.contrib.auth import authenticate
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import serializers, exceptions



class UserRegisterSerializer(serializers.ModelSerializer):
    """
    User Registration serializer
    """
    
    email = serializers.EmailField()
    password = serializers.CharField()
    last_name = serializers.CharField()
    first_name = serializers.CharField()

    class Meta:
        model = User
        fields = ("first_name", 'last_name', 'email',  'password')

  

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs

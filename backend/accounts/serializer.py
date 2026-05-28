
from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,min_length=8)

    class Meta:
        model=User
        fields=['email','name','password']

    def validate(self,data):
        email=data.get('email')
        password=data.get('password')
        name=data.get('name')
        if not email:
            raise serializers.ValidationError('Email needed')
        if not password:
            raise serializers.ValidationError('Password needed')
        if not name:
            raise serializers.ValidationError('Name needed')
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError('User already exists')
        return data
        

    
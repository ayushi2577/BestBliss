
from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['email','name','password']
        extra_kwargs={'password':{'write_only':True}}

    def validate_email(self, mail):
        if User.objects.filter(email=mail).exists():
            raise serializers.ValidationError("A user with this email already exists.") 
        return mail
    def create(self, validated_data):
        user=User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name']
        )
        return user
        

    
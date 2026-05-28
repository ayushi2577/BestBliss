from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import OTP
import random
from django.conf import settings
from django.core.mail import send_mail

User=get_user_model()

def generate_otp(email,password,name):
    if User.objects.filter(email=email).exists():
        raise Exception('User already exists')
    OTP.objects.filter(email=email,purpose='signup').delete()
    password=make_password(password)
    code=random.randint(100000,999999)
    OTP.objects.create(email=email,temp_password=password,name=name,code=str(code),purpose='signup')
    return code

def send_otp(email,code,purpose):
    if purpose=='signup':
        subject='Signup OTP'
        message='Your OTP is for signup is {}'.format(code)
    else:
        raise Exception('Invalid purpose')
    send_mail(subject,message,settings.DEFAULT_FROM_EMAIL,[email])

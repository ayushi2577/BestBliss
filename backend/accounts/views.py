from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializer import RegisterSerializer

from .models import OTP
from .utils import generate_otp,send_otp
from datetime import timedelta
from django.utils.timezone import now

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

User=get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def SendOTP(request):
    s=RegisterSerializer(data=request.data)
    if s.is_valid():
        email=s.validated_data.get('email')
        password=s.validated_data.get('password')
        name=s.validated_data.get('name')
        code=generate_otp(email=email,password=password,name=name)
        send_otp(email=email,code=code,purpose='signup')
        return Response({'message':'OTP sent to your email'},status=200)
    return Response(s.errors,status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def VerifyandRegister(request):
    data=request.data
    code=data.get('code')
    if not code:
        return Response({'error':'Code needed'},status=400)
    email=data.get('email')
    if  not email:
        return Response({'error':'Email needed'},status=400)
    try:

        otp=OTP.objects.filter(email=email,code=code,is_used=False,purpose='signup',created_at__gte=now() - timedelta(minutes=10)).latest('created_at')
    except OTP.DoesNotExist:
        return Response({'error':'Invalid code'},status=400)
    otp.is_used=True
    otp.save()
    password=otp.temp_password
    User.objects.create(email=otp.email,password=password,name=otp.name)
    return Response({'message':'User created successfully'},status=200)

@api_view(['POST'])
@permission_classes([AllowAny])
def Googleauth(request):
    token = request.data.get('token')
    if not token:
        return Response({'error':'Token needed'},status=400)
    try:
        google_data=id_token.verify_oauth2_token(token,google_requests.Request(),settings.GOOGLE_CLIENT_ID)
    except:
        return Response({'error':'Invalid token'},status=400)
    email=google_data.get('email')
    name=google_data.get('name')
    user,created=User.objects.get_or_create(email=email,defaults={'name': name})
    if created:
        user.set_unusable_password()
        user.save()
    refresh=RefreshToken.for_user(user)
    return Response({
    'access': str(refresh.access_token),
    'refresh': str(refresh),
    'created': created
}, status=200)
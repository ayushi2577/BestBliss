from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView,TokenRefreshView

urlpatterns=[
    path('signupotp/',SendOTP,name='signupotp'),
    path('verifyandregister/',VerifyandRegister,name='verifyandregister'),
    path('google/',Googleauth,name='googleauth'),
    path('login/',TokenObtainPairView.as_view(),name='login'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('logout/',TokenBlacklistView.as_view(),name='logout')
]
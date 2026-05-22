from django.urls import path
from .views import *
from .smart_view import smart

urlpatterns=[
    path('dashboard/',Dashboard,name='dashboard'),
    path('stay/',stay,name='stay'),
    path('loyalty/',loyalty,name='loyalty'),
    path('smart/',smart,name='smart'),
    path('dining/order/',place_order,name='place_order'),
] 
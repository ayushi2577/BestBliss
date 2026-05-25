from django.urls import path
from .views import *
from .smart_view import smart

urlpatterns=[
    path('dashboard/',Dashboard,name='dashboard'),

    path('stay/',stay,name='stay'),
    path('stays/booking/',BookingViewSet.as_view(),name='booking'),

    path('loyalty/',loyalty,name='loyalty'),

    path('smart/',smart,name='smart'),

    path('orders/food/',FoodOrderViewSet.as_view(),name='get_orders'),
    path('orders/offers/',OfferOrderViewSet.as_view(),name='offer_order'),
    path('orders/events/',EventBookingViewSet.as_view(),name='event_booking'),
    path('orders/redemptions/',RedemptionViewSet.as_view(),name='redemption'),
] 
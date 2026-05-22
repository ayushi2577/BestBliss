from rest_framework import serializers
from .models import *

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model=Rooms
        fields='__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bookings
        fields='__all__'

class Weekly_eventSerializer(serializers.ModelSerializer):
    class Meta:
        model=weekly_events
        fields='__all__'

class Membership_planSerializer(serializers.ModelSerializer):
    class Meta:
        model=membership_plans
        fields='__all__'

    def __init__(self,*args,**kwargs):
        fields=kwargs.pop('fields',None)   #poping out fields from kwargs to use it for dynamic feilds in serializer
        super().__init__(*args,**kwargs)         #for getting self.fields meanss all feilds serialized

        if fields:
            fields=set(fields)
            for i in set(self.fields)-fields:
                self.fields.pop(i)

class Food_menuSerializer(serializers.ModelSerializer):
    class Meta:
        model=food_menu
        fields='__all__'

class Special_eventSerializer(serializers.ModelSerializer):
    class Meta:
        model=special_events
        fields='__all__'

class RedemptionitemsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Redemption_items
        fields='__all__'

class PrivilagesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Privilages
        fields='__all__'

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model=Orders
        fields='__all__'



        

# Create your views here.

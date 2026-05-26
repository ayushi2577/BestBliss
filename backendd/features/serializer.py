
from datetime import date

from rest_framework import serializers
from .models import *

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model=Rooms
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

#========================================================BOOKING AND ORDERS SERIALIZERS========================================================

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bookings
        fields='__all__'
        read_only_fields=['user','total_price']  #allow validate to not expect these feilds from request data as they will be calculated in create method
    
    def validate(self,data):
        if data.get('check_in_date') < date.today():
            raise serializers.ValidationError("Check-in date cannot be in the past.")
        if data.get('check_out_date') <= data.get('check_in_date'):
            raise serializers.ValidationError("Check-out date must be after check-in date.")
        return data
    
    def create(self, validated_data):
        user = self.context['request'].user
        room_number = validated_data.get('room_number')
        check_in_date = validated_data.get('check_in_date')
        check_out_date = validated_data.get('check_out_date')

        # Calculate total price based on room price and number of nights
        nights = (check_out_date - check_in_date).days
        total_price = room_number.price * nights    #room_number is a object as done by validate_data --it convert automatically in dtype needded

        booking = Bookings.objects.create(
            user=user,
            room_number=room_number,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            total_price=total_price
        )
        return booking
    

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model=Orders
        fields='__all__'
        read_only_fields = ['user', 'total_price']
    
    def create(self, validated_data):
        user = self.context['request'].user
        items = validated_data.get('items', [])
        total = sum(item.price for item in items)
        order = Orders.objects.create(user=user, total_price=total)
        order.items.set(items)
        return order

    
class OfferorderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Offerorder
        fields='__all__'
        read_only_fields=['user']  #allow validate to not expect these feilds from request data as they will be calculated in create method

    def validate(self,data):
        offer=data.get('offer')
        if not offer:
            raise serializers.ValidationError("Offer must be selected.")
        user = self.context['request'].user
        if offer.plan_name != user.membership:
            raise serializers.ValidationError("This offer is not available for your membership tier.")
        return data
    
    def create(self, validated_data):
        user = self.context['request'].user
        offer = validated_data['offer']
        
        order = Offerorder.objects.create(user=user, offer=offer)
        return order

class EventBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model=EventBooking
        fields='__all__'
        read_only_fields=['user']  #allow validate to not expect these feilds from request data as they will be calculated in create method

    def validate(self,data):
        event=data.get('event')
        if not event:
            raise serializers.ValidationError("Event must be selected.")
        return data

    def create(self, validated_data):
        user = self.context['request'].user 
        event = validated_data['event']
        order = EventBooking.objects.create(user=user, event=event)
        return order


class RedemptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Redemption
        fields='__all__'
        read_only_fields=['user']  #allow validate to not expect these feilds from request data as they will be calculated in create method

    def validate(self,data):
        item=data.get('item')
        if not item:
            raise serializers.ValidationError("Redemption item must be selected.")
        if not Redemption_items.objects.filter(item_name=item).exists():
            raise serializers.ValidationError(f"Redemption item '{item}' does not exist.")
        return data
    
    def create(self, validated_data):
        user = self.context['request'].user
        item= validated_data['item']
        if user.reward_points < item.points_required:
            raise serializers.ValidationError("Insufficient reward points.")
        redemption = Redemption.objects.create(user=user, item=item)
        user.reward_points -= item.points_required
        user.save()
        return redemption


        

# Create your views here.

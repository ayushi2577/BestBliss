from httpcore import request

from .serializer import *
from .models import weekly_events,special_events,membership_plans
from datetime import date
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import APIView  

from datetime import date,timedelta 
from django.utils import timezone

# 1. Get the current time minus 10 minutes
ten_minutes_ago = timezone.now() - timedelta(minutes=10)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Dashboard(request):
    name=request.user.name

    rooms=request.user.user_bookings.all()
    rSerialzier=BookingSerializer(rooms,many=True)
    rooms=rSerialzier.data

    special=special_events.objects.filter(event_date=date.today())
    if special.exists():
        event=special
        serializer = Special_eventSerializer(event,many=True)
    else:
        event=weekly_events.objects.filter(event_day=date.today().strftime("%A") )
        serializer = Weekly_eventSerializer(event,many=True)
    event=serializer.data

    offer=membership_plans.objects.filter(plan_name=request.user.membership)
    offer_serializer=Membership_planSerializer(offer,fields=['offer_title','offer_description'],many=True)
    offer=offer_serializer.data

    return Response({
        "name":name,
        "rooms":rooms,
        "event":event,
        "offer":offer,
        "membership_status":request.user.membership,
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stay(request):
    query=Bookings.objects  .filter(user=request.user)
    serializer=BookingSerializer(query,many=True)
    rooms=serializer.data
    upcoming=[]
    past=[]
    current=[]
    for room in rooms:
        if room['check_out_date'] < str(date.today()):
            past.append(room)
        elif room['check_in_date'] > str(date.today()):
            upcoming.append(room)
        else:
            current.append(room)
    return Response({"upcoming":upcoming,"past":past,"current":current})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def loyalty(request):
    membership=request.user.membership
    point=request.user.reward_points
    referal_link=request.user.referal_link
    points_needed=membership_plans.objects.filter(tier_level__gt=request.user.tier_level).order_by('tier_level').first().price or 0
    privilages=PrivilagesSerializer(Privilages.objects.filter(tier_level=request.user.tier_level),many=True).data
    return Response({
        "membership":membership,
        "reward_points":point,
        "referal_link":referal_link,
        "privilages":privilages,
        "points_needed":points_needed
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):
    items_name=request.data.get('items',[])
    items=[]
    for i in items_name:
        f=food_menu.objects.filter(item_name=i['name'],availability=True).first()
        if f:
            items.append(f)
    if not items:
        return Response({"error": "No valid items selected"}, status=400)
    total=request.data.get('total',0)
    order=Orders.objects.create(user=request.user,total_price=float(total))
    order.items.set(items)
    order.save()

    return Response({"message":"Order placed successfully"
                     ,"order_id": order.id})

class BookingViewSet(APIView):
    def post(self, request):
        room_name=request.data.get('room_name')
        check_in_date=request.data.get('check_in_date')
        check_out_date=request.data.get('check_out_date')

        if not all([room_name, check_in_date, check_out_date]):
            return Response({"error": "Missing required fields"}, status=400)

        room=Rooms.objects.filter(room_name=room_name).room_number
        booking = Bookings.objects.create(
            user=request.user,
            room_number=room,
            check_in_date=check_in_date,
            check_out_date=check_out_date
        )

        serializer = BookingSerializer(booking)
        return Response({'message':'success'})
    
    def get(self,request):
        bookings=Bookings.objects.filter(user=request.user)
        data=BookingSerializer(bookings,many=True)
        return Response({'bookings':data})
    
    def delete(self,request):
        booking_id=request.data.get('booking_id')
        booking=Bookings.objects.filter(id=booking_id)
        if not booking.exists():
            return Response({'error':'Booking not found'})
        if request.user!=booking.user:
            return Response({'error':'Unauthorized access'})
        elif booking.check_in_date <= date.today():
            return Response({'error':'Cannot cancel past or current bookings'})
        if booking.date!=date.today():
            return Response({'error':'Bookings can only be cancelled on the day of booking'})
        Bookings.objects.delete(id=booking_id)
        return Response({'message':'Booking cancelled successfully'})

    
class FoodOrderViewSet(APIView):
    def post(self,request):
        items_name=request.data.get('items',[])
        items=[]
        for i in items_name:
            f=food_menu.objects.filter(item_name=i['name'],availability=True).first()
            if f:
                items.append(f)
        if not items:
            return Response({"error": "No valid items selected"}, status=400)
        total=request.data.get('total',0)
        order=Orders.objects.create(user=request.user,total_price=float(total))
        order.items.set(items)
        order.save()

        return Response({"message":"Order placed successfully"
                         ,"order_id": order.id})
    
    def get(self,request):
        orders=Orders.objects.filter(user=request.user)
        data=OrdersSerializer(orders,many=True)
        return Response({'orders':data})
    
    def delete(self,request):
        order_id=request.data.get('order_id')
        order=Orders.objects.filter(id=order_id)
        if not order.exists():
            return Response({'error':'Order not found'})
        if request.user!=order.user:
            return Response({'error':'Unauthorized access'})
        elif order.order_date.date() != date.today() or order.order_time > ten_minutes_ago.time():
            return Response({'error':'Orders can only be cancelled on the day of order'})
        Orders.objects.delete(id=order_id)
        return Response({'message':'Order cancelled successfully'})
    
class OfferOrderViewSet(APIView):    
    def post(self,request):
        offer_id=request.data.get('offer_id')
        offer=membership_plans.objects.filter(id=offer_id).first()
        if not offer:
            return Response({'error':'Offer not found'})
        order=Offerorder.objects.create(user=request.user,offer=offer)
        return Response({'message':'Offer ordered successfully','order_id':order.id})

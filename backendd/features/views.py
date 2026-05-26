
from .serializer import *
from .models import weekly_events,special_events,membership_plans
from datetime import date, datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from datetime import date,timedelta 
from django.utils import timezone


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
def getrooms(request):
    query=Rooms.objects.filter(availability=True)
    serializer=RoomSerializer(query,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def loyalty(request):
    Redemption_query=Redemption_items.objects.all()
    Redemption_items=RedemptionitemsSerializer(Redemption_query,many=True).data
    membership=request.user.membership
    point=request.user.reward_points
    referal_link=request.user.referal_link
    next_plan = membership_plans.objects.filter(tier_level__gt=request.user.tier_level).order_by('tier_level').first()
    points_needed = next_plan.price if next_plan else 0
    privilages=PrivilagesSerializer(Privilages.objects.filter(tier_level=request.user.tier_level),many=True).data
    return Response({
        "membership":membership,
        "reward_points":point,
        "referal_link":referal_link,
        "privilages":privilages,
        "points_needed":points_needed,
        "redemption_items":Redemption_items
    })


class BookingViewSet(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        serializer=BookingSerializer(data=request.data,context={"request":request})
        if not serializer.is_valid():
            return Response(serializer.errors,status=400)
        serializer.save()
        return Response({'message':'success'})
    
    def get(self,request):
        bookings=Bookings.objects.filter(user=request.user)
        data=BookingSerializer(bookings,many=True).data
        return Response({'bookings':data})
    
    def delete(self,request):
        booking_id=request.data.get('booking_id')
        try:
            booking = Bookings.objects.get(id=booking_id)  # ✅ get() not filter()
        except Bookings.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=404)
        if request.user!=booking.user:
            return Response({'error':'Unauthorized access'})
        elif booking.check_in_date <= date.today():
            return Response({'error':'Cannot cancel past or current bookings'})
        if booking.booking_date.date()!=date.today():
            return Response({'error':'Bookings can only be cancelled on the day of booking'})
        booking.delete()
        return Response({'message':'Booking cancelled successfully'})

    
class FoodOrderViewSet(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        data = request.data.copy()
        item_names = data.get('items', [])
    
        # convert names to IDs
        item_ids = []
        for name in item_names:
            item = food_menu.objects.filter(item_name=name, availability=True).first()
            if not item:
                return Response({'error': f"Item '{name}' is not available."}, status=400)
            item_ids.append(item.id)
    
        data['items'] = item_ids  # replace names with IDs
    
        serializer = OrdersSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self,request):
        orders=Orders.objects.filter(user=request.user)
        data=OrdersSerializer(orders,many=True).data
        return Response({'orders':data})
    
    def delete(self,request):
        order_id=request.data.get('order_id')
        order=Orders.objects.filter(id=order_id).first()
        if not order:
            return Response({'error':'Order not found'})
        if request.user!=order.user:
            return Response({'error':'Unauthorized access'})
        elif (timezone.now() - order.order_date).total_seconds() > 600:  # 10 minutes
            return Response({'error':'Orders can only be cancelled on the day of order'})
        order.delete()
        return Response({'message':'Order cancelled successfully'})
  
class OfferOrderViewSet(APIView):   
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer=OfferorderSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors,status=400)    
        serializer.save()
        return Response({"message":"Offer booked successfully"})
    
    def get(self,request):
        offers=Offerorder.objects.filter(user=request.user)
        data=OfferorderSerializer(offers,many=True).data
        return Response({'offers':data})
    
class EventBookingViewSet(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer=EventBookingSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors,status=400)    
        serializer.save()
        return Response({"message":"Event booked successfully"})
    
    def get(self,request):
        events=EventBooking.objects.filter(user=request.user)
        data=EventBookingSerializer(events,many=True).data
        return Response({'events':data})
    
class RedemptionViewSet(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer=RedemptionSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors,status=400)    
        serializer.save()
        return Response({"message":"Item redeemed successfully"})
    
    def get(self,request):
        redemptions=Redemption.objects.filter(user=request.user)
        data=RedemptionSerializer(redemptions,many=True).data
        return Response({'redemptions':data})
    
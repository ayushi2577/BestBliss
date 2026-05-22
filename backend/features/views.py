from .serializer import *
from.models import weekly_events,special_events,membership_plans

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from datetime import date

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
    query=Rooms.objects.all()
    serializer=RoomSerializer(query,many=True)
    rooms=serializer.data
    return Response({"rooms":rooms})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dining(request):
    starters=Food_menuSerializer(food_menu.objects.filter(type='starter'),many=True).data
    main_course=Food_menuSerializer(food_menu.objects.filter(type='main_course'),many=True).data
    dessert=Food_menuSerializer(food_menu.objects.filter(type='dessert'),many=True).data
    return Response({
        "starters":starters,
        "main_course":main_course,
        "dessert":dessert
    })

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

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Rooms(models.Model):
    room_number=models.CharField(null=False,unique=True,max_length=10)
    room_type=models.CharField(null=False,max_length=20)
    price=models.IntegerField(null=False)
    is_available=models.BooleanField(default=True)
    description=models.CharField(null=False,max_length=500)
    smart_id=models.CharField(null=False,unique=True,max_length=100)
    def __str__(self):
        return self.room_number 
    
class Bookings(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_bookings')
    room_number=models.ForeignKey(Rooms,on_delete=models.CASCADE,related_name='room_bookings')
    check_in_date=models.DateField(null=False)
    check_out_date=models.DateField(null=False)
    total_price=models.IntegerField(null=False)
    booking_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Booking for {self.user.name} - {self.room_number.room_number}"

    
class weekly_events(models.Model):
    event_name=models.CharField(null=False,max_length=100)
    event_description=models.CharField(null=False,max_length=500)
    event_day=models.CharField(null=False,max_length=20)
    event_location=models.CharField(null=False,max_length=100)
    event_time=models.TimeField(null=False)
    def __str__(self):
        return self.event_name

class food_menu(models.Model):
    item_name=models.CharField(null=False,max_length=100)
    item_description=models.CharField(null=False,max_length=500)
    price=models.IntegerField(null=False)
    type=models.CharField(null=False,max_length=20)
    availability=models.BooleanField(default=True)
    def __str__(self):
        return self.item_name
    
class special_events(models.Model):
    event_name=models.CharField(null=False,max_length=100)
    event_description=models.CharField(null=False,max_length=500)
    event_date=models.DateField(null=False)
    event_location=models.CharField(null=False,max_length=100)
    event_time=models.TimeField(null=False)
    def __str__(self):
        return self.event_name
    
class membership_plans(models.Model):
    plan_name=models.CharField(null=False,max_length=100)
    offer_title=models.CharField(null=False,max_length=100)
    offer_description=models.CharField(null=False,max_length=500)
    price=models.IntegerField(null=False)
    def __str__(self):
        return self.plan_name
    
class Privilages(models.Model):
    privilage_name=models.CharField(null=False,max_length=50)
    privilage_desc=models.CharField(null=False,max_length=1000)
    tier_level=models.IntegerField(null=False)

class Redemption_items(models.Model):
    item_name=models.CharField(null=False,max_length=100)
    item_description=models.CharField(null=False,max_length=500)
    points_required=models.IntegerField(null=False)

#when making orders of food then use many to many field

from django.contrib import admin
from .models import (Rooms, Bookings, weekly_events, food_menu, 
                     special_events, membership_plans, Privilages, 
                     Redemption_items, Orders, Offerorder, EventBooking, Redemption)

admin.site.register(Rooms)
admin.site.register(Bookings)
admin.site.register(weekly_events)
admin.site.register(food_menu)
admin.site.register(special_events)
admin.site.register(membership_plans)
admin.site.register(Privilages)
admin.site.register(Redemption_items)
admin.site.register(Orders)
admin.site.register(Offerorder)
admin.site.register(EventBooking)
admin.site.register(Redemption)
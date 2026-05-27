from django.core.management.base import BaseCommand
from features.models import (
    Rooms, weekly_events, food_menu, special_events,
    membership_plans, Privilages, Redemption_items
)


class Command(BaseCommand):
    help = 'Seeds the database with BestBliss production data'

    def handle(self, *args, **options):
        self._seed_rooms()
        self._seed_membership_plans()
        self._seed_privileges()
        self._seed_weekly_events()
        self._seed_special_events()
        self._seed_food_menu()
        self._seed_redemption_items()
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))

    def _seed_rooms(self):
        rooms = [
            dict(room_number='PH-1001', room_type='Royal Penthouse', price=2450, is_available=True,
                 smart_id='SUITE_ROYAL_PH_1001',
                 description='Experience the pinnacle of luxury with 360-degree city views, a private infinity pool, and a dedicated 24/7 butler service.'),
            dict(room_number='GV-202', room_type='Garden Villa', price=1800, is_available=True,
                 smart_id='VILLA_GARDEN_202',
                 description='A tranquil sanctuary featuring a private garden, outdoor rainfall shower, and seamless indoor-outdoor living spaces.'),
            dict(room_number='SS-4512', room_type='Skyline Studio', price=950, is_available=True,
                 smart_id='STUDIO_SKYLINE_4512',
                 description='Perfectly appointed for the modern professional, combining high-speed tech with refined aesthetic comfort.'),
        ]
        created = 0
        for r in rooms:
            _, made = Rooms.objects.get_or_create(room_number=r['room_number'], defaults=r)
            if made: created += 1
        self.stdout.write(f'  Rooms: {created} created.')

    def _seed_membership_plans(self):
        plans = [
            dict(plan_name='Customer',     tier_level=1, price=0,     offer_title='Standard Access',    offer_description='Access to basic community features, standard reward points tracking, and standard support.'),
            dict(plan_name='Bronze Member',tier_level=2, price=1500,  offer_title='Enhanced Rewards',   offer_description='Earn points 10% faster, unlock basic member-only discounts, and get priority email support.'),
            dict(plan_name='Silver Elite', tier_level=3, price=4500,  offer_title='Preferred Status',   offer_description='Earn points 25% faster, receive complimentary quarterly gift boxes, and access 24/7 chat support.'),
            dict(plan_name='Gold VIP',     tier_level=4, price=9900,  offer_title='Premium Privileges', offer_description='Earn points 50% faster, free express shipping on all orders, and a dedicated hotline support agent.'),
            dict(plan_name='Diamond Club', tier_level=5, price=25000, offer_title='Ultimate Luxury',    offer_description='Double points multiplier, unlimited access to VIP airport lounges, and a personal lifestyle concierge.'),
        ]
        created = 0
        for p in plans:
            _, made = membership_plans.objects.get_or_create(plan_name=p['plan_name'], defaults=p)
            if made: created += 1
        self.stdout.write(f'  Membership plans: {created} created.')

    def _seed_privileges(self):
        privileges = [
            dict(tier_level=1, privilage_name='Complimentary Welcome Drink',    privilage_desc='Enjoy a free signature mocktail or beverage curated by our head bartender upon checking in.'),
            dict(tier_level=1, privilage_name='Standard Room Booking',           privilage_desc='Access to standard room reservations with complimentary high-speed Wi-Fi.'),
            dict(tier_level=2, privilage_name="Chef's Special Appetizer",        privilage_desc='Receive a complimentary, off-menu appetizer hand-crafted by the Executive Chef during dinner service.'),
            dict(tier_level=2, privilage_name='Late Checkout Priority',          privilage_desc='Extend your stay with a guaranteed late checkout up to 1:00 PM, subject to availability.'),
            dict(tier_level=3, privilage_name='Priority Restaurant Seating',     privilage_desc='Skip the waitlist with priority table reservations and a complimentary dessert pairing from the pastry chef.'),
            dict(tier_level=3, privilage_name='Complimentary Room Upgrade',      privilage_desc='Get a free upgrade to the next available room category (e.g., Deluxe to Studio) at check-in.'),
            dict(tier_level=4, privilage_name='Bespoke 5-Course Customization',  privilage_desc='Unlock the ability to customize flavor profiles and dietary preferences directly with the culinary team for private dinners.'),
            dict(tier_level=4, privilage_name='Luxury Suite Access',             privilage_desc='Exclusive booking access to our premium Luxury Suites featuring private balconies and panoramic cliffside views.'),
            dict(tier_level=5, privilage_name='In-Suite Personal Chef Experience', privilage_desc='Have our Michelin-starred Executive Chef prepare a bespoke, multi-course meal live in your suite or private terrace.'),
            dict(tier_level=5, privilage_name='Villa Upgrade & Early Check-In',  privilage_desc='Guaranteed early check-in at 10:00 AM and automatic upgrades to top-tier private villas or penthouse suites.'),
        ]
        created = 0
        for p in privileges:
            _, made = Privilages.objects.get_or_create(
                tier_level=p['tier_level'], privilage_name=p['privilage_name'], defaults=p
            )
            if made: created += 1
        self.stdout.write(f'  Privileges: {created} created.')

    def _seed_weekly_events(self):
        events = [
            dict(event_name='Sunset Jazz & Cocktails',   event_day='Monday',    event_location='The Horizon Lounge',       event_time='18:30:00', event_description='Unwind at the start of the week with smooth live jazz performances. Enjoy expert mixologists crafting artisanal cocktails against a backdrop of breathtaking ocean views.'),
            dict(event_name='Masterclass Pastry Tasting', event_day='Tuesday',   event_location='The Grand Atelier',        event_time='15:00:00', event_description='Join our award-winning pastry chef for an intimate dessert showcase. Learn the art of French pastry making while sampling exquisite, freshly baked delicate confections.'),
            dict(event_name='Starlight Cinema Night',     event_day='Wednesday', event_location='The Rooftop Terrace',      event_time='20:00:00', event_description='Experience cinematic masterpieces under the open sky. Recline in luxury loungers with premium popcorn, artisanal snacks, and fine wine as the ocean breeze sweeps by.'),
            dict(event_name="Sommelier's Wine Vault",     event_day='Thursday',  event_location='The Reserve Cellar',       event_time='19:00:00', event_description='Descend into our private underground vault for an exclusive wine tasting. Pair rare vintage reserves with imported cheeses guided by our resident master sommelier.'),
            dict(event_name='Midnight Glow Pool Gala',   event_day='Friday',    event_location='The Oasis Infinity Pool',  event_time='21:30:00', event_description='Kickstart the weekend at our illuminated infinity pool party. Features live ambient electronic sets, glowing underwater lights, and refreshing signature tropical fruit elixirs.'),
            dict(event_name='Grand Coastal Feast',        event_day='Saturday',  event_location='The Riviera Dining Room',  event_time='13:00:00', event_description='Indulge in a spectacular live-station buffet prepared by international culinary teams. Showcases freshly caught seafood, premium grilled meats, and an endless array of gourmet delicacies.'),
            dict(event_name='Zen Sunrise Meditation',     event_day='Sunday',    event_location='The Cliffside Sanctuary',  event_time='06:30:00', event_description='Conclude your week with peaceful, guided mindfulness overlooking the ocean cliffs. Followed by a revitalizing, nutrient-dense organic green juice bar and wellness breakfast buffet.'),
        ]
        created = 0
        for e in events:
            _, made = weekly_events.objects.get_or_create(event_name=e['event_name'], defaults=e)
            if made: created += 1
        self.stdout.write(f'  Weekly events: {created} created.')

    def _seed_special_events(self):
        events = [
            dict(event_name='New Year Party', event_description='DJ night and gala dinner',
                 event_date='2026-12-31', event_location='Banquet Hall', event_time='21:00:00'),
        ]
        created = 0
        for e in events:
            _, made = special_events.objects.get_or_create(event_name=e['event_name'], defaults=e)
            if made: created += 1
        self.stdout.write(f'  Special events: {created} created.')

    def _seed_food_menu(self):
        items = [
            dict(item_name='Truffle Arancini',  type='Starters',     price=24,  availability=True, item_description='Wild mushroom risotto, black truffle essence, aged parmesan snow.'),
            dict(item_name='Burrata Di Puglia', type='Starters',     price=28,  availability=True, item_description='Heirloom tomatoes, basil emulsion, 12-year aged balsamic glaze.'),
            dict(item_name='Lobster Bisque',    type='Starters',     price=32,  availability=True, item_description='Cognac cream, butter-poached lobster medallions, chive oil.'),
            dict(item_name='Wagyu Beef Fillet', type='Main Course',  price=75,  availability=True, item_description='Grade A5, potato mousseline, marrow jus, charred asparagus.'),
            dict(item_name='Miso Glazed Cod',   type='Main Course',  price=62,  availability=True, item_description='Black cod, bok choy, ginger dashi, toasted sesame oil.'),
            dict(item_name='Saffron Risotto',   type='Main Course',  price=48,  availability=True, item_description='Acquerello rice, roasted gold beets, cashew crema, micro-greens.'),
            dict(item_name='Gold Leaf Fondant', type='Desserts',     price=22,  availability=True, item_description='70% Dark chocolate, molten center, vanilla bean gelato.'),
            dict(item_name='Yuzu Tart',         type='Desserts',     price=18,  availability=True, item_description='Shiso crystal, burnt meringue, raspberry coulis splash.'),
            dict(item_name='Artisanal Cheese',  type='Desserts',     price=35,  availability=True, item_description='Selection of 5 regional cheeses, honeycomb, fig preserve.'),
        ]
        created = 0
        for i in items:
            _, made = food_menu.objects.get_or_create(item_name=i['item_name'], defaults=i)
            if made: created += 1
        self.stdout.write(f'  Food menu: {created} created.')

    def _seed_redemption_items(self):
        items = [
            dict(item_name='Private Cliffside Dinner', points_required=85000,  item_description='A bespoke 5-course menu prepared by our executive chef on a private terrace.'),
            dict(item_name='Island Helicopter Tour',   points_required=120000, item_description='See the world from a new perspective with a helicopter tour.'),
            dict(item_name='Vintage Yacht Escape',     points_required=250000, item_description='A full-day charter on our restored 1960s classic yacht including full crew and catering.'),
        ]
        created = 0
        for i in items:
            _, made = Redemption_items.objects.get_or_create(item_name=i['item_name'], defaults=i)
            if made: created += 1
        self.stdout.write(f'  Redemption items: {created} created.')

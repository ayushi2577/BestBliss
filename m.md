<div align="center">

```
██████╗ ███████╗███████╗████████╗██████╗ ██╗     ██╗███████╗███████╗
██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██║     ██║██╔════╝██╔════╝
██████╔╝█████╗  ███████╗   ██║   ██████╔╝██║     ██║███████╗███████╗
██╔══██╗██╔══╝  ╚════██║   ██║   ██╔══██╗██║     ██║╚════██║╚════██║
██████╔╝███████╗███████║   ██║   ██████╔╝███████╗██║███████║███████║
╚═════╝ ╚══════╝╚══════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝╚══════╝╚══════╝
```

### **The Complete Luxury Hotel Web Platform**
*A full-stack, API-driven hotel management and guest engagement system — built for the modern hospitality era.*

---

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/DRF-REST_API-ff1709?style=for-the-badge&logo=django&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

</div>

---

## What is BestBliss?

**BestBliss** is a production-grade, full-stack hotel web platform that transforms the way hotels present themselves and engage their guests online. It is not a simple brochure website — it is a complete guest management ecosystem with a live REST API backend, JWT-secured authentication, dynamic loyalty programs, real-time environmental intelligence, food ordering, room booking, and a multi-page interactive frontend crafted with a luxury aesthetic design system.

> Whether you are a hotel startup looking to launch your first digital presence, or an established property seeking to replace a legacy system with something truly premium, BestBliss provides a ready-to-deploy, deeply functional foundation that you can brand and ship.

---

## Table of Contents

1. [Project Philosophy](#project-philosophy)
2. [Feature Overview](#feature-overview)
3. [Architecture](#architecture)
4. [Tech Stack](#tech-stack)
5. [Data Models](#data-models)
6. [API Reference](#api-reference)
7. [Frontend Pages](#frontend-pages)
8. [Design System](#design-system)
9. [Getting Started](#getting-started)
10. [Project Structure](#project-structure)
11. [Who Should Use BestBliss?](#who-should-use-bestbliss)
12. [BestBliss vs. The Alternatives](#bestbliss-vs-the-alternatives)
13. [Roadmap](#roadmap)
14. [Contributing](#contributing)
15. [License](#license)

---

## Project Philosophy

Most hotel websites are static, impersonal, and disconnected from actual hotel operations. Guests browse room photos, fill out a contact form, and hear nothing until check-in. BestBliss was designed around a fundamentally different belief:

**A hotel's website should be the beginning of the guest relationship, not just a booking form.**

Every feature in BestBliss is driven by three principles:

- **Guest Centricity** — Every authenticated guest gets a personalised dashboard showing their upcoming stays, today's events, and their membership offer — the moment they log in.
- **Operational Integration** — The frontend isn't decorative. It talks to a live backend, records real bookings, processes food orders, manages loyalty points, and tracks redemptions.
- **Brand Elevation** — The entire UI is built around a bespoke luxury design language — dark gold tones, refined typography, glassmorphism panels — so that any hotel using it immediately feels five-star.

---

## Feature Overview

### Guest Authentication & Identity
- Custom user model built on Django's `AbstractBaseUser`, with email as the primary credential — no usernames, no friction
- Auto-generated unique guest IDs using the hotel's own prefix (e.g., `BB-1001`, `BB-1002`), giving every guest a branded identity
- JWT-based authentication with 30-minute access tokens and 1-day rotating refresh tokens
- Token blacklisting on logout, ensuring sessions are properly invalidated — not just abandoned
- Auto-generated unique referral links (`https://bestbliss.com/ref/A7k9PqX2`) for every guest upon registration, enabling word-of-mouth growth

### Personalised Guest Dashboard
- On login, every guest immediately sees: their current bookings (with check-in/check-out status), today's events (special events take priority over recurring weekly events), and their active membership offer
- The dashboard is not a static page — it makes a live API call to `/api/dashboard/` and renders real, current data

### Room Booking & Stay Management
- Live room availability system with room types, descriptions, and per-night pricing
- Smart booking creation: total price is calculated server-side based on the number of nights — no client-side pricing manipulation
- Intelligent booking cancellation: cancellations are only permitted on the day of booking and before check-in, enforcing realistic hotel policies
- Guest stays are automatically categorised into `upcoming`, `current`, and `past` — giving guests clarity on their stay history at a glance

### Dining & Food Ordering
- Full food menu management with item types, descriptions, availability, and pricing
- Guests can place multi-item food orders; items are resolved by name to prevent invalid submissions
- Orders are cancellable within a 10-minute window — a realistic policy that protects kitchen operations
- Full order history is available per guest

### Loyalty & Rewards Program
- A tiered membership system (e.g., Customer → Silver → Gold → Platinum) with plans linked to `tier_level` integers
- Each tier unlocks a unique set of `Privileges` — displayed to the guest on their loyalty dashboard
- Reward point accumulation and redemption system: guests can redeem points for items from a managed `Redemption_items` catalogue
- Real-time display of how many points are needed to reach the next tier, motivating continued engagement
- Offer booking: guests can book membership offers, with server-side validation that the offer matches their current membership tier

### Events System
- Two-tier event architecture: `weekly_events` (recurring, day-of-week based) and `special_events` (date-specific, one-off occasions)
- The dashboard intelligently surfaces special events first when both exist on the same day
- Guests can book their spot at weekly events through the `EventBooking` system

### Smart Environment Intelligence
- A unique value-add feature: the `/api/smart/` endpoint accepts GPS coordinates and returns real-time **temperature**, **humidity**, **UV Index** (with human-readable classification), and **Air Quality Index** (US AQI standard) for any location
- Powered by the free, open-source **Open-Meteo** and **Open-Meteo Air Quality** APIs — no API key required
- Enables hotels to surface live weather and air quality data for their guests — ideal for resort properties, wellness retreats, or city hotels wanting to provide concierge-quality environmental context

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        BestBliss Platform                       │
├─────────────────────────────┬───────────────────────────────────┤
│         FRONTEND            │           BACKEND                 │
│   (Multi-Page HTML/JS)      │      (Django REST API)            │
│                             │                                   │
│  index.html   (Login)       │  /api/login/     → JWT Obtain     │
│  dashboard.html             │  /api/refresh/   → JWT Refresh    │
│  stay.html                  │  /api/logout/    → JWT Blacklist  │
│  manage_stay.html           │  /api/dashboard/ → Guest Summary  │
│  dining.html                │  /api/rooms/     → Room Listing   │
│  order.html                 │  /api/stay/      → Stay History   │
│  loyalty.html               │  /api/stays/booking/ → Bookings  │
│  smart.html                 │  /api/loyalty/   → Rewards Data   │
│  history.html               │  /api/orders/food/ → Food Orders  │
│                             │  /api/orders/offers/ → Offers     │
│  Tailwind CSS               │  /api/orders/events/ → Events     │
│  Material Icons             │  /api/orders/redemptions/         │
│  Playfair Display           │  /api/smart/     → Env. Metrics   │
│  Manrope                    │                                   │
│  Glassmorphism UI           │  Django ORM → SQLite (Dev)        │
│                             │  → PostgreSQL-ready (Prod)        │
└─────────────────────────────┴───────────────────────────────────┘
```

The backend and frontend are fully decoupled. The frontend communicates exclusively via the REST API, meaning the frontend can be replaced, redesigned, or ported to a mobile app without touching the backend — and vice versa.

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend Framework | Django 6.0 | Core application logic, ORM, admin panel |
| API Layer | Django REST Framework | Serializers, ViewSets, API views |
| Authentication | SimpleJWT + Token Blacklisting | Stateless, secure guest sessions |
| Cross-Origin | django-cors-headers | Frontend/backend separation support |
| Frontend | Vanilla HTML + TailwindCSS | Multi-page, API-connected guest portal |
| Design | Playfair Display + Manrope | Premium typographic identity |
| Icons | Google Material Symbols | Consistent iconography |
| Environment API | Open-Meteo (free, no key) | Live weather + air quality data |
| Database (Dev) | SQLite | Zero-config local development |
| Database (Prod) | PostgreSQL (recommended) | Production-scale reliability |

---

## Data Models

BestBliss uses a thoughtfully designed relational schema across two Django apps:

### `accounts` App

**`User`** — The custom guest model, extending `AbstractBaseUser`

| Field | Type | Notes |
|---|---|---|
| `id` | CharField (PK) | Auto-generated branded ID, e.g. `BB-1001` |
| `email` | EmailField (unique) | Primary login credential |
| `name` | CharField | Guest display name |
| `membership` | CharField | Current tier name (e.g. `Gold`) |
| `tier_level` | IntegerField | Numeric tier for programmatic comparison |
| `reward_points` | IntegerField | Accumulated loyalty points |
| `referal_link` | CharField (unique) | Auto-generated personal referral URL |
| `is_admin` | BooleanField | Staff access flag |

### `features` App

**`Rooms`** — The hotel's room inventory

| Field | Type | Notes |
|---|---|---|
| `room_number` | CharField | Unique room identifier |
| `room_type` | CharField | e.g., Suite, Deluxe, Standard |
| `price` | IntegerField | Per-night rate |
| `is_available` | BooleanField | Live availability flag |
| `description` | CharField | Room narrative for guests |
| `smart_id` | CharField | Unique ID for IoT/smart room integration hook |

**`Bookings`** — Room reservations

| Field | Type | Notes |
|---|---|---|
| `user` | FK → User | The booking guest |
| `room_number` | FK → Rooms | The reserved room |
| `check_in_date` | DateField | Arrival date |
| `check_out_date` | DateField | Departure date |
| `total_price` | IntegerField | Server-calculated total |
| `booking_date` | DateTimeField | Timestamp of booking creation |

**`food_menu`** — Dining menu items

**`Orders`** — Guest food orders (many-to-many with food items)

**`weekly_events`** and **`special_events`** — The two-tier event system

**`membership_plans`** — Tier-based loyalty plan definitions

**`Privileges`** — Per-tier guest benefits

**`Redemption_items`** — Redeemable rewards catalogue

**`Redemption`** — Guest redemption history, with automatic points deduction

**`Offerorder`** — Membership offer claim records

**`EventBooking`** — Guest event registrations

---

## API Reference

All endpoints (except `/api/login/` and `/api/refresh/`) require a valid JWT Bearer token in the `Authorization` header.

```
Authorization: Bearer <access_token>
```

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/login/` | Obtain JWT access + refresh token pair |
| `POST` | `/api/refresh/` | Rotate refresh token, obtain new access token |
| `POST` | `/api/logout/` | Blacklist refresh token (secure logout) |

### Guest Portal

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/dashboard/` | Guest name, current bookings, today's events, active membership offer |
| `GET` | `/api/rooms/` | All rooms with availability, type, and pricing |
| `GET` | `/api/stay/` | Guest's bookings split into upcoming / current / past |
| `GET` | `/api/loyalty/` | Membership tier, reward points, privileges, referral link, redemption catalogue, next-tier requirement |

### Bookings

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/stays/booking/` | List all bookings for authenticated guest |
| `POST` | `/api/stays/booking/` | Create a new room booking |
| `DELETE` | `/api/stays/booking/` | Cancel a booking (same-day, pre-check-in only) |

**POST body:**
```json
{
  "room_number": "101",
  "check_in_date": "2025-09-01",
  "check_out_date": "2025-09-05"
}
```

### Dining

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/orders/food/` | Guest's food order history |
| `POST` | `/api/orders/food/` | Place a food order by item names |
| `DELETE` | `/api/orders/food/` | Cancel an order (within 10 minutes) |

**POST body:**
```json
{
  "items": ["Grilled Salmon", "Caesar Salad", "Sparkling Water"]
}
```

### Loyalty & Offers

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/orders/offers/` | Guest's offer purchase history |
| `POST` | `/api/orders/offers/` | Book a membership offer |
| `GET` | `/api/orders/events/` | Guest's event bookings |
| `POST` | `/api/orders/events/` | Register for a weekly event |
| `GET` | `/api/orders/redemptions/` | Guest's redemption history |
| `POST` | `/api/orders/redemptions/` | Redeem points for a catalogue item |

### Smart Environment

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/smart/?lat=28.6139&lon=77.2090` | Real-time weather + air quality for any coordinates |

**Response:**
```json
{
  "location": { "latitude": "28.6139", "longitude": "77.2090" },
  "metrics": {
    "temperature": { "value": 32.4, "unit": "°C" },
    "humidity": { "value": 61, "unit": "%" },
    "uv_index": { "value": 7.2, "classification": "High" },
    "air_quality": { "value": 89, "classification": "Moderate", "unit": "US AQI" }
  }
}
```

---

## Frontend Pages

BestBliss ships with a complete, fully-styled multi-page guest portal:

| Page | File | Description |
|---|---|---|
| **Sign In** | `index.html` | Luxury login experience with split-screen layout |
| **Dashboard** | `dashboard.html` | Personalised guest home with live data |
| **My Stays** | `stay.html` | Stay history categorised by status |
| **Manage Stay** | `manage_stay.html` | Booking creation and cancellation interface |
| **Dining** | `dining.html` | Food menu browser and order placement |
| **Order Tracker** | `order.html` | Live food order management |
| **Loyalty Circle** | `loyalty.html` | Rewards, privileges, referral link, and redemption |
| **Smart Suite** | `smart.html` | Live environmental metrics for guest's location |
| **History** | `history.html` | Complete guest activity history |

---

## Design System

The frontend is built on a bespoke Material Design 3-inspired dark luxury design system, implemented as a Tailwind CSS theme extension.

### Color Palette — "Gilded Serenity"

The palette evokes a five-star hotel at twilight: deep charcoal surfaces, warm gold accents, and refined secondary tones.

| Role | Color | Hex |
|---|---|---|
| **Primary** | Warm Gold | `#F2CA50` |
| **Primary Container** | Antique Gold | `#D4AF37` |
| **Surface** | Deep Charcoal | `#121414` |
| **Surface Container** | Elevated Dark | `#1E2020` |
| **On Surface** | Soft White | `#E2E2E2` |
| **Outline** | Warm Sand | `#99907C` |
| **Tertiary** | Champagne | `#F1C97D` |
| **Error** | Soft Coral | `#FFB4AB` |

### Typography

| Role | Font | Usage |
|---|---|---|
| **Headlines** | Playfair Display | Section headers, hero text, brand identity |
| **Body & Labels** | Manrope | Navigation, body copy, form labels, buttons |

### Component Language

- **Glass panels** — `backdrop-filter: blur(25px)` with semi-transparent dark backgrounds and subtle white borders
- **Uppercase tracking** — Button labels and navigation items use wide letter-spacing for a refined editorial feel
- **Hairline borders** — Inputs use a single bottom-border with no box-border, reducing visual noise
- **No border-radius on primary CTAs** — Sharp-edged primary buttons signal confidence and authority
- **Material Symbols** — Outlined icon style throughout, maintaining visual consistency

---

## Getting Started

### Prerequisites

- Python 3.11 or newer
- pip (Python package manager)
- Git

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/your-username/BestBliss.git
cd BestBliss
```

**2. Set up a virtual environment**

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

**3. Install backend dependencies**

```bash
cd backend
pip install -r requirements.txt
```

**4. Apply database migrations**

```bash
python manage.py migrate
```

**5. Create a superuser (admin access)**

```bash
python manage.py createsuperuser
# Enter email, name, and password when prompted
```

**6. Start the development server**

```bash
python manage.py runserver
```

The API will be live at `http://127.0.0.1:8000/`

**7. Open the frontend**

Open any file in the `frontend/` directory in your browser. For full functionality, serve them via a local HTTP server:

```bash
cd ../frontend
python -m http.server 3000
```

Then visit `http://localhost:3000/index.html`

### Seeding Data via Django Admin

Visit `http://127.0.0.1:8000/admin/` and log in with your superuser credentials. From the admin panel, you can create:

- Rooms (with types, prices, descriptions)
- Food menu items
- Weekly and special events
- Membership plans and privileges
- Redemption catalogue items

---

## Project Structure

```
BestBliss/
├── backend/
│   ├── accounts/                  # Custom user model & authentication
│   │   ├── models.py              # User, UserManager
│   │   ├── migrations/
│   │   └── admin.py
│   ├── features/                  # Core hotel features app
│   │   ├── models.py              # Rooms, Bookings, Orders, Events, Loyalty...
│   │   ├── views.py               # Dashboard, Stay, Booking, Dining, Loyalty ViewSets
│   │   ├── smart_view.py          # Real-time environmental API integration
│   │   ├── serializer.py          # All DRF serializers with custom validation
│   │   ├── urls.py                # Feature endpoint routing
│   │   └── migrations/
│   ├── config/
│   │   ├── settings.py            # Django settings, JWT config, CORS
│   │   ├── urls.py                # Root URL configuration
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── manage.py
│   └── requirements.txt
└── frontend/
    ├── index.html                 # Login page
    ├── dashboard.html             # Guest dashboard
    ├── stay.html                  # Stay history
    ├── manage_stay.html           # Booking management
    ├── dining.html                # Restaurant & dining
    ├── order.html                 # Order tracking
    ├── loyalty.html               # Loyalty & rewards
    ├── smart.html                 # Environmental intelligence
    └── history.html               # Full guest history
```

---

## Who Should Use BestBliss?

### For Hotel Startups

If you are launching a boutique hotel, a bed & breakfast, or a resort from scratch, BestBliss gives you something that would otherwise take months and significant investment to build: a complete, branded digital platform from day one.

Instead of paying for:
- A static website designer ($2,000–$8,000)
- A booking platform subscription ($200–$800/month)
- A loyalty program SaaS ($100–$500/month)
- A custom app developer for guest portals ($10,000+)

...you get all of it in one open codebase, fully customisable, with no ongoing licensing fees.

**What you customise:**
- Swap the hotel name ("BESTBLISS") to your brand across all HTML files
- Update the Tailwind color palette in the config block to match your brand colors
- Change the guest ID prefix (`BB-`) to your property code
- Add your room inventory, menu, and events via the admin panel
- Connect a domain and deploy to any Django-compatible host (Railway, Render, Heroku, AWS, DigitalOcean)

**Time to launch:** A technically competent team can go from this codebase to a live, branded, production-ready hotel website in under a week.

### For Established Hotels

If your hotel currently has a static website that shows photos and a phone number, BestBliss represents a genuine digital transformation opportunity.

**What you gain:**

| Current State | With BestBliss |
|---|---|
| Static "Contact Us" form | Live booking system with server-validated pricing |
| No guest identity | Branded guest accounts (e.g., `BB-1001`) with loyalty history |
| Email-based dining requests | Self-service food ordering with a 10-minute cancellation window |
| Generic newsletter | Tiered loyalty program with per-privilege benefits |
| No environmental context | Real-time weather, UV, and air quality for guests at your property |
| One-off visits | Referral links, rewards, and tier progression that drive return stays |

**For multi-property groups:** The Django architecture is modular. The `features` app and `accounts` app are designed to be extended — you can scope data by property, add a `property` foreign key to models, and manage multiple locations from a single backend.

### For Developers & Agencies

If you build digital solutions for hospitality clients, BestBliss is a production-quality starter template that eliminates the most time-consuming parts of hotel platform development.

Every architectural decision has been made intentionally:
- Custom `AbstractBaseUser` instead of Django's default — because hotel guests are not generic Django users
- JWT with blacklisting — because stateless auth is essential for API-first applications
- Decoupled frontend — because your client may later want a React app, a Flutter app, or a white-labelled mobile experience
- Open-Meteo integration — because third-party API keys should not be a barrier to deploying the smart features

Fork it, white-label it, and deliver it. The foundation is solid.

---

## BestBliss vs. The Alternatives

| Capability | BestBliss | Static Hotel Website | Generic Booking Widget | Custom Build from Scratch |
|---|---|---|---|---|
| **Cost** | Free / Self-hosted | $2K–$8K one-time | $200–800/month | $30K–$150K+ |
| **Guest Accounts** | ✅ Full custom auth | ❌ None | ⚠️ Third-party only | ✅ |
| **Room Booking** | ✅ Live API | ❌ | ⚠️ External widget | ✅ |
| **Food Ordering** | ✅ | ❌ | ❌ | ✅ |
| **Loyalty Program** | ✅ Tiered + Points | ❌ | ❌ | ✅ |
| **Events System** | ✅ Two-tier | ❌ | ❌ | ✅ |
| **Referral Links** | ✅ Per-guest | ❌ | ❌ | ✅ |
| **Environmental Data** | ✅ Real-time | ❌ | ❌ | ✅ (extra cost) |
| **Full Source Access** | ✅ | ❌ | ❌ | ✅ |
| **Brand Customisation** | ✅ Complete | ⚠️ Limited | ❌ | ✅ |
| **Time to Deploy** | Days | Weeks | Hours | Months |

---

## Roadmap

The following capabilities are natural next steps for BestBliss and represent the direction for future development:

- **Guest Registration API** — A `POST /api/register/` endpoint to allow self-service account creation
- **Password Reset Flow** — Email-based password recovery using Django's built-in email framework
- **Payment Integration** — Stripe or Razorpay integration for online booking deposits and food order payments
- **Room Availability Calendar** — Date-aware room availability queries to prevent double-booking
- **Image Support** — Room photo galleries and food item images via Django's media handling or cloud storage (S3)
- **Admin Dashboard Frontend** — A hotel-staff-facing UI for managing rooms, menus, events, and viewing all guest activity
- **Push Notifications** — Booking confirmation and event reminder notifications
- **PostgreSQL Migration Guide** — Step-by-step instructions for switching from SQLite to PostgreSQL for production
- **Docker Compose Setup** — Containerised deployment configuration for one-command production launches
- **Multi-Property Support** — Property-scoped data for hotel groups managing multiple locations
- **Mobile App (React Native / Flutter)** — The REST API is already mobile-ready; a companion app is a natural extension

---

## Contributing

BestBliss welcomes contributions from developers who want to help build the future of hospitality software.

**To contribute:**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature-name`)
3. Make your changes with clear, descriptive commits
4. Ensure the Django test suite passes (`python manage.py test`)
5. Open a Pull Request with a clear description of what you've added and why

**Before opening a PR, please ensure:**
- New API endpoints include appropriate `permission_classes`
- Serializers include `read_only_fields` for server-calculated values (prices, user references)
- Any new models include migrations
- Environment secrets (API keys, passwords) are not committed to the repository

---

## Security Notes

The following items are configured for local development and **must be changed before any production deployment:**

- `SECRET_KEY` in `settings.py` — Replace with a strong, randomly-generated secret and load it from an environment variable
- `DEBUG = True` — Set to `False` in production
- `ALLOWED_HOSTS = []` — Set to your domain(s) in production
- `CORS_ALLOW_ALL_ORIGINS = True` — Restrict to your frontend's specific domain in production
- SQLite — Switch to PostgreSQL for any production workload
- `ACCESS_TOKEN_LIFETIME` — Review and adjust token lifetimes based on your security requirements

---

## License

BestBliss is released under the **MIT License**. You are free to use, modify, distribute, and build commercial products on top of this codebase. Attribution is appreciated but not required.

---

<div align="center">

**Built with precision. Designed for hospitality.**

*BestBliss — Where the city's pulse meets the serenity of the stars.*

---

⭐ If BestBliss helped you build something great, consider giving this repository a star.

</div>

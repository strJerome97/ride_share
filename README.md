# Ride Share API

A Django REST Framework-based ride-sharing application that provides APIs for managing users, rides, and ride events with geolocation features.

## 📋 Table of Contents

- [Features](#features)
- [Technical Stack](#technical-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Database Schema](#database-schema)
- [Key Features](#key-features)
- [Development Timeline](#development-timeline)
- [Code Quality & Recommendations](#code-quality--recommendations)
- [Security Considerations](#security-considerations)
- [Future Improvements](#future-improvements)

## 🚀 Features

- **User Management**: Handle riders and drivers with role-based access
- **Ride Management**: Complete ride lifecycle from request to completion
- **Real-time Events**: Track ride events and status changes
- **Geolocation**: Distance calculation using Haversine formula
- **Custom Authentication**: Header-based authentication system
- **API Filtering**: Advanced filtering by status, rider email, etc.
- **Pagination**: Built-in pagination for large datasets

## 🛠 Technical Stack

- **Backend**: Django 5.2.7
- **API Framework**: Django REST Framework 3.16.1
- **Database**: SQLite (development)
- **Authentication**: Custom header-based authentication
- **Filtering**: django-filter 25.2
- **Geolocation**: Custom Haversine distance calculation

### Dependencies

The project uses the following Python packages (see `requirements.txt`):

```
asgiref==3.10.0          # ASGI server reference implementation
Django==5.2.7            # Web framework
django-filter==25.2      # Filtering support for Django REST framework
djangorestframework==3.16.1  # REST API framework
sqlparse==0.5.3          # SQL parser
tzdata==2025.2           # Timezone database
```

## 📁 Project Structure

```
ride_share/
├── main/                    # Main application
│   ├── models.py           # User, Ride, RideEvent models
│   ├── views.py            # API ViewSets
│   ├── serializers.py      # DRF serializers
│   ├── authentication.py   # Custom authentication
│   ├── filters.py          # Custom filters
│   ├── pagination.py       # Pagination configuration
│   └── migrations/         # Database migrations
├── project/                # Django project configuration
│   ├── settings.py         # Project settings
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI configuration
├── db.sqlite3             # SQLite database
├── requirements.txt       # Python dependencies
└── manage.py              # Django management script
```

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ride_share
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (optional)
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/`

## 🔌 API Endpoints

### Base URL: `http://localhost:8000/`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/users/` | GET, POST | List/Create users |
| `/users/{id}/` | GET, PUT, DELETE | User detail operations |
| `/rides/` | GET, POST | List/Create rides |
| `/rides/{id}/` | GET, PUT, DELETE | Ride detail operations |
| `/ride-events/` | GET, POST | List/Create ride events |
| `/ride-events/{id}/` | GET, PUT, DELETE | Ride event operations |

### Query Parameters

**Rides Endpoint:**
- `status` - Filter by ride status (requested, en-route, pickup, dropoff, completed, canceled)
- `rider_email` - Filter by rider email (partial match)
- `latitude` & `longitude` - Calculate distance from specified coordinates
- `ordering` - Sort by fields (pickup_time, distance)

## 🔐 Authentication

The application uses a custom header-based authentication system:

```http
X-User-Email: admin@example.com
```

**Current Implementation:**
- Requires `X-User-Email` header
- Only users with `role="admin"` can access the API
- No password verification or tokens

## 🗃️ Database Schema

### User Model
- `id_user` (PK) - Auto-incrementing primary key
- `role` - User role (admin, rider, driver)
- `first_name`, `last_name` - User names
- `email` - Unique email address
- `phone_number` - Contact number

### Ride Model
- `id_ride` (PK) - Auto-incrementing primary key
- `status` - Ride status with predefined choices
- `id_rider`, `id_driver` - Foreign keys to User model
- `pickup_latitude`, `pickup_longitude` - Pickup coordinates
- `dropoff_latitude`, `dropoff_longitude` - Destination coordinates
- `pickup_time` - Scheduled pickup time

### RideEvent Model
- `id_ride_event` (PK) - Auto-incrementing primary key
- `id_ride` - Foreign key to Ride model
- `description` - Event description
- `created_at` - Timestamp of event creation

## 🌟 Key Features

### Geolocation Support
- Haversine formula for accurate distance calculation
- Distance-based sorting when coordinates are provided
- Efficient database queries with spatial calculations

### Advanced Filtering
- Status-based filtering with case-insensitive matching
- Email-based rider search with partial matching
- Optimized database queries with select_related and prefetch_related

### Event Tracking
- Time-based event filtering (last 24 hours)
- Efficient prefetching to avoid N+1 queries
- Nested serialization for complete ride information

## 📈 Development Timeline

Based on commit history:

1. **Initial Setup** (2025-10-22 21:09:54)
   - Project scaffolding and basic configuration
   - Initial models, views, and serializers

2. **Core Features** (2025-10-22 23:41:09)
   - Enhanced ride event handling
   - Improved serializer structure
   - Query optimization

3. **Geolocation** (2025-10-23 13:57:19)
   - Distance calculation implementation
   - Location-based sorting
   - Enhanced filtering capabilities

4. **Authentication** (2025-10-23 14:28:27)
   - Custom authentication system
   - Admin role enforcement
   - Security enhancements

5. **Documentation & Improvements** (2025-10-23 14:45:05)
   - Comprehensive README documentation
   - Enhanced error handling in views
   - Code cleanup and optimization

## ⚠️ Code Quality & Recommendations

### Current Strengths
✅ **Well-structured models** with proper relationships  
✅ **Efficient database queries** with prefetch_related  
✅ **Clean serializer design** with nested relationships  
✅ **Geographic calculations** using Haversine formula  
✅ **Proper indexing** on frequently queried fields  

### Areas for Improvement

#### 🔒 **Authentication System (CRITICAL)**

**Current Issues:**
- No password verification
- Header-based auth is insecure
- No session management or tokens
- Role checking is simplistic

**Recommendations:**
```python
# 1. Implement proper token-based authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        # or JWT: 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# 2. Create proper user permissions
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role == 'admin'

# 3. Use Django's built-in User model or extend it
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15)
```

#### 🏗️ **Model Design**

**Issues:**
- Custom primary key naming (should use Django defaults)
- No audit fields

**Recommendations:**
```python
class Ride(models.Model):
    # Use Django's default 'id' field
    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default='requested'
    )
    rider = models.ForeignKey(User, related_name='rides_as_rider', ...)
    driver = models.ForeignKey(User, related_name='rides_as_driver', ...)
    
    # Add audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Add validation
    def clean(self):
        if self.pickup_time and self.pickup_time < timezone.now():
            raise ValidationError("Pickup time cannot be in the past")
```

## 🛡️ Security Considerations

### Current Security Issues

1. **Hardcoded Secret Key** - Move to environment variables
2. **Debug Mode Enabled** - Disable in production
3. **No HTTPS Enforcement** - Enable SSL redirect
4. **Weak Authentication** - Implement proper auth system
5. **No Rate Limiting** - Add throttling

### Security Improvements

```python
# settings.py
import os
from pathlib import Path

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Add security middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # ... other middleware
]

# Security settings
SECURE_SSL_REDIRECT = not DEBUG
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Add throttling
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}
```

## 🚀 Future Improvements

### High Priority
1. **Implement proper authentication** (JWT or Token-based)
2. **Add comprehensive tests** (unit, integration, API tests)
3. **Create API documentation** (using drf-yasg or similar)
4. **Add logging and monitoring**
5. **Implement proper error handling**

### Medium Priority
1. **Add real-time notifications** (WebSocket support)
2. **Implement caching** (Redis for frequently accessed data)
3. **Add data validation** (serializer validation, model constraints)
4. **Database optimization** (PostgreSQL for production)
5. **Add API versioning**

### Low Priority
1. **Admin interface improvements**
2. **Automated deployment pipeline**
3. **Performance monitoring**
4. **API analytics**

## 🧪 Testing

**Current Status:** No tests implemented

**Recommendations:**
```bash
# Install testing dependencies (add to requirements-dev.txt)
pip install pytest-django factory-boy coverage

# Create test files
mkdir tests/
# Windows PowerShell
New-Item -ItemType File tests/test_models.py, tests/test_views.py, tests/test_authentication.py
# Linux/Mac
touch tests/test_models.py tests/test_views.py tests/test_authentication.py
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is currently unlicensed. Consider adding an appropriate license for your use case.

---

**Note**: This project is in active development. The authentication system needs immediate attention before production deployment.

---
**FOR BONUS PART**

WITH pickup_dropoff_times AS (
    SELECT
        r.id_ride,
        r.id_driver_id,
		u.first_name,
		u.last_name,
        MIN(CASE WHEN e.description = 'Status changed to pickup' THEN e.created_at END) AS pickup_time,
        MIN(CASE WHEN e.description = 'Status changed to dropoff' THEN e.created_at END) AS dropoff_time
    FROM
        main_ride r
        JOIN main_rideevent e ON e.id_ride_id = r.id_ride
		JOIN main_user u ON u.id_user = r.id_driver_id
    WHERE
        e.description IN ('Status changed to pickup', 'Status changed to dropoff')
    GROUP BY
        r.id_ride, r.id_driver_id, u.first_name, u.last_name
)
SELECT
    TO_CHAR(DATE_TRUNC('month', pickup_time), 'YYYY-MM') AS Month,
    first_name || ' ' || UPPER(SUBSTRING(last_name, 1, 1)) AS Driver,
    COUNT(*) AS "Count of Trips > 1 hr"
FROM
    pickup_dropoff_times
WHERE
    pickup_time IS NOT NULL
    AND dropoff_time IS NOT NULL
    AND EXTRACT(EPOCH FROM (dropoff_time - pickup_time)) / 3600 > 1
GROUP BY
    first_name,
	last_name,
    TO_CHAR(DATE_TRUNC('month', pickup_time), 'YYYY-MM')
ORDER BY
    month,
    first_name,
	last_name;
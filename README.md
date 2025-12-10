# Temiz Xali - Carpet Cleaning and Dry Cleaning Services

Django-based website for Temiz Xali Baku Factory. This project is developed for a carpet cleaning, dry cleaning, and laundry services company that has been operating since 2004.

## 📋 Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Docker Usage](#docker-usage)
- [Development](#development)
- [Deployment](#deployment)

## ✨ Features

### Core Functionality
- **Multi-language Support**: Azerbaijani and Russian languages
- **Service Catalog**: List of carpet cleaning, dry cleaning, and other services
- **Pricing System**: Regular, VIP, and Premium pricing variants
- **Order System**: Online order form
- **Review System**: Customer reviews and testimonials
- **Projects**: Showcase of special projects
- **Statistics**: Company statistics
- **About**: Company information

### Admin Panel
- Django Admin panel
- Nested Admin support (inline editing)
- Multi-language content management
- Image and video upload
- Order and review management

### Technical Features
- PostgreSQL database
- Gunicorn WSGI server
- Nginx reverse proxy
- Docker containerization
- Automatic static files collection
- Media files management
- Cache invalidation system

## 🛠 Technologies

### Backend
- **Django 5.2.7+**: Web framework
- **Python 3.11+**: Programming language
- **PostgreSQL**: Database
- **Gunicorn**: WSGI HTTP server
- **Pillow**: Image processing
- **psycopg2-binary**: PostgreSQL adapter

### Frontend
- **Bootstrap**: CSS framework
- **JavaScript**: Interactive functionality
- **jQuery**: DOM manipulation
- **Lightbox**: Image gallery
- **Owl Carousel**: Slider component
- **Isotope**: Filtering and sorting

### Deployment
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Nginx**: Web server and reverse proxy
- **uv**: Fast package manager

## 📁 Project Structure

```
Temizxali/
├── docker-compose.yaml      # Docker Compose configuration
├── Dockerfile              # Docker image definition
├── entrypoint.sh           # Container startup script
├── nginx.conf              # Nginx configuration
├── pyproject.toml          # Python project configuration
├── uv.lock                 # Package lock file
├── README.md               # This file
│
└── temizxali/              # Django project
    ├── manage.py           # Django management script
    ├── locale/             # Translation files
    │   └── ru/
    │       └── LC_MESSAGES/
    │
    ├── services/           # Main application
    │   ├── admin/          # Admin configuration
    │   ├── models/         # Database models
    │   ├── views/          # View functions
    │   ├── utils/          # Helper functions
    │   ├── forms.py        # Django forms
    │   ├── urls_v1.py      # URL routing
    │   └── signals.py      # Django signals
    │
    ├── temizxali/          # Django project configuration
    │   ├── settings.py     # Settings
    │   ├── urls.py         # Main URL configuration
    │   ├── wsgi.py         # WSGI configuration
    │   ├── asgi.py         # ASGI configuration
    │   └── middleware.py   # Custom middleware
    │
    ├── templates/          # HTML templates
    ├── static/             # Static files (CSS, JS, images)
    ├── staticfiles/        # Collected static files
    └── media/              # User uploaded files
```

## 🚀 Installation

### Requirements
- Python 3.11 or higher
- PostgreSQL
- Docker and Docker Compose (optional)
- uv package manager (recommended)

### Local Installation

1. **Clone the project:**
```bash
git clone <repository-url>
cd Temizxali
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install uv:**
```bash
pip install uv
```

4. **Install dependencies:**
```bash
uv pip sync uv.lock
# or
uv pip install -e .
```

5. **Set environment variables:**
Create `.env` file:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
ADMIN_URL=admin/

# PostgreSQL
POSTGRES_DB=temizxali
POSTGRES_USER=temizxali_user
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=localhost
```

6. **Create database:**
```bash
createdb temizxali  # In PostgreSQL
```

7. **Run migrations:**
```bash
cd temizxali
python manage.py migrate
```

8. **Create superuser:**
```bash
python manage.py createsuperuser
```

9. **Collect static files:**
```bash
python manage.py collectstatic
```

10. **Compile translations:**
```bash
python manage.py compilemessages
```

11. **Start development server:**
```bash
python manage.py runserver
```

## ⚙️ Configuration

### Environment Variables

The following variables are required in `.env` file:

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `django-insecure-...` |
| `DEBUG` | Debug mode | `True` / `False` |
| `ALLOWED_HOSTS` | Allowed hosts | `localhost,127.0.0.1` |
| `ADMIN_URL` | Admin panel URL path | `admin/` |
| `POSTGRES_DB` | Database name | `temizxali` |
| `POSTGRES_USER` | DB username | `temizxali_user` |
| `POSTGRES_PASSWORD` | DB password | `secure-password` |
| `POSTGRES_HOST` | DB host | `localhost` / `db` |

### Language Configuration

The project supports Azerbaijani and Russian languages:
- **Default language**: Azerbaijani (`az`)
- **Supported languages**: `az`, `ru`
- **Language switching**: Session-based

## 💻 Usage

### Admin Panel

1. Access admin panel: `http://localhost:8000/admin/`
2. Login with superuser credentials
3. Manage content:
   - **Services**: Add and edit services
   - **Orders**: View customer orders
   - **Reviews**: Manage customer reviews
   - **Projects**: Add special projects
   - **About**: Update company information

### Pages

- **Home Page** (`/`): Services, statistics, motto
- **About** (`/about/`): Company information
- **Projects** (`/projects/`): Gallery of special projects
- **Service Details** (`/service/<slug>/`): Detailed service information
- **Order** (`/order/`): Online order form
- **Review** (`/review/`): Customer review form
- **Testimonial** (`/testimonial/`): List of verified reviews

## 🐳 Docker Usage

### Starting with Docker Compose

1. **Create environment file:**
```bash
cp .env.example .env
# Edit .env file
```

2. **Start containers:**
```bash
docker-compose up -d
```

3. **Run migrations:**
```bash
docker-compose exec web python temizxali/manage.py migrate
```

4. **Create superuser:**
```bash
docker-compose exec web python temizxali/manage.py createsuperuser
```

5. **Collect static files:**
```bash
docker-compose exec web python temizxali/manage.py collectstatic --noinput
```

6. **Access the site:**
- Website: `http://localhost:8080`
- Admin panel: `http://localhost:8080/admin/`

### Docker Commands

```bash
# Stop containers
docker-compose down

# View logs
docker-compose logs -f web

# Access container
docker-compose exec web bash

# Connect to database
docker-compose exec db psql -U temizxali_user -d temizxali

# Rebuild containers
docker-compose up -d --build
```

## 🔧 Development

### Development Server

```bash
cd temizxali
python manage.py runserver
```

### Migrations

```bash
# Create new migration
python manage.py makemigrations

# Run migrations
python manage.py migrate
```

### Translations

```bash
# Create new translation messages
python manage.py makemessages -l ru

# Compile translations
python manage.py compilemessages
```

### Static Files

```bash
# In development mode
python manage.py collectstatic --noinput
```

### Code Structure

- **Models**: `services/models/` - Database models
- **Views**: `services/views/` - View functions
- **Forms**: `services/forms.py` - Django forms
- **Utils**: `services/utils/` - Helper functions
- **Templates**: `templates/` - HTML templates
- **Static**: `static/` - CSS, JS, images

## 🚢 Deployment

### Production Configuration

1. **Set environment variables:**
```env
DEBUG=False
ALLOWED_HOSTS=temizxali.az,www.temizxali.az
SECRET_KEY=<production-secret-key>
```

2. **SSL/HTTPS configuration:**
- Install SSL certificates in Nginx
- Set `CSRF_COOKIE_SECURE = True`
- Set `SESSION_COOKIE_SECURE = True`

3. **Deploy with Docker Compose:**
```bash
docker-compose -f docker-compose.prod.yaml up -d
```

### Nginx Configuration

Nginx configuration for production is defined in `nginx.conf` file:
- Serving static files
- Serving media files
- Proxy to Django/Gunicorn

### Gunicorn

Production server uses Gunicorn:
```bash
gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 120 \
  --chdir temizxali temizxali.wsgi:application
```

## 📝 Models

### Service
- Price variants (regular, VIP, Premium)
- Video and URL support
- Measurement type (m², unit, kg)
- Delivery option
- Multi-language translations

### Order
- Multiple service selection
- Customer information
- Phone number normalization
- WhatsApp integration

### Review
- Service-related reviews
- Verification system
- Order confirmation requirement

### SpecialProject
- Project images
- Multi-language descriptions
- Active status

## 🔒 Security

- **CSRF Protection**: Django CSRF protection
- **SQL Injection Protection**: Django ORM usage
- **XSS Protection**: Django template auto-escaping
- **Environment Variables**: Sensitive data in `.env` file

## 📞 Contact

For questions about the project:
- Website: [temizxali.az](https://temizxali.az)

## 📄 License

This project is proprietary and developed for Temiz Xali Baku Factory.

---

**Note**: This README file contains a complete description of the project. For additional information and updates, please review the project code.

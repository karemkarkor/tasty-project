"""
tasty_django/settings.py

Key changes from a default Django project:
  1. Custom AUTH_USER_MODEL pointing to our User model with user_type field
  2. INSTALLED_APPS includes 'recipes' and 'rest_framework' (optional DRF)
  3. TEMPLATES configured to find the existing HTML files (the frontend)
  4. STATICFILES_DIRS configured to serve JS/, Styles/, Images/ from the project root
  5. CORS headers enabled for the JS frontend (same as Express's cors() middleware)
  6. DATABASE defaults to SQLite for development (easy to swap to PostgreSQL for production)
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Security
# ---------------------------------------------------------------------------
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-replace-this-with-a-real-secret-key-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# In production, set this to your domain: ALLOWED_HOSTS = ['yourdomain.com']
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# ---------------------------------------------------------------------------
# Applications
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',       # Django REST Framework (used for serializers)
    'corsheaders',          # Mirrors Express's cors() middleware

    # Our app
    'recipes',
]

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------
MIDDLEWARE = [
    # CORS headers must come before CommonMiddleware
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    # NOTE: We use @csrf_exempt on API views (like the Express server which has no CSRF).
    # For production you should implement proper CSRF protection on non-API endpoints.
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tasty_django.urls'

# ---------------------------------------------------------------------------
# Templates — find the existing HTML frontend files
# ---------------------------------------------------------------------------
# The frontend HTML files are in the project root (same level as manage.py).
# We add that directory as a template directory so Django's TemplateView
# can serve home.html, login.html, etc. — just like Express's express.static().
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR,           # project root — finds home.html, login.html, etc.
            BASE_DIR / 'templates',  # conventional Django templates dir (optional)
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tasty_django.wsgi.application'

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
# Default: SQLite (zero-config, great for development).
# For production swap to PostgreSQL:
#   DATABASES = {
#       'default': {
#           'ENGINE': 'django.db.backends.postgresql',
#           'NAME': 'tasty_db',
#           'USER': 'tasty_user',
#           'PASSWORD': 'your_password',
#           'HOST': 'localhost',
#           'PORT': '5432',
#       }
#   }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------------------------------------------------------------------
# Custom User Model
# ---------------------------------------------------------------------------
# MUST be set before the first migration.
# Replaces Django's default User with our User model that has user_type.
AUTH_USER_MODEL = 'recipes.User'

# ---------------------------------------------------------------------------
# Password validation
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------------------------------------------------------
# Internationalization
# ---------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static files — mirrors Express's express.static(path.join(__dirname, '..'))
# ---------------------------------------------------------------------------
# URL prefix for static files
STATIC_URL = '/static/'

# Directories where Django will look for static files (JS, CSS, Images)
# These point to the existing project frontend folders.
STATICFILES_DIRS = [
    BASE_DIR,
]

# Where collectstatic puts files in production
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (user uploads — not used in original app but good to configure)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------------------------
# CORS — mirrors Express's cors() middleware
# ---------------------------------------------------------------------------
# Allow all origins in development (same as Express default cors())
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]
CORS_ALLOW_CREDENTIALS = True

# ---------------------------------------------------------------------------
# Django REST Framework (used for serializers and optional API views)
# ---------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
}

# ---------------------------------------------------------------------------
# Session settings (for login state)
# ---------------------------------------------------------------------------
SESSION_COOKIE_AGE = 86400  # 1 day in seconds
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_SECURE = False

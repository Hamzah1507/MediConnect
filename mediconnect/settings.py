import os
from pathlib import Path
from dotenv import load_dotenv

# ======================================================================
# === LOAD ENVIRONMENT VARIABLES (CRITICAL) ===
# Load variables from the .env file at the project root
load_dotenv() 
# ======================================================================

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
# --- Reading SECRET_KEY from environment ---
SECRET_KEY = os.getenv('SECRET_KEY', 'default-django-insecure-key-if-not-found') 

# SECURITY WARNING: don't run with debug turned on in production!
# --- Reading DEBUG from environment ---
# os.getenv returns a string, so we check if it equals 'True'
DEBUG = os.getenv('DEBUG', 'True') == 'True' 

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # === CRITICAL FIXES FOR PAYPAL ===
    'django.contrib.sites',  # REQUIRED for PayPal integration
    # =================================
    
    'home',
    
    # === PAYPAL INTEGRATION APP ===
    'paypal.standard.ipn',
    
    # ======================================================================
    # === NEW: REST FRAMEWORK FOR API (GUIDELINE #6) ===
    'rest_framework',
    # ======================================================================
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mediconnect.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mediconnect.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "mediconnect",
        "USER": "root",
        "PASSWORD": "G@laxy#2025Db!",
        "HOST": "localhost",
        "PORT": "3306",
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}

# Password validation (unmodified)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization (unmodified)
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static and Media files (unmodified)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Authentication Redirects (unmodified)
LOGIN_URL = 'signin'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'


# ======================================================================
# === PAYPAL SANDBOX (TEST MODE) INTEGRATION SETTINGS ===
# ======================================================================

# CRITICAL: Define SITE_ID for the Sites framework (required for PayPal)
SITE_ID = 1

# 1. Receiver Email (The fake merchant account from your Sandbox)
PAYPAL_RECEIVER_EMAIL = os.getenv('PAYPAL_RECEIVER_EMAIL')

# 2. Enable Test Mode (CRITICAL for development - Reads PAYPAL_TEST from .env if present)
PAYPAL_TEST = os.getenv('PAYPAL_TEST', 'True') == 'True' 

# 3. Currency Code (Set to INR for local context)
PAYPAL_CURRENCY_CODE = os.getenv('PAYPAL_CURRENCY_CODE', 'INR') 

# 4. REST API Keys (Optional, if using the REST SDK instead of standard forms)
PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
PAYPAL_SECRET_KEY = os.getenv('PAYPAL_SECRET_KEY')

# ======================================================================


# ======================================================================
# === COOKIES AND SESSION SETTINGS (GUIDELINE #5) ===
# ======================================================================

# Session Configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Store sessions in database
SESSION_COOKIE_NAME = 'mediconnect_sessionid'  # Custom session cookie name
SESSION_COOKIE_AGE = 1209600  # 2 weeks (in seconds)
SESSION_SAVE_EVERY_REQUEST = False  # Only save session if modified
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Session persists after browser close
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie (security)
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection

# Cookie Configuration
CSRF_COOKIE_NAME = 'mediconnect_csrftoken'  # Custom CSRF cookie name
CSRF_COOKIE_AGE = 31449600  # 1 year (in seconds)
CSRF_COOKIE_HTTPONLY = False  # Must be False for AJAX to access
CSRF_COOKIE_SECURE = False  # Set to True in production with HTTPS
CSRF_COOKIE_SAMESITE = 'Lax'  # CSRF protection

# Custom Cookie Settings for User Preferences
COOKIE_MAX_AGE = 365 * 24 * 60 * 60  # 1 year for preference cookies

# ======================================================================


# ======================================================================
# === REST FRAMEWORK CONFIGURATION (GUIDELINE #6) ===
# ======================================================================

REST_FRAMEWORK = {
    # Default permission classes
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    
    # Default authentication classes
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    
    # Pagination settings
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # Number of items per page
    
    # Filtering backends
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    
    # Rendering classes
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',  # Nice web interface for testing
    ],
    
    # Throttling (Rate limiting) - Optional but recommended
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',  # Anonymous users: 100 requests per hour
        'user': '1000/hour',  # Authenticated users: 1000 requests per hour
    },
}

# ======================================================================
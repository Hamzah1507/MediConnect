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
    'home',
    
    # === PAYPAL INTEGRATION APP ADDED ===
    'paypal.standard.ipn', 
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

# The following settings read from the .env file (PAYPAL_RECEIVER_EMAIL, PAYPAL_CLIENT_ID, etc.)

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

from pathlib import Path
import os
from dotenv import load_dotenv

# ======================================================================
# === LOAD ENVIRONMENT VARIABLES (CRITICAL) ===
load_dotenv() 
# ======================================================================

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# Reading SECRET_KEY and DEBUG from environment
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-(s4%3r4676be8(5duf&f$ubm*r=m=02gsmiy8xk5n_xhfnllj=') 
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
    'django.contrib.sites',  # REQUIRED to fix the 'RuntimeError'
    # =================================

    'home',
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = 'signin'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# ======================================================================
# === PAYPAL SANDBOX (TEST MODE) INTEGRATION SETTINGS ===
# ======================================================================

# CRITICAL: Define SITE_ID for the Sites framework
SITE_ID = 1

# 1. Receiver Email (The fake merchant account from your Sandbox)
PAYPAL_RECEIVER_EMAIL = os.getenv('PAYPAL_RECEIVER_EMAIL')

# 2. Enable Test Mode (CRITICAL for development)
PAYPAL_TEST = os.getenv('PAYPAL_TEST', 'True') == 'True' 

# 3. Currency Code
PAYPAL_CURRENCY_CODE = os.getenv('PAYPAL_CURRENCY_CODE', 'INR') 

# 4. Optional: REST API Keys
PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
PAYPAL_SECRET_KEY = os.getenv('PAYPAL_SECRET_KEY')

# Old Instamojo settings have been completely removed.
# ======================================================================

# The base folder of your project (mediconnect/ is typically where manage.py is)
BASE_DIR = Path(__file__).resolve().parent.parent 

# URL prefix for your media files
MEDIA_URL = '/media/' 

# PHYSICAL path where uploaded files are stored (Should create a 'media' folder in your project root)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
import os
from pathlib import Path
import dj_database_url
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-kuncirahasia-dummy-gantinanti'

# Izinkan domain Vercel kamu
ALLOWED_HOSTS = ['*'] 

# Jika kamu menggunakan CORS (django-cors-headers)
CORS_ALLOW_ALL_ORIGINS = True

# Pastikan DEBUG dimatikan untuk produksi
DEBUG = False


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # --- Tambahan Library Kita ---
    'rest_framework',
    'corsheaders',
    'queue_app',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # Wajib paling atas
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True # Supaya frontend HTML tidak diblokir

ROOT_URLCONF = 'iot_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'iot_backend.wsgi.application'


# Database
DATABASES = {
    'default': dj_database_url.config(
        default="postgresql://neondb_owner:npg_4pjnBNOFXx2C@ep-small-sunset-a10nhoi6.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
    )
}


# Waktu & Bahasa
LANGUAGE_CODE = 'id'
TIME_ZONE = 'Asia/Jakarta'
USE_I18N = True
USE_TZ = True


STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- KONFIGURASI DRF, JWT & RATE LIMITING ---
REST_FRAMEWORK = {
    # 1. TAMBAHKAN INI BIAR DJANGO BISA BACA TOKEN JWT
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    
    # 2. Ini yang Throttling tadi (biarkan saja seperti ini)
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1000/min',   
        'user': '10000/day'   
    }
}

from datetime import timedelta  # Pastikan ini ada di paling atas file

# ... (kode lain) ...

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
}

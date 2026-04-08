from pathlib import Path
from datetime import timedelta
import os
import dj_database_url # Add this to requirements.txt

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY: Use an environment variable for live deployment
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-b+cwi6r!r%4=&58i17l*z4d+z((yj00mvoxp-9y5(h%i-&q)xl')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Vercel provides a system env for the URL
ALLOWED_HOSTS = [
    'chat-xi-khaki-37.vercel.app', 
    '.vercel.app', # Allows all Vercel subdomains
    'localhost', 
    '127.0.0.1'
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'users',
    'api',
    'chatgroup',
    'status',
    'trends',
    
    # 'channels', # REMOVE THIS: Not supported on Vercel
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'whitenoise.runserver_nostatic', # For serving static files on Vercel
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Add this after security
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'api.authentication.SupabaseAuthentication', # Use our custom bridge
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

ROOT_URLCONF = 'app.urls'

# --- DATABASE CONFIG ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres.xxuelagumqjmytaacjgg', # Your user from the screenshot
        'PASSWORD': 'g9CLArEEdvVZkaeg',
        'HOST': 'aws-0-eu-west-1.pooler.supabase.com', # Your host from screenshot
        'PORT': '6543', # Using the pooler port from your screenshot
    }
}

# --- REMOVE ASGI/CHANNELS ---
# Since Vercel is serverless, we use standard WSGI
WSGI_APPLICATION = 'app.wsgi.application'
# ASGI_APPLICATION = "app.asgi.application" # Disabled for Vercel
# CHANNEL_LAYERS = { ... } # Disabled for Vercel

# --- STATIC FILES ---
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# --- MEDIA (SUPABASE STORAGE) ---
# Vercel's file system is read-only. You cannot save media to BASE_DIR/media.
# You will need to use Supabase Buckets or Cloudinary here.
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage' # Example for S3/Supabase

AUTH_USER_MODEL = 'users.Profiles'

CORS_ALLOWED_ORIGINS = [
    "https://chat-xi-khaki-37.vercel.app",
    "http://localhost:3000",
]

APPEND_SLASH = False
from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [
    'chat-xi-khaki-37.vercel.app',
    '.vercel.app',
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

    'rest_framework',
    'corsheaders',
    'whitenoise.runserver_nostatic',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'api.authentication.SupabaseAuthentication',
    ],
}

ROOT_URLCONF = 'app.urls'

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}

WSGI_APPLICATION = 'app.wsgi.application'

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

CORS_ALLOWED_ORIGINS = [
    "https://chat-xi-khaki-37.vercel.app",
    "http://localhost:3000",
]

APPEND_SLASH = False

WHITENOISE_KEEP_ONLY_HASHED_FILES = True
WHITENOISE_USE_FINDERS = True

# ✅ ADD THESE
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY')
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Add 'localhost' to ALLOWED_HOSTS for development
ALLOWED_HOSTS = ['localhost']
DOMAINS = ['localhost']
SECURE_SSL_REDIRECT = False
CSRF_TRUSTED_ORIGINS = ["http://localhost:8000"]



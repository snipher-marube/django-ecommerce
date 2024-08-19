# production.py
from .base import *


DEBUG = False

ALLOWED_HOSTS = ['.vercel.app']

# Configure your production database 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT'),
        'CONN_MAX_AGE': 600,
         'OPTIONS': {
            'sslmode': 'require',
            'client_encoding': 'UTF8',           
        }
    }
}



# Static and media files settings for production
STATIC_URL = '/static/'

MEDIA_URL = '/media/'

# Cloudinary storage for production
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Change this to False to keep the session even if the browser is closed

# Session age (2 weeks in seconds)
SESSION_COOKIE_AGE = 1209600  # Adjust as needed
SESSION_SAVE_EVERY_REQUEST = True

ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'


DOMAIN = "https://django-ecommerce-gamma.vercel.app/"


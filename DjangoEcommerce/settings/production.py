
from .base import *


DEBUG = True

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

# This configuration block is setting up a cache using Redis for the Django project in a production environment.
# The cache is used to store the results of expensive database queries, API calls, or other computationally expensive operations.
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('UPSTASH_REDIS_REST_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
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


ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'


DOMAIN = ['https://django-ecommerce-3nfg.vercel.app/']
CSRF_TRUSTED_ORIGINS = ['.vercel.app']


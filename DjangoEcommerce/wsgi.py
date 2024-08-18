"""
WSGI config for DjangoEcommerce project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from re import DEBUG

from django.core.wsgi import get_wsgi_application

from whitenoise import WhiteNoise

if DEBUG:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoEcommerce.settings.development')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoEcommerce.settings.production')

application = get_wsgi_application()

# wrap the application with WhiteNoise
application = WhiteNoise(application)

app = application

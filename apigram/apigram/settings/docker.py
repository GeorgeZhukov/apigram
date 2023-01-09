from .base import *

import os

DEBUG = False
ALLOWED_HOSTS = ['apigram.crabdance.com', '141.148.245.194', '127.0.0.1', 'localhost']
# ALLOWED_HOSTS = ['141.148.245.194', '127.0.0.1', 'localhost']
# ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': 'postgres',
        'HOST': 'db',
    }
}



STATIC_ROOT = os.environ.get('DJANGO_STATIC_ROOT', BASE_DIR / "static")
MEDIA_ROOT = os.environ.get('DJANGO_MEDIA_ROOT', BASE_DIR / "media")

DRF_STANDARDIZED_ERRORS = {"ENABLE_IN_DEBUG_FOR_UNHANDLED_EXCEPTIONS": True}
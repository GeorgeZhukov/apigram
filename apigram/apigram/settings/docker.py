from .base import *

DEBUG = False
ALLOWED_HOSTS = ['141.148.245.194']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'apigram_development',
        'USER': 'postgres',
        'HOST': 'db',
    }
}

MEDIA_ROOT = BASE_DIR / 'media'
STATIC_ROOT = BASE_DIR / 'static'

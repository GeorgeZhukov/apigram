from .base import *

import os

DEBUG = False
ALLOWED_HOSTS = ['apigram.crabdance.com', '141.148.245.194', '34.88.20.233', '127.0.0.1', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': 'postgres',
        'HOST': 'db',
    }
}

DRF_STANDARDIZED_ERRORS = {"ENABLE_IN_DEBUG_FOR_UNHANDLED_EXCEPTIONS": True}
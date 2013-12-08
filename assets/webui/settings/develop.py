"""Development settings and globals."""
from .base import *


STATSD_CLIENT = 'django_statsd.clients.null'

#COMPRESS_ENABLED = True
LOG_DIR = join(ROOT_DIR, 'logs')

PROTECTED_MEDIA_ROOT = join(PUBLIC_ROOT, 'private')
PROTECTED_MEDIA_URL = '/private/'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(ROOT_DIR, 'database.db'),
    }
}

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
########## END EMAIL CONFIGURATION

########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
########## END CACHE CONFIGURATION


########## TOOLBAR CONFIGURATION
INTERNAL_IPS = ('127.0.0.1', )

INSTALLED_APPS += (
    'debug_toolbar',
    'mockups',
)

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
########## END TOOLBAR CONFIGURATION

# -*- coding: utf-8 -*-
"""
Django settings for assets project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from os.path import abspath, dirname, join
from django.conf import global_settings
from django.utils.translation import ugettext_lazy as _

BASE_DIR = dirname(dirname(dirname(abspath(__file__))))
ROOT_DIR = dirname(BASE_DIR)
PUBLIC_ROOT = join(ROOT_DIR, 'public')

# Add our project to pythonpath, this way we don't need to type our project
# name in our dotted import paths:
#path.append(BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$v5or$9ev2=08z$idlp@-0mvon@7i8zx7oxmxbjpjz5yh!ild$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'assets.association',
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lineage',
    'django_select2',
    'import_export',
    'south',
    'raven.contrib.django.raven_compat',
)

MIDDLEWARE_CLASSES = (
    'django_statsd.middleware.GraphiteRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
)

ROOT_URLCONF = 'assets.webui.urls'

WSGI_APPLICATION = 'assets.webui.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGES = (
    ('fr', 'Français'),
    ('en', 'English'),
    #('ar', 'Arabia'),
)

LANGUAGE_CODE = 'fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = (join(BASE_DIR, 'locale'),)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = join(PUBLIC_ROOT, 'assets')
STATIC_URL = '/static/'

#####
SITE_NAME = 'Association'

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
)

SUIT_CONFIG = {
    'ADMIN_NAME': SITE_NAME,
    'SEARCH_URL': '/admin/association/student',
    'MENU': (
        # Keep original label and models
        'sites',

        # Rename app and set icon
        {'label': _('Students'),  'url': 'association.student',
            'icon': 'icon-user'},
        {'label': _('Staff'),  'url': 'association.staff',
            'icon': 'icon-star'},
        '-',
        {'label': _('Invoices'),  'url': 'association.invoice',
            'icon': 'icon-shopping-cart'},
        '-',
        {'label': _('Earnings'), 'models': ('association.earning', 'association.earningtype'),
            'icon': 'icon-plus-sign'},
        {'label': _('Spendings'), 'url': 'association.spending',
            'icon': 'icon-minus-sign'},
        '-',
        # Reorder app models
        {'app': 'auth', 'label': _('Authorizations'), 'icon': 'icon-lock'},

    ),
}

# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            #'filename': 'assets.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'INFO',
        },
        'association': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}

RAVEN_CONFIG = {
    'dsn': 'http://bee293ed8eb74f8da19d7d0587cc1362:9e56ae1a409e4f3eb28d3b747e3aef6d@sentry.abdourakhmane.net/2',
}

#STATSD_PATCHES = [
#    'django_statsd.patches.db',
#    'django_statsd.patches.cache',
#]

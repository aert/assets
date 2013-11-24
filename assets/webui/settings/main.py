import os
from ConfigParser import RawConfigParser

config = RawConfigParser()

ENV_KEY = 'APP_CONFIG_ASSETS'


def get_cookies(option):
    return get_optional_conf('cookies', option)


def get_db(option):
    return get_optional_conf('database', option)


def get_main(option):
    return get_optional_conf('main', option)


def get_optional_conf(section, option):
    value = ''
    if config.has_option(section, option):
        value = config.get(section, option)

    if value:
        return value
    return ''


if ENV_KEY not in os.environ:
    print("Not defined: %s" % ENV_KEY)
    from .bare import *

else:
    config_file = os.environ[ENV_KEY]
    config.read(config_file)

    DEVELOP = config.getboolean('main', 'DEVELOP')

    if DEVELOP:
        from .develop import *
    else:
        from .release import *

    # [main]
    ALLOWED_HOSTS = get_main('ALLOWED_HOSTS_').split() or ALLOWED_HOSTS
    LOG_DIR = get_main('LOG_DIR') or LOG_DIR
    LOGGING['handlers']['file']['filename'] = join(LOG_DIR, 'assets.log')
    if not DEVELOP:
        STATIC_ROOT = config.get('main', 'STATIC_ROOT')
        STATIC_URL = config.get('main', 'STATIC_URL')
        MEDIA_ROOT = config.get('main', 'MEDIA_ROOT')
        MEDIA_URL = config.get('main', 'MEDIA_URL')

        PROTECTED_MEDIA_ROOT = config.get("main", "PROTECTED_MEDIA_ROOT")
        PROTECTED_MEDIA_URL = config.get("main", "PROTECTED_MEDIA_URL")

    # [database]
    value = get_db('DATABASE_ENGINE_')
    if value:
        DATABASE_ENGINE = get_db('DATABASE_ENGINE_')
        DATABASE_NAME = get_db('DATABASE_NAME_')
        DATABASE_USER = get_db('DATABASE_USER_')
        DATABASE_PASSWORD = get_db('DATABASE_PASSWORD_')
        DATABASE_HOST = get_db('DATABASE_HOST_')
        DATABASE_PORT = get_db('DATABASE_PORT_')
        TEST_DATABASE_NAME = get_db('TEST_DATABASE_NAME_')
        DATABASES = {
            'default': {
                'ENGINE': DATABASE_ENGINE,
                'NAME': DATABASE_NAME,
                'USER': DATABASE_USER,
                'PASSWORD': DATABASE_PASSWORD,
                'HOST': DATABASE_HOST,
                'PORT': DATABASE_PORT,
            }
        }

    # [secrets]
    SECRET_KEY = config.get('secrets', 'SECRET_KEY')
    CSRF_MIDDLEWARE_SECRET = config.get('secrets', 'CSRF_MIDDLEWARE_SECRET')

    # [cookies]
    SESSION_COOKIE_DOMAIN = get_cookies('SESSION_COOKIE_DOMAIN')

    # [debug]
    DEBUG = config.getboolean('debug', 'DEBUG')
    TEMPLATE_DEBUG = config.getboolean('debug', 'TEMPLATE_DEBUG')
    VIEW_TEST = config.getboolean('debug', 'VIEW_TEST')
    value = get_optional_conf('debug', 'INTERNAL_IPS_')
    if value:
        INTERNAL_IPS = tuple(value.split())
    if config.getboolean('debug', 'SKIP_CSRF_MIDDLEWARE'):
        MIDDLEWARE_CLASSES = tuple([x for x in list(MIDDLEWARE_CLASSES)
                                   if not x.endswith('CsrfMiddleware')])

    # [email]
    SERVER_EMAIL = config.get('email', 'SERVER_EMAIL')
    EMAIL_HOST = config.get('email', 'EMAIL_HOST')

    # [admins]
    ADMINS = tuple(config.items('admins'))

    # [managers]
    MANAGERS = tuple(config.items('managers'))

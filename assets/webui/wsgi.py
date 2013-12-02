"""
WSGI config for assets project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
from django.core.handlers.wsgi import WSGIHandler

os.environ["DJANGO_SETTINGS_MODULE"] = "assets.webui.settings.main"

application = Sentry(WSGIHandler())

#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()

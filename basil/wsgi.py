"""
WSGI config for basil project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

env = os.environ.get('BASIL_ENV') or 'development'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'basil.settings.{}'.format(env))

application = get_wsgi_application()

import os
from basil.settings.base import *

DEBUG = True

INSTALLED_APPS += [
    'silk',
    'debug_toolbar',
    'django_extensions',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'silk.middleware.SilkyMiddleware',
]


GRAPHENE["MIDDLEWARE"] += [
    'graphene_django.debug.DjangoDebugMiddleware'
]

def show_toolbar(request):
    return False

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
}

from basil.settings.base import *

DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
    'silk',
    'django_extensions',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'silk.middleware.SilkyMiddleware', 
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}

def show_toolbar(request):
    return False

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
}
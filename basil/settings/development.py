import os
from basil.settings.base import *

DEBUG = True

SECRET_KEY = ')*q(vxory=r^j(gtdrdg*3*nbc$k%j@u&^rq&&(5v3^z7@h-%)'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'silk',
    'debug_toolbar',
    'django_extensions',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'silk.middleware.SilkyMiddleware', 
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('BASIL_DB_NAME') or 'basil',
        'USER': os.getenv('BASIL_DB_USER') or 'basil_user',
        'PASSWORD': os.getenv('BASIL_DB_PW') or 'password',
        'HOST': os.getenv('BASIL_DB_HOST') or '127.0.0.1',
        'PORT': os.getenv('BASIL_DB_PORT') or '5432'
    }
}

def show_toolbar(request):
    return False

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
}

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
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'db',
        'PORT': '5432'
    }
}

def show_toolbar(request):
    return False

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
}

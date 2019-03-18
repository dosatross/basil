import os
from basil.settings.base import *

SECRET_KEY = ')*q(vxory=r^j(gtdrdg*3*nbc$k%j@u&^rq&&(5v3^z7@h-%)'

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
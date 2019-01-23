import os
from basil.settings.base import BASE_DIR

DB = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'password'
DB_HOST = 'db'
DB_PORT = '5432'

DB = 'basil'
DB_USER = 'basil_user'
DB_HOST = '127.0.0.1'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT
    },
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
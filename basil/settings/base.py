import os

# https://blog.apptension.com/2017/11/09/django-settings-for-multiple-environments/

# REST Framework
REST_FRAMEWORK = {
	'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
	'COERCE_DECIMAL_TO_STRING': False,
	'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        
    )
}

ALLOWED_HOSTS = ['*']

# installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'corsheaders',
    'basil.apps.accounts',
    'basil.apps.transactions',
    'basil.apps.categories',
    
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('BASIL_DB_NAME') or 'basil-postgres',
        'USER': os.getenv('BASIL_DB_USER') or 'basil_user',
        'PASSWORD': os.getenv('BASIL_DB_PW') or 'password',
        'HOST': os.getenv('BASIL_DB_HOST') or '127.0.0.1',
        'PORT': os.getenv('BASIL_DB_PORT') or '5432'
    }
}

SECRET_KEY = os.getenv('BASIL_SECRET_KEY') or ')*q(vxory=r^j(gtdrdg*3*nbc$k%j@u&^rq&&(5v3^z7@h-%)'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

CORS_ORIGIN_WHITELIST = (
    '127.0.0.1:3000',
    'localhost:3000',
    '127.0.0.1',
    'localhost'
)

CORS_ALLOW_CREDENTIALS = True


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'basil.urls'

STATIC_URL = '/static/'
STATIC_ROOT = './static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'basil.wsgi.application'

AUTH_USER_MODEL = 'accounts.BasilUser'

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Australia/Melbourne'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

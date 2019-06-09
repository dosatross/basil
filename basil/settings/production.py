from basil.settings.base import *
import environ


env = environ.Env(
    SECRET_KEY=str,
    DATABASE_URL=str,
    ALLOWED_HOSTS=(list, []),
    DEBUG=(bool, False),
)

environ.Env.read_env(os.path.join(os.path.dirname(BASE_DIR), '.env'))

DATABASES = {
  'default': env.db(),
}

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
SECRET_KEY = env.str('SECRET_KEY')

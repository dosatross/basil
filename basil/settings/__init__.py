from split_settings.tools import optional, include
import os

env = os.environ.get('BASIL_ENV') or 'development'

include(
    '{}.py'.format(env),
    optional('local.py') # allow additional local settings
)
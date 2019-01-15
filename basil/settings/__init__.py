from split_settings.tools import optional, include

include(
    'apps.py',
    'base.py',
    'rest.py',
    'database.py',
    optional('local_settings.py')
)
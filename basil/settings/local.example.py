import os

REDIS_HOST = '192.168.1.7'
BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}

DATA_DIR = os.path.join(BASE_DIR,'..','data')
from os import environ

CACHE_STORE = environ.get('CACHE_STORE', '/tmp/cache')

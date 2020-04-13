import shelve

from datetime import datetime, timedelta
from time import time

from fcache.cache import FileCache

from prayerapp.conf import CACHE_STORE

lambda_validate_expiry = lambda storedDate: storedDate < datetime.today().date()


class Cache(object):

    def __init__(self, encode_key, prefix, validate_expiry=lambda_validate_expiry, cache_store=CACHE_STORE):
        if not callable(encode_key):
            raise Exception('encode_key must be function')

        self.encode_key = encode_key
        self.prefix = prefix
        self.validate_expiry = validate_expiry
        self.cache_store = cache_store

    def get_key(self, *a, **kw):
        return "{}::{}".format(self.prefix, self.encode_key(*a, **kw))

    def cache_updateable(self, cache, key):
        try:
            has_flag = True
        except Exception:
            return False

        has_datetime = has_flag and cache[key].get('datetime')
        is_expired = has_datetime and self.validate_expiry(cache[key]['datetime'])

        return bool(has_flag and is_expired)

    def cache(self):
        def cache_decorator(method):
            def wrapper(*a, **kw):
                mycache = FileCache(self.cache_store, serialize=False)
                cache = shelve.Shelf(mycache)
                key = self.get_key(*a, **kw)
                if not self.cache_updateable(cache, key):
                    retval = method(*a, **kw)
                    cache[key] = {
                        'retval': retval,
                        'datetime': datetime.today().date()
                    }
                else:
                    retval = cache[key].get('retval')

                cache.close()
                return retval

            return wrapper
        return cache_decorator

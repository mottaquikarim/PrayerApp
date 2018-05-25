import os
import pytest
import shelve
import time

from datetime import datetime
from requests import RequestException
from unittest import TestCase
from unittest.mock import patch

from prayerapp.cache import Cache, lambda_validate_expiry


class TestCache(TestCase):

    def test_init(self):
        with pytest.raises(Exception) as e:
            c = Cache('a', 'b', 'c', 'd')

        c = Cache(lambda: True, 'prefix', lambda: True, 'd')

        assert c.prefix == 'prefix'
        assert c.cache_store == 'd'

    def test_key(self):
        encode_key = lambda a, b: "{},{}".format(a, b)
        c = Cache(encode_key, 'prefix')
        key = c.get_key(1, 2)
        assert key == 'prefix::1,2'

    def test_cache_updateable(self):
        encode_key = lambda a, b: "{},{}".format(a, b)
        c = Cache(encode_key, 'prefix', validate_expiry=lambda *a: True)
        key = c.get_key(1, 2)
        cache = shelve.open(c.cache_store)

        try:
            del cache[key]
        except:
            pass

        assert c.cache_updateable(cache, key) is False

        cache[key] = {
            'retval': 'test',
            'datetime': datetime.today().date()
        }

        assert c.cache_updateable(cache, key) is True
        cache.close()

    def test_decorator(self):
        encode_key = lambda a, b, *aa, **kw: "{},{}".format(a, b)
        retval = int(time.time())
        c = Cache(encode_key, 'prefix', validate_expiry=lambda *a: a[0])

        try:
            cache = shelve.open(c.cache_store)
            del cache[c.get_key(True, 1)]
            cache.close()
        except:
            pass

        @c.cache()
        def _cache(a, b, t):
            if not t:
                return int(time.time())
            return t

        cache_ret = _cache(True, 1, retval)
        assert cache_ret == retval

        cache_ret = _cache(True, 1, None)
        assert cache_ret == retval

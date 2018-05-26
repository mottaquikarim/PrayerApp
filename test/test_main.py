import pytest
import shelve

from datetime import datetime
from os import environ
from time import time
from unittest.mock import patch

from prayerapp.conf import CACHE_STORE
from prayerapp.main import cached_geocode, cached_timezone, get_prayer_times

mock_timezone_payload = {'dstOffset': 3600, 'rawOffset': -18000, 'status': 'OK', 'timeZoneId': 'America/New_York', 'timeZoneName': 'Eastern Daylight Time'}
mock_timezone_bad_payload = {'dstOffset': None, 'rawOffset': -18000, 'status': 'OK', 'timeZoneId': 'America/New_York', 'timeZoneName': 'Eastern Daylight Time'}


def test_env_vars_exist():
    assert environ.get('TEST') == '1'


@patch('prayerapp.main.cached_timezone')
def test_get_prayer_times(MockCachedTimezone):
    MockCachedTimezone.return_value = mock_timezone_payload
    times = get_prayer_times(40.7128, -74.0059, 1527249151)
    assert times['imsak'] == '3:47am'
    assert times['fajr'] == '3:57am'


@patch('prayerapp.main.cached_timezone')
def test_get_prayer_times_err(MockCachedTimezone):

    MockCachedTimezone.return_value = mock_timezone_bad_payload
    with pytest.raises(Exception) as e:
        times = get_prayer_times(40.7128, -74.0059, 1527249151)


def test_cached_timezone():
    cache = shelve.open(CACHE_STORE)
    cache['BY_TIMEZONE::40.7128,-74.0059'] = {
        'retval': mock_timezone_payload,
        'datetime': datetime.today().date()
    }
    tz = cached_timezone('test', 40.7128, -74.0059, 1527249151)
    cache.close()

    assert tz == mock_timezone_payload


def test_cached_geocode():
    expected_retval = [40.7127753, -74.0059728]
    cache = shelve.open(CACHE_STORE)
    cache['BY_CITY::nyc,us'] = {
        'retval': expected_retval,
        'datetime': datetime.today().date()
    }
    gc = cached_geocode('test')
    cache.close()

    assert gc == expected_retval

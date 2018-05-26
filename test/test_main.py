import pytest
import shelve

from datetime import datetime
from os import environ
from time import time
from types import SimpleNamespace
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


@patch('prayerapp.main.Geocode')
def test_cached_geocode(MockGeocode):
    expected_retval = [40.7127753, -74.0059728]
    retval = {'results': [
        {
            'geometry': {
                'location': {
                    'lat': expected_retval[0],
                    'lng': expected_retval[1],
                }
            }
        }
    ]}

    def fake_method(*a, **kw):
        return SimpleNamespace(query=lambda: retval)

    MockGeocode.side_effect = fake_method

    try:
        cache = shelve.open(CACHE_STORE)
        del cache['BY_CITY::nyc,us']
        cache.close()
    except:
        pass

    cache = shelve.open(CACHE_STORE)
    cache['BY_CITY::nyc,us'] = {
        'retval': retval,
        'datetime': datetime.today().date()
    }
    gc = cached_geocode('test')
    cache.close()

    assert gc == expected_retval

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


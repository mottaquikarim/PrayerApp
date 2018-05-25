import pytest

from os import environ
from time import time
from unittest.mock import patch

from prayerapp.main import cached_timezone, get_prayer_times

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

# bogus, TODO: figure out a way to fix


def test_cached_timezone():
    tz = cached_timezone('test', 40.7128, -74.0059, 1527249151)

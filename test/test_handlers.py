from unittest.mock import patch
from json import loads

from prayerapp.handlers import by_location


@patch('prayerapp.handlers.get_prayer_times')
def test_by_location(MockGetPrayerTimes):
    MockGetPrayerTimes.return_value = {
        "imsak": "5:09am",
        "fajr": "5:19am",
        "sunrise": "6:23am",
        "dhuhr": "12:08pm",
        "asr": "3:26pm",
        "sunset": "5:53pm",
        "maghrib": "5:53pm",
        "isha": "6:57pm",
        "midnight": "12:08am"}

    res = by_location({
        'pathParameters': {
            'lat': 40.7127753,
            'lng': -74.0059728,
        },
        'queryStringParameters': {
            'date': 15272491510,
        }
    }, {})

    times = loads(res.get('body'))
    assert times['imsak'] == '5:09am'
    assert times['fajr'] == '5:19am'


@patch('prayerapp.handlers.get_prayer_times')
def test_by_location_err(MockGetPrayerTimes):
    def exc(*a, **kw):
        raise Exception('timezone offsets not found!')

    MockGetPrayerTimes.side_effect = exc
    res = by_location({
        'pathParameters': {
            'lat': 1,
            'lng': 2,
        },
        'queryStringParameters': {
            'date': 1527249151,
        }
    }, {})

    assert res.get('body') == 'timezone offsets not found!'

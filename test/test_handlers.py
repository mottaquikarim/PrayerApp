from json import loads

from prayerapp.handlers import by_location


def test_by_location():
    res = by_location({
        'pathParameters': {
            'lat': 40.7127753,
            'lng': -74.0059728,
        },
        'queryStringParameters': {
            'date': 1527249151,
        }
    }, {})

    times = loads(res.get('body'))
    assert times['imsak'] == '3:47am'
    assert times['fajr'] == '3:57am'


def test_by_location_err():
    res = by_location({
        'pathParameters': {
            'lat': 1,
            'lng': 2,
        },
        'queryStringParameters': {
            'date': 1527249151,
        }
    }, {})

    print(res)
    assert res.get('body') == 'timezone offsets not found!'

import os

from datetime import datetime, date

from prayerapp.cache import Cache
from prayerapp.google_apis import Geocode, GetTimezone
from prayerapp.praytimes import PrayTimes

geocache = Cache(lambda *a, **kw: '{},{}'.format(
    kw.get('city', 'nyc'),
    kw.get('country', 'us')), 'BY_CITY',)
tzcache = Cache(lambda *a, **kw: '{},{}'.format(a[1], a[2]), 'BY_TIMEZONE')


@geocache.cache()
def cached_geocode(api_key, city='nyc', country='us'):
    geocoded_data = Geocode(api_key, {
        'address': '{},{}'.format(city, country),
    }).query()

    location = geocoded_data['results'][0]['geometry']['location']
    return [location['lat'], location['lng']]


@tzcache.cache()
def cached_timezone(api_key, lat, lng, date):
    return GetTimezone(api_key, {
        'location': "{},{}".format(lat, lng),
        'timestamp': date
    }).query()


def get_prayer_times(lat, lng, date, calcMethod="ISNA", timeFmt="12h"):
    timezone_data = cached_timezone(os.environ.get('GOOGLE_API_KEY'), lat, lng, date)

    rawOffset = timezone_data.get('rawOffset', None)
    dstOffset = timezone_data.get('dstOffset', None)
    if not rawOffset or not dstOffset:
        raise Exception('timezone offsets not found!')

    pt = PrayTimes(calcMethod=calcMethod)
    dateQuery = datetime.fromtimestamp(int(date)).date()
    locationTuple = (float(lat), float(lng))
    offset = rawOffset / (60*60)
    isDayLightSavings = dstOffset
    timeFormat = timeFmt

    times = pt.getTimes(dateQuery, locationTuple, offset, isDayLightSavings, timeFormat)
    return times

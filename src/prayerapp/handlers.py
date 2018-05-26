from json import dumps

from prayerapp.lambda_event import LocationLambdaEvent
from prayerapp.main import get_prayer_times


def by_location(event, context):
    l = LocationLambdaEvent.from_event_dict(event)

    try:
        res = get_prayer_times(l.lat, l.lng, l.time_, l.calc_method, l.timefmt)
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e),
        }

    return {
        'statusCode': 200,
        'body': dumps(res)
    }

from datetime import datetime
from json import dumps
from time import time


class LambdaEvent(object):

    def __init__(self, time_, calc_method='ISNA', timefmt='12h'):
        self.time_ = int(time_ or time())

        self.calc_method = calc_method or 'ISNA'
        self.timefmt = timefmt or '12h'

    @classmethod
    def from_event_dict(cls, event):
        query_params = event.get('queryStringParameters') or {}
        ts = query_params.get('date')
        calc_method = query_params.get('calc-method')
        timefmt = query_params.get('time-format')

        return cls(ts, calc_method, timefmt)


class LocationLambdaEvent(LambdaEvent):

    def __init__(self, lat, lng, *a, **kw):
        super().__init__(*a, **kw)
        self.lat = lat
        self.lng = lng

    @classmethod
    def from_event_dict(cls, event):
        # TODO: this sucks, come up with a better way to implement
        cinst = LambdaEvent.from_event_dict(event)

        lat = event['pathParameters']['lat']
        lng = event['pathParameters']['lng']

        return cls(lat, lng, cinst.time_, cinst.calc_method, cinst.timefmt)

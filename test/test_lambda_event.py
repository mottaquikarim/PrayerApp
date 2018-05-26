import pytest
import time

from unittest import TestCase
from unittest.mock import patch

from prayerapp.conf import CACHE_STORE
from prayerapp.lambda_event import LambdaEvent, LocationLambdaEvent

now = int(time.time())


class TestLambdaEvent(TestCase):

    def test_lambda_event(self):

        l = LambdaEvent(now)

        assert l.time_ == now
        assert l.timefmt == '12h'
        assert l.calc_method == 'ISNA'

    def test_lambda_from_event(self):

        evt = {
            'queryStringParameters': {
                'date': now,
                'calc-method': 'test',
                'time-format': 'test'
            }
        }

        l = LambdaEvent.from_event_dict(evt)

        assert l.time_ == now
        assert l.timefmt == 'test'
        assert l.calc_method == 'test'

    def test_lambda_from_event_missing_params(self):

        evt = {
            'queryStringParameters': {
                'date': now,
            }
        }

        l = LambdaEvent.from_event_dict(evt)

        assert l.time_ == now
        assert l.timefmt == '12h'
        assert l.calc_method == 'ISNA'


class TestLocationLambdaEvent(TestCase):

    def test_lambda_event(self):

        l = LocationLambdaEvent(1, 2, now)

        assert l.time_ == now
        assert l.timefmt == '12h'
        assert l.calc_method == 'ISNA'
        assert l.lat == 1
        assert l.lng == 2

    def test_lambda_from_event(self):

        evt = {
            'pathParameters': {
                'lat': 1,
                'lng': 2,
            },
            'queryStringParameters': {
                'date': now,
                'calc-method': 'test',
                'time-format': 'test'
            }
        }

        l = LocationLambdaEvent.from_event_dict(evt)

        assert l.time_ == now
        assert l.timefmt == 'test'
        assert l.calc_method == 'test'
        assert l.lat == 1
        assert l.lng == 2

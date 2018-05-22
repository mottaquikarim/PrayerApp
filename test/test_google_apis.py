import os
import pytest

from unittest import TestCase
from unittest.mock import patch

from prayerapp.google_apis import GoogleAPIs


class TestGoogleAPIs(TestCase):

    def test_get_params(self):
        p = GoogleAPIs.get_params(None)

        assert p == {}

        p = GoogleAPIs.get_params({'t': 1})
        assert p == {'t': 1}

    def test_paramify(self):
        p = GoogleAPIs.paramify()

        assert p == ""

        p = GoogleAPIs.paramify({'t': 1, 's': 2})
        assert p == "t=1&s=2"

    def test_validate_params(self):
        with pytest.raises(Exception) as e:
            GoogleAPIs.validate_params()

        p = GoogleAPIs.validate_params('test', {'t': 1})
        assert p.get('api_key') == 'test'
        assert p.get('t') == 1

    def test_validate_params_requireds(self):
        with pytest.raises(Exception) as e:
            p = GoogleAPIs.validate_params('t', {'p': 1}, {'d': {'type': int, }})

        with pytest.raises(Exception) as e:
            p = GoogleAPIs.validate_params('t', {'d': '1'}, {'d': {'type': int, }})

        with pytest.raises(Exception) as e:
            p = GoogleAPIs.validate_params('t', {'d': '1'}, {'d': {'type': str,
                                                                   "matches": ".*,.*"}})

        p = GoogleAPIs.validate_params('t', {'d': 'a,b'}, {'d': {'type': str,
                                                                 "matches": ".*,.*"}})
        assert p == {'api_key': 't', 'd': 'a,b'}

    @patch('prayerapp.google_apis.requests.get')
    def test_do_api_call(self, MockGetReq):
        class MockGet(object):

            def json():
                return {'test': 1}

        MockGetReq.return_value = MockGet
        ret = GoogleAPIs.do_api_call('test', {
            'api_key': 'test'
        })

        MockGetReq.assert_called_once()
        assert ret == {'test': 1}

    @patch('prayerapp.google_apis.requests.get')
    def test_do_api_call_exception(self, MockGetReq):
        class MockGet(object):

            def json():
                raise Exception()

        MockGetReq.return_value = MockGet

        with pytest.raises(Exception) as e:
            ret = GoogleAPIs.do_api_call('test', {
                'api_key': 'test'
            })

            assert e == {'error': 'Failed to geocode latitude/longitude', }

    @patch('prayerapp.google_apis.GoogleAPIs.do_api_call')
    def test_geocode(self, MockDoApiCall):
        GoogleAPIs.geocode()

        MockDoApiCall.assert_called_once()

    @patch('prayerapp.google_apis.GoogleAPIs.do_api_call')
    def test_get_timezone(self, MockDoApiCall):
        GoogleAPIs.get_timezone()

        MockDoApiCall.assert_called_once()

    # def test_get_timezone_ftest(self):
    #     d = GoogleAPIs.get_timezone(api_key=os.environ.get('GOOGLE_API_KEY'), params={
    #         'location': '40.7128,-74.0059',
    #         'timestamp': 1497611699,
    #     })

    #     assert d.get('timeZoneId') == 'America/New_York'

    # def test_geocode_ftest(self):
    #     e = GoogleAPIs.geocode(api_key=os.environ.get('GOOGLE_API_KEY'), params={
    #         'address': 'nyc, us',
    #     })

    #     assert len(e.get('results')) > 0

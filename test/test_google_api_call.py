import os
import pytest
from types import SimpleNamespace

from requests import RequestException
from unittest import TestCase
from unittest.mock import patch

from prayerapp.google_apis import GetTimezone, Geocode,\
    GoogleAPICall, GoogleQueryEndpoint,\
    GValidationException, GValidator, ParamExists, ParamValidType, \
    ParamValidFmt


class TestGValidator(TestCase):

    def test_gvalidator(self):
        gv = GValidator('test', 'test', 'test')
        assert gv.param == 'test'
        assert gv.name == 'test'
        assert gv.val == 'test'

    def test_validate(self):
        with pytest.raises(NotImplementedError) as e:
            gv = GValidator('test', 'test', 'test')
            gv.validate()


class TestParamExists(TestCase):

    def test_param_exists(self):
        gv = ParamExists('', 't', 't')
        with pytest.raises(GValidationException) as e:
            gv.validate()

        gv.param = 't'
        gv.validate()


class TestParamValidType(TestCase):

    def test_param_valid_type(self):
        gv = ParamValidType('', 't', {'type': int})
        with pytest.raises(GValidationException) as e:
            gv.validate()

        gv.param = 1
        gv.validate()


class TestParamValidFmt(TestCase):

    def test_param_valid_fmt(self):
        gv = ParamValidFmt('test', 'location', {'type': str, 'matches': '.*,.*'})
        with pytest.raises(GValidationException) as e:
            gv.validate()

        gv2 = ParamValidFmt('test', 'location', {})
        gv2.validate()

        gv.val = {'type': str, 'matches': '.*,.*'}
        gv.param = 'a,b'
        gv.validate()


class TestGoogleAPICall(object):

    def test_init(self):

        g = GoogleAPICall('test')
        assert g.params == {'api_key': 'test'}
        assert g.required_params == {}

    def test_get_endpoint(self):
        g = GoogleAPICall('test', params={
            'test': 1,
        })

        endpt = g.get_endpoint('/test_endpoint')
        assert endpt == 'https://maps.googleapis.com/test_endpoint?api_key=test&test=1'

    def test_validate_params(self):
        g = GoogleAPICall('test', params={
            'test': 1,
        })

        # assert that if required params not present
        # we get back input params mutated with api_key
        g.validate_params()
        assert g.params == {'test': 1, 'api_key': 'test'}

        # assert error raised if required param does not exist
        with pytest.raises(GValidationException) as e:
            g = GoogleAPICall('test', params={
                'test': 1,
            }, required_params={
                'test': {'type': str},
                'timestamp': {'type': int},
            })

        # assert no errors raised if we pass in required params
        # and params that match requirements
        g = GoogleAPICall('test', params={
            'test': '1',
            'timestamp': 2,
        }, required_params={
            'test': {'type': str, 'matches': '\d'},
            'timestamp': {'type': int},
        })

        assert g.params == {'test': '1', 'api_key': 'test', 'timestamp': 2}


class TestGoogleQueryEndpoint(TestCase):

    def test_init(self):
        gq = GoogleQueryEndpoint('/test_endpoint', 'test', params={
            'test': '1',
            'timestamp': 2,
        }, required_params={
            'test': {'type': str, 'matches': '\d'},
            'timestamp': {'type': int},
        })

        assert gq.endpoint == '/test_endpoint'
        assert gq.params == {'test': '1', 'api_key': 'test', 'timestamp': 2}

    @patch('prayerapp.google_apis.requests.get')
    def test_query(self, MockRequestsGet):
        def _getJson(*a, **kw):
            return {}

        MockRequestsGet.return_value = SimpleNamespace(json=_getJson)
        gq = GoogleQueryEndpoint('/test_endpoint', 'test', params={
            'test': '1',
            'timestamp': 2,
        }, required_params={
            'test': {'type': str, 'matches': '\d'},
            'timestamp': {'type': int},
        })

        assert gq.query() == {}


class TestGeocode(TestCase):

    def test_geocode(self):
        Geocode('test', {
            'location': 'a,b',
            'timestamp': 2,
        })


class TestGetTimezone(TestCase):

    def test_gettimezone(self):
        GetTimezone('test', {
            'address': 'a,b',
        })

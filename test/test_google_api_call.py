import os
import pytest

from unittest import TestCase
from unittest.mock import patch

from prayerapp.google_apis import GoogleAPICall, GoogleQueryEndpoint,\
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
        with pytest.raises(GValidationException) as e:
            gv2.validate()

        gv.val = {'type': str, 'matches': '.*,.*'}
        gv.param = 'a,b'
        gv.validate()


class TestGoogleAPICall(object):

    def test_init(self):
        with pytest.raises(Exception) as e:
            g = GoogleAPICall()

        g = GoogleAPICall(api_key='test')
        assert g.params == {'api_key': 'test'}
        assert g.required_params == {}

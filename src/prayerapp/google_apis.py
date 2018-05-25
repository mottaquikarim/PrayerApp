import re
import requests


class GValidationException(Exception):
    pass


class GValidator(object):

    def __init__(self, param, name, val):
        self.param = param
        self.name = name
        self.val = val

    def validate(self):
        raise NotImplementedError()


class ParamExists(GValidator):
    exception_str = 'Required param {} not provided'

    def validate(self):
        if not self.param:
            raise GValidationException(self.exception_str.format(self.name))


class ParamValidType(GValidator):
    exception_str = 'Required param {} is not correct type, expected {} got {}'

    def validate(self):
        if not isinstance(self.param, self.val.get('type')):
            raise GValidationException(self.exception_str
                                       .format(self.name, self.val.get('type'), type(self.param)))


class ParamValidFmt(GValidator):
    exception_str = 'Required param {} does not match format {}'

    def validate_val_matches(self):
        if not self.val.get('matches'):
            return

        r = re.compile(self.val.get('matches'))
        if not r.match(self.param):
            raise GValidationException(self.exception_str
                                       .format(self.name, self.val.get('matches')))

    def validate(self):
        self.validate_val_matches()


class GoogleAPICall(object):
    URL_BASE = "https://maps.googleapis.com"

    def __init__(self, api_key, params=None, required_params=None):
        self.params = params or {}
        self.params.update({'api_key': api_key})
        self.required_params = required_params or {}

        self.validate_params()
        self.usable_params = self.paramify()

    def paramify(self):
        return '&'.join(["%s=%s" % (x, self.params[x]) for x in sorted(self.params.keys())])

    def get_endpoint(self, endpoint):
        return "{base}{endpoint}?{params}".format(base=self.URL_BASE,
                                                  endpoint=endpoint, params=self.usable_params)

    def validate_params(self):
        required_params = self.required_params
        params = self.params

        for rparam_name, rparam_val in required_params.items():
            param = params.get(rparam_name)
            validators = [ParamExists, ParamValidType, ParamValidFmt]
            for validator in validators:
                validator(param, rparam_name, rparam_val).validate()

    def do_api_call(self, endpoint):
        return requests.get(self.get_endpoint(endpoint)).json()


class GoogleQueryEndpoint(GoogleAPICall):

    def __init__(self, endpoint, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = endpoint

    def query(self):
        return self.do_api_call(self.endpoint)


class Geocode(GoogleQueryEndpoint):
    endpoint = '/maps/api/geocode/json'
    required_params = {
        'location': {'type': str, 'matches': '.*,.*'},
        'timestamp': {'type': int},
    }

    def __init__(self, api_key, params):
        super().__init__(self.endpoint, api_key, params=params,
                         required_params=self.required_params)


class GetTimezone(GoogleQueryEndpoint):
    endpoint = '/maps/api/timezone/json'
    required_params = {
        'address': {'type': str, 'matches': '.*,.*'},
    }

    def __init__(self, api_key, params):
        super().__init__(self.endpoint, api_key, params=params,
                         required_params=self.required_params)

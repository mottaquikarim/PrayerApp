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

    def validate_val_keys(self):
        if not self.val.get('matches') or not self.val.get('type') == str:
            raise GValidationException('type and format required')

    def validate_val_matches(self):
        r = re.compile(self.val.get('matches'))
        if not r.match(self.param):
            raise GValidationException(self.exception_str
                                       .format(self.name, self.val.get('matches')))

    def validate(self):
        self.validate_val_keys()
        self.validate_val_matches()


class GoogleAPICall(object):
    URL_BASE = "https://maps.googleapis.com"

    def __init__(self, api_key=None, params=None, required_params=None):
        if not api_key:
            raise Exception({"error": "api_key required", })

        self.params = params or {}
        self.params.update({'api_key': api_key})
        self.required_params = required_params or {}

        self.validate_params()
        self.usable_params = self.paramify()

    def paramify(self):
        return '&'.join(["%s=%s" % (x, self.params[x]) for x in self.params.keys()])

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
        try:
            return requests.get(self.get_endpoint(endpoint)).json()
        except requests.RequestException as e:
            raise Exception({'error': 'Failed to geocode latitude/longitude', })


class GoogleQueryEndpoint(GoogleAPICall):

    def __init__(self, endpoint, *args, **kwargs):
        super.__init__(*args, **kwargs)
        self.endpoint = endpoint

    def query(self):
        return self.do_api_call(self.endpoint)


class GoogleAPIs(object):
    URL_BASE = "https://maps.googleapis.com"

    @staticmethod
    def get_params(params):
        if not params:
            params = {}

        return params

    @staticmethod
    def paramify(params=None):
        params = GoogleAPIs.get_params(params)
        return '&'.join(["%s=%s" % (x, params[x]) for x in params.keys()])

    @staticmethod
    def validate_params(api_key=None, params=None, required_params=None):
        print(api_key, params, required_params)
        params = GoogleAPIs.get_params(params)
        if not api_key:
            raise Exception({"error": "api_key required", })
        else:
            params.update({'api_key': api_key})

        if not required_params:
            required_params = {}

        for rparam_name, rparam_val in required_params.items():
            param = params.get(rparam_name)
            if not param:
                raise Exception('Required param {} not provided'.format(rparam_name))

            if not isinstance(param, rparam_val.get('type')):
                raise Exception('Required param {} is not correct type, expected {} got {}'
                                .format(rparam_name, rparam_val.get('type'), type(param)))

            if rparam_val.get('matches') and rparam_val.get('type') == str:
                r = re.compile(rparam_val.get('matches'))
                if not r.match(param):
                    raise Exception('Required param {} does not match format {}'
                                    .format(rparam_name, rparam_val.get('matches')))

        return params

    @staticmethod
    def do_api_call(endpoint, api_key=None, params=None, required_params=None):
        params = GoogleAPIs.get_params(params)
        usable_params = GoogleAPIs.paramify(GoogleAPIs.validate_params(api_key=api_key,
                                                                       params=params, required_params=required_params))
        url = "{base}{endpoint}?{params}".format(base=GoogleAPIs.URL_BASE,
                                                 endpoint=endpoint, params=usable_params)

        try:
            return requests.get(url).json()
        except requests.RequestException as e:
            raise Exception({'error': 'Failed to geocode latitude/longitude', })

    @staticmethod
    def geocode(api_key=None, params=None):
        return GoogleAPIs.do_api_call('/maps/api/geocode/json',
                                      api_key=api_key, params=GoogleAPIs.get_params(params),
                                      required_params={'location': {'type': str, 'matches': '.*,.*'},
                                                       'timestamp': {'type': int},
                                                       })

    @staticmethod
    def get_timezone(api_key=None, params=None):
        return GoogleAPIs.do_api_call('/maps/api/timezone/json',
                                      api_key=api_key, params=GoogleAPIs.get_params(params),
                                      required_params={
                                          'address': {'type': str, 'matches': '.*,.*'},
                                      })

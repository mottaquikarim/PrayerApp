import re
import requests


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

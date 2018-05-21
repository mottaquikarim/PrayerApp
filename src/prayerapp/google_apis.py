import requests


class GoogleAPIs(object):
    URL_BASE = "https://maps.googleapis.com"

    @staticmethod
    def get_params(params):
        if not params:
            return {}

        return params

    @staticmethod
    def paramify(params=None):
        params = GoogleAPIs.get_params(params)
        return '&'.join(["%s=%s" % (x, params[x]) for x in params.keys()])

    @staticmethod
    def validate_params(api_key=None, params=None):
        params = GoogleAPIs.get_params(params)
        if not api_key:
            raise Exception({"error": "api_key required", })
        else:
            params.update({'api_key': api_key})

        return params

    @staticmethod
    def do_api_call(endpoint, api_key=None, params=None):
        params = GoogleAPIs.get_params(params)
        usable_params = GoogleAPIs.paramify(GoogleAPIs.validate_params(api_key=api_key, params=params))
        url = "{base}{endpoint}?{params}".format(base=GoogleAPIs.URL_BASE,
                                                 endpoint=endpoint, params=usable_params)

        try:
            return requests.get(url).json()
        except requests.RequestException as e:
            raise Exception({'error': 'Failed to geocode latitude/longitude', })

    @staticmethod
    def geocode(api_key=None, params=None):
        return GoogleAPIs.do_api_call('/maps/api/geocode/json',
                                      api_key=api_key, params=GoogleAPIs.get_params(params))

    @staticmethod
    def get_timezone(api_key=None, params=None):
        return GoogleAPIs.do_api_call('/maps/api/timezone/json',
                                      api_key=api_key, params=GoogleAPIs.get_params(params))

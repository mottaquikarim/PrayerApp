from requests import get
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn


class Resp(object):

    host = BuiltIn().get_variable_value("${HOST}")

    @property
    def url(self):
        return "{}{}".format(self.host, self.path)

    @property
    def status_code(self):
        return self.r.status_code

    @property
    def data(self):
        return self.r and self.r.json() or {}

    def __init__(self, path, payload):
        self.path = path
        self.payload = payload


class GetResp(Resp):

    def __init__(self, path, payload):
        super().__init__(path, payload)
        self.r = get(self.url, json=self.payload)


def make_request_for_status_code(path, payload=None):
    return GetResp(path, payload).status_code


def make_request_for_response(path, payload=None):
    return GetResp(path, payload).data

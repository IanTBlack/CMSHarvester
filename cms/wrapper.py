from datetime import datetime
import requests
from requests.compat import urljoin

from .core import API_URL, format_datetime

class CRLX():
    def __init__(self, api_url, verify: bool = True, verbose: bool = False, timeout: int = 300):
        self._api_url = api_url
        self._verify = verify
        self._verbose = verbose
        self._timeout = timeout

    def _get_json(self, url: str, params: dict):
        params['format'] = 'json'
        req = requests.get(url, params = params, timeout = self._timeout)
        if req.status_code == requests.codes.ok:
            json_data = req.json()
            return json_data
        else:
            if self._verbose is True:
                print(req.url)
                print(req.content)
            raise requests.exceptions.ConnectionError

    def get_instruments(self,
                        begin_datetime: datetime | None = None,
                        end_datetime: datetime | None = None,
                        enabled: bool = True):
        req_url = urljoin(self._api_url, 'sensor')
        params = {'enabled': enabled,
                  'date_after': format_datetime(begin_datetime) if begin_datetime else None,
                  'date_before': format_datetime(end_datetime) if end_datetime else None}
        params = {k:v for k,v in params.items() if v is not None}
        json_data = self._get_json(req_url, params = params)
        return json_data

    def get_instrument_variables(self, instrument_id: str, begin_datetime: datetime | None = None,
                                  end_datetime: datetime | None = None, enabled: bool = True):
        req_url = urljoin(self._api_url, 'parameter')
        params = {'enabled': enabled,
                  'date_after': format_datetime(begin_datetime) if begin_datetime else None,
                  'date_before': format_datetime(end_datetime) if end_datetime else None,
                  'sensor_id': instrument_id}
        params = {k:v for k,v in params.items() if v is not None}
        json_data = self._get_json(req_url, params = params)
        return json_data



    def get_variable_data(self, model: str, begin_datetime: datetime | None = None, end_datetime: datetime | None = None):
        req_url = urljoin(self._api_url, 'decimateData')
        params = {'model': model,
                  'decfactr': 1, #1
                  'date_0': format_datetime(begin_datetime) if begin_datetime else None,
                  'date_1': format_datetime(end_datetime) if end_datetime else None}
        params = {k:v for k,v in params.items() if v is not None}
        json_data = self._get_json(req_url, params = params)
        return json_data

class CMS(CRLX):
    def __init__(self, api_url: str = API_URL, verify: bool = True, verbose: bool = False, timeout : int = 300):
        super().__init__(api_url, verify, verbose, timeout)

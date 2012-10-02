import requests

class RESTCall:
    def __init__(self, api_url, login, api_key):
        self.api_url = api_url
        self.login = login
        self.api_key = api_key

    def _make_query(self, path):
        opts = {'headers': {'accept': 'application/json'},
                'auth': (self.login, self.api_key)}
        result = requests.get(self.api_url + path, **opts)
        return result.json

    def get_servers_info(self):
        return self._make_query('/servers/info')

    def get_dive_name(self, drive_uuid):
        drive_info = self._make_query('/drives/' + drive_uuid + '/info')
        return drive_info.get('name', None)

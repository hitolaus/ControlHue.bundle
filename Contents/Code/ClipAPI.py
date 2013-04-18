class ClipAPI:
    """ Implementation of the Clip API used by Philips Hue API """

    API_USERNAME = 'control-hue-user'

    def __init__(self, bridge):
        self.api = 'http://' + bridge + '/api'

    # http://<bridge ip address>/api/newdeveloper/lights
    # GET
    def list(self):
        results = self._request(self.api + '/' + self.API_USERNAME + '/lights')

        # [ { "active": true, "name", "Foo"} ]
        return results

    # http://<bridge ip address>/api/newdeveloper/lights/1/state
    # PUT{"on":true}
    def on(self, light):
        self._request(self.api + '/' + self.API_USERNAME + '/lights/' + light + '/state', 'PUT')

    def off(self, light):
        self._request(self.api + '/' + self.API_USERNAME + '/lights/' + light + '/state', 'PUT')

    # http://<bridge ip address>/api
    # POST {"devicetype":"test user","username":"newdeveloper"}
    def _authenticate(self):
        return None

    def _request(self, url, method='GET'):
        results = JSON.ObjectFromURL(url, method=method)

        if self._is_error(results):
            raise LinkError('Not linked')

    def _is_error(self, data):
        # [ { "error": { "type": 1 } }]
        return False


class LinkError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

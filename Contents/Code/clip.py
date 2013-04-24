class ClipAPI:
    """ Implementation of the Clip API used by Philips Hue API """

    API_USERNAME = 'testtesttest1'

    # [{'internalipaddress': '10.0.0.35', 'id': '001788fffe096c19', 'macaddress': '00:17:88:09:6c:19'}]
    def __init__(self, bridge):
        self.api = 'http://' + bridge['internalipaddress'] + '/api'

    # http://<bridge ip address>/api/newdeveloper/lights
    # GET
    def list(self):
        results = self.request(self.api + '/' + self.API_USERNAME + '/lights')

        lights = []

        #{'1': {'name': 'Miss K'}, '3': {'name': 'Ceiling Lamp'}, '2': {'name': 'AJ Floor'}}
        for key, value in results.items():
            lights.append({'id': key, 'name': value['name'], 'active': False})

        # [ { "active": true, "name", "Foo"} ]
        return lights

    # http://<bridge ip address>/api/newdeveloper/lights/1/state
    # PUT{"on":true}
    def on(self, light):
        data = JSON.StringFromObject({'on': True})
        self.request(self.api + '/' + self.API_USERNAME + '/lights/' + light + '/state', 'PUT', data)

    def off(self, light):
        data = JSON.StringFromObject({'on': False})
        self.request(self.api + '/' + self.API_USERNAME + '/lights/' + light + '/state', 'PUT', data)

    # http://<bridge ip address>/api
    # POST {"devicetype":"test user","username":"newdeveloper"}
    def authenticate(self):
        register = {'devicetype': 'test user', 'username': self.API_USERNAME}

        resp = HTTP.Request(self.api, data=JSON.StringFromObject(register)).content

        Log(resp)

        if self.is_link_error(JSON.ObjectFromString(resp)):
            raise LinkError('Not linked')

    def request(self, url, method='GET', data=None):
        #results = JSON.ObjectFromURL(url, method=method)

        resp = HTTP.Request(url, method=method, data=data).content
        results = JSON.ObjectFromString(resp)

        Log(results)

        if self.is_auth_error(results):
            self.authenticate()
            # Retry
            results = JSON.ObjectFromURL(url, method=method)
            Log(results)

        if self.is_link_error(results):
            raise LinkError('Not linked')

        return results

    def is_auth_error(self, data):
        if len(data):
            return False

        if 'error' in data[0]:
            if data[0]['error']['type'] == 1:
                return True
        return False

    def is_link_error(self, data):
        if len(data):
            return False

        if 'error' in data[0]:
            if data[0]['error']['type'] == 101:
                return True
        return False

    def is_error(self, data):
        # [ { "error": { "type": 1 } }]
        if 'error' in data[0]:
            return True

        return False


class LinkError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

from auth0_machine_to_machine import *

import http.client

class Auth0ManagementApi:
    def __init__(self, auth0: Auth0MachineToMachine):
        self.auth0 = auth0

    def getManagementApiJwt(self):
        conn = http.client.HTTPSConnection("")

        payload = "grant_type=" + self.auth0.grant_type     \
            + "&client_id=" + self.auth0.client_id          \
            + "&client_secret=" + self.auth0.client_secret  \
            + "&audience=" + self.auth0.audience
        print(payload)
        headers = { 'content-type': "application/x-www-form-urlencoded" }

        conn.request("POST", self.auth0.url, payload, headers)

        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))


class Auth0MachineToMachine():
    def __init__(self, url, audience, grant_type, client_id, client_secret):
        self.url = url
        self.grant_type = grant_type
        self.client_id = client_id
        self.client_secret = client_secret
        self.audience = audience

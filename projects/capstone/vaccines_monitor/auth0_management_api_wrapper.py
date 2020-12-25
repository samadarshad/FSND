from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0

class Auth0Error(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

class Auth0ManagementApiWrapper:
    def __init__(self, domain, non_interactive_client_secret, non_interactive_client_id):
        self.domain = domain
        self.non_interactive_client_secret = non_interactive_client_secret
        self.non_interactive_client_id = non_interactive_client_id
        self.mgmt_api_token = self._getManagementToken()
        self.auth0 = Auth0(self.domain, self.mgmt_api_token)

    def _getManagementToken(self):
        get_token = GetToken(self.domain)
        token = get_token.client_credentials(self.non_interactive_client_id,
            self.non_interactive_client_secret, 'https://{}/api/v2/'.format(self.domain))
        mgmt_api_token = token['access_token']
        return mgmt_api_token

    def createUser(self, email, password):
        ret = self.auth0.users.create({"email":email,"connection":"Username-Password-Authentication","password":password})
        return ret['user_id']

    def deleteUser(self, user_id):
        self.auth0.users.delete(user_id)

    def assignRoleToUser(self, user_id, role_id):
        self.auth0.users.add_roles(user_id, [role_id])
        # confirm the role has been added
        ret = self.auth0.users.list_roles(user_id)
        if ret['roles'][0]['id'] == role_id:
            print("success")
        else:
            print("failed to add!")

    def getUser(self, user_id):
        self.auth0.users.get(user_id)

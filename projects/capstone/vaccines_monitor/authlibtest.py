from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0

domain = 'abdus-samad-fsnd.eu.auth0.com'
non_interactive_client_id = 'hhDJ5T95Lytl5xMCM25AgeMp0AY8Vl7j'
non_interactive_client_secret = 'wXNXaM58Cs-ErbkUTfASEvMTSpkQwIMCzLrFSXtlR_0lUQFH_whrPVXgFYUmYE71'

get_token = GetToken(domain)
token = get_token.client_credentials(non_interactive_client_id,
    non_interactive_client_secret, 'https://{}/api/v2/'.format(domain))
mgmt_api_token = token['access_token']


auth0 = Auth0(domain, mgmt_api_token)
# ret = auth0.users.create({"email":"john.doe_using_python3@gmail.com","connection":"Username-Password-Authentication","password":"secret"})
# print(ret['user_id'])

#auth0.roles.add_users('rol_YSs1AgfNjAV5FHss', ['auth0|5fe4ebd1b2ac50006f71ca4b'])
# confirm the role has been added
# ret = auth0.users.list_roles('auth0|5fe4ebd1b2ac50006f71ca4b')
# check 'rol_YSs1AgfNjAV5FHss' is  ret['roles'][0]['id']s
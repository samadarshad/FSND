from auth0_management_api_wrapper import Auth0ManagementApiWrapper

import os
import config

patient_role_id = os.getenv('PATIENT_ROLE_ID')
domain = os.getenv('AUTH0_DOMAIN')
non_interactive_client_secret = os.getenv('NON_INTERACTIVE_CLIENT_SECRET')
non_interactive_client_id = os.getenv('NON_INTERACTIVE_CLIENT_ID')

auth0 = Auth0ManagementApiWrapper(domain, non_interactive_client_secret, non_interactive_client_id)

def createPatient(email, password):    
    user_id = auth0.createUser(email, password)
    auth0.assignRoleToUser(user_id, patient_role_id)
    
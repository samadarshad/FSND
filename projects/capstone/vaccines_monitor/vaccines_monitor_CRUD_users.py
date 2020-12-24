from auth0_machine_to_machine import *

VaccinesMonitorCrudUsers = Auth0MachineToMachine(
    url='https://abdus-samad-fsnd.eu.auth0.com/oauth/token',
    audience='https://abdus-samad-fsnd.eu.auth0.com/api/v2/',
    grant_type='client_credentials',
    client_id='hhDJ5T95Lytl5xMCM25AgeMp0AY8Vl7j',
    client_secret='wXNXaM58Cs-ErbkUTfASEvMTSpkQwIMCzLrFSXtlR_0lUQFH_whrPVXgFYUmYE71'
)




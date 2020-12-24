import os
from flask import Flask
from flask_cors import CORS
from models import setup_db

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': greeting = greeting + "!! !!!"
        return greeting

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    @app.route('/patients', methods=['POST'])
    @requires_auth('create:patient')
    def add_patient(jwt):
        
        '''
        0. 
        get patient username and password from json

        1.
        retrieve management token from Vaccines-monitor-CRUD-users 
        curl --request POST \
        --url 'https://abdus-samad-fsnd.eu.auth0.com/oauth/token' \
        --header 'content-type: application/x-www-form-urlencoded' \
        --data grant_type=client_credentials \
        --data 'client_id=hhDJ5T95Lytl5xMCM25AgeMp0AY8Vl7j' \
        --data client_secret=wXNXaM58Cs-ErbkUTfASEvMTSpkQwIMCzLrFSXtlR_0lUQFH_whrPVXgFYUmYE71 \
        --data 'audience=https://abdus-samad-fsnd.eu.auth0.com/api/v2/'

        there is a python version of this: https://auth0.com/docs/tokens/management-api-access-tokens/get-management-api-access-tokens-for-production 
        
        2.
        then create new patient using management token from above
        extract user_id

        3. 
        add role to patient using management token from above and user_id from above

        4. 
        add new row to our database: patient user_id (for verifying the patient can view/edit their own records), and all the other patient data i.e. 
        patient name/age/etc (for sake of ease, this could be done in a PATCH request later - however the user_id MUST NOT be editable)
        the patient username/password isnt needed to be stored in the database, because Auth0 stores it and gives us back the user_id in the JWT.
        the patient should be given their user/password to remember (just note this down in a text file)

        '''



    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

# Live Heroku Project URL
https://vaccines-monitor-samad-fsnd.herokuapp.com/

# Motivation
Udacity Full-stack Capstone Project for Vaccine testing centres
- A doctor can manage patients (including creating/deleting new users), and administer vaccines
- A patient can only view and edit their own data
- A researcher can only view test results, and manage vaccines
- An admin can do everything

# Dependencies
`pip install -r requirements.txt`

# Deployment to Localhost
`python app.py`

visit localhost:8080

# Deployment to Heroku
Push to master branch.

Heroku is setup to automatically pull in changes from master https://github.com/samadarshad/FSND and automatically deploy - so you dont need to run `(cd /media/sf_share/FSND && git subtree push --prefix projects/capstone/vaccines_monitor heroku master)`. You'd only need to run `run_migrations_on_heroku.sh` after any database migrations. You can also do `heroku run bash --app vaccines-monitor-samad-fsnd` for debugging.

# API Documentation & Testing
Visit https://documenter.getpostman.com/view/13819578/TVsxCSUo for documentation and tests.

If you want to run the tests, click "Run in Postman" in the top right corner. The collection contains all the needed login credentials for Auth0, so it will automatically obtain a new JWT token.
Note you will need to change the collection-variable `baseUrl` to be localhost:8080 if testing locally.

## Error handlers
Errors return JSON in the format:
```
{  
    [optional]code,  
    description  
}   HTTP status_code  
```

# Things needed to make this production-ready
- Syncing of the Auth0 users database and the postgres database. i.e. the app will fail to create patientX if patientX already exists in Auth0 database. The current workaround is to manually clear both databases to start the index X=1.
- Secrets are currently stored in the .env file. It should be stored as secret environment variables in Github.
- Usernames and passwords are currently stored in the Postman test collections suite to make testing easier (i.e. no need to manually generate a new JWT, the test suite automatically logs in and gets the JWT). There should be another secure way to automatically get JWTs. Alternatively, there could be separate Auth0 connection databases for development and production.
- All new Patients are created with a default password, transferred in a JSON body from this app to Auth0. This should be changed such that this app never has to deal with passwords.
- The Doctor has permissions to delete any Patient. However it would be better to restrict such that one doctor cannot delete the patients of another doctor.
- There is no CI/Automated testing. This should be a step in the CD for Heroku.
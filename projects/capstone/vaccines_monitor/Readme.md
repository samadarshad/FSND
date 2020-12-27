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
localhost:8080

# Deployment to Heroku
Push to master branch.
Heroku is setup to automatically pull in changes from master https://github.com/samadarshad/FSND and automatically deploy - so you dont need to run `(cd /media/sf_share/FSND && git subtree push --prefix projects/capstone/vaccines_monitor heroku master)`. You'd only need to run `run_migrations_on_heroku.sh` after any database migrations. You can also do `heroku run bash --app vaccines-monitor-samad-fsnd` for debugging.

# API Documentation & Testing
https://documenter.getpostman.com/view/13819578/TVsxCSUo 
If you want to run the tests, click "Run in Postman" in the top right corner. The collection contains all the needed login credentials for Auth0, so it will automatically obtain a new JWT token. In production, these login credentials shall be kept secret.
Note you will need to change the collection-variable `baseUrl` to be localhost:8080 if testing locally.


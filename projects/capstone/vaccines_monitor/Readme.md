# Deployment
Heroku is setup to automatically pull in changes from master https://github.com/samadarshad/FSND and automatically deploy - so you dont need to run `(cd /media/sf_share/FSND && git subtree push --prefix projects/capstone/vaccines_monitor heroku master)`. You'd only need to run `run_migrations_on_heroku.sh` after any database migrations. You can also do `heroku run bash` for debugging.
https://vaccines-monitor-samad-fsnd.herokuapp.com/

# Testing & API
Postman is automatically integrated with the git repo, so any changes will be reflected (you will need to pull/push).
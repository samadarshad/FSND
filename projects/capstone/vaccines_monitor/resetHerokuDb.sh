heroku pg:reset DATABASE_URL --confirm vaccines-monitor-samad-fsnd --app vaccines-monitor-samad-fsnd
heroku run flask db init --app vaccines-monitor-samad-fsnd
heroku run flask db upgrade --app vaccines-monitor-samad-fsnd
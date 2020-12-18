# Flask Recap

A simple flask server to demonstrate basic flask.

## Getting Started

### Create a Virutal Enviornment

Follow instructions [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) to create and activate virtual enviornment for this project.
 python -m virtualenv env --always-copy
 source env/bin/activate
### Install Dependencies

Run `pip install -r requirements.txt` to install any dependencies.

### Install Postman

Follow instructions on the [Postman docs](https://www.getpostman.com/) to install and run postman. Once postman is running, import the collection `./udacity-fsnd-flaskrecap.postman_collection.json`.

### Run the Server

On first run, execute `export FLASK_APP=FlaskRecap.py`. Then run `flask run --reload` to run the developer server.

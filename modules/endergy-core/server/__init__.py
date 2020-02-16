'''
This package contains the Flask REST Api for the Endergy Landing Page.
'''

from endergy_web import flask_setup

app = flask_setup.create_app(__name__)
db = flask_setup.create_db(app)
api = flask_setup.create_api(app)

# Ugly dependency, but since routes import controller classes
# the api and app objects needs to be available when importing routes
from . import routes
# Attach routes to the Flask-RESTful Resource objects found at controllers/*
routes.add_routes(api)

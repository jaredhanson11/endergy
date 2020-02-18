'''
This package contains the Flask REST Api for the Endergy Landing Page.
'''

from endergy_web import flask_setup
from endergy_rabbitmq import RMQConnection
from endergy_db import schema

app = flask_setup.create_app(__name__)
db = flask_setup.create_db(app)
# Aggressively configure Schema's on all db models
schema.configure()
api = flask_setup.create_api(app)
rmq_connection = RMQConnection(dict(app.config))

# Ugly dependency, but since routes import controller classes
# the api and app objects needs to be available when importing routes
from . import routes
# Attach routes to the Flask-RESTful Resource objects found at controllers/*
routes.add_routes(api)

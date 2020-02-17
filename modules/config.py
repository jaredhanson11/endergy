'''General config options'''
import os

# SQLALCHEMY
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

# RabbitMQ
RMQ_USER = os.environ.get('RMQ_USER')
RMQ_PASSWORD = os.environ.get('RMQ_PASSWORD')
RMQ_HOST = os.environ.get('RMQ_HOST')
RMQ_PORT = os.environ.get('RMQ_PORT')

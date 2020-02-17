'''
Handles setup of RabbitMQ connection via pika.

Setup of connections requires a config dict object with the following variables
set.
RMQ_USER, RMQ_PASSWORD, RMQ_HOST, RMQ_PORT
'''
import pika


class RMQConnection:
    '''
    Initialize this object with the proper config variables to be used
    throughout the lifecycle of the application.
    '''
    connection = None

    def __init__(self, config: dict):
        credentials = pika.PlainCredentials(
            config['RMQ_USER'], config['RMQ_PASSWORD'])
        parameters = pika.ConnectionParameters(
            host=config['RMQ_HOST'],
            port=config['RMQ_PORT'],
            credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)

    def get_connection(self) -> pika.SelectConnection:
        '''Returns BlockingConnection, when initialized properly'''
        if not self.connection:
            raise Exception('Connection object was not initialized properly.')
        return self.connection

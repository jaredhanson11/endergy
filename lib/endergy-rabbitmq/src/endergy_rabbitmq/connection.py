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
    config = None

    def __init__(self, config: dict, lazy=True):
        self.config = config
        if not lazy:
            self._connect()

    def _connect(self) -> None:
        '''Connects to RMQ instance'''
        credentials = pika.PlainCredentials(
            self.config['RMQ_USER'], self.config['RMQ_PASSWORD'])
        parameters = pika.ConnectionParameters(
            host=self.config['RMQ_HOST'],
            port=self.config['RMQ_PORT'],
            credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)

    def get_connection(self) -> pika.SelectConnection:
        '''Returns BlockingConnection, when initialized properly'''
        if not self.connection:
            self._connect()
        return self.connection

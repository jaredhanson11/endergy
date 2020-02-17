'''
RMQPublisher
'''
import pika


class RMQPublisher:
    '''Object that publishes messaged to a specific queue.'''
    channel = None
    queue = None

    def __init__(self, queue: str, connection: pika.SelectConnection):
        assert queue is not None and connection is not None
        self.channel = connection.channel()
        self.queue = queue

    def publish(self, message: str):
        '''Publish message to pre-configured queue'''
        if not self.channel or not self.queue:
            raise Exception('Publisher hasn\'t been properly initialized')
        self.channel.basic_publish('', self.queue, message)

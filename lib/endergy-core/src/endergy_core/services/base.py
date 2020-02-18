'''Common functionality for all services'''


class BaseService:
    '''BaseService for all service classes to extend'''
    db = None  # sqlalchemy db object, gets current session for queries
    rmq_connection = None  # rabbitmq connection for rmq interactions

    def __init__(self, db=None, rmq_connection=None):
        self.db = db
        self.rmq_connection = rmq_connection
        self._post_init()
    
    def _post_init(self):
        '''Implement for custom init behavior in inherited classes'''

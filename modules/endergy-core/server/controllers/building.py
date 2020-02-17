'''
Controllers interfacing with building objects.
'''
from flask_restful import Resource

from endergy_web import responses
from endergy_db.common import Building

from .. import db


class BuildingListController(Resource):
    '''API for list of building records'''

    def get(self):
        '''Get all buildings.'''
        buildings = db.session.query(Building).all()
        ret = [dict(b) for b in buildings]
        return responses.success(ret)

    def post(self):
        '''Post new building.'''
        return responses.server_error('This endpoint has not been implemented')


class BuildingController(Resource):
    '''API for individual building record'''

    def get(self, id):
        '''Get building.'''
        return responses.server_error('This endpoint has not been implemented')

    def put(self, id):
        '''Edit building.'''
        return responses.server_error('This endpoint has not been implemented')

    def delete(self, id):
        '''Delete building.'''
        return responses.server_error('This endpoint has not been implemented')

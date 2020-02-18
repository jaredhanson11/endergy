'''
Controllers interfacing with building objects.
'''
from flask import request
from flask_restful import Resource

from endergy_core.services import BuildingService
from endergy_web import responses

from .. import db, rmq_connection

# building.py globals (both Building & BuildingList use)
building_service: BuildingService = BuildingService(
        db=db, rmq_connection=rmq_connection.get_connection())


class BuildingListController(Resource):
    '''API for list of building records'''

    def get(self):
        '''Get all buildings.'''
        buildings = building_service.get_building_list()
        return responses.success(buildings)

    def post(self):
        '''Post new building.'''
        post_body = request.get_json()
        building = building_service.add_building(post_body)
        return responses.success(building)


class BuildingController(Resource):
    '''API for individual building record'''

    def get(self, id):
        '''Get building.'''
        building = building_service.get_building(id)
        if building:
            return responses.success(building)
        return responses.client_error('Building does not exist')

    def put(self, id):
        '''Edit building.'''
        return responses.server_error('This endpoint has not been implemented')

    def delete(self, id):
        '''Delete building.'''
        return responses.server_error('This endpoint has not been implemented')

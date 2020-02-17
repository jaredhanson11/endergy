'''
Controllers interfacing with building objects.
'''
from flask import request
from flask_restful import Resource

from endergy_web import responses
from endergy_db.common import Building
from endergy_rabbitmq import publish, queue

from .. import db, rmq_connection

# global within building.py since both Building & BuildingList controllers use
building_geom_publisher = publish.RMQPublisher(
    queue.NEW_BUILDING_GEOM, rmq_connection)


class BuildingListController(Resource):
    '''API for list of building records'''

    def get(self):
        '''Get all buildings.'''
        buildings = db.session.query(Building).all()
        ret = [{'name': b.name, 'id': b.id} for b in buildings]
        return responses.success(ret)

    def post(self):
        '''Post new building.'''
        post_body = request.get_json()
        building = Building()
        building.name = post_body.get('name')
        building.description = post_body.get('description')
        building.latitude = post_body.get('latitude')
        building.longitude = post_body.get('longitude')
        db.session.add(building)
        db.session.commit()
        ret = {'id': building.id}
        building_geom_publisher.publish_json(ret)
        return responses.success(ret)


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

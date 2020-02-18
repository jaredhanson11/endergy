'''Services performing building related tasks'''
from typing import Optional, List

from endergy_db.common import Building
from endergy_rabbitmq import publish, queue

from .base import BaseService


class BuildingService(BaseService):
    '''Service performing building related tasks'''
    new_building_publisher: publish.RMQPublisher

    def _post_init(self):
        '''Setup rmq publishers.'''
        self.new_building_publisher = publish.RMQPublisher(
            queue.NEW_BUILDING_GEOM, self.rmq_connection)

    def get_building_list(self) -> List[dict]:
        '''
        Gets all buildings.
        Returns:
            buildings (List[dict]): list of building objects
        '''
        buildings = self.db.session.query(Building).all()
        return Building.__marshmallow__(many=True).dump(buildings)

    def get_building(self, id) -> Optional[dict]:
        '''
        Gets building by id.
        Returns:
            building (dict): building data, if building exists
            None, if building doesn't exist
        '''
        building = self.db.session.query(Building).get(id)
        if building:
            return Building.__marshmallow__().dump(building)
        return None

    def add_building(self, request_data) -> dict:
        '''
        Add new building to buildings database, and publish message to new
            building rmq queue.
        Returns:
            building (dict): building data of newly added building
        '''
        building = Building.__marshmallow__().load(
            request_data, session=self.db.session)
        self.db.session.add(building)
        self.db.session.flush()
        building_data = Building.__marshmallow__().dump(building)
        self.new_building_publisher.publish_json(building_data)
        self.db.session.commit()
        return building_data

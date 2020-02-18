'''Services performing building related tasks'''
from typing import Optional, List

from endergy_db.common import Building
from endergy_rabbitmq import publish, queue

from .base import BaseService


class BuildingService(BaseService):
    '''Service performing building related tasks'''
    new_building_publisher: publish.RMQPublisher
    updated_building_publisher: publish.RMQPublisher

    def _post_init(self):
        '''Setup rmq publishers.'''
        self.new_building_publisher = publish.RMQPublisher(
            queue.NEW_BUILDING, self.rmq_connection)
        self.updated_building_publisher = publish.RMQPublisher(
            queue.UPDATED_BUILDING, self.rmq_connection)

    def get_building_list(self) -> List[dict]:
        '''
        Gets all buildings.
        Returns:
            buildings (List[dict]): list of building objects
        '''
        buildings = self.db.session.query(Building).all()
        return Building.__schema__(many=True).dump(buildings)

    def get_building(self, id: int) -> Optional[dict]:
        '''
        Gets building by id.
        Returns:
            building (dict): building data, if building exists
            None, if building doesn't exist
        '''
        building = self.db.session.query(Building).get(id)
        if building:
            return Building.__schema__().dump(building)
        return None

    def add_building(self, request_data: dict) -> dict:
        '''
        Add new building to buildings database, and publish message to new
            building rmq queue.
        Returns:
            building (dict): building data of newly added building
        '''
        building = Building.__schema__().load(
            request_data, session=self.db.session)
        self.db.session.add(building)
        self.db.session.flush()
        building_data = Building.__schema__().dump(building)
        self.new_building_publisher.publish_json(building_data)
        self.db.session.commit()
        return building_data

    def edit_building(self, id: int, request_data: dict) -> Optional[dict]:
        '''
        Edits existing record adding new fields.
        Returns:
            buliding (dict): updated building data
            None: if building doesn't exists or field isn't updateable
        '''
        update_fields = Building.__schema__().dump(request_data)
        # Check if any fields are not able to be updated
        NON_UPADATEABLE = ['id', 'created_at']
        for key in list(update_fields.keys()):
            if key in NON_UPADATEABLE: return None
        existing_building = self.db.session.query(Building).get(id)
        if existing_building:
            existing_fields = Building.__schema__().dump(existing_building)
            building_fields = {**existing_fields, **update_fields}
            if building_fields == existing_fields:
                # Building fields nots changed (don't publish to rmq queue)
                return building_fields
            updated_building = Building.__schema__().load(
                building_fields, session=self.db.session)
            self.db.session.add(updated_building)
            self.db.session.flush()
            building_data = Building.__schema__().dump(updated_building)
            self.updated_building_publisher.publish_json(building_data)
            self.db.session.commit()
            return building_data
        return None

        def delete_building(self, id) -> bool:
            '''
            Delete building record from database.

            Unimplemented right now because it will consist of deleting much
            more records than just in the building table. Foreign keys
            referencing this building record
            '''
            pass

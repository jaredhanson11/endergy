'''
Common Endergy related tables that will be used across all modules.
'''
from datetime import datetime

from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from . import base


class Building(base.Base, base.EndergyCommonBaseModel):
    '''
    Building stores general information related to a building.
    '''
    __tablename__ = 'building'
    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False)  # descriptive name of building
    description = Column(String(1000))  # freeform text with info on building
    created_at = Column(DateTime, default=datetime.utcnow)
    latitude = Column(Numeric(precision=12, scale=6))
    longitude = Column(Numeric(precision=12, scale=6))

    geometry_id = Column(String(200))  # id of geom file in object store

    typology_id = Column(Integer, ForeignKey(
        base.foreign_key('id', 'typology', 'surrogate')))
    typology = relationship('Typology', back_populates='buildings')

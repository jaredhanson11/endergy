'''
Database models related to the creation of the surrogate model.
'''
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from . import base


class Typology(base.Base, base.EndergySurrogateBaseModel):
    '''
    Typology represents a class of buildings with similiar geometry.
    '''
    __tablename__ = 'typology'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    buildings = relationship('Building', back_populates='typology')
    samples = relationship('SurrogateSample', back_populates='typology')


class SurrogateSample(base.Base, base.EndergySurrogateBaseModel):
    '''
    SurrogateSample mapping of typology to energyplus sample set
    Also is correlated to a typology.
    '''
    __tablename__ = 'surrogate_sample'
    id = Column(Integer, primary_key=True)

    typology_id = Column(Integer, ForeignKey(
        base.foreign_key('id', 'typology', 'surrogate')))
    typology = relationship('Typology', back_populates='samples')

    energyplus_values_id = Column(Integer, ForeignKey(
        base.foreign_key('id', 'energyplus_value_set', 'common')))
    energyplus_values = relationship('EnergyplusValueSet')

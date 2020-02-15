'''
Common Endergy related tables that will be used across all modules.
'''
import enum
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, \
    CheckConstraint, Table
from sqlalchemy.orm import relationship

from . import base


class Building(base.Base, base.EndergyCommonBaseModel):
    '''
    Building stores general information related to a building.
    '''
    __tablename__ = 'building'
    id = Column(Integer, primary_key=True)

    description = Column(String(1000))  # freeform text with info on building
    latitude = Column(Numeric(precision=12, scale=6))
    longitude = Column(Numeric(precision=12, scale=6))

    typology_id = Column(Integer, ForeignKey(
        base.foreign_key('id', 'typology', 'surrogate')))
    typology = relationship('Typology', back_populates='buildings')


class EnergyplusParameter(base.Base, base.EndergyCommonBaseModel):
    ''' Represents named parameter and possible values for that parameter'''
    __tablename__ = 'energyplus_parameter'

    id = Column(Integer, primary_key=True)
    key = Column(String(50), unique=True, nullable=False)
    name = Column(String(50))
    possible_values = relationship('EnergyplusValue',
                                   back_populates='parameter')


class EnergyplusValue(base.Base, base.EndergyCommonBaseModel):
    '''
    Represents value for an energyplus parameter
        (plus value type LOW, MID, HIGH)
    '''
    __tablename__ = 'energyplus_value'
    id = Column(Integer, primary_key=True)

    value = Column(String(100), nullable=False)
    type = Column(String(10),
                  CheckConstraint("type IN ('LOW','MEDIUM','HIGH')"),
                  nullable=False)
    parameter_id = Column(Integer, ForeignKey(
        base.foreign_key('id', 'energyplus_parameter', 'common')),
        nullable=False)
    parameter = relationship('EnergyplusParameter',
                             back_populates='possible_values')


# Table for many to many relationship of values and values set
value_set_association = Table(
    'energyplus_value_to_value_set', base.Base.metadata,
    Column('value_id', Integer, ForeignKey(
        base.foreign_key('id', 'energyplus_value', 'common'))),
    Column('value_set_id', Integer, ForeignKey(
        base.foreign_key('id', 'energyplus_value_set', 'common'))),
    schema=base.schemas['common']
)


class EnergyplusValueSet(base.Base, base.EndergyCommonBaseModel):
    '''
    ValueSet is a a list of values that represents a final endergy plust
        model (IDF). Basically EnergyplusValueSet + idf template = final IDF to 
        be run by EnergyPlus.
    '''
    __tablename__ = 'energyplus_value_set'
    id = Column(Integer, primary_key=True)
    values = relationship('EnergyplusValue', secondary=value_set_association)

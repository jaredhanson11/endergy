'''
EnergyPlus related tables.
'''
from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, \
    CheckConstraint, Table, DateTime
from sqlalchemy.orm import relationship

from . import base


class EPW(base.Base, base.EnergyplusBaseModel):
    '''Represents EPW file stored in object store'''
    __tablename__ = 'epw'
    id = Column(Integer, primary_key=True)

    name = Column(String(50))
    city = Column(String(100))
    state = Column(String(50))
    country = Column(String(50))
    postal = Column(String(20))
    latitude = Column(Numeric(precision=12, scale=6))
    longitude = Column(Numeric(precision=12, scale=6))
    created_at = Column(DateTime, default=datetime.utcnow)


class IDF(base.Base, base.EnergyplusBaseModel):
    '''Represents IDF template stored in object store'''
    __tablename__ = 'idf'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)


class EnergyplusParameter(base.Base, base.EnergyplusBaseModel):
    '''Represents named parameter and possible values for that parameter'''
    __tablename__ = 'energyplus_parameter'

    id = Column(Integer, primary_key=True)
    key = Column(String(50), unique=True, nullable=False)
    name = Column(String(50))
    possible_values = relationship('EnergyplusValue',
                                   back_populates='parameter')


class EnergyplusValue(base.Base, base.EnergyplusBaseModel):
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
        base.foreign_key('id', 'energyplus_parameter', 'energyplus')),
        nullable=False)
    parameter = relationship('EnergyplusParameter',
                             back_populates='possible_values')


# Table for many to many relationship of values and values set
value_set_association = Table(
    'energyplus_value_to_value_set', base.Base.metadata,
    Column('value_id', Integer, ForeignKey(
        base.foreign_key('id', 'energyplus_value', 'energyplus'))),
    Column('value_set_id', Integer, ForeignKey(
        base.foreign_key('id', 'energyplus_value_set', 'energyplus'))),
    schema=base.schemas['energyplus']
)


class EnergyplusValueSet(base.Base, base.EnergyplusBaseModel):
    '''
    ValueSet is a a list of values that represents a final endergy plust
        model (IDF). Basically EnergyplusValueSet + idf template = final IDF to 
        be run by EnergyPlus.
    '''
    __tablename__ = 'energyplus_value_set'
    id = Column(Integer, primary_key=True)
    values = relationship('EnergyplusValue', secondary=value_set_association)


class EnergyplusRun(base.Base, base.EnergyplusBaseModel):
    '''
    Represents a completed energyplus run.
    Components of a Eplus run are
    inputs:
        idf_template, value_set, epw_file
    & outputs:
        elec, stm, chw

    '''
    __tablename__ = 'energyplus_run'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    idf_id = Column(Integer, ForeignKey(
        base.foreign_key('id', 'idf', 'energyplus')),
        nullable=False)
    epw_id = Column(Integer, ForeignKey(
        base.foreign_key('id', 'epw', 'energyplus')),
        nullable=False)
    value_set_id = Column(Integer, ForeignKey(
        base.foreign_key('id', 'energyplus_value_set', 'energyplus')),
        nullable=False)

    idf = relationship('IDF')
    epw = relationship('EPW')
    results = relationship('EnergyplusRunResults', back_populates='eplus_run')


class EnergyplusRunResults(base.Base, base.EnergyplusBaseModel):
    '''
    Results of an energyplus run.
    stm + unit of measure
    chw + unit of measure
    elec + unit of measure
    '''
    __tablename__ = 'energyplus_run_results'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    elec = Column(Integer)
    elec_units = Column(String(20))
    stm = Column(Integer)
    stm_units = Column(String(20))
    chw = Column(Integer)
    chw_units = Column(String(20))

    eplus_run_id = Column(Integer, ForeignKey(
        base.foreign_key('id', 'energyplus_run', 'energyplus')),
        nullable=False)
    eplus_run = relationship('EnergyplusRun', back_populates='results')

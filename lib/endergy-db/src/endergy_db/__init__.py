'''
Module containing database models which are SQLAlchemy objects.
'''
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class EndergySurrogateBaseModel:
    '''
    Models related to the EndergySurrogate creation inherite this class.
    Scopes these tables to the 'endergy_surrogate' schema.
    '''
    __table_args__ = {'schema': 'endergy_surrogate'}

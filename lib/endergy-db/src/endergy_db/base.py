'''
Contians all base models and the Base object for all models to inherit.
'''
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
schemas = {
    'common': 'endergy_common',
    'surrogate': 'endergy_surrogate',
    'energyplus': 'endergy_energyplus'
}


def table(_table: str, schema=None) -> str:
    '''Return schema.table or table if schema is null.'''
    if schema:
        return '{}.{}'.format(schemas[schema], _table)
    return _table


def foreign_key(column: str, _table: str, schema=None) -> str:
    '''
    Returns 'schema.table.column' or 'table.column'
    Input:
    schema, should a key in the schemas mapping i.e. common -> endergy_common
    table, table name
    column, column name (typicaly 'id')
    '''
    table_name = table(_table, schema)
    return '{}.{}'.format(table_name, column)


class EndergyCommonBaseModel:
    '''
    Models related to the EndergySurrogate creation inherite this class.
    Scopes these tables to the 'endergy_surrogate' schema.
    '''
    __table_args__ = {'schema': schemas['common']}


class EndergySurrogateBaseModel:
    '''
    Models related to the EndergySurrogate creation inherite this class.
    Scopes these tables to the 'endergy_surrogate' schema.
    '''
    __table_args__ = {'schema': schemas['surrogate']}


class EnergyplusBaseModel:
    '''
    Models related to the Energyplus.
    Scopes these tables to the 'endergy_energyplus' schema.
    '''
    __table_args__ = {'schema': schemas['energyplus']}

'''Marshmallow sqlalchemy work'''
from sqlalchemy import event
from sqlalchemy.orm import mapper, configure_mappers
from marshmallow_sqlalchemy import ModelConversionError, SQLAlchemyAutoSchema

from . import base


def configure():
    '''
    Use this method to aggressively configure_mappers, default behavior is this
    method is called on first Model usage. This is an issue because
    Model.__schema__, isn't availabe until a model is used once.
    It errors when we want to use Model.__schema__ to load a db record.
    '''
    configure_mappers()


def setup_schema(Base):
    '''
    https://marshmallow-sqlalchemy.readthedocs.io/en/latest/recipes.html#automatically-generating-schemas-for-sqlalchemy-models
    '''
    # Create a function which incorporates the Base and session information
    def setup_schema_fn():
        for class_ in Base._decl_class_registry.values():
            if hasattr(class_, "__tablename__"):
                if class_.__name__.endswith("Schema"):
                    raise ModelConversionError(
                        "For safety, setup_schema can not be used when a"
                        "Model class ends with 'Schema'"
                    )

                class Meta(object):
                    model = class_
                    load_instance = True
                    include_fk = True

                schema_class_name = "%sSchema" % class_.__name__

                schema_class = type(
                    schema_class_name, (SQLAlchemyAutoSchema,), {"Meta": Meta}
                )

                setattr(class_, "__schema__", schema_class)

    return setup_schema_fn


event.listen(mapper, "after_configured", setup_schema(base.Base))

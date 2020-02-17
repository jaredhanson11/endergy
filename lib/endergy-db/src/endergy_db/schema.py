'''Marshmallow sqlalchemy work'''
from sqlalchemy import event
from sqlalchemy.orm import mapper
from marshmallow_sqlalchemy import ModelConversionError, SQLAlchemyAutoSchema

from . import base


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

                schema_class_name = "%sSchema" % class_.__name__

                schema_class = type(
                    schema_class_name, (SQLAlchemyAutoSchema,), {"Meta": Meta}
                )

                setattr(class_, "__marshmallow__", schema_class)

    return setup_schema_fn


event.listen(mapper, "after_configured", setup_schema(base.Base))

import zope.interface
from z3c.form import validator
import zope.component
from sqlalchemy import create_engine
from plomino.replication.connection import connection
class validateConn(validator.SimpleFieldValidator):
    def validate(self,value):
        try:
            engine = create_engine(value)
        except:
            msg = u"Invalid connection string"
            raise zope.interface.Invalid(msg)

validator.WidgetValidatorDiscriminators(validateConn, field=connection[conn_string'])

# Register the validator so it will be looked up by z3c.form machinery

zope.component.provideAdapter(validateConn)

import zope.interface
from z3c.form import validator
import zope.component
from sqlalchemy import create_engine

class validateConn(validator.SimpleFieldValidator):
    def validate(self,value):
        try:
            engine = create_engine(value)
        except:
            msg = u"Invalid connection string"
            raise zope.interface.Invalid(msg)



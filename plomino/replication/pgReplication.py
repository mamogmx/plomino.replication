from zope.interface import Interface
from zope.interface import Attribute
from zope.interface import implements


from zope import schema

import sqlalchemy as sql
import sqlalchemy.orm as orm

from copy import deepcopy
import simplejson as json
import DateTime

from Products.CMFPlomino import PlominoDocument,PlominoForm

from AccessControl.SecurityManagement import newSecurityManager



class plominoData(object):
    def __init__(self, id, form, owner, data):
        self.id = id
        self.form = form
        self.owner = owner
        self.data = data
        
class pgReplication(object):
    conn_string = "postgresql://postgres:postgres@192.168.1.133:5433/sitar"
    db_schema = "istanze"
    db_table = "test"
    plominoDoc = None
    
    def __init__(self):
        implements(IdbReplication)
        
    def __new__(doc):
        self.plominoDoc = doc
        
    def getPlominoValues(self):
        return dict(deepcopy(self.plominoDoc.items))
    
    def saveData(self,data):
        
        db = sql.create_engine(self.conn_string)
        metadata = sql.schema.MetaData(bind=db,reflect=True,schema=self.db_schema)
        table = sql.Table(self.db_table, metadata, autoload=True)
        
        rowmapper = orm.mapper(plominoData,table)
        Sess = orm.sessionmaker(bind = db)
        
        data = self.getPlominoValues()
        data = json.loads(json.dumps(data, default=DateTime.DateTime.ISO,use_decimal=True ))
        data['id'] = doc.getId()
        data['form'] = doc.getForm().getFormName()
        data['owner'] = doc.getItem('owner','')
        
        row = plominoData(data['id'],data['form'],data['owner'],data) 
        id = data['id']
        session = Sess()
        session.query(plominoData).filter_by(id=row.id).delete()
        session.commit()
        session.add(row)
        session.commit()        
import sqlalchemy as sql
import sqlalchemy.orm as orm

from copy import deepcopy
import simplejson as json
import DateTime
import datetime

from plone import api
from Products.CMFCore.utils import getToolByName


def getConnection(db):
    
    id = db.id
    catalog = getToolByName(db, 'portal_catalog')
    for brain in catalog(portal_type='connection'):
        br = brain.getObject()
        if id in br.plominodb:
            return dict(conn_string=br.conn_string, db_schema=br.db_schema, db_table=br.db_table)
    return dict()
    
def getIolRoles(doc):
    result = dict(
        iol_owner = [],
        iol_viewer = [],
        iol_reviewer = [],
        iol_manager = [],
    )
    for usr,roles in doc.get_local_roles():
        if 'Owner' in roles:
            result['iol_owner'].append(usr)
        if 'iol-viewer' in roles:
            result['iol_viewer'].append(usr)
        if 'iol-reviewer' in roles:
            result['iol_reviewer'].append(usr)
        if 'iol-manager' in roles:
            result['iol_manager'].append(usr)
    return result

class plominoData(object):
    def __init__(self, id, plominodb, form, url, review_state, review_history,iol_owner,iol_viewer,iol_reviewer,iol_manager, path, last_mod,data):
        self.id = id
        self.plominoform = form
        self.plominodb = plominodb
        self.review_state = review_state
        self.review_history = review_history
        self.url = url
        self.iol_owner = iol_owner
        self.iol_viewer = iol_viewer
        self.iol_reviewer = iol_reviewer
        self.iol_manager = iol_manager
        self.data = data
        self.path = path
        self.last_modified = last_mod
        

def serialDatagridItem(doc, obj ):
    result = list()
    itemvalue = doc.getItem(obj['name'])
    for el in itemvalue:
        i = 0
        res = dict()
        for fld in obj['field_list']:
            res[fld]= el[i]
            i+=1
        result.append(res)
    return result
    
def getPlominoValues(doc):
    results = dict(deepcopy(doc.items))
    frm = doc.getForm()
    fieldnames = []
    for i in frm.getFormFields(includesubforms=True, doc=None, applyhidewhen=False):
        if i.getFieldType()=='DATAGRID':
            fieldnames.append(dict(field=i,name=i.getId(),form=i.getSettings().associated_form,field_list=i.getSettings().field_mapping.split(',')))
    try:
        for f in fieldnames:
            if f['name'] in results:
                del results[f['name']]
            results[f['name']]=serialDatagridItem(doc,f)
    except:
        results[f['name']]= []
        api.portal.show_message(message='Errore nel campo %s' %f['name'], request=doc.REQUEST)
    return results 

def saveData(doc,events):
    #getting database configuration
    param_name = 'db_%s' %doc.getParentDatabase().id
    conf = getConnection(doc.getParentDatabase())
    if not conf:
        api.portal.show_message(message='Replication not configured', request=doc.REQUEST)
        return -1
       
    #istantiation of SQLAlquemy object
    try:
        db = sql.create_engine(conf['conn_string'])
        metadata = sql.schema.MetaData(bind=db,reflect=True,schema=conf['db_schema'])
        table = sql.Table(conf['db_table'], metadata, autoload=True)
        orm.clear_mappers() 
        rowmapper = orm.mapper(plominoData,table)
    except Exception as e:
        api.portal.show_message(message=u'Si sono verificati errori nella connessione al database : %s' %str(e), request=doc.REQUEST )
        return -1
    #creating session
    Sess = orm.sessionmaker(bind = db)
    session = Sess()

    
    #getting data from plominoDocument
    try:
        serialData = getPlominoValues(doc)
        d = json.loads(json.dumps(serialData, default=DateTime.DateTime.ISO,use_decimal=True ))
    except Exception as e:
        api.portal.show_message(message='Si sono verificati errori nella serializzazione del documento %s' %str(e), request=doc.REQUEST)
        d = dict()
    
    #initialize object plominoData
    wf = api.portal.get_tool(name='portal_workflow')
    id = doc.getId()
    roles = getIolRoles(doc)
    d['id'] = id
    data = dict(
        id = id,
        plominoform = doc.getForm().getFormName(),
        plominodb = doc.getParentDatabase().id,
        url = doc.absolute_url(),
        review_state = api.content.get_state(obj=doc),
        review_history = list(), #json.loads(json.dumps(wf.getInfoFor(doc,'review_history'), default=DateTime.DateTime.ISO,use_decimal=True )),
        iol_owner = roles['iol_owner'],
        iol_viewer = roles['iol_viewer'],
        iol_reviewer = roles['iol_reviewer'],
        iol_manager = roles['iol_manager'],
        path = doc.getPhysicalPath()[1:],
        last_modified = datetime.datetime.now(),
        data = d,
    )
    try:    
        row = plominoData(data['id'],data['plominodb'],data['plominoform'],data["url"], data["review_state"], data["review_history"],data['iol_owner'],data['iol_viewer'],data['iol_reviewer'],data['iol_manager'],data['path'],data['last_modified'],d)
        session = Sess()
        #deleting row from database
        session.query(plominoData).filter_by(id=id).delete()
        session.commit()
        #adding row to database
        session.add(row)
        session.commit()
        session.close()
        db.dispose()
    except Exception as e:
        api.portal.show_message(message=u'Si sono verificati errore nel salvataggio su database %s' %str(e), request=doc.REQUEST )
        db.dispose()
        return -1
    return 1
    
    
def delData(doc,events):
    #getting database configuration
    param_name = 'db_%s' %doc.getParentDatabase().id
    conf = getConnection(doc.getParentDatabase())
    if not conf:
        api.portal.show_message(message='Replication not configured', request=doc.REQUEST)
        return -1
    #istantiation of SQLAlquemy object
    try:
        db = sql.create_engine(conf['conn_string'])
        metadata = sql.schema.MetaData(bind=db,reflect=True,schema=conf['db_schema'])
        table = sql.Table(conf['db_table'], metadata, autoload=True)
        orm.clear_mappers() 
        rowmapper = orm.mapper(plominoData,table)
    except:
        api.portal.show_message(message=u'Si sono verificati errori nella connessione al database', request=doc.REQUEST )
        db.dispose()
        return -1
    #creating session
    Sess = orm.sessionmaker(bind = db)
    session = Sess()
    #deleting row from database
    docid = doc.getId()
    session.query(plominoData).filter_by(id=docid).delete()
    session.commit()
    session.close()
    db.dispose()

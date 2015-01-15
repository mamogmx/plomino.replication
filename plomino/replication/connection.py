from five import grok
from plone.dexterity.content import Item
from plone import api
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.dialects import postgresql

class connection(Item):
    """
    """

def createTable(connection,engine):

    metadata = MetaData()

    plominoTable = Table(connection.db_table,metadata,
        Column('id', String, primary_key=True),
        Column('plominodb', String),
        Column('plominoform', String),
        Column('url', String),
        Column('path', postgresql.ARRAY(String), primary_key=True),
        Column('review_state', String),
        Column('review_history', postgresql.JSON),
        Column('iol_owner', postgresql.ARRAY(String)),
        Column('iol_viewer', postgresql.ARRAY(String)),
        Column('iol_reviewer', postgresql.ARRAY(String)),
        Column('iol_manager', postgresql.ARRAY(String)),
        Column('last_modified', String),
        Column('data', postgresql.JSON),
        schema= connection.db_schema
    )
    plominoTable.create(engine)

@grok.subscribe(connection, IObjectAddedEvent)
def moveObj(connection, event):
    engine = create_engine(connection.conn_string)
    query = "SELECT count(*) as found FROM information_schema.tables WHERE table_schema='%s' AND table_name='%s'" % (connection.db_schema,connection.db_table)
    for r in engine.execute(query):
        found = r['found']

    if not found:
        createTable(connection,engine)
    site = api.portal.get()
    api.content.move(
        source=connection,
        target=site['replication_connections'],
        safe_id=True)


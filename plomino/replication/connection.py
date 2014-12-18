from five import grok
from plone.dexterity.content import Item
from plone import api
from interfaces import IColumn
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName

class connection(Item):
    #grok.implements(IColumn)
    #security = ClassSecurityInfo()


@grok.subscribe(connection, IObjectAddedEvent)
def moveObj(connection, event):
    site = api.portal.get()
    api.content.move(
        source=connection,
        target=site['db_connections'],
        safe_id=True)

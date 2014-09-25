from zope.i18nmessageid import MessageFactory

# Set up the i18n message factory for our package
MessageFactory = MessageFactory('plomino.replication')

from zope.component import getGlobalSiteManager
from z3c.baseregistry.baseregistry import BaseComponents
packageComponents = BaseComponents(getGlobalSiteManager(), 'PGReplication.PGReplication')
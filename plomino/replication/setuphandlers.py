from plone.app.controlpanel.security import ISecuritySchema
from plone import api
from Products.CMFCore.CMFBTreeFolder import manage_addCMFBTreeFolder

import logging

PROFILE_ID = 'profile-plomino.replication:default'
logger = logging.getLogger('plomino.replication')

def initPackage(context):
    site = api.portal.get()
    manage_addCMFBTreeFolder(site, id='db_connections',title='Database Connections for Plomino Replication')
    
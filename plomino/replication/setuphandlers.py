from plone.app.controlpanel.security import ISecuritySchema
from plone import api
from OFS.Folder import manage_addFolder

import logging

PROFILE_ID = 'profile-plomino.replication:default'
logger = logging.getLogger('plomino.replication')

def initPackage(context):
    site = api.portal.get()
    if not 'replication_connections' in site.keys():
        #api.content.create(
        #    container=site,
        #    id='replication_connections',
        #    title='Database Connections for Plomino Replication',
        #    type='Folder',
        #)
        manage_addFolder(
            site,
            id='replication_connections',
            title='Database Connections for Plomino Replication',
        )
    
from plone.app.controlpanel.security import ISecuritySchema
from plone import api


import logging

PROFILE_ID = 'profile-plomino.replication:default'
logger = logging.getLogger('plomino.replication')

def installation(context):
    site = api.portal.get()
    
    
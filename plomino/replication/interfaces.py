import re
from Acquisition import aq_base
from zope.interface import Interface, Attribute, Invalid
from zope.publisher.interfaces.browser import IBrowserPage
from zope import schema
from z3c.form import validator
from plomino.replication import MessageFactory as _
from Products.CMFCore.utils import getToolByName
from plone.directives import dexterity, form


class IConnectionSettings(form.Schema):
    """ Define the fields for the content type add form
    """
    form.model("models/connection.xml")

class IConnectionLayer(Interface):
    """Marker interface for the Browserlayer
    """
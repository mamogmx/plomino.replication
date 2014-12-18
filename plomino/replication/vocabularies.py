from five import grok
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName

class listPlominoDB(object):
    grok.implements(IContextSourceBinder)
    def __call__(self,context):
        catalog = getToolByName(context, 'portal_catalog')
        terms = list()
        for br in catalog(portal_type='PlominoDatabase'):
            db = br.getObject()
            terms.append(SimpleVocabulary.createTerm(db.id, db.id ,db.title or  db.id))
        
        return SimpleVocabulary(terms)

plominodb_list = listPlominoDB()

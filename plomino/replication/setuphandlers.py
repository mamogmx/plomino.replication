from zope.component import getSiteManager
from interfaces import IdbReplication

def install_base_registry(site):
    sm = getSiteManager(context=site)
    reg = sm.getUtility(IdbReplication, name=u'PGReplication')
    sm.__bases__ = tuple([reg] + [r for r in sm.__bases__ if r is not reg])
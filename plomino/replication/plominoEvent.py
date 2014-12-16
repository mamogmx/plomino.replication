from five import grok
from zope.component.interfaces import IObjectEvent
from zope.component.interfaces import ObjectEvent

class IPlominoSaveEvent(IObjectEvent):
    pass

class PlominoSaveEvent(ObjectEvent):
    grok.implements(IPlominoSaveEvent)

    def __init__(self,obj):
        self.object = obj
        

        
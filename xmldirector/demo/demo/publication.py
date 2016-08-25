# -*- coding: utf-8 -*-

################################################################
# xmldirector.plonecore
# (C) 2014,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################

"""
Publication
"""


import plone.api
from zope.interface import implements
from zope.schema import Choice
from zope.schema import List
from plone.dexterity.content import Item
from plone.supermodel import model
from zope.interface import directlyProvides
from zope.schema.interfaces import IContextSourceBinder

from zope.schema.vocabulary import SimpleVocabulary

from xmldirector.plonecore.i18n import MessageFactory as _



def possibleConnectors(context):
    
    catalog = plone.api.portal.get_tool('portal_catalog')
    terms = []
    for brain in catalog(portal_type='xmldirector.plonecore.connector'):
        terms.append(SimpleVocabulary.createTerm(brain.UID, brain.UID, brain.Title))
    return SimpleVocabulary(terms)
directlyProvides(possibleConnectors, IContextSourceBinder)


class IPublication(model.Schema):

#    connectors = RelationList(
#        title=u"Connectors",
#        default=[],
#        value_type=RelationChoice(title=_(u"Connectors"),
#                                  source=ObjPathSourceBinder()),
#        required=True,
#    )

    connectors = List(
        title=u"Connectors",
        default=[],
        value_type=Choice(title=u'Connector', source=possibleConnectors),
        required=True,
    )

class Publication(Item):

    implements(IPublication)

    def available_connectors(self):
        catalog = plone.api.portal.get_tool('portal_catalog')
        for uid in self.connectors:
            yield catalog(UID=uid)[0].getObject()

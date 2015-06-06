# -*- coding: utf-8 -*-

################################################################
# xmldirector.plonecore
# (C) 2014,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################

"""
A sample Dexterity content-type implementation using
all XML field types.
"""


from zope.interface import implements
from plone.dexterity.content import Item
from plone.supermodel import model

from xmldirector.plonecore.i18n import MessageFactory as _

from xmldirector.plonecore.dx import dexterity_base
from xmldirector.plonecore.dx.xml_binary import XMLBinary
from xmldirector.plonecore.dx.xml_image import XMLImage
from xmldirector.plonecore.dx.xml_field import XMLText
from xmldirector.plonecore.dx.xpath_field import XMLXPath


class IMusicXML(model.Schema):

    xml_content = XMLText(
        title=_(u'XML Content'),
        required=False
    )


class MusicXML(Item, dexterity_base.Mixin):

    implements(IMusicXML)

from Products.Five.browser import BrowserView


class MusicXMLView(BrowserView):


    def render(self):


        import os
        import tempfile

        out = tempfile.mktemp(suffix='.xml')
        pdf= tempfile.mktemp(suffix='.pdf')
        xml = self.context.xml_get('xml_content')
        open(out, 'wb').write(xml.encode('utf8'))

        cmd = 'mscore "{}" -o "{}"'.format(out, pdf)
        print cmd
        print os.system(cmd)

        pdfdata = open(pdf, 'rb').read()

        self.request.response.setHeader('content-type', 'application/pdf')
        self.request.response.setHeader('content-length', str(len(pdfdata)))
        self.request.response.write(pdfdata)

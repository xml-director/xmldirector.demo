# -*- coding: utf-8 -*-

################################################################
# xmldirector.plonecore
# (C) 2014,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################

"""
A sample Dexterity content-type implementation using
all XML field types.
"""

import os
import tempfile

from zope.interface import implements
from plone.dexterity.content import Item
from plone.supermodel import model

from xmldirector.plonecore.i18n import MessageFactory as _

from xmldirector.plonecore.dx import dexterity_base
from xmldirector.plonecore.dx.xml_binary import XMLBinary
from xmldirector.plonecore.dx.xml_image import XMLImage
from xmldirector.plonecore.dx.xml_field import XMLText
from xmldirector.plonecore.dx.xpath_field import XMLXPath

from Products.Five.browser import BrowserView


class IMusicXML(model.Schema):

    xml_content = XMLText(
        title=_(u'XML Content'),
        required=False
    )


class MusicXML(Item, dexterity_base.Mixin):

    implements(IMusicXML)



class MusicXMLView(BrowserView):

    def render(self):


        xml_out = tempfile.mktemp(suffix='.xml')
        with open(xml_out, 'wb') as fp:
            xml = self.context.xml_get('xml_content')
            fp.write(xml.encode('utf8'))

        cmd = 'mscore "{}" -o "{}"'.format(xml_out, pdf_out)
        os.system(cmd)

        pdf_out= tempfile.mktemp(suffix='.pdf')
        with open(pdf_out, 'rb') as fp
            pdfdata = fp.read()

        os.unlink(xml_out)
        os.unlink(pdf_out)

        self.request.response.setHeader('content-type', 'application/pdf')
        self.request.response.setHeader('content-length', str(len(pdfdata)))
        self.request.response.write(pdfdata)

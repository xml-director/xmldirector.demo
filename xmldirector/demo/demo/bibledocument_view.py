# -*- coding: utf-8 -*-

################################################################
# xmldirector.plonecore
# (C) 2014,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################


import lxml.etree
import lxml.html.clean
import zope.component
from Products.Five.browser import BrowserView
from xmldirector.plonecore.interfaces import IXSLTRegistry


class BibleDocument(BrowserView):

    def asHTML(self):
        """ Generate a demo PDF """
        return self.context.xml_get('xml_content')


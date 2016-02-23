################################################################
# xmldirector.plonecore
# (C) 2014,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################


import plone.api
from Products.Five.browser import BrowserView


class CREX(BrowserView):

    def new_connector(self):

        connector = plone.api.content.create(type='xmldirector.plonecore.connector', container=self.context, title=u'CREX DOCX to XML conversion')
        connector.setLayout('crex-upload-form')
        connector.plone_utils.addPortalMessage(u'Connector created')
        return self.request.response.redirect(connector.absolute_url())

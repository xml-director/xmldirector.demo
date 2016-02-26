################################################################
# xmldirector.plonecore
# (C) 2014,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################

import os
import uuid
import tempfile
from zipfile import ZipFile

import plone.api
from Products.Five.browser import BrowserView


class CREX(BrowserView):

    @property
    def handle(self):
        try:
            return self.context.get_handle(create_if_not_existing=True)
        except:
            return None

    def new_connector(self):

        connector = plone.api.content.create(type='xmldirector.plonecore.connector', container=self.context, title=u'CREX DOCX to XML conversion')
        connector.setLayout('crex-upload-form')
        connector.connector_subpath = str(uuid.uuid1())
        connector.plone_utils.addPortalMessage(u'Connector created')
        return self.request.response.redirect(connector.absolute_url())

    def have_docx(self):
        handle = self.handle
        if handle:
            return handle.exists('src/index.docx')

    def have_xml(self):
        handle = self.handle
        if handle:
            return handle.exists('result/xml/index.xml')

    def have_html(self):
        handle = self.handle
        if handle:
            return handle.exists('result/html/index.html')

    def have_dita(self):
        handle = self.handle
        if handle:
            return handle.exists('result/dita')

    def upload_docx(self):
        handle = self.handle
        docx = self.request.form['docx'].read()
        if len(docx) == 0:
            raise ValueError('No file uploaded')
        if not handle.exists('src'):
            handle.makedir('src')
        with handle.open('src/index.docx', 'wb') as fp:
            fp.write(docx)

        self.context.plone_utils.addPortalMessage(u'DOCX file uploaded and stored')
        return self.request.response.redirect(self.context.absolute_url())

    def cleanup(self):
        handle = self.handle
        if handle.exists('result'):
            handle.removedir('result', recursive=True, force=True)
        if handle.exists('src'):
            handle.removedir('src', recursive=True, force=True)
        self.context.plone_utils.addPortalMessage(u'Cleanup done')
        return self.request.response.redirect(self.context.absolute_url())

    def convert_dghodoc(self):
        return self.convert_crex(
                'https://www.c-rex.net/api/XBot/Convert//Demo.XmlDirector/XmlDirector',
                'demo@c-rex.net',
                'demo$crex'
                )

    def convert_single_topic(self):
        return self.convert_crex(
            'https://www.c-rex.net/api/XBot/Convert/Demo/docx2DITATopic',
                'demo@c-rex.net',
                'demo$crex'
            )

    def convert_split_topic(self):
        return self.convert_crex(
            'https://www.c-rex.net/api/XBot/Convert/Demo/docx2DITAMap',
                'demo@c-rex.net',
                'demo$crex'
            )

    def convert_crex(self, crex_url, crex_username, crex_password):

        from xmldirector.crex.browser.restapi import convert_crex

        zip_tmp = tempfile.mktemp(suffix='.zip')
        handle = self.handle
        with handle.open('src/index.docx', 'rb') as fp_in:
            with ZipFile(zip_tmp, 'w') as fp_out:
                fp_out.writestr('index.docx', fp_in.read())

        result_zip_fn = convert_crex(zip_tmp, crex_url, crex_username, crex_password)

        if handle.exists('result'):
            handle.removedir('result', recursive=True, force=True)

        with ZipFile(result_zip_fn, 'r') as fp_in:
            for name in fp_in.namelist():
                dirname = os.path.dirname(name).lstrip('/')
                if not handle.exists(dirname):
                    handle.makedir(dirname, recursive=True)
                with handle.open(name.lstrip('/'), 'wb') as fp_out:
                    fp_out.write(fp_in.read(name))

        self.context.plone_utils.addPortalMessage(u'Conversion results stored')
        return self.request.response.redirect(self.context.absolute_url())
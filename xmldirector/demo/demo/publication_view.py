
import fs.path
import json
import pprint

import plone.api
from zope.interface import alsoProvides
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView


KEY = 'xmldirector-content-tree'


class Publication(BrowserView):


    @property
    def src_connector(self):
        """ Returns the (first) source connector """
        catalog = plone.api.portal.get_tool('portal_catalog')
        if not self.context.src_connectors:
            return None
        uid = self.context.src_connectors[0]
        brains = catalog(UID=uid)
        if not brains:
            return None
        return brains[0].getObject()

    @property
    def target_connector(self):
        """ Returns the target connector """
        catalog = plone.api.portal.get_tool('portal_catalog')
        if not self.context.target_connector:
            return None
        uid = self.context.target_connector
        brains = catalog(UID=uid)
        if not brains:
            return None
        return brains[0].getObject()

    def connector_url(self):
        catalog = plone.api.portal.get_tool('portal_catalog')
        if not self.context.src_connectors:
            raise ValueError('No connector configured')
        uid = self.context.src_connectors[0]
        brains = catalog(UID=uid)
        if not brains:
            raise ValueError('No connector found')
        connector = brains[0].getObject()
        return connector.absolute_url()

    def load_tree(self, name='tree'):
        """ Load (json) tree from target connector """
        handle = self.target_connector.get_handle()
        handle.setContext(self.target_connector)
        fname = fs.path.join('.', name + '.json')
        with handle.open(fname, 'rb') as fp:
            data = fp.read()
        self.request.response.setHeader('content-type', 'application/json')
        return data

    def save_tree(self, name='tree'):
        """ Save (json) tree to target connector """
        alsoProvides(self.request, IDisableCSRFProtection)
        if not name:
            name = datetime.utcnow().isoformat()
        handle = self.target_connector.get_handle()
        handle.setContext(self.target_connector)
        fname = fs.path.join('.', name + '.json')
        with handle.open(fname, 'wb') as fp:
            fp.write(self.request.BODY)
        self.request.response.setStatus(200)

    def get_tree_data(self, path, mode):

        catalog = plone.api.portal.get_tool('portal_catalog')
        if not self.context.src_connectors:
            raise ValueError('No connector configured')
        uid = self.context.src_connectors[0]
        brains = catalog(UID=uid)
        if not brains:
            raise ValueError('No connector found')
        connector = brains[0].getObject()
        connector_uid = connector.UID()
        connector_url = connector.absolute_url(1)
        
        dirs = []
        files = []

        handle = connector.get_handle()
        for name, info in handle.ilistdirinfo(path, dirs_only=True):
            tooltip = u'{}, {}'.format(
                path + '/' + name,
                info['modified_time'].isoformat())
            dirs.append(dict(title=name,
                folder=True,
                lazy=True,
                tooltip=tooltip,
                extraClasses="src-node",
                modified_time=info['modified_time'].isoformat(),
                key=path + '/' + name,
                path=path + '/' + name))

        for name, info in handle.ilistdirinfo(path, files_only=True):
            tooltip = u'{}, {}, {}'.format(
                path + '/' + name,
                info['st_size'],
                info['modified_time'].isoformat())
            files.append(dict(title=name,
                folder=False,
                tooltip=tooltip,
                extraClasses="src-node",
                st_size=info['st_size'],
                connector_uid=connector_uid,
                connector_url=connector_url,
                modified_time=info['modified_time'].isoformat(),
                key=path + '/' + name,
                path=path + '/' + name))

        dirs = sorted(dirs, key=lambda d: d['title'])
        files = sorted(files, key=lambda d: d['title'])
        return json.dumps(dirs + files)

